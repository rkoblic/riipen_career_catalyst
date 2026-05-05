#!/usr/bin/env python3
"""
Convert a Career Catalyst markdown content page into Canvas-compatible HTML.

The output uses inline styles only (Canvas strips style blocks and stylesheets),
no JavaScript, no YouTube iframes — see guides/canvas-html-guide.md for the
constraints and the component library this implements.

Usage:
    python3 scripts/md_to_canvas_html.py <input.md> [<output.html>]
    python3 scripts/md_to_canvas_html.py --week 6
    python3 scripts/md_to_canvas_html.py --week 6 --stdout

Examples:
    python3 scripts/md_to_canvas_html.py weekly_content/week06/page1-overview.md
    # writes weekly_content/week06/page1-overview.canvas.html

    python3 scripts/md_to_canvas_html.py --week 6
    # writes .canvas.html for every page in week06/
"""

import argparse
import html
import re
import sys
from pathlib import Path


# ── Frontmatter ──────────────────────────────────────────────────────────────


def split_frontmatter(text):
    """Return (frontmatter_dict, body_text). Frontmatter is parsed as a tiny
    subset of YAML: top-level scalars and a single-level array of objects under
    `competencies:`."""
    meta = {}
    body = text.strip()
    if not body.startswith("---"):
        return meta, body
    end = body.find("\n---", 3)
    if end == -1:
        return meta, body
    block = body[3:end].strip()
    body = body[end + 4:].lstrip("\n")

    # Parse line by line. Track competencies as a list of dicts.
    competencies = []
    current_comp = None
    for raw_line in block.split("\n"):
        line = raw_line.rstrip()
        if not line.strip():
            continue
        # Competency list items
        m = re.match(r"^\s*-\s+area\s*:\s*(.+)$", line)
        if m:
            current_comp = {"area": m.group(1).strip().strip('"').strip("'")}
            competencies.append(current_comp)
            continue
        m = re.match(r"^\s+subskill\s*:\s*(.+)$", line)
        if m and current_comp is not None:
            current_comp["subskill"] = m.group(1).strip().strip('"').strip("'")
            continue
        # Top-level key:value
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key == "competencies":
                # The list items are parsed below
                continue
            meta[key] = val

    if competencies:
        meta["competencies"] = competencies
    return meta, body


# ── Inline markdown → HTML ───────────────────────────────────────────────────


_INLINE_PATTERN = re.compile(
    r"\*\*\*(.+?)\*\*\*"          # ***bold italic***
    r"|\*\*(.+?)\*\*"              # **bold**
    r"|\*(.+?)\*"                  # *italic*
    r"|`([^`]+)`"                  # `code`
    r"|\[([^\]]+)\]\(([^)]+)\)"    # [text](url)
)

LINK_STYLE = "color: #2454ff;"


def _esc(text):
    """Escape only `<`, `>`, `&` — leave quotes/apostrophes literal so the HTML
    is readable when Rachel inspects it in Canvas's HTML editor view."""
    return html.escape(text, quote=False)


def render_inline(text):
    """Render markdown inline formatting as HTML. Escapes structural chars only."""
    out = []
    pos = 0
    for m in _INLINE_PATTERN.finditer(text):
        if m.start() > pos:
            out.append(_esc(text[pos:m.start()]))
        if m.group(1) is not None:
            out.append(f"<strong><em>{_esc(m.group(1))}</em></strong>")
        elif m.group(2) is not None:
            out.append(f"<strong>{_esc(m.group(2))}</strong>")
        elif m.group(3) is not None:
            out.append(f"<em>{_esc(m.group(3))}</em>")
        elif m.group(4) is not None:
            out.append(
                f'<code style="background: #f7f8fa; padding: 1px 4px; border-radius: 3px; font-size: 13px;">'
                f'{_esc(m.group(4))}</code>'
            )
        elif m.group(5) is not None:
            # Recursively render inline markdown inside link text so patterns
            # like [**bold**](url) or [_italic_](url) work.
            link_text = render_inline(m.group(5))
            link_url = html.escape(m.group(6), quote=True)
            out.append(
                f'<a style="{LINK_STYLE}" href="{link_url}" '
                f'target="_blank" rel="noopener">{link_text}</a>'
            )
        pos = m.end()
    if pos < len(text):
        out.append(_esc(text[pos:]))
    return "".join(out)


# ── Callout heuristics ───────────────────────────────────────────────────────


