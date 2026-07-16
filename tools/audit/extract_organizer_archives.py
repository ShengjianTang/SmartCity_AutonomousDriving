#!/usr/bin/env python3
"""Validate and safely extract organizer archives without touching originals."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import uuid
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath


ARCHIVE_SUFFIXES = (".zip", ".rar", ".7z", ".tar", ".tgz", ".tar.gz", ".tar.xz", ".tar.bz2")


@dataclass
class Result:
    archive: str
    sha256: str
    validation: str
    extraction: str
    destination: str
    member_count: int
    extracted_file_count: int
    extracted_bytes: int
    detail: str


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_archive(path: Path) -> bool:
    lowered = path.name.lower()
    return any(lowered.endswith(suffix) for suffix in ARCHIVE_SUFFIXES)


def archive_stem(path: Path) -> str:
    lowered = path.name.lower()
    for suffix in sorted(ARCHIVE_SUFFIXES, key=len, reverse=True):
        if lowered.endswith(suffix):
            return path.name[: -len(suffix)]
    return path.stem


def validate_member_name(name: str) -> None:
    normalized = name.replace("\\", "/")
    pure = PurePosixPath(normalized)
    if not normalized or normalized.startswith("/") or pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"unsafe archive member path: {name!r}")
    if len(normalized) >= 2 and normalized[1] == ":":
        raise ValueError(f"drive-qualified archive member path: {name!r}")


def validate_zip(path: Path) -> tuple[int, str]:
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        for info in infos:
            validate_member_name(info.filename)
            if info.flag_bits & 0x1:
                raise ValueError(f"encrypted ZIP member is unsupported: {info.filename}")
            unix_mode = (info.external_attr >> 16) & 0o170000
            if unix_mode == 0o120000:
                raise ValueError(f"ZIP symlink is not extracted: {info.filename}")
        corrupt = archive.testzip()
        if corrupt:
            raise ValueError(f"ZIP CRC failure: {corrupt}")
        return len(infos), "ZIP central directory and CRC validation passed"


def extract_zip(path: Path, destination: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        archive.extractall(destination)


def validate_tar(path: Path) -> tuple[int, str]:
    with tarfile.open(path, mode="r:*") as archive:
        members = archive.getmembers()
        for member in members:
            validate_member_name(member.name)
            if member.isdev() or member.isfifo():
                raise ValueError(f"special TAR member is unsupported: {member.name}")
            if member.issym() or member.islnk():
                validate_member_name(str(PurePosixPath(member.name).parent / member.linkname))
        return len(members), "TAR headers and member paths validated"


def extract_tar(path: Path, destination: Path) -> None:
    with tarfile.open(path, mode="r:*") as archive:
        archive.extractall(destination, filter="data")


def validate_bsdtar(path: Path, tar_executable: str) -> tuple[int, str]:
    process = subprocess.run(
        [tar_executable, "-tf", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        detail = process.stderr.decode(errors="replace").strip()
        raise ValueError(f"bsdtar listing failed with {process.returncode}: {detail}")
    names = process.stdout.decode(errors="replace").splitlines()
    for name in names:
        validate_member_name(name)
    return len(names), "bsdtar listing and member path validation passed"


def extract_bsdtar(path: Path, destination: Path, tar_executable: str) -> None:
    process = subprocess.run(
        [tar_executable, "-xf", str(path), "-C", str(destination), "--no-same-owner", "--no-same-permissions"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        detail = process.stderr.decode(errors="replace").strip()
        raise ValueError(f"bsdtar extraction failed with {process.returncode}: {detail}")


def tree_stats(root: Path) -> tuple[int, int]:
    files = [path for path in root.rglob("*") if path.is_file()]
    return len(files), sum(path.stat().st_size for path in files)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("official/organizer_drop"))
    parser.add_argument("--report", type=Path, default=Path("docs/sources/archive_extraction_report.md"))
    parser.add_argument("--json-report", type=Path, default=Path("docs/sources/archive_extraction_report.json"))
    args = parser.parse_args()

    root = args.root.resolve()
    tar_executable = shutil.which("tar")
    if not tar_executable:
        raise SystemExit("bsdtar/tar executable is required for RAR and 7z validation")

    archives = sorted(
        (path for path in root.rglob("*") if path.is_file() and is_archive(path) and "extracted" not in {part.lower() for part in path.relative_to(root).parts}),
        key=lambda item: item.as_posix().lower(),
    )
    results: list[Result] = []
    for index, archive in enumerate(archives, start=1):
        relative = archive.relative_to(root).as_posix()
        print(f"[{index}/{len(archives)}] hashing {relative}", flush=True)
        digest = sha256(archive)
        destination = archive.parent / "extracted" / archive_stem(archive)
        extracted_root = (archive.parent / "extracted").resolve()
        if extracted_root not in destination.resolve().parents:
            raise RuntimeError(f"destination escaped extracted root: {destination}")

        if destination.exists():
            marker = destination / ".extraction_complete.json"
            if marker.is_file():
                data = json.loads(marker.read_text(encoding="utf-8"))
                if data.get("archive_sha256") == digest:
                    file_count, byte_count = tree_stats(destination)
                    results.append(Result(relative, digest, "VALID", "SKIPPED_EXISTING", destination.relative_to(root).as_posix(), int(data.get("member_count", 0)), file_count, byte_count, "matching completion marker; no files overwritten"))
                    print(f"[{index}/{len(archives)}] skipped completed {relative}", flush=True)
                    continue
            results.append(Result(relative, digest, "UNKNOWN", "BLOCKED_EXISTING_DESTINATION", destination.relative_to(root).as_posix(), 0, 0, 0, "destination exists without a matching completion marker; no files overwritten"))
            print(f"[{index}/{len(archives)}] blocked existing destination {relative}", flush=True)
            continue

        staging_parent = archive.parent / "extracted"
        staging_parent.mkdir(parents=True, exist_ok=True)
        staging = staging_parent / f".{archive_stem(archive)}.partial-{uuid.uuid4().hex}"
        staging.mkdir()
        validation = ""
        member_count = 0
        try:
            lowered = archive.name.lower()
            if lowered.endswith(".zip"):
                member_count, validation = validate_zip(archive)
                extract_zip(archive, staging)
            elif lowered.endswith((".tar", ".tgz", ".tar.gz", ".tar.xz", ".tar.bz2")):
                member_count, validation = validate_tar(archive)
                extract_tar(archive, staging)
            else:
                member_count, validation = validate_bsdtar(archive, tar_executable)
                extract_bsdtar(archive, staging, tar_executable)
            file_count, byte_count = tree_stats(staging)
            marker = {
                "archive": relative,
                "archive_sha256": digest,
                "validated_at": datetime.now().astimezone().isoformat(),
                "validation": validation,
                "member_count": member_count,
                "extracted_file_count": file_count,
                "extracted_bytes": byte_count,
            }
            (staging / ".extraction_complete.json").write_text(json.dumps(marker, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            staging.rename(destination)
            results.append(Result(relative, digest, "VALID", "EXTRACTED", destination.relative_to(root).as_posix(), member_count, file_count, byte_count, validation))
            print(f"[{index}/{len(archives)}] extracted {relative}: files={file_count} bytes={byte_count}", flush=True)
        except Exception as error:  # preserve the staging tree for forensic diagnosis
            results.append(Result(relative, digest, "INVALID_OR_UNSUPPORTED", "FAILED_PARTIAL_RETAINED", staging.relative_to(root).as_posix(), member_count, 0, 0, f"{type(error).__name__}: {error}"))
            print(f"[{index}/{len(archives)}] failed {relative}: {type(error).__name__}: {error}", flush=True)

    args.json_report.parent.mkdir(parents=True, exist_ok=True)
    args.json_report.write_text(json.dumps([asdict(result) for result in results], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with args.report.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# 组委会压缩包验证与解压记录\n\n")
        stream.write(f"- 扫描到的原始压缩包：{len(results)}\n")
        stream.write("- 原始压缩包保持不变；目标目录为压缩包相邻的 `extracted/<archive-name>/`。\n")
        stream.write("- 解压使用新建暂存目录并在成功后原子改名，不覆盖已有文件。\n")
        stream.write("- ZIP 使用 CRC 检查；TAR/TGZ 检查头和成员路径；RAR/7z 使用系统 bsdtar 3.8.4 列表验证。\n\n")
        stream.write("| 压缩包 | SHA-256 | 验证 | 解压 | 成员 | 文件 | 解压字节 | 目标/说明 |\n")
        stream.write("| --- | --- | --- | --- | ---: | ---: | ---: | --- |\n")
        for result in results:
            detail = result.detail.replace("|", "\\|").replace("\n", " ")
            stream.write(f"| `{result.archive}` | `{result.sha256}` | {result.validation} | {result.extraction} | {result.member_count} | {result.extracted_file_count} | {result.extracted_bytes} | `{result.destination}`; {detail} |\n")
    failures = sum(result.extraction.startswith("FAILED") or result.extraction.startswith("BLOCKED") for result in results)
    print(f"archives={len(results)} failures={failures} report={args.report}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
