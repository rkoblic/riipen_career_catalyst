# What's-Next Page Guide

This guide defines the canonical structure for the "What's next" page that closes every week of the course. Use it when writing a new what's-next page, and reference it when reviewing existing ones.

## What this guide governs (and doesn't)

**Governs:** Page-level structure for the bridging page that always sits last in the week — opening framing, the milestone H2, the prep H2, when a third H2 is permitted, prose voice, length, link conventions, and which cross-week threads the page should consciously surface.

**Does not govern:** The substance of what's coming next. Detail about the milestone itself lives on the deliverable page, the employer-touchpoint page, or the next week's overview. The what's-next page is a bridge — it names the milestone and frames the transition; it does not re-explain the milestone.

This page is structural scaffolding. It does not have a `competencies` field.

---

## Canonical structure at a glance

The dominant pattern, used by ~9 of 14 existing pages:

1. **Opening framing** (no H2) — 1–2 sentences connecting what was just completed to what's coming.
2. **`## The [specific next milestone]`** — 2–4 short paragraphs: what it is, why it matters, what's different from prior touchpoints.
3. **`## How to prepare`** — 4–10 bulleted action steps, second person, verb-first.

**Permitted variants** (each is documented below in *Section-by-section guidance* and *Worked examples*):
- 3-H2 thematic add-on — when a running artifact, rubric, or upcoming reflection prompt warrants its own preview alongside the milestone.
- Terminal-week status checklist — when prep already happened earlier in the course and the section is reporting status, not assigning work.
- Optional / skippable event — when the next event may not happen and the page coaches the call.
- Foundation-laying (Week 1 only) — longer, more reflective, includes external resource. First-week setup is a different beat than the rest of the course.
- Celebration / pause — pre-final-presentation week. Acknowledges the team finished the deliverable and adds a "take a beat" note before the closing arc opens.

---

## Frontmatter rules

```
---
week: [N]
page: [last page in the week]
title: What's Next
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: draft
---
```

- No `competencies` field — this is a structural page, not an instructional one.
- `title: What's Next` is title-cased in frontmatter; the H1 is sentence case ("What's next").
- `page` is always the last page number in the week, after content pages and any reflection.

---

## Template skeleton

```markdown
---
week: [N]
page: [last]
title: What's Next
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: draft
---

# What's next

[1–2 sentences connecting what was just completed to what's
coming. Frame the transition, not the logistics.]

---

## [Name of the next major milestone or event]

[What it is, why it matters, what the learner should expect.
2–4 short paragraphs. Distinguish from prior touchpoints when
the milestone is part of a sequence.]

---

## How to prepare

- **[Verb-first action.]** [One or two sentences explaining the why.]
- **[Verb-first action.]** [...]
- [4–10 bullets total. Skip the section if there is genuinely
  nothing to prepare.]
```

---

## Prose-style rules

- **H1 is always "What's next."** Never varies. Sentence case.
- **First H2 names the milestone specifically** — "The Direction Check," "The near-final package," "The Final Presentation." Not generic ("What's coming," "Looking ahead").
- **Sentence case** for all headings.
- **Second person** throughout. "You," "your team," "your work."
- **Past + future framing in the opening.** What just happened, what's coming next.
- **Evergreen language.** No "Week N" references in learner copy. Use "next week," "in the upcoming weeks," "later in the course."
- **Target length: 250–450 words. Hard ceiling: 500.** Week 1 is the documented exception (foundation-laying — see worked examples).
- **No video placeholders.** What's-next pages do not have video.
- **No emoji.**
- **Bullets only for genuinely list-shaped prep.** If the prep is one connected idea, use a paragraph.
- **One external link maximum** (see Curated-link rules below).

---

## Section-by-section guidance

### Opening framing (no H2)

Two or three sentences. Cover, in this order:
1. What the team just finished or is finishing this week.
2. The transition — what kind of work or moment comes next.

Frame the transition, not the logistics. "You've just heard from the employer about where the work stands. The project now enters its final production push." — not "Next week is Week 9 and you'll have a check-in meeting on Tuesday."

### First H2: the milestone

Always present. 2–4 short paragraphs. Cover:
- **What it is.** A one-sentence working definition.
- **Why it matters.** The professional analogue or the learning purpose.
- **What's different.** When the milestone is part of a recurring sequence (employer touchpoints, reflections, deliverables), name how this instance differs from the prior one. The Check-In #1 page should not read like the Direction Check page.
- **What success looks like.** Optional. A short line on what a strong version of this milestone produces.

Do not re-explain the milestone in detail. The milestone has its own page. The what's-next page sets up that page.

### Second H2: "How to prepare"

Default heading. Use it unless a permitted variant clearly applies (terminal-week status; optional event).

