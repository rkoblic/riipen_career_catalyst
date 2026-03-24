"""Convert SRT subtitle files to WebVTT format for Canvas LMS.

Usage:
    python scripts/srt_to_vtt.py path/to/file.srt
    python scripts/srt_to_vtt.py path/to/directory   # converts all .srt files in directory

Output: .vtt file alongside each .srt file.
"""

import sys
import re
from pathlib import Path


def convert_srt_to_vtt(srt_path: Path) -> Path:
    text = srt_path.read_text(encoding="utf-8-sig")  # handle BOM
    # Replace comma with period in timestamps
    text = re.sub(r"(\d{2}:\d{2}:\d{2}),(\d{3})", r"\1.\2", text)
    # Strip cue numbers (lines that are just digits before a timestamp)
    text = re.sub(r"^\d+\s*$", "", text, flags=re.MULTILINE)
    # Strip leading/trailing whitespace from each line (fixes cue text spacing)
    text = "\n".join(line.strip() for line in text.splitlines())
    # Clean up extra blank lines
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    vtt_path = srt_path.with_suffix(".vtt")
    vtt_path.write_text(f"WEBVTT\n\n{text}\n", encoding="utf-8")
    return vtt_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/srt_to_vtt.py <file.srt | directory>")
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_file() and target.suffix == ".srt":
        out = convert_srt_to_vtt(target)
        print(f"Converted: {out}")
    elif target.is_dir():
        srt_files = list(target.rglob("*.srt"))
        if not srt_files:
            print(f"No .srt files found in {target}")
            sys.exit(1)
        for srt in srt_files:
            out = convert_srt_to_vtt(srt)
            print(f"Converted: {out}")
    else:
        print(f"Not a valid .srt file or directory: {target}")
        sys.exit(1)


if __name__ == "__main__":
    main()
