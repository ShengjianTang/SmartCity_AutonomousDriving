#include "smart_city_car/mission_state_machine.hpp"

#include <utility>

namespace smart_city_car {
namespace {

bool IsTaskApproach(const MissionState state) noexcept {
    switch (state) {
        case MissionState::kCrosswalkApproach:
        case MissionState::kParkingApproach:
        case MissionState::kBarrierApproach:
        case MissionState::kConstructionApproach:
        case MissionState::kPedestrianApproach:
        case MissionState::kForkApproach:
            return true;
        default:
            return false;
    }
}

}  // namespace

const char* ToString(const MissionState state) noexcept {
    switch (state) {
        case MissionState::kInitialization: return "initialization";
        case MissionState::kReady: return "ready";
        case MissionState::kNormalDriving: return "normal_driving";
        case MissionState::kSpeedLimited: return "speed_limited";
        case MissionState::kCrosswalkApproach: return "crosswalk_approach";
        case MissionState::kCrosswalkWait: return "crosswalk_wait";
        case MissionState::kParkingApproach: return "parking_approach";
        case MissionState::kParkingExecute: return "parking_execute";
        case MissionState::kParkingExit: return "parking_exit";
        case MissionState::kBarrierApproach: return "barrier_approach";
        case MissionState::kBarrierWait: return "barrier_wait";
        case MissionState::kConstructionApproach: return "construction_approach";
        case MissionState::kConstructionAvoidance: return "construction_avoidance";
        case MissionState::kPedestrianApproach: return "pedestrian_approach";
        case MissionState::kPedestrianAvoidance: return "pedestrian_avoidance";
        case MissionState::kForkApproach: return "fork_approach";
        case MissionState::kForkLeft: return "fork_left";
        case MissionState::kForkRight: return "fork_right";
        case MissionState::kFinishApproach: return "finish_approach";
        case MissionState::kFinished: return "finished";
        case MissionState::kSafetyStop: return "safety_stop";
        case MissionState::kFault: return "fault";
    }
    return "unknown_mission_state";
}

Status MissionStateMachine::TransitionTo(const MissionState requested, std::string source) {
    if (source.empty()) {
        state_ = MissionState::kSafetyStop;
        last_transition_source_ = "missing_transition_source";
        return Status::Error(ErrorCode::kInvalidTransition, "transition source must not be empty");
    }
    if (!IsAllowed(state_, requested)) {
        const std::string message = std::string("transition rejected: ") + ToString(state_) + " -> " + ToString(requested);
        state_ = MissionState::kSafetyStop;
        last_transition_source_ = std::move(source);
        return Status::Error(ErrorCode::kInvalidTransition, message);
    }
    state_ = requested;
    last_transition_source_ = std::move(source);
    return Status::Ok();
}

bool MissionStateMachine::IsAllowed(const MissionState from, const MissionState to) noexcept {
    if (to == MissionState::kSafetyStop || to == MissionState::kFault) {
        return from != to;
    }
    switch (from) {
        case MissionState::kInitialization:
            return to == MissionState::kReady;
        case MissionState::kReady:
            return to == MissionState::kNormalDriving;
        case MissionState::kNormalDriving:
            return to == MissionState::kSpeedLimited || IsTaskApproach(to) || to == MissionState::kFinishApproach;
        case MissionState::kSpeedLimited:
            return to == MissionState::kNormalDriving;
        case MissionState::kCrosswalkApproach:
            return to == MissionState::kCrosswalkWait || to == MissionState::kNormalDriving;
        case MissionState::kCrosswalkWait:
            return to == MissionState::kNormalDriving;
        case MissionState::kParkingApproach:
            return to == MissionState::kParkingExecute;
        case MissionState::kParkingExecute:
            return to == MissionState::kParkingExit;
        case MissionState::kParkingExit:
            return to == MissionState::kNormalDriving;
        case MissionState::kBarrierApproach:
            return to == MissionState::kBarrierWait;
        case MissionState::kBarrierWait:
            return to == MissionState::kNormalDriving;
        case MissionState::kConstructionApproach:
            return to == MissionState::kConstructionAvoidance || to == MissionState::kNormalDriving;
        case MissionState::kConstructionAvoidance:
            return to == MissionState::kNormalDriving;
        case MissionState::kPedestrianApproach:
            return to == MissionState::kPedestrianAvoidance;
        case MissionState::kPedestrianAvoidance:
            return to == MissionState::kNormalDriving;
        case MissionState::kForkApproach:
            return to == MissionState::kForkLeft || to == MissionState::kForkRight;
        case MissionState::kForkLeft:
        case MissionState::kForkRight:
            return to == MissionState::kNormalDriving;
        case MissionState::kFinishApproach:
            return to == MissionState::kFinished;
        case MissionState::kFinished:
        case MissionState::kSafetyStop:
        case MissionState::kFault:
            return to == MissionState::kInitialization;
    }
    return false;
}

}  // namespace smart_city_car
