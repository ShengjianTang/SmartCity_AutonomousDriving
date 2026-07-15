#pragma once

#include <chrono>
#include <cstdint>
#include <ostream>
#include <string>

#include "smart_city_car/status.hpp"

namespace smart_city_car {

enum class CommandIntent {
    kHoldPosition,
    kSafetyStop,
};

const char* ToString(CommandIntent intent) noexcept;

struct VehicleCommand final {
    std::uint64_t sequence{0};
    std::chrono::steady_clock::time_point created_at{};
    CommandIntent intent{CommandIntent::kSafetyStop};
    std::string source;
};

class VehicleTransport {
public:
    virtual ~VehicleTransport() = default;
    virtual Status Send(const VehicleCommand& command) = 0;
    [[nodiscard]] virtual bool drives_vehicle() const noexcept = 0;
};

class RecordingTransport final : public VehicleTransport {
public:
    explicit RecordingTransport(std::ostream& output) : output_(output) {}

    Status Send(const VehicleCommand& command) override {
        const auto timestamp = std::chrono::duration_cast<std::chrono::microseconds>(command.created_at.time_since_epoch()).count();
        output_ << "monotonic_us=" << timestamp << " sequence=" << command.sequence
                << " intent=" << ToString(command.intent) << " source=" << command.source
                << " drives_vehicle=false\n";
        if (!output_) {
            return Status::Error(ErrorCode::kTransportWriteFailed, "recording transport output failed");
        }
        return Status::Ok();
    }

    [[nodiscard]] bool drives_vehicle() const noexcept override { return false; }

private:
    std::ostream& output_;
};

inline const char* ToString(const CommandIntent intent) noexcept {
    switch (intent) {
        case CommandIntent::kHoldPosition: return "hold_position";
        case CommandIntent::kSafetyStop: return "safety_stop";
    }
    return "unknown_command_intent";
}

}  // namespace smart_city_car