Format:
- 4–10 bullets.
- Each bullet starts with a bolded verb-first phrase, followed by a sentence or two of context.
- Second person, imperative mood.
- Concrete: "Review the rubric," "Assign ownership for each revision," "Confirm presentation logistics."
- Skip the section entirely if there is genuinely nothing to prepare. Do not pad.

### Third H2 (permitted, not default)

Add a third H2 only when one of the following warrants its own preview alongside the milestone:
- A **running artifact** (Change Log, Team Charter, processing agreement) is about to do significant work and needs visible attention. W9's "The Change Log" is the model.
- A **rubric** that hasn't been seen before (or hasn't been revisited) needs surfacing. W10's "Revisit the Final Deliverables rubric" is the model.
- An **upcoming reflection prompt** has thematic stakes worth previewing. W11's "Reflection #4 is coming" is the model.

Three is the ceiling. If a fourth section seems necessary, the page is doing too much — push some of it back to the milestone's own page.

### Departing from "How to prepare"

Two cases justify a different second-H2 heading:

- **Status checklist for terminal weeks.** When prep has happened across earlier weeks and the section is reporting completion status (W14: "How to enter the final week"). Bullets are status statements, not action items.
- **Optional / skippable event.** When the next event may not happen, the section coaches the call and includes any artifact the learner needs to handle the skip professionally (W12: "Your biweekly check-in," with a sample cancellation message).

Document the reason in a one-line author comment in the page if the variant is unusual for the surrounding weeks.

---

## Curated-link rules

- **Prefer in-course links.** Page-to-page links, links to deliverable pages, links to rubrics. The what's-next page should mostly point inward.
- **One external link maximum**, and only when the resource is not yet in-course and the learner needs it before the next milestone. W2's link to a kickoff-meeting resource is the exemplar.
- **Use descriptive link text.** Never bare URLs.
- **First mention format:** `[**Resource Name**](URL)` for tools and resources; `[CURATED LINK: "Title" — Source — URL]` for the standard curated-link format used elsewhere in the course.

---

## Cross-week-arc surfacing checklist

Run this checklist before publishing. Each item asks whether a course-wide thread is alive in the next week. If yes, the what's-next page should surface it briefly — usually one bullet in the prep section, sometimes its own H2 (see *Third H2 permitted*).

- **Employer touchpoint coming?** Name it specifically. Distinguish working-meetings (the team drives, brings questions) from document-review meetings (the employer pre-reads). The full sequence: Kickoff (W3) → Direction Check (W5) → Check-In #1 (W7) → Check-In #2 (W9) → Near-Final document review (W11) → Final Presentation (W14/15).
- **Deliverable due?** Link the rubric. Deliverable checkpoints: W4 Context Analysis, W7 WIP Summary, W8 Mid-Project Peer Eval, W9 Draft, W11 Near-Final, W13 Final Deliverables, W15 Final Presentation.
- **Reflection coming up?** Preview the prompt theme in one or two sentences. W11's "Reflection #4 is coming" is the model. Reflections fall in W3 (#1), W6 (#2), W9 (#3), W11/12 (#4), W14/15 (#5).
- **Running artifact in play?** Mention the next time the learner touches it. Artifacts: Your Starting Point intake (W1), Team Charter (W2), Change Log (W6 onward), team processing agreement (W9 onward).

The AI arc is intentionally not surfaced on what's-next pages. AI framing for next week lives in next week's overview, not in the bridge.

---

## Worked examples

### Dominant pattern — `weekly_content/week03/page9-whats-next.md`

- 241 words, two H2 sections.
- Opening: one sentence naming the next deliverable, one sentence framing the synthesis it asks for.
- `## The Context Analysis & Project Plan` — links the just-finished Kickoff Summary to the upcoming deliverable; describes what teams arriving prepared vs. unprepared experience.
- `## How to prepare` — short. Asks the learner to review the assignment description and rubric, with the rubric linked.

Why it works: the page does one thing — name the next deliverable, link the rubric, set expectations. It does not re-explain the deliverable; the W4 page2 deliverable page does that.

### 3-H2 thematic add-on — `weekly_content/week09/page6-whats-next.md`

- 442 words, three H2 sections.
- `## The near-final package` — distinguishes the upcoming document-review meeting from the working-session check-in just held.
- `## The Change Log` — earned its own H2 because the Change Log moves from "running record" to "the artifact the employer will see referenced in the document review." Worth the structural attention.
- `## How to prepare` — three bullets: act on feedback, assign ownership, keep the log current.

Why it works: the third H2 is justified by the cross-week arc. The Change Log has been running since the Direction Check (W5) and is about to become load-bearing for W11's review. A bullet alone wouldn't carry it.

