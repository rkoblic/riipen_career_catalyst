# Canvas Page HTML Guide

How to convert content source documents into Canvas LMS-compatible HTML pages for Riipen Career Catalyst.

This guide provides the component library, constraints, and process for turning markdown content files into styled HTML that can be copied and pasted directly into the Canvas Rich Content Editor.

---

## Canvas Constraints

- **Inline styles only.** Canvas strips `<style>` blocks and external stylesheets. Every element must be styled with the `style=""` attribute.
- **No JavaScript.** Canvas strips all `<script>` tags. Interactivity must use native HTML5 elements only.
- **No iframes.** Canvas either strips or breaks iframe embeds (YouTube iframes produce Error 153). Use bare YouTube URLs instead — Canvas auto-embeds them.
- **Canvas strips some inline styles.** Specifically: `font-weight`, `text-transform`, `letter-spacing`. Use `<strong>` tags for bold (even inside `<h2>` and `<h3>` elements, whose native bold gets stripped) and write label text in actual UPPERCASE characters instead of relying on `text-transform`.
- **Canvas normalizes `rel` attributes.** It strips `noreferrer` from `rel="noopener noreferrer"`. Use `rel="noopener"` only.
- **Expand/collapse is supported** via native `<details>` / `<summary>` HTML5 elements. These work without JavaScript.
- **Images** must be uploaded to Canvas and referenced by their Canvas URL, or linked from a stable external URL.
- **Videos** can be uploaded to Canvas Course Files (included in .imscc exports) and embedded with `<video>` tags, or linked from YouTube (Canvas auto-embeds).
- **The HTML is pasted into the Rich Content Editor** using the "HTML Editor" view (</> icon). Switch to HTML view, paste, save.

---

## Brand Colors & Accessible Colorways

Per Riipen brand guidelines, these are the approved text/background combinations:

| Background | Text Color | Usage |
|---|---|---|
| Orange `#ff7c0a` | Dark Blue `#050c2a` | Section headers |
| Dark Blue `#050c2a` | White `#ffffff` | AI guidance boxes, dark callouts |
| Electric Blue `#2454ff` | White `#ffffff` | Available but not currently used |
| Green `#18733e` | White `#ffffff` | Success/good example callouts |
| Grey `#f7f8fa` | Dark Blue `#050c2a` | Callout boxes, expandable sections |
| White `#ffffff` | Dark Blue `#050c2a` | Default body text |

Additional color usage:
- **Links:** Electric Blue `#2454ff` (passes WCAG AA at 4.5:1 on white)
- **Muted/secondary text:** `#6b7280` (passes WCAG AA at 4.6:1 on white — do NOT use `#acacac` which fails at 2.8:1)
- **Borders:** `#e2e4e9`
- **Scenario accents:** Purple `#7c3aed`

---

## Typography

Canvas strips `font-weight`, so bold must come from `<strong>` tags — even inside `<h2>` and `<h3>` elements, whose native bold Canvas also strips.

| Element | Size | Bold? | Color |
|---|---|---|---|
| Page intro text | 15px | no | Dark Blue |
| Section header (h2 in orange bar) | 16px | yes (`<strong>` inside h2) | Dark Blue (on orange) |
| H3 (subsection) | 16px | yes (`<strong>` inside h3) | Dark Blue |
| Body text | 14px | no | Dark Blue |
| List items | 14px | no | Dark Blue |
| Callout labels | 12px | no (Canvas strips it) | Varies |
| Small / muted text | 13px | no | `#6b7280` |

---

## Page Wrapper

Every Canvas page starts with this wrapper. It sets the base font, text color, line height, and max width.

```html
<div style="font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #050c2a; line-height: 1.7; max-width: 800px;">

  <!-- All page content goes here -->

</div>
```

**Note:** DM Sans is the Riipen brand font. It's listed first in the font stack. If DM Sans isn't available in the Canvas environment, the system font fallback chain ensures consistent rendering.

---

## Component Library

### 1. Section Header (Orange Bar)

