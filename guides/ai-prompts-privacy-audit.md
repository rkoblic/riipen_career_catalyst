# AI Prompt Privacy Audit — Held for Later Pass

**Status:** Findings only — no edits made. Held for a dedicated pass.
**Captured:** 2026-05-20
**Triggered by:** Rachel flagged the W15 p5 (End-of-Project Peer Evaluation) example prompt that read `Here are my notes on [teammate]…` — implying the learner would substitute a real name into an LLM. Fixed on W15 p5 (anonymization callout added + prompt placeholder changed to "this teammate"). A scan across the course found related patterns on other pages that weren't changed at the time.

## The principle

When course content includes example AI prompts, those examples are training a habit. If an example prompts a learner to paste teammate names, employer-confidential content, or client-identifying detail into a third-party LLM, the page is modeling the wrong instinct — even if the surrounding paragraph doesn't intend that.

Two existing precedents in the course already establish the principle:

- **W1 p4 ai-workplace.md** (line 57): *"don't paste it into an AI tool. Paraphrase or anonymize the details instead."* — One bullet inside a longer list. Easy to miss.
- **W9 p2 team-processing-session.md** (line 31): *"Remove identifying details before pasting."* — Inline, applied to peer feedback.
- **W15 p5 end-of-project-peer-evaluation.md** (recently added): Full Key Principle callout with *why* (workplace AI policy norms, third-party logs) and the substitution pattern ("this teammate" / "Teammate A").

The cleanest future-pass shape would be: strengthen W1 p4 as the canonical rule (Key Principle callout, workplace-AI-policy framing), then add a short cascade reminder ("scrub employer-identifying detail before pasting; see W1 p4") at each of the higher-risk paste prompts downstream.

---

## HIGH — Same pattern as the W15 p5 case (third-party identifying info in prompt examples)

### W8 p2 page2-peer-evaluation-1.md — Mid-Project Peer Evaluation
**Issue:** AI section invites learners to use AI on Continue/Start/Adjust drafts, which contain teammate-identifying detail. The example prompt itself is meta ("Does this feedback reference a specific behavior?") so less directly bad than W15 p5 was, but the two peer-eval pages should tell a consistent story.
**Suggested fix:** Add the same anonymization callout that's now on W15 p5 (Key Principle: "Before you paste: anonymize"). Parallel structure between Mid-Project and End-of-Project peer eval pages.

---

## MEDIUM — Pasting team/employer artifacts that almost certainly contain employer-confidential info

### W4 p3 page3-using-ai.md — foundational AI-in-research page
**Lines:** 27, 39
**Issue:** Example prompts like *"Here's our draft competitive analysis for [project]…"* — the analysis names the employer, competitors, and internal data. The `[project]` placeholder doesn't anonymize the body.
**Why it matters:** This is the foundational AI-in-research page; the guidance cascades through Weeks 4–14. Natural home for the "before you paste" rule.
**Suggested fix:** Add a "Before you paste" section near the top of the page that names what to scrub (org name, contact names, internal numbers, unreleased plans). Link back to W1 p4.

### W5 p5 direction-check-summary.md
**Line:** 77
**Issue:** *"Here's our context analysis and project plan for [project]. Act as a critical stakeholder…"* — the Context Analysis & Project Plan names the employer by definition.
**Suggested fix:** One-line cascade reminder linking to W4 p3 / W1 p4.

### W7 p5 working-with-data-visuals.md
**Line:** 52
**Issue:** *"Attach a spreadsheet or paste your data…"* — employer data lives in spreadsheets.
**Suggested fix:** Flag scrubbing identifying columns or paraphrasing before paste.

### W6 p5 formatting-professional-deliverables.md
**Line:** 128
**Issue:** *"Before merging, paste two or three team members' sections into an AI tool…"* — sections likely contain employer-specific content. Softer secondary concern: teammates' authorship going through AI without their say.
**Suggested fix:** Cascade reminder + a brief note about teammate awareness.

### W8 p5 ai-development-partner.md
**Lines:** 29, 33, 43, 45 — multiple paste prompts
**Issue:** Pages instructs paste-for-review across feedback application, pre-share review, multi-model review. Development-phase sections are the densest with employer-confidential content in the whole course.
**Suggested fix:** Cascade reminder at the top of the page.

### W10 p3 ai-quality-reviewer.md
**Line:** 45
**Issue:** *"Read this document as someone who has never heard of this project or client…"* — instructs the learner to paste the full near-final deliverable. **This is the highest-stakes paste in the course — the deliverable IS the employer-specific artifact.**
**Suggested fix:** Explicit anonymization callout (Key Principle level), not just a cascade reminder.

