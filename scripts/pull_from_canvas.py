#!/usr/bin/env python3
"""
Pull current Canvas LMS page bodies back into local `.canvas.html` files.

Reverse of push_to_canvas.py. Canvas is the source of truth post-Rachel-edit
(see memory `feedback_canvas_side_edits_reverse_sync`). This script handles the
mechanical pull + per-page diff report; the `.md` reverse-update is a separate
editorial step Claude does by reading the diff.

Usage:
    python3 scripts/pull_from_canvas.py weekly_content/week01/page1-overview.md
    python3 scripts/pull_from_canvas.py --week 1
    python3 scripts/pull_from_canvas.py --all
    python3 scripts/pull_from_canvas.py --week 1 --report-only   # don't write files
"""

import argparse
import difflib
import os
import re
import sys
import urllib.parse
from pathlib import Path

# Reuse infrastructure from the push script
sys.path.insert(0, str(Path(__file__).resolve().parent))
from push_to_canvas import (  # noqa: E402
    CanvasClient,
    CanvasError,
    canvas_title,
    derive_slug,
    load_env,
)
from md_to_canvas_html import (  # noqa: E402
    collect_week_pages,
    convert_file,
    output_path_for,
)


def get_page_body(client: CanvasClient, slug: str):
    """GET /api/v1/courses/:id/pages/:slug. Returns the JSON dict (with `body`,
    `title`, `updated_at`, `url`) or None on 404."""
    path = f"/api/v1/courses/{client.course_id}/pages/{urllib.parse.quote(slug, safe='')}"
    try:
        return client._request("GET", path)
    except CanvasError as e:
        if "HTTP 404" in str(e):
            return None
        raise


# ── Diff reporting ───────────────────────────────────────────────────────────


CANVAS_MEDIA_PATTERNS = [
    (re.compile(r"<iframe\b", re.IGNORECASE), "iframe"),
    (re.compile(r"<video\b", re.IGNORECASE), "video"),
    (re.compile(r"/courses/\d+/files/\d+", re.IGNORECASE), "course-file"),
    (re.compile(r"instructuremedia\.com|kaltura", re.IGNORECASE), "media-host"),
]

CANVAS_INTERNAL_LINK = re.compile(
    r'<a[^>]+href="[^"]*/courses/\d+/(?:pages|files|assignments|modules|quizzes)[^"]*"',
    re.IGNORECASE,
)


def detect_new_embeds(old_html: str, new_html: str):
    """Return a list of strings describing media / link additions in `new` that
    aren't in `old`. Heuristic — surfaces strong signals of Canvas-side edits."""
    notes = []
    for pat, label in CANVAS_MEDIA_PATTERNS:
        old_n = len(pat.findall(old_html))
        new_n = len(pat.findall(new_html))
        if new_n > old_n:
            notes.append(f"+{new_n - old_n} <{label}> tag(s)")
    old_links = set(CANVAS_INTERNAL_LINK.findall(old_html))
    new_links = set(CANVAS_INTERNAL_LINK.findall(new_html))
    added = new_links - old_links
    if added:
        notes.append(f"+{len(added)} internal Canvas link(s)")
    return notes


def short_diff(old_html: str, new_html: str, context_lines: int = 2):
    """Compact unified diff for at-a-glance review. Truncated."""
    diff = list(difflib.unified_diff(
        old_html.splitlines(),
        new_html.splitlines(),
        fromfile="local",
        tofile="canvas",
        n=context_lines,
        lineterm="",
    ))
    return diff


def report_diff(label: str, old_html: str, new_html: str, max_lines: int = 20):
    if old_html is None:
        print(f"  [NEW LOCAL FILE] no prior .canvas.html — pulled content is the new baseline ({len(new_html)} bytes)")
        return
    if old_html == new_html:
        print("  [NO DIFF] Canvas body matches existing .canvas.html exactly")
        return
    old_lines = old_html.splitlines()
    new_lines = new_html.splitlines()
    added = sum(1 for l in difflib.ndiff(old_lines, new_lines) if l.startswith("+ "))
    removed = sum(1 for l in difflib.ndiff(old_lines, new_lines) if l.startswith("- "))
    print(f"  [DIFF] +{added} / -{removed} lines  (local {len(old_lines)} → canvas {len(new_lines)})")
    embed_notes = detect_new_embeds(old_html, new_html)
    if embed_notes:
        print(f"    Canvas-side additions: {', '.join(embed_notes)}")
    diff_lines = short_diff(old_html, new_html)
    if diff_lines:
        print(f"    Unified diff (first {max_lines} lines):")
        for line in diff_lines[:max_lines]:
            print(f"      {line}")
        if len(diff_lines) > max_lines:
            print(f"      … ({len(diff_lines) - max_lines} more lines)")


# ── Per-page pull ────────────────────────────────────────────────────────────


def pull_one(client: CanvasClient, md_path: Path, report_only: bool) -> dict:
    """Pull one page. Returns {status, slug, title, ...} summary."""
    meta, _ = convert_file(md_path)
    slug = derive_slug(md_path, meta)
    title = canvas_title(md_path, meta)
    print(f"\n→ {md_path}  (slug: {slug})")

    page = get_page_body(client, slug)
    if page is None:
        print(f"  [404] Canvas has no page at slug {slug!r} — skipping")
        return {"status": "missing", "slug": slug, "path": md_path}

    canvas_html = page.get("body") or ""
    canvas_title_returned = page.get("title", "")
    canvas_updated_at = page.get("updated_at", "")
    print(f"  Canvas: title={canvas_title_returned!r}  updated_at={canvas_updated_at}")

    out_path = output_path_for(md_path)
    old_html = out_path.read_text(encoding="utf-8") if out_path.exists() else None
    report_diff(out_path.name, old_html, canvas_html)

    if not report_only:
        out_path.write_text(canvas_html, encoding="utf-8")
        print(f"  Wrote: {out_path} ({len(canvas_html)} bytes)")

    return {
        "status": "pulled",
        "slug": slug,
        "title": title,
        "canvas_title": canvas_title_returned,
        "path": md_path,
        "out_path": out_path,
        "changed": old_html != canvas_html,
        "canvas_updated_at": canvas_updated_at,
    }


