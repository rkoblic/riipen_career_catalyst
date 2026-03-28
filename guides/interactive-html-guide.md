# Interactive HTML Build Guide

How to convert interactive element source documents into self-contained HTML files for Riipen Career Catalyst.

This guide provides the component library, JavaScript architecture, and production process for turning interactive source documents (markdown files with scenarios, questions, and feedback) into working HTML files hosted on Amazon S3. These are NOT Canvas pages — they live outside Canvas and are linked from Canvas pages via the interactive placeholder component.

---

## Context

Interactive HTML files are:

- **Self-contained single HTML files** with no external dependencies except Google Fonts (DM Sans)
- **Hosted on Amazon S3** as static files
- **Linked from Canvas pages** via the interactive placeholder component (see the [Canvas Page HTML Guide](canvas-html-guide.md), Component 17)
- **Opened in a new tab** — students click a link in Canvas that opens the interactive separately
- **Responsive** — must work on both mobile and desktop
- **Accessible** — must meet WCAG AA requirements

Because these files live on S3 (not inside Canvas), they are NOT subject to Canvas constraints. They CAN use `<style>` blocks, JavaScript, CSS classes, media queries, and any standard web technology.

---

## Interactive Types

The [Interactive Element Guide](interactive-element-guide.md) defines three interactive types:

1. **Simulated Scenario** — a realistic situation presented as a narrative with decision points and sequential multiple-choice questions
2. **Critical Evaluation** — a document or artifact that students review, with click-to-highlight and action selection (fallback: sequential questions)
3. **Prioritization** — a set of items students rank, sort, or triage under constraints (fallback: sequential multiple-choice)

This guide covers the **sequential multiple-choice format**, which serves as the fallback for all three types. This is the simplest format to build and covers the majority of use cases. Richer interaction models (drag-and-drop card sorting, click-to-highlight document review) can be layered on later using the same page shell and brand styling.

For the click-to-highlight interaction model used in critical evaluation exercises, refer to the Week 2 AI evaluation interactive (`weekly_content/week02/page2-using-ai-responsibly-interactive.html`) as the reference implementation.

---

## Constraints & Hosting

- **Single file, self-contained.** All CSS goes in a `<style>` block, all JS goes in a `<script>` block. No external JS or CSS libraries. The only external dependency is Google Fonts for DM Sans.
- **No server-side logic.** Pure static HTML/CSS/JS. The file must work when opened directly from an S3 URL or from the local filesystem.
- **No frameworks.** Vanilla JS only. No React, Vue, jQuery, or other libraries.
- **File naming:** `week[NN]-[short-title]-interactive.html` (stored in `weekly_content/week[NN]/`)

---

## Brand Styling

### Colors

```
--orange:          #ff7c0a     Primary brand accent, submit button, progress bar
--dark-blue:       #050c2a     Primary text color
--electric-blue:   #2454ff     Selected state, links
--green:           #18733e     Correct feedback text/border
--purple:          #7c3aed     Scenario accent, stimulus card border
--grey-bg:         #f7f8fa     Page background, context cards
--border:          #e2e4e9     Card borders
--muted:           #6b7280     Secondary text, labels
--correct-bg:      #f0faf4     Correct feedback background
--correct-border:  #b8e6cc     Correct feedback border
--incorrect-bg:    #fff3f3     Incorrect feedback background
--incorrect-border:#ffc9c9     Incorrect feedback border
--white:           #ffffff     Card backgrounds
```

### Typography

- **Font:** DM Sans from Google Fonts
- **Body text:** 14-15px, line-height 1.7
- **Title:** 26px, bold (700)
- **Section labels:** 11-12px, uppercase, letter-spacing 2px
- **Max width:** 680px, centered

---

## Page Shell

