# Week 8 — Notes from Rachel's Pass

Hi Kim — this is a running log of changes I make to Week 8 and why.

---

## Patterns to carry forward

**Calibrate page framing to what course events actually produce.** Several pages this week treated Check-In #1 as if it generated a big bundle of unsorted client feedback. In reality it's a 30-minute team-driven working meeting where most of what the team hears is answers to questions they brought in. That mismatch inflated the overview video, bloated Page 2's sorting framework, and made Page 6 overstate what a "first structured pass at feedback" actually involved. Describe what the event actually produces and let the page framing follow.

**Treat rubric and assessment framework docs as the source of truth.** Aligning Page 2 with the Peer Evaluation Framework and Page 3 with the Employer Evaluation Framework caught real errors: wrong dimension names, missing Teamwork subskills in the YAML, softened behavioral anchors, and a vague "how you'll receive it" section we could replace with specific delivery mechanics. When a page covers a graded deliverable or assessment mechanism, open the framework doc before writing and drive the page from it.

**Right-size pages to the week's actual lifts.** Two pages of feedback-triage meta-content (old Pages 2 and 3) were more than the week needed once Check-In #1 was calibrated honestly. The calibration exercise and the Status Update standing prompt also got cut. The lift test: does this page earn its place given everything else the learner is doing this week? If a page is more meta than operationally useful, consolidate or cut.

**Frame resource pages as habits, not one-time exercises.** Page 4 (Acting on Feedback) was originally built around triaging Check-In #1 feedback specifically. Reframing it around "what to do when feedback arrives during production" made it durable across the rest of the project. For any page teaching a repeatable skill, lead with the habit and use the week's immediate event as the first use case.

**Put the macro before the detail on multi-part deliverables.** Moving "The assignment" to the top of Page 2 gives learners the four-part structure before they read through Continue/Start/Adjust and BARS. Deep-dive sections then elaborate on parts they've already seen.

**Echo strong frames across pages.** The 360-review framing opened the week in the overview video, threaded through Page 3's "how this connects to the peer evaluation" section, and appeared briefly on Page 6. Echoes across pages reinforce the same mental model and make the week cohere. Cross-reference a strong frame across multiple pages where it lands naturally.

**Use evergreen descriptive language over numbered labels and specific percentages.** "Peer Evaluation #1" became "Mid-Project Peer Evaluation." "Check-In #1" became "last week's check-in with our employer." The overview page's "~10% of your final grade" (which was also factually wrong, the math was closer to 3%) became "the Professional Engagement component of your final grade." Numbered labels read as internal-spec references. Specific percentages age badly across course changes and compound errors across pages.

**Name tool default behaviors that learners might want to override.** The AI page now flags that LLMs are built to be helpful and will generate critique even when the writing is solid, and covers how to give them explicit permission to say nothing. Naming what a tool does by default, and what you might want to override, is useful any time we're giving tool-use instructions.

**Link to authoritative sources, not just names.** The Grading section on Page 2 now links to the Professional Engagement assignment and rubric with a `URL_TBD` placeholder. Any learner-facing mention of a grading component, rubric, or external course artifact should include a link, even a placeholder one. The act of linking forces the question "where does this actually live?"

---

## Page-by-page notes

### Page 1 — Overview

- **Reframed the opening around continued production + mid-project evaluation from two directions** (peer and employer), replacing the old framing that led with "translating Check-In #1 feedback into revisions." That earlier framing overstated the scale of the feedback triage challenge — Check-In #1 is a 30-minute working meeting driven by the team's own prioritized questions, so much of what the team heard was already pre-sorted into act-on by virtue of being asked.
- **Added a line about the employer mid-project evaluation** happening this week. It's not a learner deliverable, but it also feeds Professional Engagement, and naming it makes the dual-evaluation shape of the week explicit.
- **Fixed the grade-weighting language.** The original page claimed Peer Evaluation #1 contributes "~10% of your final grade." Per the design doc, Peer Eval #1 is 30% of the peer evaluation score × 50% of Professional Engagement × 20% of the final grade — closer to 3%, not 10%. Replaced the specific percentage with "the Professional Engagement component of your final grade," which is accurate and evergreen.
- **Split step 1 of the suggested order into two steps** (read the module; then run the team planning session as a separate action) and softened the "sort your Check-In #1 feedback into act-on/note/set-aside" language. The triage is real but narrower than the step was making it sound.
- **Cut "Use it." closer** (pithy two-word imperatives read as AI-generated) and **trimmed em dashes** throughout the page, swapping to colons and sentence breaks.

