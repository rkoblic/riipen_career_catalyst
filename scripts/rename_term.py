#!/usr/bin/env python3
"""
Literal in-place string replace across multiple file globs.

Useful for sweeping terminology changes across the course content. Skips the
companion-file suffixes (`-video.md`, `-audio.md`, `-interactive.md`,
`-synthesia-script.md`) by default so video/audio scripts aren't touched.

Usage:
    python3 scripts/rename_term.py \\
        --old "Final Deliverables" --new "Project Deliverables" \\
        --glob "weekly_content/week*/page*.md" \\
        --glob "weekly_content/week*/page*.canvas.html" \\
        --glob "rubrics/*-learner.md" \\
        [--dry-run] [--include-companions]

Reports per-file replacement counts. `--dry-run` shows what would change
without writing.
"""

import argparse
import sys
from pathlib import Path

COMPANION_SUFFIXES = (
    "-video.md",
    "-audio.md",
    "-interactive.md",
    "-interactive.html",
    "-synthesia-script.md",
)


def is_companion(path: Path) -> bool:
    return any(path.name.endswith(s) for s in COMPANION_SUFFIXES)


def main():
    parser = argparse.ArgumentParser(
        description="Literal in-place string replace across globs."
    )
    parser.add_argument("--old", required=True, help="Literal string to replace")
    parser.add_argument("--new", required=True, help="Replacement string")
    parser.add_argument(
        "--glob",
        action="append",
        required=True,
        dest="globs",
        help="File glob (may be passed multiple times)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write files; just report what would change",
    )
    parser.add_argument(
        "--include-companions",
        action="store_true",
        help="Don't skip -video.md / -audio.md / -interactive.* / -synthesia-script.md",
    )
    args = parser.parse_args()

    # Collect candidate files
    seen: set[Path] = set()
    for pattern in args.globs:
        for p in Path(".").glob(pattern):
            if p.is_file():
                seen.add(p.resolve())

    if not seen:
        print("No files matched the supplied globs.", file=sys.stderr)
        sys.exit(1)

    files = sorted(seen)
    if not args.include_companions:
        files = [f for f in files if not is_companion(f)]

    total_files_changed = 0
    total_replacements = 0
    print(
        f"Scanning {len(files)} file(s) for {args.old!r} → {args.new!r} "
        f"[{'DRY-RUN' if args.dry_run else 'WRITE'}]"
    )
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Skip binaries silently
            continue
        if args.old not in text:
            continue
        count = text.count(args.old)
        new_text = text.replace(args.old, args.new)
        total_files_changed += 1
        total_replacements += count
        rel = path.relative_to(Path.cwd().resolve()) if path.is_absolute() else path
        print(f"  {count:3d}  {rel}")
        if not args.dry_run:
            path.write_text(new_text, encoding="utf-8")

    print(
        f"\n{total_replacements} replacement(s) across {total_files_changed} file(s)"
        f"{' (no writes — dry run)' if args.dry_run else ''}"
    )


if __name__ == "__main__":
    main()
