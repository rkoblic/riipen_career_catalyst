#!/usr/bin/env python3
"""
Update -video.md transcripts and .canvas.html Video Transcript blocks from SRT captions.

SRTs in `weekly_content/week*/Videos/*.srt` are the source of truth — they're exported
from the actual produced video and any drift from the local -video.md is the local file
being stale. This script:

1. Parses each SRT (cue number, timestamp, text)
2. Groups cues into paragraphs based on timing gaps (>1.5s of silence = paragraph break)
3. Finds the matching -video.md by slug
4. Replaces the body (preserves frontmatter + H1)
5. Surgically replaces the matching Video Transcript <details>...</details> block in
   the companion .canvas.html — preserves the video iframe and everything else

Skips:
- SRTs with no matching -video.md (David Park interactive scenarios in W3/6/7)
- Audio scripts (W11 Team_Walkthrough.srt has no speaker labels; reconcile manually)

Usage:
    python3 scripts/update_video_scripts_from_srt.py weekly_content/week01/Videos/foo.srt
    python3 scripts/update_video_scripts_from_srt.py --week 1
    python3 scripts/update_video_scripts_from_srt.py --all
    python3 scripts/update_video_scripts_from_srt.py --week 1 --report-only
"""

import argparse
import difflib
import re
import sys
import unicodedata
from pathlib import Path

PARAGRAPH_GAP_THRESHOLD = 1.5  # seconds — gap between cues that signals a paragraph break

SKIP_SRTS = {
    # David Park scenario videos — no -video.md counterpart; manual content
    "Kickoff Meeting with David Park.srt",
    "Direction Check with David Park.srt",
    "Development Check-in with David Park - Part 1.srt",
    "Development Check-in with David Park - Part 2.srt",
    # W11 audio walkthrough — the SRT has no speaker labels, but the -audio.md
    # is hand-built with `**Dana:**`/`**Renata:**` etc. plus Scene/Length/Production
    # metadata. Auto-overwriting from SRT strips all of that. Reconcile manually.
    "Team_Walkthrough.srt",
}

# Manual SRT → -video.md or -audio.md mappings for cases where the produced
# video title diverged from the script's H1 / [VIDEO:] placeholder title.
# Keyed by SRT filename (without directory).
OVERRIDE_MAP = {
    # W4: produced video renamed; script still says "Why this deliverable matters"
    "context-analysis-and-project-plan_-why-it-matters-captions.srt":
        "weekly_content/week04/page1-overview-video.md",
    # W4: produced video renamed; script likely the synthesis-related one (page4)
    "from-summary-to-synthesis-captions.srt":
        "weekly_content/week04/page4-research-and-analysis-video.md",
    # W7: produced video for the W7 overview ("What makes a check-in useful" → "Effective workplace meetings and check-ins")
    "effective-workplace-meetings-and-check-ins-captions.srt":
        "weekly_content/week07/page1-overview-video.md",
    # W10: produced video matches the interview-question framing; script title "The question you'll have to answer in every interview"
    "mastering-the-_tell-me-about-a-project_-interview-question-captions.srt":
        "weekly_content/week10/page1-overview-video.md",
    # W10: produced video tightened title from "actually sounds like" → "actually is"
    "what-transferable-learning-actually-is-captions.srt":
        "weekly_content/week10/page2-what-youre-learning-video.md",
    # W14: video for picking the anchor experience (W15 reflection 5 framing)
    "picking-one-thing-from-the-whole-course-captions.srt":
        "weekly_content/week15/page4-reflection-5-video.md",
    # W15: produced video has fuller title than the [VIDEO:] placeholder
    "ready,-not-polished_-final-presentation-advice-captions.srt":
        "weekly_content/week15/page2-final-presentation-video.md",
    # W3: produced video for "Prepare a kickoff agenda" — page2 has the [VIDEO:] for this script
    "how-to-write-a-meeting-agenda-that-works-captions.srt":
        "weekly_content/week03/page2-preparing-for-the-kickoff-video.md",
    # W5: page2 references this video
    "how-to-walk-through-a-document-with-a-stakeholder-captions.srt":
        "weekly_content/week05/page2-before-the-direction-check-video.md",
    # W5: page3 references this video
    "listening-without-defending-captions.srt":
        "weekly_content/week05/page3-during-the-direction-check-video.md",
    # W5: page1 (overview) references this video
    "presenting-for-feedback,-not-approval-captions.srt":
        "weekly_content/week05/page1-overview-video.md",
}


