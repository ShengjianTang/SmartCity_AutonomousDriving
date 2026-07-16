# 组委会旧工程硬件依赖审计

| 依赖 | T710 证据 | FZ3B 证据 | 当前判定 |
| --- | --- | --- | --- |
| 计算单元/ABI | AArch64 ELF、T710 命名、PPNC | FZ3B 命名、Paddle Lite | 仅 2025 旧基线，`REFERENCE_ONLY` |
| 相机 | OpenCV/旧相机封装 | OpenCV/旧相机封装 | 当前相机型号、节点、格式未知 |
| 控制链路 | `uart.hpp`，115200/8N1 | `uart.hpp`，115200/8N1 | 与控制板 PDF 有冲突，禁止正式接入 |
| MCU/执行器 | 旧协议语义 | 旧协议语义 | 未获得匹配的 MCU 源码、接线与实车验证 |
| 模型运行时 | PPNC、ONNX Runtime | Paddle Lite | 不等于当前目标板 SDK 已确认 |

具体设备节点、USB VID/PID、相机格式、执行器标定与急停电气链路均未由当前资料闭合。
