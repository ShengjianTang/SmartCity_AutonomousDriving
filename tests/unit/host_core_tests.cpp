#include <atomic>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <optional>
#include <sstream>
#include <string>
#include <vector>

#include "smart_city_car/config_validator.hpp"
#include "smart_city_car/frame.hpp"
#include "smart_city_car/frame_freshness.hpp"
#include "smart_city_car/mission_state_machine.hpp"
#include "smart_city_car/model_registry.hpp"
#include "smart_city_car/object_detector_backend.hpp"
#include "smart_city_car/offline_config.hpp"
#include "smart_city_car/offline_replay_runner.hpp"
#include "smart_city_car/replay_camera_backend.hpp"
#include "smart_city_car/safety_supervisor.hpp"
#include "smart_city_car/telemetry_logger.hpp"
#include "smart_city_car/vehicle_transport.hpp"

namespace {

class TestContext final {
public:
    void Expect(const bool condition, const std::string& message) {
        if (!condition) {
            ++failures_;
            std::cerr << "FAIL: " << message << '\n';
        }
    }

    [[nodiscard]] int failures() const noexcept { return failures_; }

private:
    int failures_{0};
};

std::shared_ptr<const smart_city_car::FrameBuffer> MakeTestBuffer() {
    auto buffer = std::make_shared<smart_city_car::FrameBuffer>();
    buffer->format = "SYNTHETIC_TEST_FIXTURE_RGB8";
    buffer->width = 1;
    buffer->height = 1;
    buffer->bytes = {std::byte{0}, std::byte{0}, std::byte{0}};
    return buffer;
}

class FiniteTestCamera final : public smart_city_car::CameraBackend {
public:
    explicit FiniteTestCamera(const std::size_t frame_count) : frame_count_(frame_count) {}

    smart_city_car::Status Open() override {
        opened_ = true;
        return smart_city_car::Status::Ok();
    }

    smart_city_car::FrameResult NextFrame() override {
        using namespace smart_city_car;
        if (!opened_) return {Status::Error(ErrorCode::kBackendUnavailable, "test camera not open"), nullptr};
        if (next_ >= frame_count_) return {Status::Error(ErrorCode::kEndOfStream, "synthetic EOF"), nullptr};
        auto frame = std::make_unique<Frame>();
        frame->sequence = next_++;
        frame->captured_at = std::chrono::steady_clock::now();
        frame->source = "SYNTHETIC_TEST_FIXTURE";
        frame->buffer = MakeTestBuffer();
        return {Status::Ok(), std::move(frame)};
    }

private:
    std::size_t frame_count_{0};
    std::size_t next_{0};
    bool opened_{false};
};

void WriteSyntheticY4m(const std::filesystem::path& path) {
    std::ofstream output(path, std::ios::binary | std::ios::trunc);
    output << "YUV4MPEG2 W2 H2 F1:1 Ip A1:1 C420jpeg\n";
    const char pixels[6] = {static_cast<char>(16), static_cast<char>(32), static_cast<char>(48),
                            static_cast<char>(64), static_cast<char>(128), static_cast<char>(128)};
    output << "FRAME\n";
    output.write(pixels, sizeof(pixels));
    output << "FRAME\n";
    output.write(pixels, sizeof(pixels));
}

}  // namespace

