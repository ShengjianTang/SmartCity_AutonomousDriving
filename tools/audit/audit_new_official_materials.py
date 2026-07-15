#!/usr/bin/env python3
"""Inventory organizer-provided files without modifying or trusting them."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import tempfile


ROOT = Path(__file__).resolve().parents[2]
SCAN_ROOTS = (
    ROOT / "official" / "organizer_drop" / "maps",
    ROOT / "official" / "organizer_drop" / "hardware",
    ROOT / "official" / "organizer_drop" / "sdk",
    ROOT / "official" / "organizer_drop" / "examples",
    ROOT / "official" / "organizer_drop" / "datasets",
    ROOT / "official" / "organizer_drop" / "models",
    ROOT / "official" / "organizer_drop" / "notices",
    ROOT / "mcu" / "official",
)
OUTPUT = ROOT / "docs" / "sources" / "new_material_audit.md"
REVIEW_EXTENSIONS = {
    ".pdf", ".md", ".markdown", ".txt", ".rst",
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp",
    ".py", ".sh", ".ps1", ".cmake", ".json", ".yaml", ".yml",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def timestamp(value: float) -> str:
    return datetime.fromtimestamp(value, timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def main() -> int:
    files: list[dict[str, object]] = []
    for scan_root in SCAN_ROOTS:
        scan_root.mkdir(parents=True, exist_ok=True)
        for path in sorted((item for item in scan_root.rglob("*") if item.is_file()), key=lambda item: item.as_posix()):
            stat = path.stat()
            extension = path.suffix.lower() or "[no extension]"
            files.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "size": stat.st_size,
                    "sha256": sha256(path),
                    "modified": timestamp(stat.st_mtime),
                    "extension": extension,
                    "pending": extension in REVIEW_EXTENSIONS,
                }
            )

    counts = Counter(str(item["extension"]) for item in files)
    lines = [
        "# 新增官方资料审计",
        "",
        f"- 扫描时间：{timestamp(datetime.now(timezone.utc).timestamp())}",
        f"- 扫描文件数：{len(files)}",
        "- 信任边界：本报告只记录投放文件，不自动认定其为官方事实。",
        "- 原始文件修改：未修改。",
        "",
        "## 扩展名统计",
        "",
    ]
    if counts:
        lines.extend(["| 扩展名 | 数量 |", "| --- | ---: |"])
        lines.extend(f"| `{extension}` | {count} |" for extension, count in sorted(counts.items()))
    else:
        lines.append("当前未发现投放文件。")

    lines.extend(["", "## 文件清单", ""])
    if files:
        lines.extend([
            "| 路径 | 大小（字节） | SHA-256 | 修改时间（UTC） | 分类 | 状态 |",
            "| --- | ---: | --- | --- | --- | --- |",
        ])
        for item in files:
            state = "PENDING_REVIEW" if item["pending"] else "INVENTORIED"
            lines.append(
                f"| `{item['path']}` | {item['size']} | `{item['sha256']}` | {item['modified']} | "
                f"`{item['extension']}` | {state} |"
            )
    else:
        lines.append("无。")

    pending = [item for item in files if item["pending"]]
    lines.extend(["", "## 待人工内容审计", ""])
    if pending:
        lines.extend(f"- `{item['path']}`" for item in pending)
    else:
        lines.append("无。")

    content = "\n".join(lines) + "\n"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="\n", prefix=f".{OUTPUT.name}.", suffix=".part",
        dir=OUTPUT.parent, delete=False
    ) as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    os.replace(temporary, OUTPUT)
    print(f"scanned={len(files)} pending_review={len(pending)} output={OUTPUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