# ── SRT parsing ──────────────────────────────────────────────────────────────


def _ts_to_seconds(ts: str) -> float:
    """`00:01:23,456` → 83.456"""
    h, m, rest = ts.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_srt(srt_path: Path):
    """Return list of cues: [(start_s, end_s, text), ...]"""
    text = srt_path.read_text(encoding="utf-8-sig")  # handle BOM
    # Split on blank lines (cue separators)
    blocks = re.split(r"\n\s*\n", text.strip())
    cues = []
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        # First line is the cue number (we ignore it). Find the timestamp line.
        ts_idx = next(
            (i for i, ln in enumerate(lines) if "-->" in ln), None
        )
        if ts_idx is None:
            continue
        start_str, _, end_str = lines[ts_idx].partition("-->")
        start_s = _ts_to_seconds(start_str.strip())
        end_s = _ts_to_seconds(end_str.strip())
        # Everything after the timestamp is the cue text (one cue may span multiple lines)
        cue_text = " ".join(lines[ts_idx + 1 :]).strip()
        # Collapse internal whitespace; trim
        cue_text = re.sub(r"\s+", " ", cue_text)
        if cue_text:
            cues.append((start_s, end_s, cue_text))
    return cues


def cues_to_paragraphs(cues, gap_threshold=PARAGRAPH_GAP_THRESHOLD):
    """Group cues into paragraphs. A gap > threshold between (prev.end, next.start)
    triggers a paragraph break. Returns list of paragraph strings."""
    if not cues:
        return []
    paragraphs = []
    current = [cues[0][2]]
    last_end = cues[0][1]
    for start, end, text in cues[1:]:
        gap = start - last_end
        if gap > gap_threshold:
            paragraphs.append(" ".join(current).strip())
            current = [text]
        else:
            current.append(text)
        last_end = end
    if current:
        paragraphs.append(" ".join(current).strip())
    # Normalize: collapse double spaces, trim
    paragraphs = [re.sub(r"\s+", " ", p).strip() for p in paragraphs]
    return [p for p in paragraphs if p]


# Common sentence-starter words used to detect captioning-tool punctuation gaps.
# Conservative list — these words are very rarely mid-sentence in narration.
_SENTENCE_STARTERS = (
    r"(?:The|This|That|These|Those|It|We|You|Your|They|Their|He|She|"
    r"But|And|So|Now|Here|There|If|When|Before|After|Once|While|"
    r"Although|However|What|Who|Why|How|Each|Either|Most|Some)"
)
# Match: lowercase letter, whitespace, sentence-starter word with a word boundary
_MISSING_PERIOD = re.compile(rf"([a-z])\s+({_SENTENCE_STARTERS})\b")


def fix_missing_periods(text: str) -> str:
    """Insert a period where a captioning tool dropped one. Fires only when a
    lowercase letter is followed by whitespace and a known sentence-starter
    word (`The`, `It`, `We`, `But`, etc.) — conservative enough to be safe in
    narration scripts. Won't fire if there's already any punctuation."""
    return _MISSING_PERIOD.sub(r"\1. \2", text)


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


def split_sentences(text: str) -> list[str]:
    """Naive sentence splitter — splits on `.`/`!`/`?` followed by whitespace and a
    capitalized character or open quote. Good enough for narration scripts."""
    return [s.strip() for s in _SENTENCE_SPLIT.split(text.strip()) if s.strip()]


