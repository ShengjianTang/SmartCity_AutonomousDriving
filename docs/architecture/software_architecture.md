# 软件架构

## 分层

1. **证据与配置层**：来源锁、事实登记、需求矩阵、schema、标定文件。
2. **后端适配层**：`CameraBackend`、`ObjectDetectorBackend`、`VehicleTransport`。官方接口未获得前保持不可用。
3. **感知层**：图像预处理、车道边界、目标/信号识别、时序过滤；依赖真实数据后实现。
4. **任务与规划层**：`DecisionStateMachine`、`LocalPlanner`、`SpeedPlanner`，输出带有效性和来源的语义请求，不直接写硬件。
5. **控制与安全层**：`SteeringController`、`SafetySupervisor`；控制参数和执行器接口缺失时拒绝下发。
6. **可观测性层**：`TelemetryLogger`、错误码、命令记录、验证证据。

## 后端契约

| 接口 | 可用实现 | 失败实现/边界 |
| --- | --- | --- |
| `CameraBackend` | `OfficialCameraBackend`：获得官方接口后；`ReplayCameraBackend`：只读真实采集视频 | 未配置时返回明确错误，不产生图像 |
| `ObjectDetectorBackend` | `OfficialInferenceBackend`：获得 SDK/模型后 | `DisabledDetectorBackend` 返回 unavailable，不生成检测框 |
| `VehicleTransport` | `OfficialSerialTransport`：获得协议并验证后 | `RecordingTransport` 只记录命令并标明不会驱动车辆 |

## 核心约束

- 每帧携带单调时钟时间戳、来源和序号；过期阈值必须来自配置证据。
- 每个感知结果携带来源帧和有效性；无结果与“未运行”不可混淆。
- 任务状态机只消费经过验证的语义事件，不直接读取模型类别编号。
- 规划输出是目标路径/速度语义；控制器只有在标定完整、后端可用、安全监督授权时才可形成执行命令。
- 所有硬件输出先经过安全监督；日志失败不得静默掩盖关键错误。
- 任何未配置依赖都会阻止相关能力启动，而不是使用第三方参数。
