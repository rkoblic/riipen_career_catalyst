---
artifact: Your Starting Point Questionnaire
audience: Riipen platform team (form builder spec)
referenced_from: weekly_content/week01/page6-project-browsing-intake.md
status: draft
created: 2026-05-12
last_updated: 2026-05-12
---

# Your Starting Point Questionnaire — Platform Spec

This document specifies the questions, field types, help text, and validation rules for the Your Starting Point Questionnaire that learners complete in Week 1. It is the source-of-truth content for the form Riipen builds on its platform.

The questionnaire serves two roles. It informs project matching, and it is the baseline that learners' graded reflections will reach back to in Weeks 3, 9, 12, and 14. Part 1's responses are quoted (in spirit, not always verbatim) by those reflection prompts, so the questions below are written to surface the specific dimensions those reflections circle back to: learning goals, the professional challenge the learner wants to work on, and the skills and experiences they brought in.

---

## Submission settings

| Setting | Value |
|---|---|
| Submission type | Individual |
| Grading | Completion-based (pass on submission, no quality rubric) |
| AI use | Not permitted on Part 1 (self-assessment) or on the written rationale in Part 2. Permitted as a thinking tool for *comparing* project briefs before writing the rationale. |
| Editable after submission? | No. Responses are frozen at submission so they remain a true baseline for later reflections. |
| Visibility | Learner sees their own responses any time. Instructor sees all. Employers do not see responses. |
| Reference access | Learner can view their submitted responses inline when drafting Reflections #1, #3, #4, and #5. (See "Post-submission behavior" at the end of this spec.) |

---

## Pre-questionnaire framing (shown above Part 1 on the form)

> **Before you begin.** This questionnaire takes about 25–35 minutes. It has two parts: a self-assessment and your project preferences. Together they capture where you're beginning this experience.
>
> Your responses inform project matching, but their more important job is to be a baseline you'll reference back to in graded reflections later in the course. That only works if your answers are honest — not aspirational, not polished. If you're unsure about something, say so. If you've never done something before, say that. The goal is an accurate starting point, not an impressive one.
>
> **AI use.** Do not use AI on Part 1 or on the written rationale in Part 2. You *can* use AI to compare project briefs before writing your rationale; that is a thinking tool, not a shortcut. The reasoning itself must be yours.

---

## Part 1 — About you

Part 1 captures who the learner is at the start of the course. All questions in this part are required.

### Q1. Learning goals

**Field type:** Long text (textarea)
**Character limit:** 200–800 characters (soft minimum 200, hard maximum 800)
**Required:** Yes

**Prompt shown to learner:**

> What do you most want to learn or develop in this course? Name two or three specific goals — capabilities, habits, or kinds of judgment you want to build, not topics you want to "be exposed to." Concrete is more useful than impressive.

**Help text (below the field, in grey 9pt):**

> *Examples of the level of specificity we're looking for: "Get better at translating a vague employer ask into a scoped project plan." "Learn how I work in a team I didn't pick." "Build confidence presenting analysis to someone more senior than me." You'll come back to this answer in graded reflections in Weeks 3, 9, and 14.*

**Validation:** Reject submission if blank or under 200 characters. Show inline warning: "Most useful answers are at least two or three sentences." (Warn, do not block, between 200 and 350 characters.)

---

### Q2. The professional challenge you want to work on

**Field type:** Long text (textarea)
**Character limit:** 200–600 characters
**Required:** Yes

**Prompt shown to learner:**

> Beyond skills, what is the *professional challenge* you want to work on during this course? This is the part of working as a professional that you find hardest, most uncertain, or most worth pushing on right now. It might be something interpersonal (giving direct feedback, asking for help, being heard in a group), something about your work habits (following through, planning realistically, managing time across competing priorities), or something about how you show up (speaking up earlier, taking up less space, taking up more).

**Help text:**

> *This question is asked separately from your learning goals because it tends to surface different things. Goals are what you want to build; the professional challenge is what gets in your way. Both are useful, and reflections later in the course return to this one specifically.*

**Validation:** Reject if blank or under 150 characters.

---

### Q3. Skills and experiences you're bringing in

**Field type:** Long text (textarea)
**Character limit:** 200–1000 characters
**Required:** Yes

**Prompt shown to learner:**

> What relevant skills, experiences, or prior projects are you bringing into this course? Include coursework, jobs, internships, volunteer roles, side projects, or anything else you'd point to if asked "what have you done that's relevant to professional work?" Be honest about depth — a one-week assignment isn't the same as a year of practice, and naming the difference now will help you in the reflections.

**Help text:**

> *Reflection #4 in Week 12 looks back at this answer and asks where your stated capabilities actually showed up in the team's work, where you may have overestimated yourself, and where skills you didn't list turned out to matter more than expected. That comparison only works if this answer is specific.*

**Validation:** Reject if blank or under 150 characters.

---

### Q4. Self-assessment: confidence on the course competencies

**Field type:** 5 × Likert rating (radio buttons), one row per competency area
**Scale:** 1 — Very low confidence · 2 — Low · 3 — Moderate · 4 — High · 5 — Very high confidence
**Required:** Yes (all five rows)

**Prompt shown to learner:**

> Rate your current confidence in each of the five competency areas the course develops. There's no "right" pattern — uneven self-assessments are more useful than uniformly high or uniformly low ones. You'll see growth in these ratings (and shifts in your own definition of each area) over the course of the term.

**Rows (with one-line definition shown next to each label):**

