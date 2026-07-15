#include "smart_city_car/config_validator.hpp"

#include <fstream>
#include <system_error>

namespace smart_city_car {

Status ValidateRequiredFile(const std::filesystem::path& path) {
    if (path.empty()) {
        return Status::Error(ErrorCode::kConfigurationMissing, "required file path is empty");
    }
    std::error_code error;
    const bool exists = std::filesystem::exists(path, error);
    if (error || !exists) {
        return Status::Error(ErrorCode::kConfigurationMissing, "required file does not exist: " + path.string());
    }
    if (!std::filesystem::is_regular_file(path, error) || error) {
        return Status::Error(ErrorCode::kFileOpenFailed, "required path is not a regular file: " + path.string());
    }
    const auto size = std::filesystem::file_size(path, error);
    if (error) {
        return Status::Error(ErrorCode::kFileOpenFailed, "cannot inspect required file: " + path.string());
    }
    if (size == 0U) {
        return Status::Error(ErrorCode::kFileEmpty, "required file is empty: " + path.string());
    }
    std::ifstream stream(path, std::ios::binary);
    if (!stream) {
        return Status::Error(ErrorCode::kFileOpenFailed, "cannot open required file: " + path.string());
    }
    return Status::Ok();
}

}  // namespace smart_city_car
