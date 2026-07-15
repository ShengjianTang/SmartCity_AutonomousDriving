# IntelligentCar_Baidu 硬件假设审计

以下均来自第三方仓库，只描述原项目，不是当前赛题事实。

| 第三方假设 | 证据位置 | 当前项目处理 |
| --- | --- | --- |
| Edgeboard 智能车赛事专用版上位机 | `race/README.md`、`detection.hpp` | `REFERENCE_ONLY`；不得认定当前计算单元型号 |
| TC264 下位机 | `race/README.md` | `REFERENCE_ONLY`；当前 MCU 型号仍 `BLOCKED` |
| Linux 与 V4L2 | `libimage_process.cpp`、`race/onnx/README.md` | 当前目标 OS/相机 API 仍未知 |
| `/dev/video0`、`/dev/video1` | `libimage_process.cpp` | 不进入当前配置 schema |
| 320×240、MJPG、120 FPS 请求 | `libimage_process.cpp` | 未经当前相机验证，不复用 |
| `/dev/ttyUSB0`、`/dev/ttyUSB1` | `libuart_eb.cpp` | 当前设备节点未知 |
| 115200、8N1 | `libdata_store.h`、`libuart_eb.cpp` | 当前串口参数未知 |
| 帧头 `0xA0 0xA1`、尾字节 `0xA2` | `libdata_store.h`、`libuart_eb.cpp` | 当前协议未知；不得称其为 CRC16 |
| 下位机提供陀螺仪状态 | `libdata_store.h`、`libdata_process.cpp` | 当前传感器/反馈未知 |
| 舵机方向/角度、电机速度以单字节发送 | `libdata_process.cpp`、`libuart_eb.cpp` | 当前单位、范围、映射均未知 |
| PPNC 与 ONNX 混合推理 | `detection.hpp`、`race/CMakeLists.txt` | 当前 AI SDK、模型格式均未知 |
| 固定相机透视点和大量像素阈值 | `libimage_process.cpp`、`config/*.json` | 必须由当前实车标定替代，不能复制 |

## 安全影响

原工程在串口打开失败时 `abort()`，接收和推理多处无限忙等，未见命令新鲜度、真实急停确认、数据完整校验或通信断开后的受控降级。它不能作为当前项目的实车安全实现。
