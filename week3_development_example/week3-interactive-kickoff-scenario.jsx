import { useState } from "react";

const SCENARIO = {
  employer: "Dana Whitfield",
  title: "Director of Community Engagement",
  org: "Lakeview Regional Health System",
  transcript: [
    {
      speaker: "Dana",
      text: "Thanks for meeting with me today. So, as you probably saw in the brief, we're looking for help with our community health outreach — specifically around preventive care messaging for underserved populations in the eastern part of our service area.",
      signals: [],
    },
    {
      speaker: "Dana",
      text: "We've been doing outreach for years, honestly, but the numbers just aren't moving. Screening rates in those ZIP codes are still way below the rest of our region. We've tried mailers, we've tried social media, we've partnered with a few churches — some of it gets traction, some doesn't.",
      signals: ["frustration with past efforts", "has tried multiple approaches"],
    },
    {
      speaker: "Dana",
      text: "What I'm hoping you can help with is — and I know this is broad — figuring out why it's not landing. Like, is it the messaging? Is it the channels? Is it a trust issue? I don't honestly know. I have my theories but I've been too close to it.",
      signals: ["acknowledges uncertainty", "open to being wrong", "wants outside perspective"],
    },
    {
      speaker: "Dana",
      text: "The deliverable, ideally, would be some kind of assessment with recommendations. Something I can take to our leadership team. We have a board presentation in late June — that's not a hard deadline for you, but it would be really helpful to have something by then.",
      signals: ["board presentation = real deadline", '"not a hard deadline" = it actually is'],
    },
    {
      speaker: "Dana",
      text: "I should mention — our VP of Marketing has opinions about this. She thinks we just need better creative. I'm not sure that's the whole story, but she'll want to see that we considered it. Just... be aware of that dynamic.",
      signals: ["internal politics", "needs to satisfy a stakeholder", "diplomatic warning"],
    },
    {
      speaker: "Dana",
      text: "The other thing is, we just went through a big system merger last year. Lakeview used to be two separate hospitals, so the eastern communities — some of them have had a complicated relationship with us. That's probably relevant.",
      signals: ["trust issues are organizational", "merger = recent disruption", '"probably relevant" = definitely relevant'],
    },
    {
      speaker: "Dana",
      text: "Anyway, I'm excited about this. I think fresh eyes will help. What questions do you have for me?",
      signals: [],
    },
  ],
};

const QUESTIONS = [
  {
    id: 1,
    question: "What does Dana seem to care most about?",
    options: [
      { id: "a", text: "Creating better marketing materials and creative content", correct: false },
      { id: "b", text: "Understanding why their outreach isn't reaching the communities that need it", correct: true },
      { id: "c", text: "Preparing a polished presentation for the board", correct: false },
      { id: "d", text: "Resolving the internal disagreement with the VP of Marketing", correct: false },
    ],
    explanation: "Dana explicitly says 'figuring out why it's not landing' is what she wants help with. She names messaging, channels, and trust as possibilities — she's not sure which it is. The board presentation and the VP of Marketing are real factors, but they're constraints she's navigating, not the thing she cares most about. Notice she says the VP 'thinks we just need better creative' and then adds 'I'm not sure that's the whole story' — she's signaling that her own hypothesis goes deeper than creative.",
  },
  {
    id: 2,
    question: "What is the real deadline for this project?",
    options: [
      { id: "a", text: "There is no deadline — Dana said it's not a hard deadline", correct: false },
      { id: "b", text: "Late June — the board presentation", correct: true },
      { id: "c", text: "End of the semester", correct: false },
      { id: "d", text: "It's unclear — you'd need to ask a follow-up question", correct: false },
    ],
    explanation: "When a client says 'that's not a hard deadline for you, but it would be really helpful,' that's a soft way of telling you it's the deadline. Dana wants to bring your work to her board in late June. If you deliver after that, your recommendations miss the moment they'd actually be used. In professional settings, pay attention when someone downplays a deadline while also naming it — they're usually being polite, not flexible.",
  },
  {
    id: 3,
    question: "Dana mentions the VP of Marketing. Why is she telling you this?",
    options: [
      { id: "a", text: "She wants you to focus your recommendations on creative and marketing materials", correct: false },
      { id: "b", text: "She's warning you about an internal dynamic your work will need to account for", correct: true },
      { id: "c", text: "She disagrees with the VP and wants you to prove the VP wrong", correct: false },
      { id: "d", text: "It's not relevant to your project — just office politics", correct: false },
    ],
    explanation: "Dana is giving you a diplomatic heads-up. She doesn't say 'the VP is wrong' — she says 'she'll want to see that we considered it.' That's a signal: your recommendations need to address the creative/messaging angle even if you conclude the real issue is trust or channels. If your final deliverable ignores what the VP cares about, it becomes harder for Dana to use it internally. This is a common professional dynamic — your work needs to be useful not just to your contact, but to the people your contact answers to.",
  },
  {
    id: 4,
    question: "Dana says the merger is 'probably relevant.' How relevant is it?",
    options: [
      { id: "a", text: "Somewhat — it's background context but not central to the project", correct: false },
      { id: "b", text: "Very — it likely explains why trust is low and outreach isn't working", correct: true },
      { id: "c", text: "Not very — the merger is done and the organization has moved on", correct: false },
      { id: "d", text: "It's impossible to know without more research", correct: false },
    ],
    explanation: "When someone brings up a major organizational change and calls it 'probably relevant,' it's almost certainly central. Dana has already told you that screening rates are low specifically in the eastern communities, and that those communities 'have had a complicated relationship' with the system since the merger. She's connecting the dots for you without stating it outright. In your post-kickoff research, the merger and its impact on community trust should be a primary line of inquiry — not an afterthought.",
  },
];

