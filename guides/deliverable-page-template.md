# Deliverable Page Template

This guide defines the canonical structure for any learner-facing page whose primary purpose is to explain a graded or completion-based deliverable. Use it when writing a new deliverable page, and reference it when reviewing existing ones.

## What this template governs (and doesn't)

**Governs:** Page-level structure for deliverable-explainer pages — which sections appear, in what order, with what standard headings, and which sections are required vs. conditional based on deliverable type.

**Does not govern:** Rubric content, framework content, the substance of what learners are producing. Those live in `rubrics/` (e.g., `rubrics/reflection-portfolio-framework.md`, `rubrics/context-analysis-rubric.md`) and are referenced from the page rather than restated.

This template is page scaffolding. Substance comes from the rubric, the framework, and the design doc.

---

## The four deliverable types

Every deliverable page falls into one of four types. The type determines which sections are required and how a few of them are phrased.

### Type A — Graded team deliverable, employer-shared
Produced by the team. Graded against a rubric. Auto-shared with the employer on submission and forms the basis of the next employer touchpoint.
Examples: W4 p2 Context Analysis & Project Plan, W13 p2 Project Deliverables, W15 p2 Final Presentation.

*Note on live deliverables (W15 p2):* a presentation is a Type A deliverable with two adjustments — the Submission section becomes "Format/logistics" (slides submitted in advance, presentation is live), and AI disclosure moves to the final slide of the deck rather than a written disclosure statement.

### Type B — Graded individual deliverable, recurring
Produced individually. Graded against a fixed rubric used across multiple instances. Not shared with employer or peers.
Examples: Reflections #1–5 (W3 p8, W6 p2, W9 p5, W12 p4, W15 p4).

Reflection content (DEAL framework, depth escalation, prompt design) is governed by `rubrics/reflection-portfolio-framework.md`. This template only governs the page-level scaffolding.

### Type C — Graded individual deliverable, instrument-based
Produced individually using a fixed instrument (e.g., BARS rating scales + qualitative prompts). Aggregated feedback may be shared back, but ratings stay confidential.
Examples: W8 p2 Mid-Project Peer Evaluation, W15 p5 End-of-Project Peer Evaluation.

### Type D — Completion-based team checkpoint, internal
Produced by the team. Verified for completion, not graded for quality. Not shared with the employer. Submitted to the platform for completion verification.
Examples: W7 p6 Work-in-Progress Summary, W9 p3 Draft Deliverable.

---

## Canonical page structure

Seven sections, in this order. Sections marked **Required** must appear on every page of the relevant type. Sections marked **Conditional** appear only when the rule next to them is true.

