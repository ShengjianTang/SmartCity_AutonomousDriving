# 智慧城市无人驾驶算法应用赛工程

本仓库为“全球校园人工智能算法精英大赛——智慧城市无人驾驶算法应用赛”建立证据驱动的工程基础。当前成果包括官方/组委会资料固化、规则/需求与旧工程审计、架构与安全设计、未知参数 schema，以及不依赖目标板 SDK 的 Host 离线回放应用。它不是已完成的实车系统。

## 赛题来源

- [赛题页面](https://www.aicomp.cn/tracks/4548.html)
- [官方规则 PDF](https://www.aicomp.cn/wp-content/uploads/2026/06/11%E6%99%BA%E6%85%A7%E5%9F%8E%E5%B8%82%E6%97%A0%E4%BA%BA%E9%A9%BE%E9%A9%B6%E7%AE%97%E6%B3%95%E5%BA%94%E7%94%A8%E8%B5%9B.pdf)
- 本地来源锁：`docs/sources/SOURCES.lock.yaml`
- 官方规则 SHA-256：`41cd80412a740049f15bf02bc9f9ea28b9b89f96af1d8a4335fb750f98c03988`

## 证据驱动原则

官方文件和真实测量优先于第三方代码与经验。硬件、协议、参数、模型和性能没有证据时保持未知/`BLOCKED`；规则范围不转化为任意固定配置；单元测试不证明实车能力。

## 当前状态

- `VERIFIED`：公开规则、组委会 33 个原始投放文件、12 个压缩包、石墨 12 附件索引及清理后 1,146 文件 manifest 已形成证据记录；Host 构建和测试命令已实际运行。
- `IMPLEMENTED_UNVERIFIED`：Host Core、FFmpeg 视频回放、配置/模型登记读取、安全拒绝、记录传输和 CLI 已由 Clang 21.1.0 构建，CTest 1/1；旧示例视频 189 帧正常 EOF、无驱车输出。
- `BLOCKED`：所有当前目标板、真实相机、可用模型、无冲突通信协议、规划控制和实车任务仍等待硬件/标定/数据与场地验证。
- `REJECTED`：Kesci 2018 仓库不适用于当前赛题，未克隆。
- `REFERENCE_ONLY`：`IntelligentCar_Baidu` 固定到指定 commit，仅作审计参考，整体许可证未确认。

详见 `PROJECT_STATE.md`、`docs/requirements/requirement_traceability_matrix.md` 和 `docs/requirements/blockers.md`。

## 目录

```text
official/       已锁定公开资料与组委会资料投放区
third_party/    隔离的第三方参考仓库（主仓库忽略其工作树）
docs/           环境、来源、需求、架构、安全、审计与验证文档
config/         来源约束 schema 与强制 dry-run 的 Host 配置；未知值为 null
include/, src/  硬件无关 Host Core、视频回放与离线应用
mcu/            官方 MCU 工程等待区；当前无臆测实现
models/, data/  有来源资料的存放边界；禁止假模型/假数据
tools/          下载、规则提取与官方资料审计工具
tests/          Host 单元/离线集成测试；当前 CTest 1/1 通过
logs/           初始化命令和运行日志边界
```

## 重新下载公开资料

Windows：

```powershell
.\tools\bootstrap\bootstrap.ps1
```

或直接运行：

```powershell
.\.venv\Scripts\python.exe tools\download\download_public_sources.py
```

Linux/macOS 可运行 `bash tools/bootstrap/bootstrap.sh`。脚本下载到临时文件后校验并原子替换；现有文件 SHA-256 正确时不会覆盖。上游内容若改变会校验失败并保留错误报告，不会静默更新来源锁。

## 审计新增组委会资料

按 `official/organizer_drop/README.md` 投放原文件，然后运行：

```powershell
.\.venv\Scripts\python.exe tools\audit\audit_new_official_materials.py
```

输出为 `docs/sources/new_material_audit.md`。该步骤只清点哈希和待审内容，不自动把文件认定为官方事实。

## 构建和验证 Host

项目局部 CMake/Ninja/Zig 的已验证配置细节见 `docs/environment/host_build_report.md`。配置完成后执行：

```powershell
.\.venv\Scripts\cmake.exe --build build\host_app
.\.venv\Scripts\ctest.exe --test-dir build\host_app --output-on-failure
```

离线运行必须显式传入 `--dry-run`：

```powershell
.\build\host_app\smart_city_host_app.exe --dry-run --config config\host\offline_replay.yaml --replay-video <video-path> --log-output logs\runtime\offline_replay.log
```

程序没有实车模式；检测器未配置，传输固定为 `RecordingTransport`。

## 当前阻塞项

核心阻塞包括最终地图/物料、计算单元与 SDK、官方相机接口、MCU 工程与串口协议、执行器/急停机制、车辆几何与控制标定、感知类别/数据/模型和真实车载视频。完整 58 项见 `docs/requirements/blockers.md`。

## 第三方仓库声明

`third_party/IntelligentCar_Baidu/` 是第十九届智能车竞赛百度完全模型组工程，不是当前赛题官方代码。它明确耦合 Edgeboard 赛事版、TC264、V4L2、固定串口和原比赛任务；仓库无整体许可证，核心检测文件还带非商业限制。其源码、二进制、模型、协议和参数均未复制到正式工程。审计见 `docs/reference_audit/`。

## 为什么不能声称已完成实车系统

现有组委会资料主要是 2025 旧工程/教程，仍未闭合当前硬件、OS/SDK、设备节点、无冲突通信协议、合法可用模型、数据、控制参数或最终地图；项目也没有真实赛具和场地测试。Host 已编译成功只证明软件骨架可在主机运行，不证明真实摄像头、AI、舵机、电机、巡线、避障、泊车、两圈运行或急停有效。

## 接入正式赛具的顺序

1. 投放并审计组委会硬件、SDK、MCU、地图、数据和模型资料。
2. 更新来源锁、事实登记、需求矩阵和 schema 实例。
3. 在真实设备上记录接口枚举与工具链环境。
4. 完成相机、车辆几何、舵机、电机、制动和停车标定。
5. 实现隔离的官方后端，先台架再低速封闭场地验证。
6. 使用真实车载数据完成离线回放和感知评估，再进行分任务/全赛道测试。

## 安全

未验证真实急停、制动和通信看门狗前，不得让本工程驱动车辆。测试按 Host 逻辑、真实回放、台架、低速封闭场地、完整赛道逐级进行；每级保留配置哈希、日志和视频。危害分析见 `docs/safety/hazard_analysis.md`。
