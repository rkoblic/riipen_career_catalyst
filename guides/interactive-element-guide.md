# Interactive Element Guide

How to design interactive practice elements for Riipen Career Catalyst.

This document covers the content design process. It produces a source-of-truth document that contains everything needed to build the interactive in any tool (LMS quiz builder, HTML, third-party platform). The actual build is a separate step.

---

## Inputs

Each interactive element requires:

1. **The weekly development plan** — identifies where the interactive lives, what activity it absorbs, and how much time it should take
2. **The weekly design document** — provides the source material: what skill is being practiced, what the activity prepares students for, and what competencies are in play
3. **The page content file** — the interactive should connect naturally to the content surrounding it; read the page it will live on before designing the scenario

---

## When to Use Interactive Elements

Interactive elements serve a specific purpose. Use them when:

- **Students face a high-stakes first.** Before the kickoff meeting, direction check, progress review, or final presentation. Students get a low-stakes practice rep before the real thing. (Content Development Principle 8.)
- **Students need to evaluate rather than recall.** When the skill is judgment (What did the employer actually confirm? Which claims in this summary are unsupported?) rather than knowledge (What are the three stages of the DEAL model?).
- **Reading alone won't build the skill.** Some things need to be experienced, even in a simplified form. Interpreting ambiguous employer statements, spotting AI errors, and prioritizing under constraints all benefit from practice over explanation.

Don't use interactive elements for:
- Content that's better served by a checklist or template
- Skills that students will practice for real within the same week (the real experience is the practice)
- Knowledge checks that could be a simple self-reflection question

---

## Design Principles

These principles should guide every interactive element. They were extracted from production and review of the Week 2 AI evaluation exercise.

1. **Practice over quiz.** The interactive should feel like doing the task, not answering questions about the task. "Review this document and decide what needs attention" is practice. "Which of the following is an example of a hallucinated source?" is a quiz. If a student could answer the questions without reading the stimulus, it's a quiz.

2. **The student drives the interaction.** Where possible, let students choose what to engage with rather than presenting pre-selected prompts in sequence. Missing something should be a learning moment, not impossible. This means the design needs to account for what students skip, not just what they select.

3. **Match the interaction model to the real task.** Choose a format that mirrors how the skill is actually performed. Document review = click-to-highlight. Meeting interpretation = narrative with decision points. Prioritization = drag-and-sort or ranking. If the interaction model doesn't resemble the real task, students practice the wrong thing.

4. **Action categories should teach a skill taxonomy.** Instead of generic ratings (good/bad/uncertain), use specific action categories that name what the student should do and why. "Look up this source" teaches a different move than "Find the original data" or "Check for more recent information." Students walk away with a repertoire of moves they can apply to any future situation.

5. **Include items that don't need action.** A realistic mix includes things that are fine alongside things that aren't. If every item is a problem, students learn blanket skepticism rather than judgment. The skill is knowing the difference.

6. **Provide feedback for what students miss.** Don't only give feedback on items students engage with. If they skip something important, the feedback should tell them what they should have noticed and why it matters. This is where some of the best learning happens.

7. **Always include a fallback format.** Describe the ideal interaction model (click-to-highlight, drag-and-sort, etc.) but specify a simpler fallback (sequential questions with the same content) for build tools that don't support the preferred model.

8. **Constraints:** All interactives must support automated, immediate feedback with no LLM or human grading. This means every response needs a deterministic correct answer or best answer, even for judgment-based questions.

---

## Interactive Element Types

### Type 1: Simulated Scenario

A realistic situation students will encounter, presented as a narrative with decision points.

**Best for:** Pre-first-time experiences (kickoff meetings, employer conversations, team conflicts). Students experience a simplified version of the real thing and practice interpreting what happens.

