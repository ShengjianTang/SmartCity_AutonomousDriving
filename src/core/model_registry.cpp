#include "smart_city_car/model_registry.hpp"

#include <algorithm>
#include <cctype>
#include <fstream>
#include <string>

#include "smart_city_car/config_validator.hpp"

namespace smart_city_car {
namespace {

std::string Trim(std::string text) {
    const auto not_space = [](const unsigned char value) { return std::isspace(value) == 0; };
    text.erase(text.begin(), std::find_if(text.begin(), text.end(), not_space));
    text.erase(std::find_if(text.rbegin(), text.rend(), not_space).base(), text.end());
    return text;
}

std::string ValueAfterColon(const std::string& line) {
    const auto delimiter = line.find(':');
    return delimiter == std::string::npos ? std::string{} : Trim(line.substr(delimiter + 1));
}

}  // namespace

Status LoadModelRegistrySummary(const std::filesystem::path& path, ModelRegistrySummary& summary) {
    const Status required = ValidateRequiredFile(path);
    if (!required.ok()) {
        return required;
    }
    std::ifstream input(path);
    if (!input) {
        return Status::Error(ErrorCode::kFileOpenFailed, "cannot open model registry: " + path.string());
    }
    ModelRegistrySummary parsed;
    std::string line;
    while (std::getline(input, line)) {
        const std::string trimmed = Trim(line);
        if (trimmed.rfind("registry_version:", 0U) == 0U) {
            parsed.registry_version = ValueAfterColon(trimmed);
        } else if (trimmed.rfind("- model_id:", 0U) == 0U) {
            const std::string id = ValueAfterColon(trimmed);
            if (id.empty()) {
                return Status::Error(ErrorCode::kInvalidArgument, "model registry contains an empty model_id");
            }
            parsed.model_ids.push_back(id);
        } else if (trimmed.rfind("validation_status:", 0U) == 0U &&
                   ValueAfterColon(trimmed) == "REFERENCE_ONLY") {
            ++parsed.reference_only_models;
        }
    }
    if (parsed.registry_version.empty() || parsed.model_ids.empty()) {
        return Status::Error(ErrorCode::kInvalidArgument, "model registry has no version or registered models");
    }
    if (parsed.reference_only_models != parsed.model_ids.size()) {
        return Status::Error(ErrorCode::kUnsupported,
                             "offline application accepts only explicitly REFERENCE_ONLY organizer models");
    }
    summary = std::move(parsed);
    return Status::Ok();
}

}  // namespace smart_city_car