Every interactive HTML file starts with this structure. Copy this as the starting template.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Interactive Title] — Riipen Career Catalyst</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
<style>
  :root {
    --orange: #ff7c0a;
    --dark-blue: #050c2a;
    --electric-blue: #2454ff;
    --green: #18733e;
    --purple: #7c3aed;
    --grey-bg: #f7f8fa;
    --border: #e2e4e9;
    --muted: #6b7280;
    --correct-bg: #f0faf4;
    --correct-border: #b8e6cc;
    --incorrect-bg: #fff3f3;
    --incorrect-border: #ffc9c9;
    --white: #ffffff;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: 'DM Sans', sans-serif;
    color: var(--dark-blue);
    background: var(--white);
    line-height: 1.7;
  }

  /* ── Container ── */

  .container {
    max-width: 680px;
    margin: 0 auto;
    padding: 40px 24px 60px;
  }

  /* ── Header ── */

  .header {
    border-bottom: 2px solid var(--orange);
    padding-bottom: 16px;
    margin-bottom: 32px;
  }

  .header .label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--orange);
    font-weight: 600;
    margin-bottom: 6px;
  }

  .header h1 {
    font-size: 26px;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 6px;
    color: var(--dark-blue);
  }

  .header .subtitle {
    font-size: 14px;
    color: var(--muted);
    font-style: italic;
  }

  /* ── Context Card ── */

  .context-card {
    background: var(--grey-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 24px;
    margin-bottom: 24px;
    font-size: 14.5px;
    line-height: 1.7;
  }

  .context-card p + p {
    margin-top: 12px;
  }

  /* ── Progress Bar ── */

  .progress-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
  }

  .progress-text {
    font-size: 13px;
    color: var(--muted);
    white-space: nowrap;
    min-width: 80px;
  }

  .progress-bar {
    flex: 1;
    background: var(--border);
    height: 4px;
    border-radius: 2px;
    overflow: hidden;
  }

  .progress-fill {
    background: var(--orange);
    height: 100%;
    width: 0%;
    transition: width 0.3s ease;
    border-radius: 2px;
  }

  /* ── Stimulus Card ── */

  .stimulus-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-left: 4px solid var(--purple);
    border-radius: 0 10px 10px 0;
    padding: 20px 24px;
    margin-bottom: 24px;
    font-size: 14.5px;
    line-height: 1.7;
  }

  .stimulus-card .stimulus-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--purple);
    font-weight: 600;
    margin-bottom: 8px;
  }

  .stimulus-card p + p {
    margin-top: 12px;
  }

  /* ── Question Prompt ── */

  .question-prompt {
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 16px;
    line-height: 1.5;
  }

  /* ── Answer Options ── */

  .options-group {
    list-style: none;
    margin-bottom: 20px;
  }

  .option-btn {
    display: block;
    width: 100%;
    background: var(--white);
    border: 1.5px solid var(--border);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 8px;
    font-size: 14px;
    font-family: 'DM Sans', sans-serif;
    color: var(--dark-blue);
    text-align: left;
    cursor: pointer;
    line-height: 1.5;
    transition: border-color 0.15s, background 0.15s;
  }

  .option-btn:hover:not(.disabled) {
    border-color: var(--electric-blue);
    background: #f5f7ff;
  }

  .option-btn:focus-visible {
    outline: 2px solid var(--electric-blue);
    outline-offset: 2px;
  }

  .option-btn.selected {
    border-color: var(--electric-blue);
    background: #eef2ff;
  }

  .option-btn.disabled {
    cursor: default;
    opacity: 0.7;
  }

  .option-btn .option-label {
    display: inline-block;
    font-weight: 700;
    min-width: 24px;
    margin-right: 6px;
  }

  /* ── Submit Button ── */

  .btn {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 600;
    padding: 12px 28px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: opacity 0.15s, background 0.15s;
  }

  .btn:focus-visible {
    outline: 2px solid var(--electric-blue);
    outline-offset: 2px;
  }

  .btn-submit {
    background: var(--orange);
    color: var(--dark-blue);
  }

  .btn-submit:hover:not(:disabled) {
    opacity: 0.9;
  }

  .btn-submit:disabled {
    opacity: 0.35;
    cursor: default;
  }

  .btn-next {
    background: var(--electric-blue);
    color: var(--white);
    margin-top: 16px;
  }

  .btn-next:hover {
    opacity: 0.9;
  }

  /* ── Feedback Panel ── */

  .feedback-panel {
    border-radius: 8px;
    padding: 20px 24px;
    margin-top: 16px;
    font-size: 14px;
    line-height: 1.7;
    display: none;
  }

  .feedback-panel.visible {
    display: block;
  }

  .feedback-panel.correct {
    background: var(--correct-bg);
    border-left: 4px solid var(--green);
  }

  .feedback-panel.incorrect {
    background: var(--incorrect-bg);
    border-left: 4px solid var(--incorrect-border);
  }

  .feedback-label {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }

  .feedback-label.correct {
    color: var(--green);
  }

  .feedback-label.incorrect {
    color: #dc2626;
  }

  .feedback-text {
    font-size: 14px;
  }

  /* ── Results Screen ── */

  .results-screen {
    display: none;
  }

  .results-screen.active {
    display: block;
  }

  .score-card {
    background: var(--dark-blue);
    color: var(--white);
    border-radius: 10px;
    padding: 28px 24px;
    text-align: center;
    margin-bottom: 24px;
  }

  .score-number {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 4px;
  }

  .score-label {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 16px;
  }

  .score-bar-container {
    background: rgba(255, 255, 255, 0.15);
    height: 8px;
    border-radius: 4px;
    overflow: hidden;
    max-width: 300px;
    margin: 0 auto;
  }

  .score-bar-fill {
    height: 100%;
    border-radius: 4px;
    background: var(--green);
    transition: width 0.5s ease;
  }

  /* Debrief */

  .debrief-card {
    background: var(--white);
    border: 2px solid var(--orange);
    border-radius: 10px;
    padding: 24px;
    margin-bottom: 24px;
    font-size: 14.5px;
    line-height: 1.7;
  }

  .debrief-card h3 {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 8px;
  }

  .debrief-card p + p {
    margin-top: 12px;
  }

  /* Review Section */

  .review-toggle {
    display: block;
    width: 100%;
    background: var(--grey-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 14px;
    font-family: 'DM Sans', sans-serif;
    color: var(--dark-blue);
    font-weight: 500;
    cursor: pointer;
    text-align: left;
    margin-bottom: 16px;
  }

  .review-toggle:focus-visible {
    outline: 2px solid var(--electric-blue);
    outline-offset: 2px;
  }

  .review-toggle::after {
    content: ' ▸';
  }

  .review-toggle.expanded::after {
    content: ' ▾';
  }

  .review-section {
    display: none;
  }

  .review-section.visible {
    display: block;
  }

  .review-item {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 12px;
  }

  .review-item .review-q-number {
    font-size: 12px;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
  }

  .review-item .review-prompt {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 10px;
  }

  .review-item .review-answer {
    font-size: 13px;
    margin-bottom: 4px;
  }

  .review-item .review-answer.yours {
    color: var(--dark-blue);
  }

  .review-item .review-answer.correct-answer {
    color: var(--green);
  }

  .review-item .review-feedback {
    font-size: 13px;
    color: var(--muted);
    margin-top: 8px;
    line-height: 1.6;
  }

  .review-item .review-badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 10px;
  }

  .review-badge-correct {
    background: var(--correct-bg);
    color: var(--green);
  }

  .review-badge-incorrect {
    background: var(--incorrect-bg);
    color: #dc2626;
  }

  /* Close note */

  .close-note {
    text-align: center;
    font-size: 13px;
    color: var(--muted);
    margin-top: 32px;
    padding-top: 20px;
    border-top: 1px solid var(--border);
  }

  /* ── Responsive ── */

  @media (max-width: 480px) {
    .container {
      padding: 24px 16px 40px;
    }
    .header h1 {
      font-size: 22px;
    }
    .option-btn {
      padding: 12px 14px;
    }
  }
