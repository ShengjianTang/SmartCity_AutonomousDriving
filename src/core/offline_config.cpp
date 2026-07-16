#include "smart_city_car/offline_config.hpp"

#include <algorithm>
#include <cctype>
#include <fstream>
#include <limits>
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

Status ParseBoolean(const std::string& text, const char* key, bool& value) {
    if (text == "true") {
        value = true;
        return Status::Ok();
    }
    if (text == "false") {
        value = false;
        return Status::Ok();
    }
    return Status::Error(ErrorCode::kInvalidArgument, std::string("invalid boolean for ") + key);
}

}  // namespace

Status LoadOfflineReplayConfig(const std::filesystem::path& path, OfflineReplayConfig& config) {
    const Status required = ValidateRequiredFile(path);
    if (!required.ok()) {
        return required;
    }
    std::ifstream input(path);
    if (!input) {
        return Status::Error(ErrorCode::kFileOpenFailed, "cannot open offline replay configuration: " + path.string());
    }

    OfflineReplayConfig parsed;
    bool saw_mode = false;
    bool saw_dry_run = false;
    bool saw_detector = false;
    bool saw_motion = false;
    bool saw_freshness = false;
    bool saw_registry = false;
    std::string line;
    while (std::getline(input, line)) {
        const auto comment = line.find('#');
        if (comment != std::string::npos) {
            line.erase(comment);
        }
        line = Trim(std::move(line));
        if (line.empty()) {
            continue;
        }
        const auto delimiter = line.find(':');
        if (delimiter == std::string::npos) {
            return Status::Error(ErrorCode::kInvalidArgument, "configuration line has no key delimiter");
        }
        const std::string key = Trim(line.substr(0, delimiter));
        std::string value = Trim(line.substr(delimiter + 1));
        if (value.size() >= 2U && value.front() == '"' && value.back() == '"') {
            value = value.substr(1, value.size() - 2U);
        }
        if (key == "mode") {
            if (value != "offline_replay") {
                return Status::Error(ErrorCode::kUnsupported, "only mode=offline_replay is supported");
            }
            saw_mode = true;
        } else if (key == "dry_run_required") {
            const Status status = ParseBoolean(value, "dry_run_required", parsed.dry_run_required);
            if (!status.ok()) return status;
            saw_dry_run = true;
        } else if (key == "detector_required") {
            const Status status = ParseBoolean(value, "detector_required", parsed.detector_required);
            if (!status.ok()) return status;
            saw_detector = true;
        } else if (key == "motion_configuration_complete") {
            const Status status = ParseBoolean(value, "motion_configuration_complete", parsed.motion_configuration_complete);
            if (!status.ok()) return status;
            saw_motion = true;
        } else if (key == "maximum_frame_age_ms") {
            saw_freshness = true;
            if (value == "null") {
                parsed.maximum_frame_age.reset();
            } else {
                try {
                    const long long count = std::stoll(value);
                    if (count < 0 || count > std::numeric_limits<int>::max()) {
                        return Status::Error(ErrorCode::kInvalidArgument, "maximum_frame_age_ms is out of range");
                    }
                    parsed.maximum_frame_age = std::chrono::milliseconds(count);
                } catch (const std::exception&) {
                    return Status::Error(ErrorCode::kInvalidArgument, "maximum_frame_age_ms must be null or an integer");
                }
            }
        } else if (key == "model_registry_path") {
            if (value.empty() || value == "null") {
                return Status::Error(ErrorCode::kConfigurationMissing, "model_registry_path is required");
            }
            parsed.model_registry_path = path.parent_path() / std::filesystem::path(value);
            saw_registry = true;
        }
    }
    if (!saw_mode || !saw_dry_run || !saw_detector || !saw_motion || !saw_freshness || !saw_registry) {
        return Status::Error(ErrorCode::kConfigurationMissing, "offline replay configuration is missing one or more required keys");
    }
    if (!parsed.dry_run_required) {
        return Status::Error(ErrorCode::kUnsupported, "dry_run_required=false is prohibited by this host application");
    }
    config = std::move(parsed);
    return Status::Ok();
}

}  // namespace smart_city_car
