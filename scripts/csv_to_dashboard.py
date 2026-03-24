#!/usr/bin/env python3
"""
Generate an interactive HTML dashboard from the Career Catalyst activity CSV.

Usage:
    python3 scripts/csv_to_dashboard.py "path/to/activities.csv" [output.html]
"""

import csv
import json
import sys
import argparse
from pathlib import Path
from collections import defaultdict


def read_csv(csv_path):
    """Read the CSV and return a list of activity dicts."""
    activities = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Strip BOM and whitespace from keys
            row = {k.strip().lstrip('\ufeff'): v for k, v in row.items()}
            row['Time (min)'] = int(row.get('Time (min)', 0) or 0)
            row['Week Number'] = int(row.get('Week Number', 0) or 0)
            activities.append(row)
    # Sort by Activity ID
    activities.sort(key=lambda x: x.get('Activity ID', ''))
    return activities


def compute_stats(activities):
    """Compute summary statistics."""
    total_time = sum(a['Time (min)'] for a in activities)
    weeks = defaultdict(lambda: {'activities': [], 'total_time': 0, 'categories': defaultdict(int)})

    categories = set()
    formats = set()
    statuses = set()

    for a in activities:
        wk = a['Week Number']
        weeks[wk]['title'] = f"Week {wk} — {a['Week Title']}"
        weeks[wk]['activities'].append(a)
        weeks[wk]['total_time'] += a['Time (min)']
        weeks[wk]['categories'][a['Category']] += a['Time (min)']
        categories.add(a['Category'])
        formats.add(a['Format'])
        statuses.add(a['Status'])

    return {
        'total_activities': len(activities),
        'total_time': total_time,
        'num_weeks': len(weeks),
        'num_categories': len(categories),
        'weeks': dict(weeks),
        'categories': sorted(categories),
        'formats': sorted(formats),
        'statuses': sorted(statuses),
    }


# Category colors using Riipen palette
CATEGORY_COLORS = {
    'Course Orientation': '#2454FF',
    'Project Work': '#FF7C0A',
    'Team Formation': '#18733E',
    'Professional Fundamentals': '#050C2A',
    'Employer Engagement': '#7C3AED',
    'Project Orientation': '#0891B2',
    'Admin': '#ACACAC',
}


def get_category_color(cat):
    return CATEGORY_COLORS.get(cat, '#ACACAC')


