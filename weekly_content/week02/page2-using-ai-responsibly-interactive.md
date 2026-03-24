---
week: 2
page: 2
title: Review This AI Output — What's Your Next Move?
type: interactive-source
interactive_type: critical-evaluation
estimated_time: 5 min
created: 2026-03-19
last_updated: 2026-03-19
status: draft
---

# Review This AI Output — What's Your Next Move?

## Purpose

This exercise practices the skill of reviewing AI-generated research the way a professional would: reading each claim and knowing what to do with it. The goal isn't just to spot errors. It's to build a repertoire of specific moves you can apply whenever you're working with AI output: checking for hallucinations, questioning relevance, looking for fresher data, tracking down original sources. Students practice choosing the right move for each situation.

## Interaction Model

**Format: Click-to-highlight with action selection.**

The passage is displayed as continuous text. Each sentence or clause is a clickable element. Students read through the passage and click on any part they think needs attention before they'd trust it in their own work. When they click, the action options appear for that passage. Passages they don't click are implicitly treated as "no action needed."

After the student has finished reviewing, they submit and receive feedback on:
- Passages they correctly flagged, with confirmation of the right action
- Passages they flagged but assigned the wrong action, with an explanation of the better choice
- Passages they missed that should have been flagged, with an explanation of what to watch for

This should feel like reviewing a document at your desk, not answering a quiz. Students decide which parts to engage with, not just respond to pre-selected prompts.

**Fallback format:** If the build tool doesn't support click-to-highlight, present each passage sequentially and ask students to choose an action (including "No action needed — looks fine").

## Context Setup

Your team has been matched with GreenPath Solutions, a mid-size company that provides sustainability consulting to retail businesses. Before your kickoff meeting, you asked an AI tool to help you learn about the company and its industry.

Below is what AI returned. Read through it the way you would before putting any of this into your own work. Click on any passage you think needs attention, and choose what you'd do with it.

**Your action options (shown when you click a passage):**

- **No action needed** — This is general enough to work with. Low risk.
- **Confirm on their website** — Basic facts that are easy to check at the source.
- **Look up this source** — A specific organization, report, or citation is mentioned. Verify it exists.
- **Find the original data** — A specific number or statistic is cited. Track down where it actually comes from.
- **Check for more recent information** — This may be outdated. Look for what's current.
- **Question the relevance** — This might be true, but is it actually useful for your specific situation?

## Stimulus

> **GreenPath Solutions — Company Overview**
>
> GreenPath Solutions is a sustainability consulting firm founded in 2016, headquartered in Portland, Oregon. The company works primarily with mid-size retail businesses to help them reduce their environmental footprint through supply chain optimization, waste reduction programs, and sustainability reporting.
>
> The company has grown rapidly, expanding from 12 employees at launch to over 200 staff across three offices in the Pacific Northwest. According to a 2023 report by the National Sustainability Consulting Association, GreenPath ranks among the top 15 sustainability consultancies in North America by revenue.
>
> The retail sustainability consulting market is valued at approximately $4.2 billion and is projected to grow at 12% annually through 2030, driven by increasing consumer demand for environmentally responsible brands and tightening ESG reporting regulations in the US and EU. GreenPath's primary competitors include EcoVadis, Anthesis Group, and South Pole, all of which operate at a significantly larger global scale.
>
> GreenPath differentiates itself through its focus on mid-market retailers, a segment that larger consultancies tend to overlook. Their proprietary assessment framework, the Retail Sustainability Scorecard, has been adopted by over 300 retail clients since its launch in 2019. The company's CEO, Maria Chen, was named to the GreenBiz 30 Under 30 list in 2017 and has spoken at SXSW and the Aspen Ideas Festival on the intersection of retail and sustainability.
>
> Recent developments include a Series B funding round of $18 million in late 2024 and a partnership with Walmart's supplier sustainability program announced in early 2025.

## Annotation Map

