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

### Overview page structure

Every week starts with an overview page (`page1-overview.md`). Overview pages are structural, not instructional — they orient the learner to the week, not teach skills. Use this standard structure:

```markdown
---
week: [N]
page: 1
title: Week Overview
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: draft
---

# [Thematic title]

[1–2 paragraphs framing the week: what's happening, why it matters
professionally, how it connects to what came before.]

[VIDEO: Title]

---

## What's due this week

[List deliverables. Use a numbered list if there are multiple
deliverables; a single bold line if there's only one. For each,
include format (team/individual), grading status (completion-based
or graded with weight).]

---

## Suggested order of completion

[Numbered list. Walk through the week in the order that makes the
most sense pedagogically. Include brief rationale where the ordering
isn't obvious.]

---

## [Optional: week-specific section]

[Only if the week has something unique that belongs on the overview
— e.g., "Introduce yourself" in Week 1, "What 'done' looks like"
in a production week. Don't force a section if there's nothing to
say.]
```

**Overview page rules:**
- **No `competencies` field** — overview pages are structural, not instructional.
- **H1 is a thematic title**, never "Week N overview." It should capture the week's focus in a phrase (e.g., "From research to strategy," "Understanding your client," "Building your team").
- **"What's due this week"** and **"Suggested order of completion"** are the two standard H2 sections. Use these exact headings for consistency.
- **Suggested order always uses a numbered list** — sequence matters, so use numbers, not bullets.
- **VIDEO placeholder** goes after the opening paragraphs, before the first H2.
- **All headings in sentence case** (consistent with the rest of the course).

### What's next page structure

Every week ends with a "What's next" page. See [whats-next-page-guide.md](./whats-next-page-guide.md) for the canonical structure, template, prose-style rules, cross-week-arc checklist, worked examples, and per-week audit.

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

**Register:** Conversational but professional. Use contractions naturally. Avoid academic jargon unless it's a term learners need to learn (and then define it plainly on the spot). When a formal term appears in a section heading or deliverable part name, open with a one-line plain-language translation: "Strategic implications is a formal way of saying: based on what you found, what do you recommend, and why?" Don't assume learners know what terms like "synthesis," "stakeholder mapping," or "strategic implications" mean just because the design doc uses them. No filler phrases ("it's important to note that..."). Say it directly.

**Spelling:** American English throughout (per Riipen brand guidelines).

**Framing:** Professional relevance first, always. Open every section with *why a working professional would care about this* — not learning objectives, not course requirements. "In any consulting engagement, the first meeting sets the tone for the entire relationship" rather than "This module will help you prepare for the kickoff meeting." Highlight potential and possibility for growth, but don't overpromise. Never make lofty claims about career outcomes, guaranteed employer interest, or realized dreams. Frame things as opportunities, not assurances.

**Respect:** Assume learners are intelligent adults encountering professional contexts for the first time. Don't condescend. Don't over-explain what's obvious. Do explain what's genuinely new.

**Language to avoid:** No slang, idioms, or culturally specific expressions (per Riipen brand guidelines, these undermine accessibility for diverse, international learner populations). No emojis in course content (Riipen reserves emojis for social media only). Use exclamation marks sparingly — Riipen's brand is reliable, calm, and professional, not excitable.

**Avoid AI-sounding patterns.** This is the most common quality issue in produced content. Scrub for it explicitly during review.

- **Minimize em dashes.** Use commas, periods, parentheses, or sentence breaks instead. They're especially bad in video scripts, where they're hard to deliver verbally.
- **Limit "this isn't X, it's Y" constructions** and their variants ("not X — Y"; "X isn't Y. It's Z."; "That's not X — it's Y."). They sound rhetorical and add up fast.
- **Avoid parallel triplets** ("clear, concise, and compelling") and pithy aphorisms ("If everything is called out, nothing is."; "The friction is the point."; "Readers don't experience a team; they experience a document.").
- **Avoid "the place where Y lives"** type metaphors and "What replaces it is..." formal constructions.
- **Watch for filler phrases** that sound authoritative but say nothing ("It's worth noting that...", "The key here is...").
- **Avoid extreme or hyperbolic language.** Soften absolute claims. Use "tends to," "often," or "in most cases" instead of "always" or "never." Avoid sweeping statements like "before a reader engages with a single idea" or "the most important conversation of the year." If the prose gets dramatic, it's probably less accurate too.
- **Don't open with failure modes.** Lead with what the work looks like in practice, or with what success looks like — not with how things will go wrong if learners ignore the advice. "Most professional projects include a moment like this..." invites the learner in; "Multi-week documents fail in a predictable way..." warns them off. The failure mode can come later as a contrast, not as the opener.

Read sentences aloud during review. If they sound like a chatbot wrote them, rewrite.

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

