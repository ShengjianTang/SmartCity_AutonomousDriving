#!/usr/bin/env python3
"""Download and verify the two public competition sources atomically."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
ERROR_LOG = ROOT / "logs" / "setup" / "download_public_sources_error.log"
LAST_REPORT = ROOT / "logs" / "setup" / "download_public_sources_last.json"

SOURCES: tuple[dict[str, Any], ...] = (
    {
        "name": "aicomp_track_4548",
        "url": "https://www.aicomp.cn/tracks/4548.html",
        "path": ROOT / "official" / "public" / "webpages" / "track_4548.html",
        "sha256": "8ebbfc4e95cf0cf22e0752499239d8302e11d1a73085b8e9cbb7d18c9bdc8f7f",
        "kind": "html",
    },
    {
        "name": "smart_city_driverless_official_rules",
        "url": (
            "https://www.aicomp.cn/wp-content/uploads/2026/06/"
            "11%E6%99%BA%E6%85%A7%E5%9F%8E%E5%B8%82%E6%97%A0%E4%BA%BA%E9%A9%BE%E9%A9%B6"
            "%E7%AE%97%E6%B3%95%E5%BA%94%E7%94%A8%E8%B5%9B.pdf"
        ),
        "path": ROOT / "official" / "public" / "rules" / "智慧城市无人驾驶算法应用赛_官方规则.pdf",
        "sha256": "41cd80412a740049f15bf02bc9f9ea28b9b89f96af1d8a4335fb750f98c03988",
        "kind": "pdf",
    },
)


class ValidationError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate(path: Path, source: dict[str, Any], content_type: str | None = None) -> None:
    size = path.stat().st_size
    if size <= 0:
        raise ValidationError("file is empty")
    actual_hash = sha256(path)
    if actual_hash != source["sha256"]:
        raise ValidationError(f"SHA-256 mismatch: expected {source['sha256']}, got {actual_hash}")
    with path.open("rb") as stream:
        prefix = stream.read(4096)
    if source["kind"] == "pdf":
        if content_type and "application/pdf" not in content_type.lower():
            raise ValidationError(f"unexpected Content-Type: {content_type}")
        if not prefix.startswith(b"%PDF-"):
            raise ValidationError("missing %PDF- file header")
        if size < 1024:
            raise ValidationError(f"unreasonable PDF size: {size}")
    elif source["kind"] == "html":
        lowered = prefix.lower()
        if content_type and "html" not in content_type.lower():
            raise ValidationError(f"unexpected Content-Type: {content_type}")
        if b"<html" not in lowered and b"<!doctype" not in lowered:
            raise ValidationError("file does not contain an HTML document header")


def download(source: dict[str, Any]) -> dict[str, Any]:
    destination: Path = source["path"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        validate(destination, source)
        return {
            "name": source["name"],
            "action": "kept_verified_existing_file",
            "path": destination.relative_to(ROOT).as_posix(),
            "sha256": sha256(destination),
            "size_bytes": destination.stat().st_size,
        }

    request = Request(source["url"], headers={"User-Agent": "SmartCityDriverlessSourceAudit/1.0"})
    temporary_path: Path | None = None
    try:
        with urlopen(request, timeout=120) as response:
            status = response.getcode()
            if status != 200:
                raise ValidationError(f"unexpected HTTP status: {status}")
            content_type = response.headers.get("Content-Type")
            with tempfile.NamedTemporaryFile(
                mode="wb", prefix=f".{destination.name}.", suffix=".part", dir=destination.parent, delete=False
            ) as temporary:
                temporary_path = Path(temporary.name)
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    temporary.write(chunk)
                temporary.flush()
                os.fsync(temporary.fileno())
            validate(temporary_path, source, content_type)
            os.replace(temporary_path, destination)
            temporary_path = None
            return {
                "name": source["name"],
                "action": "downloaded",
                "http_status": status,
                "final_url": response.geturl(),
                "content_type": content_type,
                "path": destination.relative_to(ROOT).as_posix(),
                "sha256": sha256(destination),
                "size_bytes": destination.stat().st_size,
            }
    except Exception:
        if temporary_path and temporary_path.exists():
            failed = destination.with_name(
                f"{destination.name}.failed-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.part"
            )
            os.replace(temporary_path, failed)
        raise


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", prefix=f".{path.name}.", suffix=".part", dir=path.parent, delete=False
    ) as temporary:
        json.dump(value, temporary, ensure_ascii=False, indent=2)
        temporary.write("\n")
        temporary.flush()
        os.fsync(temporary.fileno())
        temporary_path = Path(temporary.name)
    os.replace(temporary_path, path)


def main() -> int:
    report: dict[str, Any] = {"run_at": utc_now(), "results": []}
    try:
        for source in SOURCES:
            result = download(source)
            report["results"].append(result)
            print(f"{result['name']}: {result['action']} ({result['sha256']})")
        report["status"] = "success"
        write_json_atomic(LAST_REPORT, report)
        return 0
    except (HTTPError, URLError, OSError, ValidationError) as exc:
        report["status"] = "failure"
        report["error_type"] = type(exc).__name__
        report["error"] = str(exc)
        write_json_atomic(LAST_REPORT, report)
        ERROR_LOG.parent.mkdir(parents=True, exist_ok=True)
        with ERROR_LOG.open("a", encoding="utf-8") as stream:
            stream.write(f"{utc_now()} {type(exc).__name__}: {exc}\n")
        print(f"download failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
