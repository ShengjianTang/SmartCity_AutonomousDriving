#!/usr/bin/env python3
"""Extract organizer PDF text page-by-page and record parse evidence."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path("official/organizer_drop")
OUTPUT = Path("docs/sources/organizer_pdf_text")
SUMMARY_CSV = Path("docs/sources/organizer_pdf_audit.csv")
SUMMARY_MD = Path("docs/sources/organizer_pdf_audit.md")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_name(relative: Path) -> str:
    value = relative.as_posix().removesuffix(".pdf")
    value = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._-]+", "_", value)
    return value.strip("_") + ".md"


def main() -> int:
    root = ROOT.resolve()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str | int]] = []
    for path in sorted(root.rglob("*.pdf"), key=lambda item: item.as_posix().lower()):
        relative = path.relative_to(root)
        digest = sha256(path)
        pages = 0
        text_pages = 0
        text_chars = 0
        status = "PARSED"
        error = ""
        extracted: list[str] = [
            f"# PDF 逐页文本：{relative.as_posix()}",
            "",
            f"- SHA-256：`{digest}`",
            "",
        ]
        try:
            reader = PdfReader(path)
            pages = len(reader.pages)
            for index, page in enumerate(reader.pages, start=1):
                try:
                    text = page.extract_text() or ""
                except Exception as page_error:
                    text = f"[PAGE_EXTRACTION_ERROR: {type(page_error).__name__}: {page_error}]"
                if text.strip() and not text.startswith("[PAGE_EXTRACTION_ERROR"):
                    text_pages += 1
                    text_chars += len(text)
                normalized_text = "\n".join(line.rstrip() for line in text.splitlines())
                extracted.extend([f"## 第 {index} 页", "", normalized_text, ""])
        except Exception as parse_error:
            status = "PARSE_FAILED"
            error = f"{type(parse_error).__name__}: {parse_error}"
            extracted.extend(["## 解析失败", "", error, ""])
        output_path = OUTPUT / safe_name(relative)
        output_path.write_text("\n".join(extracted).rstrip() + "\n", encoding="utf-8")
        rows.append(
            {
                "relative_path": relative.as_posix(),
                "sha256": digest,
                "size_bytes": path.stat().st_size,
                "pages": pages,
                "text_pages": text_pages,
                "text_characters": text_chars,
                "status": status,
                "error": error,
                "text_output": output_path.as_posix(),
            }
        )

    with SUMMARY_CSV.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
    with SUMMARY_MD.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# 组委会 PDF 解析审计\n\n")
        stream.write(f"- PDF 文件：{len(rows)}\n")
        stream.write(f"- pypdf 可解析：{sum(row['status'] == 'PARSED' for row in rows)}\n")
        stream.write(f"- 解析失败：{sum(row['status'] != 'PARSED' for row in rows)}\n")
        stream.write("- 文本提取不替代版面核验；关键 PDF 另行使用 Poppler 渲染检查。\n\n")
        stream.write("| 文件 | 页数 | 有文本页 | 字符 | 状态 | 逐页文本 |\n")
        stream.write("| --- | ---: | ---: | ---: | --- | --- |\n")
        for row in rows:
            stream.write(f"| `{row['relative_path']}` | {row['pages']} | {row['text_pages']} | {row['text_characters']} | {row['status']} | `{row['text_output']}` |\n")
    failures = sum(row["status"] != "PARSED" for row in rows)
    print(f"pdfs={len(rows)} parsed={len(rows)-failures} failed={failures}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