7. **Varied media breaks up density.** Where the development plan specifies a video, place the `[VIDEO]` placeholder at the point where the video should appear — typically after the opening framing sentence or at the start of a new conceptual section. **Videos must not duplicate the page text.** There are two models for how videos and page text should relate:

   - **Overview videos** (page 1 of each week): The page covers logistics (what's due, what order). The video covers motivation and professional relevance (why this matters, how the skills show up in real work). Neither duplicates the other. See `guides/overview-video-guide.md` for the full guide on writing overview video scripts, including common patterns to avoid.
   - **Instructional videos** (concept-teaching pages): The video is the primary teaching vehicle — it teaches the concept with concrete examples. The page text becomes a scannable bulleted recap learners can reference while they work. Don't write the same explanation twice in two formats. See `guides/instructional-video-guide.md` for the full guide on writing instructional video scripts, including when to use the video-as-primary-teaching-vehicle pattern and how to restructure page text around it.

   In both models, every video should give learners a reason to press play that they can't get from skimming the page. Redundancy makes videos skippable.

8. **Scannable over dense.** Use headers, bullet points, and short paragraphs. A learner should be able to skim a page and understand the structure before reading deeply. Long unbroken paragraphs are a sign that the content needs restructuring, not just editing.

9. **Vary examples across weeks.** When illustrating a concept with examples (professional roles, industries, scenarios), check what examples were used in previous weeks' content and use different ones. Repetition of the same examples (e.g., "a marketing manager drafts copy, a consultant synthesizes research") across multiple pages or weeks makes the course feel narrow and formulaic. Diverse examples across weeks signal that these skills apply broadly, expose learners to a wider range of professional contexts, and keep the content feeling fresh. Before writing examples, scan the content from the surrounding weeks for overlap.

   **Running examples within a week:** When a week's guidance varies by project type (e.g., what "research" means for a marketing plan vs. a community engagement strategy vs. a process improvement project), choose 2–3 plausible, diverse project types and use them as running examples across that week's pages. Introduce the examples on a framing page, then use them consistently in subsequent pages and video scripts. This helps learners see how the same analytical framework applies to their specific project. Not every section needs all three examples — use whichever are most illustrative for that particular concept.

10. **Surface the pedagogy.** When asking learners to do something, explain *why the course is designed that way* and how it benefits them. Don't just describe the activity — make the design logic visible. Why is this activity sequenced here and not later? Why is it completion-based instead of graded? Why does the course ask you to skim before deep-reading, or draft before using AI, or preview a template before your first meeting? Learners who understand the reasoning behind a course's structure are more motivated, less anxious, and more likely to engage meaningfully with activities that might otherwise feel like busywork. This doesn't mean citing research papers — a sentence or two of plain-language rationale is enough. "We ask you to review the syllabus early because learners who understand the full arc and expectations from day one manage their time and stress better across the semester" is the right register. The goal is transparency: learners should never have to wonder why they're doing something.

11. **Explain the "why" behind every deliverable section.** For graded deliverables with multiple parts, each part should open with a "Why this section exists" explanation that connects to the employer's perspective and professional practice. Don't just tell learners what goes in each section — tell them what it accomplishes and why the employer cares about it. Frame it from the reader's perspective: "This section answers a question the employer can't help but have: does this team actually understand what we do and what we need?" This is especially important for deliverables where the connection between the section and its professional purpose isn't obvious.

12. **Connect deliverables to professional gates and checkpoints.** When introducing a graded deliverable, frame it as the kind of checkpoint that exists in real professional work — not as a course requirement. Client check-ins, direction reviews, progress gates, and alignment meetings are standard professional practice. Learners should understand that the deliverable mirrors something they'd do in any consulting, agency, or project-based role, and that the employer meeting that follows is the accountability mechanism, not the grade.

13. **Write format-agnostic where possible.** Riipen projects produce a wide range of deliverables: research reports, content strategies, presentation decks, campaign briefs, process maps, prototypes, training modules, and mixed-format packages. Don't assume "document" when describing team production work. Use "deliverable," "workspace," "piece," or "component" when a principle applies regardless of format. When examples help, span formats ("sections of a report, slides of a deck, scenes of a video, screens of a prototype"). Where content is genuinely written-deliverable-specific, say so explicitly so learners producing other formats can adapt or skip it.

14. **Reference earlier work, don't re-teach it.** When a framework, concept, or process was introduced earlier in the course (DEAL, a rubric, a tool, a methodology), point learners back to where they first encountered it instead of re-teaching the basics. The second encounter should focus on what's *different* this time: the experience pool they're drawing from, the expectations that have shifted, the new application. This respects learner time and reinforces the developmental arc of the course.

15. **Align with course documentation and frameworks.** Several documents in this project are authoritative sources for specific elements: the reflection portfolio framework (`rubrics/reflection-portfolio-framework.md`), the rubrics for graded deliverables, the AI arc, and the employer touchpoint arc. When writing content for a recurring course element, check the relevant framework first and align the page with what's documented there: experiential pool, secondary competencies, framing prompts, calibration notes. The framework is the source of truth; the page is the application. If the page and the framework conflict, fix the page (or flag the framework if it's the framework that needs updating).

