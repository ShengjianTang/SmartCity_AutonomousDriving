#include "smart_city_car/replay_camera_backend.hpp"

#include <cctype>
#include <limits>
#include <memory>
#include <string>
#include <utility>

#include "smart_city_car/config_validator.hpp"

namespace smart_city_car {
namespace {

bool ContainsUnsafeCommandCharacter(const std::string& text) {
    return text.find('"') != std::string::npos || text.find('\n') != std::string::npos ||
           text.find('\r') != std::string::npos;
}

std::FILE* OpenPipe(const char* command) {
#ifdef _WIN32
    return _popen(command, "rb");
#else
    return popen(command, "r");
#endif
}

int CloseProcessPipe(std::FILE* pipe) noexcept {
#ifdef _WIN32
    return _pclose(pipe);
#else
    return pclose(pipe);
#endif
}

}  // namespace

ReplayCameraBackend::ReplayCameraBackend(std::filesystem::path video_path,
                                         std::filesystem::path ffmpeg_path, Clock clock)
    : video_path_(std::move(video_path)), ffmpeg_path_(std::move(ffmpeg_path)), clock_(std::move(clock)) {}

ReplayCameraBackend::~ReplayCameraBackend() {
    ClosePipe();
}

Status ReplayCameraBackend::Open() {
    if (pipe_ != nullptr) {
        return Status::Error(ErrorCode::kInvalidArgument, "replay camera is already open");
    }
    const Status video_status = ValidateRequiredFile(video_path_);
    if (!video_status.ok()) {
        return video_status;
    }
    if (ffmpeg_path_.empty()) {
        return Status::Error(ErrorCode::kConfigurationMissing, "ffmpeg executable path is empty");
    }
    const std::string video = std::filesystem::absolute(video_path_).string();
    const std::string ffmpeg = ffmpeg_path_.string();
    if (ContainsUnsafeCommandCharacter(video) || ContainsUnsafeCommandCharacter(ffmpeg)) {
        return Status::Error(ErrorCode::kInvalidArgument, "replay paths contain unsupported command characters");
    }
    std::string command = "\"" + ffmpeg + "\" -nostdin -hide_banner -loglevel error -i \"" +
                          video + "\" -f image2pipe -vcodec ppm -";
#ifdef _WIN32
    // cmd.exe removes one outer quote layer. Without it, a quoted executable at
    // the start of an _popen command is parsed as an invalid command name.
    command = "\"" + command + "\"";
#endif
    pipe_ = OpenPipe(command.c_str());
    if (pipe_ == nullptr) {
        return Status::Error(ErrorCode::kProcessLaunchFailed, "failed to launch ffmpeg replay decoder");
    }
    next_sequence_ = 0;
    has_timestamp_ = false;
    return Status::Ok();
}

bool ReplayCameraBackend::ReadToken(std::string& token) {
    token.clear();
    int value = 0;
    for (;;) {
        value = std::fgetc(pipe_);
        if (value == EOF) return false;
        if (value == '#') {
            while ((value = std::fgetc(pipe_)) != EOF && value != '\n') {}
            continue;
        }
        if (std::isspace(static_cast<unsigned char>(value)) == 0) break;
    }
    do {
        token.push_back(static_cast<char>(value));
        value = std::fgetc(pipe_);
    } while (value != EOF && std::isspace(static_cast<unsigned char>(value)) == 0);
    return !token.empty();
}

FrameResult ReplayCameraBackend::NextFrame() {
    if (pipe_ == nullptr) {
        return {Status::Error(ErrorCode::kBackendUnavailable, "replay camera is not open"), nullptr};
    }
    std::string magic;
    if (!ReadToken(magic)) {
        const int exit_code = ClosePipe();
        if (exit_code != 0) {
            return {Status::Error(ErrorCode::kInputUnavailable, "ffmpeg decoder exited with an error"), nullptr};
        }
        return {Status::Error(ErrorCode::kEndOfStream, "replay reached end of stream"), nullptr};
    }
    std::string width_text;
    std::string height_text;
    std::string maximum_text;
    if (magic != "P6" || !ReadToken(width_text) || !ReadToken(height_text) || !ReadToken(maximum_text)) {
        ClosePipe();
        return {Status::Error(ErrorCode::kInputUnavailable, "decoder output is not a complete P6 PPM frame"), nullptr};
    }
    std::size_t width = 0;
    std::size_t height = 0;
    int maximum = 0;
    try {
        width = std::stoull(width_text);
        height = std::stoull(height_text);
        maximum = std::stoi(maximum_text);
    } catch (const std::exception&) {
        ClosePipe();
        return {Status::Error(ErrorCode::kInputUnavailable, "decoder returned invalid PPM dimensions"), nullptr};
    }
    constexpr std::size_t channels = 3U;
    if (width == 0U || height == 0U || maximum != 255 ||
        width > std::numeric_limits<std::size_t>::max() / height ||
        width * height > std::numeric_limits<std::size_t>::max() / channels) {
        ClosePipe();
        return {Status::Error(ErrorCode::kInputUnavailable, "decoder returned unsupported PPM metadata"), nullptr};
    }
    auto buffer = std::make_shared<FrameBuffer>();
    buffer->format = "RGB8";
    buffer->width = width;
    buffer->height = height;
    buffer->bytes.resize(width * height * channels);
    const std::size_t read = std::fread(buffer->bytes.data(), 1U, buffer->bytes.size(), pipe_);
    if (read != buffer->bytes.size()) {
        ClosePipe();
        return {Status::Error(ErrorCode::kInputUnavailable, "decoder returned a truncated PPM frame"), nullptr};
    }
    auto timestamp = clock_();
    if (has_timestamp_ && timestamp <= last_timestamp_) {
        timestamp = last_timestamp_ + std::chrono::nanoseconds(1);
    }
    last_timestamp_ = timestamp;
    has_timestamp_ = true;

    auto frame = std::make_unique<Frame>();
    frame->sequence = next_sequence_++;
    frame->captured_at = timestamp;
    frame->source = video_path_.string();
    frame->buffer = std::move(buffer);
    return {Status::Ok(), std::move(frame)};
}

int ReplayCameraBackend::ClosePipe() noexcept {
    if (pipe_ == nullptr) return 0;
    std::FILE* const pipe = pipe_;
    pipe_ = nullptr;
    return CloseProcessPipe(pipe);
}

}  // namespace smart_city_car
