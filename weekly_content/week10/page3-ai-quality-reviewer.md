---
week: 10
page: 3
title: AI as a quality reviewer
created: 2026-04-21
last_updated: 2026-04-21
status: draft
competencies:
  - area: Critical Thinking
    subskill: Prioritization
---

# Using AI as a quality reviewer

Professional work usually has a moment before something goes out the door when someone else reads it first. A colleague, an editor, a sharp teammate who hasn't been buried in the draft for three weeks and can still see it fresh. The point of that second read is to catch what the producer can't catch anymore, because they're too close to the work.

This week you learn to use AI in that role. Your team has complete enough draft content to evaluate as a whole. AI as a quality reviewer is what you use in that moment.

This is also the last new AI skill the course introduces. From here, you apply the full toolkit you've built (research prompting, Socratic partner, production partner, and now quality reviewer) independently through the remaining phases of the course.

---

## What the quality reviewer role is

AI in this role is different from AI as a production partner, which you met last week. Production partner helps while you're building: drafting a section, refining a paragraph, stress-testing a recommendation. Quality reviewer happens after you have something complete enough to evaluate.

You hand AI a complete draft or section and ask for evaluation. What comes back is a list of things to examine, not a rewrite.

Four things quality review is good at:

- **Reading for consistency across sections.** Team-produced documents often drift. Voice shifts between authors, terminology changes mid-way through, the same concept gets defined differently in two places. AI is good at catching these seams because it reads the whole document in one pass, which no single teammate does.
- **Flagging logical gaps and unsupported claims.** Anywhere a section asserts something without grounding it in evidence or prior setup, AI will usually notice. It won't always be right that the gap is real, but it's a useful list to examine.
- **Identifying tone mismatches.** Sections written under different pressures often carry different registers. A rushed section may sound abrupt; a heavily-edited one may sound overqualified. Both read awkwardly next to each other.
- **Surfacing where an unfamiliar reader would lose the thread.** This is the one AI does best. You and your teammates are saturated in this project; an unfamiliar reader isn't. AI can simulate that unfamiliar reader more reliably than anyone on your team can at this point.

---

## Prompt strategies

Three prompt templates you can adapt to your own draft.

**Fresh reader**
> Read this document as someone who has never heard of this project or client. Where do you get lost? Where do you have to re-read? Be specific about the paragraph or sentence.

**Consistency check**
> Does this read as one coherent piece, or like sections written by different people? Flag the seams: voice shifts, terminology drift, structural gaps. Point to specific passages.

**Weakest-link analysis**
> What are the three weakest points in this argument? Be specific about why each is weak. Is it the evidence, the reasoning, the scope, or the framing?

What to do with the output: treat AI's list as questions to investigate, not verdicts to act on. Your team still makes the judgment call on each flagged item. Some flags will be real. Others will be AI noticing a surface inconsistency that's actually intentional. The point of the exercise is to surface a list. Your team decides what's on it.

---

## Working with AI well in this role

Two moves that consistently improve the output.

**Give the model explicit permission to say nothing.** LLMs default to being helpful. Hand a solid section to a model and ask what's wrong with it, and the model will generate critique even when there's nothing substantive to critique. Add a line to your prompt: "If this section is working, say so and move on." Models respond well to being released from the expectation of finding problems.

**Use more than one model if the stakes are high.** Different LLMs surface different things. Running your draft through two models shows the overlap (usually the real issues) and the divergence, which is often useful in itself. Differences reveal what each model is more or less sensitive to. You don't have to act on every flag from either.

---

## When to use quality review this week

The production block and the internal review gate are where this tool first earns its place. Before your team runs the internal review gate manually, try the fresh reader prompt on your assembled sections. Whatever the model flags becomes input to the review. Anywhere your team notices the same issue independently, that's a real problem. Anywhere the model flags something your team doesn't see, decide whether the model is catching a seam or generating noise.

Using AI this way is also the warm-up for the remaining weeks. The near-final package, the final deliverables submission, and the final presentation all benefit from a fresh-reader pass before they leave your team. This week is the first chance to build the habit.