16. **Explain course-specific terms; don't assume them.** Terms like "team sync," "Direction Check," "Development Check-In #1," and "Work-in-Progress presentation" are specific to this course. Learners may not know what they mean. Explain them in plain language on first use, and frame scheduled course elements as suggestions with context built in: "We strongly encourage you to find time to get together as a team this week. There's a team sync built into the time allocation for Week 6 specifically to make space for this." Don't write as if the learner is already inside the course's vocabulary.

17. **Walk the logical arc; check for missing steps.** When teaching a process, walk through it from the learner's perspective. Where does the action actually start? What decision do they need to make first? What happens before the thing the page is teaching? A common gap: pages that jump straight to execution without covering the planning or organizing conversation that should precede it. If the page assumes a step that hasn't happened yet, name and describe that step first.

18. **Hyperlink tools consistently.** When a tool, resource, or external reference is mentioned in learner-facing content, link the first mention with a markdown link in the form `[**Tool name**](URL)`. Drop bare-text URLs in parentheses; the link does the same work without the visual clutter. Subsequent mentions of the same tool can stay unlinked plain text. For tools with distinct subpages worth pointing at separately (e.g., Canva's general site vs. its chart templates), each subpage URL gets its own link the first time it appears.

19. **Required deliverables and checkpoints get their own findable page, and follow the structure in [`guides/deliverable-page-template.md`](deliverable-page-template.md).** When a week has a graded deliverable, a required checkpoint, or another mandatory student action, give it its own page with a clear title and a "What this checkpoint is (and isn't)" section up front. Don't tuck required submissions inside a meeting-prep or context-setting page where they'll be missed. A learner scanning for "what do I actually have to do this week?" should find each requirement unmissable. The deliverable page template defines the canonical section order, naming standards, and which sections are required vs. conditional based on deliverable type (graded team / graded individual / instrument-based / completion-based). Reusable concepts (e.g., a feedback reception protocol) that apply in multiple contexts across the course also earn their own findable page rather than living buried inside the page where they first come up.

20. **Watch for guidance that's too definitive when the real answer has exceptions.** When a page gives a strong directional rule (cut hedge language, lead with the recommendation, write in active voice), check whether learners also need to know where that rule stops applying. The fix isn't to soften the original advice — it's to surface the exceptions explicitly so learners can distinguish the default case from edge cases. Stated as a blanket rule, "cut all hedges" pushes learners to overstate findings; paired with "and here's when hedging is the right call," it teaches judgment instead of compliance.

21. **On human and interpersonal advice, draw on real workplace experience.** Anywhere a page is coaching a human interaction — giving feedback, receiving it, navigating a meeting, managing a tense moment — AI tends to miss the softer texture of how those things actually play out at work. Read your draft as if you were the learner about to follow it in a real workplace. Would the advice land the way you'd want it to? Does the example dialogue sound like something a person would actually say? Blunt-but-technically-correct guidance is a common failure mode here. Reframe verdicts as conversation openers: questions instead of declarations ("Is there any data that would support this directly?"), reader-perspective framings ("I'm not following how this connects…" rather than "this isn't connected"), and acknowledgments of the choice behind the work before suggesting a change. Feedback is often subjective, and language that opens a conversation is more accurate, not just softer.

22. **Check that each page connects to what's actually happening for learners that week.** Step back and ask: in this specific week, what is the learner *doing*, what feedback or conversations are coming at them, and what work is in front of them? Does each page meet learners at that moment? A page on receiving feedback in a week where learners are getting feedback from two directions (employer in a meeting, teammates in document comments) needs to address both. A page that only covers half of what's actually happening this week leaves learners on their own for the other half. The week's design doc, employer touchpoint arc, and the surrounding pages should all inform what each individual page covers.

---

## AI Guidance Principles

**Before writing any AI-related content, consult `guides/ai-arc.md`.** The AI arc document maps every AI skill, prompt strategy, and literacy topic across the 15-week course. Use it to:
- Check what AI concepts learners have already encountered (don't re-teach what's been covered)
- Identify what's new this week (introduce it properly, don't assume learners know it)
- Ensure prompt strategies build on what came before (don't hand learners a prompt for a technique they haven't learned yet)
- Verify that the accountability mechanism for this week's AI use is clear

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
- **Authoritative source** — published by a recognized organization, institution, or established professional voice (e.g., TED, MindTools, Duarte, Presentation Zen, Toastmasters, a well-known professional development platform). Articles, YouTube videos, and short courses are all fair game. Avoid personal blogs, low-authority content farms, or paywalled academic journals.
- **Stable URL** — prefer institutional or organizational URLs that are unlikely to break. YouTube channels from established organizations or educators are fine. Avoid medium.com posts, LinkedIn articles, or other platforms where content can be deleted by the author.
- **Accessible** — no paywall, no login required, no aggressive pop-ups. Learners should be able to click and read immediately. **Harvard Business Review (hbr.org) is paywalled and should not be used**, even when the content is a strong thematic fit.
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