### Terminal-week status checklist — `weekly_content/week14/page5-whats-next.md`

- 289 words, two H2 sections.
- Opening: "This week was translation. Next week is delivery."
- `## The Final Presentation` — names the live Q&A standard the upcoming week tests.
- `## How to enter the final week` — five status statements (Outline submitted, deck rehearsed, Reflection #5 in draft, Peer Eval underway, logistics confirmed). The bullets are status, not action.

Why it works: by Week 14, prep has already happened. The status format honors that and gives the learner a quick "am I ready?" pass without inventing busywork.

### Foundation-laying outlier — `weekly_content/week01/page9-whats-next.md`

- 765 words, two H2 sections, one curated external resource.
- The first-week page does more setup work than other what's-next pages: it walks through the Team Charter's components, links a curated reading on team norms, and uses reflective questions instead of action bullets.

Why this is allowed: Week 1 is the only week where the learner has no prior team experience inside the course to draw on. The longer foundation-laying form is a one-time exception, not a precedent. No subsequent week should hit 700+ words on its what's-next page.

### Celebration / pause variant — `weekly_content/week13/page4-whats-next.md`

- 304 words, two H2 sections.
- `## The Final Presentation` — names the Refinement→Integration phase shift; sets expectations for the upcoming week.
- `## How to prepare` — five bullets, ending with **"Take a beat before the next phase starts. Submission is a real accomplishment. Rest, appreciate what your team built, and come back ready for the presentation work in the coming week."**

Why this is allowed: the team has just submitted the Final Deliverables. The celebration / pause beat is a deliberate emotional acknowledgment before the closing arc opens. This variant is reserved for this week — it is not a general-purpose option.

---

## Per-week audit (2026-04-28)

Initial audit performed alongside the creation of this guide. Action vocabulary: `keep` (matches dominant pattern, no edits) · `copy-edit` (small changes, no structural move) · `restructure` (section-level rewrite) · `intentional variant` (departs from dominant pattern with documented justification).

| Week | Page | Words | Current shape | Action | Notes |
|---|---|---|---|---|---|
| 1 | page9 | 765 | 2 H2, reflective questions, external link | `intentional variant` | Foundation-laying outlier. Documented as a worked example above. First-week-only exception. |
| 2 | page8 | 288 | 2 H2 + external link | `keep` | Exemplar for the permitted external-link case (kickoff-meeting resource isn't yet in-course). |
| 3 | page9 | 241 | 2 H2 | `keep` | Dominant-pattern exemplar. Documented as a worked example above. |
| 4 | page5 | 314 | 2 H2 | `keep` | |
| 5 | page6 | 261 | 2 H2, narrative second section | `restructure` | Convert "What comes next week" → "How to prepare" with bullets. No documented reason for the variant. |
| 6 | page10 | 434 | 2 H2 | `copy-edit` | Tighten toward 350. R#2 sits inside W6, so no reflection preview needed. |
| 7 | page8 | 339 | 2 H2 | `keep` | |
| 8 | page6 | 263 | 2 H2 | `copy-edit` | Add a one-line Reflection #3 preview following W11's pattern. |
| 9 | page6 | 442 | 3 H2 (Change Log) | `keep` | 3-H2 variant exemplar. Documented as a worked example above. |
| 10 | page4 | 443 | 3 H2 (rubric revisit) | `keep` | Audit Change Log mention in prep for consistency with W9. |
| 11 | page5 | 480 | 3 H2 (Reflection #4 preview) | `keep` | Reflection-preview model. Audit Change Log mention. |
| 12 | page5 | 330 | 2 H2 (optional check-in + cancellation template) | `intentional variant` | Optional / skippable-event form. The cancellation message template is justified — coaches the call. Audit Change Log mention. |
| 13 | page4 | 304 | narrative bullets, "Take a beat" | `intentional variant` | Celebration / pause variant. Documented as a worked example above. Add a one-line Reflection #5 preview during the documenting pass. |
| 14 | page5 | 289 | status checklist | `keep` | Terminal-week status-checklist exemplar. Documented as a worked example above. |

---

## Where this fits with other guides

- **`guides/content-production-guide.md`** — overall voice/tone/format conventions for all learner-facing content. The what's-next section in that guide now points here.
- **`guides/deliverable-page-template.md`** — companion template for graded/completion-based deliverable pages. The two cover different page types.
- **`guides/actual-content-map.md`** — current page-by-page state of weeks 1–9 plus the cross-week arcs (employer touchpoints, deliverables, reflections, running artifacts). Source for the *Cross-week-arc surfacing checklist*.
- **Per-week `CHANGELOG.md`** — captures the *why* behind structural decisions on already-restructured weeks.