def align_paragraphs(srt_text: str, existing_paragraphs: list[str]) -> list[str]:
    """Rebuild paragraphs by taking the SRT's canonical text and slotting it into
    the existing .md paragraph structure.

    Strategy: walk through existing paragraphs in order. For each paragraph except
    the last, use its final sentence as an anchor to find the matching position in
    the SRT sentence list (via SequenceMatcher ratio). Take all SRT sentences up to
    that anchor as the new paragraph. Last paragraph gets everything remaining.

    If no good anchor match is found, fall back to a proportional split (allocating
    SRT sentences to paragraphs in proportion to the existing paragraph sizes).
    """
    if not existing_paragraphs:
        return [srt_text.strip()]
    srt_sentences = split_sentences(srt_text)
    if not srt_sentences:
        return existing_paragraphs

    new_paragraphs = []
    cursor = 0  # next unconsumed SRT sentence index

    # Pre-compute proportional sentence counts as fallback
    md_counts = [max(1, len(split_sentences(p))) for p in existing_paragraphs]
    total_md = sum(md_counts)
    total_srt = len(srt_sentences)

    for i, md_para in enumerate(existing_paragraphs):
        if i == len(existing_paragraphs) - 1:
            # Last paragraph: everything remaining
            new_paragraphs.append(" ".join(srt_sentences[cursor:]).strip())
            break

        md_sents = split_sentences(md_para)
        anchor = md_sents[-1] if md_sents else md_para
        anchor_norm = re.sub(r"\s+", " ", anchor.lower()).strip()

        # Look for the best-matching SRT sentence ahead of `cursor`. Cap the
        # search window so we don't drift past the rough proportional location.
        proportional_end = cursor + max(1, round(md_counts[i] * total_srt / total_md))
        search_end = min(len(srt_sentences), proportional_end + max(3, md_counts[i]))

        best_idx, best_ratio = -1, 0.5  # require at least 50% similarity
        for j in range(cursor, search_end):
            candidate = re.sub(r"\s+", " ", srt_sentences[j].lower()).strip()
            ratio = difflib.SequenceMatcher(None, anchor_norm, candidate).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_idx = j

        if best_idx >= 0:
            chunk = srt_sentences[cursor : best_idx + 1]
            cursor = best_idx + 1
        else:
            # Proportional fallback
            take = max(1, round(md_counts[i] * total_srt / total_md))
            chunk = srt_sentences[cursor : cursor + take]
            cursor += len(chunk)

        new_paragraphs.append(" ".join(chunk).strip())

    return [p for p in new_paragraphs if p]


def extract_md_paragraphs(md_path: Path) -> list[str]:
    """Extract paragraphs from the body of a -video.md (everything after the H1).
    Paragraphs are blank-line-separated blocks; multi-line paragraphs are joined."""
    text = md_path.read_text(encoding="utf-8")
    m = re.match(r"^(---\n.*?\n---\n\n)(#\s+[^\n]+\n)", text, re.DOTALL)
    body = text[m.end():] if m else text
    paragraphs = []
    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if not block:
            continue
        # Collapse newlines within a paragraph
        paragraphs.append(re.sub(r"\s+", " ", block))
    return paragraphs


# ── Slug matching ───────────────────────────────────────────────────────────


def slugify(text: str) -> str:
    """Canvas-compatible slug. Mirrors push_to_canvas.slugify but standalone."""
    s = text.strip().lower()
    s = s.replace("#", " number ").replace("&", " and ")
    # Drop apostrophes (straight and curly)
    s = re.sub(r"['‘’ʼ]", "", s)
    # Strip common SRT filename punctuation that doesn't belong in slugs
    s = s.replace("_", " ")
    # Replace non-alphanumeric with hyphens, collapse
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def srt_slug(srt_path: Path) -> str:
    """`why-this-course-is-different-captions.srt` → `why-this-course-is-different`.
    Handles a few filename quirks (trailing `-captions`, `_-` artifacts, etc.)."""
    name = srt_path.stem  # without `.srt`
    # Strip `-captions` if present
    if name.endswith("-captions"):
        name = name[: -len("-captions")]
    # Clean up `_-` and similar punctuation artifacts
    name = name.replace("_-", "-").replace("_", " ")
    # Strip quoted-segment underscores that produced `_x_` markers
    name = re.sub(r"\s+", "-", name)
    return slugify(name)


def video_md_h1_slug(md_path: Path) -> str | None:
    """Extract the slug from a -video.md's H1: `# Video Script: Why this course is different`."""
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(?:Video Script|Audio Script):\s+(.+)$", text, re.MULTILINE)
    if not m:
        return None
    return slugify(m.group(1).strip())


# ── Markdown body replacement ───────────────────────────────────────────────


def replace_md_body(md_path: Path, paragraphs: list[str]) -> None:
    """Preserve frontmatter and the first H1. Replace everything after the H1 with
    the new paragraphs joined by blank lines."""
    text = md_path.read_text(encoding="utf-8")
    # Match frontmatter (--- block) + H1, keep them
    m = re.match(
        r"^(---\n.*?\n---\n\n)(#\s+[^\n]+\n)",
        text,
        re.DOTALL,
    )
    if not m:
        raise ValueError(f"Could not find frontmatter+H1 in {md_path}")
    head = m.group(1) + m.group(2)
    body = "\n" + "\n\n".join(paragraphs) + "\n"
    md_path.write_text(head + body, encoding="utf-8")