Below is every clickable passage in the stimulus text, with its expected action and feedback. Passages not listed here have no expected action (students who click on them should see: "No action needed. This part of the summary is general enough to work with.").

### Passage 1: "GreenPath Solutions is a sustainability consulting firm founded in 2016, headquartered in Portland, Oregon."

**Should be flagged:** Yes
**Expected action:** Confirm on their website
**Feedback:** Founding dates and headquarters locations can be slightly off in AI output. It takes 30 seconds to pull up the company's About page and confirm. Get in the habit of checking basic facts at the source. If you walk into the kickoff and say "You were founded in 2016, right?" and the answer is 2014, you've shown you didn't look at their website.
**Feedback if not flagged:** This looks straightforward, but founding dates and locations are worth a quick check. AI sometimes gets basic facts slightly wrong, and your employer will notice if you repeat incorrect details about their own company.

### Passage 2: "The company works primarily with mid-size retail businesses to help them reduce their environmental footprint through supply chain optimization, waste reduction programs, and sustainability reporting."

**Should be flagged:** No
**Expected action:** No action needed
**Feedback if flagged:** Good instinct to be thorough, but this is general service description language. Even if the exact phrasing doesn't match their website word for word, it's low-risk and useful for orienting yourself. You'll learn the precise details at the kickoff.

### Passage 3: "expanding from 12 employees at launch to over 200 staff across three offices in the Pacific Northwest"

**Should be flagged:** Yes
**Expected action:** Confirm on their website
**Feedback:** Specific growth numbers like these are easy for AI to fabricate. A quick check on LinkedIn or the company's website can confirm their approximate size. Getting team size wrong isn't a disaster, but quoting a number confidently when it's off makes you look like you didn't do real research.
**Feedback if not flagged:** Specific numbers about team size and office count are the kind of details AI sometimes gets wrong. Worth a quick check on LinkedIn or the company website so you're working with accurate information.

### Passage 4: "According to a 2023 report by the National Sustainability Consulting Association, GreenPath ranks among the top 15 sustainability consultancies in North America by revenue."

**Should be flagged:** Yes
**Expected action:** Look up this source
**Feedback:** This is the move whenever AI cites a specific organization or report. The "National Sustainability Consulting Association" sounds official, but AI frequently invents professional associations and industry reports. Search for the organization. If you can't find it, the citation is almost certainly fabricated. The specificity ("top 15," "by revenue," "2023 report") makes it feel credible, which is exactly what makes hallucinated sources dangerous.
**Feedback if not flagged:** This is the most important passage to catch. The "National Sustainability Consulting Association" may not be a real organization. AI routinely invents official-sounding sources, complete with specific dates and rankings. Always verify that a cited source exists before you trust or repeat the claim.

### Passage 5: "The retail sustainability consulting market is valued at approximately $4.2 billion and is projected to grow at 12% annually through 2030"

**Should be flagged:** Yes
**Expected action:** Find the original data
**Feedback:** Whenever AI gives you a specific number, your next move is to find where it came from. AI generates market figures that sound precise but are often blended from multiple sources, rounded, or fabricated. If you find a market research report that matches, great. If you can't trace it to a source, don't use it. The general direction (growing market, driven by ESG regulation) is easier to verify and probably more useful than a dollar figure you can't back up.
**Feedback if not flagged:** Precise-sounding statistics are one of AI's most convincing tricks. "$4.2 billion at 12% CAGR" reads like it came from a research report, but AI may have generated it to sound authoritative. If a number matters to your work, track down the original source.

### Passage 6: "GreenPath's primary competitors include EcoVadis, Anthesis Group, and South Pole, all of which operate at a significantly larger global scale."

