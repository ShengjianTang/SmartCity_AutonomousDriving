#!/usr/bin/env python3
"""Incrementally audit the four user-supplied PDFs at the repository root.

The script deliberately reads only the four named PDFs, the locked current-rule
copy, and pre-existing small indexes.  It does not walk or re-hash the organizer
material tree.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any

from pypdf import PdfReader
import yaml


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs" / "sources" / "four_new_documents_incremental_audit.json"
MANIFEST = ROOT / "docs" / "sources" / "organizer_material_manifest.csv"
SOURCE_LOCK = ROOT / "docs" / "sources" / "SOURCES.lock.yaml"
SHIMO_INDEX = ROOT / "docs" / "sources" / "shimo_attachment_index.json"
LOCKED_CURRENT_RULES = ROOT / "official" / "public" / "rules" / "智慧城市无人驾驶算法应用赛_官方规则.pdf"
DOCUMENTS = (
    {
        "path": ROOT / "2025-AIC-智慧城市无人驾驶算法应用赛-技术分享.-20250914-2.pdf",
        "classification": "LEGACY_2025_ORGANIZER_REFERENCE",
        "render_key": "technical_share",
    },
    {
        "path": ROOT / "AIC2025-智慧交通无人驾驶学习手册.pdf",
        "classification": "LEGACY_2025_RESOURCE_INDEX",
        "render_key": "learning_manual",
    },
    {
        "path": ROOT / "[智慧城市无人驾驶算法应用赛]场地铺设说明20250922.pdf",
        "classification": "LEGACY_2025_FIELD_REFERENCE",
        "render_key": "field_guide",
    },
    {
        "path": ROOT / "11智慧城市无人驾驶算法应用赛.pdf",
        "classification": "CURRENT_2026_RULES_BYTE_IDENTICAL_COPY",
        "render_key": "current_rules",
    },
)
AUDIT_ADDED_SOURCE_NAMES = {
    "user_copy_current_2026_rules",
    "legacy_2025_organizer_technical_share",
    "legacy_2025_resource_index_manual",
    "legacy_2025_field_reference",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_text_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def page_text_hashes(path: Path) -> list[str]:
    reader = PdfReader(path)
    return [normalized_text_hash(page.extract_text() or "") for page in reader.pages]


def rendered_page_hashes(directory: Path) -> list[dict[str, Any]]:
    def page_number(path: Path) -> int:
        match = re.search(r"(\d+)$", path.stem)
        if not match:
            raise ValueError(f"Rendered page has no numeric suffix: {path}")
        return int(match.group(1))

    pages = sorted(directory.glob("*.png"), key=page_number)
    return [
        {"page": page_number(path), "sha256": sha256(path), "size_bytes": path.stat().st_size}
        for path in pages
    ]


def render_pdf(pdftoppm: str, source: Path, output_directory: Path) -> None:
    output_directory.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [pdftoppm, "-r", "100", "-png", str(source), str(output_directory / "page")],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def load_manifest() -> list[dict[str, str]]:
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def load_source_lock() -> list[dict[str, Any]]:
    with SOURCE_LOCK.open("r", encoding="utf-8") as stream:
        payload = yaml.safe_load(stream) or {}
    return payload.get("sources", [])


def load_shimo_index() -> dict[str, Any]:
    with SHIMO_INDEX.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def safe_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pdftoppm",
        default=os.environ.get("PDFTOPPM") or shutil.which("pdftoppm"),
        help="Path to Poppler pdftoppm (or set PDFTOPPM)",
    )
    args = parser.parse_args()
    if not args.pdftoppm:
        raise RuntimeError("pdftoppm was not found; pass --pdftoppm or set PDFTOPPM")

    for item in DOCUMENTS:
        if not item["path"].is_file():
            raise FileNotFoundError(item["path"])
    if not LOCKED_CURRENT_RULES.is_file():
        raise FileNotFoundError(LOCKED_CURRENT_RULES)

    manifest = load_manifest()
    locked_sources = load_source_lock()
    shimo = load_shimo_index()
    shimo_by_name = {item["name"]: item for item in shimo.get("attachments", [])}

    results: list[dict[str, Any]] = []
    temporary_parent = ROOT / "tmp"
    temporary_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="four-document-audit-", dir=temporary_parent) as temporary_name:
        render_root = Path(temporary_name)
        for item in DOCUMENTS:
            render_pdf(args.pdftoppm, item["path"], render_root / item["render_key"])
        render_pdf(args.pdftoppm, LOCKED_CURRENT_RULES, render_root / "locked_current_rules")

        for item in DOCUMENTS:
            path: Path = item["path"]
            digest = sha256(path)
            size = path.stat().st_size
            text_hashes = page_text_hashes(path)
            render_hashes = rendered_page_hashes(render_root / item["render_key"])

            manifest_hash_matches = [row["relative_path"] for row in manifest if row.get("sha256") == digest]
            manifest_name_size_matches = [
                row["relative_path"]
                for row in manifest
                if row.get("file_name") == path.name and int(row.get("size_bytes") or -1) == size
            ]
            source_lock_hash_matches = [
                source.get("name")
                for source in locked_sources
                if source.get("sha256") == digest and source.get("name") not in AUDIT_ADDED_SOURCE_NAMES
            ]
            shimo_item = shimo_by_name.get(path.name)
            shimo_name_size_match = bool(shimo_item and shimo_item.get("size") == size)

            if path.name == "11智慧城市无人驾驶算法应用赛.pdf":
                locked_text_hashes = page_text_hashes(LOCKED_CURRENT_RULES)
                locked_render_hashes = rendered_page_hashes(render_root / "locked_current_rules")
                byte_identical = digest == sha256(LOCKED_CURRENT_RULES) and path.read_bytes() == LOCKED_CURRENT_RULES.read_bytes()
                page_comparison = []
                for page_number, (root_text, locked_text, root_render, locked_render) in enumerate(
                    zip(text_hashes, locked_text_hashes, render_hashes, locked_render_hashes, strict=True), start=1
                ):
                    page_comparison.append(
                        {
                            "page": page_number,
                            "normalized_text_sha256": root_text,
                            "locked_normalized_text_sha256": locked_text,
                            "text_match": root_text == locked_text,
                            "rendered_png_sha256": root_render["sha256"],
                            "locked_rendered_png_sha256": locked_render["sha256"],
                            "render_match": root_render["sha256"] == locked_render["sha256"],
                        }
                    )
                disposition = "DUPLICATE_OF_LOCKED_CURRENT_2026_RULES"
                current_rule_copy = {
                    "locked_path": safe_relative(LOCKED_CURRENT_RULES),
                    "byte_identical": byte_identical,
                    "page_count_match": len(text_hashes) == len(locked_text_hashes),
                    "all_text_pages_match": all(row["text_match"] for row in page_comparison),
                    "all_rendered_pages_match": all(row["render_match"] for row in page_comparison),
                    "pages": page_comparison,
                }
            else:
                disposition = "NEW_LOCAL_FILE_MATCHING_SHIMO_NAME_AND_SIZE" if shimo_name_size_match else "NEW_LOCAL_FILE_UNMATCHED"
                current_rule_copy = None

            results.append(
                {
                    "path": safe_relative(path),
                    "size_bytes": size,
                    "sha256": digest,
                    "pdf_pages": len(text_hashes),
                    "rendered_pages": len(render_hashes),
                    "classification": item["classification"],
                    "disposition": disposition,
                    "comparison": {
                        "organizer_manifest_sha256_matches": manifest_hash_matches,
                        "organizer_manifest_name_and_size_matches": manifest_name_size_matches,
                        "source_lock_sha256_matches": source_lock_hash_matches,
                        "shimo_attachment_name_and_size_match": shimo_name_size_match,
                        "shimo_attachment_url": shimo_item.get("url") if shimo_item else None,
                    },
                    "current_rule_copy_verification": current_rule_copy,
                }
            )

    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "scope": {
            "mode": "INCREMENTAL_FOUR_DOCUMENTS_ONLY",
            "full_organizer_tree_rescanned": False,
            "inputs_hashed": [safe_relative(item["path"]) for item in DOCUMENTS] + [safe_relative(LOCKED_CURRENT_RULES)],
            "indexes_read_without_rehashing_indexed_files": [
                safe_relative(MANIFEST), safe_relative(SOURCE_LOCK), safe_relative(SHIMO_INDEX)
            ],
            "original_pdfs_modified": False,
        },
        "documents": results,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="\n", prefix=f".{OUTPUT.name}.", suffix=".part",
        dir=OUTPUT.parent, delete=False
    ) as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    os.replace(temporary, OUTPUT)
    print(f"documents={len(results)} output={safe_relative(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
