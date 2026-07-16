# 组委会资料总审计

## 范围与结论

2026-07-16 对 `official/organizer_drop/` 做文件级清点、SHA-256、压缩包完整性/路径安全、PDF 文本与全页渲染、视频元数据/抽帧、源码/模型/许可证静态审计。原始投放为 33 个文件、22,960,347,578 字节；解压后首轮清单为 1,210 个文件、114,392,891,318 字节。安全清理后重算为 1,146 个文件、114,392,868,846 字节，恰好少 63 个 AppleDouble 文件和 1 个 `.DS_Store`（22,472 字节）。12 个原始压缩包均完成验证和隔离解压，失败数 0。

机器可读证据：

- `docs/sources/organizer_material_manifest.csv`
- `docs/sources/organizer_material_checksums.sha256`
- `docs/sources/archive_extraction_report.json`
- `docs/sources/organizer_pdf_audit.csv`
- `docs/sources/organizer_media_audit.csv`
- `docs/sources/organizer_onnx_structure.json`

## 可用边界

- 2025 T710/FZ3B 工程、模型、场地图和教程只作 `REFERENCE_ONLY`，不能替代 2026 最终赛期资料或真实硬件证据。
- 两个 ONNX 后处理图结构检查通过，但不等于完整检测模型可运行或有合法复用许可。
- 控制板 PDF 与旧 `uart.hpp` 在最大帧长、按键地址和实际发送长度上存在冲突，因此未生成正式串口实现。
- 唯一明确许可证文件属于 USB Image Tool；旧工程和模型没有可确认的标准复用许可。

安全清理仅删除 AppleDouble/Finder 元数据和可再生临时渲染/石墨占位文件，共 77,697,613 字节；原始压缩包、源码、模型、PDF、视频和审计证据均保留。详见 `docs/reports/cleanup_execution_report.md`。