</style>
</head>
<body>

<div class="container">

  <!-- Header -->
  <div class="header">
    <div class="label">Interactive Exercise</div>
    <h1 id="interactiveTitle"></h1>
    <div class="subtitle" id="interactiveSubtitle"></div>
  </div>

  <!-- Question Area (populated by JS) -->
  <div id="questionArea"></div>

  <!-- Results Screen -->
  <div class="results-screen" id="resultsScreen"></div>

</div>

<script>
// ─────────────────────────────────────────────
// DATA — Replace this object with real content
// ─────────────────────────────────────────────

const interactiveData = {
  title: "Interactive Title Here",
  subtitle: "About 5 minutes",
  context: "Context setup text. This is what students see before the first question. It sets the scene: who they are, what's happening, what they know going in. Written in second person, warm mentor tone.",
  stimulus: "", // Optional. For critical evaluation fallback, paste the artifact text here. Leave empty if not needed.
  questions: [
    {
      id: 1,
      prompt: "Question text as students will see it.",
      options: [
        { label: "A", text: "First answer option" },
        { label: "B", text: "Second answer option" },
        { label: "C", text: "Third answer option" },
        { label: "D", text: "Fourth answer option" }
      ],
      correctAnswer: "A",
      feedback: {
        correct: "Feedback shown when the student selects the correct answer. Explains why this is right.",
        incorrect: {
          "B": "Feedback for selecting option B. Explains what assumption led them astray.",
          "C": "Feedback for selecting option C.",
          "D": "Feedback for selecting option D."
        }
      }
    }
    // Add more question objects following the same structure
  ],
  debrief: "Debrief text shown after all questions. Summarizes what students practiced and ties it back to the real situation they're preparing for."
};


// ─────────────────────────────────────────────
// STATE
// ─────────────────────────────────────────────

let currentQuestion = 0;
let answers = []; // { questionId, selectedLabel, isCorrect }
let selectedOption = null;


// ─────────────────────────────────────────────
// INITIALIZATION
// ─────────────────────────────────────────────

function init() {
  document.getElementById('interactiveTitle').textContent = interactiveData.title;
  document.getElementById('interactiveSubtitle').textContent = interactiveData.subtitle;
  document.title = interactiveData.title + ' — Riipen Career Catalyst';
  renderContext();
}

