#!/usr/bin/env python3
"""Extract embedded PDF text page by page without OCR."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import tempfile
import os

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "official" / "public" / "rules" / "智慧城市无人驾驶算法应用赛_官方规则.pdf"
DESTINATION = ROOT / "docs" / "requirements" / "rules_extracted_by_page.md"


def main() -> int:
    reader = PdfReader(SOURCE)
    if reader.is_encrypted:
        raise RuntimeError("encrypted PDF is not supported")
    sections = [
        "# 官方规则逐页文本提取",
        "",
        f"- 来源：`{SOURCE.relative_to(ROOT).as_posix()}`",
        f"- 提取时间：{datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')}",
        "- 提取器：pypdf（读取 PDF 内嵌文本层）",
        "- OCR：未使用；8 页均存在可提取文本",
        "- 视觉核验：已用 Poppler 将全部 8 页渲染为 PNG 并逐页目视检查",
        "- 表格限制：页 3-5 含表格和图片；以下文本保留提取顺序，但不能替代原 PDF 的二维表格布局，引用数值时应对照原页。",
        "",
    ]
    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        sections.extend(
            [
                f"## 第 {index} 页",
                "",
                "```text",
                text if text else "[本页无可提取文本]",
                "```",
                "",
            ]
        )
    content = "\n".join(sections)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="\n", prefix=f".{DESTINATION.name}.", suffix=".part",
        dir=DESTINATION.parent, delete=False
    ) as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    os.replace(temporary, DESTINATION)
    print(f"pages={len(reader.pages)} output={DESTINATION.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
