# 工程初始化与审计执行报告

## 1. 实际完成的操作

- 审计主机、工具链、资源和网络；初始化 Git 和本地 `.venv`。
- 建立任务指定的目录、忽略规则、长期约束和状态记录。
- 实际下载、校验、解析并渲染检查官方网页/PDF；建立来源锁和幂等下载脚本。
- 实际克隆并锁定第三方仓库；记录 Kesci 来源为 `REJECTED`；完成五类静态审计。
- 逐页提取官方规则，建立摘要、31 条需求矩阵、15 项事实登记和 58 项阻塞清单。
- 建立架构、状态机、安全/危害分析、6 份配置 schema 和资料投放审计工具。
- 编写 Host Core 和单元测试源码；实际尝试构建并保留工具链阻塞证据。
- 完成 Python 语法、YAML/CSV、哈希、必需文件、第三方洁净、大文件、密钥和高风险词检查。

## 2. 下载和克隆结果

- 官方网页：`official/public/webpages/track_4548.html`
- 官方 PDF：`official/public/rules/智慧城市无人驾驶算法应用赛_官方规则.pdf`
- PDF SHA-256：`41cd80412a740049f15bf02bc9f9ea28b9b89f96af1d8a4335fb750f98c03988`
- 参考仓库：`third_party/IntelligentCar_Baidu/`
- 参考 commit：`be05851d04154d374e46687e10809e13e997f712`
- 未解决的下载/克隆失败：无。
- 已恢复故障：Poppler 包装脚本首次路径错误，临时 PDF 未被误标为成功；改用直接 Poppler 可执行文件和 pypdf 后完成验证与原子保存，失败日志已保留。

## 3. 创建的主要文件

- 状态/约束：`AGENTS.md`、`README.md`、`PROJECT_STATE.md`、`CHANGELOG.md`。
- 来源/需求：`docs/sources/*.yaml`、`docs/requirements/`、`docs/reference_audit/`。
- 架构/安全：`docs/architecture/`、`docs/safety/hazard_analysis.md`。
- 工具：`tools/download/download_public_sources.py`、`tools/audit/extract_rules_by_page.py`、`tools/audit/audit_new_official_materials.py`、两套 bootstrap 脚本。
- 配置：`config/schemas/*.yaml`。
- Host Core：`include/smart_city_car/`、`src/core/`、`src/decision/`、`src/logging/`、`src/safety/`、`tests/unit/host_core_tests.cpp`、`CMakeLists.txt`。

## 4. 构建与测试结果

| 命令/检查 | 退出码 | 结果 |
| --- | ---: | --- |
| 下载脚本幂等检查 | 0 | 两个来源哈希正确，未覆盖 |
| 规则逐页提取 | 0 | 8 页，未使用 OCR |
| 新资料审计 | 0 | 当前投放文件 0 |
| Python `compileall` | 0 | 工具脚本语法通过 |
| YAML/CSV/哈希语义检查 | 0 | 31 条需求、9 个 YAML、2 个来源哈希通过 |
| `cmake -S . -B build -DBUILD_TESTING=ON` | 1 | 找不到 CMake；未编译、未运行 CTest |

## 5. 当前可以确认的事实

- 官网两处来源均曾返回 HTTP 200；本地 HTML 为 17,471 字节，PDF 为 776,654 字节。
- PDF 文件头为 `%PDF-`，两种解析器均报告 8 页，8 页都有内嵌文本；8 页渲染图均已目视检查。
- 根目录原有 PDF 与官网下载 PDF 哈希完全相同。
- 官方规则确认彩色摄像头直连计算单元、单片机与计算单元通信并直接控制执行器；没有给出具体型号、SDK 或协议。
- 第三方仓库工作树干净，锁定 commit 如上；它无根许可证文件，且不是当前赛题官方工程。
- 当前 PATH 找不到 CMake 和已探测的 C++ 编译器。

## 6. 当前阻塞项

- 组委会最终地图/物料、赛区形式、赛具、基础工程、数据、模型和计时接口。
- 计算单元/OS/SDK/相机接口，MCU/串口协议/执行器/急停机制。
- 相机、车辆几何、舵机、电机、编码器（是否存在仍未知）、制动、转弯和停车标定。
- 最终类别、标注、真实车载视频、权重、精度和板端性能。
- 本机 CMake 和 C++17 编译器，因而 Host Core 构建与 CTest 阻塞。

## 7. 当前工程状态

- `VERIFIED`：公开来源、PDF 结构/页数/渲染、哈希；已运行的 Python 工具和语义检查；第三方版本/洁净静态事实。
- `IMPLEMENTED_UNVERIFIED`：无；Host Core 未编译，不使用该状态。
- `BLOCKED`：Host Core 构建，以及全部真实硬件、AI、通信、控制和场地任务。
- `REJECTED`：Kesci 2018 仓库。
- `REFERENCE_ONLY`：`IntelligentCar_Baidu` 及其全部硬件、协议、参数、模型和算法实现。

## 8. 下一步

1. 提供可调用的 CMake/C++17 工具链或授权安装项目本地工具链，随后真实构建并运行 CTest。
2. 将组委会资料按 `official/organizer_drop/README.md` 投放并运行审计，更新事实与阻塞项。
3. 获取实际赛具后先做接口枚举和完整标定，再实现官方后端并按 Host、回放、台架、低速场地、完整赛道逐级验证。