function renderContext() {
  const area = document.getElementById('questionArea');
  let html = '';

  // Context card
  html += '<div class="context-card">';
  html += formatParagraphs(interactiveData.context);
  html += '</div>';

  // Stimulus card (if present)
  if (interactiveData.stimulus) {
    html += '<div class="stimulus-card">';
    html += '<div class="stimulus-label">Scenario</div>';
    html += formatParagraphs(interactiveData.stimulus);
    html += '</div>';
  }

  // Start button
  html += '<button class="btn btn-submit" onclick="startQuestions()" aria-label="Begin the exercise">Begin</button>';

  area.innerHTML = html;
}


// ─────────────────────────────────────────────
// QUESTION RENDERING
// ─────────────────────────────────────────────

function startQuestions() {
  currentQuestion = 0;
  answers = [];
  selectedOption = null;
  renderQuestion();
}

function renderQuestion() {
  const q = interactiveData.questions[currentQuestion];
  const total = interactiveData.questions.length;
  const area = document.getElementById('questionArea');

  selectedOption = null;

  let html = '';

  // Progress bar
  html += '<div class="progress-wrapper">';
  html += '  <span class="progress-text" aria-live="polite">Question ' + (currentQuestion + 1) + ' of ' + total + '</span>';
  html += '  <div class="progress-bar" role="progressbar" aria-valuenow="' + (currentQuestion + 1) + '" aria-valuemin="1" aria-valuemax="' + total + '">';
  html += '    <div class="progress-fill" style="width: ' + ((currentQuestion + 1) / total * 100) + '%"></div>';
  html += '  </div>';
  html += '</div>';

  // Stimulus card (persistent if present)
  if (interactiveData.stimulus) {
    html += '<div class="stimulus-card">';
    html += '<div class="stimulus-label">Scenario</div>';
    html += formatParagraphs(interactiveData.stimulus);
    html += '</div>';
  }

  // Question prompt
  html += '<div class="question-prompt" id="questionPrompt">' + escapeHtml(q.prompt) + '</div>';

  // Options
  html += '<div class="options-group" role="radiogroup" aria-labelledby="questionPrompt">';
  q.options.forEach(function(opt) {
    html += '<button class="option-btn" role="radio" aria-checked="false" ';
    html += 'data-label="' + opt.label + '" ';
    html += 'onclick="handleSelect(\'' + opt.label + '\')" ';
    html += 'tabindex="0">';
    html += '<span class="option-label">' + escapeHtml(opt.label) + '.</span> ';
    html += escapeHtml(opt.text);
    html += '</button>';
  });
  html += '</div>';

  // Submit button
  html += '<button class="btn btn-submit" id="submitBtn" onclick="handleSubmit()" disabled aria-label="Submit your answer">Submit</button>';

  // Feedback region
  html += '<div class="feedback-panel" id="feedbackPanel" role="status" aria-live="polite"></div>';

  area.innerHTML = html;

  // Focus management: move focus to the question prompt
  var prompt = document.getElementById('questionPrompt');
  prompt.setAttribute('tabindex', '-1');
  prompt.focus();

  // Keyboard navigation for options
  setupKeyboardNav();
}

function setupKeyboardNav() {
  var options = document.querySelectorAll('.option-btn');
  options.forEach(function(btn, index) {
    btn.addEventListener('keydown', function(e) {
      var target = null;
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
        e.preventDefault();
        target = options[(index + 1) % options.length];
      } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
        e.preventDefault();
        target = options[(index - 1 + options.length) % options.length];
      } else if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        btn.click();
      }
      if (target) target.focus();
    });
  });
}


// ─────────────────────────────────────────────
// INTERACTION HANDLERS
// ─────────────────────────────────────────────

function handleSelect(label) {
  // Don't allow changing answer after submission
  if (document.getElementById('feedbackPanel').classList.contains('visible')) return;

  selectedOption = label;

  // Update visual state
  document.querySelectorAll('.option-btn').forEach(function(btn) {
    var isSelected = btn.dataset.label === label;
    btn.classList.toggle('selected', isSelected);
    btn.setAttribute('aria-checked', isSelected ? 'true' : 'false');
  });

  // Enable submit
  document.getElementById('submitBtn').disabled = false;
}

