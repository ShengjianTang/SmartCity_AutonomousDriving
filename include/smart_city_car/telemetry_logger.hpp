#pragma once

#include <chrono>
#include <ostream>
#include <string>

#include "smart_city_car/mission_state.hpp"
#include "smart_city_car/status.hpp"

namespace smart_city_car {

struct LogRecord final {
    std::chrono::steady_clock::time_point timestamp{};
    MissionState state{MissionState::kInitialization};
    ErrorCode error{ErrorCode::kOk};
    std::string source;
    std::string message;
};

class TelemetryLogger final {
public:
    explicit TelemetryLogger(std::ostream& output) : output_(output) {}
    Status Write(const LogRecord& record);

private:
    std::ostream& output_;
};

}  // namespace smart_city_car