**Should be flagged:** Yes
**Expected action:** Question the relevance
**Feedback:** These are real companies in the sustainability space, so they're not hallucinated. But read the claim carefully: it says they "operate at a significantly larger global scale." If GreenPath focuses on mid-size retailers and these companies are global enterprises, are they actually competing for the same clients? AI tends to list the most prominent names in a sector rather than the most relevant competitors. Ask your employer at the kickoff who they actually see as competitors. That answer will be more useful than anything AI can give you.
**Feedback if not flagged:** The companies are real, so it's easy to skim past this. But the summary itself tells you they operate at a "significantly larger global scale." That's a clue that they might not be real competitors for a mid-market-focused firm. AI lists famous names. Your employer can tell you who they actually compete with.

### Passage 7: "GreenPath differentiates itself through its focus on mid-market retailers, a segment that larger consultancies tend to overlook."

**Should be flagged:** No
**Expected action:** No action needed
**Feedback if flagged:** Being thorough is good, but this is general strategic framing that's consistent with the rest of the summary. The idea (mid-market focus as a differentiator) is low-risk. You can bring it into your kickoff conversation and let the employer refine it. Part of reviewing AI output well is knowing when something is good enough to use.

### Passage 8: "Their proprietary assessment framework, the Retail Sustainability Scorecard, has been adopted by over 300 retail clients since its launch in 2019."

**Should be flagged:** Yes
**Expected action:** Confirm on their website
**Feedback:** Proprietary frameworks, product names, and adoption numbers are specific enough to check and specific enough to be wrong. AI sometimes invents product names or inflates numbers. A quick look at the company's website will tell you if the "Retail Sustainability Scorecard" actually exists and how they describe it.
**Feedback if not flagged:** Specific product names and adoption numbers are worth checking. AI can invent plausible-sounding frameworks and tools. If you reference the "Retail Sustainability Scorecard" at the kickoff and it doesn't exist, that's awkward.

### Passage 9: "The company's CEO, Maria Chen, was named to the GreenBiz 30 Under 30 list in 2017 and has spoken at SXSW and the Aspen Ideas Festival."

**Should be flagged:** Yes
**Expected action:** Check for more recent information
**Feedback:** Two things to check. Is Maria Chen still the CEO? People change roles, and AI may be working with outdated information. A quick LinkedIn search will tell you. Also, the "30 Under 30" mention is from 2017, almost a decade ago. AI often surfaces historical details alongside current information without flagging how old they are. Find out who you're actually meeting with and what their current role is. That matters more for your kickoff than a 2017 award.
**Feedback if not flagged:** Biographical details are easy to skim past, but they go stale fast. The "30 Under 30" mention is from 2017. Is Maria Chen still the CEO? Has the company's leadership changed? Always check that the people AI tells you about are still in the roles it describes.

### Passage 10: "Recent developments include a Series B funding round of $18 million in late 2024 and a partnership with Walmart's supplier sustainability program announced in early 2025."

**Should be flagged:** Yes
**Expected action:** Check for more recent information
**Feedback:** When AI says "recent," always ask: recent relative to what? AI's training data has a cutoff, so events described as recent may be outdated or fabricated. A quick news search will tell you whether the funding round and partnership actually happened. If they're real, they're great context for your kickoff. If you can't find them, don't bring them up. Mentioning events that didn't happen would not build confidence with your employer.
**Feedback if not flagged:** Anything AI labels as "recent" deserves scrutiny. AI's training data has a cutoff date, and it sometimes generates plausible-sounding recent events that never happened. Always verify before referencing recent developments with your employer.

## Debrief

**Shown after submission with a summary of results (e.g., "You flagged 6 of 8 passages that needed attention and chose the right action for 5 of them").**

That passage had 10 reviewable segments. Eight needed some kind of attention. Two were fine to use. You just practiced six different evaluation moves: confirming basic facts at the source, looking up cited sources, tracking down original data, questioning relevance, recognizing when something is good enough to use, and checking for more recent information. Not every claim needed the same response, and that's the point. The skill isn't blanket skepticism. It's knowing which move to make for which kind of claim. When you use AI for research in this course, read every piece of output with this same question in mind: what's my next move with this?