function handleSubmit() {
  if (!selectedOption) return;

  var q = interactiveData.questions[currentQuestion];
  var isCorrect = selectedOption === q.correctAnswer;

  // Record answer
  answers.push({
    questionId: q.id,
    selectedLabel: selectedOption,
    isCorrect: isCorrect
  });

  // Disable options
  document.querySelectorAll('.option-btn').forEach(function(btn) {
    btn.classList.add('disabled');
    btn.setAttribute('tabindex', '-1');
  });

  // Hide submit button
  document.getElementById('submitBtn').style.display = 'none';

  // Show feedback
  var panel = document.getElementById('feedbackPanel');
  var feedbackText = '';
  var feedbackType = '';

  if (isCorrect) {
    feedbackType = 'correct';
    feedbackText = q.feedback.correct;
  } else {
    feedbackType = 'incorrect';
    feedbackText = q.feedback.incorrect[selectedOption] || q.feedback.incorrect['default'] || 'That\'s not quite right.';
  }

  var isLast = currentQuestion >= interactiveData.questions.length - 1;
  var nextLabel = isLast ? 'See Results' : 'Next';
  var nextArrow = isLast ? ' \u2192' : ' \u2192';

  panel.className = 'feedback-panel visible ' + feedbackType;
  panel.innerHTML =
    '<div class="feedback-label ' + feedbackType + '">' +
    (isCorrect ? '\u2713 Correct' : 'Not quite') +
    '</div>' +
    '<div class="feedback-text">' + escapeHtml(feedbackText) + '</div>' +
    '<button class="btn btn-next" onclick="nextQuestion()" aria-label="' +
    (isLast ? 'See your results' : 'Go to next question') +
    '">' + nextLabel + nextArrow + '</button>';

  // Focus the feedback panel
  panel.setAttribute('tabindex', '-1');
  panel.focus();
}

function nextQuestion() {
  currentQuestion++;
  if (currentQuestion >= interactiveData.questions.length) {
    showResults();
  } else {
    selectedOption = null;
    renderQuestion();
  }
}


// ─────────────────────────────────────────────
// RESULTS SCREEN
// ─────────────────────────────────────────────

function showResults() {
  document.getElementById('questionArea').innerHTML = '';

  var total = interactiveData.questions.length;
  var correctCount = answers.filter(function(a) { return a.isCorrect; }).length;
  var pct = Math.round((correctCount / total) * 100);

  var screen = document.getElementById('resultsScreen');
  screen.classList.add('active');

  var html = '';

  // Score card
  html += '<div class="score-card">';
  html += '  <div class="score-number">' + correctCount + ' of ' + total + '</div>';
  html += '  <div class="score-label" aria-live="polite">questions answered correctly</div>';
  html += '  <div class="score-bar-container">';
  html += '    <div class="score-bar-fill" style="width: ' + pct + '%" role="img" aria-label="Score: ' + pct + ' percent"></div>';
  html += '  </div>';
  html += '</div>';

  // Debrief
  html += '<div class="debrief-card">';
  html += '  <h3>What you just practiced</h3>';
  html += formatParagraphs(interactiveData.debrief);
  html += '</div>';

  // Review toggle
  html += '<button class="review-toggle" id="reviewToggle" onclick="toggleReview()" aria-expanded="false" aria-controls="reviewSection">Review your answers</button>';

  // Review section
  html += '<div class="review-section" id="reviewSection" role="region" aria-label="Answer review">';
  interactiveData.questions.forEach(function(q, i) {
    var answer = answers[i];
    var selectedOpt = q.options.find(function(o) { return o.label === answer.selectedLabel; });
    var correctOpt = q.options.find(function(o) { return o.label === q.correctAnswer; });
    var feedbackText = answer.isCorrect
      ? q.feedback.correct
      : (q.feedback.incorrect[answer.selectedLabel] || q.feedback.incorrect['default'] || '');

    html += '<div class="review-item">';
    html += '  <div class="review-q-number">Question ' + (i + 1) + '</div>';
    html += '  <span class="review-badge ' + (answer.isCorrect ? 'review-badge-correct' : 'review-badge-incorrect') + '">';
    html += answer.isCorrect ? 'Correct' : 'Incorrect';
    html += '</span>';
    html += '  <div class="review-prompt">' + escapeHtml(q.prompt) + '</div>';
    html += '  <div class="review-answer yours"><strong>Your answer:</strong> ' + escapeHtml(answer.selectedLabel + '. ' + selectedOpt.text) + '</div>';
    if (!answer.isCorrect) {
      html += '  <div class="review-answer correct-answer"><strong>Correct answer:</strong> ' + escapeHtml(q.correctAnswer + '. ' + correctOpt.text) + '</div>';
    }
    html += '  <div class="review-feedback">' + escapeHtml(feedbackText) + '</div>';
    html += '</div>';
  });
  html += '</div>';

  // Close note
  html += '<div class="close-note">You can close this tab to return to the course.</div>';

  screen.innerHTML = html;

  // Scroll to top and focus score
  window.scrollTo({ top: 0, behavior: 'smooth' });
  var scoreCard = screen.querySelector('.score-card');
  scoreCard.setAttribute('tabindex', '-1');
  scoreCard.focus();
}

function toggleReview() {
  var toggle = document.getElementById('reviewToggle');
  var section = document.getElementById('reviewSection');
  var expanded = toggle.classList.toggle('expanded');
  section.classList.toggle('visible', expanded);
  toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
}