**Structure:**
1. Context setup (who you are, what's happening, what you know going in)
2. Stimulus (what someone said, what happened, what you're looking at)
3. Interpretation questions (what does this mean, what should you do, what's actually going on)
4. Per-question feedback with explanation

**Example:** Week 3 kickoff scenario. Students read a simulated employer's statements and determine what was actually confirmed vs. what they're assuming.

### Type 2: Critical Evaluation Exercise

A piece of work product (AI output, a draft, a data summary) that students review and annotate.

**Best for:** Building the habit of reviewing critically rather than accepting at face value. Works well for AI literacy, peer review skills, and quality standards.

**Preferred interaction model: Click-to-highlight with action selection.** The artifact is displayed as continuous text. Each sentence or clause is a clickable element. Students read through and click on parts they think need attention. When they click, action options appear (e.g., "Look up this source," "Find the original data," "Check for more recent information"). Items they don't click are implicitly treated as "no action needed." After submission, feedback covers what they flagged correctly, what action they chose, and what they missed.

**Fallback interaction model:** Present each passage sequentially and ask students to choose an action (including "No action needed").

**Structure:**
1. Context setup (what this artifact is, who produced it, what it's supposed to do)
2. The artifact itself (the AI-generated summary, the draft section, the data)
3. Annotation map: each reviewable passage with its expected action, feedback if caught, and feedback if missed
4. Debrief summarizing results and tying back to real-world application

**Example:** Week 2 AI evaluation exercise. Students review an AI-generated research summary and decide what action each claim requires: confirm at the source, look up a citation, find original data, check for recency, question relevance, or no action needed.

### Type 3: Prioritization Exercise

A set of options or tasks that students must rank, select, or triage under constraints.

**Best for:** Decision-making under time pressure or resource constraints. Works well for question prioritization before meetings, scope decisions, and task management.

**Structure:**
1. Context setup (what you're working with, what the constraints are)
2. The options (a list of questions, tasks, or items to evaluate)
3. Prioritization questions (which ones matter most, what would you cut, what's the right order)
4. Per-question feedback explaining the reasoning behind the recommended prioritization

**Example:** Given 10 questions and 20 minutes left in a meeting, which 4 do you ask? Why?

---

## Source Document Format

Each interactive element is documented as a markdown file. This is the source of truth — everything needed to build the interactive in any tool.

**File naming:** `page[N]-[short-title]-interactive.md` (stored in `weekly_content/week[NN]/`)

**Structure:**

```markdown
---
week: [N]
page: [N]
title: [Interactive title]
type: interactive-source
interactive_type: [simulated-scenario | critical-evaluation | prioritization]
estimated_time: [N] min
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: draft | review | final
---

# [Interactive Title]

## Purpose

[1–2 sentences: what skill this practices, what it prepares students for,
and why interactive practice is better than reading about it.]

## Interaction Model

[Describe how the student interacts with the content. What do they see?
What do they click/select/drag? What happens when they respond? What
does submission look like? Include a fallback format for simpler tools.]

## Context Setup

[The setup text students see before the interaction. Sets the scene:
who they are, what's happening, what they know going in. Written in
second person, warm mentor tone.]

## Stimulus

[The artifact, scenario, or situation students are responding to.
For a simulated scenario: what the employer said, what happened.
For a critical evaluation: the full text of the artifact being evaluated.
For a prioritization: the list of items to evaluate.]
```

**For question-based interactives (simulated scenarios, prioritization):**

```markdown
## Questions

### Question 1

**Question text:** [The question as students will see it]

**Type:** [multiple-choice | select-all | ranking]

**Options:**
- A) [Option text]
- B) [Option text]
- C) [Option text]
- D) [Option text]

**Correct answer:** [Letter(s)]

**Feedback if correct:** [Explanatory feedback]

**Feedback if incorrect:** [Per-option explanatory feedback.
Warm and instructive, not punitive.]

### Question 2
[Same structure]

[3–5 questions total]
```

**For annotation-based interactives (critical evaluation):**

```markdown
## Annotation Map

[Note: Passages not listed here have no expected action.
Students who click on them should see a brief "no action needed" message.]

### Passage 1: "[Exact text of the clickable passage]"

**Should be flagged:** [Yes | No]
**Expected action:** [The action category, or "No action needed"]
**Feedback:** [Shown when the student flags this passage
and selects the correct action]
**Feedback if not flagged:** [Shown after submission if the student
missed this passage. Explains what they should have noticed.]
**Feedback if flagged with wrong action:** [Optional. Shown if they
flagged it but chose the wrong action category.]

### Passage 2: "[Exact text]"
[Same structure]
```

**All interactives end with:**

```markdown
## Debrief

[2–3 sentences shown after submission. Summarize results if applicable
(e.g., "You flagged X of Y passages that needed attention"). Tie the
practice back to the real situation students will face.]
```

---

## Design Process

### Step 1: Identify the skill and the stakes

Read the development plan and design doc. Answer:

- What skill is this interactive practicing?
- What real situation does it prepare students for?
- What's the most common mistake students will make in the real situation?

The most common mistake becomes the foundation for your wrong answers. Good distractors aren't random — they represent the specific errors students are likely to make.

### Step 2: Choose the interaction model

Before writing content, decide how students will interact with it. The interaction model should mirror the real task (Design Principle 3). Common models:

- **Click-to-highlight with action selection** — for document review and evaluation tasks. Students read continuous text and click on parts that need attention.
- **Narrative with decision points** — for simulated scenarios. Students read a situation and choose how to respond at key moments.
- **Drag-and-sort or ranking** — for prioritization tasks. Students arrange items by importance or sequence.
- **Sequential questions** — fallback for any type when the build tool doesn't support richer interactions.

Always specify a fallback format in the source document.

### Step 3: Build the scenario or artifact

For simulated scenarios, write a realistic situation based on the design doc's activity descriptions. Make it specific enough to feel real but generic enough that it doesn't depend on a particular project or employer. Use fictional company names so students don't confuse the scenario with their actual assignment.

For critical evaluation exercises, create the artifact (AI output, draft, summary) with deliberate problems embedded. The problems should be realistic (the kind of errors that would actually occur, not obvious mistakes no one would miss). Include items that don't need action. A mix of genuine problems, things that need checking, and things that are fine teaches judgment, not blanket skepticism (Design Principle 5).

For prioritization exercises, create a list of options that includes clear must-dos, reasonable but lower-priority items, and plausible distractors.

### Step 4: Write the questions or annotation map

**For question-based interactives:**

Write 3–5 questions, each testing a different aspect of the skill. Avoid questions that test the same thing in different words.

- **Make wrong answers tempting.** The best distractors represent specific mistakes students are likely to make. "All of the above" is lazy. A distractor that represents a common misconception is useful.
- **Test interpretation, not recall.** "What did the employer say?" is recall. "What did the employer actually commit to?" is interpretation. Aim for interpretation.
- **One clearly best answer per question.** Avoid questions where two options are both defensible. Students should walk away confident about what the right answer is and why.
- **Keep options concise.** Long answer options make the exercise feel like a reading comprehension test rather than practice.

**For annotation-based interactives:**

Break the stimulus into reviewable passages. For each passage, document whether it should be flagged, what the expected action is, and what category of action it represents. Use specific, educational action categories rather than generic trust levels (Design Principle 4). Good action categories name a skill: "Look up this source," "Find the original data," "Check for more recent information," "Question the relevance."

### Step 5: Write feedback for every response path

**For question-based interactives:** Every answer choice gets feedback, not just the correct one.

**For annotation-based interactives:** Every passage gets three types of feedback:
- Feedback when correctly flagged with the right action
- Feedback when flagged with the wrong action (if applicable)
- Feedback when missed (shown after submission)

The "feedback if missed" is where some of the best learning happens (Design Principle 6). Students discover blind spots they didn't know they had.

All feedback should be:

- **Explanatory.** Don't just say "Correct!" or "Incorrect." Explain why.
- **Instructive on wrong answers or missed items.** Tell students what they missed or what assumption led them astray.
- **Warm, not punitive.** "Good instinct to be thorough, but..." not "Wrong."
- **Connected to the real situation.** Where possible, explain why this distinction matters in practice.

### Step 6: Write the debrief

A short closing statement (2–3 sentences) shown after submission. For annotation-based interactives, include a results summary (e.g., "You flagged X of Y passages that needed attention"). Tie the practice back to the real situation and name the specific skills or moves that students practiced. The debrief should leave students with a mental checklist they can carry forward.

### Step 7: Review against time budget

The full interactive (context + stimulus + interaction + reading feedback) should fit within the time budget from the development plan (typically 5–10 minutes). If it's running long, cut passages or questions rather than rushing the feedback. Feedback quality matters more than quantity of items.

---

## Quality Checks

Before considering an interactive element complete:

- [ ] It feels like practice, not a quiz. Students are doing the task, not answering questions about the task.
- [ ] The interaction model mirrors the real task students are preparing for
- [ ] Preferred interaction model and fallback format are both specified
- [ ] Purpose is clear: the interactive practices a specific skill, not general knowledge
- [ ] Context setup is specific enough to feel real, generic enough to work for any team/project
- [ ] Uses fictional company/scenario names so students don't confuse it with their actual assignment
- [ ] Includes items that don't need action (for evaluation exercises) so the mix is realistic
- [ ] Action categories are specific and educational, not generic trust levels
- [ ] Every response path has explanatory feedback (correct, incorrect, and missed)
- [ ] Feedback is warm and instructive, not punitive
- [ ] Debrief summarizes results and ties the practice back to the real upcoming situation
- [ ] Total estimated time fits within the development plan's budget
- [ ] Voice is consistent with the rest of the course content (warm mentor)
- [ ] No week numbers or hardcoded course specifics in student-facing text
- [ ] YAML frontmatter is complete