Used to divide the page into major sections. Orange background, dark blue text, rounded top corners. Always followed by a Section Body. Uses a semantic `<h2>` for screen reader navigation.

```html
<div style="background: #ff7c0a; padding: 12px 18px; border-radius: 8px 8px 0 0; margin-top: 28px;">
  <h2 style="font-size: 16px; color: #050c2a; margin: 0;"><strong>Section Title Here</strong></h2>
</div>
```

### 2. Section Body

The content container below a Section Header. Light border, rounded bottom corners.

```html
<div style="border: 1px solid #e2e4e9; border-top: none; border-radius: 0 0 8px 8px; padding: 20px 24px; margin-bottom: 24px;">

  <!-- Section content goes here -->

</div>
```

### 3. H3 Subsection Heading

Used within section bodies to break content into sub-topics.

```html
<h3 style="font-size: 16px; color: #050c2a; margin: 24px 0 8px;"><strong>Subsection Title</strong></h3>
```

For the first H3 in a section body, use `margin: 0 0 8px` to remove the top margin.

### 4. Body Text

Standard paragraph text.

```html
<p style="font-size: 14px; margin-bottom: 12px;">Paragraph text here.</p>
```

### 5. Bullet List

```html
<ul style="font-size: 14px; margin: 0 0 16px 20px;">
  <li style="margin-bottom: 6px;">First item</li>
  <li style="margin-bottom: 6px;">Second item</li>
  <li style="margin-bottom: 6px;">Third item</li>
</ul>
```

For bold-label bullets (common in this course):

```html
<ul style="font-size: 14px; margin: 0 0 16px 20px;">
  <li style="margin-bottom: 6px;"><strong>Label.</strong> Description text here.</li>
  <li style="margin-bottom: 6px;"><strong>Label.</strong> Description text here.</li>
</ul>
```

### 6. Numbered List

```html
<ol style="font-size: 14px; margin: 0 0 16px 20px;">
  <li style="margin-bottom: 6px;">First item</li>
  <li style="margin-bottom: 6px;">Second item</li>
  <li style="margin-bottom: 6px;">Third item</li>
</ol>
```

For bold-label numbered items:

```html
<ol style="font-size: 14px; margin: 0 0 16px 20px;">
  <li style="margin-bottom: 6px;"><strong>Label (N min).</strong> Description text here.</li>
  <li style="margin-bottom: 6px;"><strong>Label (N min).</strong> Description text here.</li>
</ol>
```

### 7. Info Callout (Blue Left Border)

Used for agendas, suggested timelines, structured guidance, and practical tips. Label text is written in actual uppercase (Canvas strips `text-transform`).

```html
<div style="background: #f7f8fa; border-left: 4px solid #2454ff; padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 16px 0;">
  <div style="font-size: 12px; margin-bottom: 6px; color: #2454ff;">CALLOUT LABEL</div>
  <p style="font-size: 14px; margin: 0;">Callout content here.</p>
</div>
```

### 8. Key Principle Callout (Orange Left Border)

Used for important rules, key distinctions, and course policies that students should pay special attention to.

```html
<div style="background: #fff8f1; border-left: 4px solid #ff7c0a; padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 16px 0;">
  <div style="font-size: 12px; margin-bottom: 6px; color: #ff7c0a;">KEY PRINCIPLE</div>
  <p style="font-size: 14px; margin: 0;">Principle text here.</p>
</div>
```

### 9. Scenario Example Box (Purple Dashed Border)

Used for worked examples, "what this looks like in practice" scenarios, and case illustrations.

```html
<div style="background: #f7f8fa; border: 2px dashed #7c3aed; border-radius: 10px; padding: 20px 24px; margin: 16px 0;">
  <div style="font-size: 11px; color: #7c3aed; margin-bottom: 8px;">SCENARIO EXAMPLE</div>
  <p style="font-size: 14px; margin: 0;">Scenario content here.</p>
</div>
```

### 10. Checklist Box