const phases = ["intro", "transcript", "questions", "debrief"];

export default function KickoffScenario() {
  const [phase, setPhase] = useState("intro");
  const [currentLine, setCurrentLine] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);

  const allAnswered = Object.keys(answers).length === QUESTIONS.length;
  const allRevealed = Object.keys(showResults).length === QUESTIONS.length;

  return (
    <div style={{
      minHeight: "100vh",
      background: "#fafaf8",
      fontFamily: "'Georgia', 'Times New Roman', serif",
      color: "#1a1a2e",
    }}>
      <div style={{
        maxWidth: 720,
        margin: "0 auto",
        padding: "40px 24px",
      }}>
        {/* Header */}
        <div style={{
          borderBottom: "2px solid #2d6a4f",
          paddingBottom: 16,
          marginBottom: 32,
        }}>
          <p style={{
            fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
            fontSize: 11,
            textTransform: "uppercase",
            letterSpacing: 2,
            color: "#2d6a4f",
            margin: "0 0 6px 0",
          }}>Interactive Scenario</p>
          <h1 style={{
            fontSize: 28,
            fontWeight: "normal",
            margin: "0 0 6px 0",
            lineHeight: 1.2,
          }}>Reading Between the Lines</h1>
          <p style={{
            fontSize: 15,
            color: "#666",
            margin: 0,
            fontStyle: "italic",
          }}>Practice interpreting a client conversation before your real kickoff meeting.</p>
        </div>

        {/* INTRO PHASE */}
        {phase === "intro" && (
          <div>
            <div style={{
              background: "#f0f7f4",
              border: "1px solid #d8f3dc",
              borderRadius: 8,
              padding: 24,
              marginBottom: 24,
            }}>
              <p style={{ fontSize: 15, lineHeight: 1.7, margin: "0 0 16px 0" }}>
                In a kickoff meeting, the most important information isn't always what's said directly. 
                Experienced professionals learn to read the conversation — to hear what's emphasized, 
                what's repeated, and what's left unsaid.
              </p>
              <p style={{ fontSize: 15, lineHeight: 1.7, margin: "0 0 16px 0" }}>
                You're about to watch a simulated kickoff meeting with a fictional employer. 
                Pay attention not just to <em>what</em> she says, but <em>how</em> she says it — 
                what she emphasizes, what she downplays, and what she mentions in passing that 
                might actually be critical.
              </p>
              <p style={{ fontSize: 15, lineHeight: 1.7, margin: 0 }}>
                After the meeting, you'll answer a few interpretation questions. 
                Then we'll show you what an experienced consultant would have picked up from the same conversation.
              </p>
            </div>

            <div style={{
              background: "white",
              border: "1px solid #ddd",
              borderRadius: 8,
              padding: 24,
              marginBottom: 24,
            }}>
              <p style={{
                fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                fontSize: 11,
                textTransform: "uppercase",
                letterSpacing: 1.5,
                color: "#999",
                margin: "0 0 12px 0",
              }}>The Scenario</p>
              <p style={{ fontSize: 15, lineHeight: 1.7, margin: "0 0 8px 0" }}>
                <strong>{SCENARIO.employer}</strong>, {SCENARIO.title} at <strong>{SCENARIO.org}</strong>, 
                is meeting with your team for the first time to discuss a community health outreach project.
              </p>
              <p style={{ fontSize: 14, lineHeight: 1.7, margin: 0, color: "#666" }}>
                Time: ~5 minutes to read, ~5 minutes to answer questions
              </p>
            </div>

            <button
              onClick={() => { setPhase("transcript"); setCurrentLine(0); }}
              style={{
                background: "#2d6a4f",
                color: "white",
                border: "none",
                borderRadius: 6,
                padding: "14px 32px",
                fontSize: 15,
                fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                cursor: "pointer",
                display: "block",
                margin: "0 auto",
              }}
            >
              Start the Meeting
            </button>
          </div>
        )}

        {/* TRANSCRIPT PHASE */}
        {phase === "transcript" && (
          <div>
            <div style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: 24,
            }}>
              <p style={{
                fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                fontSize: 12,
                color: "#999",
                margin: 0,
              }}>
                {currentLine + 1} of {SCENARIO.transcript.length}
              </p>
              <div style={{
                background: "#e8e8e8",
                borderRadius: 4,
                height: 4,
                flex: 1,
                marginLeft: 16,
                overflow: "hidden",
              }}>
                <div style={{
                  background: "#2d6a4f",
                  height: "100%",
                  width: `${((currentLine + 1) / SCENARIO.transcript.length) * 100}%`,
                  transition: "width 0.3s ease",
                  borderRadius: 4,
                }} />
              </div>
            </div>

            {/* Video placeholder */}
            <div style={{
              background: "#1a1a2e",
              borderRadius: 8,
              padding: "32px 28px",
              marginBottom: 8,
              minHeight: 180,
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
            }}>
              <div style={{
                display: "flex",
                alignItems: "flex-start",
                gap: 16,
              }}>
                <div style={{
                  width: 44,
                  height: 44,
                  borderRadius: "50%",
                  background: "#2d6a4f",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "white",
                  fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                  fontSize: 16,
                  fontWeight: "bold",
                  flexShrink: 0,
                }}>DW</div>
                <div>
                  <p style={{
                    color: "#8ec8a0",
                    fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                    fontSize: 12,
                    margin: "0 0 8px 0",
                    fontWeight: "bold",
                  }}>
                    {SCENARIO.employer} — {SCENARIO.title}
                  </p>
                  <p style={{
                    color: "#e8e8e8",
                    fontSize: 16,
                    lineHeight: 1.8,
                    margin: 0,
                    fontStyle: "italic",
                  }}>
                    "{SCENARIO.transcript[currentLine].text}"
                  </p>
                </div>
              </div>
            </div>

            <p style={{
              fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
              fontSize: 11,
              color: "#bbb",
              textAlign: "center",
              margin: "0 0 24px 0",
              fontStyle: "italic",
            }}>
              In the actual course, this would be a video of the employer speaking. Read carefully — you'll be asked about what you noticed.
            </p>

            <div style={{
              display: "flex",
              justifyContent: "space-between",
              gap: 12,
            }}>
              <button
                onClick={() => setCurrentLine(Math.max(0, currentLine - 1))}
                disabled={currentLine === 0}
                style={{
                  background: "white",
                  color: currentLine === 0 ? "#ccc" : "#1a1a2e",
                  border: "1px solid #ddd",
                  borderRadius: 6,
                  padding: "12px 24px",
                  fontSize: 14,
                  fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                  cursor: currentLine === 0 ? "default" : "pointer",
                }}
              >
                ← Back
              </button>

              {currentLine < SCENARIO.transcript.length - 1 ? (
                <button
                  onClick={() => setCurrentLine(currentLine + 1)}
                  style={{
                    background: "#2d6a4f",
                    color: "white",
                    border: "none",
                    borderRadius: 6,
                    padding: "12px 24px",
                    fontSize: 14,
                    fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                    cursor: "pointer",
                  }}
                >
                  Continue →
                </button>
              ) : (
                <button
                  onClick={() => { setPhase("questions"); setCurrentQuestion(0); }}
                  style={{
                    background: "#2d6a4f",
                    color: "white",
                    border: "none",
                    borderRadius: 6,
                    padding: "12px 24px",
                    fontSize: 14,
                    fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                    cursor: "pointer",
                  }}
                >
                  The meeting's over. What did you notice? →
                </button>
              )}
            </div>
          </div>
        )}

        {/* QUESTIONS PHASE */}
        {phase === "questions" && (
          <div>
            <div style={{
              background: "#f0f7f4",
              border: "1px solid #d8f3dc",
              borderRadius: 8,
              padding: 16,
              marginBottom: 28,
            }}>
              <p style={{ fontSize: 14, margin: 0, lineHeight: 1.6 }}>
                The meeting's over. Before you look at your notes or talk to your team — 
                what did you pick up? Answer based on what you heard, not what you'd guess.
              </p>
            </div>

            {QUESTIONS.map((q, qi) => (
              <div key={q.id} style={{
                background: "white",
                border: showResults[q.id]
                  ? `1px solid ${answers[q.id] === q.options.find(o => o.correct)?.id ? "#2d6a4f" : "#cc6b49"}`
                  : "1px solid #ddd",
                borderRadius: 8,
                padding: 24,
                marginBottom: 20,
              }}>
                <p style={{
                  fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                  fontSize: 11,
                  textTransform: "uppercase",
                  letterSpacing: 1.5,
                  color: "#999",
                  margin: "0 0 8px 0",
                }}>Question {q.id} of {QUESTIONS.length}</p>
                <p style={{
                  fontSize: 16,
                  fontWeight: "bold",
                  margin: "0 0 16px 0",
                  lineHeight: 1.5,
                }}>{q.question}</p>

                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {q.options.map((opt) => {
                    const isSelected = answers[q.id] === opt.id;
                    const revealed = showResults[q.id];
                    let bg = "white";
                    let borderColor = "#ddd";
                    let textColor = "#1a1a2e";

                    if (revealed) {
                      if (opt.correct) {
                        bg = "#f0f7f4";
                        borderColor = "#2d6a4f";
                      } else if (isSelected && !opt.correct) {
                        bg = "#fef2ee";
                        borderColor = "#cc6b49";
                      }
                    } else if (isSelected) {
                      bg = "#f0f7f4";
                      borderColor = "#2d6a4f";
                    }

                    return (
                      <button
                        key={opt.id}
                        onClick={() => {
                          if (!revealed) {
                            setAnswers({ ...answers, [q.id]: opt.id });
                          }
                        }}
                        style={{
                          background: bg,
                          border: `1.5px solid ${borderColor}`,
                          borderRadius: 6,
                          padding: "12px 16px",
                          fontSize: 14,
                          fontFamily: "Georgia, serif",
                          textAlign: "left",
                          cursor: revealed ? "default" : "pointer",
                          color: textColor,
                          lineHeight: 1.5,
                          transition: "all 0.15s ease",
                        }}
                      >
                        {opt.text}
                        {revealed && opt.correct && (
                          <span style={{ color: "#2d6a4f", marginLeft: 8, fontWeight: "bold" }}>✓</span>
                        )}
                        {revealed && isSelected && !opt.correct && (
                          <span style={{ color: "#cc6b49", marginLeft: 8 }}>✗</span>
                        )}
                      </button>
                    );
                  })}
                </div>

                {answers[q.id] && !showResults[q.id] && (
                  <button
                    onClick={() => setShowResults({ ...showResults, [q.id]: true })}
                    style={{
                      background: "none",
                      border: "none",
                      color: "#2d6a4f",
                      fontSize: 13,
                      fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                      cursor: "pointer",
                      marginTop: 12,
                      padding: 0,
                      textDecoration: "underline",
                    }}
                  >
                    Check your answer
                  </button>
                )}

                {showResults[q.id] && (
                  <div style={{
                    background: "#fafaf8",
                    borderRadius: 6,
                    padding: 16,
                    marginTop: 16,
                    borderLeft: "3px solid #2d6a4f",
                  }}>
                    <p style={{
                      fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                      fontSize: 11,
                      textTransform: "uppercase",
                      letterSpacing: 1.5,
                      color: "#2d6a4f",
                      margin: "0 0 8px 0",
                      fontWeight: "bold",
                    }}>What an experienced consultant would say</p>
                    <p style={{
                      fontSize: 14,
                      lineHeight: 1.7,
                      margin: 0,
                      color: "#444",
                    }}>{q.explanation}</p>
                  </div>
                )}
              </div>
            ))}

            {allRevealed && (
              <button
                onClick={() => setPhase("debrief")}
                style={{
                  background: "#2d6a4f",
                  color: "white",
                  border: "none",
                  borderRadius: 6,
                  padding: "14px 32px",
                  fontSize: 15,
                  fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                  cursor: "pointer",
                  display: "block",
                  margin: "12px auto 0",
                }}
              >
                See the full debrief →
              </button>
            )}
          </div>
        )}

        {/* DEBRIEF PHASE */}
        {phase === "debrief" && (
          <div>
            <h2 style={{ fontSize: 22, fontWeight: "normal", margin: "0 0 8px 0" }}>
              The Full Picture
            </h2>
            <p style={{ fontSize: 15, color: "#666", lineHeight: 1.7, margin: "0 0 28px 0" }}>
              Here's what that conversation revealed — the kind of reading 
              that gets easier with practice.
            </p>

            {[
              {
                label: "What she actually wants",
                content: "Dana wants to understand why outreach isn't reaching underserved communities — not just better marketing materials. She's open to the answer being about trust, channels, or messaging. Your job is to figure out which, not to assume.",
              },
              {
                label: "The real deadline",
                content: "Late June, tied to a board presentation. When a client softens a deadline ('not a hard deadline for you'), they're being polite. They've already told you when your work needs to be done to be useful.",
              },
              {
                label: "The internal politics",
                content: "The VP of Marketing wants better creative. Dana isn't sure that's the answer. Your deliverable needs to address both perspectives — not to pick sides, but to be usable by Dana in a room where the VP is also present. This is a very common professional situation.",
              },
              {
                label: "The elephant in the room",
                content: "The merger. Lakeview used to be two separate hospitals. The eastern communities have a 'complicated relationship' with the system. Dana calls this 'probably relevant' — which in professional-speak means 'this is the context that explains everything, and I'm curious whether you'll pick up on it.' Your post-kickoff research should start here.",
              },
              {
                label: "What would go in your Kickoff Summary",
                content: "Confirmed scope: assess why preventive care outreach isn't reaching underserved populations in the eastern service area. Deliverable: assessment with recommendations, formatted for leadership/board consumption. Timeline: board presentation late June. Key contact: Dana Whitfield. Open questions: what specific ZIP codes or communities? What data do they already have on screening rates? Can you speak with anyone in the eastern communities directly? What's the VP of Marketing's specific critique of current creative?",
              },
            ].map((item, i) => (
              <div key={i} style={{
                background: "white",
                border: "1px solid #ddd",
                borderRadius: 8,
                padding: 24,
                marginBottom: 16,
              }}>
                <p style={{
                  fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                  fontSize: 12,
                  textTransform: "uppercase",
                  letterSpacing: 1.5,
                  color: "#2d6a4f",
                  margin: "0 0 8px 0",
                  fontWeight: "bold",
                }}>{item.label}</p>
                <p style={{
                  fontSize: 15,
                  lineHeight: 1.7,
                  margin: 0,
                  color: "#333",
                }}>{item.content}</p>
              </div>
            ))}

            <div style={{
              background: "#f0f7f4",
              border: "1px solid #d8f3dc",
              borderRadius: 8,
              padding: 24,
              marginTop: 28,
            }}>
              <p style={{
                fontSize: 15,
                lineHeight: 1.7,
                margin: "0 0 12px 0",
                fontWeight: "bold",
              }}>The takeaway</p>
              <p style={{
                fontSize: 15,
                lineHeight: 1.7,
                margin: 0,
              }}>
                In your real kickoff, you'll hear all of this in real time — without the 
                ability to reread or pause. That's why preparation matters, why having a 
                note-taker matters, and why debriefing with your team immediately after 
                matters. The signals are there. You just have to practice noticing them.
              </p>
            </div>

            <button
              onClick={() => {
                setPhase("intro");
                setCurrentLine(0);
                setAnswers({});
                setShowResults({});
                setCurrentQuestion(0);
              }}
              style={{
                background: "white",
                color: "#2d6a4f",
                border: "1px solid #2d6a4f",
                borderRadius: 6,
                padding: "12px 24px",
                fontSize: 14,
                fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
                cursor: "pointer",
                display: "block",
                margin: "24px auto 0",
              }}
            >
              Start over
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