def generate_html(activities, stats):
    """Generate the full HTML dashboard with expandable week cards."""
    activities_json = json.dumps(activities, ensure_ascii=False)
    category_colors_json = json.dumps(CATEGORY_COLORS)

    # Build expandable week cards with embedded tables
    week_sections_html = ''
    for wk_num in sorted(stats['weeks'].keys()):
        wk = stats['weeks'][wk_num]
        count = len(wk['activities'])
        hours = wk['total_time'] // 60
        mins = wk['total_time'] % 60
        time_str = f"{hours}h {mins}m" if hours else f"{mins}m"

        # Category bar segments
        cat_bars = ''
        total = wk['total_time']
        for cat, time in sorted(wk['categories'].items(), key=lambda x: -x[1]):
            pct = (time / total * 100) if total else 0
            color = get_category_color(cat)
            cat_bars += f'<div class="cat-bar-segment" style="width:{pct:.1f}%;background:{color}" title="{cat}: {time} min ({pct:.0f}%)"></div>'

        # Category legend items (alphabetical)
        cat_legend = ''
        for cat, time in sorted(wk['categories'].items(), key=lambda x: x[0]):
            color = get_category_color(cat)
            cat_legend += f'<span class="cat-legend-item"><span class="cat-dot" style="background:{color}"></span>{cat} ({time}m)</span>'

        # Build activity table rows for this week
        sorted_activities = sorted(wk['activities'], key=lambda x: x.get('Activity ID', ''))
        table_rows = ''
        for idx, a in enumerate(sorted_activities):
            row_class = ' class="alt-row"' if idx % 2 == 1 else ''
            cat_color = get_category_color(a['Category'])
            table_rows += f'''
                <tr{row_class}>
                    <td class="col-id">{a['Activity ID']}</td>
                    <td class="col-name">{a['Activity Name']}</td>
                    <td class="col-category"><span class="category-badge" style="background:{cat_color}">{a['Category']}</span></td>
                    <td class="col-format">{a['Format']}</td>
                    <td class="col-time">{a['Time (min)']} min</td>
                    <td class="col-notes">{a['Notes']}</td>
                </tr>'''

        week_sections_html += f'''
        <div class="week-section" id="week-{wk_num}">
            <div class="week-card" onclick="toggleWeek({wk_num})">
                <div class="week-card-top">
                    <div class="week-card-left">
                        <div class="week-card-header">Week {wk_num}</div>
                        <div class="week-card-title">{wk['title']}</div>
                    </div>
                    <div class="week-card-right">
                        <div class="week-card-stats">
                            <div class="week-stat">
                                <div class="week-stat-value">{count}</div>
                                <div class="week-stat-label">Activities</div>
                            </div>
                            <div class="week-stat">
                                <div class="week-stat-value">{time_str}</div>
                                <div class="week-stat-label">Total Time</div>
                            </div>
                        </div>
                    </div>
                    <div class="week-card-chevron">
                        <svg class="chevron-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="6 9 12 15 18 9"></polyline>
                        </svg>
                    </div>
                </div>
                <div class="week-card-bottom">
                    <div class="cat-bar">{cat_bars}</div>
                    <div class="cat-legend">{cat_legend}</div>
                </div>
            </div>
            <div class="week-detail" id="detail-{wk_num}">
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Activity</th>
                                <th>Category</th>
                                <th>Format</th>
                                <th>Time</th>
                                <th>Notes</th>
                            </tr>
                        </thead>
                        <tbody>{table_rows}</tbody>
                    </table>
                </div>
            </div>
        </div>'''

    total_hours = stats['total_time'] // 60
    total_mins = stats['total_time'] % 60

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Riipen Career Catalyst — Activity Dashboard</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #F8F8F8;
    color: #050C2A;
    line-height: 1.5;
}}

.header {{
    background: #050C2A;
    color: white;
    padding: 24px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.header-logo {{
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
}}

.header-logo .ii {{
    color: #FF7C0A;
}}

.header-title {{
    font-size: 16px;
    font-weight: 400;
    opacity: 0.8;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 32px 24px;
}}

/* Summary Cards */
.summary-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 40px;
}}

.summary-card {{
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}}

.summary-card-value {{
    font-size: 32px;
    font-weight: 700;
    color: #FF7C0A;
}}

.summary-card-label {{
    font-size: 13px;
    color: #6B7280;
    margin-top: 4px;
}}

/* Week Sections */
.week-section {{
    margin-bottom: 16px;
}}

.week-card {{
    background: white;
    border-radius: 12px;
    padding: 28px 32px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    cursor: pointer;
    transition: box-shadow 0.2s, border-color 0.2s;
    border: 2px solid transparent;
}}

.week-card:hover {{
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border-color: #FF7C0A;
}}

.week-section.open .week-card {{
    border-color: #FF7C0A;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
}}

.week-card-top {{
    display: flex;
    align-items: center;
    gap: 32px;
    margin-bottom: 16px;
}}

.week-card-left {{
    flex: 1;
}}

.week-card-header {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #FF7C0A;
    margin-bottom: 2px;
}}

.week-card-title {{
    font-size: 20px;
    font-weight: 700;
}}

.week-card-right {{
    flex-shrink: 0;
}}

.week-card-stats {{
    display: flex;
    gap: 40px;
}}

.week-stat-value {{
    font-size: 28px;
    font-weight: 700;
}}

.week-stat-label {{
    font-size: 12px;
    color: #6B7280;
}}

.week-card-chevron {{
    flex-shrink: 0;
    color: #ACACAC;
    transition: transform 0.3s, color 0.2s;
}}

.week-section.open .week-card-chevron {{
    transform: rotate(180deg);
    color: #FF7C0A;
}}

.week-card-bottom {{
    margin-top: 4px;
}}

.cat-bar {{
    display: flex;
    height: 8px;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 10px;
}}

.cat-bar-segment {{
    transition: width 0.3s;
}}

.cat-legend {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px 16px;
}}

