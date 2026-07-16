#!/usr/bin/env python3
"""Register organizer model bundles without modifying organizer originals."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import onnx
import yaml


ROOT = Path(__file__).resolve().parents[2]
DROP = ROOT / "official" / "organizer_drop"
OUTPUT = ROOT / "models" / "official" / "metadata" / "model_registry.yaml"
STRUCTURE_OUTPUT = ROOT / "docs" / "sources" / "organizer_onnx_structure.json"

T710_ROOT = (
    DROP
    / "examples"
    / "开源工程"
    / "extracted"
    / "icar_autopilot_2025th"
    / "icar_autopilot_2025th"
)
FZ3B_ROOT = (
    DROP
    / "examples"
    / "开源工程"
    / "extracted"
    / "icar_autopilot_2025th_FZ3B"
    / "icar_autopilot_2025th"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def artifact_format(path: Path) -> str:
    mapping = {
        ".json": "JSON_METADATA",
        ".txt": "LABEL_LIST",
        ".onnx": "ONNX",
        ".params": "PPNC_PARAMETER_REFERENCE",
        ".ro": "AARCH64_RELOCATABLE_OBJECT",
        ".so": "AARCH64_ELF_SHARED_OBJECT",
        ".tar": "TAR_MODEL_OR_OBJECT_BUNDLE",
    }
    if path.name == "mobilenet-ssd-model":
        return "PADDLE_MODEL_STRUCTURE"
    if path.name == "mobilenet-ssd-params":
        return "PADDLE_MODEL_PARAMETERS"
    return mapping.get(path.suffix.lower(), "UNKNOWN")


def artifacts(model_dir: Path) -> list[dict[str, Any]]:
    result = []
    for path in sorted(item for item in model_dir.rglob("*") if item.is_file()):
        result.append(
            {
                "original_path": relative(path),
                "sha256": sha256(path),
                "format": artifact_format(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return result


def labels(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def tensor_shape(value_info: Any) -> list[int | str | None]:
    result: list[int | str | None] = []
    for dimension in value_info.type.tensor_type.shape.dim:
        if dimension.HasField("dim_value"):
            result.append(dimension.dim_value)
        elif dimension.HasField("dim_param"):
            result.append(dimension.dim_param)
        else:
            result.append(None)
    return result


def inspect_onnx(path: Path) -> dict[str, Any]:
    model = onnx.load(str(path), load_external_data=False)
    onnx.checker.check_model(model)
    describe = lambda value: {
        "name": value.name,
        "data_type": onnx.TensorProto.DataType.Name(value.type.tensor_type.elem_type),
        "shape": tensor_shape(value),
    }
    return {
        "original_path": relative(path),
        "sha256": sha256(path),
        "checker_status": "PASS",
        "ir_version": model.ir_version,
        "producer_name": model.producer_name or None,
        "producer_version": model.producer_version or None,
        "opsets": [
            {"domain": item.domain or "ai.onnx", "version": item.version}
            for item in model.opset_import
        ],
        "inputs": [describe(value) for value in model.graph.input],
        "outputs": [describe(value) for value in model.graph.output],
        "node_count": len(model.graph.node),
        "initializer_count": len(model.graph.initializer),
    }


def t710_entry(model_id: str, directory_name: str) -> dict[str, Any]:
    model_dir = T710_ROOT / "res" / "models" / directory_name
    io_path = model_dir / "io_paddle.json"
    io_metadata = json.loads(io_path.read_text(encoding="utf-8"))
    input_record = next(item for item in io_metadata if item["type"] == "INPUT")
    outputs = [item for item in io_metadata if item["type"] == "OUTPUT"]
    label_path = model_dir / "label_list.txt"
    return {
        "model_id": model_id,
        "original_path": relative(model_dir),
        "source": "organizer archive icar_autopilot_2025th.zip",
        "source_archive_sha256": "54f0c38151b5844b0108754d3917b2bfcab983e8a8a79f03d0bea8d5eacf69c7",
        "year": 2025,
        "target_board": "T710 organizer legacy baseline",
        "inference_sdk": ["PPNC", "ONNX Runtime"],
        "model_compiler": None,
        "model_compiler_source_required": "Exact compiler build and conversion record for this artifact",
        "input_tensor": input_record["name"],
        "input_size": input_record["shape"],
        "data_type": input_record["dtype"],
        "channel_order": "RGB",
        "normalization": {
            "scale": "1/255",
            "mean": [0.485, 0.456, 0.406],
            "std": [0.229, 0.224, 0.225],
            "evidence": relative(T710_ROOT / "include" / "utils" / "detection.hpp"),
            "scope": "LEGACY_REFERENCE_ONLY",
        },
        "output_tensors": outputs,
        "label_file": relative(label_path),
        "classes": labels(label_path),
        "quantization": None,
        "quantization_source_required": "Original conversion report or SDK metadata",
        "license": "LICENSE_UNVERIFIED",
        "current_usage": "LEGACY_REFERENCE",
        "validation_status": "REFERENCE_ONLY",
        "artifacts": artifacts(model_dir),
    }


def fz3b_entry() -> dict[str, Any]:
    model_dir = FZ3B_ROOT / "res" / "models" / "ssd_mobilenet_v1"
    label_path = model_dir / "label_list.txt"
    evidence = relative(FZ3B_ROOT / "include" / "utils" / "detection.hpp")
    return {
        "model_id": "legacy_2025_fz3b_ssd_mobilenet_v1",
        "original_path": relative(model_dir),
        "source": "organizer archive icar_autopilot_2025th_FZ3B.zip",
        "source_archive_sha256": "c03a6a6b74ba0ba18a8f6ff673ea5548201ea55373d1e2a520427111ea7517a4",
        "year": 2025,
        "target_board": "FZ3B organizer legacy baseline",
        "inference_sdk": ["Paddle Lite"],
        "model_compiler": None,
        "model_compiler_source_required": "Original Paddle conversion/export record",
        "input_tensor": None,
        "input_tensor_source_required": "Paddle model graph introspection on a supported environment",
        "input_size": [1, 3, 300, 300],
        "input_size_evidence": evidence,
        "data_type": None,
        "data_type_source_required": "Paddle model graph metadata",
        "channel_order": "RGB",
        "normalization": {
            "mean": [127.5, 127.5, 127.5],
            "scale": [0.007843, 0.007843, 0.007843],
            "evidence": evidence,
            "scope": "LEGACY_REFERENCE_ONLY",
        },
        "output_tensors": None,
        "output_tensors_source_required": "Paddle model graph introspection on a supported environment",
        "label_file": relative(label_path),
        "classes": labels(label_path),
        "quantization": None,
        "quantization_source_required": "Original conversion report or SDK metadata",
        "license": "LICENSE_UNVERIFIED",
        "current_usage": "LEGACY_REFERENCE",
        "validation_status": "REFERENCE_ONLY",
        "artifacts": artifacts(model_dir),
    }


def main() -> int:
    onnx_files = sorted(T710_ROOT.rglob("*.onnx"))
    onnx_structures = [inspect_onnx(path) for path in onnx_files]
    registry = {
        "registry_version": 1,
        "generated_by": "tools/audit/register_organizer_models.py",
        "policy": {
            "organizer_2025_projects": "LEGACY_REFERENCE_ONLY",
            "final_competition_model": "BLOCKED pending 2026 classes, license, target-board and real validation evidence",
        },
        "models": [
            t710_entry("legacy_2025_t710_yolov3_mobilenet_v1", "yolov3_mobilenet_v1"),
            t710_entry("legacy_2025_t710_yolov3_mobilenet_v1_past", "yolov3_mobilenet_v1_past"),
            fz3b_entry(),
        ],
        "onnx_structure_audit": onnx_structures,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        yaml.safe_dump(registry, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    STRUCTURE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    STRUCTURE_OUTPUT.write_text(
        json.dumps(onnx_structures, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"models={len(registry['models'])}")
    print(f"onnx_files={len(onnx_structures)}")
    print(f"registry={OUTPUT}")
    print(f"onnx_structure={STRUCTURE_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
