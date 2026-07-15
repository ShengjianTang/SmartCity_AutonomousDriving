#include <chrono>
#include <filesystem>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "smart_city_car/config_validator.hpp"
#include "smart_city_car/frame.hpp"
#include "smart_city_car/mission_state_machine.hpp"
#include "smart_city_car/object_detector_backend.hpp"
#include "smart_city_car/safety_supervisor.hpp"
#include "smart_city_car/telemetry_logger.hpp"
#include "smart_city_car/vehicle_transport.hpp"

namespace {

class TestContext final {
public:
    void Expect(const bool condition, const std::string& message) {
        if (!condition) {
            ++failures_;
            std::cerr << "FAIL: " << message << '\n';
        }
    }

    [[nodiscard]] int failures() const noexcept { return failures_; }

private:
    int failures_{0};
};

}  // namespace

int main() {
    using namespace smart_city_car;
    TestContext test;

    MissionStateMachine machine;
    test.Expect(machine.TransitionTo(MissionState::kReady, "configuration_validated").ok(), "initialization to ready");
    test.Expect(machine.TransitionTo(MissionState::kNormalDriving, "operator_start_authorized").ok(), "ready to normal driving");
    const Status invalid = machine.TransitionTo(MissionState::kFinished, "invalid_test_transition");
    test.Expect(!invalid.ok() && invalid.code() == ErrorCode::kInvalidTransition, "invalid transition is rejected");
    test.Expect(machine.state() == MissionState::kSafetyStop, "invalid transition enters safety stop");

    SafetySupervisor safety;
    SafetyInputs unavailable;
    const Status denied = safety.AuthorizeMotion(unavailable);
    test.Expect(!denied.ok() && denied.code() == ErrorCode::kConfigurationMissing, "incomplete configuration denies motion");

    UnavailableCameraBackend camera;
    test.Expect(camera.Open().code() == ErrorCode::kBackendUnavailable, "unconfigured camera explicitly fails");

    DisabledDetectorBackend detector;
    Frame frame;
    std::vector<Detection> detections{{"preexisting_test_value", 1.0, 0, 0, 1, 1}};
    const Status detector_status = detector.Detect(frame, detections);
    test.Expect(detector_status.code() == ErrorCode::kBackendUnavailable, "disabled detector explicitly fails");
    test.Expect(detections.empty(), "disabled detector returns no fabricated result");

    std::ostringstream command_output;
    RecordingTransport transport(command_output);
    VehicleCommand command{1, std::chrono::steady_clock::now(), CommandIntent::kSafetyStop, "unit_test"};
    test.Expect(transport.Send(command).ok(), "recording transport records command");
    test.Expect(!transport.drives_vehicle(), "recording transport declares no vehicle actuation");
    test.Expect(command_output.str().find("drives_vehicle=false") != std::string::npos, "record contains actuation disclaimer");

    std::ostringstream log_output;
    TelemetryLogger logger(log_output);
    const LogRecord record{std::chrono::steady_clock::now(), MissionState::kSafetyStop,
                           ErrorCode::kManualStop, "unit_test", "manual stop semantics"};
    test.Expect(logger.Write(record).ok(), "structured log write succeeds");
    test.Expect(log_output.str().find("state=safety_stop") != std::string::npos, "log contains state");
    test.Expect(log_output.str().find("error=manual_stop") != std::string::npos, "log contains error code");

    const auto absent = std::filesystem::path("file_that_must_not_exist_for_test.yaml");
    test.Expect(ValidateRequiredFile(absent).code() == ErrorCode::kConfigurationMissing,
                "missing required file is rejected");

    if (test.failures() == 0) {
        std::cout << "host_core_tests: all checks passed\n";
        return 0;
    }
    std::cerr << "host_core_tests: " << test.failures() << " check(s) failed\n";
    return 1;
}
