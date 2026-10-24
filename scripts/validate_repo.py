#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
WIDTH = 1536
HEIGHT = 2288
CELL_WIDTH = 192
CELL_HEIGHT = 208
COLUMNS = 8
FRAMES_PER_ROW = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
SLUGS = ["aqua", "megumin", "kazuma", "darkness"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        add_error(errors, f"{path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        add_error(errors, f"{path.relative_to(ROOT)}: expected a JSON object")
        return {}
    return value


def validate_atlas(path: Path, label: str, errors: list[str]) -> Image.Image | None:
    try:
        with Image.open(path) as opened:
            image = opened.convert("RGBA")
    except OSError as exc:
        add_error(errors, f"{label}: cannot open image: {exc}")
        return None

    if image.size != (WIDTH, HEIGHT):
        add_error(errors, f"{label}: expected {WIDTH}x{HEIGHT}, got {image.width}x{image.height}")
        return image

    alpha = image.getchannel("A")
    for row, required in enumerate(FRAMES_PER_ROW):
        for column in range(COLUMNS):
            bounds = (
                column * CELL_WIDTH,
                row * CELL_HEIGHT,
                (column + 1) * CELL_WIDTH,
                (row + 1) * CELL_HEIGHT,
            )
            cell_alpha = alpha.crop(bounds)
            visible = sum(cell_alpha.histogram()[17:])
            if column < required:
                if visible < 64:
                    add_error(errors, f"{label}: missing artwork at row {row}, column {column}")
            elif cell_alpha.getbbox() is not None:
                add_error(errors, f"{label}: unused cell is not transparent at row {row}, column {column}")
            if visible == CELL_WIDTH * CELL_HEIGHT:
                add_error(errors, f"{label}: cell is fully opaque at row {row}, column {column}")
    return image


def main() -> None:
    errors: list[str] = []
    manifest_path = ROOT / "manifest.json"
    manifest = load_json(manifest_path, errors)
    entries = manifest.get("pets", [])
    if not isinstance(entries, list):
        add_error(errors, "manifest.json: pets must be an array")
        entries = []
    by_slug = {
        str(entry.get("slug")): entry
        for entry in entries
        if isinstance(entry, dict) and entry.get("slug")
    }
    if sorted(by_slug) != sorted(SLUGS):
        add_error(errors, f"manifest.json: expected slugs {SLUGS}, got {sorted(by_slug)}")

    format_spec = manifest.get("spriteFormat", {})
    expected_format = {
        "version": 2,
        "width": WIDTH,
        "height": HEIGHT,
        "cellWidth": CELL_WIDTH,
        "cellHeight": CELL_HEIGHT,
        "columns": COLUMNS,
        "rows": 11,
        "framesPerRow": FRAMES_PER_ROW,
    }
    if format_spec != expected_format:
        add_error(errors, "manifest.json: spriteFormat does not match the v2 contract")

    for slug in SLUGS:
        entry = by_slug.get(slug, {})
        pet_dir = ROOT / "pets" / slug
        pet_json = load_json(pet_dir / "pet.json", errors)
        if pet_json.get("spritesheetPath") != "spritesheet.webp":
            add_error(errors, f"pets/{slug}/pet.json: spritesheetPath must be spritesheet.webp")
        if pet_json.get("spriteVersion") != 2:
            add_error(errors, f"pets/{slug}/pet.json: spriteVersion must be 2")
        if not pet_json.get("displayName") or not pet_json.get("description"):
            add_error(errors, f"pets/{slug}/pet.json: displayName and description are required")

        png_path = ROOT / "assets/spritesheets" / f"{slug}.png"
        webp_path = pet_dir / "spritesheet.webp"
        png = validate_atlas(png_path, png_path.relative_to(ROOT).as_posix(), errors)
        webp = validate_atlas(webp_path, webp_path.relative_to(ROOT).as_posix(), errors)
        if png is not None and webp is not None and png.tobytes() != webp.tobytes():
            add_error(errors, f"pets/{slug}: PNG master and WebP package pixels differ")

        expected_hashes = entry.get("sha256", {})
        if png_path.is_file() and expected_hashes.get("pngMaster") != sha256(png_path):
            add_error(errors, f"{png_path.relative_to(ROOT)}: manifest hash mismatch")
        if webp_path.is_file() and expected_hashes.get("spritesheetWebp") != sha256(webp_path):
            add_error(errors, f"{webp_path.relative_to(ROOT)}: manifest hash mismatch")

        for field in ("idlePreview", "allStatesPreview", "lookPreview"):
            relative = entry.get(field)
            if not isinstance(relative, str) or not (ROOT / relative).is_file():
                add_error(errors, f"pets/{slug}: missing manifest artifact for {field}")

    sums_path = ROOT / "SHA256SUMS"
    listed: set[str] = set()
    try:
        lines = sums_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        add_error(errors, f"SHA256SUMS: {exc}")
        lines = []
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2:
            add_error(errors, f"SHA256SUMS:{line_number}: malformed line")
            continue
        expected, relative = parts
        listed.add(relative)
        path = ROOT / relative
        if not path.is_file():
            add_error(errors, f"SHA256SUMS:{line_number}: missing {relative}")
        elif sha256(path) != expected:
            add_error(errors, f"SHA256SUMS:{line_number}: hash mismatch for {relative}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name == "SHA256SUMS":
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith(".git/"):
            continue
        if relative not in listed:
            add_error(errors, f"SHA256SUMS: missing entry for {relative}")

    result = {
        "ok": not errors,
        "collection": manifest.get("collection"),
        "pets": SLUGS,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
