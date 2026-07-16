# 组委会模型审计

`models/official/metadata/model_registry.yaml` 登记 3 个逻辑模型、21 个工件，全部为 `REFERENCE_ONLY` 且许可证未确认。

- T710 两组 YOLOv3 MobileNet V1 工件，各含 Paddle/PPNC 产物和 `post.onnx`；输入证据为 NCHW float32 `[1,3,320,320]`、RGB、1/255 及源码中的 mean/std，15 个旧类别。
- 两个 `post.onnx` 字节相同，SHA-256 `f346d1679599f7dbc08aad462ccbbf35a347f4567db63fbcd1020094e80bb980`；ONNX checker 通过，IR 8、opset 11、268 节点、0 initializer。它是后处理图，输入为三个特征图及 `im_shape/scale_factor`，不是完整图像检测模型。
- FZ3B SSD MobileNet V1 记录到 `[1,3,300,300]` 与源码预处理线索；张量名、dtype、输出、转换记录仍为 `null/source_required`。

未运行真实推理、未报告精度/速度、未生成当前赛事类别映射。离线应用只读取登记表并保持检测后端 unavailable。
