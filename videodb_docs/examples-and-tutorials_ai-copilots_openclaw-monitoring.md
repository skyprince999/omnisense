### Overview

- [Examples &amp; Tutorials](\examples-and-tutorials)

### Agentic Workflows

- [Overview](\examples-and-tutorials\ai-copilots)
- [Pair Programmer](\examples-and-tutorials\ai-copilots\pair-programmer)
- [OpenClaw Monitoring](\examples-and-tutorials\ai-copilots\openclaw-monitoring)
- [Call.md](\examples-and-tutorials\ai-copilots\call-md)
- [Bloom](\examples-and-tutorials\ai-copilots\bloom)
- [Focusd](\examples-and-tutorials\ai-copilots\focusd)

### Video Search and Understanding

- [Overview](\examples-and-tutorials\video-rag)
- [Keyword Search](\examples-and-tutorials\video-rag\keyword-search)
- [Character Extraction](\examples-and-tutorials\video-rag\character-clips)
- [Multimodal Search](\examples-and-tutorials\video-rag\multimodal-search)
- [Case Study: NFL Game Analysis](\examples-and-tutorials\video-rag\case-study-nfl)
- [Use Case: Conference Slide Extraction](\examples-and-tutorials\video-rag\use-case-conference-slides)

### Live Intelligence

- [Overview](\examples-and-tutorials\live-intelligence)
- [Baby Crib Monitoring with AI](\examples-and-tutorials\live-intelligence\baby-crib-monitoring)
- [Intelligent Property Intrusion Detection](\examples-and-tutorials\live-intelligence\intrusion-detection)
- [Flash Flood Early Warning System](\examples-and-tutorials\live-intelligence\flash-flood-detection)
- [Multi-Use Road Monitoring System](\examples-and-tutorials\live-intelligence\road-monitoring)
- [Dashcam Monitoring of Traffic](\examples-and-tutorials\live-intelligence\roadcam-monitoring)
- [Traffic Violation Detection](\examples-and-tutorials\live-intelligence\traffic-violations)
- [Live Cricket Highlight Detection](\examples-and-tutorials\live-intelligence\cricket-match-monitoring)
- [Multi-Camera Basketball Analytics](\examples-and-tutorials\live-intelligence\multicam-basketball-analysis)
- [Multi-Camera Public Safety Surveillance](\examples-and-tutorials\live-intelligence\multicam-public-surveillance)
- [TwelveLabs Integration](\examples-and-tutorials\live-intelligence\twelvelabs-integration)

### Content Factory

- [Overview](\examples-and-tutorials\content-factory)
- [Faceless Video Creator](\examples-and-tutorials\content-factory\faceless-video-creator)
- [AI-Generated Ads](\examples-and-tutorials\content-factory\ai-ad-films)
- [TikTok Style Lyric Video Creator](\examples-and-tutorials\content-factory\tiktok-lyric-video)
- [Video Dubbing](\examples-and-tutorials\content-factory\dubbing)
- [AI Voiceovers](\examples-and-tutorials\content-factory\voiceovers)
- [Trailer Narration](\examples-and-tutorials\content-factory\trailer-narration)
- [Voice Cloning](\examples-and-tutorials\content-factory\voice-cloning)
- [Text to Video](\examples-and-tutorials\content-factory\text-prompts)
- [AI Storyteller for Kids](\examples-and-tutorials\content-factory\ai-storyteller-kids)
- [Annual Video Statistics Recap](\examples-and-tutorials\content-factory\year-in-frames)
- [PromptClip](\pages\community\open-source\promptclip)

### Programmatic Editing

- [Overview](\examples-and-tutorials\programmatic-editing)
- [Intro/Outro](\examples-and-tutorials\programmatic-editing\intro-outro)
- [Brand Elements](\examples-and-tutorials\programmatic-editing\brand-elements)
- [Audio Overlay](\examples-and-tutorials\programmatic-editing\audio-overlay)
- [Dynamic Ads](\examples-and-tutorials\programmatic-editing\dynamic-ads)
- [Dynamic Streams](\examples-and-tutorials\programmatic-editing\dynamic-streams)
- [Word Counter](\examples-and-tutorials\programmatic-editing\word-counter)
- [Chess Match Montage Generator](\examples-and-tutorials\programmatic-editing\chess-montage)

### Safety &amp; Compliance

- [Overview](\examples-and-tutorials\safety-compliance)
- [Profanity Detection](\examples-and-tutorials\safety-compliance\beep-profanity)
- [AI-Powered Content Moderation](\examples-and-tutorials\safety-compliance\remove-content)
- [AI Video Copyright Detection](\examples-and-tutorials\safety-compliance\copyright-detection)

