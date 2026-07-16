#include "smart_city_car/safety_supervisor.hpp"

namespace smart_city_car {

Status SafetySupervisor::AuthorizeMotion(const SafetyInputs& inputs) const {
    if (inputs.manual_stop_requested) {
        return Status::Error(ErrorCode::kManualStop, "manual stop requested");
    }
    if (!inputs.configuration_complete) {
        return Status::Error(ErrorCode::kConfigurationMissing, "motion denied: configuration is incomplete");
    }
    if (!inputs.camera_available) {
        return Status::Error(ErrorCode::kBackendUnavailable, "motion denied: camera backend is unavailable");
    }
    if (!inputs.freshness_limit_configured) {
        return Status::Error(ErrorCode::kConfigurationMissing, "motion denied: frame freshness limit is not configured from evidence");
    }
    if (!inputs.input_fresh) {
        return Status::Error(ErrorCode::kInputStale, "motion denied: frame input is stale or invalid");
    }
    if (inputs.detector_required && !inputs.detector_available) {
        return Status::Error(ErrorCode::kBackendUnavailable, "motion denied: required detector is unavailable");
    }
    if (!inputs.transport_available) {
        return Status::Error(ErrorCode::kBackendUnavailable, "motion denied: vehicle transport is unavailable");
    }
    return Status::Ok();
}

}  // namespace smart_city_car
