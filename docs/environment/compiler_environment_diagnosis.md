# 编译环境诊断

## 结论

原先“主机找不到 CMake/C++ 编译器”的阻塞已在项目局部环境中解除。当前使用 `.venv` 内 CMake/Ninja 和 Zig 0.16.0 的 `c++` 前端，Host Core、离线应用与测试已真实编译链接。

## 必要设置

- `python-zig.exe` 是多命令入口，CMake 必须同时设置 `CMAKE_CXX_COMPILER_ARG1=c++`；旧工程包含 C 时另设 `CMAKE_C_COMPILER_ARG1=cc`。
- Zig 默认全局缓存目录在受限环境不可写，构建时显式将 `ZIG_GLOBAL_CACHE_DIR`、`ZIG_LOCAL_CACHE_DIR` 指向 `build/`。
- Windows 静态库工具使用 `tools/toolchains/zig-ar.cmd` 与 `zig-ranlib.cmd`。
- CMake 显式使用 `.venv/Scripts/ninja.exe`，避免依赖系统 PATH。

首次缺少 `c++` 子命令和缓存权限的失败记录被保留；它们不是源码失败。此工具链只证明 Windows Host 构建，不证明随包旧工程或目标板构建。
