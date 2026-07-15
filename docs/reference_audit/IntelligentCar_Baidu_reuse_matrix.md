# IntelligentCar_Baidu 复用矩阵

许可证未确认前，表中“可否复用”均指源码能否复制；设计概念只能在当前官方证据和独立实现下参考。

| 模块 | 参考文件 | 原项目用途 | 当前赛题相关性 | 许可证状态 | 可否复用 | 需要适配内容 | 风险 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CMake 构建 | `race/CMakeLists.txt` | 构建 Edgeboard/TC264 上位机 | 低 | UNVERIFIED | 否 | 独立重写；等待官方 SDK | 固定 Linux 路径和预编译库 |
| 摄像头采集 | `libimage_process.cpp` | V4L2/样例视频取流 | 中 | UNVERIFIED | 否 | 官方相机 API、分辨率、时间戳、断流策略 | 设备节点和参数硬编码 |
| 图像预处理 | `libimage_process.cpp` | 灰度、OTSU、Sobel、形态学 | 中 | UNVERIFIED | 否；仅概念参考 | 真实相机标定、光照数据、独立实现 | 像素坐标和核固定 |
| 边线提取 | `path_side_search.cpp` | 八邻域左右边线 | 中 | UNVERIFIED | 否；仅概念参考 | 当前赛道数据集、边界失败检测、测试 | 固定数组/阈值、越界风险 |
| 中心线计算 | `path_side_search.cpp` | 左右边线中点滤波 | 中 | UNVERIFIED | 否；仅概念参考 | 车辆坐标、标定、可信度输出 | 只在图像坐标运行 |
| 圆环/十字状态 | `libdata_process.cpp`、`path_circle.cpp` | 原智能车赛道元素 | 低 | UNVERIFIED | 否 | 当前赛题任务语义完全重建 | 任务不匹配、帧数阈值硬编码 |
| 目标检测 | `detection.hpp`、`libmodel_ppnc.cpp` | PPNC+ONNX 推理 | 低 | 受限声明/UNVERIFIED | 否 | 官方 SDK、类别、模型、输入、后处理 | 第三方公司声明请勿商用；二进制依赖 |
| 施工/障碍逻辑 | `path_model.cpp` | 危险区补线和舵角倍率 | 中 | UNVERIFIED | 否；仅风险参考 | 当前锥桶/施工区数据、车辆包络、实测规划 | 无几何标定，阈值/倍率不可迁移 |
| 停车/车库逻辑 | `path_model.cpp` | 救援区转交下位机入库 | 低 | UNVERIFIED | 否 | 当前停车场规则、车位定位、完整标定 | 与当前停车任务不同，未含完整轨迹 |
| 串口传输 | `libuart_wz.cpp`、`libuart_eb.cpp` | Linux termios 与 TC264 帧 | 低 | UNVERIFIED | 否 | 官方协议、设备、校验、超时、安全状态 | 固定设备/波特率，尾字节伪称 CRC16 |
| 控制量 | `libdata_process.cpp` | 像素前瞻到舵角和分段电机值 | 低 | UNVERIFIED | 否 | 车辆运动学、执行器/速度标定、限幅 | 单位不明、缩窄到单字节 |
| 配置 | `config/*.json` | 三套速度/像素/帧阈值 | 低 | UNVERIFIED | 否 | 用当前 schema 和来源字段替代 | 大量无来源硬编码值 |
| 日志 | `ImgShow`/`ImgSave`/`DataPrint` | 图像保存与终端打印 | 低 | UNVERIFIED | 否 | 结构化时间戳、错误码、轮转和磁盘保护 | 缺少持久化安全审计 |
| HSV/LDC 工具 | `self/tool/` | 调色和逆透视辅助 | 中 | UNVERIFIED | 否；仅概念参考 | 当前标定流程、误差报告、独立实现 | 工具含已提交构建产物，无验证记录 |

结论：没有任何第三方源码被复制到 `src/`。后续若要借鉴算法思路，必须记录独立设计、官方/实测依据和许可证审查结果。