| # | Section | A | B | C | D |
|---|---|---|---|---|---|
| 1 | Opening framing (no H2) | Required | Required | Required | Required |
| 2 | What this is (and isn't) | Conditional | Conditional | Conditional | **Required** |
| 3 | The substance | Required | Required | Required | Required |
| 4 | How you'll be assessed | Required | Required | Required | — |
| 5 | How to do it well | Conditional | Conditional | Conditional | Conditional |
| 6 | Using AI | Required | Required | Required | Required |
| 7 | Submission | Required | Required | Required | Required |

The order matches what learners need: what is this → (clarify if needed) → what am I producing → how is it assessed → how do I do it well → AI rules → how do I submit.

### 1. Opening framing — Required (all types)

Sits directly under the H1, no H2 heading. Two or three short paragraphs that cover, in this order:

1. **Professional relevance.** What kind of work this deliverable mirrors in professional practice.
2. **Audience-and-use statement.** Who reads the submitted artifact and what it's used for. This is non-optional and must appear in the opening, not buried later. Phrasing per type:
   - **Type A:** "When you submit this, it's automatically shared with your employer and forms the basis of [next check-in name]."
   - **Type B:** "Individual submission, [X]% of grade as part of the Reflection Portfolio."
   - **Type C:** "Individual submission. Contributes to your peers' Professional Engagement grade. Your ratings are not shared back with teammates."
   - **Type D:** "Team submission, completion-based. Not graded for quality. Not shared with the employer."
3. **Type/grading statement** (if not already covered by #2). Required vs. optional, individual vs. team, graded vs. completion-based, weight or rubric reference.

The audience-and-use statement is the most common gap in existing pages. Always check that it's there.

### 2. What this is (and isn't) — Conditional

**Required for Type D.** Completion-based checkpoints have high misinterpretation risk: learners assume completion-based things are graded, or that internal documents go to the employer. Stating the boundaries explicitly prevents this.

**Optional for A/B/C** unless the deliverable has a misinterpretation risk the opening framing doesn't fully resolve. Use this section if learners might confuse this deliverable with another one in the course (e.g., Draft Deliverable vs. Project Deliverables, mid-project peer eval vs. end-of-project peer eval).

When used, the section name should be exactly **"What this is (and isn't)"** or **"What this checkpoint is (and isn't)"** for completion-based items.

### 3. The substance — Required (all types)

The body of the page. Section heading varies by type:

- **Type A:** "The [N] parts" (multi-part deliverable) or "What this submission is" (assembled package)
- **Type B:** "The prompt"
- **Type C:** "The assignment"
- **Type D:** "What goes in the [name]"

Substance is type-shaped. For Type A, walk through each part with a "Why this part exists" framing (per principle 11 in the content production guide). For Type B, give the prompt and connect it to the learner's prior reflection work. For Type C, walk through each component of the instrument. For Type D, walk through each section of the document and explain what the writing exercise is meant to surface.

### 4. How you'll be assessed — Required (A/B/C); omitted (D)

**Standard heading: "How you'll be assessed."** Deprecated alternatives: "Rubric dimensions," "What the rubric assesses," "Submission and grading."

Always includes:
- A rubric reference: `[LINKED RESOURCE: <Rubric Name>]` when the rubric exists.
- The dimensions, with weights when they differ.
- A short statement of what each dimension actually evaluates.

Use a markdown table when there are 4+ dimensions with distinct weights (matches the W13 pattern). Use a bulleted list when dimensions are equally weighted (matches the W3 / W4 pattern).

For Type B (reflections), the rubric is the same across all five instances. Reference it once per page; don't restate the framework that's already in `rubrics/reflection-portfolio-framework.md`.

### 5. How to do it well — Conditional

Skill-building or production guidance specific to the deliverable. Section heading varies by type:

- **Type A:** "How to produce this as a team" — covers individual research, team synthesis, drafting, async cross-review, integration pass, final sign-off. Always includes integration guidance for multi-author documents.
- **Type B:** "Choosing an anchor experience" / "Common pitfalls" / "What changes for [this reflection]" — depth-escalation guidance specific to which reflection in the portfolio.
- **Type C:** "What makes a [response/rating] specific" — weak/strong evidence examples that show learners what specificity looks like.
- **Type D:** "What the completion criteria require" — names what counts as completion vs. placeholder.

Skip this section when the substance section already covers production guidance inline (some Type A pages do this).

### 6. Using AI — Required (all types)

**Standard heading: "Using AI."** Deprecated alternatives: "AI guidance," "Using AI as a thinking partner," "AI in this deliverable."

Body always covers, in this order:
1. **What's permitted.** Specific use cases that fit the deliverable.
2. **What's off-limits.** What AI cannot do for this submission.
3. **Why the line is drawn there.** A one-line reason that connects to the assessment standard or the learning objective.

Disclosure requirement is mentioned in the Submission section (#7) by default, not here. If the AI guidance is long enough that learners might miss the disclosure note in Submission, add a one-line "**Disclosure required**" callout at the end of this section as well.

### 7. Submission — Required (all types)

**Standard heading: "Submission."** Deprecated alternatives: "Format and submission," "Submission and grading," "Submission logistics," "How to submit."

Always covers:
- **Format/length.** Page count or word range, file format if relevant.
- **Where to submit.** Riipen platform reference. Use `[PLATFORM: TBD — submission link]` if the platform path isn't confirmed yet.
- **Deadline/timing.** When it's due relative to other course events.
- **AI disclosure requirement.** One line: required regardless of whether AI was used; brief description if used, one-line statement if not.

Type-specific additions:
- **Type A:** Add a reminder that the document is automatically shared with the employer and forms the basis of the next check-in.
- **Type C:** Add a reminder that the evaluation is anonymized to teammates (or describe what's shared back).
- **Type D:** Add the late-submission consequence — since the artifact's purpose is meeting prep, late submissions cannot serve that purpose.
- **Live-presentation Type A (W15 p2):** Replace this section with "Format/logistics" — slides submitted in advance, presentation delivered live, AI disclosure on the final slide.

---

## Naming standards

A short reference for section heading wording. Use these exactly; deprecated alternatives are listed for retrofit reference.

| Section | Standard heading | Deprecated alternatives observed in current pages |
|---|---|---|
| Assessment | How you'll be assessed | Rubric dimensions; What the rubric assesses; Submission and grading |
| AI guidance | Using AI | AI guidance; Using AI as a thinking partner |
| Submission | Submission | Format and submission; Submission and grading; Submission logistics; How to submit |
| Boundary clarification | What this is (and isn't) | What this checkpoint is (and isn't) — acceptable when the deliverable is explicitly a checkpoint |

---

## Worked examples

### Type A example — Context Analysis & Project Plan

File: `weekly_content/week04/page2-context-analysis-and-project-plan.md`

Section list, mapped to the canonical structure:
1. **Opening framing** (under H1) — professional relevance + audience-and-use ("automatically shared with your employer; forms the basis of the Direction Check") + template callout.
2. *(What this is — not used; the opening is unambiguous)*
3. **The four parts** — substance: each part with "Why this section exists" framing.
4. **How you'll be assessed** — five dimensions equally weighted at 20% each, rubric linked.
5. **How to produce this as a team** — production workflow + integration pass.
6. **Using AI** — top-level H2 with "Getting oriented" and "Going deeper: prompting techniques" as sub-sections.
7. **Submission** — format/length, AI disclosure, employer-share reminder.

### Type D example — Work-in-Progress Summary

File: `weekly_content/week07/page6-work-in-progress-summary.md`

Section list, mapped:
1. **Opening framing** (under H1) — professional relevance ("teams write things down before meetings that matter") + audience-and-use ("not a document the employer reads"); team submission, completion-based.
2. **What this checkpoint is (and isn't)** — explicit boundary clarification (required for Type D).
3. **What goes in the summary** — substance: the four sections of the WIP, each with the team-internal reason it matters.
4. *(How you'll be assessed — omitted; Type D is completion-based)*
5. **What the completion criteria require** — production guidance.
6. **Using AI** — what's permitted, what's off-limits, and why the line is drawn there.
7. **Submission** — completion-based, late = useless.

---

## Where this fits with other guides

- **`guides/content-production-guide.md`** — overall voice/tone/format conventions for all learner-facing content. Principles 11 (explain "why" behind each deliverable section), 12 (frame deliverables as professional checkpoints), 13 (format-agnostic language), and 19 (required deliverables get their own findable page) inform this template directly.
- **`rubrics/`** — authoritative source for rubric content. The deliverable page links to the rubric; it does not restate it.
- **`rubrics/reflection-portfolio-framework.md`** — governs reflection content (DEAL framework, depth escalation, prompts). For Type B pages, this template only governs scaffolding; the framework governs everything else.
- **`guides/actual-content-map.md`** — current page-by-page state of weeks 1–9 after restructuring passes. Consult before retrofitting any existing page; the design docs have drifted.
- **Per-week `CHANGELOG.md`** — captures the *why* behind structural decisions on already-restructured weeks (currently 07, 08, 09). Read these before retrofitting pages in those weeks.

---

## Retrofit history

The initial retrofit pass against this template happened on 2026-04-28, alongside the template's creation. All 14 deliverable pages in `weekly_content/` were aligned at the section-naming and structural level:

- **Heading renames standardized** across all pages: "Format and submission" / "Submission and grading" / "Submission logistics" → "Submission"; "AI guidance" / "Using AI as a thinking partner" / variants → "Using AI"; "Rubric dimensions" / "What the rubric assesses" / "What you are being assessed on" → "How you'll be assessed".
- **Audience-and-use statements added** to the opening of Reflections #2, #3, #4 (the recurring reflections inherited their framing from Reflection #1 but didn't restate the portfolio context).
- **Structural moves:** W4 p2 had its AI guidance promoted from H3 subsections under "How to produce this as a team" to a top-level "## Using AI" H2. W8 p2 had "Submission and grading" split into separate "How you'll be assessed" and "Submission" sections, with "Using AI" reordered to sit before "Submission". W14 p4's inline `**Submission:**` line was promoted to a top-level "## Submission" H2.
- **Live-presentation variant (W15 p2):** kept its existing "Format/logistics" handling under "## The presentation" → "### The format" rather than introducing a separate Submission section. Only the assessment heading was renamed.

What the retrofit deliberately did NOT change: substance, section bodies, examples, internal logic, or the order of sections beyond the small cases noted above. Reflection content remains governed by `rubrics/reflection-portfolio-framework.md`.

Pages aligned: W3 p7, W4 p2, W6 p2, W7 p6, W8 p2, W9 p3, W9 p5, W12 p4, W13 p2, W14 p3, W14 p4, W15 p2, W15 p4, W15 p5.

### 2026-05-19 — Reflection #5 and End-of-Project Peer Evaluation moved to Week 15

Canonical deliverable pages for Reflection #5 and the End-of-Project Peer Evaluation moved from Week 14 to Week 15 to put the home page on the week the deliverable is due. Week 14 collapsed the prior two "begin this week, submit next week" pages (transfer-reflection-5 and end-of-project-peer-evaluation) into a single `page4-getting-a-head-start.md` that hyperlinks to the Week 15 pages as the source of truth and names the worth-doing-now prep moves (anchor selection for the reflection; evidence gathering across the arc for the peer evaluation). The What's Next page renumbered from W14 p6 → W14 p5. Substance pulled forward from the deleted Week 14 pages — the prompt and DEAL framework substance, the Transfer concept, the full-arc anchor scan and "what changed in how I work" guidance, and the BARS dimensions / mid-vs-end comparison / "evaluating contributions that evolved" framing. Both pages now include a Recommended workflow across the two weeks section to keep the early-start affordance visible from the canonical home.

Pages affected: W14 p4 (new head-start page replacing two pages), W14 p5 (renumbered from p6), W15 p4 (Reflection #5, was page4-reflection-5-finalize.md → page4-reflection-5.md), W15 p5 (End-of-Project Peer Evaluation, was page5-peer-evaluation-finalize.md → page5-end-of-project-peer-evaluation.md). Video script `page4-transfer-reflection-5-video.md` moved from W14 to W15.
