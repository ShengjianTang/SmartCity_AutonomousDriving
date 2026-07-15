# PROJECT_STATE

- 更新时间：2026-07-15T20:35:05+08:00
- Git 分支：`master`
- Git commit：未产生首个 commit（unborn repository）
- 当前官方需求数量：31
- 需求矩阵状态：`VERIFIED` 4、`BLOCKED` 23、`NOT_STARTED` 4

## 已完成工作

- 完成主机、工具链、磁盘、内存和网络可达性审计。
- 初始化 Git，建立目录、忽略规则和本地 `.venv`。
- 下载、校验并锁定官方网页与规则 PDF；逐页渲染检查。
- 建立幂等下载、规则提取和新增官方资料审计脚本，并实际运行。
- 克隆并锁定第三方参考仓库；完成版本、构建、硬件、复用和许可证审计。
- 建立规则摘要、31 条需求追踪矩阵、事实登记和 58 项阻塞清单。
- 建立长期代理约束、架构、状态机、安全策略和 6 份配置 schema。
- 写入 C++17 Host Core 源码和单元测试源码；真实构建因工具链缺失而阻塞。

## 已下载资料

| 资料 | 本地路径 | SHA-256/状态 |
| --- | --- | --- |
| 赛题网页 | `official/public/webpages/track_4548.html` | `8ebbfc4e95cf0cf22e0752499239d8302e11d1a73085b8e9cbb7d18c9bdc8f7f` / VERIFIED |
| 官方规则 PDF | `official/public/rules/智慧城市无人驾驶算法应用赛_官方规则.pdf` | `41cd80412a740049f15bf02bc9f9ea28b9b89f96af1d8a4335fb750f98c03988` / VERIFIED |

根目录原有 PDF 与官网下载 PDF 哈希一致，已保留且不作为第二份来源记录。

## 第三方版本

- 路径：`third_party/IntelligentCar_Baidu/`
- commit：`be05851d04154d374e46687e10809e13e997f712`
- 分支：`master`
- 工作树：克隆后干净
- 状态：`REFERENCE_ONLY`
- 许可证：`UNVERIFIED`

## VERIFIED

- 两个公开来源的 HTTP、大小、Content-Type、SHA-256 和本地文件有效性。
- PDF `%PDF-` 文件头、pypdf/Poppler 均为 8 页、8 页文本可提取、全页渲染可读。
- 下载脚本幂等校验退出码 0；规则提取脚本退出码 0；新增资料审计脚本退出码 0。
- 来源锁、事实表和 6 份 schema 共 9 个 YAML 文件已实际解析通过。
- 第三方 commit/分支/remote/干净状态及许可证文件缺失的静态检查结果。

## IMPLEMENTED_UNVERIFIED

- 无。Host Core 源码存在，但按照任务约束，未真实编译前不使用此状态。

## BLOCKED

- Host Core 构建与 CTest：主机找不到 CMake，且 PATH 未发现 C++ 编译器。
- 真实相机、板端 AI、串口、舵机、电机、速度闭环、巡线、避障、道闸、行人、停车、两圈运行、性能和最终合规性。
- 目标板/SDK、MCU/协议、最终地图与物料、全套实车标定、感知数据/模型和真实回放视频。

## REJECTED

- `https://github.com/Kesci/nanjing_AI_competition_2018.git`：2018 年其他比赛，未克隆、未依赖。

## REFERENCE_ONLY

- `IntelligentCar_Baidu`：硬件/任务/许可证均不满足直接复用条件。

## 最近构建和测试

| 命令 | 退出码 | 结果 |
| --- | ---: | --- |
| `.venv\Scripts\python.exe tools\download\download_public_sources.py` | 0 | 两个已锁定文件校验通过并保留 |
| `.venv\Scripts\python.exe tools\audit\extract_rules_by_page.py` | 0 | 提取 8 页内嵌文本 |
| `.venv\Scripts\python.exe tools\audit\audit_new_official_materials.py` | 0 | 扫描 0 个投放文件 |
| Python YAML/CSV 校验 | 0 | 31 条需求；9 个 YAML 文件解析通过 |
| `cmake -S . -B build -DBUILD_TESTING=ON` | 1 | `cmake` 命令不存在；未编译、未运行 CTest |

## 下一步可自动执行

- 在用户提供 CMake 和 C++17 编译器或确认可安装本地工具链后，配置、构建并运行 CTest，修复真实编译问题。
- 新资料投放后运行清点、哈希和内容审计，再更新证据系统。
- 持续运行 Python 语法、YAML、CSV、哈希和高风险词终检。

## 下一步必须由用户/组委会/真实硬件提供

- 组委会硬件/SDK/MCU/地图/数据/模型/通知。
- 实际赛具、接口枚举、相机与车辆标定、真实车载视频和封闭场地测试机会。
- 若要求在本机完成 C++ 构建：可调用的 CMake 与 C++17 工具链。

## 当前最高风险

真实安全停止链路、控制协议和车辆标定均未知。任何把第三方参数或 Host 语义直接连接到实车的行为都可能导致车辆失控，必须禁止。
