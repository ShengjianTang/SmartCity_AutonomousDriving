#include "smart_city_car/offline_replay_runner.hpp"

#include <chrono>

#include "smart_city_car/frame_freshness.hpp"
#include "smart_city_car/mission_state_machine.hpp"
#include "smart_city_car/safety_supervisor.hpp"
#include "smart_city_car/semantic_observation.hpp"

namespace smart_city_car {

Status OfflineReplayRunner::RecordSafetyStop(const std::uint64_t sequence, const Status& reason,
                                             OfflineReplaySummary& summary) {
    const auto now = std::chrono::steady_clock::now();
    const VehicleCommand command{sequence, now, CommandIntent::kSafetyStop, "offline_replay_safety_supervisor"};
    const Status send_status = transport_.Send(command);
    if (!send_status.ok()) return send_status;
    ++summary.safety_commands_recorded;
    return logger_.Write({now, MissionState::kSafetyStop, reason.code(), "offline_replay_safety_supervisor", reason.message()});
}

Status OfflineReplayRunner::Run(CameraBackend& camera, const OfflineReplayConfig& config,
                                const ModelRegistrySummary& registry, OfflineReplaySummary& summary) {
    summary = OfflineReplaySummary{};
    if (!config.dry_run_required) {
        return Status::Error(ErrorCode::kUnsupported, "offline runner rejects dry_run_required=false");
    }
    if (registry.model_ids.empty()) {
        return Status::Error(ErrorCode::kConfigurationMissing, "model registry summary is empty");
    }
    const Status open_status = camera.Open();
    if (!open_status.ok()) return open_status;

    MissionStateMachine state_machine;
    const Status ready = state_machine.TransitionTo(MissionState::kReady, "offline_configuration_validated");
    if (!ready.ok()) return ready;
    const auto start = std::chrono::steady_clock::now();
    const Status start_log = logger_.Write({start, state_machine.state(), ErrorCode::kOk,
                                            "offline_replay", "dry_run=true vehicle_transport=recording_only"});
    if (!start_log.ok()) return start_log;

    SafetySupervisor safety;
    for (;;) {
        if (stop_requested_.load()) {
            summary.manual_stop = true;
            if (state_machine.state() != MissionState::kSafetyStop) {
                state_machine.TransitionTo(MissionState::kSafetyStop, "manual_stop");
            }
            const Status reason = Status::Error(ErrorCode::kManualStop, "manual stop requested");
            const Status recorded = RecordSafetyStop(summary.frames_processed, reason, summary);
            return recorded.ok() ? reason : recorded;
        }

        FrameResult result = camera.NextFrame();
        if (result.status.code() == ErrorCode::kEndOfStream) {
            summary.end_of_stream = true;
            return logger_.Write({std::chrono::steady_clock::now(), state_machine.state(), ErrorCode::kEndOfStream,
                                  "offline_replay", "normal replay end_of_stream"});
        }
        if (!result.status.ok() || !result.frame) {
            const Status reason = result.status.ok()
                ? Status::Error(ErrorCode::kInputUnavailable, "camera returned no frame")
                : result.status;
            if (state_machine.state() != MissionState::kSafetyStop) {
                state_machine.TransitionTo(MissionState::kSafetyStop, "camera_failure");
            }
            const Status recorded = RecordSafetyStop(summary.frames_processed, reason, summary);
            return recorded.ok() ? reason : recorded;
        }

        ++summary.frames_processed;
        const Status freshness = ValidateFrameFreshness(*result.frame, std::chrono::steady_clock::now(),
                                                        config.maximum_frame_age);
        const SemanticObservation observation = ObserveFrame(*result.frame, detector_);
        const SafetyInputs inputs{
            config.motion_configuration_complete,
            true,
            config.detector_required,
            observation.detector_status.ok(),
            config.maximum_frame_age.has_value(),
            freshness.ok(),
            transport_.drives_vehicle(),
            false,
        };
        const Status authorization = safety.AuthorizeMotion(inputs);
        if (!authorization.ok()) {
            if (state_machine.state() != MissionState::kSafetyStop) {
                state_machine.TransitionTo(MissionState::kSafetyStop, "motion_authorization_denied");
            }
            const Status recorded = RecordSafetyStop(result.frame->sequence, authorization, summary);
            if (!recorded.ok()) return recorded;
        } else {
            return Status::Error(ErrorCode::kUnsupported,
                                 "motion authorization unexpectedly succeeded in recording-only offline mode");
        }
    }
}

}  // namespace smart_city_car
