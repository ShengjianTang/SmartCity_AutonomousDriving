# 缺失信息与阻塞项

更新时间：2026-07-16。58 项原始阻塞全部保留并获得稳定 ID；资料到位不等于功能完成，只有证据、实现和相应验证都闭合后才能标为 `RESOLVED`。

本表专用状态：`RESOLVED`、`PARTIALLY_RESOLVED`、`STILL_BLOCKED`、`REQUIRES_USER_FILE`、`REQUIRES_TARGET_HARDWARE`、`REQUIRES_REAL_MEASUREMENT`、`LICENSE_UNVERIFIED`、`LEGACY_REFERENCE_ONLY`。

## 1. 官方赛期资料（B-001—B-010）

| ID | 阻塞项 | 影响 | 当前证据与解锁条件 | 状态 |
| --- | --- | --- | --- | --- |
| B-001 | 最终地图 | 路径/状态/回放 | 只有规则示意和 2025 场地资料；需 2026 最终图纸 | REQUIRES_USER_FILE |
| B-002 | 详细赛道图纸 | 场地建模/停车/岔路 | 需带尺寸、版本和发布日期的最终图纸 | REQUIRES_USER_FILE |
| B-003 | 元素最终实物样式 | 类别/采集/识别 | 2025 标牌只作旧参考；需 2026 实物图或赛具 | REQUIRES_USER_FILE |
| B-004 | 元素摆放规则 | 任务触发/局部规划 | 需最终布局说明 | REQUIRES_USER_FILE |
| B-005 | 赛区具体比赛形式 | 测试/提交 | 石墨有通知链接但本地未闭合当前赛区最终通知 | REQUIRES_USER_FILE |
| B-006 | 官方赛具包情况 | 硬件/合规 | 已有旧赛事专用卡、镜像、控制板资料，但未证明对应当前整车 | PARTIALLY_RESOLVED |
| B-007 | 官方基础工程 | 驱动/通信/部署 | 已有 2025 T710/FZ3B 工程；年份、目标板、依赖和许可证不足 | LEGACY_REFERENCE_ONLY |
| B-008 | 官方训练数据 | 训练/验证 | 未发现可确认的数据集和授权 | STILL_BLOCKED |
| B-009 | 官方模型 | 目标板推理 | 已登记 3 个 2025 旧模型，不能作为当前最终模型 | LEGACY_REFERENCE_ONLY |
| B-010 | 官方计时接口 | 计时/比赛日志 | 当前规则与资料未给机器接口 | STILL_BLOCKED |

## 2. 计算单元（B-011—B-023）

| ID | 阻塞项 | 影响 | 当前证据与解锁条件 | 状态 |
| --- | --- | --- | --- | --- |
| B-011 | 具体品牌和型号 | 全部板端集成 | T710/FZ3B 只出现在 2025 旧资料；需当前赛具铭牌/清单 | LEGACY_REFERENCE_ONLY |
| B-012 | CPU 架构 | 交叉编译/部署 | 随包旧 ELF 为 AArch64；不等于当前板确认 | LEGACY_REFERENCE_ONLY |
| B-013 | 系统镜像 | 部署/驱动 | 已有镜像烧写资料和大体积镜像工件，仍需确认板型/版本匹配 | PARTIALLY_RESOLVED |
| B-014 | 操作系统 | 系统 API/服务 | 旧资料提供 Linux 线索；需目标机 `uname/os-release` 留档 | PARTIALLY_RESOLVED |
| B-015 | 目标编译器/ABI | 目标端构建 | Host Clang 21.1.0 仅用于 Windows；旧 AArch64 工件不可替代工具链 | LEGACY_REFERENCE_ONLY |
| B-016 | AI 推理 SDK | OfficialInferenceBackend | 旧工程提到 PPNC/ONNX Runtime/Paddle Lite；需当前 SDK | LEGACY_REFERENCE_ONLY |
| B-017 | 支持的模型格式 | 转换/加载 | 旧模型格式已登记，当前 SDK 支持范围未知 | LEGACY_REFERENCE_ONLY |
| B-018 | 支持的算子 | 网络设计/转换 | 需当前 SDK 清单并在目标板实测 | REQUIRES_TARGET_HARDWARE |
| B-019 | 模型转换工具 | 模型部署 | 有旧模型编译教程；需当前版本和可重现转换记录 | LEGACY_REFERENCE_ONLY |
| B-020 | 相机接口 | CameraBackend | 旧工程/教程有接口线索，当前相机型号与格式未确认 | PARTIALLY_RESOLVED |
| B-021 | 串口接口 | VehicleTransport | 旧工程与控制板教程有 USB/UART 线索，但版本/物理口未闭合 | PARTIALLY_RESOLVED |
| B-022 | 设备节点 | 相机/串口启动 | 必须在目标机枚举并记录 | REQUIRES_TARGET_HARDWARE |
| B-023 | 部署流程 | 板端交付 | 已有旧烧写/远程操作教程；需在匹配目标板复现 | PARTIALLY_RESOLVED |

