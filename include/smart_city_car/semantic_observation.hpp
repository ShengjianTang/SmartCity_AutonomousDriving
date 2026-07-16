#pragma once

#include <vector>

#include "smart_city_car/object_detector_backend.hpp"

namespace smart_city_car {

struct SemanticObservation final {
    std::uint64_t frame_sequence{0};
    Status detector_status{Status::Error(ErrorCode::kBackendUnavailable, "detector not evaluated")};
    std::vector<Detection> detections;
};

inline SemanticObservation ObserveFrame(const Frame& frame, ObjectDetectorBackend& detector) {
    SemanticObservation observation;
    observation.frame_sequence = frame.sequence;
    observation.detector_status = detector.Detect(frame, observation.detections);
    return observation;
}

}  // namespace smart_city_car
