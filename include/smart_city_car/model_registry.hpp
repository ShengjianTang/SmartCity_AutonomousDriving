#pragma once

#include <cstddef>
#include <filesystem>
#include <string>
#include <vector>

#include "smart_city_car/status.hpp"

namespace smart_city_car {

struct ModelRegistrySummary final {
    std::string registry_version;
    std::vector<std::string> model_ids;
    std::size_t reference_only_models{0};
};

Status LoadModelRegistrySummary(const std::filesystem::path& path, ModelRegistrySummary& summary);

}  // namespace smart_city_car