## 3. 控制单元和底盘（B-024—B-032）

| ID | 阻塞项 | 影响 | 当前证据与解锁条件 | 状态 |
| --- | --- | --- | --- | --- |
| B-024 | MCU 型号 | MCU 工程/通信 | 旧教程写 GD32F103C8T6；需确认当前赛具丝印/清单 | PARTIALLY_RESOLVED |
| B-025 | MCU 工程 | 电机/舵机/鸣笛 | PDF 展示代码结构但未投放对应完整源码；需原工程 | REQUIRES_USER_FILE |
| B-026 | 舵机控制方式 | 转向 | 旧 PDF/API 与协议表仅作线索；需当前接线、固件和标定 | PARTIALLY_RESOLVED |
| B-027 | 电机驱动方式 | 速度 | 旧 PDF 描述闭环模块；需当前驱动硬件/固件 | PARTIALLY_RESOLVED |
| B-028 | 编码器是否存在 | 速度/里程反馈 | 旧资料提到编码器，需当前实物确认 | REQUIRES_TARGET_HARDWARE |
| B-029 | 速度反馈方式 | SpeedPlanner/闭环 | 旧协议有速度字段，单位/方向/实车对应未验证 | PARTIALLY_RESOLVED |
| B-030 | 串口协议 | VehicleTransport | PDF 与 `uart.hpp` 在帧长、地址、发送长度冲突 | PARTIALLY_RESOLVED |
| B-031 | 急停机制 | 实车安全 | 仅有 Host 安全拒绝接口；需物理急停/看门狗/断链实测 | REQUIRES_TARGET_HARDWARE |
| B-032 | 蜂鸣器控制方式 | 鸣笛 | 旧 PDF/协议有语义，需当前 MCU 工程和实物验证 | PARTIALLY_RESOLVED |

## 4. 实车标定（B-033—B-048）