# Map normalized cue (lowercase) → (component_kind, label_text_to_render)
CALLOUT_CUES = {
    "important": ("key_principle", "IMPORTANT"),
    "key principle": ("key_principle", "KEY PRINCIPLE"),
    "remember": ("key_principle", "REMEMBER"),
    "rule": ("key_principle", "RULE"),

    "tip": ("info", "TIP"),
    "note": ("info", "NOTE"),
    "heads up": ("info", "HEADS UP"),
    "agenda": ("info", "AGENDA"),
    "suggested agenda": ("info", "SUGGESTED AGENDA"),
    "timeline": ("info", "TIMELINE"),

    "ai use": ("ai", "AI USE"),
    "ai guidance": ("ai", "AI GUIDANCE"),
    "using ai": ("ai", "AI USE"),

    "scenario": ("scenario", "SCENARIO EXAMPLE"),
    "example": ("scenario", "EXAMPLE"),
    "what this looks like": ("scenario", "WHAT THIS LOOKS LIKE"),
    "in practice": ("scenario", "IN PRACTICE"),
}

# Match a paragraph that starts with **Label.** or **Label:** followed by content.
_CALLOUT_PREFIX = re.compile(r"^\*\*([^*]+?)[\.:]\*\*\s+(.+)$", re.DOTALL)


def detect_callout(paragraph_text):
    """If the paragraph matches a known callout cue, return
    (component_kind, label_text, body_text). Otherwise return None."""
    m = _CALLOUT_PREFIX.match(paragraph_text.strip())
    if not m:
        return None
    label_raw = m.group(1).strip().lower()
    body = m.group(2).strip()
    cue = CALLOUT_CUES.get(label_raw)
    if not cue:
        return None
    component_kind, label_display = cue
    return component_kind, label_display, body


# ── Component renderers ──────────────────────────────────────────────────────


PAGE_WRAPPER_OPEN = (
    '<div style="font-family: \'DM Sans\', -apple-system, BlinkMacSystemFont, '
    "'Segoe UI', Roboto, sans-serif; color: #050c2a; line-height: 1.7; "
    'max-width: 800px;">'
)
PAGE_WRAPPER_CLOSE = "</div>"


def render_intro_paragraph(text):
    return f'<p style="font-size: 15px; margin-bottom: 16px;">{render_inline(text)}</p>'


def render_competency_badges(competencies):
    if not competencies:
        return ""
    spans = []
    for c in competencies:
        area = _esc(c.get("area", ""))
        sub = _esc(c.get("subskill", ""))
        label = f"{area}: {sub}" if sub else area
        spans.append(
            '<span style="display: inline-block; background: #f7f8fa; '
            'border: 1px solid #e2e4e9; border-radius: 12px; padding: 3px 10px; '
            f'font-size: 11px; color: #050c2a;">{label}</span>'
        )
    return (
        '<p style="font-size: 12px; color: #6b7280; margin: 0 0 6px;"><strong>SKILLS YOU\'LL PRACTICE</strong></p>'
        '<div style="margin: 0 0 20px; display: flex; flex-wrap: wrap; gap: 6px;">'
        + "".join(spans)
        + "</div>"
    )


def render_section_header(title):
    return (
        '<div style="background: #ff7c0a; padding: 12px 18px; '
        'border-radius: 8px 8px 0 0; margin-top: 28px;">'
        f'<h2 style="font-size: 16px; color: #050c2a; margin: 0;">'
        f"<strong>{render_inline(title)}</strong></h2></div>"
    )


def render_section_body_open():
    return (
        '<div style="border: 1px solid #e2e4e9; border-top: none; '
        'border-radius: 0 0 8px 8px; padding: 20px 24px; margin-bottom: 24px;">'
    )


SECTION_BODY_CLOSE = "</div>"


def render_h3(title, first_in_section=False):
    margin = "0 0 8px" if first_in_section else "24px 0 8px"
    return (
        f'<h3 style="font-size: 16px; color: #050c2a; margin: {margin};">'
        f"<strong>{render_inline(title)}</strong></h3>"
    )


def render_paragraph(text):
    return f'<p style="font-size: 14px; margin-bottom: 12px;">{render_inline(text)}</p>'


def render_bullet_list(items):
    parts = ['<ul style="font-size: 14px; margin: 0 0 16px 20px;">']
    for item in items:
        parts.append(f'<li style="margin-bottom: 6px;">{render_inline(item)}</li>')
    parts.append("</ul>")
    return "".join(parts)