int main() {
    using namespace smart_city_car;
    TestContext test;

    MissionStateMachine machine;
    test.Expect(machine.TransitionTo(MissionState::kReady, "configuration_validated").ok(), "initialization to ready");
    test.Expect(machine.TransitionTo(MissionState::kNormalDriving, "operator_start_authorized").ok(), "ready to normal driving");
    const Status invalid = machine.TransitionTo(MissionState::kFinished, "invalid_test_transition");
    test.Expect(!invalid.ok() && invalid.code() == ErrorCode::kInvalidTransition, "invalid transition is rejected");
    test.Expect(machine.state() == MissionState::kSafetyStop, "invalid transition enters safety stop");

    SafetySupervisor safety;
    SafetyInputs unavailable;
    const Status denied = safety.AuthorizeMotion(unavailable);
    test.Expect(!denied.ok() && denied.code() == ErrorCode::kConfigurationMissing, "incomplete configuration denies motion");

    SafetyInputs stale_input;
    stale_input.configuration_complete = true;
    stale_input.camera_available = true;
    stale_input.freshness_limit_configured = true;
    stale_input.input_fresh = false;
    stale_input.transport_available = true;
    test.Expect(safety.AuthorizeMotion(stale_input).code() == ErrorCode::kInputStale,
                "stale input explicitly denies motion");

    UnavailableCameraBackend camera;
    test.Expect(camera.Open().code() == ErrorCode::kBackendUnavailable, "unconfigured camera explicitly fails");

    DisabledDetectorBackend detector;
    Frame frame;
    std::vector<Detection> detections{{"preexisting_test_value", 1.0, 0, 0, 1, 1}};
    const Status detector_status = detector.Detect(frame, detections);
    test.Expect(detector_status.code() == ErrorCode::kBackendUnavailable, "disabled detector explicitly fails");
    test.Expect(detections.empty(), "disabled detector returns no fabricated result");

    std::ostringstream command_output;
    RecordingTransport transport(command_output);
    VehicleCommand command{1, std::chrono::steady_clock::now(), CommandIntent::kSafetyStop, "unit_test"};
    test.Expect(transport.Send(command).ok(), "recording transport records command");
    test.Expect(!transport.drives_vehicle(), "recording transport declares no vehicle actuation");
    test.Expect(command_output.str().find("drives_vehicle=false") != std::string::npos, "record contains actuation disclaimer");

    std::ostringstream log_output;
    TelemetryLogger logger(log_output);
    const LogRecord record{std::chrono::steady_clock::now(), MissionState::kSafetyStop,
                           ErrorCode::kManualStop, "unit_test", "manual stop semantics"};
    test.Expect(logger.Write(record).ok(), "structured log write succeeds");
    test.Expect(log_output.str().find("state=safety_stop") != std::string::npos, "log contains state");
    test.Expect(log_output.str().find("error=manual_stop") != std::string::npos, "log contains error code");

    const auto absent = std::filesystem::path("file_that_must_not_exist_for_test.yaml");
    test.Expect(ValidateRequiredFile(absent).code() == ErrorCode::kConfigurationMissing,
                "missing required file is rejected");

    OfflineReplayConfig missing_config;
    test.Expect(LoadOfflineReplayConfig(absent, missing_config).code() == ErrorCode::kConfigurationMissing,
                "missing offline configuration is rejected");

    Frame freshness_frame;
    freshness_frame.captured_at = std::chrono::steady_clock::now() - std::chrono::milliseconds(10);
    freshness_frame.buffer = MakeTestBuffer();
    test.Expect(ValidateFrameFreshness(freshness_frame, std::chrono::steady_clock::now(), std::nullopt).code() ==
                    ErrorCode::kConfigurationMissing,
                "null production freshness limit explicitly blocks validation");
    test.Expect(ValidateFrameFreshness(freshness_frame, std::chrono::steady_clock::now(),
                                       std::chrono::milliseconds(1)).code() == ErrorCode::kInputStale,
                "test-fixture stale frame is rejected");
    test.Expect(ValidateFrameFreshness(freshness_frame, std::chrono::steady_clock::now(),
                                       std::chrono::milliseconds(100)).ok(),
                "test-fixture frame inside explicit test limit is accepted");

    const std::filesystem::path test_directory = std::filesystem::current_path() / "synthetic_test_fixtures";
    std::filesystem::create_directories(test_directory);
    const auto registry_path = test_directory / "registry.yaml";
    {
        std::ofstream registry_file(registry_path, std::ios::trunc);
        registry_file << "registry_version: 1\nmodels:\n- model_id: synthetic_registry_entry\n"
                         "  validation_status: REFERENCE_ONLY\n";
    }
    ModelRegistrySummary registry;
    test.Expect(LoadModelRegistrySummary(registry_path, registry).ok(), "reference-only model registry loads");
    test.Expect(registry.model_ids.size() == 1U && registry.reference_only_models == 1U,
                "model registry summary preserves reference-only status");

    const auto config_path = test_directory / "offline.yaml";
    {
        std::ofstream config_file(config_path, std::ios::trunc);
        config_file << "schema_version: 1\nmode: offline_replay\ndry_run_required: true\n"
                       "detector_required: true\nmotion_configuration_complete: false\n"
                       "maximum_frame_age_ms: null\nmodel_registry_path: registry.yaml\n";
    }
    OfflineReplayConfig parsed_config;
    test.Expect(LoadOfflineReplayConfig(config_path, parsed_config).ok(), "offline replay configuration loads");
    test.Expect(!parsed_config.maximum_frame_age.has_value(), "unknown production freshness remains null");

    FiniteTestCamera finite_camera(1U);
    std::atomic_bool no_stop{false};
    std::ostringstream replay_log;
    RecordingTransport replay_transport(replay_log);
    TelemetryLogger replay_logger(replay_log);
    DisabledDetectorBackend replay_detector;
    OfflineReplayRunner runner(replay_detector, replay_transport, replay_logger, no_stop);
    OfflineReplaySummary replay_summary;
    const Status replay_status = runner.Run(finite_camera, parsed_config, registry, replay_summary);
    test.Expect(replay_status.ok(), "finite offline replay exits normally at EOF");
    test.Expect(replay_summary.frames_processed == 1U && replay_summary.end_of_stream,
                "offline replay reports processed frame and EOF");
    test.Expect(replay_summary.safety_commands_recorded == 1U,
                "unconfigured motion records exactly one safety command for one frame");
    test.Expect(replay_log.str().find("drives_vehicle=false") != std::string::npos,
                "offline runner stays on recording-only transport");

    FiniteTestCamera stopped_camera(1U);
    std::atomic_bool stop{true};
    std::ostringstream stop_log;
    RecordingTransport stop_transport(stop_log);
    TelemetryLogger stop_logger(stop_log);
    OfflineReplayRunner stopped_runner(replay_detector, stop_transport, stop_logger, stop);
    OfflineReplaySummary stopped_summary;
    const Status stopped_status = stopped_runner.Run(stopped_camera, parsed_config, registry, stopped_summary);
    test.Expect(stopped_status.code() == ErrorCode::kManualStop && stopped_summary.manual_stop,
                "manual stop terminates replay with explicit safe status");
    test.Expect(stopped_summary.safety_commands_recorded == 1U,
                "manual stop records a safety command without vehicle actuation");

#ifdef SMART_CITY_TEST_FFMPEG_PATH
    const auto video_path = test_directory / "SYNTHETIC_TEST_FIXTURE.y4m";
    WriteSyntheticY4m(video_path);
    const auto fixed_time = std::chrono::steady_clock::now();
    ReplayCameraBackend replay_camera(video_path, SMART_CITY_TEST_FFMPEG_PATH, [fixed_time] { return fixed_time; });
    test.Expect(replay_camera.Open().ok(), "ffmpeg replay camera opens synthetic video fixture");
    FrameResult first = replay_camera.NextFrame();
    FrameResult second = replay_camera.NextFrame();
    FrameResult eof = replay_camera.NextFrame();
    test.Expect(first.status.ok() && second.status.ok(), "ffmpeg replay camera decodes two fixture frames");
    test.Expect(first.frame && second.frame && first.frame->buffer->width == 2U && first.frame->buffer->height == 2U,
                "decoded replay frame dimensions are preserved");
    test.Expect(first.frame && second.frame && second.frame->sequence == first.frame->sequence + 1U,
                "replay frame sequence strictly increases");
    test.Expect(first.frame && second.frame && second.frame->captured_at > first.frame->captured_at,
                "replay timestamps strictly increase even when clock values repeat");
    test.Expect(eof.status.code() == ErrorCode::kEndOfStream, "replay camera reports explicit EOF");

    ReplayCameraBackend missing_video(absent, SMART_CITY_TEST_FFMPEG_PATH);
    test.Expect(missing_video.Open().code() == ErrorCode::kConfigurationMissing,
                "missing replay video is rejected before decoder launch");
#else
    std::cout << "SKIP: ffmpeg replay integration test (ffmpeg not found at configure time)\n";
#endif

    std::error_code cleanup_error;
    std::filesystem::remove_all(test_directory, cleanup_error);
    test.Expect(!cleanup_error, "synthetic test fixtures clean up successfully");

    if (test.failures() == 0) {
        std::cout << "host_core_tests: all checks passed\n";
        return 0;
    }
    std::cerr << "host_core_tests: " << test.failures() << " check(s) failed\n";
    return 1;
}
