#include "smart_city_car/telemetry_logger.hpp"

namespace smart_city_car {

Status TelemetryLogger::Write(const LogRecord& record) {
    if (record.source.empty()) {
        return Status::Error(ErrorCode::kLogWriteFailed, "log source must not be empty");
    }
    const auto timestamp = std::chrono::duration_cast<std::chrono::microseconds>(record.timestamp.time_since_epoch()).count();
    output_ << "monotonic_us=" << timestamp << " state=" << ToString(record.state)
            << " error=" << ToString(record.error) << " source=" << record.source
            << " message=" << record.message << '\n';
    if (!output_) {
        return Status::Error(ErrorCode::kLogWriteFailed, "telemetry output failed");
    }
    return Status::Ok();
}

}  // namespace smart_city_car
