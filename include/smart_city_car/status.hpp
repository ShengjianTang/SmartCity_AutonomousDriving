#pragma once

#include <string>
#include <utility>

namespace smart_city_car {

enum class ErrorCode {
    kOk = 0,
    kUnsupported,
    kBackendUnavailable,
    kInvalidTransition,
    kConfigurationMissing,
    kFileOpenFailed,
    kFileEmpty,
    kManualStop,
    kInputUnavailable,
    kTransportWriteFailed,
    kLogWriteFailed,
    kEndOfStream,
    kInputStale,
    kInvalidArgument,
    kProcessLaunchFailed,
};

const char* ToString(ErrorCode code) noexcept;

class Status final {
public:
    static Status Ok();
    static Status Error(ErrorCode code, std::string message);

    [[nodiscard]] bool ok() const noexcept { return code_ == ErrorCode::kOk; }
    [[nodiscard]] ErrorCode code() const noexcept { return code_; }
    [[nodiscard]] const std::string& message() const noexcept { return message_; }

private:
    Status(ErrorCode code, std::string message) : code_(code), message_(std::move(message)) {}

    ErrorCode code_;
    std::string message_;
};

}  // namespace smart_city_car