// ─────────────────────────────────────────────
// UTILITIES
// ─────────────────────────────────────────────

function escapeHtml(text) {
  var div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function formatParagraphs(text) {
  return text.split('\n\n').map(function(p) {
    return '<p>' + escapeHtml(p.trim()) + '</p>';
  }).join('');
}


// ─────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────

init();
</script>
</body>
</html>
```

---

## Component Reference

This section describes each visual component. The complete CSS and HTML for all components is included in the page shell above. This reference explains when and how each one is used.

### Header

The header appears at the top of every interactive. It shows a small orange "INTERACTIVE EXERCISE" label, the interactive title (from `interactiveData.title`), and a subtitle with the estimated time (from `interactiveData.subtitle`).

The header is separated from the content below by a 2px orange bottom border.

### Context Card

Displays the context setup text from the source document. Grey background (`#f7f8fa`), rounded corners, appears before the questions begin. This is where you set the scene: who the student is, what's happening, what they know going in.

The context text is pulled from `interactiveData.context`. Separate paragraphs with `\n\n` in the string and the `formatParagraphs()` utility will wrap each in `<p>` tags.

### Stimulus Card (Optional)

Used when the interactive includes an artifact, passage, or scenario text that students reference while answering questions. This is common for critical evaluation exercises (fallback format) where the stimulus is the document being evaluated.

Displayed as a white card with a 4px purple left border (`#7c3aed`), matching the scenario accent used in Canvas pages. Includes a small "SCENARIO" label in purple.

The stimulus text is pulled from `interactiveData.stimulus`. If this field is empty, the stimulus card is not rendered. When present, the stimulus card persists on screen alongside each question so students can refer back to it.

### Progress Bar

Shows the current question number and a visual progress bar with orange fill. The text reads "Question X of Y" and the bar fills proportionally.

The progress bar updates automatically as students advance through questions.

### Question Prompt

Displays the current question text. Rendered at 16px, medium weight, with enough visual weight to distinguish it from the answer options below.

### Answer Options

Multiple-choice options rendered as full-width clickable cards (not radio buttons). Each card shows the option label (A, B, C, D) in bold followed by the option text.

**States:**
- **Default:** White background, light grey border
- **Hover:** Light blue background (`#f5f7ff`), blue border
- **Selected:** Slightly deeper blue background (`#eef2ff`), electric blue border
- **Disabled:** Reduced opacity (after submission)

Students click to select. Only one option can be selected at a time. The selected option gets `aria-checked="true"`.

### Submit Button

Orange background (`#ff7c0a`), dark blue text, rounded corners. Disabled until an answer is selected (reduced opacity at 35%). After the student submits, the button is hidden and replaced by the feedback panel.

### Feedback Panel

Appears after submission, sliding in below the options.

- **Correct:** Green-tinted background (`#f0faf4`), green left border (`#18733e`). Shows a checkmark and "Correct" label in green, followed by the explanatory feedback text.
- **Incorrect:** Red-tinted background (`#fff3f3`), red left border (`#ffc9c9`). Shows "Not quite" label in red, followed by per-option feedback text.

Both versions include a "Next" button (or "See Results" for the last question) at the bottom. The button uses electric blue background with white text.

Focus is moved to the feedback panel after it appears, so screen readers announce the result.

### Results Screen

Displayed after all questions are answered. Replaces the question area entirely.

**Score Card:** Dark blue background with white text, centered. Shows "X of Y" in large type, "questions answered correctly" as a label, and a visual score bar (green fill against a translucent track).

**Debrief Card:** White background, 2px orange border. Shows a "What you just practiced" heading followed by the debrief text from the source document. This is where you tie the practice back to the real situation.

**Review Section:** Collapsed by default behind a "Review your answers" toggle button. When expanded, shows one card per question with:
- Question number and correct/incorrect badge
- The question prompt
- The student's answer
- The correct answer (only shown if the student got it wrong)
- The feedback text

**Close Note:** A subtle line at the bottom: "You can close this tab to return to the course."

---

## JavaScript Architecture

The JavaScript is intentionally simple. No frameworks, no build tools, no modules. Everything lives in a single `<script>` block at the bottom of the page.

### Data Model

All content is stored in the `interactiveData` object at the top of the script. This is the only thing that changes between interactives. The structure:

```javascript
const interactiveData = {
  title: "",           // Displayed in the header
  subtitle: "",        // e.g., "About 5 minutes"
  context: "",         // Setup text. Use \n\n for paragraph breaks.
  stimulus: "",        // Optional. The artifact or scenario text. Leave "" if not needed.
  questions: [
    {
      id: 1,
      prompt: "",      // The question as students see it
      options: [
        { label: "A", text: "" },
        { label: "B", text: "" },
        { label: "C", text: "" },
        { label: "D", text: "" }
      ],
      correctAnswer: "A",   // The label of the correct option
      feedback: {
        correct: "",         // Shown when the student picks the right answer
        incorrect: {
          "B": "",           // Per-option feedback for each wrong answer
          "C": "",
          "D": ""
        }
      }
    }
    // ... more questions (typically 3-5)
  ],
  debrief: ""          // Shown on the results screen. Use \n\n for paragraph breaks.
};
```

### State

Two variables track state:

- `currentQuestion` — index into the questions array (starts at 0)
- `answers` — array of objects recording each response: `{ questionId, selectedLabel, isCorrect }`

A third variable, `selectedOption`, tracks which option is currently highlighted before submission.

### Flow

1. `init()` — Sets up the header and renders the context card with a "Begin" button
2. `startQuestions()` — Resets state and renders the first question
3. `renderQuestion()` — Builds the progress bar, stimulus (if present), question prompt, option buttons, and submit button
4. `handleSelect(label)` — Highlights the selected option, enables submit
5. `handleSubmit()` — Records the answer, disables options, shows the feedback panel with correct/incorrect styling and a "Next" button
6. `nextQuestion()` — Advances to the next question or calls `showResults()`
7. `showResults()` — Builds the results screen with score, debrief, and collapsible review section

### Utilities

- `escapeHtml(text)` — Prevents XSS by escaping HTML entities in user-facing content
- `formatParagraphs(text)` — Splits on double newlines and wraps each block in `<p>` tags

---

## Accessibility Requirements

These are built into the page shell template, but verify them during testing.

### Keyboard Navigation

- **Tab** moves between interactive elements (options, buttons)
- **Arrow keys** (Up/Down/Left/Right) move between answer options within a question
- **Enter** or **Space** selects an option or activates a button
- All buttons have visible focus indicators (2px electric blue outline)

### Focus Management

- When a new question renders, focus moves to the question prompt (which has `tabindex="-1"` for programmatic focus)
- When feedback appears, focus moves to the feedback panel
- When results appear, focus moves to the score card
- Focus never gets trapped — Tab always moves forward through the page

### ARIA

- Answer options use `role="radiogroup"` on the container and `role="radio"` with `aria-checked` on each option
- The feedback panel uses `role="status"` and `aria-live="polite"` so screen readers announce feedback automatically
- The review toggle uses `aria-expanded` and `aria-controls` to communicate its state
- The review section uses `role="region"` with `aria-label="Answer review"`
- The progress bar uses `role="progressbar"` with `aria-valuenow`, `aria-valuemin`, and `aria-valuemax`

### Color Independence

Color is never the sole indicator of state:

- **Correct feedback:** Green background AND a checkmark symbol AND the word "Correct"
- **Incorrect feedback:** Red background AND the phrase "Not quite"
- **Selected option:** Blue border AND blue background tint (visually distinct even in greyscale)
- **Review badges:** Colored background AND text labels ("Correct" / "Incorrect")

### Contrast

All color combinations from the brand palette meet WCAG AA (4.5:1 minimum for normal text):

- Dark blue `#050c2a` on white: 17.4:1
- Dark blue on grey `#f7f8fa`: 16.2:1
- Muted `#6b7280` on white: 4.6:1
- Green `#18733e` on `#f0faf4`: 5.2:1
- White on dark blue `#050c2a`: 17.4:1
- Dark blue on orange `#ff7c0a`: 5.8:1

---

## Production Process

### Step 1: Read the interactive source document

Open the source document from `weekly_content/week[NN]/`. The source document is a markdown file created using the [Interactive Element Guide](interactive-element-guide.md). It contains everything needed: purpose, context, stimulus, questions (with options, correct answers, and per-option feedback), and debrief.

Identify:
- The interactive type (simulated scenario, critical evaluation, or prioritization)
- Whether a stimulus card is needed
- The number of questions
- Whether every answer option has per-option feedback written

### Step 2: Copy the HTML template

Copy the complete page shell from this guide (the full HTML block in the Page Shell section above). Save it as `weekly_content/week[NN]/week[NN]-[short-title]-interactive.html`.

### Step 3: Populate the interactiveData object

Replace the placeholder `interactiveData` object with real content from the source document:

1. **title** — From the source document's title (H1 heading)
2. **subtitle** — Use the estimated time, e.g., "About 5 minutes"
3. **context** — From the "Context Setup" section. Use `\n\n` between paragraphs
4. **stimulus** — From the "Stimulus" section, if present. Leave as `""` if the interactive type doesn't use a persistent stimulus
5. **questions** — From the "Questions" section. For each question:
   - `id` — Sequential number (1, 2, 3...)
   - `prompt` — From "Question text"
   - `options` — From "Options", using A/B/C/D labels
   - `correctAnswer` — From "Correct answer"
   - `feedback.correct` — From "Feedback if correct"
   - `feedback.incorrect` — Map each wrong option label to its feedback from "Feedback if incorrect"
6. **debrief** — From the "Debrief" section. Use `\n\n` between paragraphs

### Step 4: Update the page title

In the `<title>` tag, replace `[Interactive Title]` with the actual title.

### Step 5: Test locally

Open the file directly in a browser (File > Open or drag to browser). Click through the full exercise:

1. Read the context card and click "Begin"
2. Answer each question — try both correct and incorrect answers
3. Verify each feedback panel shows the right text for the option you selected
4. Check that the progress bar advances
5. On the results screen, verify the score and debrief
6. Expand the review section and verify all questions, answers, and feedback are shown
7. Close and reopen the file to verify it works from a fresh load

### Step 6: Test keyboard navigation

Without using a mouse:

1. Tab to the "Begin" button and press Enter
2. Use arrow keys to move between options
3. Press Enter to select an option
4. Tab to "Submit" and press Enter
5. Verify focus moves to the feedback panel
6. Tab to "Next" and press Enter
7. Repeat through all questions
8. On results, Tab to "Review your answers" and press Enter

### Step 7: Test on mobile

Open the file on a phone or use browser dev tools in responsive mode. Verify:
- Text is readable without zooming
- Option cards are large enough to tap (minimum 44px tap target)
- Progress bar and score card display correctly
- No horizontal scrolling

---

## Testing Checklist

Before considering the interactive complete:

- [ ] All questions render with correct text from the source document
- [ ] Each answer option shows the correct per-option feedback (test every option)
- [ ] Correct answers show green feedback panel with checkmark and "Correct"
- [ ] Incorrect answers show red feedback panel with "Not quite"
- [ ] Progress bar advances correctly and shows accurate "Question X of Y"
- [ ] Results screen shows accurate score (X of Y correct)
- [ ] Score bar fills to the correct proportion
- [ ] Debrief text appears on results screen and matches source document
- [ ] Review section expands/collapses and shows all questions with answers and feedback
- [ ] Review section shows "Correct answer" line only for questions answered incorrectly
- [ ] Works on mobile — responsive layout, large enough tap targets, no horizontal scroll
- [ ] Keyboard navigation works — Tab to options, arrow keys between options, Enter to select/submit
- [ ] Focus moves to feedback panel after submission
- [ ] Focus moves to results screen after completing all questions
- [ ] Screen reader can navigate the full flow (test with VoiceOver on Mac: Cmd+F5)
- [ ] No console errors (open browser dev tools, check Console tab)
- [ ] File is self-contained — works when opened directly from the filesystem
- [ ] File name follows convention: `week[NN]-[short-title]-interactive.html`
- [ ] Page title includes the interactive title and "Riipen Career Catalyst"

---

## Notes

- **Stimulus persistence.** For critical evaluation fallback exercises, the stimulus card stays visible alongside each question so students can refer back to the artifact. For simulated scenarios where the stimulus is just context, you may prefer to show it only on the context screen (set `stimulus` to `""` and include the scenario text in `context` instead).
- **Per-option feedback coverage.** Every wrong answer option MUST have its own feedback entry in the `incorrect` object. If a feedback key is missing for an option the student selects, the code falls back to `feedback.incorrect['default']` or a generic message. Avoid this — the per-option feedback is where the learning happens.
- **Paragraph breaks.** Use `\n\n` in string values to create paragraph breaks. The `formatParagraphs()` function handles wrapping. Single `\n` line breaks are treated as part of the same paragraph.
- **Special characters in content.** The `escapeHtml()` function handles quotes, angle brackets, and ampersands in content strings. You do not need to manually escape these in the `interactiveData` object. However, use `\'` for apostrophes inside single-quoted JS strings, or use double-quoted strings.
- **Google Fonts.** The DM Sans import in the `<link>` tag loads weights 400 (regular), 500 (medium), and 700 (bold), plus italic 400. This covers all typography in the interactive.
- **No "Try Again" on this format.** Unlike the click-to-highlight format, the sequential question format does not include a "Try again" button on the results screen. Once students have seen the correct answers and feedback for every question, repeating the exercise has diminishing returns. If you want to add one, follow the pattern from the Week 2 interactive (`resetExercise()` function).
- **Future interaction models.** This guide covers the sequential multiple-choice fallback format only. For richer interactions (drag-and-drop card sorting, click-to-highlight with action selection), use the same page shell and brand styling but replace the question rendering and interaction logic. The Week 2 AI evaluation interactive (`weekly_content/week02/page2-using-ai-responsibly-interactive.html`) demonstrates the click-to-highlight model.