Used for meeting checklists, completion criteria, and reference lists students should check off mentally. Uses text checkboxes since Canvas strips form elements.

```html
<div style="background: white; border: 1px solid #e2e4e9; border-radius: 10px; padding: 18px 22px; margin: 12px 0 20px;">
  <div style="font-size: 14px; margin-bottom: 10px;"><strong>Checklist Title</strong></div>
  <p style="font-size: 14px; margin-bottom: 4px;"><span aria-hidden="true">&#9744; </span><strong>Item one</strong> — description</p>
  <p style="font-size: 14px; margin-bottom: 4px;"><span aria-hidden="true">&#9744; </span><strong>Item two</strong> — description</p>
  <p style="font-size: 14px; margin-bottom: 0;"><span aria-hidden="true">&#9744; </span><strong>Item three</strong> — description</p>
</div>
```

**Note:** The `&#9744;` renders as ☐. It's wrapped in `aria-hidden="true"` so screen readers skip the symbol and read the text content directly. If Canvas strips `aria-hidden`, the fallback is acceptable — screen readers will announce "ballot box" which is understandable in context.

### 11. Comparison Columns (Good vs. Bad)

Used to show contrasting examples side by side. Red-tinted for weak examples, green-tinted for strong ones. Label text is written in actual uppercase.

```html
<div style="display: flex; gap: 16px; margin: 16px 0 20px;">
  <div style="flex: 1; background: #fff3f3; border: 1px solid #ffc9c9; border-radius: 8px; padding: 14px 16px; font-size: 13px; line-height: 1.6;">
    <strong style="display: block; font-size: 12px; margin-bottom: 6px;">Weak Example</strong>
    Weak example text here.
  </div>
  <div style="flex: 1; background: #f0faf4; border: 1px solid #b8e6cc; border-radius: 8px; padding: 14px 16px; font-size: 13px; line-height: 1.6;">
    <strong style="display: block; font-size: 12px; margin-bottom: 6px;">Strong Example</strong>
    Strong example text here.
  </div>
</div>
```

**Mobile fallback:** If flex columns display poorly on narrow screens, use stacked blocks instead:

```html
<div style="background: #fff3f3; border: 1px solid #ffc9c9; border-radius: 8px; padding: 14px 16px; font-size: 13px; line-height: 1.6; margin: 16px 0 8px;">
  <strong style="display: block; font-size: 12px; margin-bottom: 6px;">Weak Example</strong>
  Weak example text here.
</div>
<div style="background: #f0faf4; border: 1px solid #b8e6cc; border-radius: 8px; padding: 14px 16px; font-size: 13px; line-height: 1.6; margin: 0 0 20px;">
  <strong style="display: block; font-size: 12px; margin-bottom: 6px;">Strong Example</strong>
  Strong example text here.
</div>
```

### 12. Expand/Collapse Section

Used for optional content, detailed examples, or supplementary material that not every student needs to read. Uses native HTML5 `<details>` / `<summary>` elements (no JavaScript required).

```html
<details style="border: 1px solid #e2e4e9; border-radius: 8px; margin: 16px 0; overflow: hidden;">
  <summary style="background: #f7f8fa; padding: 12px 18px; font-size: 14px; color: #050c2a; cursor: pointer;">
    Click to expand: Section Title
  </summary>
  <div style="padding: 16px 20px;">
    <p style="font-size: 14px; margin-bottom: 12px;">Expandable content here.</p>
  </div>
</details>
```

**Note:** Do NOT set `list-style: none` on the summary — the native disclosure triangle (▸/▾) is an important visual cue that the content is expandable.

### 13. YouTube Video (Auto-Embed)

Used for external YouTube videos. Canvas auto-embeds YouTube URLs as inline video players when the link is inside a container. The bare URL must be the link text.

```html
<div style="background: #f7f8fa; border: 1px solid #e2e4e9; border-radius: 10px; padding: 20px 24px; margin: 20px 0;">
  <p style="font-size: 14px; color: #050c2a; margin-bottom: 4px;">Video Title Here</p>
  <p style="font-size: 13px; color: #6b7280; margin-bottom: 12px;">Source (duration). Brief description.</p>
  <a style="color: #2454ff;" href="https://youtu.be/VIDEO_ID" target="_blank" rel="noopener">https://youtu.be/VIDEO_ID</a>
</div>
```

