# Career Catalyst — Project Notes for Claude

## Pushing content to Canvas — full editorial workflow

To get the **same quality as the hand-built weeks 1-2 pages** (callouts, comparison columns, expand/collapse, key principle wraps), the conversion has to go through Claude's editorial judgment, not the deterministic Python script.

### The right command for polished pages

```bash
python3 scripts/push_to_canvas.py --week <N> --use-html --module --yes
```

The `--use-html` flag tells the script to use whatever `.canvas.html` file exists alongside each source markdown (whatever Claude produced) instead of regenerating it from the deterministic converter.

### The full polished pipeline (what to do before that command)

1. Run the deterministic converter once to get a baseline structural HTML for every page in the week:
   ```bash
   python3 scripts/md_to_canvas_html.py --week <N>
   ```
   This writes `<source>.canvas.html` files alongside every source markdown.

2. **Editorial pass (this is the part that needs Claude, not the script).** For each page:
   - Read the source markdown.
   - Refer to `guides/canvas-html-guide.md` for the component library and the constraints (inline styles only, `<strong>` for bold, etc.).
   - Refer to a hand-built reference like `weekly_content/week01/page8-setting-up-success.html` to calibrate on what "good" looks like.
   - Edit the `<source>.canvas.html` file: promote single-paragraph principles to **Key Principle Callouts** (orange), wrap practical guidance as **Info Callouts** (blue), wrap AI rules as **AI Guidance Boxes** (dark blue), wrap worked examples as **Scenario Boxes** (purple dashed), convert good/bad pairs to **Comparison Columns** (red/green), wrap optional content in **Expand/Collapse**.

3. Then push with `--use-html`:
   ```bash
   python3 scripts/push_to_canvas.py --week <N> --use-html --module --yes
   ```

### Pushing a single page (when only one page changed locally)

```bash
python3 scripts/push_to_canvas.py weekly_content/weekNN/pageX-name.md --use-html --yes
```

**Use this any time you've only edited one page locally** — especially when other pages in the same week have Canvas-side edits you want to preserve. `--week N` pushes ALL 10 pages in the week and will overwrite any Canvas-side work on the other pages with whatever `.canvas.html` files exist locally (which may be stale). The positional-arg form pushes only that one page. `--module` isn't needed if the page is already at the right position.

### Fast / deterministic mode (no editorial pass)

```bash
python3 scripts/push_to_canvas.py --week <N> --module --yes
```

Uses the deterministic converter directly. Fine for first drafts and quick iteration; lacks editorial polish.

### Important workflow rules

- **The `.canvas.html` file is the source of truth for the polished version.** If it exists, push with `--use-html`. If you push without `--use-html`, the script regenerates from the source markdown using the deterministic converter, which **will overwrite your editorial polish**.
- The `.canvas.html` files are gitignored, so they live only on this machine. They're rebuilt by re-running step 1 above.
- Slug convention: `page1-overview.md` → `week-N-overview`, `page*-whats-next.md` → `week-N-whats-next`, content pages → slugified frontmatter title. The `--module` flag auto-places pages into the matching `Week N: ...` Canvas module in source-file order.
- Test course: course 107 ("Career Catalyst") on `riipen.instructure.com`. Pages default to unpublished — review in Canvas before publishing.

### Skills

- `/md-to-canvas-html` — convert one or more pages with editorial pass (writes `.canvas.html`)
- `/push-to-canvas` — convert (with editorial pass) + push to Canvas

### Composition reminders for the editorial pass

- **SKILLS YOU'LL PRACTICE badges go at the very top of the page** (above the intro paragraph), not after the intro.
- Don't double-box: checklists and callouts inside a Section Body wrapper should not have their own outer box border. (Checklist component was simplified for this reason.)
- Bold inside link text (`[**Datawrapper**](url)`) is supported by the converter — renders as `<strong>` inside `<a>`.
