#!/usr/bin/env python3
"""Build a PowerPoint deck from naturally sorted slide images."""
from __future__ import annotations

import argparse
import json
import re
import tempfile
from contextlib import nullcontext
from pathlib import Path

from PIL import Image, ImageOps
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches

DEFAULT_EXTENSIONS = (".png", ".jpg", ".jpeg")
def natural_key(path: Path) -> list[object]:
    parts = re.split(r"(\d+)", path.name.lower())
    return [int(part) if part.isdigit() else part for part in parts]
def collect_images(input_dir: Path, extensions: tuple[str, ...]) -> list[Path]:
    normalized = {ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions}
    return sorted(
        (path for path in input_dir.iterdir() if path.is_file() and path.suffix.lower() in normalized),
        key=natural_key,
    )
def add_background(slide, color: str) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(color)
def image_size(image_path: Path) -> tuple[int, int]:
    with Image.open(image_path) as image:
        image = ImageOps.exif_transpose(image)
        return image.size
def prepare_image(
    image_path: Path,
    index: int,
    work_dir: Path,
    max_width: int,
    jpeg_quality: int,
    background: str,
) -> Path:
    """Return an embeddable image, optionally downscaled and re-encoded."""
    with Image.open(image_path) as image:
        image = ImageOps.exif_transpose(image)
        if max_width > 0 and image.width > max_width:
            new_height = round(image.height * max_width / image.width)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        if jpeg_quality > 0:
            suffix = ".jpg"
            if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
                rgba = image.convert("RGBA")
                canvas = Image.new("RGB", rgba.size, f"#{background}")
                canvas.paste(rgba, mask=rgba.getchannel("A"))
                image = canvas
            elif image.mode != "RGB":
                image = image.convert("RGB")
            target = work_dir / f"{index:04d}-{image_path.stem}{suffix}"
            image.save(target, "JPEG", quality=jpeg_quality, optimize=True)
        else:
            suffix = image_path.suffix.lower()
            target = work_dir / f"{index:04d}-{image_path.stem}{suffix}"
            if suffix in (".jpg", ".jpeg"):
                image.save(target, "JPEG", quality=95)
            else:
                image.save(target)
    return target
def add_fitted_picture(
    slide,
    image_path: Path,
    slide_width: int,
    slide_height: int,
    fit: str,
    name: str = "",
) -> None:
    if fit == "stretch":
        picture = slide.shapes.add_picture(str(image_path), 0, 0, width=slide_width, height=slide_height)
    else:
        image_width, image_height = image_size(image_path)
        if image_width <= 0 or image_height <= 0:
            raise ValueError(f"Invalid image dimensions: {image_path}")
        image_ratio = image_width / image_height
        slide_ratio = slide_width / slide_height
        if fit == "contain":
            if image_ratio >= slide_ratio:
                width = slide_width
                height = int(slide_width / image_ratio)
                left = 0
                top = int((slide_height - height) / 2)
            else:
                height = slide_height
                width = int(slide_height * image_ratio)
                top = 0
                left = int((slide_width - width) / 2)
            picture = slide.shapes.add_picture(str(image_path), left, top, width=width, height=height)
        else:
            # Cover: place the picture at full slide size and center-crop the
            # overflow via crop attributes, so no pixels extend past the canvas.
            picture = slide.shapes.add_picture(
                str(image_path), 0, 0, width=slide_width, height=slide_height
            )
            if image_ratio > slide_ratio:
                crop = (1 - slide_ratio / image_ratio) / 2
                picture.crop_left = crop
                picture.crop_right = crop
            elif image_ratio < slide_ratio:
                crop = (1 - image_ratio / slide_ratio) / 2
                picture.crop_top = crop
                picture.crop_bottom = crop
    if name:
        picture.name = name
def build_deck(args: argparse.Namespace) -> dict[str, object]:
    input_dir = args.input_dir.resolve()
    output = args.output.resolve()
    if not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    images = collect_images(input_dir, tuple(args.extensions))
    if not images:
        raise FileNotFoundError(f"No supported images found in: {input_dir}")
    presentation = Presentation()
    presentation.slide_width = Inches(args.width)
    presentation.slide_height = Inches(args.height)
    presentation.core_properties.title = args.title or output.stem
    slide_width = presentation.slide_width
    slide_height = presentation.slide_height
    blank_layout = presentation.slide_layouts[6]
    process = args.max_width > 0 or args.jpeg_quality > 0
    with (tempfile.TemporaryDirectory() if process else nullcontext(None)) as tmp:
        for index, image_path in enumerate(images):
            embed_path = (
                prepare_image(
                    image_path, index, Path(tmp), args.max_width, args.jpeg_quality, args.background
                )
                if process
                else image_path
            )
            slide = presentation.slides.add_slide(blank_layout)
            add_background(slide, args.background)
            add_fitted_picture(
                slide, embed_path, slide_width, slide_height, args.fit, name=image_path.stem
            )
        output.parent.mkdir(parents=True, exist_ok=True)
        presentation.save(output)
    verification = Presentation(output)
    if len(verification.slides) != len(images):
        raise RuntimeError("Saved deck slide count does not match source image count")
    return {
        "output": str(output),
        "slides": len(images),
        "slide_size_inches": [args.width, args.height],
        "fit": args.fit,
        "max_width": args.max_width,
        "jpeg_quality": args.jpeg_quality,
        "images": [path.name for path in images],
    }
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path, help="Directory containing ordered slide images")
    parser.add_argument("output", type=Path, help="Output .pptx path")
    parser.add_argument("--fit", choices=("cover", "contain", "stretch"), default="cover")
    parser.add_argument("--width", type=float, default=13.333333, help="Slide width in inches")
    parser.add_argument("--height", type=float, default=7.5, help="Slide height in inches")
    parser.add_argument("--background", default="FFFFFF", help="Six-digit RGB background color")
    parser.add_argument("--title", default="", help="PowerPoint document title")
    parser.add_argument("--extensions", nargs="+", default=list(DEFAULT_EXTENSIONS))
    parser.add_argument(
        "--max-width",
        type=int,
        default=0,
        help="Downscale images wider than this many pixels before embedding (0 keeps original size)",
    )
    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=0,
        help="Re-encode images as JPEG at this quality (1-95) before embedding (0 keeps original format)",
    )
    args = parser.parse_args()
    if args.output.suffix.lower() != ".pptx":
        parser.error("output must use the .pptx extension")
    if args.width <= 0 or args.height <= 0:
        parser.error("slide width and height must be positive")
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", args.background):
        parser.error("background must be a six-digit RGB value such as FFFFFF")
    args.background = args.background.upper()
    if args.max_width < 0:
        parser.error("max-width must be a non-negative pixel count")
    if args.jpeg_quality != 0 and not 1 <= args.jpeg_quality <= 95:
        parser.error("jpeg-quality must be between 1 and 95 (0 disables re-encoding)")
    return args
def main() -> None:
    result = build_deck(parse_args())
    print(json.dumps(result, ensure_ascii=True, indent=2))
if __name__ == "__main__":
    main()