## On this page

- [What Is It?](#what-is-it)
- [Why Teams Need It](#why-teams-need-it)
- [How It Works](#how-it-works)
- [CLI Commands](#cli-commands)
- [Real-World Scenarios](#real-world-scenarios)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Try Without Setup](#try-without-setup)
- [Privacy &amp; Security](#privacy-%26-security)
- [Related Tutorials](#related-tutorials)

[Agentic Workflows](\examples-and-tutorials\ai-copilots\index)

# OpenClaw Monitoring

Copy page

CCTV for AI agents - record every session, watch runs live, and search agent activity with natural language

Copy page

## OpenClaw Monitoring on GitHub

Complete source code, installation guide, and configuration examples

## [ What Is It?](#what-is-it)

Your AI agent just did something on a remote server. Do you know what? Right now, most people running agents are doing this: Send task → Wait → Get "Success" in Slack → Hope for the best. That's not monitoring. That's faith. And faith breaks down fast. Your agent could have:

- Gotten stuck on a CAPTCHA and retried 47 times
- Navigated to the wrong site and filled forms with test data
- Completed the task correctly but missed a validation step
- Encountered an error you'll never see because logs don't capture visual context

**VideoDB Monitoring** turns your OpenClaw agent into an observable, auditable worker. Every run becomes a live stream (watch in real-time), a replayable recording (shareable URL, not a dead video file), and a searchable archive (find "when did it open the spreadsheet?"). Think of it as a dashcam for your AI agent, or CCTV for computer-use agents.

**Platform Support** : OpenClaw Monitoring is platform-agnostic-it runs on any system that supports Node.js 18+ and TypeScript. Works on macOS, Windows, and Linux.

## [ Why Teams Need It](#why-teams-need-it)

- Full Visibility
- Searchable History
- Compliance Ready

### [ See Everything](#see-everything)

- **Live stream** - watch your agent work in real-time
- **Replayable recordings** - shareable URL, not a dead video file
- **Full session capture** - screen and audio recorded continuously
- Catch issues before they become incidents

### [ Find Any Moment](#find-any-moment)

- **Searchable moments** - find "when did it open the spreadsheet?"
- AI-generated summaries of agent sessions
- Timestamped results with auto-generated clips
- Full transcripts of audio content

### [ Audit Everything](#audit-everything)

- Complete visual audit trail of agent actions
- **Webhook alerts** - get notified when something looks off
- Replay failures to see exactly where things went wrong
- Meet regulatory requirements with searchable evidence

**Why Logs Aren't Enough** Traditional logging captures what your code does. But autonomous agents interact with visual interfaces-browsers, desktop apps, forms-where the "ground truth" is what's on screen, not what's in a log file. You can log "clicked button #submit" but you can't log "the submit button was disabled because the CAPTCHA wasn't solved yet" unless you see the screen. Visual monitoring captures this reality, giving you the same view the agent had when it made decisions.

## [ How It Works](#how-it-works)

1

Screen Capture

A monitor daemon ( `monitor.ts` ) runs alongside your OpenClaw agent, continuously capturing the screen. Recordings stream directly to VideoDB.

2

On-Demand Indexing

Indexing is separate from recording - you only pay for it when needed. When triggered, VideoDB processes recordings with:

- **Visual indexing** - scene descriptions, active apps, URLs, and error detection
- **Transcript** - speech-to-text from system audio
- **Audio indexing** - semantic indexing of audio content

3

Search &amp; Summarize

Query agent history using natural language. Get timestamped results, auto-generated clips, and session summaries. The agent can even use its own recordings - "summarize what you did in the last 2 hours."

4

Two Setup Options

**Option 1** : Install as an OpenClaw skill - the agent handles recording, indexing, and search automatically. **Option 2** : Use VideoDB's indexing APIs directly for post-recording analysis, summaries, and search.

## [ CLI Commands](#cli-commands)

The `videodb.ts` CLI tool provides these commands:

| Command              | What It Does                                        |
|----------------------|-----------------------------------------------------|
| `start-indexing`     | Start all indexing (visual + audio + transcript)    |
| `stop-indexing`      | Stop all indexing                                   |
| `start-visual-index` | Start visual scene indexing                         |
| `stop-visual-index`  | Stop visual scene indexing                          |
| `start-audio-index`  | Start audio indexing                                |
| `stop-audio-index`   | Stop audio indexing                                 |
| `start-transcript`   | Start transcript extraction                         |
| `stop-transcript`    | Stop transcript extraction                          |
| `search`             | Natural language search across indexed recordings   |
| `summary`            | Generate an AI summary of agent activity            |
| `transcript`         | Get full transcript of audio content                |
| `stream`             | Get a playable stream URL for a specific time range |

## [ Real-World Scenarios](#real-world-scenarios)

Debugging Failed Runs

An agent task failed overnight. Instead of digging through logs, search "when did the error first appear" and get a video clip of exactly what happened - the commands run, the error messages, and the state of the screen.

Compliance Auditing

Need proof of what your AI agents did and when? OpenClaw Monitoring provides timestamped, searchable visual records that serve as a full audit trail of agent actions.

Security Monitoring

Catch agents going off-script or accessing unexpected domains. Webhook alerts notify you when something looks off, giving you video evidence of unexpected behavior.

QA &amp; Testing

Review agent workflows before pushing to production. Record test sessions, then search for edge cases, errors, or unexpected behaviors. Share specific clips with your team.

Agent Self-Reporting

Your agent can use its own recordings: "Summarize what you did in the last 2 hours", "Make a highlight video of today's work and post it to YouTube", or "Find the moment when you encountered the error."

## [ Tech Stack](#tech-stack)

## TypeScript

Monitor daemon and CLI tooling ( `monitor.ts` , `videodb.ts` )

## Python + Flask

Backend server for session management and Cloudflare tunneling

## VideoDB SDK

Media streaming, AI indexing, and semantic search

## OpenClaw

Autonomous agent framework with skill system

## [ Getting Started](#getting-started)

**Prerequisites**

- [OpenClaw](https://openclaw.ai/) installed and running
- Node.js 18+
- [VideoDB API key](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs)

1

Install the Skill

Point your OpenClaw agent at the repo:

```
please install https://github.com/video-db/openclaw-monitoring skill and set it up
```

Or install manually:

```
git clone https://github.com/video-db/openclaw-monitoring.git
mkdir -p ~/.openclaw/workspace/skills/videodb-monitoring
cp -r openclaw-monitoring/videodb-monitoring-skill/ * ~/.openclaw/workspace/skills/videodb-monitoring/
cd ~/.openclaw/workspace/skills/videodb-monitoring
npm install
```

2

Set Your API Key

```
openclaw config set skills.entries.videodb-monitoring.env.VIDEODB_API_KEY 'sk-xxx'
```

Get your API key at [console.videodb.io](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) .

3

Start the Monitor

```
cd ~/.openclaw/workspace/skills/videodb-monitoring
nohup npx tsx monitor.ts > ~/.videodb/logs/monitor.log 2>&1 & disown
openclaw gateway restart
```

4

Use It

Ask your agent:

- "Do X on the browser and send me the recording"
- "What did I do in the last hour?"
- "Find when I opened the spreadsheet"

**Cost Note** : VideoDB ingestion is billed at **$0.084 / hour** of captured content. Indexing is on-demand - you only pay for it when you trigger it. See the [Capture SDK overview](\pages\ingest\capture-sdks\overview) for details.

## [ Try Without Setup](#try-without-setup)

Skip installation and try indexing against a hosted live OpenClaw session at [matrix.videodb.io](https://matrix.videodb.io/) :

```
git clone https://github.com/video-db/openclaw-monitoring.git
cd openclaw-monitoring
echo "VIDEO_DB_API_KEY=your_api_key_here" > .env
uv run try_without_setup.py
```

This connects to the public agent's live streams, starts indexing, and prints events to your terminal. Press `Ctrl+C` to stop and search the indexed content.

## [ Privacy &amp; Security](#privacy-&-security)

**API Key Security** - Keys stored locally via OpenClaw config, never transmitted except to VideoDB

**On-Demand Indexing** - AI processing runs only when you trigger it, keeping costs controlled

**Visual Audit Trail** - Complete recordings provide verifiable evidence of agent activity

**Secure Tunneling** - Cloudflare Tunnel for webhook delivery without exposing ports

## Complete Setup Guide on GitHub

Full installation instructions, advanced setup, and troubleshooting

## [ Related Tutorials](#related-tutorials)

## Pair Programmer

AI coding assistant with real-time screen and audio context

## FocusD

AI-powered productivity tracking with automatic time insights

[Pair Programmer](\examples-and-tutorials\ai-copilots\pair-programmer) [Call.md](\examples-and-tutorials\ai-copilots\call-md)

⌘ I