**Important:**
- The `<a>` tag's text content must be the bare YouTube URL (e.g., `https://youtu.be/VIDEO_ID`) — this is what triggers Canvas to auto-embed.
- Do NOT use descriptive link text (e.g., "Watch Video") — Canvas won't auto-embed it.
- Do NOT use `<iframe>` embeds — Canvas produces Error 153.
- The video width is controlled by Canvas, not by our CSS. It may not fill the full card width.
- Put `style` before `href` on the `<a>` tag (this matches what Canvas saves).

### 14. Canvas-Hosted Video

**Do NOT add Canvas-hosted videos through HTML.** Canvas strips `<video>` and `<track>` elements and manages its own media player. Instead, add videos through the Rich Content Editor's media upload tool during the Canvas page build step. See the [Canvas Build Guide](end_to_end_production_guide.md) for the full workflow.

In the HTML file, leave a comment where the video should be inserted:

```html
<!-- VIDEO: Title Here (filename.mp4 + filename.srt) -->
```

Always include a Video Transcript component (below) directly after the video comment.

### 15. Video Transcript

Place directly below any video component (YouTube, Canvas-hosted, or placeholder). Uses an expand/collapse section so it doesn't add clutter but is available for students who need or prefer it. Required for WCAG AA compliance.

```html
<details style="border: 1px solid #e2e4e9; border-radius: 8px; margin: 0 0 20px; overflow: hidden;">
  <summary style="background: #f7f8fa; padding: 12px 18px; font-size: 14px; color: #050c2a; cursor: pointer;">
    <strong>Video Transcript</strong>: Title Here
  </summary>
  <div style="padding: 16px 20px;">
    <p style="font-size: 14px; margin-bottom: 12px;">Transcript text here. Use multiple &lt;p&gt; tags for natural paragraph breaks from the script.</p>
    <p style="font-size: 14px; margin-bottom: 0;">Final paragraph of transcript.</p>
  </div>
</details>
```

**Notes:**
- Use `margin: 0 0 20px` (no top margin) so the transcript sits flush against the video card above it.
- The transcript source is typically the video script file (`*-video.md`) cleaned up for reading.
- For YouTube videos with auto-generated or uploaded captions, a transcript is still recommended — captions and transcripts serve different accessibility needs.

### 16. Video Placeholder

Used where a video will be embedded but hasn't been produced yet.

```html
<div style="background: #f7f8fa; border: 1px solid #e2e4e9; border-radius: 10px; padding: 24px; text-align: center; margin: 20px 0;">
  <p style="font-size: 14px; color: #050c2a; margin-bottom: 4px;"><span aria-hidden="true">&#127916; </span>Video: Title Here</p>
  <p style="font-size: 13px; color: #6b7280; margin: 0;">Video will be embedded here once produced.</p>
</div>
```

### 17. Interactive Element Placeholder

Used where an interactive exercise will be linked or embedded.

```html
<div style="background: #f7f8fa; border: 2px dashed #7c3aed; border-radius: 10px; padding: 20px 24px; text-align: center; margin: 16px 0;">
  <p style="font-size: 15px; margin-bottom: 4px;"><span aria-hidden="true">&#127919; </span>Interactive: Title Here</p>
  <p style="font-size: 13px; color: #6b7280; margin-bottom: 12px;">Brief description. ~X minutes.</p>
  <p style="font-size: 14px; margin: 0;"><a style="color: #2454ff;" href="#" target="_blank" rel="noopener">Open the Interactive &rarr;</a></p>
</div>
```

### 18. Curated Link

Used for external resources (articles, non-YouTube videos).

```html
<p style="font-size: 14px;"><span aria-hidden="true">&#128206; </span><a href="URL_HERE" target="_blank" rel="noopener" style="color: #2454ff;">Resource Title</a> — Source name. Brief description of what the resource covers.</p>
```

