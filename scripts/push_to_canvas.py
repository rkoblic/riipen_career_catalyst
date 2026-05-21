#!/usr/bin/env python3
"""
Push converted Canvas-HTML pages to a Canvas LMS course via the REST API.

Reads CANVAS_API_TOKEN, CANVAS_BASE_URL, and CANVAS_COURSE_ID from a `.env`
file in the project root (gitignored). Converts markdown → Canvas HTML using
md_to_canvas_html.py, then `PUT`s each page to Canvas via the wiki_pages API.
Pages are created as **unpublished** by default so they can be reviewed before
going live.

Usage:
    python3 scripts/push_to_canvas.py <input.md>
    python3 scripts/push_to_canvas.py --week 6
    python3 scripts/push_to_canvas.py --week 6 --dry-run    # convert + report, no API
    python3 scripts/push_to_canvas.py --week 6 --yes        # skip confirmation pause
    python3 scripts/push_to_canvas.py --week 6 --publish    # publish (default: unpublished)

Slug convention (matches Riipen's existing course 107):
    page1-overview.md     → week-N-overview
    page10-whats-next.md  → week-N-whats-next
    other pages           → slugified frontmatter `title` (e.g., "Team Charter" → team-charter)
    Override per file via frontmatter `canvas_page_url:` if needed.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# Allow importing the converter from the same scripts/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_to_canvas_html import (  # noqa: E402
    collect_week_pages,
    convert_file,
    output_path_for,
)


# ── .env loading (no external dependency) ────────────────────────────────────


def load_env(env_path: Path):
    """Tiny .env parser. KEY=VALUE per line, # for comments. Quoted values
    have surrounding quotes stripped. Sets os.environ for missing keys only."""
    if not env_path.exists():
        return
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip()
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        os.environ.setdefault(key, val)


# ── Slug derivation ──────────────────────────────────────────────────────────


def slugify(text: str) -> str:
    """Match Canvas's slug convention as observed in course 107:
        'Reflection #1'           → 'reflection-number-1'
        "Week 6 What's Next"      → 'week-6-whats-next'   (apostrophes dropped)
        'AI in Today's Workplace' → 'ai-in-todays-workplace'
        'Intro (DEAL)'            → 'intro-deal'
        'A & B'                   → 'a-and-b'
    """
    s = text.strip().lower()
    s = s.replace("#", " number ").replace("&", " and ")
    # Drop apostrophes entirely (straight, curly, and right-single-quote variants)
    s = re.sub(r"['‘’ʼ]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


PAGE_FILENAME = re.compile(r"^page(\d+)-(.+)\.md$")


def page_kind(input_path: Path, frontmatter: dict):
    """Classify a content page. Returns (kind, week_int) where kind is one of:
    'overview', 'whats_next', 'content'. week_int may be None."""
    week = frontmatter.get("week")
    if not week:
        m = re.search(r"week(\d+)", str(input_path))
        if m:
            week = str(int(m.group(1)))
    week_int = int(week) if week else None

    name = input_path.name
    m = PAGE_FILENAME.match(name)
    page_num = int(m.group(1)) if m else None
    short = m.group(2) if m else input_path.stem

    if page_num == 1 and "overview" in short:
        return "overview", week_int
    if "whats-next" in short:
        return "whats_next", week_int
    return "content", week_int


def canvas_title(input_path: Path, frontmatter: dict) -> str:
    """Compute the title sent to Canvas. For overview/whats-next pages, prefix
    with 'Week N' so Canvas's auto-slugify produces 'week-N-overview' /
    'week-N-whats-next'. For content pages, pass through the frontmatter title."""
    kind, week_int = page_kind(input_path, frontmatter)
    if kind == "overview" and week_int is not None:
        return f"Week {week_int} Overview"
    if kind == "whats_next" and week_int is not None:
        return f"Week {week_int} What's Next"
    title = frontmatter.get("title", "").strip()
    return title or input_path.stem.replace("-", " ").title()


def derive_slug(input_path: Path, frontmatter: dict) -> str:
    """Slug derivation rules (in order):
    1. Frontmatter `canvas_page_url:` override wins.
    2. page1-overview.md → week-N-overview
    3. page*-whats-next.md → week-N-whats-next
    4. Otherwise: slugified canvas_title (which falls through to frontmatter title).

    The slug is what Canvas will assign based on the title we send. Keeping these
    aligned means re-runs reliably UPDATE existing pages instead of creating
    duplicates at unexpected slugs."""
    if frontmatter.get("canvas_page_url"):
        return frontmatter["canvas_page_url"].strip()
    return slugify(canvas_title(input_path, frontmatter))


# ── Canvas API ───────────────────────────────────────────────────────────────


class CanvasError(Exception):
    pass


class CanvasClient:
    def __init__(self, base_url: str, token: str, course_id: str):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.course_id = str(course_id)

    def _request(self, method: str, path: str, body=None, query=None):
        url = f"{self.base_url}{path}"
        if query:
            url += "?" + urllib.parse.urlencode(query)

        data = None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=data, method=method, headers=headers)

        # Retry up to 3 times on 5xx/network errors
        last_err = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    raw = resp.read().decode("utf-8")
                    return json.loads(raw) if raw else None
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="replace")
                if 500 <= e.code < 600 and attempt < 2:
                    last_err = e
                    time.sleep(1.5 * (attempt + 1))
                    continue
                raise CanvasError(
                    f"HTTP {e.code} from {method} {path}: {err_body}"
                ) from e
            except urllib.error.URLError as e:
                if attempt < 2:
                    last_err = e
                    time.sleep(1.5 * (attempt + 1))
                    continue
                raise CanvasError(f"Network error on {method} {path}: {e}") from e
        raise CanvasError(f"Retries exhausted for {method} {path}: {last_err}")

    def list_pages(self):
        """Return all pages for the course, paging through results."""
        pages = []
        path = f"/api/v1/courses/{self.course_id}/pages"
        query = {"per_page": 100}
        while path:
            url = f"{self.base_url}{path}"
            if query:
                url += "?" + urllib.parse.urlencode(query)
                query = None  # cursor URL on subsequent pages already includes params
            req = urllib.request.Request(
                url,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/json",
                },
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
                pages.extend(json.loads(raw))
                # Parse Link header for next page
                link_header = resp.headers.get("Link", "")
                next_url = self._parse_next_link(link_header)
                if not next_url:
                    break
                # Convert absolute URL to path
                parsed = urllib.parse.urlparse(next_url)
                path = parsed.path + ("?" + parsed.query if parsed.query else "")
                # We've baked the query into path; null out query for next iter
                if "?" in path:
                    path, _, q = path.partition("?")
                    query = dict(urllib.parse.parse_qsl(q))
        return pages

    @staticmethod
    def _parse_next_link(link_header):
        if not link_header:
            return None
        for part in link_header.split(","):
            segs = part.strip().split(";")
            if len(segs) < 2:
                continue
            url_part = segs[0].strip()
            rel_part = "".join(s.strip() for s in segs[1:])
            if 'rel="next"' in rel_part and url_part.startswith("<") and url_part.endswith(">"):
                return url_part[1:-1]
        return None

    def upsert_page(self, slug: str, title: str, body_html: str, published: bool = False):
        """Create or update a page. Canvas's PUT on a page URL is upsert.

        Note: we pass `wiki_page[url]` matching the path slug. Canvas honors this
        on page CREATION (locks the new page's slug to whatever we send). On
        EXISTING page updates, Canvas appears to ignore `wiki_page[url]` and
        re-derives the slug from the title — empirically observed 2026-05-21
        when the W13 page2 title changed and Canvas rewrote the slug from
        `graded-final-deliverables` to `project-deliverables-submission`
        regardless of `wiki_page[url]`. The old slug continues to resolve via
        Canvas's auto-redirect, so existing internal links don't break."""
        path = f"/api/v1/courses/{self.course_id}/pages/{urllib.parse.quote(slug, safe='')}"
        payload = {
            "wiki_page": {
                "title": title,
                "url": slug,
                "body": body_html,
                "published": bool(published),
                "editing_roles": "teachers",
            }
        }
        return self._request("PUT", path, body=payload)

    def list_modules(self):
        return self._request("GET", f"/api/v1/courses/{self.course_id}/modules", query={"per_page": 100})

    def list_module_items(self, module_id):
        return self._request(
            "GET", f"/api/v1/courses/{self.course_id}/modules/{module_id}/items",
            query={"per_page": 100},
        )

    def add_page_to_module(self, module_id, page_slug, position):
        return self._request(
            "POST", f"/api/v1/courses/{self.course_id}/modules/{module_id}/items",
            body={"module_item": {"type": "Page", "page_url": page_slug, "position": position}},
        )

    def update_module_item_position(self, module_id, item_id, position):
        return self._request(
            "PUT", f"/api/v1/courses/{self.course_id}/modules/{module_id}/items/{item_id}",
            body={"module_item": {"position": position}},
        )


# ── Pipeline ─────────────────────────────────────────────────────────────────


def gather_inputs(args):
    """Return a list of input markdown Paths to process."""
    if args.week is not None:
        return collect_week_pages(args.week)
    return [Path(args.input)]


def build_plan(input_paths, existing_slugs, use_html=False):
    """For each input, convert and derive its slug + page title.
    Returns a list of dicts with the data needed to push.

    If use_html=True, look for an existing `.canvas.html` file alongside each
    source markdown and use that as the body instead of running the converter.
    Used by the Claude-driven skill workflow where Claude has already produced
    polished HTML files.
    """
    plan = []
    for p in input_paths:
        meta, _baseline_html = convert_file(p)  # always need frontmatter
        if use_html:
            html_path = output_path_for(p)
            if not html_path.exists():
                raise FileNotFoundError(
                    f"--use-html: expected {html_path} alongside {p}, but it does not exist. "
                    f"Run the conversion (skill or md_to_canvas_html.py) first."
                )
            html_out = html_path.read_text(encoding="utf-8")
        else:
            html_out = _baseline_html
        slug = derive_slug(p, meta)
        title = canvas_title(p, meta)
        action = "UPDATE existing" if slug in existing_slugs else "CREATE"
        # Capture follow-ups: video and interactive placeholders the user must
        # finish manually in Canvas.
        videos = re.findall(r"Video: ([^<]+)", html_out)
        interactives = re.findall(r"Interactive: ([^<]+)", html_out)
        plan.append({
            "input": p,
            "slug": slug,
            "title": title,
            "html": html_out,
            "action": action,
            "videos": videos,
            "interactives": interactives,
        })
    return plan


def print_plan(plan, course_id):
    print(f"\nPlan ({len(plan)} page{'s' if len(plan) != 1 else ''}, course {course_id}):")
    for item in plan:
        marker = "[CREATE]            " if item["action"] == "CREATE" else "[UPDATE existing]   "
        print(f"  {marker} {item['slug']:35s}  ←  {item['input']}")


def find_week_module(modules, week_num):
    """Find a module whose name matches `Week N` (with optional colon and subtitle)."""
    pattern = re.compile(rf"^Week\s+{week_num}\b", re.IGNORECASE)
    for m in modules:
        if pattern.match(m["name"]):
            return m
    return None


def place_pages_in_module(client, module, plan):
    """Add or re-position each plan slug in `module` so that the items end up in
    plan order. Idempotent: existing items are left in place but re-positioned;
    missing items are added; items in the module that aren't in the plan are
    left untouched (positioned after the managed items)."""
    desired_slugs = [item["slug"] for item in plan]
    existing_items = client.list_module_items(module["id"])
    existing_by_slug = {it.get("page_url"): it for it in existing_items if it.get("type") == "Page"}

    print(f"\nModule placement → {module['name']!r} (id={module['id']}):")

    failures = []
    for position, slug in enumerate(desired_slugs, start=1):
        if slug in existing_by_slug:
            item_id = existing_by_slug[slug]["id"]
            current_pos = existing_by_slug[slug]["position"]
            if current_pos == position:
                print(f"  {position:2d}. = {slug:42s} (already at position {position})")
                continue
            try:
                client.update_module_item_position(module["id"], item_id, position)
                print(f"  {position:2d}. ↕ {slug:42s} (moved from {current_pos} to {position})")
            except CanvasError as e:
                print(f"  {position:2d}. ✗ {slug:42s} REPOSITION FAILED: {e}", file=sys.stderr)
                failures.append((slug, str(e)))
        else:
            try:
                result = client.add_page_to_module(module["id"], slug, position)
                print(f"  {position:2d}. + {slug:42s} (added at position {position}, item id {result['id']})")
            except CanvasError as e:
                print(f"  {position:2d}. ✗ {slug:42s} ADD FAILED: {e}", file=sys.stderr)
                failures.append((slug, str(e)))

    # Surface non-managed items so Rachel sees them
    non_managed = [it for it in existing_items if it.get("page_url") not in set(desired_slugs)]
    if non_managed:
        print(f"\n  Non-managed items left in place ({len(non_managed)}):")
        for it in sorted(non_managed, key=lambda x: x["position"]):
            print(f"    pos={it['position']}  type={it['type']}  title={it.get('title', '')!r}")

    return failures


def print_followups(plan):
    """Print summary of follow-up work (videos / interactives needing manual upload)."""
    pending_videos = [(p["slug"], v) for p in plan for v in p["videos"]]
    pending_interactives = [(p["slug"], i) for p in plan for i in p["interactives"]]
    if not pending_videos and not pending_interactives:
        return
    print("\nFollow-up work (must be added manually in Canvas):")
    if pending_videos:
        print("  Videos to upload via Rich Content Editor:")
        for slug, title in pending_videos:
            print(f"    - {slug}: {title}")
    if pending_interactives:
        print("  Interactives to embed (waiting on S3 URLs):")
        for slug, title in pending_interactives:
            print(f"    - {slug}: {title}")


# ── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Push markdown content pages to Canvas LMS")
    parser.add_argument("input", nargs="?", help="Input .md file (or use --week)")
    parser.add_argument("--week", type=int, help="Push all pages in weekly_content/weekNN/")
    parser.add_argument("--course-id", help="Override CANVAS_COURSE_ID from env")
    parser.add_argument("--dry-run", action="store_true", help="Convert + report, skip API")
    parser.add_argument("--yes", action="store_true", help="Skip the confirmation pause before pushing")
    parser.add_argument("--publish", action="store_true", help="Publish pages (default: unpublished)")
    parser.add_argument("--write-html", action="store_true",
                        help="Also write .canvas.html files alongside the source markdown")
    parser.add_argument("--module", action="store_true",
                        help="After pushing, place pages in the matching 'Week N' module in source order")
    parser.add_argument("--module-id", type=int,
                        help="Place pages in this module id specifically (overrides --module auto-detect)")
    parser.add_argument("--module-name",
                        help="Place pages in the module whose name starts with this string (case-insensitive)")
    parser.add_argument("--use-html", action="store_true",
                        help="Use existing <source>.canvas.html files instead of running the converter. "
                             "For the Claude-driven skill workflow.")
    args = parser.parse_args()

    if not args.week and not args.input:
        parser.print_help()
        sys.exit(1)

    # Load .env (project root)
    project_root = Path(__file__).resolve().parent.parent
    load_env(project_root / ".env")

    base_url = os.environ.get("CANVAS_BASE_URL")
    token = os.environ.get("CANVAS_API_TOKEN")
    course_id = args.course_id or os.environ.get("CANVAS_COURSE_ID")

    if not args.dry_run:
        missing = [k for k, v in [
            ("CANVAS_BASE_URL", base_url),
            ("CANVAS_API_TOKEN", token),
            ("CANVAS_COURSE_ID", course_id),
        ] if not v]
        if missing:
            print(f"Error: missing env vars: {', '.join(missing)}", file=sys.stderr)
            print("Set these in .env at the project root.", file=sys.stderr)
            sys.exit(1)

    inputs = gather_inputs(args)
    if not inputs:
        print("No input files found.", file=sys.stderr)
        sys.exit(1)
    for p in inputs:
        if not p.exists():
            print(f"Error: {p} does not exist.", file=sys.stderr)
            sys.exit(1)

    # Get existing slugs for collision report (skip in dry-run if no creds)
    existing_slugs = set()
    client = None
    if base_url and token and course_id:
        client = CanvasClient(base_url, token, course_id)
        try:
            existing_pages = client.list_pages()
            existing_slugs = {p["url"] for p in existing_pages}
        except CanvasError as e:
            print(f"Warning: could not list existing pages: {e}", file=sys.stderr)
            if not args.dry_run:
                sys.exit(1)

    # Build the plan (converts each page and derives slugs)
    try:
        plan = build_plan(inputs, existing_slugs, use_html=args.use_html)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print_plan(plan, course_id or "(no course)")

    # Optionally write HTML files alongside the markdown
    if args.write_html:
        for item in plan:
            out = output_path_for(item["input"])
            out.write_text(item["html"], encoding="utf-8")
            print(f"  Wrote: {out}")

    if args.dry_run:
        print_followups(plan)
        print("\n--dry-run: skipping API push.")
        return

    # Confirmation pause
    if not args.yes:
        try:
            answer = input("\nProceed with push? [y/N]: ").strip().lower()
        except EOFError:
            answer = ""
        if answer not in ("y", "yes"):
            print("Aborted.")
            sys.exit(1)

    # Push each page
    print("")
    failures = []
    for item in plan:
        try:
            result = client.upsert_page(
                slug=item["slug"],
                title=item["title"],
                body_html=item["html"],
                published=args.publish,
            )
            page_url = result.get("html_url", "(no html_url returned)")
            state = "published" if args.publish else "unpublished"
            print(f"  ✓ {item['slug']:35s}  →  {page_url} ({state})")
        except CanvasError as e:
            print(f"  ✗ {item['slug']:35s}  →  FAILED: {e}", file=sys.stderr)
            failures.append((item["slug"], str(e)))

    # Module placement (optional)
    module_failures = []
    use_module = args.module or args.module_id or args.module_name
    if use_module and not failures:
        module = None
        if args.module_id:
            modules = client.list_modules()
            module = next((m for m in modules if m["id"] == args.module_id), None)
            if not module:
                print(f"\nWarning: module id {args.module_id} not found in course {course_id}.", file=sys.stderr)
        elif args.module_name:
            modules = client.list_modules()
            needle = args.module_name.lower()
            module = next((m for m in modules if m["name"].lower().startswith(needle)), None)
            if not module:
                print(f"\nWarning: no module name starting with {args.module_name!r} found.", file=sys.stderr)
        else:
            # Auto-detect by week number — only sensible in --week mode
            if args.week is None:
                print("\nWarning: --module auto-detect requires --week. Skipping module placement.",
                      file=sys.stderr)
            else:
                modules = client.list_modules()
                module = find_week_module(modules, args.week)
                if not module:
                    print(f"\nWarning: no module matching 'Week {args.week}' found.", file=sys.stderr)

        if module:
            module_failures = place_pages_in_module(client, module, plan)

    print_followups(plan)

    total_failures = len(failures) + len(module_failures)
    if total_failures:
        print(f"\n{total_failures} operation(s) failed.", file=sys.stderr)
        sys.exit(1)
    print(f"\nPushed {len(plan)} page(s).")


if __name__ == "__main__":
    main()
