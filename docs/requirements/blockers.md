# 缺失信息与阻塞项

审计范围：已下载官方赛题页面与 8 页规则，已扫描 `official/organizer_drop/`（当前无投放资料）。下列项目未在现有官方公开资料中得到确认，均保持 `BLOCKED`。获得资料后先运行新增资料审计，再更新事实登记表和需求矩阵。

## 1. 官方赛期资料

| 缺失项 | 为什么需要 | 阻塞功能 | 应从哪里获得 | 获得后放置 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 最终地图 | 确认真实路线与拓扑 | 路径规划、状态触发、回放验证 | 组委会赛期文件/赛区通知 | `official/organizer_drop/maps/` | BLOCKED |
| 详细赛道图纸 | 获取可量化几何与元素位置 | 场地建模、停车/岔路规划 | 组委会详细图纸 | `official/organizer_drop/maps/` | BLOCKED |
| 元素最终实物样式 | 公开规则图片仅为示意 | 类别定义、采集、识别验证 | 组委会实物资料/真实赛具 | `official/organizer_drop/notices/` 或 `data/raw/` | BLOCKED |
| 元素摆放规则 | 任务触发依赖实际摆放 | 状态机触发、局部规划 | 组委会布局说明 | `official/organizer_drop/maps/` | BLOCKED |
| 赛区具体比赛形式 | 规则说明赛后续通知 | 测试流程、提交形式 | 赛区/组委会通知 | `official/organizer_drop/notices/` | BLOCKED |
| 官方赛具包情况 | 确认实物平台和供应边界 | 硬件选型、合规检查 | 组委会/赛区 | `official/organizer_drop/hardware/` | BLOCKED |
| 官方基础工程 | 确认支持接口与工程边界 | 驱动、通信、部署 | 组委会 | `official/organizer_drop/examples/` | BLOCKED |
| 官方训练数据 | 建立合法、匹配赛具的数据基线 | 模型训练和验证 | 组委会 | `official/organizer_drop/datasets/` | BLOCKED |
| 官方模型 | 确认类别、输入和权重来源 | 目标板推理 | 组委会 | `official/organizer_drop/models/` | BLOCKED |
| 官方计时接口 | 判断是否存在机器接口或仅视频计时 | 计时集成、比赛日志 | 组委会/赛区 | `official/organizer_drop/sdk/` 或 `notices/` | BLOCKED |

## 2. 计算单元

| 缺失项 | 为什么需要 | 阻塞功能 | 应从哪里获得 | 获得后放置 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 具体品牌和型号 | 不能由规则规格反推产品 | 全部板端集成 | 官方赛具清单/铭牌 | `official/organizer_drop/hardware/` | BLOCKED |
| CPU 架构 | 决定编译目标与依赖二进制 | 交叉编译、部署 | 官方硬件手册或设备探测 | `official/organizer_drop/hardware/`；记录到 `docs/environment/` | BLOCKED |
| 系统镜像 | 确认运行环境和恢复方式 | 部署、设备驱动 | 组委会 | `official/organizer_drop/sdk/` | BLOCKED |
| 操作系统 | 决定系统 API 和服务管理 | 运行时、设备访问 | 官方镜像说明或真实设备 | `official/organizer_drop/hardware/` | BLOCKED |
| 编译器 | 确认 ABI 和可用标准 | 目标端构建 | 官方工具链 | `official/organizer_drop/sdk/` | BLOCKED |
| AI 推理 SDK | 确认模型加载与执行 API | OfficialInferenceBackend | 官方 SDK | `official/organizer_drop/sdk/` | BLOCKED |
| 支持的模型格式 | 决定训练产物交付格式 | 模型转换、加载 | SDK 文档 | `official/organizer_drop/sdk/` | BLOCKED |
| 支持的算子 | 避免部署不兼容网络 | 模型设计与转换 | SDK 算子清单/实测 | `official/organizer_drop/sdk/` | BLOCKED |
| 模型转换工具 | 生成可部署产物并保留记录 | 模型部署 | 官方工具链 | `official/organizer_drop/sdk/` | BLOCKED |
| 相机接口 | 决定 CameraBackend 实现 | 真实取流 | 硬件/SDK 手册 | `official/organizer_drop/hardware/` 或 `sdk/` | BLOCKED |
| 串口接口 | 确认物理/逻辑通信能力 | VehicleTransport | 硬件手册 | `official/organizer_drop/hardware/` | BLOCKED |
| 设备节点 | 运行时打开设备所需 | 相机和串口启动 | 真实设备枚举 | `docs/environment/target_environment.md` | BLOCKED |
| 部署流程 | 确认可重复安装和启动 | 板端交付 | 官方指南 | `official/organizer_drop/sdk/` | BLOCKED |

## 3. 控制单元和底盘

| 缺失项 | 为什么需要 | 阻塞功能 | 应从哪里获得 | 获得后放置 | 状态 |
| --- | --- | --- | --- | --- | --- |
| MCU 型号 | 确认工具链与外设 | MCU 工程、通信 | 赛具手册/实物丝印 | `official/organizer_drop/hardware/` | BLOCKED |
| MCU 工程 | 确认官方控制逻辑和引脚 | 电机、舵机、鸣笛 | 组委会 | `mcu/official/` | BLOCKED |
| 舵机控制方式 | 确认命令语义和电气接口 | 转向控制 | 手册、接线图、官方工程 | `official/organizer_drop/hardware/` | BLOCKED |
| 电机驱动方式 | 确认命令语义和安全边界 | 速度控制 | 手册、接线图、官方工程 | `official/organizer_drop/hardware/` | BLOCKED |
| 编码器是否存在 | 判断是否具备速度/里程反馈 | 闭环速度、里程计 | 实物检查/硬件手册 | `official/organizer_drop/hardware/` | BLOCKED |
| 速度反馈方式 | 确认测量来源和单位 | SpeedPlanner、闭环控制 | 官方协议/实车测量 | `docs/interfaces/` | BLOCKED |
| 串口协议 | 定义帧、字段、校验和异常处理 | VehicleTransport | 官方协议/MCU 源码 | `official/organizer_drop/sdk/` 或 `mcu/official/` | BLOCKED |
| 急停机制 | 建立可验证的安全停机链路 | SafetySupervisor、实车安全 | 赛具手册/组委会 | `official/organizer_drop/hardware/` | BLOCKED |
| 蜂鸣器控制方式 | 满足规则鸣笛能力 | 声音提示 | MCU 工程/接线图 | `mcu/official/` | BLOCKED |

