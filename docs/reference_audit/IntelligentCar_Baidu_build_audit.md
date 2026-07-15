# IntelligentCar_Baidu 构建审计

## 构建声明

| 子工程 | 标准/目标 | 依赖 | 入口 |
| --- | --- | --- | --- |
| `race/` | CMake ≥3.5，C++14，`INCAR.RUN` | OpenCV、PkgConfig/GLib、pthread、ONNX Runtime、PPNC runtime | `race/src/main.cpp` |
| `self/` | CMake ≥3.5，C++14，`SWAN.RUN` | OpenCV、pthread；ONNX 部分默认注释 | `self/src/src/demo.cpp` |
| HSV/LDC/ImageCollect 工具 | 各自 CMake | OpenCV 等 | 各工具 `src/*.cpp` |

## 不可复现点

- `race/CMakeLists.txt` 硬编码 `/usr/local/include/onnx`、`/usr/local/lib/onnx` 和 `/usr/local/lib/ppnc`。
- `race/onnx/README.md` 要求以 `sudo` 复制文件到 `/usr/local`，且声明其中库为 x86；主 README 同时称比赛工程面向 Edgeboard，架构边界需要原作者工具链才能澄清。
- 仓库同时提交 x86/aarch64 ONNX Runtime 1.17.1 补充库，以及 `race/onnx` 的 1.16.3 文件，版本和使用路径不统一。
- PPNC 模型依赖预编译 `.so`、`.tar`、`.ro`、`.params` 和运行时库，缺少本仓库可独立重建这些产物的完整来源链。
- 配置文件由终端交互选择，非法输入没有明确处理；相对路径假定从 `race/build` 启动。
- `compile.sh` 会递归删除相对 `../build`，`init.sh` 还会删除 `../img/ImgAll`；本次审计未运行这些脚本，也未修改仓库。

## 当前主机结果

- 当前 Windows 主机 PATH 未发现 CMake、GCC/G++、Clang、MSVC 或 Ninja。
- 即使补齐主机编译器，`race/` 仍依赖 Linux V4L2、termios、pthread、GLib、PPNC 和指定预编译库，不能直接在当前主机完成有意义的目标构建。
- 因此未执行第三方编译，构建状态为 `BLOCKED`；这不影响完成静态审计。

## 迁移判断

构建文件只可作为第三方 `REFERENCE_ONLY` 证据。当前项目应维持独立的 Host Core 构建，不链接这些预编译库，不复制 CMake 片段，并在获得官方目标板 SDK 后新建隔离后端。
