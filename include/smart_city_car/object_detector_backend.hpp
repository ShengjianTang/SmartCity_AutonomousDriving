#pragma once

#include <string>
#include <vector>

#include "smart_city_car/frame.hpp"
#include "smart_city_car/status.hpp"

namespace smart_city_car {

struct Detection final {
    std::string label;
    double confidence{0.0};
    int x{0};
    int y{0};
    int width{0};
    int height{0};
};

class ObjectDetectorBackend {
public:
    virtual ~ObjectDetectorBackend() = default;
    virtual Status Detect(const Frame& frame, std::vector<Detection>& detections) = 0;
};

class DisabledDetectorBackend final : public ObjectDetectorBackend {
public:
    Status Detect(const Frame&, std::vector<Detection>& detections) override {
        detections.clear();
        return Status::Error(ErrorCode::kBackendUnavailable, "object detector is not configured");
    }
};

}  // namespace smart_city_car
