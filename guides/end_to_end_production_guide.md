# Design Doc to Canvas — End-to-End Production Guide

How to take a weekly design document and turn it into finished Canvas pages. This is the master workflow — it references the detailed guides for each step.

---

## Pipeline Overview

```
Design Doc → Development Plan → Content → Interactives → Interactive HTML → Videos → Content HTML → Canvas Pages
```

| Phase                       | Input                                        | Output                                          | Guide                                                                   |
| --------------------------- | -------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------- |
| 1. Development Plan         | Design doc                                   | Development plan                                | [Content Development Plan Process](content-development-plan-process.md) |
| 2. Content Production       | Development plan + design doc                | Markdown content files + video scripts          | [Content Production Guide](content-production-guide.md)                 |
| 3. Interactive Design       | Development plan + design doc + page content | Interactive source documents                    | [Interactive Element Guide](interactive-element-guide.md)               |
| 4. Interactive HTML Build   | Interactive source documents                 | Self-contained `.html` files on S3              | [Interactive HTML Guide](interactive-html-guide.md)                     |
| 5. Video Production         | Video script files                           | `.mp4` files + `.srt` caption files             | (Lumen5 or equivalent)                                                  |
| 6. Content HTML Production  | Markdown content files + interactive URLs    | `.html` files with transcripts + interactive links | [Canvas HTML Guide](canvas-html-guide.md)                            |
| 7. Canvas Page Build        | HTML files + videos + captions               | Live Canvas pages                               | This guide (Phase 7 below)                                              |

---

## Phase 1: Create the Development Plan

**Input:** `weekly_design_docs/week[NN]-design-doc.md`
**Output:** `weekly_development_plans/week[NN]-development-plan.md`
**Guide:** [Content Development Plan Process](content-development-plan-process.md)

1. Read the design doc — identify the week's anchor events, deliverables, and activities
2. Sort activities into three buckets: needs produced content, absorbed into another page, or no content needed
3. Define the page list — how many Canvas pages, what each covers, and in what order
4. For each page, specify the content pieces, sub-elements, production approach, and word count targets
5. Identify which pages need video scripts, interactive elements, or curated external links
6. Save the development plan to `weekly_development_plans/`

**Checkpoint:** The development plan should give a complete picture of what needs to be produced and where it lives. Every activity from the design doc should be accounted for.

---

## Phase 2: Produce the Content

**Input:** Development plan + design doc
**Output:** Markdown content files in `weekly_content/week[NN]/`
**Guide:** [Content Production Guide](content-production-guide.md)

1. Create the week folder: `weekly_content/week[NN]/`
2. Work through the development plan page by page, producing each content file:
   - `page[N]-[short-title].md` — student-facing page content
   - `page[N]-[short-title]-video.md` — video scripts (where the development plan calls for them)
3. Include placeholders in the markdown for elements that will be produced separately:
   - `[VIDEO: title]` — where a video will be embedded
   - `[INTERACTIVE: description]` — where an interactive exercise will be linked
   - `[CURATED LINK: topic]` — where an external resource needs to be sourced, with options listed below
   - `[TEMPLATE: description]` — where a template or checklist will appear
   - `[LINKED RESOURCE: description]` — where an internal course link will go
4. Source and select curated links — verify URLs are accessible (no login walls) and appropriate for students

**Checkpoint:** Every page listed in the development plan has a corresponding `.md` file. Video scripts exist for every `[VIDEO:]` placeholder. Curated links have been selected.

---

## Phase 3: Design Interactive Elements

**Input:** Development plan + design doc + page content files
**Output:** Interactive source documents in `weekly_content/week[NN]/`
**Guide:** [Interactive Element Guide](interactive-element-guide.md)

Not every week has interactives. Check the development plan — it specifies which pages need them.

1. Read the page content the interactive will live on — understand the context
2. Design the scenario, questions, and feedback following the interactive element guide
3. Save as `page[N]-[short-title]-interactive.md`

**Checkpoint:** Each interactive has a complete source document with scenario, all question branches, and feedback text.

---

## Phase 4: Build Interactive HTML

**Input:** Interactive source documents (`*-interactive.md`) from Phase 3
**Output:** Self-contained `.html` files uploaded to S3
**Guide:** [Interactive HTML Guide](interactive-html-guide.md)

Not every week has interactives. Check the development plan — if Phase 3 produced no interactive source documents, skip this phase.

