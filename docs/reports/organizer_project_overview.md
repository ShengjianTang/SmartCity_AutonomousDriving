# 组委会旧工程概览

| 工程 | 来源归档 SHA-256 | 目标线索 | 正式 C/C++ 文件 | 当前用途 |
| --- | --- | --- | ---: | --- |
| `icar_autopilot_2025th` | `54f0c38151b5844b0108754d3917b2bfcab983e8a8a79f03d0bea8d5eacf69c7` | T710、AArch64、PPNC/ONNX Runtime | 45 | `REFERENCE_ONLY` |
| `icar_autopilot_2025th_FZ3B` | `c03a6a6b74ba0ba18a8f6ff673ea5548201ea55373d1e2a520427111ea7517a4` | FZ3B、Paddle Lite | 44 | `REFERENCE_ONLY` |

36 个正式 C/C++ 文件字节相同；差异集中在串口、检测、控制中心、停车、采集/启动工具，T710 另有 `running.cpp`。随包 `build/` 中二进制的 ELF `e_machine=0xB7`（AArch64），只是历史产物。

这些工程提供模块划分和接口调查线索，但年份、目标板、依赖、协议一致性与许可证均不足以直接并入当前 `src/`。
