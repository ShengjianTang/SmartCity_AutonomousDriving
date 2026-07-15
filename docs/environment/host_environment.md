# 主机环境审计

- 审计时间：2026-07-15T19:38:50+08:00
- 工作区绝对路径：`F:\SmartCity_Driverless`
- 初始目录状态：非空；仅发现 `11智慧城市无人驾驶算法应用赛.pdf`
- 初始 Git 状态：未初始化；随后按任务要求执行了 `git init`
- 当前执行账户：`LAPTOP-GQLODGN3\CodexSandboxOffline`
- 操作系统：Microsoft Windows 11 家庭版 中文版，版本 `10.0.26200`，构建 `26200`
- OS/进程架构：x64/x64
- CPU：AMD Ryzen 7 7840H with Radeon 780M Graphics，64 位
- 审计时可用物理内存：15,010,131,968 字节
- F: 可用空间：367,707,041,792 字节；总空间：535,570,673,664 字节

## 工具链

| 工具 | 探测结果 | 证据/版本 |
| --- | --- | --- |
| Git | 存在 | `git version 2.53.0.windows.2` |
| Python | 存在 | `Python 3.12.7`；路径 `F:\pytorch\conda\condaDownload\python.exe` |
| 项目虚拟环境 | 已创建 | `.venv`，Python 3.12.7 |
| CMake | 当前 PATH 未发现 | `BLOCKED` |
| GCC/G++ | 当前 PATH 未发现 | `BLOCKED` |
| Clang/Clang++/clang-cl | 当前 PATH 未发现 | `BLOCKED` |
| MSVC `cl` / MSBuild / nmake | 当前 PATH 未发现；vswhere 未发现带 C++ 工具的安装 | `BLOCKED` |
| Make | 当前 PATH 未发现 | `BLOCKED` |
| Ninja | 当前 PATH 未发现 | `BLOCKED` |
| PowerShell | 存在 | Windows PowerShell `powershell.exe` |
| curl/wget | 名称可解析 | 均为 PowerShell `Invoke-WebRequest` 别名，不是独立可执行文件 |
| OpenCV (Python `cv2`) | 探测所用 Python 中未发现 | `BLOCKED`；未推断系统其他位置 |
| Poppler | 捆绑运行时中存在 | `pdfinfo.exe` 与 `pdftoppm.exe` 可直接调用 |
| pypdf/pdfplumber | 捆绑运行时中存在 | pypdf 6.10.0；pdfplumber 0.11.9 |

## 网络可达性

沙箱内网络探测因隔离策略失败；经授权在沙箱外执行相同的只读 HEAD 请求后：

| 目标 | HTTP 状态 | 最终 URL | 结论 |
| --- | ---: | --- | --- |
| GitHub | 200 | `https://github.com/` | 可达 |
| 赛题官网 | 200 | `https://www.aicomp.cn/tracks/4548.html` | 可达 |

## 边界说明

- “当前 PATH 未发现”不等同于断言主机磁盘中绝对不存在该工具，只说明本次可重复探测无法调用它。
- 目标计算单元、目标操作系统、编译器和 AI SDK 均未由本主机审计推断。
- 由于当前未发现 CMake 和 C++ 编译器，Host Core 的真实构建暂时标记为 `BLOCKED`，后续仍会建立不依赖目标硬件的源码和测试骨架。
