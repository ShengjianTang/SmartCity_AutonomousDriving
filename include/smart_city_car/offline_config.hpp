#pragma once

#include <chrono>
#include <filesystem>
#include <optional>

#include "smart_city_car/status.hpp"

namespace smart_city_car {

struct OfflineReplayConfig final {
    bool dry_run_required{true};
    bool detector_required{true};
    bool motion_configuration_complete{false};
    std::optional<std::chrono::milliseconds> maximum_frame_age;
    std::filesystem::path model_registry_path;
};

Status LoadOfflineReplayConfig(const std::filesystem::path& path, OfflineReplayConfig& config);

}  // namespace smart_city_car