| Competency area | Definition shown to learner |
|---|---|
| **Career & Self-Development** | Knowing yourself as a professional, setting goals, reflecting on growth. |
| **Communication** | Writing and speaking clearly for a professional audience; adapting tone and depth to context. |
| **Critical Thinking** | Framing problems, using evidence, weighing tradeoffs, deciding what to prioritize. |
| **Professionalism** | Following through, owning your work, being someone teammates and employers can rely on. |
| **Teamwork** | Contributing to a group's shared work; navigating disagreement; sharing accountability. |

**Help text below the table:**

> *These five areas come from the course's competency framework and align with how every graded deliverable is assessed. You won't be graded on your ratings — the point is to capture a baseline you can compare against later.*

**Validation:** Reject if any of the five rows is unrated.

---

### Q5. Expectations and concerns

**Field type:** Long text (textarea)
**Character limit:** 150–700 characters
**Required:** Yes

**Prompt shown to learner:**

> What are you hoping this course will give you, and what are you genuinely worried about? Naming the concern is not a complaint — it's a signal to your instructor and a marker you can revisit later when you find out whether the worry held up.

**Help text:**

> *Honest concerns help the team designing your project experience anticipate the friction points. They are not held against you and are not visible to employers.*

**Validation:** Reject if blank or under 100 characters.

---

### Q6. Logistics: anything that affects how you can show up

**Field type:** Long text (textarea), optional
**Character limit:** 0–500 characters
**Required:** No (clearly labelled "Optional")

**Prompt shown to learner:**

> Optional. Is there anything about your schedule, time zone, working setup, or other commitments this term that we should know about so we can match you to a team that works for you? This isn't an exhaustive list and you don't need to over-explain.

**Help text:**

> *Examples: time-zone constraints, a heavy course load this term, a part-time job with fixed hours, a known week you'll be away. Skip if nothing applies.*

**Validation:** None (field is optional and may be left blank).

---

## Part 2 — Your project preferences

Part 2 captures the learner's ranked project selections with a brief written rationale for each. The Riipen platform should pull the list of available project briefs for the current term into this section dynamically.

### Q7. Ranked project preferences

**Field type:** Ranked selection. Show the available project briefs as a list. The learner drags-and-drops or uses up/down arrows to order them; the top N positions are submitted as their ranked preferences.

**N (number of ranked positions required):** 3 (the top 3 must be ranked; learners may rank beyond 3 if they want to but it is not required).

**Required:** Yes, all top 3 positions filled.

**Prompt shown to learner:**

> Rank at least your top three project choices from most preferred to least preferred. You can rank more if you'd like to express stronger preferences across the full list, but the top three are what the matching process uses.

**Validation:** Reject if fewer than 3 ranked positions are filled, or if the same brief is somehow ranked twice.

---

### Q8. Rationale for each ranked preference

**Field type:** Long text (textarea), one per ranked position 1, 2, and 3.
**Character limit per rationale:** 150–500 characters
**Required:** Yes for positions 1, 2, and 3. (Optional for positions beyond 3 if the learner ranked more.)

**Prompt shown above each rationale field (with the project name auto-filled):**

> **Rationale for [Project name] (your rank #X):** What draws you to this project, and what would you hope to gain from working on it? A useful rationale names the project, says what draws you to it, and explains what you'd hope to gain. Two or three sentences is enough. Be specific and honest — "this sounds interesting" doesn't tell us anything.

**Help text:**

> *You can use AI to help you compare and evaluate the project briefs themselves — generating comparison criteria, identifying questions to ask about each, surfacing tradeoffs. That is a legitimate use of AI as a thinking tool. The rationale you submit, though, must be your own reasoning in your own words.*

**Validation:** Reject if any of the three required rationales is blank or under 100 characters.

---

## Confirmation step (shown before submit)

Above the Submit button, show a single confirmation checkbox:

> &#9744; I completed Part 1 (self-assessment) and the written rationales in Part 2 without using AI assistance. I understand my responses are the baseline I'll reference back to in graded reflections later in this course, and that submitting an AI-generated baseline would make those reflections impossible to write honestly.

**Validation:** Submit button is disabled until the box is checked.

---

## Post-submission behavior

These behaviors keep the questionnaire useful as a baseline across the rest of the course. They are part of the spec, not nice-to-haves.

1. **Frozen on submission.** Responses cannot be edited after submission. If a learner needs to correct a significant error, the instructor can re-open the submission via the platform's existing override flow; the learner cannot self-edit.
2. **Inline access from reflection pages.** When a learner opens Reflection #1 (Week 3), #3 (Week 9), #4 (Week 12), or #5 (Week 14), their Part 1 responses for Q1 (learning goals), Q2 (professional challenge), and Q3 (skills and experiences brought in) should be available inline — either expanded by default or behind a single click labelled "View your Starting Point responses." Q4 (the competency ratings) should also be available on Reflection #4 and #5.
3. **Permanent learner-side access.** Learners can view their own full submission at any time from a stable URL or dashboard tile labelled "Your Starting Point" — they should not have to dig through a list of past submissions to find it.
4. **Instructor visibility.** Instructors see all responses across the cohort in a sortable list. The competency ratings (Q4) should be exportable as CSV for cohort-level visibility on starting-point patterns.
5. **No employer visibility.** Employers do not see learner self-assessment responses, ranked preferences, or rationales. These are between the learner, the instructor, and the matching process.

---

## Open questions for the platform team

- Is the ranked-preference field (Q7) something the existing Riipen platform supports natively, or does it need a new control?
- For the "view your Starting Point inline" behavior on reflection pages (item 2 above), is the right mechanism a sidebar widget, a top-of-page expand block, or a link out to a separate read-only view?
- Should the optional logistics field (Q6) feed into the matching algorithm automatically, or is it surfaced to a human matcher to read before placement?