1. For each interactive source document, build the self-contained HTML file following the Interactive HTML Guide
2. Populate the question data from the source document's questions, options, correct answers, and per-option feedback
3. Test locally — click through every question path, verify all feedback renders, check mobile, check keyboard navigation
4. Upload to S3:
   - Bucket: `riipen-career-catalyst-interactives` (or the designated bucket)
   - Path: `week[NN]/week[NN]-[short-title]-interactive.html`
   - Set `Content-Type: text/html` and public-read permissions
   - Note the full S3 URL (e.g., `https://riipen-career-catalyst-interactives.s3.amazonaws.com/week01/week01-deal-sorting-interactive.html`)
5. Update the corresponding content markdown file: replace the `[INTERACTIVE: ...]` placeholder with the specific title, description, and S3 URL so that Phase 6 produces a working link

**Checkpoint:** Every interactive source document has a corresponding `.html` file uploaded to S3 with a working public URL. The content markdown files have been updated with the real URLs.

---

## Phase 5: Produce Videos

**Input:** Video script files (`*-video.md`)
**Output:** `.mp4` video files + `.srt` caption files in `weekly_content/week[NN]/`

This phase uses Lumen5 or equivalent video production tools.

1. Create the video from the script
2. Publish and download the video as `.mp4`
3. Download the `.srt` caption file from Lumen5.
4. Save both files to the week's content folder

**Checkpoint:** Every `[VIDEO:]` placeholder in the content has a corresponding `.mp4` and `.srt` file.

---

## Phase 6: Produce the Content HTML

**Input:** Markdown content files from Phase 2 + interactive URLs from Phase 4
**Output:** `.html` files in `weekly_content/week[NN]/`
**Guide:** [Canvas HTML Guide](canvas-html-guide.md)

This phase converts the content markdown files (not interactives) into Canvas-compatible HTML.

1. For each page markdown file, create the corresponding `.html` file
2. Use the component library in the Canvas HTML Guide to convert each section:
   - Section headers → orange bar with `<h2><strong>` inside
   - Subsections → `<h3><strong>` headings
   - Guidance/tips → info callouts (blue border)
   - Rules/policies → key principle callouts (orange border)
   - Examples → scenario boxes (purple dashed) or comparison columns
   - AI guidance → dark blue AI guidance box
   - External links → curated link component or YouTube video card
   - Checklists → checklist box component
   - Optional content → expand/collapse sections
3. For `[VIDEO:]` placeholders, add an HTML comment and a transcript section:
   ```html
   <!-- VIDEO: Title (filename.mp4 + filename.srt) -->
   <details style="border: 1px solid #e2e4e9; border-radius: 8px; margin: 0 0 20px; overflow: hidden;">
     <summary style="background: #f7f8fa; padding: 12px 18px; font-size: 14px; color: #050c2a; cursor: pointer;">
       <strong>Video Transcript</strong>: Title
     </summary>
     <div style="padding: 16px 20px;">
       <!-- Transcript text from the video script file -->
     </div>
   </details>
   ```
4. For `[INTERACTIVE:]` placeholders, use the interactive placeholder component. These placeholders should now have real S3 URLs from Phase 4 — use the actual URL in the interactive placeholder component's link (not `href="#"`)
5. Review: count opening and closing `<div>` tags — they must match

**Checkpoint:** Every `.md` content file has a corresponding `.html` file. Transcripts are included for all videos. Interactive placeholders have working S3 URLs. No broken `<div>` nesting.

---

## Phase 7: Build the Canvas Pages

**Input:** HTML files + video files + caption files
**Output:** Live Canvas pages

This phase is done manually in the Canvas browser interface.

### 7.1 Upload Media to Course Files

Before building pages, upload all media for the week:

1. In Canvas, go to **Files** in the left sidebar
2. Create a folder for the week (e.g., `Week 02`)
3. Upload all `.mp4` video files for the week
4. Upload any images referenced in the content

### 7.2 Create the Module

1. Go to **Modules** in the left sidebar
2. Create a module for the week (e.g., "Week 2: Building Your Team")

### 7.3 Create and Build Each Page

For each page in the week, in order:

#### Create the page
1. Inside the module, click **+** to add an item
2. Select **New Page**, enter the page title (from the H1 in the markdown, e.g., "Building Your Team")
3. Save the blank page — it's automatically added to the module in order