| ID | 阻塞项 | 阻塞功能 | 解锁记录 | 状态 |
| --- | --- | --- | --- | --- |
| B-033 | 相机内参 | 去畸变/定位 | 实际相机标定文件、图像与误差报告 | REQUIRES_REAL_MEASUREMENT |
| B-034 | 畸变参数 | 车道/目标定位 | 同 B-033 | REQUIRES_REAL_MEASUREMENT |
| B-035 | 相机安装高度 | 逆透视/距离 | 带测量方法和设备 ID 的实测 | REQUIRES_REAL_MEASUREMENT |
| B-036 | 相机俯仰角 | 逆透视/距离 | 外参标定与原始记录 | REQUIRES_REAL_MEASUREMENT |
| B-037 | 相机相对车体坐标 | 感知/控制坐标 | 外参和车体坐标定义 | REQUIRES_REAL_MEASUREMENT |
| B-038 | 车辆轴距 | 运动学/跟踪 | 实车几何测量 | REQUIRES_REAL_MEASUREMENT |
| B-039 | 车辆轮距 | 包络/规划 | 实车几何测量 | REQUIRES_REAL_MEASUREMENT |
| B-040 | 轮胎实际直径 | 速度/里程 | 负载条件下实测 | REQUIRES_REAL_MEASUREMENT |
| B-041 | 舵机中值 | 直行基准 | 架空轮/低速安全标定 | REQUIRES_REAL_MEASUREMENT |
| B-042 | 舵机左右限位 | 转向安全 | 机械限位与电流/温升记录 | REQUIRES_REAL_MEASUREMENT |
| B-043 | 舵机值到前轮角映射 | 路径跟踪 | 多点测量与拟合记录 | REQUIRES_REAL_MEASUREMENT |
| B-044 | 电机值到速度映射 | 速度控制 | 封闭场地分档实测 | REQUIRES_REAL_MEASUREMENT |
| B-045 | 编码器换算关系 | 速度/里程 | 确认编码器后留档测量 | REQUIRES_REAL_MEASUREMENT |
| B-046 | 制动距离 | 安全停车 | 分速度/电量/地面实测 | REQUIRES_REAL_MEASUREMENT |
| B-047 | 转弯半径 | 可行性/绕障 | 分舵角低速实测 | REQUIRES_REAL_MEASUREMENT |
| B-048 | 停车动作标定 | 停车任务 | 真实车位多次重复记录 | REQUIRES_REAL_MEASUREMENT |

## 5. 感知数据与模型（B-049—B-058）

| ID | 阻塞项 | 影响 | 当前证据与解锁条件 | 状态 |
| --- | --- | --- | --- | --- |
| B-049 | 最终类别列表 | 输出语义 | 2025 旧模型有 15/16 项标签；需 2026 最终定义 | REQUIRES_USER_FILE |
| B-050 | 类别定义 | 标注/后处理 | 需边界情况和状态定义 | REQUIRES_USER_FILE |
| B-051 | 标注格式 | 数据管线 | 无当前官方格式或获批团队规范 | STILL_BLOCKED |
| B-052 | 训练集 | 模型训练 | 无合法、匹配当前赛具的数据 | STILL_BLOCKED |
| B-053 | 验证集 | 模型选择/精度 | 无独立留档验证集 | STILL_BLOCKED |
| B-054 | 真实车载摄像头视频 | 回放/验证 | 旧示例视频非当前真实车载采集 | REQUIRES_TARGET_HARDWARE |
| B-055 | 光照范围 | 鲁棒性 | 需真实场地分条件采集/测量 | REQUIRES_REAL_MEASUREMENT |
| B-056 | 模型权重许可 | 真实推理 | 旧模型存在但没有明确许可证/训练来源 | LICENSE_UNVERIFIED |
| B-057 | 模型精度 | 模型验收 | 需固定验证集、版本化脚本和实测报告 | REQUIRES_REAL_MEASUREMENT |
| B-058 | 板端推理速度 | 实时预算 | 需目标板模型基准 | REQUIRES_TARGET_HARDWARE |

## 汇总与最高影响链

| 状态 | 数量 |
| --- | ---: |
| RESOLVED | 0 |
| PARTIALLY_RESOLVED | 12 |
| STILL_BLOCKED | 5 |
| REQUIRES_USER_FILE | 8 |
| REQUIRES_TARGET_HARDWARE | 6 |
| REQUIRES_REAL_MEASUREMENT | 18 |
| LICENSE_UNVERIFIED | 1 |
| LEGACY_REFERENCE_ONLY | 8 |

总计 58。当前最大链路仍是“当前目标板/SDK与设备节点 → 版本一致的 MCU/协议/急停 → 实车标定 → 当前类别与真实数据 → 模型/规划/控制 → 封闭场地验证”。Host 离线构建和回放成功不会自动解除其中任何实车项。
