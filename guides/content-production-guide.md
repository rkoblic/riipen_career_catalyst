# Content Production Guide

How to produce content from a weekly development plan for Riipen Career Catalyst.

This document is a reference for generating learner-facing content. It assumes the development plan for the week already exists and specifies what to produce — this guide covers *how* to produce it.

---

## Inputs

Each content production session requires two inputs:

1. **The weekly development plan** (`week[NN]-development-plan.md`) — specifies the content pieces, sub-elements, production approaches, and word count targets
2. **The weekly design document** (`week[NN]-design-doc.md` in `weekly_design_docs/`) — the source material: activity descriptions, learning objectives, competency alignment, AI guidance, and deliverable specifications

The development plan tells you *what* to produce. The design doc tells you *what to say*.

---

## Output Structure

### Folder structure

```
weekly_development_plans/              ← internal, not shared with Riipen
├── content-development-plan-process.md
├── content-production-guide.md
├── week01-development-plan.md
├── week02-development-plan.md
└── ...

weekly_content/                        ← deliverable, shareable with Riipen
├── week01/
│   ├── page1-overview.md
│   ├── page1-overview-video.md
│   └── ...
├── week02/
│   ├── page1-overview.md
│   └── ...
└── ...
```

### File naming conventions

- **Week folders:** `week[NN]` — zero-padded (e.g., `week01`, `week15`)
- **Page files:** `page[N]-[short-title].md` — no week prefix (the folder provides it)
- **Video scripts:** `page[N]-[short-title]-video.md`
- **Future templates:** `page[N]-[short-title]-template.md`
- **Future interactive files:** `page[N]-[short-title]-interactive.html`
- **Short titles:** lowercase, hyphenated, 2–4 words max (e.g., `team-charter`, `using-ai-responsibly`, `communication-skills`)
- **Page numbers** match the development plan numbering (e.g., "### 3. Team Formation & Charter Anchor Prompt" → `page3-team-charter.md`)
- **Development plans:** `week[NN]-development-plan.md` — zero-padded, stored in `weekly_development_plans/`

**Example for Week 2:**
```
weekly_content/week02/
├── page1-overview.md
├── page1-overview-video.md
├── page2-using-ai-responsibly.md
├── page2-using-ai-responsibly-video.md
├── page3-team-charter.md
├── page4-outreach-email.md
├── page5-researching-an-organization.md
├── page6-communication-skills.md
└── page7-whats-next.md
```

### File metadata

Every content file and development plan includes YAML frontmatter for tracking.

**Content page files:**
```yaml
---
week: 2
page: 3
title: Team Formation & Charter
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: draft | review | final
competencies:
  - area: Teamwork
    subskill: Shared Accountability
  - area: Communication
    subskill: Professional Correspondence
---
```

The `competencies` field lists the NACE competency areas and subskills the page touches. These are used to render competency badges in the Canvas HTML version. Map competencies based on the design doc's competency alignment table. Pages that are purely logistical (e.g., a week overview with no skill-building content) can omit this field.

**Video script files:**
```yaml
---
week: 2
page: 3
title: Team Formation & Charter
type: video-script
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: draft | review | final
---
```

**Development plan files:**
```yaml
---
week: 2
title: Building Your Team
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
design_doc: week02-design-doc.md
---
```

### Page file structure

Each page file is a self-contained markdown document. Structure:

```markdown
---
[frontmatter]
---

# [Page Title]

[Opening — "why this matters" framing, 1–3 sentences. Front-load professional relevance.]

---

## [Section heading]

[Content]

[VIDEO: Title of video]

[CURATED LINK: Brief description of what the link covers]
- Option 1: [Title] — [URL] — [1-sentence rationale]
- Option 2: [Title] — [URL] — [1-sentence rationale]
- Option 3: [Title] — [URL] — [1-sentence rationale]

---

## [Next section heading]

[Content]
```

### Video script files

Plain narrator text only. No stage directions, no visual cues, no formatting beyond paragraph breaks. The script should be ready to copy and paste directly into Lumen5.

```markdown
# Video Script: [Title]

[Narrator text, paragraph by paragraph. Written to be heard, not read — short sentences, conversational rhythm, natural pauses between ideas.]
```

---

## Voice and Tone

**Who is speaking:** A smart mentor who respects your time. Warm, direct, professional. Someone who's been through this before and wants you to succeed — not a textbook, not a cheerleader.

**Person:** Second person ("you," "your team"). Never "students will..." or "learners should..." — always speak directly to the reader.

**Register:** Conversational but professional. Use contractions naturally. Avoid academic jargon unless it's a term learners need to learn (and then define it plainly). No filler phrases ("it's important to note that..."). Say it directly.

**Spelling:** American English throughout (per Riipen brand guidelines).

