#!/usr/bin/env python3
"""Validate the evidence-driven integration checkpoint without changing files."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    yaml_paths = [
        *sorted((ROOT / "config").rglob("*.yaml")),
        ROOT / "docs/sources/fact_registry.yaml",
        ROOT / "docs/sources/SOURCES.lock.yaml",
        ROOT / "docs/sources/THIRD_PARTY.lock.yaml",
        ROOT / "models/official/metadata/model_registry.yaml",
    ]
    for path in yaml_paths:
        require(path.is_file(), f"missing YAML: {path.relative_to(ROOT)}")
        with path.open("r", encoding="utf-8") as stream:
            yaml.safe_load(stream)

    with (ROOT / "docs/requirements/requirement_traceability_matrix.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as stream:
        requirements = list(csv.DictReader(stream))
    require(len(requirements) == 35, f"expected 35 requirements, got {len(requirements)}")
    requirement_counts = Counter(row["Current status"] for row in requirements)
    require(
        requirement_counts
        == Counter({"BLOCKED": 23, "VERIFIED": 4, "NOT_STARTED": 4, "IMPLEMENTED_UNVERIFIED": 4}),
        f"unexpected requirement statuses: {requirement_counts}",
    )

    blocker_text = (ROOT / "docs/requirements/blockers.md").read_text(encoding="utf-8")
    blocker_rows = re.findall(
        r"^\| (B-\d{3}) \|.*?\| (RESOLVED|PARTIALLY_RESOLVED|STILL_BLOCKED|REQUIRES_USER_FILE|"
        r"REQUIRES_TARGET_HARDWARE|REQUIRES_REAL_MEASUREMENT|LICENSE_UNVERIFIED|LEGACY_REFERENCE_ONLY) \|$",
        blocker_text,
        flags=re.MULTILINE,
    )
    require([item[0] for item in blocker_rows] == [f"B-{index:03d}" for index in range(1, 59)],
            "blocker IDs are not exactly B-001 through B-058")
    blocker_counts = Counter(item[1] for item in blocker_rows)
    expected_blockers = Counter({
        "PARTIALLY_RESOLVED": 12,
        "STILL_BLOCKED": 5,
        "REQUIRES_USER_FILE": 8,
        "REQUIRES_TARGET_HARDWARE": 6,
        "REQUIRES_REAL_MEASUREMENT": 18,
        "LICENSE_UNVERIFIED": 1,
        "LEGACY_REFERENCE_ONLY": 8,
    })
    require(blocker_counts == expected_blockers, f"unexpected blocker statuses: {blocker_counts}")

    with (ROOT / "docs/sources/organizer_material_manifest.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as stream:
        manifest = list(csv.DictReader(stream))
    require(len(manifest) == 1146, f"expected 1146 manifest files, got {len(manifest)}")
    require(sum(int(row["size_bytes"]) for row in manifest) == 114_392_868_846,
            "manifest total byte count differs from the post-cleanup audit")
    require(not any("__MACOSX" in row["relative_path"] or row["file_name"] == ".DS_Store" for row in manifest),
            "post-cleanup manifest still contains Apple metadata")

    with (ROOT / "docs/sources/organizer_pdf_audit.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as stream:
        pdf_audit = list(csv.DictReader(stream))
    require(len(pdf_audit) == 16 and all(row["status"] == "PARSED" for row in pdf_audit),
            "post-cleanup PDF audit must contain 16 parsed PDFs and no stale AppleDouble row")

    shimo = json.loads((ROOT / "docs/sources/shimo_attachment_index.json").read_text(encoding="utf-8"))
    attachments = shimo["attachments"] if isinstance(shimo, dict) else shimo
    require(len(attachments) == 12, f"expected 12 Shimo attachments, got {len(attachments)}")

    registry = yaml.safe_load((ROOT / "models/official/metadata/model_registry.yaml").read_text(encoding="utf-8"))
    models = registry["models"]
    require(len(models) == 3, f"expected 3 registered models, got {len(models)}")
    require(sum(len(model["artifacts"]) for model in models) == 21, "expected 21 registered model artifacts")
    require(all(model["validation_status"] == "REFERENCE_ONLY" for model in models),
            "organizer models must remain REFERENCE_ONLY")

    onnx_audit = json.loads((ROOT / "docs/sources/organizer_onnx_structure.json").read_text(encoding="utf-8"))
    require(len(onnx_audit) == 2 and all(item["checker_status"] == "PASS" for item in onnx_audit),
            "ONNX structure audit is incomplete")

    required = [
        "build/host_app/smart_city_host_app.exe",
        "config/host/offline_replay.yaml",
        "docs/verification/offline_replay_verification.md",
        "docs/reports/organizer_project_actual_build_result.md",
        "docs/interfaces/serial_protocol_evidence.md",
        "USER_INPUT_REQUIRED.md",
    ]
    for relative in required:
        require((ROOT / relative).is_file(), f"missing required artifact: {relative}")

    first_party_code = "\n".join(
        path.read_text(encoding="utf-8")
        for base in (ROOT / "include", ROOT / "src")
        for path in base.rglob("*")
        if path.is_file()
    )
    require("class OfficialSerialTransport" not in first_party_code,
            "conflicted legacy serial protocol must not be implemented")

    print(f"yaml={len(yaml_paths)} requirements={len(requirements)} blockers={len(blocker_rows)}")
    print(f"manifest={len(manifest)} pdfs={len(pdf_audit)} shimo_attachments={len(attachments)} "
          f"models={len(models)} artifacts=21")
    print("integration_state=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
