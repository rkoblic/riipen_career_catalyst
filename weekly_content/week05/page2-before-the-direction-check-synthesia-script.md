---
week: 5
page: 2
title: When the Direction Shifts — Pushback Video Script
type: synthesia-script
character: David Park, Director of Community Programs, Bridgeway Community Health
estimated_runtime: 1:30 at ~150 wpm
created: 2026-05-13
status: ready for Synthesia
---

# Direction Check Pushback Script — David Park

Synthesia avatar script for the Week 5 interactive ("When the direction shifts"). Returning character from the Week 3 kickoff video. This is the moment, mid-meeting, where David pushes back on the team's research framing. Students watch, then answer questions about what he actually said versus what they might be assuming.

## Production notes

- **Same avatar as Week 3.** Continuity matters — David is a recurring character across the project arc. Reuse the same avatar, voice, and background from `Kickoff Meeting with David Park.mp4` if possible.
- **Register**: Warm but firm. Respectful pushback, not aggressive criticism. He's the kind of director who has done this many times — he's not nervous about giving feedback, but he's also not enjoying it. Think experienced manager delivering an honest note.
- **Pacing**: ~150 wpm. The natural pauses ("OK. So...", "And honestly...") need real breathing room — they're moments of thought, not stutters. Don't let the avatar rush through them.
- **In media res — no greeting.** This is not the top of a meeting. David has just listened to the team present for several minutes; he's now responding. The video should open with him in a posture of having just listened (a small beat, maybe a slight nod), and then he begins. Do NOT have him say "Hi team" or "Thanks for that" or any framing — the interactive's on-page context already places the student inside the meeting.
- **End on the last word, no wrap-up.** The video should end with "I'd like to know what your plan is there." No "I'll let you respond" or closing flourish. The natural beat after his last sentence — the silence where the team has to decide what to say — is the emotional center of the exercise. The interactive immediately follows with Q1, which functionally fills that beat.
- **Tone check before committing to full render.** This is a harder register than the Week 3 kickoff. Generate Section 1 first as a 30-second test. Watch for: does the avatar sound passive-aggressive (bad), robotic (bad), or like a director giving an honest note (good)? Adjust voice/avatar selection before generating the full video.
- **No on-screen text overlays.** Same as Week 3 — captions for accessibility are fine, but no section labels or visual signposting.

## Script

### Section 1 — Acknowledgement and the pivot

OK. So... I want to start by saying I appreciate the rigor here. The framework you're describing is one I've come across before — it's well-grounded work. But I do want to push back a little, because I'm not sure it's the right starting point for us.

### Section 2 — The critique

A lot of what I'm reading in your draft is grounded in research with general adult populations. And that work matters — I'm not dismissing it. But most of our participants don't fit those samples. We've had community health educators working with these specific communities for years now, and they've built up a lot of knowledge about what actually shifts behavior here. What worries me is that if your recommendations are mostly built from the outside literature, we'll end up with something that's intellectually sound but doesn't reflect what our team already knows works on the ground.

### Section 3 — The ask

Now — I don't want you to walk away thinking we're starting from scratch. That's not what I'm asking. What I'd like to see is how you're going to weigh what our educators have told you against what the literature says. And honestly... if you haven't talked to them yet, I'd like to know what your plan is there.

## What the script is testing (for reference — don't include in the video)

Each question in the interactive maps to specific phrases students need to catch by ear:

| Question | Listening target | Key phrases in the script |
|---|---|---|
| Q1 — What is David pushing back on | The *relevance* of the source material, not the methodology | "I appreciate the rigor here," "general adult populations," "most of our participants don't fit those samples," "what actually shifts behavior here" |
| Q2 — Best next response | Ask a clarifying question before defending or pivoting | (Tests team behavior, not a specific phrase — but option C connects to David's "weigh what our educators have told you") |
| Q3 — Best note version | Capture exact language, not paraphrase | "I'd like to see how you're going to weigh what our educators have told you against what the literature says" |
| Q4 — Teammate wants to scrap everything | David did NOT ask for a full rebuild | "I don't want you to walk away thinking we're starting from scratch," "What worries me is..." |
| Q5 — Summary phrasing | Captures the specific ask, not the emotional shape | "weigh what our educators have told you against what the literature says" |

If you adjust the script during recording, make sure the bolded phrases still land — the feedback strings in the interactive quote them directly.

## What's different from the original text version

The text version used three phrases that read clearly but would sound too rehearsed when spoken aloud — they'd telegraph the right answer:

- "I'm not saying scrap what you have" → "I don't want you to walk away thinking we're starting from scratch" (same meaning, less neon)
- "I'm worried that..." → "What worries me is..." (more reflective, more spoken-English natural)
- "weight what our educators have told you" → "weigh what our educators have told you" (the verb "weigh" is more conversational than "weight")

The feedback strings in `page2-before-the-direction-check-interactive.html` have been updated to quote the new phrasing.

## What just happened (text card after the video)

The interactive shows this framing on a separate screen after the video, before the questions begin:

> **What just happened**
>
> Your team had not planned to consult the community health educators. That wasn't in the original scope, and primary research was excluded at the kickoff. Your team has been working primarily from secondary research.

This is meta-narration (the teacher pulling the curtain back, not David speaking), so it stays as a text card rather than being added to the video.

## File destination

When the MP4 is generated, upload to Riipen's S3 bucket alongside the Week 3 video. Suggested filename:
```
Direction Check with David Park.mp4
```

Resulting URL pattern:
```
https://riipen-product.s3.ca-central-1.amazonaws.com/career-catalyst/Direction+Check+with+David+Park.mp4
```

Update the `videoSrc` field in `page2-before-the-direction-check-interactive.html` once uploaded. Captions can be burned in (same as Week 3) — no separate `.srt` / `.vtt` file needed.