**Once a link is selected,** convert to the finalized inline format with a brief description of what the learner will get from it:

```markdown
[CURATED LINK: "Title" (format, ~duration) — Source — URL] One or two sentences explaining what the resource covers and why it's relevant to the work learners are doing.
```

For example:
```markdown
[CURATED LINK: "The Pyramid Principle" (video, ~10 min) — Communicate with IMPACT — https://youtu.be/example] This video walks through McKinsey's Pyramid Principle — a framework for structuring any argument or analysis. Directly relevant to structuring your research findings section.
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

**Voice:** Second person ("you," "your team"), same as page text. Never use first person ("I," "me," "let me show you"). The narrator is not a character — they're a voice guiding the learner. "Here's what that looks like" not "Let me walk you through this."

**Keep framing tight.** The opening (before examples or core content) and closing (after) should be as concise as possible. Get to the substance quickly. If the opening takes more than 2–3 sentences to set up the concept, it's too long. If the closing restates points the examples already made, cut it down. The examples and core content are what earn the video its runtime — the framing around them should be minimal.

**Target length:** ~120–150 words per minute of video. A 60–90 second video = ~120–200 words of narration. Instructional videos that walk through multiple examples may run longer (2–3 minutes / ~300–450 words).

**Two types of video scripts:**

- **Motivational/framing videos** (typically page 1 overviews): Short (~60–90 sec). Set up why the week's work matters professionally. Don't repeat what the page text says.
- **Instructional videos** (concept-teaching pages): The primary teaching vehicle for that concept. Walk through concrete examples — ideally using the week's running project types — to show the concept in action. The companion page text should be a scannable recap, not a restatement. These may be longer than overview videos.

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

1. **Read the development plan, design doc, AI arc, and employer touchpoint arc together.** Understand the week's architecture before writing anything. Check `guides/ai-arc.md` for what AI skills have been introduced in prior weeks, what's new this week, and what the accountability mechanism is. Check `guides/employer-touchpoint-arc.md` for how this week's employer touchpoint (if any) should be framed, what makes it distinct from previous meetings, and whether it's a presentation, working session, or document review.
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
- [ ] Academic or professional jargon is defined in plain language where it first appears
- [ ] Graded deliverable sections each explain *why they exist* from the employer/professional perspective
- [ ] Content is scannable — headers, bullets, short paragraphs (cluster long lists under bold subheaders)
- [ ] No content references something learners haven't encountered yet (unless flagged as a preview)
- [ ] AI-isms scrubbed: em dashes minimized, no "X isn't Y, it's Z" patterns, no aphorisms or filler phrases (read aloud)
- [ ] Language is not hyperbolic or absolute where "tends to" or "often" would be more accurate
- [ ] Content does not open with a failure mode or a warning about how things will go wrong
- [ ] Language is format-agnostic where the deliverable type isn't fixed (or marked as written-specific where appropriate)
- [ ] Course-specific terms (team sync, Direction Check, etc.) are explained in plain language on first use
- [ ] Recurring frameworks (DEAL, rubrics) are referenced rather than re-taught when learners have encountered them before
- [ ] Required deliverables and checkpoints have their own dedicated page (not buried inside a meeting-prep or context-setting page)
- [ ] Strong directional rules either have no real exceptions or surface the exceptions explicitly
- [ ] Pages coaching human interactions read like advice that would actually land in a real workplace
- [ ] The page connects to what learners are actually doing and receiving this specific week (not just what the page is about in isolation)
- [ ] Content for recurring course elements aligns with the relevant rubric or framework document (`rubrics/`)
- [ ] First mention of each external tool is hyperlinked; bare-text URLs removed
- [ ] Accessibility basics covered where relevant: real heading styles, color isn't the only signal, descriptive link text, captions on video
- [ ] YAML frontmatter is present with correct `week`, `page`, `title`, `created`, `last_updated`, and `status`
- [ ] If editing an existing file, `last_updated` has been changed to today's date
