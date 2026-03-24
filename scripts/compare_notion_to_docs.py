#!/usr/bin/env python3
"""
Compare Notion CSV activity data against markdown design docs for Weeks 2–9.

Reports:
  - Activities in CSV but missing from markdown (by Activity ID)
  - Activities in markdown but missing from CSV
  - Field-level differences for matching activities (Time, Category, Format, Name, Notes)
  - Time totals: CSV sum vs markdown stated total vs markdown row sum
  - Summary of total discrepancies across all weeks
"""

import csv
import re
import os
import sys
import unicodedata
from pathlib import Path
from collections import OrderedDict

# ---------------------------------------------------------------------------
# Paths (auto-detect project root from script location)
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

CSV_PATH = PROJECT_ROOT / "Riipen Career Catalyst — Activity Breakdown c71532f48aae46fea5c2e162a4fcd358.csv"
DOCS_DIR = PROJECT_ROOT / "weekly_design_docs"

WEEKS = range(2, 10)  # 2..9

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize_text(s: str) -> str:
    """Normalize a string for comparison: collapse whitespace, strip, lowercase."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    # Replace smart quotes / curly quotes with straight ones
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2014", "—").replace("\u2013", "–")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def normalize_note(s: str) -> str:
    """Normalize a note for loose comparison: strip whitespace, punctuation noise."""
    s = normalize_text(s)
    # Strip trailing periods/semicolons for comparison
    s = s.rstrip(";. ")
    return s


def strip_bold(s: str) -> str:
    """Remove markdown bold markers."""
    return s.replace("**", "")


def extract_minutes(text: str) -> int | None:
    """Extract a minute value from text like '500 min', '~8 hrs 20 min (500 min)', '585 min (~9 hrs 45 min)', etc."""
    # First try: NNN min inside parentheses, e.g. "(500 min)" or "(460 min)"
    m = re.search(r"\((\d+)\s*min\)", text)
    if m:
        return int(m.group(1))
    # Second try: NNN min at the start or standalone, e.g. "585 min (~9 hrs 45 min)"
    m = re.search(r"(\d{3,})\s*min", text)
    if m:
        return int(m.group(1))
    # Fallback: any number before "min"
    m = re.search(r"(\d+)\s*min", text)
    if m:
        return int(m.group(1))
    return None


# ---------------------------------------------------------------------------
# CSV parsing
# ---------------------------------------------------------------------------

def load_csv_activities() -> dict[int, list[dict]]:
    """Load CSV and return dict keyed by week number -> list of activity dicts."""
    weeks: dict[int, list[dict]] = {}
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                week_num = int(row["Week Number"])
            except (ValueError, KeyError):
                continue
            activity = {
                "id": row.get("Activity ID", "").strip(),
                "name": row.get("Activity Name", "").strip(),
                "category": row.get("Category", "").strip(),
                "format": row.get("Format", "").strip(),
                "time": int(row.get("Time (min)", 0) or 0),
                "notes": row.get("Notes", "").strip(),
            }
            weeks.setdefault(week_num, []).append(activity)
    return weeks


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------

def parse_md_table_rows(lines: list[str], start_idx: int) -> list[list[str]]:
    """Parse markdown table rows starting at start_idx.
    Returns list of cell-value lists (excluding header and separator rows)."""
    rows = []
    # Find header row (first pipe-delimited line)
    i = start_idx
    while i < len(lines) and not lines[i].strip().startswith("|"):
        i += 1
    if i >= len(lines):
        return rows
    # Skip header row
    i += 1
    # Skip separator row (|---|---|...)
    if i < len(lines) and re.match(r"\|[\s:*-]+\|", lines[i].strip()):
        i += 1
    # Read data rows
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.split("|")]
        # split on | gives empty strings at start/end
        cells = cells[1:-1] if len(cells) > 2 else cells
        rows.append(cells)
        i += 1
    return rows


def parse_markdown_file(filepath: Path) -> dict:
    """Parse a weekly design doc markdown file.

    Returns dict with:
      - 'stated_total': int or None  (minutes from At a Glance)
      - 'activities': list of dicts with id, name, category, format, time, notes
    """
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()

    result = {
        "stated_total": None,
        "activities": [],
    }

    # --- Parse At a Glance total ---
    for line in lines:
        if "Total Student Time" in line:
            mins = extract_minutes(line)
            if mins:
                result["stated_total"] = mins
            break

    # --- Find the activity table ---
    # Look for the table header row that contains columns: #, Category, Activity, Format, Min, Note
    table_start = None
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("|") and "Category" in stripped and "Activity" in stripped and "Min" in stripped:
            table_start = idx
            break

    if table_start is None:
        return result

    # Parse table rows
    rows = parse_md_table_rows(lines, table_start)

    for cells in rows:
        if len(cells) < 6:
            continue
        raw_id = strip_bold(cells[0]).strip()
        category = strip_bold(cells[1]).strip()
        name = strip_bold(cells[2]).strip()
        fmt = strip_bold(cells[3]).strip()
        time_str = strip_bold(cells[4]).strip()
        note = strip_bold(cells[5]).strip() if len(cells) > 5 else ""

        # Skip TOTAL row
        if "TOTAL" in raw_id.upper() or "TOTAL" in category.upper() or "TOTAL" in name.upper():
            continue
        # Skip empty ID rows
        if not raw_id:
            continue

        try:
            time_val = int(re.sub(r"[^\d]", "", time_str)) if time_str else 0
        except ValueError:
            time_val = 0

        result["activities"].append({
            "id": raw_id,
            "name": name,
            "category": category,
            "format": fmt,
            "time": time_val,
            "notes": note,
        })

    return result


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

def compare_week(week_num: int, csv_activities: list[dict], md_data: dict) -> dict:
    """Compare CSV activities vs markdown activities for one week.

    Returns a report dict with:
      - csv_only: list of activity IDs in CSV but not markdown
      - md_only: list of activity IDs in markdown but not CSV
      - differences: list of dicts describing field diffs for matching IDs
      - time_csv_total: sum of CSV times
      - time_md_stated: stated total from At a Glance
      - time_md_row_sum: sum of markdown activity row times
    """
    csv_by_id = OrderedDict()
    for a in csv_activities:
        csv_by_id[a["id"]] = a

    md_by_id = OrderedDict()
    for a in md_data["activities"]:
        md_by_id[a["id"]] = a

    csv_ids = set(csv_by_id.keys())
    md_ids = set(md_by_id.keys())

    csv_only = sorted(csv_ids - md_ids)
    md_only = sorted(md_ids - csv_ids)
    common = sorted(csv_ids & md_ids)

    differences = []
    for aid in common:
        ca = csv_by_id[aid]
        ma = md_by_id[aid]
        diffs = []

        # Compare Time
        if ca["time"] != ma["time"]:
            diffs.append(("Time (min)", str(ca["time"]), str(ma["time"])))

        # Compare Category
        if normalize_text(ca["category"]) != normalize_text(ma["category"]):
            diffs.append(("Category", ca["category"], ma["category"]))

        # Compare Format
        if normalize_text(ca["format"]) != normalize_text(ma["format"]):
            diffs.append(("Format", ca["format"], ma["format"]))

        # Compare Activity Name
        if normalize_text(ca["name"]) != normalize_text(ma["name"]):
            diffs.append(("Activity Name", ca["name"], ma["name"]))

        # Compare Notes (normalized)
        if normalize_note(ca["notes"]) != normalize_note(ma["notes"]):
            diffs.append(("Notes", ca["notes"], ma["notes"]))

        if diffs:
            differences.append({"id": aid, "fields": diffs})

    return {
        "csv_only": csv_only,
        "md_only": md_only,
        "differences": differences,
        "time_csv_total": sum(a["time"] for a in csv_activities),
        "time_md_stated": md_data["stated_total"],
        "time_md_row_sum": sum(a["time"] for a in md_data["activities"]),
        "csv_only_details": {aid: csv_by_id[aid] for aid in csv_only},
        "md_only_details": {aid: md_by_id[aid] for aid in md_only},
    }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(week_num: int, report: dict) -> int:
    """Print a readable report for one week. Returns count of discrepancies."""
    discrepancies = 0
    has_issues = False

    header = f"WEEK {week_num}"
    print(f"\n{'=' * 70}")
    print(f"  {header}")
    print(f"{'=' * 70}")

    # --- Time totals ---
    csv_total = report["time_csv_total"]
    md_stated = report["time_md_stated"]
    md_row_sum = report["time_md_row_sum"]

    print(f"\n  Time Totals:")
    print(f"    CSV sum:             {csv_total} min")
    print(f"    Markdown stated:     {md_stated} min" if md_stated else "    Markdown stated:     (not found)")
    print(f"    Markdown row sum:    {md_row_sum} min")

    time_issues = []
    if csv_total != md_row_sum:
        time_issues.append(f"CSV sum ({csv_total}) != Markdown row sum ({md_row_sum})")
    if md_stated is not None and csv_total != md_stated:
        time_issues.append(f"CSV sum ({csv_total}) != Markdown stated ({md_stated})")
    if md_stated is not None and md_row_sum != md_stated:
        time_issues.append(f"Markdown row sum ({md_row_sum}) != Markdown stated ({md_stated})")

    if time_issues:
        has_issues = True
        for t in time_issues:
            discrepancies += 1
            print(f"    ** MISMATCH: {t}")
    else:
        print(f"    (all match)")

    # --- CSV-only activities ---
    if report["csv_only"]:
        has_issues = True
        print(f"\n  Activities in CSV but NOT in markdown ({len(report['csv_only'])}):")
        for aid in report["csv_only"]:
            discrepancies += 1
            detail = report["csv_only_details"][aid]
            print(f"    + {aid}: {detail['name']}")
            print(f"      Category: {detail['category']}  |  Format: {detail['format']}  |  Time: {detail['time']} min")

    # --- Markdown-only activities ---
    if report["md_only"]:
        has_issues = True
        print(f"\n  Activities in markdown but NOT in CSV ({len(report['md_only'])}):")
        for aid in report["md_only"]:
            discrepancies += 1
            detail = report["md_only_details"][aid]
            print(f"    - {aid}: {detail['name']}")
            print(f"      Category: {detail['category']}  |  Format: {detail['format']}  |  Time: {detail['time']} min")

    # --- Field differences for matching activities ---
    if report["differences"]:
        has_issues = True
        print(f"\n  Field differences for matching activities ({len(report['differences'])} activities):")
        for diff in report["differences"]:
            discrepancies += len(diff["fields"])
            print(f"\n    {diff['id']}:")
            for field, csv_val, md_val in diff["fields"]:
                if field == "Notes":
                    print(f"      {field}:")
                    print(f"        CSV: {csv_val[:120]}{'...' if len(csv_val) > 120 else ''}")
                    print(f"        MD:  {md_val[:120]}{'...' if len(md_val) > 120 else ''}")
                else:
                    print(f"      {field}:")
                    print(f"        CSV: {csv_val}")
                    print(f"        MD:  {md_val}")

    if not has_issues:
        print(f"\n  No discrepancies found.")

    return discrepancies


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not CSV_PATH.exists():
        print(f"ERROR: CSV file not found at {CSV_PATH}")
        sys.exit(1)

    csv_data = load_csv_activities()
    total_discrepancies = 0
    weeks_with_diffs = 0

    print("=" * 70)
    print("  NOTION CSV vs MARKDOWN DESIGN DOCS — COMPARISON REPORT")
    print(f"  Weeks: {min(WEEKS)}–{max(WEEKS)}")
    print("=" * 70)

    for week_num in WEEKS:
        md_path = DOCS_DIR / f"week{week_num}-design-doc.md"
        if not md_path.exists():
            print(f"\n{'=' * 70}")
            print(f"  WEEK {week_num}")
            print(f"{'=' * 70}")
            print(f"  WARNING: Markdown file not found: {md_path.name}")
            continue

        csv_activities = csv_data.get(week_num, [])
        if not csv_activities:
            print(f"\n{'=' * 70}")
            print(f"  WEEK {week_num}")
            print(f"{'=' * 70}")
            print(f"  WARNING: No CSV activities found for week {week_num}")
            continue

        md_data = parse_markdown_file(md_path)
        report = compare_week(week_num, csv_activities, md_data)
        disc = print_report(week_num, report)
        total_discrepancies += disc
        if disc > 0:
            weeks_with_diffs += 1

    # --- Summary ---
    print(f"\n{'=' * 70}")
    print(f"  SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Weeks compared:            {len(list(WEEKS))}")
    print(f"  Weeks with discrepancies:  {weeks_with_diffs}")
    print(f"  Total discrepancies:       {total_discrepancies}")
    print()


if __name__ == "__main__":
    main()