## 4. 实车标定

| 缺失项 | 为什么需要 | 阻塞功能 | 应从哪里获得 | 获得后放置 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 相机内参 | 像素到射线/地面的映射基础 | 去畸变、定位、规划 | 实际相机标定 | `data/calibration/camera_intrinsics.*` | BLOCKED |
| 畸变参数 | 修正镜头几何误差 | 车道与目标定位 | 实际相机标定 | `data/calibration/camera_intrinsics.*` | BLOCKED |
| 相机安装高度 | 建立相机到地面关系 | 逆透视、距离估计 | 实车测量 | `data/calibration/camera_extrinsics.*` | BLOCKED |
| 相机俯仰角 | 建立相机姿态 | 逆透视、距离估计 | 实车标定 | `data/calibration/camera_extrinsics.*` | BLOCKED |
| 相机相对车体坐标 | 统一感知和控制坐标系 | 路径跟踪 | 实车测量 | `data/calibration/camera_extrinsics.*` | BLOCKED |
| 车辆轴距 | 运动学模型必需 | 转向/路径跟踪 | 实车测量 | `data/calibration/vehicle_geometry.*` | BLOCKED |
| 车辆轮距 | 碰撞包络和几何验证 | 规划、安全边界 | 实车测量 | `data/calibration/vehicle_geometry.*` | BLOCKED |
| 轮胎实际直径 | 速度/里程换算 | 速度反馈 | 实车测量 | `data/calibration/vehicle_geometry.*` | BLOCKED |
| 舵机中值 | 定义直行基准 | SteeringController | 架空轮和低速标定 | `data/calibration/steering.*` | BLOCKED |
| 舵机左右限位 | 防止机械冲击 | 转向安全 | 实车标定 | `data/calibration/steering.*` | BLOCKED |
| 舵机控制值与前轮转角映射 | 把命令转为车辆运动 | 路径跟踪 | 实车标定 | `data/calibration/steering.*` | BLOCKED |
| 电机控制值与实际速度映射 | 把速度目标转为驱动命令 | 速度控制 | 安全场地实测 | `data/calibration/motor_speed.*` | BLOCKED |
| 编码器换算关系 | 将计数转为速度/距离 | 速度反馈、里程 | 确认编码器后标定 | `data/calibration/encoder.*` | BLOCKED |
| 制动距离 | 安全停车和任务停车规划 | SafetySupervisor、停车 | 分速度实车测量 | `data/calibration/braking.*` | BLOCKED |
| 转弯半径 | 路径可行性和障碍绕行 | LocalPlanner | 实车测量 | `data/calibration/turning.*` | BLOCKED |
| 停车动作标定数据 | 形成可重复入位/驶出轨迹 | 停车任务 | 真实车位实测 | `data/calibration/parking.*` | BLOCKED |

## 5. 感知数据

| 缺失项 | 为什么需要 | 阻塞功能 | 应从哪里获得 | 获得后放置 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 最终类别列表 | 定义模型输出语义 | 目标/信号识别 | 组委会数据说明/最终实物 | `official/organizer_drop/datasets/` | BLOCKED |
| 类别定义 | 消除相似标志和状态歧义 | 标注、后处理、状态机 | 官方标签说明 | `official/organizer_drop/datasets/` | BLOCKED |
| 标注格式 | 建立可复现数据管线 | 训练/评估 | 官方数据说明或团队规范审批 | `data/annotations/README.md` | BLOCKED |
| 训练集 | 学习真实任务元素 | 模型训练 | 组委会或合规实车采集 | `official/organizer_drop/datasets/` 或 `data/raw/` | BLOCKED |
| 验证集 | 得到独立评估证据 | 模型选择、精度报告 | 官方划分或留档采集 | `data/processed/validation/` | BLOCKED |
| 真实车载摄像头视频 | 覆盖真实视角、曝光和运动 | 回放、感知验证 | 实际赛具采集 | `data/replay/` | BLOCKED |
| 光照范围 | 定义数据覆盖与失效边界 | 鲁棒性验证 | 真实场地测量/组委会说明 | `docs/verification/lighting.md` | BLOCKED |
| 模型权重 | 执行真实推理 | ObjectDetectorBackend | 官方模型或可追溯训练 | `models/official/` 或 `models/converted/` | BLOCKED |
| 模型精度 | 判断是否满足任务需求 | 模型验收 | 固定验证集实测 | `docs/verification/model_metrics.md` | BLOCKED |
| 板端推理速度 | 判断实时预算 | 运行时线程与降级策略 | 目标板基准测试 | `docs/verification/target_benchmark.md` | BLOCKED |

## 当前最高影响链

计算单元/SDK、MCU/串口协议、真实赛具标定、最终地图与真实感知数据同时缺失，使真实摄像头、板端推理、实车控制和全部任务闭环均保持 `BLOCKED`。这些阻塞项不会因 Host Core 纯逻辑代码可编译而自动解除。