def render_numbered_list(items):
    parts = ['<ol style="font-size: 14px; margin: 0 0 16px 20px;">']
    for item in items:
        parts.append(f'<li style="margin-bottom: 6px;">{render_inline(item)}</li>')
    parts.append("</ol>")
    return "".join(parts)


def render_checklist(title, items):
    """Render checklist items as a flat sequence of paragraphs with checkbox
    characters. No outer wrapper box — section body already provides the
    container, and a box-within-a-box is visually redundant."""
    parts = []
    if title:
        parts.append(
            f'<p style="font-size: 14px; margin-bottom: 10px;">'
            f"<strong>{render_inline(title)}</strong></p>"
        )
    for item in items:
        parts.append(
            f'<p style="font-size: 14px; margin-bottom: 6px;">'
            f'<span aria-hidden="true">&#9744; </span>{render_inline(item)}</p>'
        )
    return "".join(parts)


def render_callout(kind, label, body):
    """kind is one of: key_principle, info, ai, scenario.

    Labels are wrapped in <strong> because Canvas strips font-weight from
    inline styles — without <strong>, the label loses contrast against the
    callout background.
    """
    if kind == "key_principle":
        return (
            '<div style="background: #fff8f1; border-left: 4px solid #ff7c0a; '
            'padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 16px 0;">'
            f'<div style="font-size: 12px; margin-bottom: 6px; color: #b54708;">'
            f"<strong>{_esc(label)}</strong></div>"
            f'<p style="font-size: 14px; margin: 0;">{render_inline(body)}</p></div>'
        )
    if kind == "info":
        return (
            '<div style="background: #f7f8fa; border-left: 4px solid #2454ff; '
            'padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 16px 0;">'
            f'<div style="font-size: 12px; margin-bottom: 6px; color: #2454ff;">'
            f"<strong>{_esc(label)}</strong></div>"
            f'<p style="font-size: 14px; margin: 0;">{render_inline(body)}</p></div>'
        )
    if kind == "ai":
        return (
            '<div style="background: #050c2a; color: white; border-radius: 8px; '
            'padding: 16px 20px; margin: 16px 0;">'
            f'<div style="font-size: 12px; margin-bottom: 6px;">'
            f"<strong>{_esc(label)}</strong></div>"
            f'<p style="font-size: 14px; margin: 0; color: white;">{render_inline(body)}</p></div>'
        )
    if kind == "scenario":
        return (
            '<div style="background: #f7f8fa; border: 2px dashed #7c3aed; '
            'border-radius: 10px; padding: 20px 24px; margin: 16px 0;">'
            f'<div style="font-size: 11px; color: #7c3aed; margin-bottom: 8px;">'
            f"<strong>{_esc(label)}</strong></div>"
            f'<p style="font-size: 14px; margin: 0;">{render_inline(body)}</p></div>'
        )
    raise ValueError(f"Unknown callout kind: {kind}")


def render_table(header_cells, body_rows):
    parts = [
        '<table style="border-collapse: collapse; width: 100%; '
        'margin: 16px 0; font-size: 14px;">',
        "<thead>",
        '<tr style="background: #f7f8fa;">',
    ]
    for cell in header_cells:
        parts.append(
            '<th style="border: 1px solid #e2e4e9; padding: 8px 12px; '
            f'text-align: left;"><strong>{render_inline(cell)}</strong></th>'
        )
    parts.append("</tr></thead><tbody>")
    for row in body_rows:
        parts.append("<tr>")
        for col_idx in range(len(header_cells)):
            cell = row[col_idx] if col_idx < len(row) else ""
            parts.append(
                '<td style="border: 1px solid #e2e4e9; padding: 8px 12px; '
                f'vertical-align: top;">{render_inline(cell)}</td>'
            )
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def render_video_placeholder(title):
    return (
        '<div style="background: #f7f8fa; border: 1px solid #e2e4e9; '
        'border-radius: 10px; padding: 24px; text-align: center; margin: 20px 0;">'
        f'<p style="font-size: 14px; color: #050c2a; margin-bottom: 4px;">'
        f'<span aria-hidden="true">&#127916; </span>Video: {_esc(title)}</p>'
        '<p style="font-size: 13px; color: #6b7280; margin: 0;">'
        "Video will be embedded here once produced.</p></div>"
    )


