#!/usr/bin/env python3
"""
objectives_matrix.py

Three-level competency coverage matrix (Taught / Practiced / Assessed).

Reads:
  - learning-objectives-review.md  → T (Taught) mappings
  - Activity Breakdown CSV          → P (Practiced) mappings via rule-based classification
  - Hardcoded assessment map        → A (Assessed) mappings

Outputs:
  - competency-matrix.html          → interactive branded dashboard
"""

import csv
import re
import os
from pathlib import Path
from collections import defaultdict
from glob import glob as _glob

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_MD = PROJECT_ROOT / "learning-objectives-review.md"
OUTPUT_FILE = PROJECT_ROOT / "competency-matrix.html"

# Auto-detect CSV (BOM-encoded activity breakdown)
_csv_candidates = list(PROJECT_ROOT.glob("Riipen Career Catalyst*Activity Breakdown*.csv"))
INPUT_CSV = _csv_candidates[0] if _csv_candidates else None

# ---------------------------------------------------------------------------
# Competency framework (canonical order — 20 subskills, 5 areas)
# ---------------------------------------------------------------------------
COMPETENCY_FRAMEWORK = {
    "Career & Self-Development": [
        "Self-Awareness", "Reflection", "Growth Orientation", "Career Articulation"
    ],
    "Communication": [
        "Written Clarity", "Oral Presentation", "Professional Correspondence", "Active Listening"
    ],
    "Critical Thinking": [
        "Problem Framing", "Research & Analysis", "Evidence-Based Reasoning", "Prioritization"
    ],
    "Professionalism": [
        "Dependability", "Quality & Attention to Detail", "Initiative", "Feedback Reception"
    ],
    "Teamwork": [
        "Reliability", "Collaborative Contribution", "Constructive Feedback", "Shared Accountability"
    ],
}

AREA_COLORS = {
    "Career & Self-Development": "#18733E",
    "Communication": "#2454FF",
    "Critical Thinking": "#FF7C0A",
    "Professionalism": "#050C2A",
    "Teamwork": "#7C3AED",
}

# Lighter tints for light fills (20% opacity approximation)
AREA_LIGHT = {
    "Career & Self-Development": "#d4eddc",
    "Communication": "#d4dbff",
    "Critical Thinking": "#ffe4c4",
    "Professionalism": "#d4d5d9",
    "Teamwork": "#e4d9f7",
}

# Build reverse lookup: subskill -> area
SUBSKILL_TO_AREA = {}
for _area, _subs in COMPETENCY_FRAMEWORK.items():
    for _s in _subs:
        SUBSKILL_TO_AREA[_s] = _area


# ---------------------------------------------------------------------------
# 1. Parse T (Taught) from learning-objectives-review.md
# ---------------------------------------------------------------------------
def parse_competencies(comp_str):
    """Return list of (area, subskill) tuples from a competency cell string."""
    results = []
    parts = [p.strip() for p in comp_str.split(";")]
    for part in parts:
        if "→" not in part:
            continue
        area, rest = part.split("→", 1)
        area = area.strip()
        subskills = [s.strip() for s in rest.split(",")]
        for sub in subskills:
            if sub:
                results.append((area, sub))
    return results


def parse_objectives(filepath):
    """Parse learning-objectives-review.md → list of week dicts with objectives."""
    text = filepath.read_text(encoding="utf-8")
    weeks = []
    week_pattern = re.compile(r"^## Week (\d+)\s*[—–-]\s*(.+)$", re.MULTILINE)
    matches = list(week_pattern.finditer(text))

    for i, m in enumerate(matches):
        week_num = int(m.group(1))
        week_title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]

        objectives = []
        row_pattern = re.compile(
            r"^\|\s*\*\*(\d+)\*\*\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|",
            re.MULTILINE,
        )
        for row in row_pattern.finditer(block):
            obj_num = int(row.group(1))
            obj_text = row.group(2).strip()
            comp_text = row.group(3).strip()
            comps = parse_competencies(comp_text)
            objectives.append({
                "num": obj_num,
                "text": obj_text,
                "competencies": comps,
                "comp_raw": comp_text,
            })

        weeks.append({
            "week": week_num,
            "title": week_title,
            "objectives": objectives,
        })
    return weeks


def build_taught_map(weeks):
    """Build T mapping: {(area, subskill): {week: [objective_text, ...]}}"""
    t_map = defaultdict(lambda: defaultdict(list))
    for w in weeks:
        for obj in w["objectives"]:
            for area, sub in obj["competencies"]:
                t_map[(area, sub)][w["week"]].append(obj["text"])
    return t_map


# ---------------------------------------------------------------------------
# 2. Parse P (Practiced) from CSV using rule-based classification
# ---------------------------------------------------------------------------
def parse_activities(csv_path):
    """Parse CSV → list of activity dicts."""
    activities = []
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            activities.append({
                "name": row.get("Activity Name", "").strip(),
                "id": row.get("Activity ID", "").strip(),
                "category": row.get("Category", "").strip(),
                "format": row.get("Format", "").strip(),
                "notes": row.get("Notes", "").strip(),
                "week": int(row.get("Week Number", "0")),
                "week_title": row.get("Week Title", "").strip(),
            })
    return activities


