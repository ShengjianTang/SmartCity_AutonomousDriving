#pragma once

#include <string>

#include "smart_city_car/mission_state.hpp"
#include "smart_city_car/status.hpp"

namespace smart_city_car {

class MissionStateMachine final {
public:
    [[nodiscard]] MissionState state() const noexcept { return state_; }
    [[nodiscard]] const std::string& last_transition_source() const noexcept { return last_transition_source_; }

    Status TransitionTo(MissionState requested, std::string source);

private:
    static bool IsAllowed(MissionState from, MissionState to) noexcept;

    MissionState state_{MissionState::kInitialization};
    std::string last_transition_source_{"process_start"};
};

}  // namespace smart_city_car