def render_video_transcript(title, transcript_paragraphs):
    if not transcript_paragraphs:
        return ""
    paragraph_html = []
    last_idx = len(transcript_paragraphs) - 1
    for idx, para in enumerate(transcript_paragraphs):
        margin = "0" if idx == last_idx else "12px"
        paragraph_html.append(
            f'<p style="font-size: 14px; margin-bottom: {margin};">'
            f"{render_inline(para)}</p>"
        )
    return (
        '<details style="border: 1px solid #e2e4e9; border-radius: 8px; '
        'margin: 0 0 20px; overflow: hidden;">'
        '<summary style="background: #f7f8fa; padding: 12px 18px; font-size: 14px; '
        'color: #050c2a; cursor: pointer;">'
        f"<strong>Video Transcript</strong>: {_esc(title)}</summary>"
        '<div style="padding: 16px 20px;">'
        + "".join(paragraph_html)
        + "</div></details>"
    )


def render_interactive_placeholder(title, description=""):
    return (
        '<div style="background: #f7f8fa; border: 2px dashed #7c3aed; '
        'border-radius: 10px; padding: 20px 24px; text-align: center; margin: 16px 0;">'
        f'<p style="font-size: 15px; margin-bottom: 4px;">'
        f'<span aria-hidden="true">&#127919; </span>Interactive: {_esc(title)}</p>'
        + (
            f'<p style="font-size: 13px; color: #6b7280; margin-bottom: 12px;">'
            f"{render_inline(description)}</p>"
            if description
            else ""
        )
        + '<p style="font-size: 14px; margin: 0;">'
        "Interactive will be embedded here once produced.</p></div>"
    )


# Curated link format: [CURATED LINK: "Title" (type, ~Xmin) — Source — URL] description
_CURATED_LINK = re.compile(
    r'^\[CURATED LINK:\s*"([^"]+)"\s*\(([^)]+)\)\s*[—–-]\s*([^—–\-]+?)\s*[—–-]\s*(\S+?)\]\s*(.*)$'
)


def render_curated_link(title, meta, source, url, description):
    bits = [meta.strip()] if meta.strip() else []
    if source.strip():
        bits.append(source.strip())
    sub = " · ".join(bits)
    return (
        f'<p style="font-size: 14px; margin-bottom: 12px;">'
        f'<span aria-hidden="true">&#128206; </span>'
        f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener" '
        f'style="{LINK_STYLE}">{_esc(title)}</a>'
        + (f' — <span style="color: #6b7280;">{_esc(sub)}</span>' if sub else "")
        + (f". {render_inline(description)}" if description else "")
        + "</p>"
    )


def render_curated_link_simple(body):
    """Fallback for [CURATED LINK: ...] entries that don't match the structured format."""
    return (
        f'<p style="font-size: 14px; margin-bottom: 12px;">'
        f'<span aria-hidden="true">&#128206; </span>{render_inline(body)}</p>'
    )


def render_template_box(description):
    return (
        '<div style="background: white; border: 1px solid #e2e4e9; '
        'border-radius: 10px; padding: 18px 22px; margin: 12px 0 20px;">'
        f'<div style="font-size: 12px; color: #6b7280; margin-bottom: 8px;"><strong>TEMPLATE</strong></div>'
        f'<p style="font-size: 14px; margin: 0;">{render_inline(description)}</p></div>'
    )


def render_linked_resource(description):
    return (
        '<div style="background: #f7f8fa; border: 1px solid #e2e4e9; '
        'border-radius: 8px; padding: 14px 18px; margin: 12px 0;">'
        '<div style="font-size: 12px; color: #6b7280; margin-bottom: 4px;"><strong>LINKED RESOURCE</strong></div>'
        f'<p style="font-size: 14px; margin: 0;">{render_inline(description)}</p></div>'
    )


# ── Block parser ─────────────────────────────────────────────────────────────


def _is_table_separator(line):
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return False
    middle = s.replace("|", "").replace(":", "").replace(" ", "")
    return bool(middle) and set(middle) <= {"-"}


def _next_nonblank(lines, idx, predicate):
    """Look past blank lines starting at idx; return True if the next non-blank
    line satisfies the predicate. Used to keep list blocks together when items
    are separated by blank lines."""
    j = idx
    while j < len(lines):
        s = lines[j].strip()
        if not s:
            j += 1
            continue
        return predicate(s)
    return False


