#!/usr/bin/env python3
"""Render key organizer PDFs with Poppler and build visual-review contact sheets."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


KEY_PDFS = [
    "examples/开源工程/EdgeBoard赛事专用卡-开源工程说明.pdf",
    "hardware/board_image/赛事专用卡-镜像开源资料/EdgeBoard赛事专用卡-镜像烧写说明.pdf",
    "hardware/control_board/智能汽车竞赛-开源资料及智控板使用教程/智能汽车竞赛-开源资料及智控板使用教程.pdf",
    "hardware/remote_access/赛事专用卡-远程操作资料/EdgeBoard赛事专用卡-远程操作说明.pdf",
    "maps/场地资料/AIC2025-场地喷绘加工（4.7x4.2m）-推荐油画布.pdf",
    "maps/场地资料/标牌加工/AIC2025-场地贴纸加工.pdf",
    "models/training/模型训练及部署/目标检测模型训练及部署教程 (FZ3B+SSD).pdf",
    "models/training/模型训练及部署/目标检测模型训练及部署教程 (T710+Yolov3).pdf",
    "sdk/model_compiler/赛事专用卡-模型编译教程/赛事专用卡-模型编译教程.pdf",
]


def slug(index: int, path: str) -> str:
    name = Path(path).stem
    name = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._-]+", "_", name).strip("_")
    return f"{index:02d}_{name}"


def make_contact_sheet(images: list[Path], output: Path) -> None:
    columns = 4
    thumb_width = 320
    label_height = 26
    gap = 10
    thumbnails: list[Image.Image] = []
    heights: list[int] = []
    for image_path in images:
        with Image.open(image_path) as source:
            converted = source.convert("RGB")
            height = max(1, round(converted.height * thumb_width / converted.width))
            thumbnails.append(converted.resize((thumb_width, height), Image.Resampling.LANCZOS))
            heights.append(height + label_height)
    rows = (len(thumbnails) + columns - 1) // columns
    row_heights = [max(heights[row * columns : (row + 1) * columns]) for row in range(rows)]
    width = columns * thumb_width + (columns + 1) * gap
    total_height = sum(row_heights) + (rows + 1) * gap
    sheet = Image.new("RGB", (width, total_height), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    y = gap
    for row in range(rows):
        x = gap
        for column in range(columns):
            index = row * columns + column
            if index >= len(thumbnails):
                break
            image = thumbnails[index]
            sheet.paste(image, (x, y + label_height))
            draw.text((x, y + 5), f"page {index + 1}", fill="black", font=font)
            x += thumb_width + gap
        y += row_heights[row] + gap
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, format="PNG", optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdftoppm", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=Path("official/organizer_drop"))
    parser.add_argument("--output", type=Path, default=Path("tmp/pdfs/organizer"))
    args = parser.parse_args()

    root = args.root.resolve()
    output_root = args.output.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    for index, relative in enumerate(KEY_PDFS, start=1):
        input_path = root / Path(relative)
        document_slug = slug(index, relative)
        document_dir = output_root / document_slug
        document_dir.mkdir(parents=True, exist_ok=True)
        prefix = document_dir / "page"
        command = [str(args.pdftoppm), "-png", "-scale-to", "1800", str(input_path), str(prefix)]
        if args.pdftoppm.suffix.lower() in {".cmd", ".bat"}:
            command = ["cmd.exe", "/d", "/c", *command]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if process.returncode != 0:
            raise RuntimeError(f"Poppler failed for {relative}: {process.stderr.decode(errors='replace')}")
        pages = sorted(document_dir.glob("page-*.png"))
        if not pages:
            raise RuntimeError(f"Poppler produced no pages for {relative}")
        contact = output_root / f"{document_slug}_contact.png"
        make_contact_sheet(pages, contact)
        print(f"rendered {relative}: pages={len(pages)} contact={contact}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
