#pragma once

#include "smart_city_car/status.hpp"

namespace smart_city_car {

struct SafetyInputs final {
    bool configuration_complete{false};
    bool camera_available{false};
    bool detector_required{false};
    bool detector_available{false};
    bool transport_available{false};
    bool manual_stop_requested{false};
};

class SafetySupervisor final {
public:
    Status AuthorizeMotion(const SafetyInputs& inputs) const;
};

}  // namespace smart_city_car