def _normalize_dashes(text):
    """The curated link regex uses em/en dashes — input may use any of them."""
    return text


def parse_video_transcript(video_md):
    """Strip frontmatter and H1 from a video script, return list of paragraph
    strings for the transcript expand/collapse component."""
    _, body = split_frontmatter(video_md)
    paragraphs = []
    current = []
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith("# "):
            continue  # skip H1
        if s in ("---", "***", "___"):
            continue
        if not s:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        # Skip blockquoted lines (rare in scripts, but if used as direction notes)
        if s.startswith("> "):
            continue
        current.append(s)
    if current:
        paragraphs.append(" ".join(current))
    return paragraphs


def find_video_script(input_path):
    """Look for a sibling -video.md file matching the page (e.g.,
    page1-overview.md → page1-overview-video.md). Return its content or None."""
    parent = input_path.parent
    stem = input_path.stem
    candidate = parent / f"{stem}-video.md"
    if candidate.exists():
        return candidate.read_text(encoding="utf-8")
    return None


def convert_body_to_html(body, video_md_lookup=None):
    """Walk the markdown body line by line and emit HTML blocks.

    video_md_lookup: callable(video_title) -> raw video script markdown, or None.
    Used to inline transcripts under [VIDEO:] placeholders.
    """
    lines = body.split("\n")
    out = []  # list of HTML strings
    section_open = False  # tracks whether we're inside a section body wrapper
    h3_just_after_section_open = False
    saw_first_paragraph = False  # first non-empty paragraph after H1 = intro
    intro_emitted = False
    seen_h1 = False

    def close_section():
        nonlocal section_open
        if section_open:
            out.append(SECTION_BODY_CLOSE)
            section_open = False

    def open_section(title):
        nonlocal section_open, h3_just_after_section_open
        close_section()
        out.append(render_section_header(title))
        out.append(render_section_body_open())
        section_open = True
        h3_just_after_section_open = True

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue
        if stripped in ("---", "***", "___"):
            i += 1
            continue

        # H1 — page title (skip; the page title goes in the Canvas page title field, not the body)
        if stripped.startswith("# ") and not stripped.startswith("## "):
            seen_h1 = True
            i += 1
            continue

        # H2 — open a new section
        if stripped.startswith("## "):
            title = stripped[3:].strip()
            open_section(title)
            i += 1
            continue

        # H3 — subsection
        if stripped.startswith("### "):
            title = stripped[4:].strip()
            out.append(render_h3(title, first_in_section=h3_just_after_section_open))
            h3_just_after_section_open = False
            i += 1
            continue

        # Markdown table
        if stripped.startswith("|") and stripped.endswith("|") and i + 1 < len(lines):
            if _is_table_separator(lines[i + 1]):
                header_cells = [c.strip() for c in stripped.strip("|").split("|")]
                i += 2  # skip header and separator
                body_rows = []
                while i < len(lines):
                    row = lines[i].strip()
                    if not (row.startswith("|") and row.endswith("|")):
                        break
                    body_rows.append([c.strip() for c in row.strip("|").split("|")])
                    i += 1
                out.append(render_table(header_cells, body_rows))
                h3_just_after_section_open = False
                continue

        # Checkbox list → checklist box (handles blank lines between items)
        if stripped.startswith("- [ ] ") or stripped.startswith("- [x] "):
            items = []
            while i < len(lines):
                s = lines[i].strip()
                if s.startswith("- [ ] ") or s.startswith("- [x] "):
                    items.append(s[6:].strip())
                    i += 1
                elif not s and _next_nonblank(lines, i, lambda x: x.startswith("- [ ] ") or x.startswith("- [x] ")):
                    i += 1
                else:
                    break
            out.append(render_checklist(title="", items=items))
            h3_just_after_section_open = False
            continue

        # Unordered list (handles blank lines between items)
        if stripped.startswith("- ") or stripped.startswith("* "):
            items = []
            while i < len(lines):
                s = lines[i].strip()
                if s.startswith("- ") or s.startswith("* "):
                    items.append(s[2:].strip())
                    i += 1
                elif not s and _next_nonblank(lines, i, lambda x: x.startswith("- ") or x.startswith("* ")):
                    i += 1
                else:
                    break
            out.append(render_bullet_list(items))
            h3_just_after_section_open = False
            continue

        # Ordered list (handles blank lines between items)
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(lines):
                s = lines[i].strip()
                m = re.match(r"^\d+\.\s+(.+)", s)
                if m:
                    items.append(m.group(1).strip())
                    i += 1
                elif not s and _next_nonblank(lines, i, lambda x: bool(re.match(r"^\d+\.\s+", x))):
                    i += 1
                else:
                    break
            out.append(render_numbered_list(items))
            h3_just_after_section_open = False
            continue

        # VIDEO placeholder
        if stripped.startswith("[VIDEO:"):
            title = stripped[len("[VIDEO:"):].rstrip("]").strip()
            out.append(render_video_placeholder(title))
            if video_md_lookup is not None:
                video_md = video_md_lookup(title)
                if video_md:
                    transcript = parse_video_transcript(video_md)
                    out.append(render_video_transcript(title, transcript))
            h3_just_after_section_open = False
            i += 1
            continue

        # AUDIO placeholder — render as a video-style placeholder for now
        if stripped.startswith("[AUDIO:"):
            title = stripped[len("[AUDIO:"):].rstrip("]").strip()
            out.append(
                '<div style="background: #f7f8fa; border: 1px solid #e2e4e9; '
                'border-radius: 10px; padding: 24px; text-align: center; margin: 20px 0;">'
                f'<p style="font-size: 14px; color: #050c2a; margin-bottom: 4px;">'
                f'<span aria-hidden="true">&#127911; </span>Audio: {_esc(title)}</p>'
                '<p style="font-size: 13px; color: #6b7280; margin: 0;">'
                "Audio will be embedded here once produced.</p></div>"
            )
            h3_just_after_section_open = False
            i += 1
            continue

        # INTERACTIVE placeholder
        if stripped.startswith("[INTERACTIVE:"):
            body_text = stripped[len("[INTERACTIVE:"):].rstrip("]").strip()
            # Some entries include a description; use the first chunk before a colon
            # as the title if a colon is present, otherwise the whole thing.
            if ":" in body_text:
                title, _, desc = body_text.partition(":")
                out.append(render_interactive_placeholder(title.strip(), desc.strip()))
            else:
                out.append(render_interactive_placeholder(body_text))
            h3_just_after_section_open = False
            i += 1
            continue

        # CURATED LINK — single-line block
        if stripped.startswith("[CURATED LINK:"):
            m = _CURATED_LINK.match(stripped)
            if m:
                out.append(render_curated_link(*m.groups()))
            else:
                # Fall back to rendering the raw block as a paragraph
                out.append(render_curated_link_simple(stripped[1:-1] if stripped.endswith("]") else stripped))
            h3_just_after_section_open = False
            i += 1
            continue

        # TEMPLATE placeholder
        if stripped.startswith("[TEMPLATE:"):
            body_text = stripped[len("[TEMPLATE:"):].rstrip("]").strip()
            out.append(render_template_box(body_text))
            h3_just_after_section_open = False
            i += 1
            continue

        # LINKED RESOURCE placeholder
        if stripped.startswith("[LINKED RESOURCE:"):
            body_text = stripped[len("[LINKED RESOURCE:"):].rstrip("]").strip()
            out.append(render_linked_resource(body_text))
            h3_just_after_section_open = False
            i += 1
            continue

        # Blockquote — admonition escape hatch first, fallback to plain quote
        if stripped.startswith("> "):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                qline = lines[i].strip()
                quote_lines.append(qline[2:] if qline.startswith("> ") else qline[1:])
                i += 1
            # Admonition: first line is `[!kind] OPTIONAL LABEL`, body follows
            adm = re.match(r"^\[!(key|info|ai|scenario)\](?:\s+(.+))?$", quote_lines[0].strip())
            if adm:
                kind_short = adm.group(1)
                label_override = (adm.group(2) or "").strip()
                kind_map = {
                    "key": ("key_principle", label_override or "KEY PRINCIPLE"),
                    "info": ("info", label_override or "NOTE"),
                    "ai": ("ai", label_override or "AI USE"),
                    "scenario": ("scenario", label_override or "SCENARIO EXAMPLE"),
                }
                kind, label = kind_map[kind_short]
                body_text = " ".join(q.strip() for q in quote_lines[1:] if q.strip())
                out.append(render_callout(kind, label, body_text))
                h3_just_after_section_open = False
                continue
            quote_text = " ".join(q for q in quote_lines if q.strip())
            out.append(
                '<blockquote style="border-left: 3px solid #e2e4e9; '
                'margin: 16px 0; padding: 4px 0 4px 16px; color: #6b7280; '
                f'font-size: 14px;">{render_inline(quote_text)}</blockquote>'
            )
            h3_just_after_section_open = False
            continue

        # Paragraph — could be intro, callout, or plain
        # Collect consecutive non-empty lines that aren't a structural marker into one paragraph
        para_lines = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt:
                break
            if (
                nxt.startswith("# ")
                or nxt.startswith("## ")
                or nxt.startswith("### ")
                or nxt.startswith("- ")
                or nxt.startswith("* ")
                or re.match(r"^\d+\.\s+", nxt)
                or nxt.startswith("> ")
                or nxt.startswith("|")
                or nxt.startswith("[VIDEO:")
                or nxt.startswith("[AUDIO:")
                or nxt.startswith("[INTERACTIVE:")
                or nxt.startswith("[CURATED LINK:")
                or nxt.startswith("[TEMPLATE:")
                or nxt.startswith("[LINKED RESOURCE:")
                or nxt in ("---", "***", "___")
            ):
                break
            para_lines.append(nxt)
            i += 1
        paragraph_text = " ".join(para_lines)

        # Intro paragraph: first paragraph after H1, before first H2
        if seen_h1 and not intro_emitted and not section_open:
            out.append(render_intro_paragraph(paragraph_text))
            intro_emitted = True
            saw_first_paragraph = True
            continue

        # Callout heuristic
        callout = detect_callout(paragraph_text)
        if callout:
            kind, label, body_text = callout
            out.append(render_callout(kind, label, body_text))
            h3_just_after_section_open = False
            continue

        out.append(render_paragraph(paragraph_text))
        h3_just_after_section_open = False

    close_section()
    return "\n".join(out)