### W14 p3 presentation-outline.md (line 82), W12 p3 presentation-fundamentals.md (line 101), W15 p2 final-presentation.md (line 160)
**Issue:** Three late-stage pages telling learners to paste/attach the recommendation, outline, or deck for AI review. All employer-shaped artifacts.
**Suggested fix:** Cascade reminder on each.

---

## MEDIUM — Recording / transcript pages with consent gaps

### W9 p4 development-check-in-2.md (line 78), and similar late-stage check-in pages
**Issue:** References AI note-taking tools and transcripts without restating *"ask the employer's permission to record."* W7 p7 (line 59) does establish the consent norm — but if a learner lands on a later check-in page first, they may miss it.
**Suggested fix:** One-line cascade reminder. *"Permission to record was established at the first check-in (see W7 p7); reconfirm if anything has changed."*

---

## LOW — Adjacent concerns worth considering

### W1 p9 professional-email.md
**Line:** 80
**Issue:** *"Here's my draft: [paste draft]. Review it for professional tone…"* — the draft email contains the recipient's name and possibly the employer org.
**Why low:** This is the first AI prompt example a learner sees, so the framing matters — but the content (a single first-message draft) is low-stakes compared to the deliverable-level pastes downstream.
**Suggested fix:** Light note: scrub the recipient's name and the org name before pasting; the prompt works fine with "Hi [Name]" placeholders.

### W7 p7 development-check-in-1.md
**Line:** 51
**Issue:** *"Here's a brief summary of our project and where we are: [paste summary]."* Same concern as the deliverable-level pastes; brief summaries usually name the employer.
**Suggested fix:** Cascade reminder.

### W4 p4 research-and-analysis.md
**Line:** 133
**Issue:** *"Here are research findings from four team members on [topic]…"* — research findings often include employer-confidential context.
**Suggested fix:** Cascade reminder.

### W15 p7 articulating-your-experience.md
**Issue:** Different category — this is the learner pasting their *own* resume / writing into AI. Not a third-party issue. But:
1. Resumes contain PII (address, phone) the learner may want to scrub before pasting into a free-tier AI.
2. Some employers run AI-detection on application materials — worth letting learners know that polishing is fine but generating raw text isn't.
**Suggested fix:** Add a short note about both (PII scrubbing + AI-detection on applications).

### Reflection pages (W3 p8, W6 p2, W9 p5, W12 p4)
**Issue:** Reflection prompts often surface specific teammate behavior. If learners paste draft Examine paragraphs that name teammates, that's a third-party issue.
**Why low:** Reflections rarely use long verbatim quotes of teammates' words. Risk exists but is smaller than the deliverable-level pastes.
**Suggested fix:** Rely on a strengthened W1 p4 + the in-place callouts on the two peer-eval pages. Or add a one-line reminder in the Using AI section of each reflection.

---

## Suggested approach when this gets picked up

1. **Strengthen W1 p4 ai-workplace.md** as the canonical anonymization rule. Promote the current single bullet to a Key Principle callout, add the workplace-AI-policy framing we used on W15 p5 (third-party service logs; workplace AI policies prohibit this; the course is teaching learners what NOT to put into AI as much as what to put into it).

2. **Add a "Before you paste" section to W4 p3** (foundational AI-for-research page) — one short paragraph that establishes the team-side practice, since this is where most of the downstream pasting begins. Cascade reminders downstream link back here.

3. **One-line cascade reminders** on the MEDIUM-severity pages: W4 p4, W5 p5, W6 p5, W7 p5, W7 p7, W8 p5, W10 p3, W12 p3, W14 p3, W15 p2. Short, consistent, doesn't bloat each page. Example: *"Scrub employer-identifying detail before pasting — see [Using AI Responsibly](W2 p2) and [Using AI in your Discovery work](W4 p3)."*

4. **Parallel anonymization callout on W8 p2** (Mid-Project Peer Evaluation) — same Key Principle component now on W15 p5, so the two peer-eval pages match.

5. **W15 p7 articulating-your-experience.md** — add the resume PII + AI-detection note as a separate consideration. Different category from third-party privacy; worth its own short section.

6. **Optional: reflection pages** — add a one-line "anonymize teammate references in any draft paragraphs you paste" reminder in each Using AI section. Or rely on the strengthened W1 p4 to carry it.

## Memory pointer

The principle that drove this audit is captured in [feedback_ai_prompts_no_pii.md](../../../.claude/projects/-Users-rachelkoblic-riipen-career-catalyst/memory/feedback_ai_prompts_no_pii.md) (project memory). That memory should be loaded automatically; when the later pass happens, it will already be in scope.
