cmake_minimum_required(VERSION 3.20)

project(smart_city_driverless_host_core LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(smart_city_host_core
    src/core/config_validator.cpp
    src/core/frame_freshness.cpp
    src/core/model_registry.cpp
    src/core/offline_config.cpp
    src/core/status.cpp
    src/decision/mission_state_machine.cpp
    src/io/replay_camera_backend.cpp
    src/logging/telemetry_logger.cpp
    src/runtime/offline_replay_runner.cpp
    src/safety/safety_supervisor.cpp
)

target_include_directories(smart_city_host_core PUBLIC include)

if(MSVC)
    target_compile_options(smart_city_host_core PRIVATE /W4 /permissive- /WX)
else()
    target_compile_options(smart_city_host_core PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

find_program(FFMPEG_EXECUTABLE NAMES ffmpeg)

add_executable(smart_city_host_app src/app/smart_city_host_app.cpp)
target_link_libraries(smart_city_host_app PRIVATE smart_city_host_core)
if(FFMPEG_EXECUTABLE)
    target_compile_definitions(smart_city_host_app PRIVATE SMART_CITY_DEFAULT_FFMPEG_PATH="${FFMPEG_EXECUTABLE}")
endif()
if(MSVC)
    target_compile_options(smart_city_host_app PRIVATE /W4 /permissive- /WX)
else()
    target_compile_options(smart_city_host_app PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

include(CTest)
if(BUILD_TESTING)
    add_executable(host_core_tests tests/unit/host_core_tests.cpp)
    target_link_libraries(host_core_tests PRIVATE smart_city_host_core)
    if(FFMPEG_EXECUTABLE)
        target_compile_definitions(host_core_tests PRIVATE SMART_CITY_TEST_FFMPEG_PATH="${FFMPEG_EXECUTABLE}")
    endif()
    if(MSVC)
        target_compile_options(host_core_tests PRIVATE /W4 /permissive- /WX)
    else()
        target_compile_options(host_core_tests PRIVATE -Wall -Wextra -Wpedantic -Werror)
    endif()
    add_test(NAME host_core_tests COMMAND host_core_tests)
endif()