.cat-legend-item {{
    font-size: 11px;
    color: #6B7280;
    display: flex;
    align-items: center;
    gap: 4px;
}}

.cat-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}}

/* Expandable Detail */
.week-detail {{
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s ease;
}}

.week-section.open .week-detail {{
    max-height: 3000px;
}}

.week-detail .table-wrap {{
    background: white;
    border-top: 1px solid #F3F4F6;
    border-radius: 0 0 12px 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    overflow: hidden;
}}

/* Table */
table {{
    width: 100%;
    border-collapse: collapse;
}}

thead th {{
    background: #FF7C0A;
    color: white;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 10px 16px;
    text-align: left;
    white-space: nowrap;
}}

tbody tr {{
    border-bottom: 1px solid #F3F4F6;
    transition: background 0.15s;
}}

tbody tr.alt-row {{
    background: #FAFAFA;
}}

tbody tr:hover {{
    background: #FFF7ED;
}}

td {{
    padding: 10px 16px;
    font-size: 13px;
    vertical-align: top;
}}

td.col-id {{
    font-weight: 600;
    white-space: nowrap;
    color: #FF7C0A;
    width: 60px;
}}

td.col-time {{
    text-align: right;
    font-weight: 600;
    white-space: nowrap;
    width: 70px;
}}

td.col-name {{
    min-width: 200px;
}}

td.col-notes {{
    font-size: 12px;
    color: #6B7280;
}}

td.col-category {{
    white-space: nowrap;
}}

.category-badge {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    color: white;
}}

td.col-format {{
    white-space: nowrap;
    width: 70px;
}}

/* Responsive */
@media (max-width: 768px) {{
    .summary-row {{
        grid-template-columns: repeat(2, 1fr);
    }}
    .week-card-top {{
        flex-direction: column;
        gap: 16px;
        align-items: flex-start;
    }}
    .week-card-chevron {{
        position: absolute;
        top: 28px;
        right: 24px;
    }}
    .week-card {{
        position: relative;
    }}
    .header {{
        flex-direction: column;
        gap: 8px;
        text-align: center;
    }}
}}
</style>
</head>
<body>

<div class="header">
    <div class="header-logo">R<span class="ii">ii</span>pen</div>
    <div class="header-title">Career Catalyst — Activity Dashboard</div>
</div>

<div class="container">
    <!-- Summary Cards -->
    <div class="summary-row">
        <div class="summary-card">
            <div class="summary-card-value">{stats['total_activities']}</div>
            <div class="summary-card-label">Total Activities</div>
        </div>
        <div class="summary-card">
            <div class="summary-card-value">{total_hours}h {total_mins}m</div>
            <div class="summary-card-label">Total Student Time</div>
        </div>
        <div class="summary-card">
            <div class="summary-card-value">{stats['num_weeks']}</div>
            <div class="summary-card-label">Weeks</div>
        </div>
        <div class="summary-card">
            <div class="summary-card-value">{stats['num_categories']}</div>
            <div class="summary-card-label">Categories</div>
        </div>
    </div>

    <!-- Week Sections (expandable) -->
    {week_sections_html}
</div>

<script>
const CAT_COLORS = {category_colors_json};

function toggleWeek(weekNum) {{
    const section = document.getElementById('week-' + weekNum);
    section.classList.toggle('open');
}}
</script>

</body>
</html>'''

    return html


def main():
    parser = argparse.ArgumentParser(description='Generate interactive HTML dashboard from CSV')
    parser.add_argument('input', help='Input CSV file path')
    parser.add_argument('output', nargs='?', help='Output HTML file path (default: dashboard.html)')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    output_path = args.output or str(input_path.parent / 'dashboard.html')

    activities = read_csv(str(input_path))
    stats = compute_stats(activities)
    html = generate_html(activities, stats)

    Path(output_path).write_text(html, encoding='utf-8')
    print(f"Created: {output_path}")
    print(f"  {stats['total_activities']} activities across {stats['num_weeks']} weeks")
    print(f"  Total time: {stats['total_time']} min ({stats['total_time']//60}h {stats['total_time']%60}m)")


if __name__ == '__main__':
    main()
