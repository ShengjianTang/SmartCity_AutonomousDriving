# 安全清理 dry-run

- 生成日期：2026-07-16
- 范围：仅 `F:\SmartCity_Driverless`
- 原则：原始压缩包、PDF、镜像、模型、源码、许可证、哈希清单、成功构建/测试日志和审计报告均不删除。
- 明细：`docs/reports/cleanup_candidates.csv`

## 建议执行

| 路径 | 字节 | 理由 | 证明 |
| --- | ---: | --- | --- |
| `official/.../extracted/DRIVER_R4.19.5001/__MACOSX` | 14,276 | 63 个 AppleDouble 资源叉元数据文件 | 原始 `DRIVER_R4.19.5001.zip` 存在，SHA-256 已登记且解压报告为 `VALID`/`SKIPPED_EXISTING` |
| `official/.../extracted/DRIVER_R4.19.5001/DRIVER_R4.19.5001/.DS_Store` | 8,196 | Finder 目录元数据 | 同上；实际驱动文件保留 |
| `tmp/pdfs` | 76,170,509 | 已完成 PDF 视觉审计后留下的可再生渲染图/联系表 | 16 份现存 PDF 和 `organizer_pdf_audit.*` 均保留 |
| `tmp/videos` | 1,205,142 | 已完成视频视觉审计后留下的可再生联系表 | 9 份原始 MP4 和 `organizer_media_audit.*` 均保留 |

建议删除合计 `77,398,123` 字节。删除不会改变任何 `official/organizer_drop` 原始文件；仅清理成功解压目录内的 OS 元数据和 `tmp/` 下工具输出。

## 石墨审计后追加候选

石墨正文解析完成后新增两项临时文件：38,421 字节正文快照已转为去除无关联系方式的结构化索引；260,725 字节所谓 PDF 实为防盗链 PNG 占位图。两项均位于 `tmp/`、可再生成且不是官方附件原件，建议删除合计 `299,146` 字节。

清理后重跑 PDF 审计，16 份现存 PDF 全部解析成功；另识别到 344 字节的旧 AppleDouble 空文本提取记录。它只指向已删除的 `._*.pdf` 元数据且不再被审计表引用，追加为可再生删除候选。全部候选合计 `77,697,613` 字节。

## 明确不执行

- 全项目未发现 `.partial-*`，因此没有基于历史记忆删除任何大文件。
- `build/organizer_project/` 保留：它包含本轮两套旧工程配置失败的可复现缓存，且没有对应成功旧工程构建可替代。
- 两组 Zig 缓存暂保留：虽然可再生成，但早期失败/成功尝试的边界未能仅凭目录证明，未满足自动删除的严格条件。
- 未发现需要移入 `quarantine/pending_review/` 的唯一或来源不明文件；不确定项原地保留。

## 执行前验证条件

1. 七个待删路径的解析绝对路径必须均位于 `F:\SmartCity_Driverless`。
2. `DRIVER_R4.19.5001.zip` 的哈希必须仍为 `76b8c13127835ba636935961a78f83a63d92cf9b2d9f563d61530be5a10dfc42`。
3. `docs/sources/archive_extraction_report.md` 必须仍记录该压缩包 `VALID` 且正式解压目录存在。
4. 原始 PDF、MP4 和审计报告必须存在。
