# 任务状态机设计

阈值原则：所有距离、时间、置信度、速度、角度和动作持续量均保持未配置，除非官方规则明确给出且语义相同，或有实车标定记录。缺失参数导致对应转换不可用并进入 `kSafetyStop` 或 `kFault`，不采用经验值。

## 状态表

| 状态 | 官方依据 | 进入事件 | 退出事件 | 允许转换 | 超时策略 | 故障策略 | 感知输入 | 真实参数依赖 | 当前状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kInitialization | 工程安全语义 | 进程启动 | 配置/后端自检完成 | Ready, Fault | 未配置；不得启动运动 | Fault | 配置和后端健康 | 全部必需配置 | BLOCKED（Host 源码已写但未编译） |
| kReady | 工程安全语义 | 自检通过 | 明确启动授权 | NormalDriving, SafetyStop, Fault | 未配置 | SafetyStop/Fault | 启动授权 | 急停和传输健康 | BLOCKED（Host 源码已写但未编译） |
| kNormalDriving | 第 2 页常规道路/两圈 | 启动或任务退出 | 任务候选/终点/故障 | 各 Approach, FinishApproach, SafetyStop, Fault | 输入过期阈值未配置 | SafetyStop | 车道、任务观察、圈数 | 车道/控制标定 | BLOCKED（Host 源码已写但未编译） |
| kSpeedLimited | 第 3、5 页测速区 | 确认进入测速区 | 确认解除限速标志 | NormalDriving, SafetyStop | 区域超时未配置 | SafetyStop | 测速区边界、速度反馈 | 速度反馈和控制标定 | BLOCKED |
| kCrosswalkApproach | 第 3 页斑马线/信号牌 | 确认斑马线与指示 | 通行或等待语义确认 | CrosswalkWait, NormalDriving, SafetyStop | 未配置 | SafetyStop | 斑马线、信号状态 | 触发/制动标定 | BLOCKED |
| kCrosswalkWait | 第 3 页停车指示 | 停车语义确认 | 允许通行语义 | NormalDriving, SafetyStop | 停留时间未规定 | SafetyStop | 信号状态、车辆停止确认 | 停车/速度反馈 | BLOCKED |
| kParkingApproach | 第 3、5 页停车场 | 确认停车标志/车位 | 轨迹准备完成 | ParkingExecute, SafetyStop | 未配置 | SafetyStop | 标志、车位、车体定位 | 车位几何和标定 | BLOCKED |
| kParkingExecute | 第 5 页四轮同一车位 | 真实停车轨迹授权 | 入位且停止确认 | ParkingExit, SafetyStop | 未配置 | SafetyStop | 车位/车辆姿态 | 完整停车标定 | BLOCKED |
| kParkingExit | 第 5 页重新驶出 | 停留条件满足 | 安全退出车位 | NormalDriving, SafetyStop | “片刻”无数值 | SafetyStop | 出口/车辆姿态 | 完整停车标定 | BLOCKED |
| kBarrierApproach | 第 4、5 页道闸 | 确认道闸 | 停止确认 | BarrierWait, SafetyStop | 未配置 | SafetyStop | 道闸、车辆速度 | 触发和制动标定 | BLOCKED |
| kBarrierWait | 第 4、5 页等待开启 | 已在道闸前停稳 | 确认横杆抬起 | NormalDriving, SafetyStop | 未配置 | SafetyStop | 道闸状态、停止确认 | 道闸状态定义 | BLOCKED |
| kConstructionApproach | 第 4、5 页施工区 | 确认施工标志 | 障碍/路径准备完成 | ConstructionAvoidance, NormalDriving, SafetyStop | 未配置 | SafetyStop | 标志、锥桶/障碍 | 触发和车辆包络 | BLOCKED |
| kConstructionAvoidance | 第 4、5 页正确避障 | 安全绕行路径已验证 | 离开施工区 | NormalDriving, SafetyStop | 未配置 | SafetyStop | 障碍和可行路径 | 车辆几何/控制标定 | BLOCKED |
| kPedestrianApproach | 第 4、5 页行人 | 确认行人 | 避让路径/停止语义准备 | PedestrianAvoidance, SafetyStop | 未配置 | SafetyStop | 行人观察 | 类别、触发和制动标定 | BLOCKED |
| kPedestrianAvoidance | 第 5 页正确避障 | 安全行为已授权 | 确认风险解除 | NormalDriving, SafetyStop | 未配置 | SafetyStop | 行人时序/路径 | 真实数据与控制标定 | BLOCKED |
| kForkApproach | 第 4、5 页岔路 | 确认岔路和指示 | 分支指示稳定 | ForkLeft, ForkRight, SafetyStop | 未配置 | SafetyStop | 岔路和方向指示 | 最终地图/定位 | BLOCKED |
| kForkLeft | 第 4、5 页选择正确道路 | 左指示确认 | 通过岔路 | NormalDriving, SafetyStop | 未配置 | SafetyStop | 分支路径 | 地图和转向标定 | BLOCKED |
| kForkRight | 第 4、5 页选择正确道路 | 右指示确认 | 通过岔路 | NormalDriving, SafetyStop | 未配置 | SafetyStop | 分支路径 | 地图和转向标定 | BLOCKED |
| kFinishApproach | 第 2、5、7 页两圈/终点 | 两圈且终点确认 | 停车确认 | Finished, SafetyStop | 未配置 | SafetyStop | 终点、圈数、速度 | 圈计数/制动标定 | BLOCKED |
| kFinished | 第 5-7 页任务结束 | 终点停车确认 | 人工复位 | Initialization | 不适用 | SafetyStop | 停止确认 | 真实控制反馈 | BLOCKED |
| kSafetyStop | 工程安全语义与第 6 页失控终止 | 任一安全触发 | 仅人工检查与复位 | Initialization, Fault | 不自动恢复 | 保持停止请求 | 全部健康事件 | 真实急停/制动接口 | BLOCKED（Host 源码未编译，且不是实车急停） |
| kFault | 工程错误语义 | 不可恢复初始化/配置错误 | 人工修复并重启 | Initialization | 不自动恢复 | 禁止运动 | 错误记录 | 无 | BLOCKED（Host 源码已写但未编译） |

## 事件规范

- 事件必须含来源、关联帧/命令序号和单调时间戳。
- `Candidate` 感知不能直接触发危险动作；需要由尚待真实数据确定的时序过滤策略形成 `Confirmed` 事件。
- 状态不接受其允许列表之外的转换；非法转换产生结构化错误并进入 `kSafetyStop`。
- Host 单元测试只验证转换规则，不证明感知、规划或车辆动作。
