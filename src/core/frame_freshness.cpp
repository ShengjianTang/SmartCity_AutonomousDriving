#include "smart_city_car/frame_freshness.hpp"

namespace smart_city_car {

Status ValidateFrameFreshness(
    const Frame& frame,
    const std::chrono::steady_clock::time_point now,
    const std::optional<std::chrono::milliseconds> maximum_age) {
    if (!maximum_age.has_value()) {
        return Status::Error(ErrorCode::kConfigurationMissing,
                             "frame freshness limit is null; source_required must be resolved before motion");
    }
    if (maximum_age->count() < 0) {
        return Status::Error(ErrorCode::kInvalidArgument, "frame freshness limit must not be negative");
    }
    if (!frame.buffer || frame.buffer->bytes.empty()) {
        return Status::Error(ErrorCode::kInputUnavailable, "frame buffer is absent or empty");
    }
    if (frame.captured_at > now) {
        return Status::Error(ErrorCode::kInputStale, "frame timestamp is later than the monotonic observation time");
    }
    if (now - frame.captured_at > *maximum_age) {
        return Status::Error(ErrorCode::kInputStale, "frame age exceeds the configured evidence-backed limit");
    }
    return Status::Ok();
}

}  // namespace smart_city_car
