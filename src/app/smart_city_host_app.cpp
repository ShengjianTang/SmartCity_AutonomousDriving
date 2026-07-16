#include <atomic>
#include <csignal>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <string>
#include <thread>

#include "smart_city_car/model_registry.hpp"
#include "smart_city_car/object_detector_backend.hpp"
#include "smart_city_car/offline_config.hpp"
#include "smart_city_car/offline_replay_runner.hpp"
#include "smart_city_car/replay_camera_backend.hpp"
#include "smart_city_car/telemetry_logger.hpp"
#include "smart_city_car/vehicle_transport.hpp"

namespace {

std::atomic_bool g_stop_requested{false};

void HandleSignal(int) {
    g_stop_requested.store(true);
}

struct Arguments final {
    std::filesystem::path config;
    std::filesystem::path replay_video;
    std::filesystem::path log_output;
#ifdef SMART_CITY_DEFAULT_FFMPEG_PATH
    std::filesystem::path ffmpeg{SMART_CITY_DEFAULT_FFMPEG_PATH};
#else
    std::filesystem::path ffmpeg{"ffmpeg"};
#endif
    bool dry_run{false};
};

smart_city_car::Status ParseArguments(const int argc, char** argv, Arguments& arguments) {
    for (int index = 1; index < argc; ++index) {
        const std::string argument = argv[index];
        if (argument == "--dry-run") {
            arguments.dry_run = true;
        } else if ((argument == "--config" || argument == "--replay-video" ||
                    argument == "--log-output" || argument == "--ffmpeg") && index + 1 < argc) {
            const std::filesystem::path value = argv[++index];
            if (argument == "--config") arguments.config = value;
            else if (argument == "--replay-video") arguments.replay_video = value;
            else if (argument == "--log-output") arguments.log_output = value;
            else arguments.ffmpeg = value;
        } else {
            return smart_city_car::Status::Error(smart_city_car::ErrorCode::kInvalidArgument,
                                                  "unknown or incomplete command-line argument: " + argument);
        }
    }
    if (!arguments.dry_run) {
        return smart_city_car::Status::Error(smart_city_car::ErrorCode::kUnsupported,
                                              "--dry-run is mandatory; real vehicle output is not implemented");
    }
    if (arguments.config.empty() || arguments.replay_video.empty()) {
        return smart_city_car::Status::Error(smart_city_car::ErrorCode::kConfigurationMissing,
                                              "--config and --replay-video are required");
    }
    return smart_city_car::Status::Ok();
}

}  // namespace

int main(const int argc, char** argv) {
    using namespace smart_city_car;
    Arguments arguments;
    const Status argument_status = ParseArguments(argc, argv, arguments);
    if (!argument_status.ok()) {
        std::cerr << "error=" << ToString(argument_status.code()) << " message=" << argument_status.message() << '\n';
        return 2;
    }

    OfflineReplayConfig config;
    const Status config_status = LoadOfflineReplayConfig(arguments.config, config);
    if (!config_status.ok()) {
        std::cerr << "error=" << ToString(config_status.code()) << " message=" << config_status.message() << '\n';
        return 2;
    }
    ModelRegistrySummary registry;
    const Status registry_status = LoadModelRegistrySummary(config.model_registry_path, registry);
    if (!registry_status.ok()) {
        std::cerr << "error=" << ToString(registry_status.code()) << " message=" << registry_status.message() << '\n';
        return 2;
    }

    std::unique_ptr<std::ofstream> file_output;
    std::ostream* output = &std::cout;
    if (!arguments.log_output.empty()) {
        std::error_code directory_error;
        const auto parent = arguments.log_output.parent_path();
        if (!parent.empty()) std::filesystem::create_directories(parent, directory_error);
        if (directory_error) {
            std::cerr << "error=file_open_failed message=cannot create log output directory\n";
            return 2;
        }
        file_output = std::make_unique<std::ofstream>(arguments.log_output, std::ios::out | std::ios::trunc);
        if (!*file_output) {
            std::cerr << "error=file_open_failed message=cannot open log output\n";
            return 2;
        }
        output = file_output.get();
    }

    std::signal(SIGINT, HandleSignal);
    ReplayCameraBackend camera(arguments.replay_video, arguments.ffmpeg);
    DisabledDetectorBackend detector;
    RecordingTransport transport(*output);
    TelemetryLogger logger(*output);
    OfflineReplayRunner runner(detector, transport, logger, g_stop_requested);
    OfflineReplaySummary summary;
    Status run_status = Status::Error(ErrorCode::kInputUnavailable, "worker did not start");
    std::thread worker([&] { run_status = runner.Run(camera, config, registry, summary); });
    worker.join();

    *output << "summary frames_processed=" << summary.frames_processed
            << " safety_commands_recorded=" << summary.safety_commands_recorded
            << " end_of_stream=" << (summary.end_of_stream ? "true" : "false")
            << " manual_stop=" << (summary.manual_stop ? "true" : "false")
            << " status=" << ToString(run_status.code()) << '\n';
    output->flush();
    if (run_status.ok() || run_status.code() == ErrorCode::kManualStop) return 0;
    std::cerr << "error=" << ToString(run_status.code()) << " message=" << run_status.message() << '\n';
    return 1;
}