# ── Top-level convert ───────────────────────────────────────────────────────


def convert_file(input_path):
    """Read a markdown page, return (frontmatter, html_body)."""
    raw = Path(input_path).read_text(encoding="utf-8")
    meta, body = split_frontmatter(raw)
    badges_html = render_competency_badges(meta.get("competencies"))

    body_html = convert_body_to_html(body, video_md_lookup=lambda _t: find_video_script(Path(input_path)))
    # Competency badges go at the very top of the page, before the intro paragraph.
    if badges_html:
        body_html = badges_html + "\n" + body_html

    full_html = PAGE_WRAPPER_OPEN + "\n" + body_html + "\n" + PAGE_WRAPPER_CLOSE
    return meta, full_html


# ── CLI ─────────────────────────────────────────────────────────────────────


def output_path_for(input_path: Path) -> Path:
    return input_path.with_suffix(".canvas.html")


def collect_week_pages(week_num: int):
    week_dir = Path(f"weekly_content/week{week_num:02d}")
    if not week_dir.exists():
        print(f"Error: {week_dir} does not exist.", file=sys.stderr)
        sys.exit(1)
    def page_sort_key(p):
        m = re.match(r"page(\d+)", p.name)
        return (int(m.group(1)) if m else 9999, p.name)
    pages = sorted(week_dir.glob("page*.md"), key=page_sort_key)
    return [
        f for f in pages
        if "-video.md" not in f.name
        and "-audio.md" not in f.name
        and "-interactive.md" not in f.name
    ]


def main():
    parser = argparse.ArgumentParser(description="Convert markdown content pages to Canvas HTML")
    parser.add_argument("input", nargs="?", help="Input .md file")
    parser.add_argument("output", nargs="?", help="Output .html file (default: alongside input as .canvas.html)")
    parser.add_argument("--week", type=int, help="Convert all content pages in weekly_content/weekNN/")
    parser.add_argument("--stdout", action="store_true", help="Print HTML to stdout instead of writing to file")
    args = parser.parse_args()

    if args.week is not None:
        pages = collect_week_pages(args.week)
        if not pages:
            print(f"No pages found for week {args.week}", file=sys.stderr)
            sys.exit(1)
        for p in pages:
            _meta, html_out = convert_file(p)
            out_path = output_path_for(p)
            out_path.write_text(html_out, encoding="utf-8")
            print(f"Wrote: {out_path}")
        return

    if not args.input:
        parser.print_help()
        sys.exit(1)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    _meta, html_out = convert_file(input_path)
    if args.stdout:
        print(html_out)
        return

    out_path = Path(args.output) if args.output else output_path_for(input_path)
    out_path.write_text(html_out, encoding="utf-8")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
