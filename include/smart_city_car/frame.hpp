#pragma once

#include <chrono>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "smart_city_car/status.hpp"

namespace smart_city_car {

struct FrameBuffer final {
    std::vector<std::byte> bytes;
    std::string format;
    std::size_t width{0};
    std::size_t height{0};
};

struct Frame final {
    std::uint64_t sequence{0};
    std::chrono::steady_clock::time_point captured_at{};
    std::string source;
    std::shared_ptr<const FrameBuffer> buffer;
};

struct FrameResult final {
    Status status{Status::Error(ErrorCode::kInputUnavailable, "no frame")};
    std::unique_ptr<Frame> frame;
};

class CameraBackend {
public:
    virtual ~CameraBackend() = default;
    virtual Status Open() = 0;
    virtual FrameResult NextFrame() = 0;
};

class UnavailableCameraBackend final : public CameraBackend {
public:
    Status Open() override {
        return Status::Error(ErrorCode::kBackendUnavailable, "camera backend is not configured");
    }

    FrameResult NextFrame() override {
        return {Status::Error(ErrorCode::kBackendUnavailable, "camera backend is not configured"), nullptr};
    }
};

}  // namespace smart_city_car
