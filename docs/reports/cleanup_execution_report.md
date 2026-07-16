# 安全清理执行报告

- 执行日期：2026-07-16
- dry-run：`docs/reports/cleanup_dry_run.md`
- 候选表：`docs/reports/cleanup_candidates.csv`
- 退出码：`0`
- 实际释放：`77,697,613` 字节
- 移入 `quarantine/pending_review/`：无

## 已删除

| 路径 | 字节 | 结果 |
| --- | ---: | --- |
| `official/organizer_drop/hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/extracted/DRIVER_R4.19.5001/__MACOSX` | 14,276 | 删除成功；仅 AppleDouble 元数据 |
| `official/organizer_drop/hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/extracted/DRIVER_R4.19.5001/DRIVER_R4.19.5001/.DS_Store` | 8,196 | 删除成功；仅 Finder 元数据 |
| `tmp/pdfs` | 76,170,509 | 删除成功；可由 Poppler 重新渲染 |
| `tmp/videos` | 1,205,142 | 删除成功；可由 ffmpeg 重新生成 |
| `tmp/shimo_1hXhe9FzipozjCuf.content` | 38,421 | 删除成功；已形成去除无关联系方式的结构化索引 |
| `tmp/pdfs/shimo_learning_manual/AIC2025-智慧交通无人驾驶学习手册.pdf` | 260,725 | 删除成功；文件实际为防盗链 PNG 占位图，不是 PDF |
| `docs/sources/organizer_pdf_text/...___MACOSX..._._Driver_Install_and_Uninstall_Guide.md` | 344 | 删除成功；重跑 PDF 审计后不再引用的 AppleDouble 空提取记录 |

## 执行前自动核验

- 七个解析后的绝对路径均位于 `F:\SmartCity_Driverless`。
- 原始 `DRIVER_R4.19.5001.zip` SHA-256 仍为 `76b8c13127835ba636935961a78f83a63d92cf9b2d9f563d61530be5a10dfc42`。
- 解压报告仍记录该包 `VALID`/`SKIPPED_EXISTING`，正式解压目录存在。
- PDF/视频原件及 `organizer_pdf_audit.md`、`organizer_media_audit.md` 均存在。

没有删除原始压缩包、PDF、镜像、模型、源码、许可证、哈希清单、构建/测试日志或审计报告。全项目执行前未发现 `.partial-*`，因此没有以历史记录替代现场证据进行删除。
