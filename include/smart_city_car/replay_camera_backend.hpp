#pragma once

#include <chrono>
#include <cstdio>
#include <filesystem>
#include <functional>

#include "smart_city_car/frame.hpp"

namespace smart_city_car {

class ReplayCameraBackend final : public CameraBackend {
public:
    using Clock = std::function<std::chrono::steady_clock::time_point()>;

    ReplayCameraBackend(std::filesystem::path video_path, std::filesystem::path ffmpeg_path,
                        Clock clock = [] { return std::chrono::steady_clock::now(); });
    ~ReplayCameraBackend() override;

    ReplayCameraBackend(const ReplayCameraBackend&) = delete;
    ReplayCameraBackend& operator=(const ReplayCameraBackend&) = delete;

    Status Open() override;
    FrameResult NextFrame() override;

private:
    bool ReadToken(std::string& token);
    int ClosePipe() noexcept;

    std::filesystem::path video_path_;
    std::filesystem::path ffmpeg_path_;
    Clock clock_;
    std::FILE* pipe_{nullptr};
    std::uint64_t next_sequence_{0};
    std::chrono::steady_clock::time_point last_timestamp_{};
    bool has_timestamp_{false};
};

}  // namespace smart_city_car