# ── Canvas HTML surgical replacement ────────────────────────────────────────


# Match the entire Video Transcript <details> block. We rely on its distinctive
# `<summary>` containing `Video Transcript`. Non-greedy match to the closest </details>.
TRANSCRIPT_BLOCK = re.compile(
    r"(<details[^>]*>\s*<summary[^>]*><strong>Video Transcript</strong>:\s*([^<]+)</summary>\s*<div[^>]*>)(.*?)(</div>\s*</details>)",
    re.DOTALL,
)


def update_canvas_html(html_path: Path, expected_slug: str, paragraphs: list[str]) -> bool:
    """Find a Video Transcript <details> block in the .canvas.html whose summary
    title slugifies to `expected_slug`, and replace the inner paragraphs.

    Preserves the wrapper <details>/<summary>/<div> shells and everything else in
    the HTML (including the video iframe that sits before the <details>).

    Returns True if a match was found and replaced, False otherwise.
    """
    if not html_path.exists():
        return False
    html = html_path.read_text(encoding="utf-8")

    def replacer(m):
        wrapper_open, title, _old_body, wrapper_close = (
            m.group(1),
            m.group(2),
            m.group(3),
            m.group(4),
        )
        title_slug = slugify(title.strip())
        # Accept exact match OR SRT slug as prefix of Canvas title slug.
        # Canvas titles often have a subtitle appended via em-dash
        # (e.g., SRT "why-reflective-practice-matters" matches Canvas
        # title slug "why-reflective-practice-matters-in-professional-work").
        if title_slug != expected_slug and not title_slug.startswith(expected_slug + "-"):
            return m.group(0)  # not our transcript; leave alone
        # Build new body — each paragraph as a <p>, last one with margin: 0;
        body_parts = []
        for idx, p in enumerate(paragraphs):
            last = idx == len(paragraphs) - 1
            mb = "0" if last else "12px"
            body_parts.append(
                f'<p style="font-size: 14px; margin-bottom: {mb};">{_html_escape_text(p)}</p>'
            )
        new_body = "".join(body_parts)
        return wrapper_open + new_body + wrapper_close

    new_html, n = TRANSCRIPT_BLOCK.subn(replacer, html)
    if n == 0:
        return False
    if new_html != html:
        html_path.write_text(new_html, encoding="utf-8")
        return True
    return False