# ── Local index for reverse mapping ──────────────────────────────────────────


def build_local_slug_index():
    """Walk every weekly_content/week*/page*.md (excluding video/audio/interactive
    companions) and return {slug: md_path}. Lets us surface Canvas pages whose
    slugs don't correspond to any local source (e.g., graded-* pages Rachel
    created Canvas-side)."""
    index = {}
    weekly = Path("weekly_content")
    if not weekly.exists():
        return index
    for week_dir in sorted(weekly.glob("week*")):
        for md in week_dir.glob("page*.md"):
            if any(suffix in md.name for suffix in ("-video.md", "-audio.md", "-interactive.md")):
                continue
            try:
                meta, _ = convert_file(md)
            except Exception as e:
                print(f"  ! could not parse {md}: {e}", file=sys.stderr)
                continue
            slug = derive_slug(md, meta)
            if slug in index:
                print(f"  ! slug collision: {slug} → {md} and {index[slug]}", file=sys.stderr)
            index[slug] = md
    return index


def report_canvas_only_pages(client: CanvasClient, local_index: dict):
    """List Canvas pages whose slug is NOT in the local index — these are
    pages Rachel created Canvas-side and we have no local source for."""
    print("\nScanning Canvas course for pages without a local source…")
    try:
        pages = client.list_pages()
    except CanvasError as e:
        print(f"  ! could not list Canvas pages: {e}", file=sys.stderr)
        return
    canvas_slugs = {p.get("url"): p for p in pages if p.get("url")}
    orphans = sorted(s for s in canvas_slugs if s not in local_index)
    if not orphans:
        print("  All Canvas page slugs have a matching local source.")
        return
    print(f"  Canvas-only pages ({len(orphans)}) — no local .md exists:")
    for slug in orphans:
        p = canvas_slugs[slug]
        print(f"    - {slug}  (title: {p.get('title','')!r}, updated: {p.get('updated_at','')})")


# ── CLI ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Pull Canvas LMS page bodies back into local .canvas.html files")
    parser.add_argument("input", nargs="?", help="Input .md file (or use --week / --all)")
    parser.add_argument("--week", type=int, help="Pull all pages in weekly_content/weekNN/")
    parser.add_argument("--all", action="store_true", help="Pull every page in every week")
    parser.add_argument("--course-id", help="Override CANVAS_COURSE_ID from env")
    parser.add_argument("--report-only", action="store_true",
                        help="Don't write .canvas.html files; just print the diff summary")
    parser.add_argument("--list-orphans", action="store_true",
                        help="Also list Canvas pages whose slug has no matching local .md")
    args = parser.parse_args()

    if not args.week and not args.input and not args.all:
        parser.print_help()
        sys.exit(1)

    project_root = Path(__file__).resolve().parent.parent
    load_env(project_root / ".env")

    base_url = os.environ.get("CANVAS_BASE_URL")
    token = os.environ.get("CANVAS_API_TOKEN")
    course_id = args.course_id or os.environ.get("CANVAS_COURSE_ID")
    missing = [k for k, v in [
        ("CANVAS_BASE_URL", base_url),
        ("CANVAS_API_TOKEN", token),
        ("CANVAS_COURSE_ID", course_id),
    ] if not v]
    if missing:
        print(f"Error: missing env vars: {', '.join(missing)}", file=sys.stderr)
        print("Set these in .env at the project root.", file=sys.stderr)
        sys.exit(1)

    client = CanvasClient(base_url, token, course_id)

    # Gather input markdown paths
    if args.all:
        inputs = []
        for week_dir in sorted(Path("weekly_content").glob("week*")):
            m = re.match(r"week(\d+)", week_dir.name)
            if m:
                inputs.extend(collect_week_pages(int(m.group(1))))
    elif args.week is not None:
        inputs = collect_week_pages(args.week)
    else:
        inputs = [Path(args.input)]

    if not inputs:
        print("No input pages found.", file=sys.stderr)
        sys.exit(1)

    mode = "REPORT-ONLY" if args.report_only else "PULL + WRITE"
    print(f"Pulling {len(inputs)} page(s) from course {course_id} [{mode}]")

    summaries = [pull_one(client, p, args.report_only) for p in inputs]

    if args.list_orphans:
        report_canvas_only_pages(client, build_local_slug_index())

    # Final summary
    pulled = [s for s in summaries if s["status"] == "pulled"]
    missing_pages = [s for s in summaries if s["status"] == "missing"]
    changed = [s for s in pulled if s["changed"]]
    print("\n" + "=" * 60)
    print(f"Summary: {len(pulled)} pulled, {len(changed)} with diffs, {len(missing_pages)} missing on Canvas")
    if changed:
        print("\nPages with Canvas-side changes (review for .md reverse-update):")
        for s in changed:
            print(f"  - {s['path']}  (slug: {s['slug']})")
    if missing_pages:
        print("\nPages with no Canvas counterpart (slug mismatch or never pushed):")
        for s in missing_pages:
            print(f"  - {s['path']}  (expected slug: {s['slug']})")

    print(
        "\nNext step for pages with diffs: reverse-update the .md per "
        "feedback_canvas_side_edits_reverse_sync (mirror substantive text/link "
        "changes, leave [VIDEO:] placeholders alone, bump last_updated)."
    )


if __name__ == "__main__":
    main()