**Framing:** Professional relevance first, always. Open every section with *why a working professional would care about this* — not learning objectives, not course requirements. "In any consulting engagement, the first meeting sets the tone for the entire relationship" rather than "This module will help you prepare for the kickoff meeting." Highlight potential and possibility for growth, but don't overpromise. Never make lofty claims about career outcomes, guaranteed employer interest, or realized dreams. Frame things as opportunities, not assurances.

**Respect:** Assume learners are intelligent adults encountering professional contexts for the first time. Don't condescend. Don't over-explain what's obvious. Do explain what's genuinely new.

**Language to avoid:** No slang, idioms, or culturally specific expressions (per Riipen brand guidelines, these undermine accessibility for diverse, international learner populations). No emojis in course content (Riipen reserves emojis for social media only). Use exclamation marks sparingly — Riipen's brand is reliable, calm, and professional, not excitable.

**Avoid AI-sounding patterns.** Minimize em dashes; use commas, periods, or parentheses instead. Limit the "this isn't X, it's Y" construction. Avoid parallel triplets ("clear, concise, and compelling"). Watch for filler phrases that sound authoritative but say nothing ("It's worth noting that...", "The key here is..."). Read sentences aloud. If they sound like a chatbot wrote them, rewrite.

---

## Terminology and Brand Vocabulary

**"Learners," not "students":** Per Riipen brand guidelines, Career Catalyst uses "learners" (or "work-ready learners") when referring to participants. Do not use "students" in content. When speaking directly to the reader in second person ("you," "your team"), this distinction rarely surfaces — but when referring to participants in the third person or as a group, always use "learners."

**Preferred vocabulary (from Riipen brand guidelines):**
- Use: full potential, career readiness, career clarity, employable skills, real-work projects, grow/growth, fresh perspective, accessibility, equitable opportunities
- Avoid: experts, scholar, young talent, fully-subsidized

**Heading case:** All section headings in learner-facing content should use **sentence case** (capitalize only the first word and proper nouns), per Riipen brand guidelines. For example: "Preparing for the kickoff meeting" not "Preparing for the Kickoff Meeting."

---

## Content Principles (applied during production)

These principles are established in the development plan process. During content production, they translate into concrete writing rules:

1. **Front-load "Why This Matters."** Every section opens with professional relevance. The first sentence of any section should make a working professional nod, not make a learner groan. **Connect every activity to real-world practice.** When asking learners to do something, make clear that this isn't just a course exercise — show how working professionals do the same thing. A team charter isn't a school assignment; it's what consulting firms do at project kickoff. An outreach message isn't busywork; it's how you start every professional relationship. Learners should never wonder "why are we doing this?"

2. **Recommend, don't prescribe.** "We recommend debriefing immediately after the meeting while impressions are fresh" — not "You must complete your debrief within 30 minutes." Embed guidance in context rather than issuing mandates.

3. **Link, don't build for generic skills.** When a topic is a generic professional skill (email etiquette, time management, active listening), provide a brief framing sentence and a curated link. Reserve original text for course-specific material that can't be found elsewhere.

4. **Keep language evergreen.** Never reference specific week numbers in learner-facing content. Course structure may change, and content should not require updating when it does. Instead of "In Week 1, you learned email basics," write "You've already practiced professional email skills earlier in the course." Instead of "Next week's Direction Check," write "The upcoming Direction Check." Use relative time references ("earlier in the course," "in an upcoming session," "when you first formed your team") rather than absolute ones ("in Week 2").

5. **Avoid hardcoding course specifics.** Don't state specific team sizes, course durations, or structural details that may vary by cohort or partner. Write "your team" not "your team of four"; "the rest of the course" not "the next fifteen weeks." This is the same logic as the evergreen language rule, extended to course structure details that could change across implementations. **Platform specifics:** All employer communication and deliverable submissions happen through the Riipen platform. When referring to what learners actually send, use "message" and name the platform. When teaching the general professional skill (e.g., how to write professional correspondence), "email" is fine — the skill is transferable even though the delivery mechanism is Riipen.

6. **Content at the point of need.** Don't explain something learners won't use until later. If it's in this page, it should be useful *now* or within this week's activities.

