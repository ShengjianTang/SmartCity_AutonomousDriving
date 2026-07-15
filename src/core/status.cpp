#include "smart_city_car/status.hpp"

namespace smart_city_car {

const char* ToString(const ErrorCode code) noexcept {
    switch (code) {
        case ErrorCode::kOk: return "ok";
        case ErrorCode::kUnsupported: return "unsupported";
        case ErrorCode::kBackendUnavailable: return "backend_unavailable";
        case ErrorCode::kInvalidTransition: return "invalid_transition";
        case ErrorCode::kConfigurationMissing: return "configuration_missing";
        case ErrorCode::kFileOpenFailed: return "file_open_failed";
        case ErrorCode::kFileEmpty: return "file_empty";
        case ErrorCode::kManualStop: return "manual_stop";
        case ErrorCode::kInputUnavailable: return "input_unavailable";
        case ErrorCode::kTransportWriteFailed: return "transport_write_failed";
        case ErrorCode::kLogWriteFailed: return "log_write_failed";
    }
    return "unknown_error_code";
}

Status Status::Ok() {
    return Status(ErrorCode::kOk, {});
}

Status Status::Error(const ErrorCode code, std::string message) {
    return Status(code, std::move(message));
}

}  // namespace smart_city_car
