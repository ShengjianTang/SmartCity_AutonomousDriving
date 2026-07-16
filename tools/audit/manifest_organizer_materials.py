#!/usr/bin/env python3
"""Create a deterministic evidence manifest for organizer-provided materials."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ARCHIVE_SUFFIXES = (".zip", ".rar", ".7z", ".tar", ".tgz", ".tar.gz", ".tar.xz", ".tar.bz2")
DOCUMENT_SUFFIXES = {".pdf", ".txt", ".md", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"}
SOURCE_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".py", ".sh", ".ps1", ".cmake",
    ".json", ".yaml", ".yml", ".xml", ".pro", ".pri", ".s", ".asm", ".ld", ".java",
}
MODEL_SUFFIXES = {".onnx", ".pt", ".pth", ".weights", ".engine", ".tflite", ".pb", ".pdmodel", ".nb"}
IMAGE_SUFFIXES = {".img", ".iso", ".pac", ".wic", ".vhd", ".vhdx"}
TOOL_SUFFIXES = {".exe", ".msi", ".dll", ".sys", ".bat", ".cmd"}
YEAR_PATTERN = re.compile(r"(?<!\d)(?:19|20)\d{2}(?:th)?(?!\d)", re.IGNORECASE)
VERSION_PATTERN = re.compile(r"(?<![A-Za-z0-9])v?\d+(?:[._-]\d+){1,3}(?![A-Za-z0-9])", re.IGNORECASE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def has_archive_suffix(name: str) -> bool:
    lowered = name.lower()
    return any(lowered.endswith(suffix) for suffix in ARCHIVE_SUFFIXES)


def flag(value: bool) -> str:
    return "true" if value else "false"


def format_modified_time(epoch_seconds: float) -> str:
    try:
        return datetime.fromtimestamp(epoch_seconds).astimezone().isoformat()
    except (OSError, OverflowError, ValueError):
        return f"UNREPRESENTABLE_EPOCH:{epoch_seconds}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("official/organizer_drop"))
    parser.add_argument("--output-dir", type=Path, default=Path("docs/sources"))
    args = parser.parse_args()

    root = args.root.resolve()
    output_dir = args.output_dir.resolve()
    if not root.is_dir():
        raise SystemExit(f"organizer material root does not exist: {root}")
    output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str | int]] = []
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.as_posix().lower()):
        relative = path.relative_to(root).as_posix()
        stat = path.stat()
        suffix = path.suffix.lower()
        lowered_path = relative.lower()
        years = sorted(set(YEAR_PATTERN.findall(relative)))
        versions = sorted(set(VERSION_PATTERN.findall(relative)))
        is_archive = has_archive_suffix(path.name)
        is_extracted = "extracted" in {part.lower() for part in path.relative_to(root).parts}
        rows.append(
            {
                "relative_path": relative,
                "file_name": path.name,
                "extension": "".join(path.suffixes).lower(),
                "size_bytes": stat.st_size,
                "sha256": sha256(path),
                "modified_time": format_modified_time(stat.st_mtime),
                "is_archive": flag(is_archive),
                "is_document": flag(suffix in DOCUMENT_SUFFIXES),
                "is_source": flag(suffix in SOURCE_SUFFIXES or path.name.lower() in {"cmakelists.txt", "makefile"}),
                "is_model": flag(suffix in MODEL_SUFFIXES or "/models/" in f"/{lowered_path}/"),
                "is_image": flag(suffix in IMAGE_SUFFIXES or ".pac." in path.name.lower() or "board_image" in lowered_path),
                "is_tool": flag(suffix in TOOL_SUFFIXES or "工具" in relative or "installer" in path.name.lower()),
                "is_extracted": flag(is_extracted),
                "year_tokens": ";".join(years),
                "version_tokens": ";".join(versions),
            }
        )

    fieldnames = list(rows[0].keys()) if rows else [
        "relative_path", "file_name", "extension", "size_bytes", "sha256", "modified_time",
        "is_archive", "is_document", "is_source", "is_model", "is_image", "is_tool",
        "is_extracted", "year_tokens", "version_tokens",
    ]
    csv_path = output_dir / "organizer_material_manifest.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    checksum_path = output_dir / "organizer_material_checksums.sha256"
    with checksum_path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(f"{row['sha256']} *official/organizer_drop/{row['relative_path']}\n")

    counts = Counter()
    for row in rows:
        for key in ("is_archive", "is_document", "is_source", "is_model", "is_image", "is_tool", "is_extracted"):
            if row[key] == "true":
                counts[key] += 1
    total_bytes = sum(int(row["size_bytes"]) for row in rows)
    markdown_path = output_dir / "organizer_material_manifest.md"
    with markdown_path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# 组委会资料清单\n\n")
        stream.write(f"- 扫描根目录：`official/organizer_drop/`\n")
        stream.write(f"- 文件数量：{len(rows)}\n")
        stream.write(f"- 文件总大小：{total_bytes} 字节\n")
        stream.write(f"- 压缩包：{counts['is_archive']}\n")
        stream.write(f"- 文档：{counts['is_document']}\n")
        stream.write(f"- 源码候选：{counts['is_source']}\n")
        stream.write(f"- 模型候选：{counts['is_model']}\n")
        stream.write(f"- 镜像候选：{counts['is_image']}\n")
        stream.write(f"- 工具程序候选：{counts['is_tool']}\n")
        stream.write(f"- 解压派生文件：{counts['is_extracted']}\n\n")
        stream.write("分类只表示文件类型候选，不代表 2026 适用性、许可证或功能已经确认。完整字段见 CSV。\n\n")
        stream.write("| 相对路径 | 大小 | SHA-256 | 类型 | 年份/版本 |\n")
        stream.write("| --- | ---: | --- | --- | --- |\n")
        for row in rows:
            kinds = [name.removeprefix("is_") for name in ("is_archive", "is_document", "is_source", "is_model", "is_image", "is_tool", "is_extracted") if row[name] == "true"]
            tokens = "; ".join(filter(None, (str(row["year_tokens"]), str(row["version_tokens"])))) or "-"
            escaped_path = str(row["relative_path"]).replace("|", "\\|")
            stream.write(f"| `{escaped_path}` | {row['size_bytes']} | `{row['sha256']}` | {', '.join(kinds) or '-'} | {tokens} |\n")

    print(f"files={len(rows)} bytes={total_bytes} csv={csv_path} markdown={markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
