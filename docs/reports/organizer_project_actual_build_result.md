# 组委会旧工程实际构建结果

2026-07-16 在原源码之外分别使用 `build/organizer_project/t710_attempt3` 与 `fz3b_attempt3` 配置。

| 项目 | 编译器探测 | 配置 | 构建 | 结论 |
| --- | --- | --- | --- | --- |
| T710 | C/C++ Clang 21.1.0 通过 | 失败：缺 `pkg-config`/`glib-2.0` 与 OpenCV | 未启动 | `BLOCKED` |
| FZ3B | C/C++ Clang 21.1.0 通过 | 失败：缺 `pkg-config`/`glib-2.0` 与 OpenCV | 未启动 | `BLOCKED` |

详细摘要见 `logs/setup/organizer_t710_configure.log`、`organizer_fz3b_configure.log`。原工程未修改。随包 AArch64 ELF 不计入本次结果。
