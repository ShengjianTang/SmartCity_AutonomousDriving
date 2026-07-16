# PROJECT_STATE

- 更新时间：2026-07-16T15:48:31+08:00
- Git 分支：`audit/organizer-materials-integration`
- 本轮基线 commit：`9d9b624f1fa10e57bdd6e592a685656a1b93b8d6`
- 需求矩阵：35 项（`VERIFIED` 4、`IMPLEMENTED_UNVERIFIED` 4、`BLOCKED` 23、`NOT_STARTED` 4）
- 阻塞清单：58 项，0 项真正解除

## 当前工程在做什么

本仓库把“官方/组委会资料证据”转成可追踪需求和安全边界，在 Windows Host 上提供一个不会驱动车辆的离线算法骨架：读取视频帧、校验配置/模型登记/帧时效、形成语义观测、运行任务状态与安全监督、只记录安全停止和遥测。真实相机、板端推理、规划控制和串口执行必须等当前硬件、协议、标定与数据闭合后再接入。

## VERIFIED

- 官网赛题页和 8 页规则 PDF 的 HTTP、SHA-256、解析与全页渲染。
- 组委会原始投放 33 文件、22,960,347,578 字节；12 个压缩包完整性/路径安全检查及隔离解压，失败 0。
- 清理后 manifest 为 1,146 文件、114,392,868,846 字节；清理只移除核准元数据和可再生临时文件。
- 石墨公开页元数据/内容快照与 12 个附件索引；附件防盗链阻塞按事实记录，未绕过。
- 两个 ONNX 后处理图的哈希与结构检查；旧工程源码差异、AArch64 ELF、依赖和许可证静态事实。
- Host 本机真实配置/构建/链接，CTest 1/1 通过。

## IMPLEMENTED_UNVERIFIED

- C++17 Host Core：状态/错误、配置文件检查、任务状态机、安全监督、结构化日志、`RecordingTransport`。
- `ReplayCameraBackend`：通过 FFmpeg 从视频读取 RGB8 帧，维护递增序号和严格单调时间戳，显式 EOF/错误。
- Host 离线应用：强制 `--dry-run`，读取模型登记，禁用检测器，工作线程可停止并 `join`。
- 组委会旧示例 `fine.mp4` dry-run：189 帧、189 条安全停止、正常 EOF、0 条 `drives_vehicle=true`。
- 自动化测试覆盖缺配置/缺视频、EOF、时间戳、过期输入、禁用检测器、手动停止、非法迁移和非驱车传输。

这些状态都未经过当前目标板、当前真实车载视频或真实赛道验证，不能升级为车辆功能 `VERIFIED`。

## BLOCKED

- 真实相机后端、当前目标板 SDK/推理后端、最终类别/合法数据/可用模型。
- 版本一致的 MCU 工程、无冲突串口协议、物理急停/看门狗与 `OfficialSerialTransport`。
- 车辆几何、相机内外参、舵机/电机/编码器/制动/停车全部实测标定。
- 车道/边界感知、目标识别、局部规划、速度/转向控制及所有比赛任务闭环。
- 2026 最终地图、实物样式、赛区通知、目标板基准、封闭场地两圈与提交材料。

58 项细分：`PARTIALLY_RESOLVED` 12、`STILL_BLOCKED` 5、`REQUIRES_USER_FILE` 8、`REQUIRES_TARGET_HARDWARE` 6、`REQUIRES_REAL_MEASUREMENT` 18、`LICENSE_UNVERIFIED` 1、`LEGACY_REFERENCE_ONLY` 8。

## REFERENCE_ONLY / REJECTED

- 组委会 2025 T710/FZ3B 工程、模型、场地图和示例视频：`REFERENCE_ONLY`；未复制源码/协议实现。
- `third_party/IntelligentCar_Baidu` commit `be05851d04154d374e46687e10809e13e997f712`：`REFERENCE_ONLY`，许可证未确认。
- Kesci 2018 其他比赛仓库：`REJECTED`，未依赖。

## 最近验证

| 操作 | 结果 |
| --- | --- |
| Host CMake configure/build | exit 0；Clang 21.1.0；`-Werror`；3 个目标链接成功 |
| Host CTest | exit 0；1/1 通过；0.46 秒 |
| T710/FZ3B 隔离配置 | 编译器检查通过；均因缺 glib/OpenCV 停止；未修改源码 |
| 模型登记 | 3 个逻辑模型、21 个工件；ONNX checker PASS×2 |
| 实际视频 dry-run | exit 0；189 帧；正常 EOF；只写 RecordingTransport |
| 清理后全量 manifest | exit 0；1,146 文件；114,392,868,846 字节 |

## 下一步

用户应优先按 `USER_INPUT_REQUIRED.md` 补组装视频/学习手册、当前赛具/目标板证据、匹配 MCU 工程与协议，然后提供最终地图/类别/数据和全部标定记录。资料不足时仍可继续增强纯 Host 测试与审计工具，但不能安全完成实车功能。
