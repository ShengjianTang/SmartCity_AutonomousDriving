#!/usr/bin/env python3
"""Record ffprobe evidence for organizer-provided MP4 files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ffprobe", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=Path("official/organizer_drop"))
    parser.add_argument("--csv", type=Path, default=Path("docs/sources/organizer_media_audit.csv"))
    parser.add_argument("--markdown", type=Path, default=Path("docs/sources/organizer_media_audit.md"))
    args = parser.parse_args()

    root = args.root.resolve()
    rows: list[dict[str, str | int]] = []
    for path in sorted(root.rglob("*.mp4"), key=lambda item: item.as_posix().lower()):
        relative = path.relative_to(root).as_posix()
        process = subprocess.run(
            [
                str(args.ffprobe), "-v", "error", "-show_entries",
                "format=format_name,duration,size,bit_rate:stream=codec_name,codec_type,width,height,r_frame_rate,avg_frame_rate,sample_rate,channels",
                "-of", "json", str(path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        row: dict[str, str | int] = {
            "relative_path": relative,
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
            "duration_seconds": "",
            "video_codec": "",
            "width": "",
            "height": "",
            "average_frame_rate": "",
            "audio_codec": "",
            "audio_sample_rate": "",
            "audio_channels": "",
            "status": "PARSED" if process.returncode == 0 else "PARSE_FAILED",
            "error": process.stderr.decode(errors="replace").strip(),
        }
        if process.returncode == 0:
            data = json.loads(process.stdout)
            format_data = data.get("format", {})
            row["duration_seconds"] = format_data.get("duration", "")
            for stream in data.get("streams", []):
                if stream.get("codec_type") == "video" and not row["video_codec"]:
                    row["video_codec"] = stream.get("codec_name", "")
                    row["width"] = stream.get("width", "")
                    row["height"] = stream.get("height", "")
                    row["average_frame_rate"] = stream.get("avg_frame_rate", "")
                if stream.get("codec_type") == "audio" and not row["audio_codec"]:
                    row["audio_codec"] = stream.get("codec_name", "")
                    row["audio_sample_rate"] = stream.get("sample_rate", "")
                    row["audio_channels"] = stream.get("channels", "")
        rows.append(row)

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
    with args.markdown.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# 组委会视频媒体审计\n\n")
        stream.write(f"- MP4 文件：{len(rows)}\n")
        stream.write(f"- ffprobe 可解析：{sum(row['status'] == 'PARSED' for row in rows)}\n")
        stream.write("- 媒体可解析不代表内容适用于 2026 当前赛题；内容和年份另行审计。\n\n")
        stream.write("| 文件 | SHA-256 | 时长秒 | 视频 | 分辨率/帧率 | 音频 | 状态 |\n")
        stream.write("| --- | --- | ---: | --- | --- | --- | --- |\n")
        for row in rows:
            resolution = f"{row['width']}x{row['height']} @ {row['average_frame_rate']}"
            audio = f"{row['audio_codec']} {row['audio_sample_rate']}Hz {row['audio_channels']}ch" if row["audio_codec"] else "none"
            stream.write(f"| `{row['relative_path']}` | `{row['sha256']}` | {row['duration_seconds']} | {row['video_codec']} | {resolution} | {audio} | {row['status']} |\n")
    failures = sum(row["status"] != "PARSED" for row in rows)
    print(f"videos={len(rows)} parsed={len(rows)-failures} failed={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