7. **Varied media breaks up density.** Where the development plan specifies a video, place the `[VIDEO]` placeholder at the point where the video should appear — typically after the opening framing sentence or at the start of a new conceptual section. Videos are openers and motivators, not replacements for instructional text. **Videos must not duplicate the page text.** If the page covers logistics (what's due, what order), the video should cover motivation (why this matters, how the skills show up in real professional work). If the page teaches a concept, the video should frame why a professional would care — not re-explain the concept. Redundancy makes videos skippable. Every video should give learners a reason to press play that they can't get from skimming the page.

8. **Scannable over dense.** Use headers, bullet points, and short paragraphs. A learner should be able to skim a page and understand the structure before reading deeply. Long unbroken paragraphs are a sign that the content needs restructuring, not just editing.

9. **Vary examples across weeks.** When illustrating a concept with examples (professional roles, industries, scenarios), check what examples were used in previous weeks' content and use different ones. Repetition of the same examples (e.g., "a marketing manager drafts copy, a consultant synthesizes research") across multiple pages or weeks makes the course feel narrow and formulaic. Diverse examples across weeks signal that these skills apply broadly, expose learners to a wider range of professional contexts, and keep the content feeling fresh. Before writing examples, scan the content from the surrounding weeks for overlap.

10. **Surface the pedagogy.** When asking learners to do something, explain *why the course is designed that way* and how it benefits them. Don't just describe the activity — make the design logic visible. Why is this activity sequenced here and not later? Why is it completion-based instead of graded? Why does the course ask you to skim before deep-reading, or draft before using AI, or preview a template before your first meeting? Learners who understand the reasoning behind a course's structure are more motivated, less anxious, and more likely to engage meaningfully with activities that might otherwise feel like busywork. This doesn't mean citing research papers — a sentence or two of plain-language rationale is enough. "We ask you to review the syllabus early because learners who understand the full arc and expectations from day one manage their time and stress better across the semester" is the right register. The goal is transparency: learners should never have to wonder why they're doing something.

---

## AI Guidance Principles

When writing learner-facing AI guidance, follow these principles:

1. **AI for learning, primary sources for facts.** Encourage learners to use AI to understand unfamiliar domains: have a conversation, ask it to explain an industry, clarify terminology. For facts about specific organizations, people, or recent events, direct learners to primary sources (company websites, LinkedIn, news). Verification takes as long as just looking it up.

2. **Learner drafts first, AI refines.** Don't encourage learners to have AI generate first drafts. The professional habit we're building is: write it yourself, then use AI to polish tone, tighten language, or catch gaps. This keeps the learner's voice and thinking in the work.

3. **Provide example prompts only when introducing a new AI strategy.** If a page introduces a genuinely new prompting pattern (e.g., asking AI to argue against your position, using AI to synthesize across team members' notes), include an example prompt. If learners are applying a strategy they've already learned (e.g., giving context when prompting), let them do it themselves. Handing them a prompt for something they already know how to do undercuts the skill we're building.

4. **Disclosure follows the submission, not the tool.** AI disclosure requirements apply to course submissions and graded work. Don't tell learners to disclose AI use on individual emails or messages to employers. Nobody does that in professional practice.

5. **Always note the training data limitation.** When mentioning AI for research, flag that its knowledge has a cutoff date and may miss recent developments. This is especially relevant for organizational research where recency matters.

---

## How to Handle Each Production Type

### AI-generated text

Write original text following the voice, tone, and content principles above. Use the design doc's activity descriptions, notes, and competency alignment as source material — but rewrite everything for the learner audience. Never copy design doc language directly into learner-facing content; the design doc is written for curriculum designers, not learners.

**Word count targets** in the development plan are guidelines, not hard limits. Stay within ±20%. If a section naturally runs shorter because it says what it needs to say, that's fine. Don't pad.

### Curated links

For each curated link specified in the development plan, provide **three options** for the course designer to choose from. Each option should include:

- The title of the resource
- The URL
- A one-sentence rationale for why this option is a good fit

**Selection criteria for curated links:**
- **Authoritative source** — published by a recognized organization, institution, or established professional voice (e.g., Harvard Business Review, MindTools, a well-known professional development platform). Articles, YouTube videos, and short courses are all fair game. Avoid personal blogs, low-authority content farms, or paywalled academic journals.
- **Stable URL** — prefer institutional or organizational URLs that are unlikely to break. YouTube channels from established organizations or educators are fine. Avoid medium.com posts, LinkedIn articles, or other platforms where content can be deleted by the author.
- **Accessible** — no paywall, no login required, no aggressive pop-ups. Learners should be able to click and read immediately.
- **Appropriate length** — the curated link should fill the time budget noted in the development plan (typically 5–10 minutes of reading or viewing). A 30-minute video is too long; a 200-word blog post is too thin.
- **Evergreen** — avoid content tied to a specific year, trend cycle, or news event. Prefer timeless professional guidance over "Top 10 Tips for 2024."
- **Inclusive and professional** — no content that assumes a specific cultural context, uses exclusionary language, or adopts a tone inconsistent with the course's professional framing.

**Finding YouTube videos:** The AI web search tool does not have a video filter and struggles to surface specific YouTube URLs. When YouTube options are needed, use Google Video search directly (google.com → Videos tab) to find candidates, then add them to the options list. Flag any YouTube URLs that need manual verification with `REPLACE_WITH_ACTUAL_URL`.

In the page file, place a `[CURATED LINK]` block with the three options:

```markdown
[CURATED LINK: Topic description]
- Option 1: [Title] — [URL] — [rationale]
- Option 2: [Title] — [URL] — [rationale]
- Option 3: [Title] — [URL] — [rationale]
```

### Checklists

Format as a markdown checklist with clear, actionable items. Each item should be a concrete action, not a vague reminder.

```markdown
### [Checklist title]
- [ ] [Action item — specific and concrete]
- [ ] [Action item]
- [ ] [Action item]
```

### Video scripts

Write plain narrator text. No stage directions, no "[show graphic of...]", no formatting cues. Write to be heard — short sentences, conversational rhythm, natural pauses between ideas. Each paragraph is roughly one "slide" worth of narration in Lumen5.

**Target length:** ~120–150 words per minute of video. A 60–90 second video = ~120–200 words of narration.

Save as a separate file: `page[N]-[short-title]-video.md`

### Templates

*Not currently in scope for AI production. Skip any template items in the development plan.*

### Interactive elements

*Not currently in scope for AI production. Skip any interactive practice items in the development plan.*

---

## Using the Design Document

The design doc is your source material, not your script. Here's what to pull from it and how:

| Design doc section | How to use it |
|---|---|
| **Activity descriptions and notes** | Primary source for *what* to write about. Rewrite entirely for learners — the design doc describes activities for curriculum designers; you're writing for the learners doing them. |
| **Learning objectives** | Use as a background guide for what learners should walk away understanding. Don't reproduce them verbatim — they're written in assessment language, not learner language. |
| **Competency alignment** | Use to understand *why* an activity matters and what skill it develops. Translate into professional relevance framing ("This matters because..."), not competency labels. |
| **Deliverable connection** | Critical for anchor prompts — use the deliverable specs, completion criteria, and AI guidance directly. This is the most important section for assignment-type pages. |
| **AI in This Week** | Reproduce the guidance accurately but in learner-friendly language. What's permitted, what's off-limits, and what requires disclosure must be clear and precise. Don't soften or hedge the boundaries. |
| **Open Questions / Flags** | Be aware of these but don't reference them in learner-facing content. They may affect how you write certain sections (e.g., if a submission platform isn't confirmed, keep submission instructions generic). |

---

## Production Workflow

For each week:

1. **Read the development plan and design doc together.** Understand the week's architecture before writing anything.
2. **Produce pages in order.** Start with the Overview, then work through the content pieces as numbered. This ensures forward references are intentional.
3. **Write each page file completely** before moving to the next. Include all sub-elements specified in the development plan. Include YAML frontmatter with `week`, `page`, `title`, `created`, `last_updated`, and `status` fields.
4. **Write video scripts as separate files** as you encounter them in the page flow. Include YAML frontmatter with `type: video-script`.
5. **Search for curated links** where specified. Provide three options per link with rationales.
6. **Skip templates and interactive elements** — note them as `[TEMPLATE: description]` or `[INTERACTIVE: description]` placeholders in the page file.
7. **Review against word count targets.** Check each sub-element is within ±20% of the target. Flag any significant deviations.
8. **Update YAML metadata when modifying any file.** Always update `last_updated` to the current date when editing. Update `status` as the file progresses through `draft` → `review` → `final`.

---

## Quality Checks

Before considering a page complete:

- [ ] Every section opens with professional relevance, not a learning objective
- [ ] No specific week numbers appear in learner-facing text
- [ ] Voice is consistent — second person, warm, direct, no academic register
- [ ] American English spelling throughout
- [ ] No slang, idioms, or culturally specific expressions
- [ ] No emojis in course content
- [ ] Exclamation marks used sparingly (if at all)
- [ ] Section headings use sentence case
- [ ] Correct participant terminology used (see Terminology and Brand Vocabulary section)
- [ ] No overpromising — opportunities and growth, not guaranteed outcomes
- [ ] Curated links have three options each with rationales
- [ ] Video placeholders are positioned where specified in the development plan
- [ ] Word counts are within ±20% of targets
- [ ] AI guidance (what's permitted, what's off-limits, disclosure requirements) is accurate and unambiguous
- [ ] No design-doc language leaked into learner-facing content
- [ ] Content is scannable — headers, bullets, short paragraphs
- [ ] No content references something learners haven't encountered yet (unless flagged as a preview)
- [ ] YAML frontmatter is present with correct `week`, `page`, `title`, `created`, `last_updated`, and `status`
- [ ] If editing an existing file, `last_updated` has been changed to today's date