def build_practiced_map(activities):
    """Apply P mapping rules to activities. Returns {(area, subskill): {week: [activity_name, ...]}}"""
    p_map = defaultdict(lambda: defaultdict(list))

    def add_p(week, area, subskill, activity_name):
        p_map[(area, subskill)][week].append(activity_name)

    for act in activities:
        name_lower = act["name"].lower()
        cat = act["category"]
        week = act["week"]
        name = act["name"]

        # Employer touchpoint activities
        if cat == "Employer Engagement" or "employer meeting" in name_lower:
            add_p(week, "Communication", "Oral Presentation", name)
            add_p(week, "Communication", "Active Listening", name)
            add_p(week, "Communication", "Professional Correspondence", name)

        # Async team communication activities
        if "async team communication" in name_lower:
            add_p(week, "Teamwork", "Shared Accountability", name)

        # Team meeting/sync activities
        team_meeting_keywords = [
            "first team meeting", "team sync", "team huddle",
            "team prep session", "team processing session"
        ]
        if any(kw in name_lower for kw in team_meeting_keywords):
            add_p(week, "Teamwork", "Collaborative Contribution", name)
            add_p(week, "Teamwork", "Shared Accountability", name)

        # Production block activities
        production_keywords = [
            "drafting", "research", "outlining", "section development",
            "project production", "deep research", "individual drafting",
            "integration pass"
        ]
        if any(kw in name_lower for kw in production_keywords):
            add_p(week, "Communication", "Written Clarity", name)

        # Also catch the explicit "Project work — research, drafting, outlining, and section development"
        if "project work" in name_lower and any(
            kw in name_lower for kw in ["drafting", "research", "outlining", "section development"]
        ):
            # Already caught above, but ensure it's there
            pass

        # Reflection activities (DEAL reflections)
        if "reflection" in name_lower and ("deal" in name_lower or "draft and submit" in name_lower):
            add_p(week, "Career & Self-Development", "Self-Awareness", name)
            add_p(week, "Career & Self-Development", "Reflection", name)

        # Post-meeting debrief activities
        if "post-meeting debrief" in name_lower or "post-presentation debrief" in name_lower:
            add_p(week, "Communication", "Active Listening", name)
            add_p(week, "Communication", "Written Clarity", name)

        # Internal review gate activities
        if "internal review gate" in name_lower:
            add_p(week, "Professionalism", "Quality & Attention to Detail", name)

        # Email coordination activities
        if "email" in name_lower and ("coordination" in name_lower or "scheduling" in name_lower or "exchange" in name_lower or "outreach" in name_lower):
            add_p(week, "Communication", "Professional Correspondence", name)

        # Feedback processing activities
        if "feedback" in name_lower and ("processing" in name_lower or "response planning" in name_lower or "incorporate" in name_lower):
            add_p(week, "Professionalism", "Feedback Reception", name)

        # Charter/norms activities
        if "charter" in name_lower or "norms" in name_lower:
            add_p(week, "Teamwork", "Shared Accountability", name)

        # Peer evaluation activities
        if "peer evaluation" in name_lower or "peer eval" in name_lower:
            add_p(week, "Teamwork", "Constructive Feedback", name)
            add_p(week, "Teamwork", "Shared Accountability", name)
            add_p(week, "Teamwork", "Reliability", name)
            add_p(week, "Teamwork", "Collaborative Contribution", name)

    return p_map