#### Paste the HTML
1. Edit the page
2. Click the **HTML Editor** button (`</>`) to switch to HTML view
3. Open the `.html` file and copy the full contents
4. Paste into the HTML editor
5. **Important:** The HTML will contain `<!-- VIDEO: ... -->` comments where videos go. These are invisible markers — leave them in place for now.
6. Save and verify the page renders correctly (orange headers, callout boxes, expand/collapse sections)

#### Add videos
For each `<!-- VIDEO: ... -->` comment in the HTML:

1. Edit the page in the **visual editor** (not HTML view)
2. Place your cursor above the Video Transcript section
3. Click the **Media** icon in the toolbar > **Upload/Record Media**
4. Upload the `.mp4` file
5. Click on the inserted video to select it
6. **Resize to Large** — select the largest size option so the video fills the content width
7. Save

#### Add captions
1. After saving, view the page and play the video briefly
2. Click the **three dots** menu on the video player
3. Select **CC** or **Captions/Subtitles**
4. Upload the `.srt` file and set language to English
5. Verify captions appear when toggled on

#### Add images (if any)
1. Edit the page in the visual editor
2. Place cursor where the image should go
3. Click the **Images** icon > select from Course Files
4. Add descriptive **alt text**

### 7.4 Verify the Week

Run through every page and check:

- [ ] Page titles are correct and consistent
- [ ] All text renders with correct formatting
- [ ] All `<div>` tags are properly closed (nothing looks broken)
- [ ] Videos play and fill the content width
- [ ] Captions toggle on/off correctly
- [ ] Video transcripts expand and collapse
- [ ] All expand/collapse sections work and show the disclosure triangle
- [ ] Links open in new tabs
- [ ] YouTube videos auto-embed as inline players (if applicable)
- [ ] Interactive links open the correct S3-hosted interactive in a new tab
- [ ] Interactive placeholders are clearly marked
- [ ] Pages appear in correct order in the module
- [ ] Pages look acceptable on mobile (use browser responsive mode)

---

## Folder Structure Reference

```
weekly_design_docs/
  week[NN]-design-doc.md              ← Phase 1 input

weekly_development_plans/
  week[NN]-development-plan.md        ← Phase 1 output / Phase 2 input

weekly_content/week[NN]/
  page[N]-[short-title].md            ← Phase 2 output (content)
  page[N]-[short-title]-video.md      ← Phase 2 output (video scripts)
  page[N]-[short-title]-interactive.md ← Phase 3 output (interactive source)
  week[NN]-[short-title]-interactive.html  ← Phase 4 output (interactive HTML, also uploaded to S3)
  [video-name].mp4                    ← Phase 5 output (video file)
  [video-name]-captions.srt           ← Phase 5 output (caption file)
  page[N]-[short-title].html          ← Phase 6 output (Canvas-ready HTML)

guides/
  content-development-plan-process.md  ← Phase 1 guide
  content-production-guide.md          ← Phase 2 guide
  interactive-element-guide.md         ← Phase 3 guide
  interactive-html-guide.md            ← Phase 4 guide
  canvas-html-guide.md                 ← Phase 6 guide
  canvas-build-guide.md                ← This file (master workflow + Phase 7)
```

---

## Tips

- **Work in order.** Each phase depends on the previous one. Don't skip ahead — the development plan shapes everything downstream.
- **Save frequently in Canvas.** Canvas can lose unsaved work if the session times out.
- **Check HTML view after Canvas saves.** Canvas normalizes HTML on save — it strips `font-weight`, `text-transform`, `letter-spacing`, and lowercases hex colors. This is expected and accounted for in the HTML guide.
- **If formatting breaks after adding a video,** switch to HTML view and check that Canvas didn't insert the video inside a `<div>` that breaks the structure. Move it outside if needed.
- **Bold in Canvas.** Canvas strips native heading bold. The HTML guide accounts for this with `<strong>` tags inside `<h2>` and `<h3>` elements. If headings appear unbolded, you can select them in the visual editor and press Ctrl/Cmd+B.
- **One week at a time.** Complete all phases for one week before moving to the next. This keeps context fresh and avoids cross-week confusion.
- **Interactive URLs must be live before Phase 6.** Content HTML production needs the real S3 URLs to put in the interactive placeholder links. If you're working on interactives and content HTML in parallel, use a temporary placeholder URL and update it before the Canvas build.