### Page 1 video script

- **Full rewrite.** The previous script was built on the premise that Check-In #1 produced a large, unsorted bundle of client feedback with stylistic preferences hiding in passing comments. In practice it was a short working meeting organized around the team's own questions. The framing overstated the scale of the feedback problem and drifted into Page 2's instructional territory with the "what would actually change if you acted on it?" heuristic.
- **New framing** opens with mid-project evaluation as a built-in rhythm of professional work, names that this week learners are on both sides of one of those checkpoints, and lands on the actual skill the peer evaluation asks for: naming the specific behavior behind each rating.
- **Removed em dashes** (the overview video guide is unambiguous on this) and **trimmed from ~210 to ~155 words** to stay inside the 120–200 range.
- **Removed the closing handoff** ("The module that follows walks through this in detail. But that question is where to start.") in favor of landing on the manager/performance-review parallel.

**Second pass (later the same day):**

- **Dropped the "Peer Evaluation #1" label from learner-facing text.** It isn't actually the first graded individual deliverable of the course, and the numbered labeling reads like an internal spec reference. "The peer evaluation" or "your peer evaluation" is cleaner and clearer.
- **Added the reciprocal framing.** Learners aren't just evaluating teammates — each teammate is also evaluating them. That reciprocal loop is what makes the peer evaluation part of a real feedback exchange, not just an individual submission.
- **Added the Week 9 loop-back.** Next week, results come back and the team discusses them. Without that, the peer evaluation reads as a one-way grade-generator; with it, it reads as a mid-project feedback loop with a processing session built in.
- **Trimmed the employer evaluation wording** now that "Professional Engagement" is introduced earlier in the page — no need to restate it at the same length.

**Third pass (video script reframe):**

- **Swapped the professional analog.** The "mid-project evaluation from the client" framing was inaccurate — in real consulting work, a client doesn't typically evaluate the consultant's individual performance mid-project. The better analog is a corporate performance review with a 360 element: feedback from peers and colleagues, not just from a manager. This week's peer-plus-employer structure maps cleanly onto that pattern, and most learners will encounter exactly this kind of review in their first corporate roles.
- **Added a "why practice this" beat.** Writing specific, behavior-based feedback is a core skill for anyone who ends up leading a team. The closer now names that future-management connection explicitly, which makes the peer evaluation feel like a skill worth getting good at, not just a course requirement.

### Page order — restructured around the week's actual centers of gravity

- The peer evaluation is the most important individual work this week, so its module is now Page 2 (was Page 4 after the consolidation, originally Page 5 before that).
- Added a new Page 3, **About the employer mid-project evaluation** — an FYI page covering what the employer is being asked, when, why mid-project, and how it factors into Professional Engagement. The "How you'll receive it" section is flagged TBD pending confirmation of the platform delivery mechanism.
- The two production-support pages (**Acting on Feedback During Production** and **AI as a Production Partner**) are now positioned as resource pages after the evaluation content, since they're references learners reach for during production rather than sequential instruction.

**New Week 8 page order:**

| Page | Title | Notes |
|---|---|---|
| 1 | Week Overview | — |
| 2 | Peer Evaluation | The week's central individual work |
| 3 | About the employer mid-project evaluation | New FYI page |
| 4 | Acting on feedback during production | Resource page |
| 5 | AI as a Production Partner | Resource page |
| 6 | What's Next | — |

The Page 1 suggested-order-of-completion list was updated to match.

### Page 2 — Mid-Project Peer Evaluation *(was Page 4 after first restructure; originally Page 5)*

