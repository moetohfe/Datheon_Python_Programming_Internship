"""
Automated File Organizer & Cleanup Utility
Task 3 - Datheon Python Programming Internship

Sorts the files in a folder (for example Downloads) into category
subfolders based on file extension. Handles name collisions and
permission errors, logs every move, and prints a summary at the end.

Usage:
    python organizer.py <folder>            # organize the folder
    python organizer.py <folder> --dry-run  # preview without moving anything
"""

import argparse
import logging
import os
import shutil
from collections import Counter
from pathlib import Path

# Extension -> category folder
EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".xlsx": "Documents", ".csv": "Documents",
    ".pptx": "Documents", ".md": "Documents",
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
    ".gif": "Images", ".bmp": "Images", ".svg": "Images", ".webp": "Images",
    # Videos
    ".mp4": "Videos", ".mov": "Videos", ".avi": "Videos", ".mkv": "Videos",
    # Audio
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio",
    # Archives
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives",
    ".tar": "Archives", ".gz": "Archives",
    # Code
    ".py": "Code", ".js": "Code", ".html": "Code", ".css": "Code",
    ".java": "Code", ".cpp": "Code", ".c": "Code", ".json": "Code",
}
OTHER = "Others"


def unique_destination(dest: Path) -> Path:
    """If dest already exists, add ' (1)', ' (2)', ... until the name is free."""
    if not dest.exists():
        return dest
    counter = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({counter}){dest.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize(folder: Path, dry_run: bool = False) -> Counter:
    """Move each file in `folder` into its category subfolder."""
    stats = Counter()

    with os.scandir(folder) as entries:
        for entry in entries:
            # Skip folders (including our own category folders) and hidden files
            if not entry.is_file() or entry.name.startswith("."):
                continue

            src = Path(entry.path)
            category = EXTENSION_MAP.get(src.suffix.lower(), OTHER)
            target_dir = folder / category
            dest = unique_destination(target_dir / src.name)

            if dry_run:
                logging.info("[DRY RUN] %s -> %s/%s", src.name, category, dest.name)
                stats[category] += 1
                continue

            try:
                target_dir.mkdir(exist_ok=True)
                shutil.move(str(src), str(dest))
                logging.info("Moved %s -> %s/%s", src.name, category, dest.name)
                stats[category] += 1
            except PermissionError:
                logging.warning("Permission denied, skipped: %s", src.name)
                stats["Skipped"] += 1
            except FileExistsError:
                logging.warning("File already exists, skipped: %s", src.name)
                stats["Skipped"] += 1
            except OSError as err:
                logging.error("Could not move %s: %s", src.name, err)
                stats["Skipped"] += 1

    return stats


def print_summary(stats: Counter, dry_run: bool) -> None:
    skipped = stats.pop("Skipped", 0)
    total = sum(stats.values())
    print("\n" + "=" * 40)
    print(" EXECUTION SUMMARY" + (" (dry run)" if dry_run else ""))
    print("=" * 40)
    for category, count in sorted(stats.items()):
        print(f" {category:<12} {count:>5} file(s)")
    print("-" * 40)
    print(f" {'Relocated':<12} {total:>5}")
    print(f" {'Skipped':<12} {skipped:>5}")
    print("=" * 40)


def main():
    parser = argparse.ArgumentParser(description="Organize files into folders by type.")
    parser.add_argument("folder", help="Folder to organize, e.g. ~/Downloads")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving files")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        parser.error(f"Not a folder: {folder}")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-7s %(message)s",
        handlers=[logging.StreamHandler(),
                  logging.FileHandler("organizer.log", encoding="utf-8")],
    )
    logging.info("Organizing %s", folder)
    stats = organize(folder, dry_run=args.dry_run)
    print_summary(stats, args.dry_run)


if __name__ == "__main__":
    main()
