# 数据流

```text
官方资料/实测标定
        │
        v
配置加载与来源校验 ──失败──> Fault / 禁止启动
        │
        v
CameraBackend ──> Frame{sequence, monotonic_timestamp, source, image}
        │
        ├──> 预处理 ──> 车道/边界感知 ─────────────┐
        └──> ObjectDetectorBackend ─> 时序过滤 ───┤
                                                  v
                                       SemanticObservation
                                                  │
                                                  v
                                        DecisionStateMachine
                                                  │
                         ┌────────────────────────┴──────────────┐
                         v                                       v
                    LocalPlanner                           SpeedPlanner
                         └────────────────────────┬──────────────┘
                                                  v
                                      SteeringController
                                                  │
                          health/config/events ─> SafetySupervisor
                                                  │
                         ┌────────────────────────┴──────────────┐
                         v                                       v
                  VehicleTransport                         TelemetryLogger
```

## 数据有效性

- `Frame`：缺图像、时间戳倒退、序号异常或来源不明时无效。
- `SemanticObservation`：必须区分“未检测到”“后端未运行”“推理失败”“检测到”。
- `MotionRequest`：速度、角度或路径参数缺少有证据配置时无效。
- `VehicleCommand`：只有 `SafetySupervisor` 明确授权且真实后端可用时才可发送。
- `RecordingTransport` 输出只能作为接口测试记录，不能作为车辆动作证据。