# ---------------------------------------------------------------------------
# 3. Hardcoded A (Assessed) mappings
# ---------------------------------------------------------------------------
def build_assessed_map():
    """Return {(area, subskill): {week: [deliverable_name, ...]}}"""
    a_map = defaultdict(lambda: defaultdict(list))

    def add_a(week, area, subskill, deliverable):
        a_map[(area, subskill)][week].append(deliverable)

    # Reflections: Weeks 3, 6, 9, 12, 15
    for wk, label in [(3, "Reflection #1"), (6, "Reflection #2"), (9, "Reflection #3"),
                       (12, "Reflection #4"), (15, "Reflection #5")]:
        add_a(wk, "Career & Self-Development", "Self-Awareness", label)
        add_a(wk, "Career & Self-Development", "Reflection", label)
        add_a(wk, "Career & Self-Development", "Growth Orientation", label)

    # Week 15 Reflection #5 also assesses Career Articulation
    add_a(15, "Career & Self-Development", "Career Articulation", "Reflection #5")

    # Week 4: Context Analysis & Project Plan
    for sub in ["Problem Framing", "Research & Analysis", "Evidence-Based Reasoning", "Prioritization"]:
        add_a(4, "Critical Thinking", sub, "Context Analysis & Project Plan")
    add_a(4, "Communication", "Written Clarity", "Context Analysis & Project Plan")

    # Week 5: Direction Check Summary
    add_a(5, "Communication", "Written Clarity", "Direction Check Summary")

    # Week 8: Peer Evaluation #1
    for sub in ["Reliability", "Collaborative Contribution", "Constructive Feedback", "Shared Accountability"]:
        add_a(8, "Teamwork", sub, "Peer Evaluation #1")

    # Week 13: Final Deliverables
    for sub in ["Problem Framing", "Research & Analysis", "Evidence-Based Reasoning", "Prioritization"]:
        add_a(13, "Critical Thinking", sub, "Final Deliverables")
    add_a(13, "Communication", "Written Clarity", "Final Deliverables")
    add_a(13, "Professionalism", "Quality & Attention to Detail", "Final Deliverables")
    add_a(13, "Professionalism", "Feedback Reception", "Final Deliverables")

    # Week 15: Peer Evaluation #2
    for sub in ["Reliability", "Collaborative Contribution", "Constructive Feedback", "Shared Accountability"]:
        add_a(15, "Teamwork", sub, "Peer Evaluation #2")

    # Week 15: Final Presentation
    add_a(15, "Communication", "Oral Presentation", "Final Presentation")
    add_a(15, "Communication", "Active Listening", "Final Presentation")

    # Week 8: Employer mid-project survey
    add_a(8, "Professionalism", "Dependability", "Employer Mid-Project Survey")
    add_a(8, "Professionalism", "Initiative", "Employer Mid-Project Survey")
    add_a(8, "Communication", "Professional Correspondence", "Employer Mid-Project Survey")

    # Week 15: Employer final evaluation
    add_a(15, "Professionalism", "Dependability", "Employer Final Evaluation")
    add_a(15, "Professionalism", "Initiative", "Employer Final Evaluation")
    add_a(15, "Communication", "Professional Correspondence", "Employer Final Evaluation")

    return a_map


# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------
def merge_coverage(t_map, p_map, a_map):
    """Build unified coverage structure.
    Returns coverage[(area, subskill)][week] = {'T': [...], 'P': [...], 'A': [...]}
    """
    coverage = defaultdict(lambda: defaultdict(lambda: {"T": [], "P": [], "A": []}))
    for key, week_dict in t_map.items():
        for wk, texts in week_dict.items():
            coverage[key][wk]["T"].extend(texts)
    for key, week_dict in p_map.items():
        for wk, texts in week_dict.items():
            coverage[key][wk]["P"].extend(texts)
    for key, week_dict in a_map.items():
        for wk, texts in week_dict.items():
            coverage[key][wk]["A"].extend(texts)
    return coverage


def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------
def generate_html(weeks, coverage, t_map, p_map, a_map):
    total_objectives = sum(len(w["objectives"]) for w in weeks)
    avg_per_week = total_objectives / len(weeks) if weeks else 0

    # Count unique subskills that have any coverage
    all_subskills_count = sum(len(subs) for subs in COMPETENCY_FRAMEWORK.values())

    # ── Summary cards ──
    summary_html = f"""
    <div class="summary">
        <div class="summary-card"><div class="num">{total_objectives}</div><div class="label">Total Objectives</div></div>
        <div class="summary-card"><div class="num">{len(COMPETENCY_FRAMEWORK)}</div><div class="label">Competency Areas</div></div>
        <div class="summary-card"><div class="num">{all_subskills_count}</div><div class="label">Unique Subskills</div></div>
        <div class="summary-card"><div class="num">{avg_per_week:.1f}</div><div class="label">Avg Objectives / Week</div></div>
    </div>"""

    # ── Legend ──
    legend_html = _build_legend_html()

    # ── Heatmap matrix ──
    heatmap_html = _build_heatmap_html(coverage)

    # ── Coverage progression ──
    progression_html = _build_progression_html(coverage)

    # ── Gap analysis ──
    gap_html = _build_gap_html(t_map, p_map, a_map)

    # ── Detailed objectives by week ──
    detail_html = _build_detail_html(weeks)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Career Catalyst — Learning Objectives &amp; Competency Map</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<style>
{_get_css()}
</style>
</head>
<body>
<div class="container">
    <!-- Section 1: Header -->
    <div class="header">
        <h1><span>Career Catalyst</span> — Learning Objectives &amp; Competency Map</h1>
        <p>RIIPEN CAREER CATALYST &nbsp;|&nbsp; 15-Week Experiential Learning Course &nbsp;|&nbsp; Three-Level Competency Coverage (Taught / Practiced / Assessed)</p>
    </div>

    <!-- Section 2: Summary Cards -->
    {summary_html}

    <!-- Section 3: Legend -->
    <div class="section-title">Coverage Legend</div>
    {legend_html}

    <!-- Section 4: Heatmap Matrix -->
    <div class="section-title">Competency Coverage Matrix</div>
    {heatmap_html}

    <!-- Section 5: Coverage Progression -->
    <div class="section-title">Coverage Progression by Area</div>
    {progression_html}

    <!-- Section 6: Gap Analysis -->
    <div class="section-title">Gap Analysis</div>
    {gap_html}

    <!-- Section 7: Detailed Objectives by Week -->
    <div class="section-title">Detailed Objectives by Week</div>
    {detail_html}