### 19. AI Guidance Box (Dark Blue Background)

Used for AI use and disclosure information specific to a deliverable or activity.

```html
<div style="background: #050c2a; color: white; border-radius: 8px; padding: 16px 20px; margin: 16px 0;">
  <div style="font-size: 12px; margin-bottom: 6px;">AI USE</div>
  <p style="font-size: 14px; margin: 0; color: white;">AI guidance text here.</p>
</div>
```

---

## Choosing Components

Use this guide to match content types to components:

| Content type | Component |
|---|---|
| Major page sections (Before/During/After, deliverable sections) | Section Header + Section Body |
| Sub-topics within a section | H3 Subsection Heading |
| Step-by-step instructions, agendas | Numbered List |
| Practical guidance, agendas, structured tips | Info Callout (blue) |
| Important rules, key distinctions, policies | Key Principle Callout (orange) |
| Worked examples, "what this looks like" | Scenario Example Box (purple) |
| Reference checklists, completion criteria | Checklist Box |
| Good vs. bad, before vs. after | Comparison Columns |
| Optional or supplementary content | Expand/Collapse Section |
| AI permissions and disclosure rules | AI Guidance Box (dark blue) |
| External articles, non-YouTube video links | Curated Link |
| YouTube videos | YouTube Video (auto-embed) |
| Videos uploaded to Canvas | HTML comment placeholder (added via Rich Content Editor during build) |
| Videos not yet produced | Video Placeholder |
| Transcript for any video | Video Transcript (expand/collapse below video) |
| Interactive exercises (linked separately) | Interactive Placeholder |

---

## Production Process

### Step 1: Read the content source document

Open the page's markdown file from `weekly_content/week[NN]/`. Read the full content and identify which components each section needs.

### Step 2: Set up the page wrapper

Start with the page wrapper div. Add an intro paragraph if the page has one.

### Step 3: Convert section by section

Work through the markdown content top to bottom. For each section:

1. Determine the right component (use the table above)
2. Copy the component HTML from this guide
3. Replace placeholder text with the actual content
4. Apply inline styles to any sub-elements (bold with `<strong>`, italic with `<em>`, links)

### Step 4: Handle special elements

- **[VIDEO: ...]** placeholders in the markdown become Video Placeholder, YouTube Video, or Canvas-Hosted Video components depending on the source
- **[INTERACTIVE: ...]** placeholders become Interactive Placeholder components
- **[CURATED LINK: ...]** blocks become Curated Link or YouTube Video components (use the selected option, not all listed)
- **[TEMPLATE: ...]** placeholders — use a Checklist Box or expand/collapse section depending on the template content
- **[LINKED RESOURCE: ...]** placeholders become Curated Link components pointing to the course material

### Step 5: Review in Canvas

Paste the HTML into Canvas Rich Content Editor (HTML view), save, and preview. Check:

- [ ] Page renders correctly with no broken styles
- [ ] All sections are properly closed (missing closing `</div>` tags break everything below them)
- [ ] Heading hierarchy is correct (h2 for section headers, h3 for subsections)
- [ ] Links open in new tabs (`target="_blank" rel="noopener"`)
- [ ] YouTube videos auto-embed as inline players
- [ ] Expand/collapse sections work and show the disclosure triangle
- [ ] Text is readable and properly spaced
- [ ] No horizontal scrolling on mobile (comparison columns may need testing)
- [ ] Video and interactive placeholders are clearly marked

---

## Common Patterns

### Full section with multiple sub-topics

