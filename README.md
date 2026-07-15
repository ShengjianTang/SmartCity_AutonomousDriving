# 智慧城市无人驾驶算法应用赛工程

本仓库为“全球校园人工智能算法精英大赛——智慧城市无人驾驶算法应用赛”建立证据驱动的工程基础。当前成果包括官方资料固化、规则/需求审计、第三方参考审计、架构与安全设计、未知参数 schema，以及不依赖目标板 SDK 的 Host Core 源码。它不是已完成的实车系统。

## 赛题来源

- [赛题页面](https://www.aicomp.cn/tracks/4548.html)
- [官方规则 PDF](https://www.aicomp.cn/wp-content/uploads/2026/06/11%E6%99%BA%E6%85%A7%E5%9F%8E%E5%B8%82%E6%97%A0%E4%BA%BA%E9%A9%BE%E9%A9%B6%E7%AE%97%E6%B3%95%E5%BA%94%E7%94%A8%E8%B5%9B.pdf)
- 本地来源锁：`docs/sources/SOURCES.lock.yaml`
- 官方规则 SHA-256：`41cd80412a740049f15bf02bc9f9ea28b9b89f96af1d8a4335fb750f98c03988`

## 证据驱动原则

官方文件和真实测量优先于第三方代码与经验。硬件、协议、参数、模型和性能没有证据时保持未知/`BLOCKED`；规则范围不转化为任意固定配置；单元测试不证明实车能力。完整约束见 `AGENTS.md`。

## 当前状态

- `VERIFIED`：官方网页/PDF 已下载并锁定；PDF 经两种解析器确认 8 页、8 页有文本，并逐页渲染检查；下载、逐页提取和新增资料审计 Python 工具已实际运行。
- `BLOCKED`：Host Core 源码已写，但本机未发现 CMake 和 C++ 编译器，真实构建/CTest 未运行；所有目标板、摄像头、模型、通信、控制和实车任务均等待官方资料/硬件/标定/数据。
- `REJECTED`：Kesci 2018 仓库不适用于当前赛题，未克隆。
- `REFERENCE_ONLY`：`IntelligentCar_Baidu` 固定到指定 commit，仅作审计参考，整体许可证未确认。

详见 `PROJECT_STATE.md`、`docs/requirements/requirement_traceability_matrix.md` 和 `docs/requirements/blockers.md`。

## 目录

```text
official/       已锁定公开资料与组委会资料投放区
third_party/    隔离的第三方参考仓库（主仓库忽略其工作树）
docs/           环境、来源、需求、架构、安全、审计与验证文档
config/         只含有来源约束的 schema；未知值为 null
include/, src/  硬件无关 Host Core 接口与源码
mcu/            官方 MCU 工程等待区；当前无臆测实现
models/, data/  有来源资料的存放边界；禁止假模型/假数据
tools/          下载、规则提取与官方资料审计工具
tests/          纯逻辑单元测试源码；尚未编译运行
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

## 构建 Host Core

预期命令：

```powershell
cmake -S . -B build -DBUILD_TESTING=ON
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

本次主机实际执行第一条命令时退出码为 1，原因是找不到 `cmake`；因此不能把 Host Core 标为 `IMPLEMENTED_UNVERIFIED`。获得 CMake 和受支持的 C++17 编译器后才可继续构建并运行测试。

## 当前阻塞项

核心阻塞包括最终地图/物料、计算单元与 SDK、官方相机接口、MCU 工程与串口协议、执行器/急停机制、车辆几何与控制标定、感知类别/数据/模型和真实车载视频。完整 58 项见 `docs/requirements/blockers.md`。

## 第三方仓库声明

`third_party/IntelligentCar_Baidu/` 是第十九届智能车竞赛百度完全模型组工程，不是当前赛题官方代码。它明确耦合 Edgeboard 赛事版、TC264、V4L2、固定串口和原比赛任务；仓库无整体许可证，核心检测文件还带非商业限制。其源码、二进制、模型、协议和参数均未复制到正式工程。审计见 `docs/reference_audit/`。

## 为什么不能声称已完成实车系统

官方公开规则没有提供具体硬件、OS/SDK、设备节点、通信协议、模型、数据、控制参数或最终地图；项目也没有真实赛具和场地测试。Host 逻辑即使未来编译成功，也只证明软件骨架在主机可构建，不证明摄像头、AI、舵机、电机、巡线、避障、泊车、两圈运行或急停有效。

## 接入正式赛具的顺序

1. 投放并审计组委会硬件、SDK、MCU、地图、数据和模型资料。
2. 更新来源锁、事实登记、需求矩阵和 schema 实例。
3. 在真实设备上记录接口枚举与工具链环境。
4. 完成相机、车辆几何、舵机、电机、制动和停车标定。
5. 实现隔离的官方后端，先台架再低速封闭场地验证。
6. 使用真实车载数据完成离线回放和感知评估，再进行分任务/全赛道测试。

## 安全

未验证真实急停、制动和通信看门狗前，不得让本工程驱动车辆。测试按 Host 逻辑、真实回放、台架、低速封闭场地、完整赛道逐级进行；每级保留配置哈希、日志和视频。危害分析见 `docs/safety/hazard_analysis.md`。
