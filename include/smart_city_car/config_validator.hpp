#pragma once

#include <filesystem>

#include "smart_city_car/status.hpp"

namespace smart_city_car {

Status ValidateRequiredFile(const std::filesystem::path& path);

}  // namespace smart_city_car