</div>
</body>
</html>'''
    return html


def _build_legend_html():
    return '''<div class="legend-wrap">
        <div class="legend-grid">
            <div class="legend-item">
                <div class="legend-cell legend-empty"></div>
                <div class="legend-desc"><strong>Empty</strong> — No coverage this week</div>
            </div>
            <div class="legend-item">
                <div class="legend-cell legend-p-only">P</div>
                <div class="legend-desc"><strong>P (Practiced)</strong> — Used through structured activity; not instructional focus</div>
            </div>
            <div class="legend-item">
                <div class="legend-cell legend-t-only">T</div>
                <div class="legend-desc"><strong>T (Taught)</strong> — Learning objective explicitly targets this subskill</div>
            </div>
            <div class="legend-item">
                <div class="legend-cell legend-a-only">A</div>
                <div class="legend-desc"><strong>A (Assessed)</strong> — Graded deliverable formally measures this subskill</div>
            </div>
            <div class="legend-item">
                <div class="legend-cell legend-tp">T</div>
                <div class="legend-desc"><strong>T+P</strong> — Taught and practiced</div>
            </div>
            <div class="legend-item">
                <div class="legend-cell legend-ta">T</div>
                <div class="legend-desc"><strong>T+A</strong> — Taught and assessed</div>
            </div>
            <div class="legend-item">
                <div class="legend-cell legend-pa">P</div>
                <div class="legend-desc"><strong>P+A</strong> — Practiced and assessed</div>
            </div>
            <div class="legend-item">
                <div class="legend-cell legend-tpa">T</div>
                <div class="legend-desc"><strong>T+P+A</strong> — Full coverage: taught, practiced, and assessed</div>
            </div>
        </div>
    </div>'''


def _build_heatmap_html(coverage):
    week_headers = "".join(f"<th>W{i}</th>" for i in range(1, 16))

    rows = []
    # Track column totals
    col_t = defaultdict(int)
    col_p = defaultdict(int)
    col_a = defaultdict(int)

    for area, subskills in COMPETENCY_FRAMEWORK.items():
        color = AREA_COLORS[area]
        num_cols = 17  # subskill label + 15 weeks + totals
        rows.append(
            f'<tr class="area-header" style="background:{color};color:#fff;">'
            f'<td colspan="{num_cols}" style="font-weight:700;padding:8px 12px;font-size:13px;">{area}</td></tr>'
        )

        for sub in subskills:
            key = (area, sub)
            light = AREA_LIGHT[area]

            row_t, row_p, row_a = 0, 0, 0
            cells = ""

            for wk in range(1, 16):
                cell_data = coverage[key][wk]
                has_t = len(cell_data["T"]) > 0
                has_p = len(cell_data["P"]) > 0
                has_a = len(cell_data["A"]) > 0

                if has_t:
                    row_t += 1
                    col_t[wk] += 1
                if has_p:
                    row_p += 1
                    col_p[wk] += 1
                if has_a:
                    row_a += 1
                    col_a[wk] += 1

                # Build tooltip
                tip_parts = []
                if has_t:
                    for t in cell_data["T"]:
                        tip_parts.append(f"T: {t}")
                if has_p:
                    # Deduplicate activity names
                    seen = set()
                    for p in cell_data["P"]:
                        if p not in seen:
                            tip_parts.append(f"P: {p}")
                            seen.add(p)
                if has_a:
                    seen = set()
                    for a in cell_data["A"]:
                        if a not in seen:
                            tip_parts.append(f"A: {a}")
                            seen.add(a)
                tip_text = escape_html("&#10;".join(tip_parts)) if tip_parts else ""

                # Determine cell style and label
                cell_class, cell_label = _cell_style(has_t, has_p, has_a, color, light)

                tooltip_attr = f' title="{tip_text}"' if tip_text else ""
                cells += f'<td class="cell {cell_class}" style="{_cell_inline_style(has_t, has_p, has_a, color, light)}"{tooltip_attr}>{cell_label}</td>'

            # Totals column
            total_parts = []
            if row_t:
                total_parts.append(f"T:{row_t}")
            if row_p:
                total_parts.append(f"P:{row_p}")
            if row_a:
                total_parts.append(f"A:{row_a}")
            total_str = " ".join(total_parts) if total_parts else ""
            cells += f'<td class="cell row-total">{total_str}</td>'

            label_style = f"color:{color};font-weight:500;"
            rows.append(
                f'<tr><td class="subskill-label" style="{label_style}">{sub}</td>{cells}</tr>'
            )

    # Bottom totals row
    total_cells = ""
    for wk in range(1, 16):
        t = col_t[wk]
        p = col_p[wk]
        a = col_a[wk]
        total_cells += f'<td class="cell col-total"><span class="ct-t">{t}</span>/<span class="ct-p">{p}</span>/<span class="ct-a">{a}</span></td>'
    grand_t = sum(col_t.values())
    grand_p = sum(col_p.values())
    grand_a = sum(col_a.values())
    total_cells += f'<td class="cell col-total"><span class="ct-t">{grand_t}</span>/<span class="ct-p">{grand_p}</span>/<span class="ct-a">{grand_a}</span></td>'

    rows.append(
        f'<tr class="totals-row"><td class="subskill-label" style="font-weight:700;">Density (T/P/A)</td>{total_cells}</tr>'
    )

    return f'''<div class="heatmap-wrap">
        <table class="heatmap">
            <thead><tr><th>Subskill</th>{week_headers}<th>Totals</th></tr></thead>
            <tbody>
{"".join(rows)}
            </tbody>
        </table>
    </div>'''


def _cell_style(has_t, has_p, has_a, color, light):
    """Return (extra_css_class, label_text) for a cell."""
    if not has_t and not has_p and not has_a:
        return "cell-empty", ""
    if has_t and has_p and has_a:
        return "cell-tpa", "T"
    if has_t and has_a:
        return "cell-ta", "T"
    if has_t and has_p:
        return "cell-tp", "T"
    if has_p and has_a:
        return "cell-pa", "P"
    if has_t:
        return "cell-t", "T"
    if has_p:
        return "cell-p", "P"
    if has_a:
        return "cell-a", "A"
    return "cell-empty", ""


def _cell_inline_style(has_t, has_p, has_a, color, light):
    """Return inline style string for a matrix cell."""
    if not has_t and not has_p and not has_a:
        return "background:#fff;"

    # T present → solid fill
    if has_t:
        border = f"box-shadow:inset 0 0 0 3px #fff, inset 0 0 0 5px {color};" if has_a else ""
        return f"background:{color};color:#fff;font-weight:700;{border}"

    # P only or P+A → light fill
    if has_p:
        border = f"box-shadow:inset 0 0 0 3px #fff, inset 0 0 0 5px {color};" if has_a else ""
        return f"background:{light};color:{color};font-weight:600;{border}"

    # A only → white with colored border ring
    if has_a:
        return f"background:#fff;color:{color};font-weight:700;box-shadow:inset 0 0 0 3px #fff, inset 0 0 0 5px {color};"

    return "background:#fff;"


def _build_progression_html(coverage):
    """For each area, show 15 week dots colored by coverage level."""
    html_parts = []

    for area, subskills in COMPETENCY_FRAMEWORK.items():
        color = AREA_COLORS[area]
        light = AREA_LIGHT[area]

        dots = ""
        covered_weeks = 0
        first_taught = None

        for wk in range(1, 16):
            # Check any subskill in this area for this week
            has_t = any(len(coverage[(area, sub)][wk]["T"]) > 0 for sub in subskills)
            has_p = any(len(coverage[(area, sub)][wk]["P"]) > 0 for sub in subskills)
            has_a = any(len(coverage[(area, sub)][wk]["A"]) > 0 for sub in subskills)

            if has_t or has_p or has_a:
                covered_weeks += 1
                if has_t and first_taught is None:
                    first_taught = wk

                # Color intensity: T darkest, A medium, P lightest
                if has_t:
                    dot_style = f"background:{color};color:#fff;"
                elif has_a:
                    dot_style = f"background:{color};opacity:0.6;color:#fff;"
                else:
                    dot_style = f"background:{light};color:{color};"
                dots += f'<span class="prog-dot filled" style="{dot_style}" title="Week {wk}">{wk}</span>'
            else:
                dots += f'<span class="prog-dot empty" title="Week {wk}">{wk}</span>'

        taught_text = f"First taught: Week {first_taught}" if first_taught else "Not explicitly taught"
        span_text = f"{covered_weeks} of 15 weeks | {taught_text}"

        html_parts.append(f'''
        <div class="prog-row">
            <div class="prog-label" style="color:{color};">{area}</div>
            <div class="prog-dots">{dots}</div>
            <div class="prog-span">{span_text}</div>
        </div>''')

    return f'<div class="prog-section">{"".join(html_parts)}</div>'


def _build_gap_html(t_map, p_map, a_map):
    """Three gap categories."""
    assessed_not_taught = []
    taught_not_assessed = []
    low_coverage = []

    for area, subskills in COMPETENCY_FRAMEWORK.items():
        for sub in subskills:
            key = (area, sub)
            has_t = len(t_map.get(key, {})) > 0
            has_a = len(a_map.get(key, {})) > 0
            total_t = sum(len(v) for v in t_map.get(key, {}).values())
            total_p = sum(len(v) for v in p_map.get(key, {}).values())
            total_a = sum(len(v) for v in a_map.get(key, {}).values())
            total_all = total_t + total_p + total_a

            # Count unique weeks with any coverage
            all_weeks = set()
            for wk_dict in [t_map.get(key, {}), p_map.get(key, {}), a_map.get(key, {})]:
                all_weeks.update(wk_dict.keys())

            if has_a and not has_t:
                assessed_not_taught.append((area, sub))
            if has_t and not has_a:
                taught_not_assessed.append((area, sub))
            if len(all_weeks) < 3:
                low_coverage.append((area, sub, len(all_weeks)))

    html = '<div class="gap-section">'

    # Category 1: Assessed but never taught
    html += '<h3 class="gap-cat-title gap-warning">Assessed but Never Taught</h3>'
    if assessed_not_taught:
        html += '<p class="gap-note">These subskills are formally assessed but no learning objective teaches them. Consider whether practice alone provides adequate preparation.</p>'
        for area, sub in assessed_not_taught:
            color = AREA_COLORS[area]
            html += f'<div class="gap-item"><span class="gap-badge" style="background:{color};">{area}</span> <strong>{sub}</strong></div>'
    else:
        html += '<p class="gap-ok">None found. All assessed subskills have at least one teaching objective.</p>'

    # Category 2: Taught but never assessed
    html += '<h3 class="gap-cat-title gap-info">Taught but Never Assessed</h3>'
    if taught_not_assessed:
        html += '<p class="gap-note">These subskills have teaching objectives but no formal assessment. Students develop these skills but evidence of learning depends on indirect measures.</p>'
        for area, sub in taught_not_assessed:
            color = AREA_COLORS[area]
            html += f'<div class="gap-item"><span class="gap-badge" style="background:{color};">{area}</span> <strong>{sub}</strong></div>'
    else:
        html += '<p class="gap-ok">None found. All taught subskills are formally assessed.</p>'

    # Category 3: Low coverage
    html += '<h3 class="gap-cat-title gap-caution">Low Coverage (fewer than 3 weeks)</h3>'
    if low_coverage:
        html += '<p class="gap-note">These subskills appear in fewer than 3 weeks across all coverage levels. Consider whether additional touchpoints would strengthen development.</p>'
        for area, sub, count in low_coverage:
            color = AREA_COLORS[area]
            label = "no coverage" if count == 0 else f"{count} week{'s' if count != 1 else ''}"
            html += f'<div class="gap-item"><span class="gap-badge" style="background:{color};">{area}</span> <strong>{sub}</strong> — {label}</div>'
    else:
        html += '<p class="gap-ok">All subskills appear in 3+ weeks. Good coverage density.</p>'

    html += '</div>'
    return html


def _build_detail_html(weeks):
    """Expandable week cards with objective tables."""
    cards = ""
    for w in weeks:
        rows = ""
        for obj in w["objectives"]:
            comp_badges = ""
            for area, sub in obj["competencies"]:
                color = AREA_COLORS.get(area, "#666")
                comp_badges += f'<span class="comp-badge" style="background:{color};">{sub}</span> '
            rows += f'<tr><td class="obj-num">{obj["num"]}</td><td class="obj-text">{escape_html(obj["text"])}</td><td>{comp_badges}</td></tr>'

        cards += f'''
        <div class="week-card" onclick="this.classList.toggle('open')">
            <div class="week-header">
                <span class="chevron">&#9654;</span>
                <span class="week-num">Week {w["week"]}</span>
                <span class="week-title">{escape_html(w["title"])}</span>
                <span class="obj-count">{len(w["objectives"])} objectives</span>
            </div>
            <div class="week-body">
                <table class="obj-table">
                    <thead><tr><th>#</th><th>Objective</th><th>Competencies</th></tr></thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
        </div>'''
    return cards


def _get_css():
    return '''* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'DM Sans',sans-serif; background:#F8F8F8; color:#050C2A; }