```html
<div style="background: #ff7c0a; padding: 12px 18px; border-radius: 8px 8px 0 0; margin-top: 28px;">
  <h2 style="font-size: 16px; color: #050c2a; margin: 0;"><strong>Section Title</strong></h2>
</div>
<div style="border: 1px solid #e2e4e9; border-top: none; border-radius: 0 0 8px 8px; padding: 20px 24px; margin-bottom: 24px;">

  <h3 style="font-size: 16px; color: #050c2a; margin: 0 0 8px;"><strong>First Sub-topic</strong></h3>
  <p style="font-size: 14px; margin-bottom: 12px;">Content here.</p>

  <h3 style="font-size: 16px; color: #050c2a; margin: 24px 0 8px;"><strong>Second Sub-topic</strong></h3>
  <p style="font-size: 14px; margin-bottom: 12px;">Content here.</p>

  <div style="background: #f7f8fa; border-left: 4px solid #2454ff; padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 16px 0;">
    <div style="font-size: 12px; margin-bottom: 6px; color: #2454ff;">TIP</div>
    <p style="font-size: 14px; margin: 0;">A helpful callout within the section.</p>
  </div>

</div>
```

### Page with intro + video + sections

```html
<div style="font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #050c2a; line-height: 1.7; max-width: 800px;">

  <p style="font-size: 15px; margin-bottom: 16px;">Opening paragraph that frames the page.</p>

  <div style="background: #f7f8fa; border: 1px solid #e2e4e9; border-radius: 10px; padding: 20px 24px; margin: 20px 0;">
    <p style="font-size: 14px; color: #050c2a; margin-bottom: 4px;">Video Title</p>
    <p style="font-size: 13px; color: #6b7280; margin-bottom: 12px;">Source (duration). Brief description.</p>
    <a style="color: #2454ff;" href="https://youtu.be/VIDEO_ID" target="_blank" rel="noopener">https://youtu.be/VIDEO_ID</a>
  </div>

  <!-- Section 1 -->
  <div style="background: #ff7c0a; padding: 12px 18px; border-radius: 8px 8px 0 0; margin-top: 28px;">
    <h2 style="font-size: 16px; color: #050c2a; margin: 0;"><strong>Section One</strong></h2>
  </div>
  <div style="border: 1px solid #e2e4e9; border-top: none; border-radius: 0 0 8px 8px; padding: 20px 24px; margin-bottom: 24px;">
    <p style="font-size: 14px; margin-bottom: 12px;">Section content.</p>
  </div>

</div>
```

---

## Accessibility Checklist

These practices are built into the components above but worth verifying:

- **Semantic headings.** Section headers use `<h2>`, subsections use `<h3>`. This enables screen reader heading navigation.
- **Color contrast.** All text/background combos follow Riipen brand colorways which meet WCAG AA. Muted text uses `#6b7280` (not `#acacac`).
- **Link security.** All `target="_blank"` links include `rel="noopener"`.
- **Decorative emoji.** Wrapped in `<span aria-hidden="true">` so screen readers skip them. If Canvas strips `aria-hidden`, the fallback is acceptable.
- **Expand/collapse.** Native `<details>/<summary>` preserves the disclosure triangle for visual affordance and is announced by screen readers.
- **No color-only meaning.** Comparison columns use text labels ("Weak Example" / "Strong Example") alongside color backgrounds.

---

## Notes

- **DM Sans availability.** If DM Sans is not loaded in your Canvas instance, you may need to add a Google Fonts link in your Canvas theme settings, or accept the system font fallback. Check with your LMS administrator.
- **Mobile responsiveness.** Comparison columns (`display: flex`) may stack poorly on narrow screens. Test on mobile. If needed, use the stacked block alternative (see Component 11).
- **Emoji encoding.** Emoji are encoded as HTML entities (`&#127916;` for film clapper, `&#127919;` for bullseye, `&#128206;` for paperclip, `&#9744;` for checkbox) for maximum compatibility. They render natively in all modern browsers.
- **Closing tags.** The most common rendering bug is a missing `</div>`. Count your opening and closing tags before pasting. One missing close tag will break everything below it.
- **Canvas style stripping.** Canvas normalizes HTML when saving. It strips `font-weight`, `text-transform`, and `letter-spacing`. It lowercases hex colors. It removes `noreferrer` from `rel` attributes. All component templates in this guide account for this — do not add these stripped properties back.
