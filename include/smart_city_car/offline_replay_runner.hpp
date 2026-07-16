#pragma once

#include <atomic>
#include <cstdint>

#include "smart_city_car/frame.hpp"
#include "smart_city_car/model_registry.hpp"
#include "smart_city_car/object_detector_backend.hpp"
#include "smart_city_car/offline_config.hpp"
#include "smart_city_car/status.hpp"
#include "smart_city_car/telemetry_logger.hpp"
#include "smart_city_car/vehicle_transport.hpp"

namespace smart_city_car {

struct OfflineReplaySummary final {
    std::uint64_t frames_processed{0};
    std::uint64_t safety_commands_recorded{0};
    bool end_of_stream{false};
    bool manual_stop{false};
};

class OfflineReplayRunner final {
public:
    OfflineReplayRunner(ObjectDetectorBackend& detector, VehicleTransport& transport,
                        TelemetryLogger& logger, std::atomic_bool& stop_requested)
        : detector_(detector), transport_(transport), logger_(logger), stop_requested_(stop_requested) {}

    Status Run(CameraBackend& camera, const OfflineReplayConfig& config,
               const ModelRegistrySummary& registry, OfflineReplaySummary& summary);

private:
    Status RecordSafetyStop(std::uint64_t sequence, const Status& reason, OfflineReplaySummary& summary);

    ObjectDetectorBackend& detector_;
    VehicleTransport& transport_;
    TelemetryLogger& logger_;
    std::atomic_bool& stop_requested_;
};

}  // namespace smart_city_car