def _html_escape_text(text: str) -> str:
    """Minimal HTML escape for plain text body content. Preserves ASCII apostrophes
    and quotes — Canvas WYSIWYG renders them fine and matches existing transcripts."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _canvas_transcript_drift(html_path: Path, expected_slug: str, srt_normalized_text: str) -> bool:
    """Return True if the .canvas.html Video Transcript block (matched by slug) has
    text content that differs from the SRT-derived text (whitespace-normalized)."""
    html = html_path.read_text(encoding="utf-8")
    for m in TRANSCRIPT_BLOCK.finditer(html):
        title = m.group(2).strip()
        title_slug = slugify(title)
        if title_slug != expected_slug and not title_slug.startswith(expected_slug + "-"):
            continue
        body_html = m.group(3)
        # Strip tags to get plain text
        body_text = re.sub(r"<[^>]+>", " ", body_html)
        body_text = re.sub(r"&amp;", "&", body_text)
        body_text = re.sub(r"&lt;", "<", body_text)
        body_text = re.sub(r"&gt;", ">", body_text)
        body_normalized = re.sub(r"\s+", " ", body_text).strip()
        return body_normalized != srt_normalized_text
    # No matching transcript block found — nothing to update
    return False


# ── Mapping ─────────────────────────────────────────────────────────────────


def find_companion_md(srt_path: Path, week_dir: Path):
    """Find the -video.md (or -audio.md) corresponding to this SRT.

    Match strategy (first hit wins):
      1. Hardcoded OVERRIDE_MAP for cases where the produced video title diverged
         from the script's H1/[VIDEO:] placeholder.
      2. SRT slug exactly matches a `[VIDEO: Title]` slug in any of the week's
         page .md files; map to the page's -video.md.
      3. SRT slug exactly matches a -video.md or -audio.md H1 slug.
      4. SRT slug is a prefix of a [VIDEO:] slug (the SRT title is often a
         shorter version of the [VIDEO:] title which has an em-dash subtitle).
      5. SRT slug is a prefix of a -video.md H1 slug.
    """
    target = srt_slug(srt_path)

    # 1. Override
    if srt_path.name in OVERRIDE_MAP:
        p = Path(OVERRIDE_MAP[srt_path.name])
        if p.exists():
            return p

    # Build week-scoped indexes
    video_mds = list(week_dir.glob("page*-video.md")) + list(week_dir.glob("page*-audio.md"))
    h1_index = {video_md_h1_slug(m): m for m in video_mds if video_md_h1_slug(m)}

    # [VIDEO:] placeholder index: page.md → -video.md
    placeholder_index = {}  # slug → -video.md
    for page_md in week_dir.glob("page*.md"):
        if any(s in page_md.name for s in ("-video.md", "-audio.md", "-interactive.md", "-synthesia-script.md")):
            continue
        text = page_md.read_text(encoding="utf-8")
        for m in re.finditer(r"\[(?:VIDEO|AUDIO):\s*([^\]]+)\]", text):
            title_slug = slugify(m.group(1).strip())
            # Map to companion video/audio .md
            stem = page_md.stem  # e.g., page1-overview
            for suffix in ("-video.md", "-audio.md"):
                candidate = week_dir / f"{stem}{suffix}"
                if candidate.exists():
                    placeholder_index[title_slug] = candidate
                    break

    # 2. Exact [VIDEO:] match
    if target in placeholder_index:
        return placeholder_index[target]

    # 3. Exact H1 match
    if target in h1_index:
        return h1_index[target]

    # 4. Prefix match against [VIDEO:] slugs (SRT slug is shorter)
    for s, md in placeholder_index.items():
        if s.startswith(target + "-") or s == target:
            return md

    # 5. Prefix match against H1 slugs
    for s, md in h1_index.items():
        if s.startswith(target + "-") or s == target:
            return md

    return None


def find_page_md_for_video_md(video_md: Path) -> Path | None:
    """`page1-overview-video.md` → `page1-overview.md`. Used to locate the
    companion .canvas.html where the Video Transcript block lives."""
    name = video_md.name
    for suffix in ("-video.md", "-audio.md"):
        if name.endswith(suffix):
            base = name[: -len(suffix)] + ".md"
            return video_md.parent / base
    return None


# ── Pipeline ────────────────────────────────────────────────────────────────


def process_srt(srt_path: Path, report_only: bool) -> dict:
    """Process one SRT. Returns a summary dict."""
    result = {
        "srt": srt_path,
        "status": None,  # 'skipped' | 'no-match' | 'no-change' | 'updated' | 'updated-md-only'
        "video_md": None,
        "canvas_html": None,
        "paragraphs": 0,
    }

    if srt_path.name in SKIP_SRTS:
        result["status"] = "skipped"
        result["reason"] = "in SKIP_SRTS allowlist"
        return result

    week_dir = srt_path.parent.parent  # weekly_content/weekNN/Videos/ → weekly_content/weekNN/
    companion_md = find_companion_md(srt_path, week_dir)
    if not companion_md:
        result["status"] = "no-match"
        return result

    result["video_md"] = companion_md
    cues = parse_srt(srt_path)
    srt_text = " ".join(c[2] for c in cues)
    srt_text = re.sub(r"\s+", " ", srt_text).strip()
    srt_text = fix_missing_periods(srt_text)

    # Compute current body to see if anything actually changed
    current = companion_md.read_text(encoding="utf-8")
    head_match = re.match(
        r"^(---\n.*?\n---\n\n)(#\s+[^\n]+\n)",
        current,
        re.DOTALL,
    )
    if not head_match:
        result["status"] = "no-match"
        result["reason"] = "missing frontmatter+H1"
        return result
    current_body = current[head_match.end() :].strip()

    # Align SRT text to the existing .md paragraph structure. This preserves
    # hand-tuned paragraph breaks while substituting canonical SRT content into
    # each paragraph.
    existing_paragraphs = extract_md_paragraphs(companion_md)
    if existing_paragraphs:
        paragraphs = align_paragraphs(srt_text, existing_paragraphs)
    else:
        # New file or no body — fall back to timing-gap-based paragraphing
        paragraphs = cues_to_paragraphs(cues)
    result["paragraphs"] = len(paragraphs)

    # Normalize whitespace for text-equivalence check. If the SRT-derived text
    # matches the current .md text (ignoring paragraph structure), preserve the
    # existing hand-tuned paragraph breaks — don't rewrite for purely structural
    # differences. Only update when the SRT introduces actual word-level drift.
    current_normalized = re.sub(r"\s+", " ", current_body).strip()
    new_normalized = re.sub(r"\s+", " ", " ".join(paragraphs)).strip()
    md_unchanged = current_normalized == new_normalized

    # .canvas.html companion
    page_md = find_page_md_for_video_md(companion_md)
    canvas_html_path = (
        page_md.with_suffix(".canvas.html") if page_md else None
    )

    # Check whether the .canvas.html transcript also matches SRT text. If yes,
    # nothing to do on the HTML side either.
    html_drift = canvas_html_path and canvas_html_path.exists() and _canvas_transcript_drift(
        canvas_html_path, srt_slug(srt_path), new_normalized
    )

    if report_only:
        if md_unchanged and not html_drift:
            result["status"] = "no-change"
        else:
            result["status"] = "would-update"
        result["canvas_html"] = canvas_html_path
        return result

    md_changed = False
    if not md_unchanged:
        replace_md_body(companion_md, paragraphs)
        md_changed = True

    html_changed = False
    if html_drift:
        html_changed = update_canvas_html(
            canvas_html_path, srt_slug(srt_path), paragraphs
        )

    if md_changed and html_changed:
        result["status"] = "updated"
    elif md_changed:
        result["status"] = "updated-md-only"
    elif html_changed:
        result["status"] = "updated-html-only"
    else:
        result["status"] = "no-change"
    result["canvas_html"] = canvas_html_path
    return result


# ── CLI ────────────────────────────────────────────────────────────────────


def gather_srts(args) -> list[Path]:
    """Collect SRTs based on CLI flags."""
    if args.input:
        return [Path(args.input)]
    if args.week is not None:
        week_dir = Path(f"weekly_content/week{args.week:02d}")
        return sorted((week_dir / "Videos").glob("*.srt"))
    if args.all:
        srts = []
        for week_dir in sorted(Path("weekly_content").glob("week*")):
            srts.extend(sorted((week_dir / "Videos").glob("*.srt")))
        return srts
    return []


def main():
    parser = argparse.ArgumentParser(
        description="Update -video.md transcripts and .canvas.html Video Transcript blocks from SRT captions"
    )
    parser.add_argument("input", nargs="?", help="Path to a single SRT file")
    parser.add_argument("--week", type=int, help="Process all SRTs in weekly_content/weekNN/Videos/")
    parser.add_argument("--all", action="store_true", help="Process every week's SRTs")
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Don't write files; show what would change",
    )
    args = parser.parse_args()

    srts = gather_srts(args)
    if not srts:
        parser.print_help()
        sys.exit(1)

    mode = "REPORT-ONLY" if args.report_only else "UPDATE"
    print(f"Processing {len(srts)} SRT file(s) [{mode}]\n")

    results = []
    for srt in srts:
        r = process_srt(srt, args.report_only)
        results.append(r)
        status = r["status"]
        if status == "skipped":
            print(f"  [SKIP]   {srt.name}  ({r.get('reason', '')})")
        elif status == "no-match":
            reason = r.get("reason", "no -video.md/-audio.md matches this slug")
            print(f"  [NOMATCH] {srt.name}  ({reason})")
        elif status == "no-change":
            print(f"  [OK]     {srt.name}  → {r['video_md'].name} (no drift)")
        elif status == "would-update":
            print(f"  [DRIFT]  {srt.name}  → {r['video_md'].name} ({r['paragraphs']} paragraphs)")
        elif status == "updated":
            print(f"  [WROTE]  {srt.name}  → {r['video_md'].name} + .canvas.html")
        elif status == "updated-md-only":
            print(f"  [WROTE]  {srt.name}  → {r['video_md'].name} (no canvas.html change)")
        elif status == "updated-html-only":
            print(f"  [WROTE]  {srt.name}  → .canvas.html only (.md was already in sync)")

    # Summary
    by_status = {}
    for r in results:
        by_status.setdefault(r["status"], 0)
        by_status[r["status"]] += 1
    print("\n" + "=" * 60)
    print(f"Summary: {dict(by_status)}")


if __name__ == "__main__":
    main()
