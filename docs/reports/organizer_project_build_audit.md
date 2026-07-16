# 组委会旧工程构建静态审计

## T710

需要 PkgConfig/glib-2.0、OpenCV、libserial、PPNC、ONNX，使用 Linux `/usr/local` 路径和 `-mcpu=native -flto -pthread`。定义 `boot/camera/img2video/calibration/imging/detection/collection/icar/running` 等目标。

## FZ3B

需要 PkgConfig/glib-2.0、OpenCV、Paddle Lite 和串口库；目标集合与 T710 相近但没有 `running`。

## 判定

两者都是为特定 Linux/板端环境准备的旧工程。Windows Host 不具备这些 SDK/ABI；不得通过删除依赖、伪造包或链接随包旧二进制来制造“构建成功”。