- Renumbered.
- **Renamed throughout to "Mid-Project Peer Evaluation"** (YAML title, H1, four in-body references, and assignment section). This replaces "Peer Evaluation #1" as the learner-facing term and aligns with the "mid-project" language used for the employer evaluation on Page 3 and in the Employer Evaluation Framework. Sets up "End-of-Project Peer Evaluation" as a clean pair for Week 14/15. The filename still carries "-1" as internal organization — we can rename that later if useful.
- **Added a link to the Professional Engagement assignment page and rubric** in the Grading section (with a `URL_TBD` placeholder). The page now points learners to where they can see how peer evaluation, employer feedback, and instructor observation combine into the Professional Engagement component of their final grade.
- **Named the Team Processing Session** in the opener so the reference is consistent with Page 3. The original opener described it generically ("a structured team discussion next week") without naming it.
- **Softened the "formative, not to finalize grades" construction** in the opener. Dropped the "X, not Y" pattern. "Formative" does the framing work; the Grading section later confirms the grade contribution.
- **Fixed "abstract 1–5 numbers"** — the BARS scales on the page are all 1–4, so the opening reference to 1–5 was wrong. Changed to "abstract numeric ratings."
- **Cleaned em dashes** across the page: opening paragraph, formative-evaluation line, the "specific behavior" clarification, the Adjustment-vs-cessation line, the Constructive Engagement Strong evidence example, the self-evaluation purpose line, the four "Part A / B / C / D" labels (swapped to colons), the Grading line, and the AI guidance line.

**Second pass — opening paragraph refinement:**

