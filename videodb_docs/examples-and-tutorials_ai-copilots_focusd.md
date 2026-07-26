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
- [Why It's Different](#why-it%E2%80%99s-different)
- [The 5-Layer Pipeline](#the-5-layer-pipeline)
- [Key Features](#key-features)
- [Who It's For](#who-it%E2%80%99s-for)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Privacy First](#privacy-first)
- [Related Tutorials](#related-tutorials)

[Agentic Workflows](\examples-and-tutorials\ai-copilots\index)

# Focusd - Productivity and Personal Work Memory

Copy page

AI-powered desktop app that records your screen, understands what you're doing, and builds your personal work memory

Copy page

## Focusd on GitHub

Complete source code, installation guide, and demo download

## [ What Is It?](#what-is-it)

Your personal productivity oracle. You know that sinking feeling at 5 PM when you wonder "where did my day go?" Or when you bill clients and can't remember what you worked on Tuesday morning? Or when you want to optimize your workflow but have no data about where time actually goes? Focusd solves this by running invisibly all day, watching your screen and understanding context-not just "you used Chrome," but "what you were reading in Chrome and which project it relates to." No manual timers. No app-switching. No logging. Just automatic, intelligent tracking that tells you where your time went, what you accomplished, and how to improve tomorrow.

**The Insight** : "You spent 2.3 hours on the authentication refactor, switching between VSCode (67%) and documentation (33%). You were blocked for 23 minutes waiting for builds. Consider optimizing your build pipeline."

**Platform Support** : macOS and Windows (Linux support coming soon)

## [ Why It's Different](#why-it’s-different)

- Zero Manual Work
- AI Understanding
- Actionable Insights

### [ Automatic Everything](#automatic-everything)

Forget manual time tracking. Focusd:

- Records continuously in background
- Understands context from your screen
- Detects when you switch projects
- Identifies productive vs idle time
- Generates summaries automatically

### [ Smart Analysis](#smart-analysis)

Not just "you used Chrome for 3 hours." Focusd knows:

- *What* you were reading in Chrome
- *Which* project you were working on
- *Why* you switched contexts
- *How* productive each session was

### [ Real Improvements](#real-improvements)

Daily recaps include:

- Session summaries with context
- App usage breakdown by project
- Productivity patterns identified
- Specific suggestions to improve

## [ The 5-Layer Pipeline](#the-5-layer-pipeline)

Focusd transforms raw screen captures into structured insights through intelligent summarization:

1

L0: Raw Events

Screen indexed every ~3 seconds. Extracts app names, page titles, visible content.

2

L1: Activity Segments

Events grouped into time-based chunks (e.g., 5-minute windows).

3

L2: Micro-Summaries

Each segment summarized by LLM: *what you did, which app, productive or not* .

4

L3: Session Summaries

Micro-summaries roll up into session overviews with app stats and project breakdown.

5

L4: Daily Summary

Everything consolidates into a headline, highlights, and actionable suggestions.

**Why 5 Layers?** This hierarchical approach balances cost, accuracy, and latency. Layer 0 captures everything (cheap, fast). Layers 1-2 group and summarize in small batches (moderate cost). Layers 3-4 synthesize larger contexts (higher cost but fewer calls). The result: near-instant activity tracking at the bottom, actionable insights at the top, and a reasonable API bill. Without this structure, running LLM calls on every screen capture would be prohibitively expensive.

## [ Key Features](#key-features)

Live Activity Timeline

Real-time feed of what you're doing, updated every few seconds. See your work unfold as it happens.

🤖 AI Session Summaries

Automatic overviews of each work session:

- What you worked on
- Which apps you used
- Projects and time breakdown
- Productivity assessment

🔍 Drill Down Analysis

Select any time range for detailed breakdown:

- App usage percentages
- Project time distribution
- Context from screen captures

📈 Dashboard Analytics

Visual insights:

- Total tracked time
- Productive time percentage
- Top applications used
- Project distribution

Daily Recap

End-of-day report with:

- Headline summary
- Session highlights
- Productivity insights
- Tomorrow's suggestions

🕐 History Browser

Browse past days with full summaries and activity data. Understand your weekly and monthly patterns.

## [ Who It's For](#who-it’s-for)

## Freelancers

Track client projects automatically. Generate accurate time reports without manual logging.

## Developers

Understand where coding time goes. Identify interruptions, context switches, and optimize your flow.

## Knowledge Workers

See how much time you spend in meetings vs deep work. Find patterns in your most productive hours.

## Remote Workers

Stay accountable without micromanagement. Get insights into your work patterns and share summaries with your team.

## [ Tech Stack](#tech-stack)

Built with modern desktop technologies for performance and reliability:

## Electron + React

Desktop app shell with React UI

## TypeScript

Type-safe throughout

## SQLite

Local data storage for privacy

## VideoDB SDK

Screen capture and AI indexing

## OpenAI

LLM for summarization pipeline

## Recharts

Dashboard visualizations

## [ Getting Started](#getting-started)

**Prerequisites**

- macOS 12+ (Apple Silicon or Intel) or Windows 10+
- Node.js 18+
- [VideoDB API key](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs)

1

Clone and Install

```
git clone https://github.com/video-db/focusd.git
cd focusd
npm install
```

2

Configure API Key

Copy `.env.sample` to `.env` and add your VideoDB API key.

3

Run Development Mode

Run `npm run dev` to start the app in development mode.

4

Grant Permissions

macOS will prompt for Screen Recording permission. Grant it in System Settings.

5

Start Tracking

Hit the record button. Wait a few minutes, then check your live timeline and dashboard!

**System Permissions** Required in **System Settings &gt; Privacy &amp; Security** :

- Screen Recording (mandatory)
- System Audio Recording (optional, for audio context)

## [ Configuration](#configuration)

All settings adjustable from the Settings page:

| Setting                | Default   | Purpose                              |
|------------------------|-----------|--------------------------------------|
| `segment_flush_mins`   | 5 min     | How often events group into segments |
| `micro_summary_mins`   | 10 min    | Frequency of segment summarization   |
| `session_summary_mins` | 30 min    | Session-level summary generation     |
| `idle_threshold_mins`  | 5 min     | Inactivity threshold before pausing  |

Tweak these to balance between insight granularity and performance.

## [ Privacy First](#privacy-first)

**Local Storage** - All data stored in SQLite on your machine ( `~/Library/Application Support/VideoDB Focusd/` )

**Encrypted Keys** - API keys stored in macOS Keychain via Electron's safeStorage

**No Cloud Storage** - Summaries generated, then stored locally. Screen captures processed and discarded.

**Full Control** - Delete all data anytime: `rm -rf ~/Library/Application\ Support/VideoDB\ Focusd/`

## Complete Setup Guide on GitHub

Detailed installation instructions, configuration guide, and troubleshooting help

## [ Related Tutorials](#related-tutorials)

## Bloom

Screen recorder for creating searchable video documentation

## Pair Programmer

Transform Claude Code into a context-aware AI coding assistant

## Capture SDK Overview

Learn how to build screen capture apps with VideoDB

[Bloom](\examples-and-tutorials\ai-copilots\bloom) [Overview](\examples-and-tutorials\video-rag)

⌘ I