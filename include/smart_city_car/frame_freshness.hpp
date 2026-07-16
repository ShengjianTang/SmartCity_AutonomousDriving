#pragma once

#include <chrono>
#include <optional>

#include "smart_city_car/frame.hpp"
#include "smart_city_car/status.hpp"

namespace smart_city_car {

Status ValidateFrameFreshness(
    const Frame& frame,
    std::chrono::steady_clock::time_point now,
    std::optional<std::chrono::milliseconds> maximum_age);

}  // namespace smart_city_car