- Reframed the deliverable from "graded individual deliverable" to "required individual deliverable that will contribute to your peers' Professional Engagement grade." Names a real stake (peers' grades) that makes the responsibility tangible. The self-grading piece still lives in the Grading section later.
- Softened the closing sentence: "You'll receive anonymized feedback from your peers next week, and your team will have the chance to discuss it and agree on specific changes." Uses contractions consistent with the rest of the paragraph, trims an article, and cleans up a double-infinitive ("discuss the feedback to agree on" → "discuss it and agree on").

**Third pass — alignment with the Peer Evaluation Framework:**

- **Fixed the YAML competencies list.** The framework is explicit that all four BARS dimensions map to Teamwork subskills — Reliability, Collaborative Contribution, Constructive Feedback, Shared Accountability. The page had "Communication → Written Clarity" listed, which doesn't correspond to any peer evaluation dimension in the framework. Swapped in the correct Teamwork → Collaborative Contribution entry (for the Contribution dimension).
- **Restored the full Accountability level-1 descriptor.** Framework language: "May actively undermine team cohesion through gossip, complaints, or disengagement." The page had shortened this to "May undermine team cohesion through disengagement," which drops two specific behaviors (gossip, complaints) the framework calls out at this worst level.
- **Restored the Accountability level-2 descriptor.** Framework language: "May blame external factors (the employer, the timeline, the tools) rather than examining their own role." The page had softened "blame" to "attribute issues" and removed the parenthetical examples. Restored both — the concrete examples make the anchor more useful to evaluators, and "blame" is the right verb at this level.

**Fourth pass — structural reorganization:**

- **Moved "The assignment" section to the top** as a brief bulleted overview of the four parts (Part A / B / C / D). Macro framing before the deep-dive sections. The detailed content that was in "The assignment" (two-sentence minimum, "select the lower one" guidance, "evidence statements encouraged but not required," Part D instructor-only note) was folded into the relevant deep-dive sections where learners actually need that guidance in the moment.
- **Added a new "What you'll receive" section** before Submission and Grading. Explains what comes back from each part — anonymized qualitative comments (Part A), averaged dimension scores not individual rater scores (Part B), instructor-only for C and D. This closes the loop on the framework's anonymization and aggregation specifications so learners know they can't reverse-engineer individual teammate ratings from the data.
- **Renamed the old bottom section to "Submission and grading"** now that the parts overview has moved up. Submission logistics and Grading both still live there.
- **"Select the lower one" guidance retained** per your decision and moved into the BARS ratings section where it actually applies.

**Fifth pass — Check-In #1 scrub:**

- Replaced all four "Check-In #1" references in the examples with plain language: "last week's check-in with our employer" / "our prep session for last week's check-in with our employer" / "preparing for last week's check-in with our employer." Matches the Page 1 overview shift away from the numbered label in narrative text.

**Sixth pass — calibration exercise removed:**

- Removed the entire "Calibration exercise: Maple & Main" section, including the `[INTERACTIVE: ...]` placeholder and the Jordan profile exercise. The BARS tables plus the weak-vs-strong evidence pairs were already doing the calibration work on their own, and removing the interactive placeholder eliminates a separate build dependency.
- Updated the "rest of this page" transition at the bottom of the assignment overview to drop the calibration mention: now reads "The rest of this page walks through each part in more detail."

### Page 3 — About the employer mid-project evaluation *(new page)*

- New FYI page. Names what the employer is being asked, when it happens, why mid-project feedback exists in professional contexts, and what learners can do with the knowledge that the survey is happening.

**Second pass — alignment with the Employer Evaluation Framework:**

- **Corrected the dimensions.** The original draft listed Responsiveness, Communication quality, and Professionalism. The actual instrument per the framework is Communication, Preparedness, Responsiveness — and "Professionalism" was deliberately removed from the framework because it's too vague and gets covered by the other three dimensions in practice. This was the most important fix.
- **Filled in "How you'll receive it"** with the concrete delivery mechanism from the framework. Three dimension scores and the verbatim qualitative response come back to the team before the Team Processing Session next week. The instructor-only confidence signal stays with the instructor. No more TBD placeholder.
- **Named the open-ended question verbatim** ("Is there anything specific you would like the team to do differently in how they communicate or work with you for the remainder of the project?") so learners know exactly what kind of input to expect — actionable behavior change, not vague praise.
- **Added Kickoff to the touchpoint list** in "When and why now" — the framework names Kickoff, Direction Check, Check-In #1, and ongoing email as the touchpoints the mid-project survey reflects on.
- **Added a new "How this connects to the peer evaluation" section.** The framework calls this "one of the most powerful learning moments in the course" — peer eval surfaces the team's internal experience, employer eval surfaces the external view, and where the two pictures diverge is where the most useful Team Processing Session conversations come from. This extends the 360-review framing from the overview video.
- **Added the scope boundary** ("Internal team dynamics and the quality of the deliverables are assessed elsewhere") — the framework is explicit that the employer survey only covers what employers can directly observe, and naming that helps learners understand why teamwork dynamics aren't on this survey but are on the peer eval.
- **Trimmed "What you can do with this"** since the next-week processing is now covered by the new connection section. Kept the page focused on this-week behavior.
- **Em-dash-clean throughout.**

### Page 4 — Acting on feedback during production *(was Page 2 after consolidation)*

- **Consolidated the old Page 2 (Processing Feedback & Revision) and Page 3 (Structural vs. Targeted Revisions) into one page.** The two were doing more meta-feedback-theory than the week's reality calls for. With Check-In #1 calibrated honestly, most of what the team heard was answers to their own prioritized questions — already act-on by default. Two pages of sorting + revision-type frameworks before any actual revision happens is a lot of meta before the work. One tighter page covers the same ground without the front-loading.
- **Reframed the page from a Check-In #1 triage exercise to an evergreen production-phase habit.** New opener: as you progress in production, feedback arrives constantly from multiple sources, and most of it is small. This page is what to do when something arrives that asks you to shift what you're producing. The framework still applies to Check-In #1 (the immediate use case this week), but it's also applicable to async messages, internal review, and any feedback that lands during the rest of production.
- **Folded in the structural vs. targeted distinction** as a sub-section under "Build a quick revision plan" — placed at the moment learners are filling out the revision plan, which is when they actually need it. Kept the "would your teammates notice if you didn't tell them?" test, which is the strongest single move from the old Page 3.
- **Dropped the video.** The five-feedback walkthrough was strong content, but a tighter all-text page reads cleanly without it. The example contrasts (community outreach, process improvement, social media — across all three categories) are now inline on the page.
- **Cut prescriptive time estimates** ("a targeted edit takes an hour; a structural revision takes a day") and the "'the whole team' owns nothing" aphorism. Both replaced with plain guidance.
- **Trimmed em dashes** throughout the table, examples, and inline text.
- **Moved the Change Log introduction to Week 6 page 3** (Revisiting the Final Deliverable), where it belongs. By Week 8, teams have already had Direction Check feedback and internal reviews — the Change Log should already exist by then. Page 2's reference is now a brief connection back to the Change Log that was started earlier, not an introduction.

### Page 5 — AI as a Production Partner *(was Page 3 after consolidation; originally Page 4)*

- Renumbered.
- **Softened the "fresh reader" framing.** The original opener leaned on "AI's ability to read your work as a relatively fresh reader," which is the framing the AI arc reserves for the Week 10 quality reviewer capstone. Reframed around what the production-partner role is actually for this week: evaluating logic and structure (argument strength, transitions, evidence-claim alignment).
- **Cleaned three em dashes** in the opener, the "good editor" line, and the "wasn't at the meeting" line.
- Did not add an AI-for-organizing-the-feedback-response-plan section here — that guidance belongs on Page 4 (Acting on Feedback) where the revision plan template lives, if anywhere. Did not add a peer-eval bridge — that AI guidance lives on Page 2 (Peer Evaluation).

**Second pass — added two items:**

- **Added "Catching AI-isms in AI-assisted work"** to the "What AI is well suited to" list. Names the common fingerprints (em dashes, "not X but Y" constructions, parallel triplets, hyperbolic closers) and gives a prompt for having AI flag them. This closes a loop that's otherwise invisible to learners: AI-assisted prose has predictable tells, and AI can help find them.
- **Added a new "Working with AI well in this phase" section** with two tips: (1) use more than one model and cross-check (different LLMs give different feedback; you don't have to act on all of it; can ask one model to help you sort another's suggestions); (2) give the model explicit permission to say nothing, since LLMs are built to be helpful and will generate critique even when the writing is solid.

### Page 6 — What's Next *(was Page 5 after consolidation; originally Page 6)*

- Renumbered.
- **Trimmed from four H2 sections to two** to bring the page back in line with the production guide's "What's next" rules (one H2 for the next milestone, optional second H2 for "How to prepare"). The page had drifted into a multi-topic content page rather than a tight bridge.
- **Cut the Status Update to Employer section entirely.** Per earlier direction, that behavior shouldn't be introduced this week — if anywhere, it belongs earlier in the course.
- **Cut the standalone Team Processing Session section.** It duplicated content now on Page 3 (the 360-degree connection between peer and employer evaluation feedback). Replaced with a single-sentence mention in the opener.
- **Dropped "first peer evaluation" framing.** Consistent with the earlier removal of "Peer Evaluation #1" labeling from learner-facing text. Now: "the mid-project peer evaluation."
- **Softened the opener.** "First structured pass at incorporating employer feedback" overstated the work, especially after Page 4 (Acting on Feedback) was reframed as an evergreen production-phase habit. Now: "layered employer feedback into your team's revision plan."
- **Added a "Hold onto your peer evaluation notes" prep bullet** so learners are ready to think about what they received against the evidence that informed their own ratings.
- **Cleaned up the em dash** in the opener and removed the "Vague drafts produce vague questions" aphorism.

---

## Knock-on edits in other weeks

- **Week 6 page 3 (Revisiting the Final Deliverable)** — added a new H2 section, "The Change Log: a component to start now," that introduces the Change Log as a Final Deliverable component. Recommends teams start tracking now and gives a simple format. This relocates the Change Log introduction from Week 8 to where it actually belongs in the project arc, since by Week 8 teams have already had Direction Check feedback and internal review feedback that should be tracked.

---

Happy to talk through any of this if it's useful, or push back on anything.