.container { max-width:1500px; margin:0 auto; padding:24px 32px; }

/* Header */
.header { background:#050C2A; color:#fff; padding:28px 32px; margin-bottom:24px; border-radius:8px; }
.header h1 { font-size:24px; font-weight:700; }
.header h1 span { color:#FF7C0A; }
.header p { font-size:13px; color:#aaa; margin-top:4px; }

/* Summary cards */
.summary { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:28px; }
.summary-card { background:#fff; border-radius:8px; padding:20px; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,.06); }
.summary-card .num { font-size:32px; font-weight:700; color:#FF7C0A; }
.summary-card .label { font-size:12px; color:#666; margin-top:4px; text-transform:uppercase; letter-spacing:.5px; }

/* Section titles */
.section-title { font-size:18px; font-weight:700; color:#050C2A; margin:28px 0 14px; padding-bottom:6px; border-bottom:2px solid #FF7C0A; display:inline-block; }

/* Legend */
.legend-wrap { background:#fff; border-radius:8px; padding:20px 24px; margin-bottom:28px; box-shadow:0 1px 4px rgba(0,0,0,.06); }
.legend-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }
.legend-item { display:flex; align-items:center; gap:10px; }
.legend-cell { width:36px; height:28px; display:flex; align-items:center; justify-content:center; border-radius:4px; font-size:11px; font-weight:700; flex-shrink:0; }
.legend-empty { background:#fff; border:1px solid #ddd; }
.legend-p-only { background:#ffe4c4; color:#FF7C0A; }
.legend-t-only { background:#FF7C0A; color:#fff; }
.legend-a-only { background:#fff; color:#FF7C0A; box-shadow:inset 0 0 0 3px #fff, inset 0 0 0 5px #FF7C0A; }
.legend-tp { background:#FF7C0A; color:#fff; }
.legend-ta { background:#FF7C0A; color:#fff; box-shadow:inset 0 0 0 3px #fff, inset 0 0 0 5px #FF7C0A; }
.legend-pa { background:#ffe4c4; color:#FF7C0A; box-shadow:inset 0 0 0 3px #fff, inset 0 0 0 5px #FF7C0A; }
.legend-tpa { background:#FF7C0A; color:#fff; box-shadow:inset 0 0 0 3px #fff, inset 0 0 0 5px #FF7C0A; }
.legend-desc { font-size:12px; line-height:1.4; }

/* Heatmap */
.heatmap-wrap { overflow-x:auto; margin-bottom:28px; }
.heatmap { border-collapse:collapse; width:100%; font-size:12px; }
.heatmap th { background:#050C2A; color:#fff; padding:6px 8px; font-weight:500; text-align:center; position:sticky; top:0; z-index:2; }
.heatmap th:first-child { text-align:left; min-width:200px; }
.heatmap .subskill-label { padding:6px 12px; font-size:12px; white-space:nowrap; border-bottom:1px solid #eee; }
.heatmap .cell { text-align:center; padding:6px 4px; border-bottom:1px solid #eee; min-width:46px; cursor:default; font-size:12px; border-radius:2px; }
.heatmap .cell:hover { outline:2px solid #050C2A; outline-offset:-2px; z-index:1; position:relative; }
.heatmap .cell-empty { background:#fff; }
.heatmap .row-total { background:#f5f5f5 !important; color:#050C2A !important; font-size:10px; font-weight:600; min-width:80px; box-shadow:none !important; }
.heatmap .col-total { background:#f5f5f5 !important; color:#050C2A !important; font-weight:600; font-size:10px; box-shadow:none !important; }
.heatmap .area-header td { border-bottom:none; }
.heatmap .totals-row td { border-top:2px solid #050C2A; }
.ct-t { color:#FF7C0A; font-weight:700; }
.ct-p { color:#888; }
.ct-a { color:#050C2A; font-weight:700; }

/* Progression */
.prog-section { margin-bottom:28px; background:#fff; border-radius:8px; padding:20px 24px; box-shadow:0 1px 4px rgba(0,0,0,.06); }
.prog-row { display:flex; align-items:center; margin-bottom:10px; gap:12px; }
.prog-label { width:220px; font-size:13px; font-weight:600; flex-shrink:0; }
.prog-dots { display:flex; gap:4px; }
.prog-dot { width:32px; height:28px; display:flex; align-items:center; justify-content:center; border-radius:4px; font-size:10px; font-weight:600; }
.prog-dot.filled { color:#fff; }
.prog-dot.empty { background:#e8e8e8; color:#bbb; }
.prog-span { font-size:11px; color:#888; margin-left:8px; }

/* Gap analysis */
.gap-section { background:#fff; border-radius:8px; padding:20px 24px; margin-bottom:28px; box-shadow:0 1px 4px rgba(0,0,0,.06); }
.gap-cat-title { font-size:14px; font-weight:700; margin:16px 0 6px; padding-bottom:4px; }
.gap-cat-title:first-child { margin-top:0; }
.gap-warning { color:#c0392b; border-bottom:2px solid #c0392b; display:inline-block; }
.gap-info { color:#2454FF; border-bottom:2px solid #2454FF; display:inline-block; }
.gap-caution { color:#FF7C0A; border-bottom:2px solid #FF7C0A; display:inline-block; }
.gap-item { margin-bottom:6px; font-size:13px; padding-left:4px; }
.gap-badge { display:inline-block; color:#fff; font-size:10px; padding:2px 8px; border-radius:3px; margin-right:6px; font-weight:500; }
.gap-note { font-size:12px; color:#666; margin-bottom:8px; font-style:italic; }
.gap-ok { font-size:12px; color:#18733E; margin-bottom:8px; }

/* Week detail cards */
.week-card { background:#fff; border-radius:8px; margin-bottom:8px; box-shadow:0 1px 3px rgba(0,0,0,.05); overflow:hidden; }
.week-header { display:flex; align-items:center; gap:10px; padding:14px 18px; cursor:pointer; user-select:none; }
.week-header:hover { background:#fafafa; }
.chevron { font-size:11px; color:#888; transition:transform .2s; }
.week-card.open .chevron { transform:rotate(90deg); }
.week-num { font-weight:700; color:#FF7C0A; font-size:14px; }
.week-title { font-weight:500; font-size:14px; flex:1; }
.obj-count { font-size:11px; color:#888; }
.week-body { display:none; padding:0 18px 14px; }
.week-card.open .week-body { display:block; }
.obj-table { width:100%; border-collapse:collapse; font-size:12px; margin-top:8px; }
.obj-table th { background:#f4f4f4; text-align:left; padding:6px 8px; font-weight:600; border-bottom:1px solid #ddd; }
.obj-table td { padding:8px; border-bottom:1px solid #eee; vertical-align:top; }
.obj-table .obj-num { width:30px; text-align:center; font-weight:700; color:#FF7C0A; }
.obj-table .obj-text { line-height:1.5; }
.comp-badge { display:inline-block; color:#fff; font-size:10px; padding:2px 7px; border-radius:3px; margin:2px 2px; white-space:nowrap; font-weight:500; }

/* Print styles */
@media print {
    body { background:#fff; font-size:10px; }
    .container { padding:0; max-width:100%; }
    .header { border-radius:0; page-break-after:avoid; }
    .week-card .week-body { display:block !important; }
    .chevron { display:none; }
    .heatmap .cell:hover { outline:none; }
    .summary { grid-template-columns:repeat(4,1fr); }
    .legend-grid { grid-template-columns:repeat(4,1fr); }
    .heatmap-wrap { overflow:visible; }
    .heatmap { font-size:9px; }
    .heatmap .cell { min-width:30px; padding:3px 2px; }
    .section-title { page-break-after:avoid; }
    .gap-section, .prog-section { page-break-inside:avoid; }
}

@media (max-width:900px) {
    .summary { grid-template-columns:repeat(2,1fr); }
    .legend-grid { grid-template-columns:repeat(2,1fr); }
    .prog-row { flex-wrap:wrap; }
    .prog-label { width:100%; }
}'''


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if not INPUT_MD.exists():
        print(f"ERROR: Cannot find {INPUT_MD}")
        return
    if INPUT_CSV is None or not INPUT_CSV.exists():
        print(f"ERROR: Cannot find activity breakdown CSV in {PROJECT_ROOT}")
        return

    # 1. Parse T (Taught) from objectives markdown
    weeks = parse_objectives(INPUT_MD)
    t_map = build_taught_map(weeks)

    # 2. Parse P (Practiced) from activity CSV
    activities = parse_activities(INPUT_CSV)
    p_map = build_practiced_map(activities)

    # 3. Build A (Assessed) hardcoded map
    a_map = build_assessed_map()

    # 4. Merge into unified coverage
    coverage = merge_coverage(t_map, p_map, a_map)

    # 5. Generate HTML
    html = generate_html(weeks, coverage, t_map, p_map, a_map)
    OUTPUT_FILE.write_text(html, encoding="utf-8")

    # ── Console summary ──
    total_obj = sum(len(w["objectives"]) for w in weeks)
    print(f"Parsed {len(weeks)} weeks, {total_obj} objectives")
    print(f"Competency areas: {len(COMPETENCY_FRAMEWORK)}")
    print(f"Subskills: {sum(len(s) for s in COMPETENCY_FRAMEWORK.values())}")
    print(f"Average objectives/week: {total_obj/len(weeks):.1f}")
    print(f"Activities parsed from CSV: {len(activities)}")

    # Count T/P/A instances
    total_t = sum(sum(len(v) for v in wk_dict.values()) for wk_dict in t_map.values())
    total_p = sum(sum(len(v) for v in wk_dict.values()) for wk_dict in p_map.values())
    total_a = sum(sum(len(v) for v in wk_dict.values()) for wk_dict in a_map.values())
    print(f"Coverage instances — T: {total_t}, P: {total_p}, A: {total_a}")

    # Count unique subskill-week cells with any coverage
    filled_cells = 0
    for area, subskills in COMPETENCY_FRAMEWORK.items():
        for sub in subskills:
            for wk in range(1, 16):
                cell = coverage[(area, sub)][wk]
                if cell["T"] or cell["P"] or cell["A"]:
                    filled_cells += 1
    total_cells = 20 * 15
    print(f"Matrix fill: {filled_cells}/{total_cells} cells ({filled_cells/total_cells*100:.0f}%)")

    # Gap check
    print("\nGap Analysis:")
    gap_count = 0
    for area, subskills in COMPETENCY_FRAMEWORK.items():
        for sub in subskills:
            key = (area, sub)
            has_t = len(t_map.get(key, {})) > 0
            has_a = len(a_map.get(key, {})) > 0
            if has_a and not has_t:
                print(f"  WARNING: {area} > {sub} — Assessed but never taught")
                gap_count += 1
            if has_t and not has_a:
                print(f"  NOTE: {area} > {sub} — Taught but never assessed")
                gap_count += 1
            all_weeks = set()
            for wk_dict in [t_map.get(key, {}), p_map.get(key, {}), a_map.get(key, {})]:
                all_weeks.update(wk_dict.keys())
            if len(all_weeks) < 3:
                print(f"  LOW: {area} > {sub} — Only {len(all_weeks)} week(s)")
                gap_count += 1
    if gap_count == 0:
        print("  No gaps found.")

    print(f"\nOutput: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
