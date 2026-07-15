#pragma once

namespace smart_city_car {

enum class MissionState {
    kInitialization,
    kReady,
    kNormalDriving,
    kSpeedLimited,
    kCrosswalkApproach,
    kCrosswalkWait,
    kParkingApproach,
    kParkingExecute,
    kParkingExit,
    kBarrierApproach,
    kBarrierWait,
    kConstructionApproach,
    kConstructionAvoidance,
    kPedestrianApproach,
    kPedestrianAvoidance,
    kForkApproach,
    kForkLeft,
    kForkRight,
    kFinishApproach,
    kFinished,
    kSafetyStop,
    kFault,
};

const char* ToString(MissionState state) noexcept;

}  // namespace smart_city_car
