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
- [Why You Need This](#why-you-need-this)
- [How It Works](#how-it-works)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
    - [MCP Server Setup](#mcp-server-setup)
- [Privacy &amp; Data](#privacy-%26-data)
- [Related Tutorials](#related-tutorials)

[Agentic Workflows](\examples-and-tutorials\ai-copilots\index)

# Call.md

Copy page

Turn meetings into live agent loops - real-time AI meeting assistant with dual-channel transcription and intelligent automation

Copy page

## Call.md on GitHub

Complete source code, installation guide, and configuration

## [ What Is It?](#what-is-it)

Your AI meeting assistant, live during every call. Most meeting tools transcribe after the fact. Call.md is different: it understands your meeting as it happens, giving you AI-powered suggestions, conversation metrics, and automatic tool triggers in real-time. It's like having an AI copilot who watches your meeting, tracks engagement, and whispers helpful context right when you need it. After the call ends, it generates three-part summaries (overview, key points, action items) and can automatically update your CRM or project management tools through workflow webhooks. If you've used Otter.ai or Fireflies.ai, think of Call.md as the same idea but built for agent automation-not just passive transcription, but active intelligence during and after meetings.

**The Power** : During calls, AI generates contextual suggestions, monitors conversation balance, and automatically triggers your MCP tools when information needs arise - all in real-time.

## [ Why You Need This](#why-you-need-this)

- Live Intelligence
- Meeting Intelligence
- Agent Integration

### [ During the Meeting](#during-the-meeting)

Get real-time assistance while you talk:

- AI-generated suggestions (things to say, questions to ask)
- Conversation metrics (talk ratio, pace, questions asked)
- MCP tools triggered automatically from conversation context
- Coaching nudges when conversation needs steering

### [ Post-Meeting Analysis](#post-meeting-analysis)

Comprehensive summaries after every call:

- Three-part AI summary (overview, key points, action items)
- Full transcript with dual-channel separation
- Conversation metrics and engagement statistics
- Markdown export with complete meeting intelligence

### [ MCP Automation](#mcp-automation)

Connect your agent ecosystem:

- Auto-triggers MCP tools during conversations
- Results appear inline during meetings
- Workflow webhooks to n8n, Zapier, CRMs
- Agent-ready structured output

## [ How It Works](#how-it-works)

1

Dual-Channel Transcription

Captures your mic (labeled "you") and system audio (labeled "them") separately. This separation powers all downstream intelligence.

**Why Dual-Channel Matters** : Separating "you" (microphone) from "them" (system audio) isn't just for attribution. It enables Call.md to track conversation balance, detect when one person is dominating, measure your speaking pace independently, and generate insights like "You asked 3 questions but the client asked 0-they might not be engaged." Single-channel transcription can't do this.

1

Live Assist

Every 20 seconds, AI analyzes recent transcript and generates contextual suggestions: things to say, questions to ask.

2

Conversation Metrics

Real-time tracking of talk ratio, speaking pace (WPM), questions asked, and monologue detection. No LLM required - pure statistics.

3

MCP Auto-Triggering

Intent detector scans conversation for information needs (active or passive). When detected, automatically calls relevant MCP tools and displays results inline.

4

Post-Meeting Intelligence

When the meeting ends, generates three parallel summaries: narrative overview, key points by topic, and action items. Sends to workflow automation platforms.

## [ Key Features](#key-features)

Recording &amp; Transcription

**Real-Time Speech-to-Text**

- Separate channels for you and them
- Live transcription powered by VideoDB
- Recording history with full transcripts
- Screen, mic, and system audio capture

Live Assist

**AI-Generated Suggestions**

- Contextual things to say
- Questions to ask
- Updates every 20 seconds
- Based on recent conversation context

Conversation Metrics

**Track Engagement**

- Talk ratio (you vs them)
- Speaking pace and question count
- Engagement score
- Monologue detection (45s threshold)

MCP Integration

**Model Context Protocol**

- Auto-triggers tools from conversation
- Runs every 20 seconds
- Max 3 tool calls per run
- Results display inline during meetings
- Supports stdio and HTTP servers

MCP Auto-Triggering Example

**How it works in practice:** During a sales call, the client mentions "Can you send me pricing for the enterprise plan?" The MCP intent detector recognizes this as an information need, automatically calls your CRM tool to fetch the pricing doc, and displays it inline. You see the result immediately and can reference it without breaking flow. Or: A customer says "I'm seeing error code 502." The MCP agent searches your knowledge base tool, finds relevant docs, and shows them to you in real-time-before you even finish taking notes. This happens automatically every 20 seconds based on conversation context. You configure which MCP tools are available; the agent decides when to call them.

Post-Meeting Summaries

**Three-Part AI Analysis**

- Short overview (3-5 sentence narrative)
- Key points by topic (attributed to participants)
- Action items (3-10 concrete next steps)
- Generated in parallel for speed

Workflow Webhooks

**Automation Integration**

- Auto-send to n8n, Zapier, CRMs
- Triggered when meeting ends
- Structured data payload
- Agent-ready output format

Meeting Preparation

**Setup Wizard**

- AI-generated probing questions
- Dynamic discussion checklist
- Google Calendar integration
- Sync upcoming meetings

Bookmarking

**Mark Important Moments**

- Quick bookmark during calls
- Review later with context
- Share with team

## [ Tech Stack](#tech-stack)

Built for performance and reliability:

## Electron 34

Desktop application shell

## React 19 + TypeScript 5.8

Modern UI with full type safety

## tRPC 11

Type-safe API layer

## Drizzle + SQLite

Local offline-first storage

## VideoDB SDK (0.2.4)

Recording and transcription

## MCP SDK (1.0.0)

Model Context Protocol integration

## OpenAI SDK (6.19.0)

LLM calls via VideoDB API

## Tailwind + shadcn/ui

Beautiful, modern interface

## [ Getting Started](#getting-started)

**Prerequisites**

- macOS 12+ (Monterey or later) or Windows 10+
- [VideoDB API key](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) (free tier available)

1

Install Call.md

**macOS** (Apple Silicon &amp; Intel):

```
curl -fsSL https://artifacts.videodb.io/call.md/install | bash
```

*Currently available for macOS and Windows - Linux support coming soon*

2

Launch and Register

1. Launch Call.md from Applications or Spotlight
2. Enter your VideoDB API key ( [get one free](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) )
3. Grant system permissions when prompted

3

Configure Recording

Configure preferences:

- Enable microphone capture
- Enable system audio capture
- Select screen to record
- Optionally connect Google Calendar

4

Start Your First Meeting

1. Click "New Meeting" from home screen
2. Optionally run Meeting Setup wizard
3. Click "Start Recording"
4. Watch live transcription and intelligence

**macOS Permissions Required** Grant in **System Preferences &gt; Privacy &amp; Security** :

- Microphone (for voice recording)
- Screen Recording (for screen capture)

## [ Configuration](#configuration)

All features are configurable through Settings:

| Feature              | Customizable                               |
|----------------------|--------------------------------------------|
| Live Assist          | Enable/disable, configure timing           |
| Conversation Metrics | Set thresholds for talk ratio alerts       |
| MCP Servers          | Add stdio/HTTP servers, manage connections |
| Workflow Webhooks    | Configure n8n, Zapier, or custom endpoints |
| Google Calendar      | Connect/disconnect calendar sync           |

### [ MCP Server Setup](#mcp-server-setup)

Connect MCP servers in **Settings → MCP Servers** :

1. Click **Add Server**
2. Choose transport: **stdio** (local) or **http** (remote)
3. Configure connection details
4. Click **Connect**

The MCP agent runs automatically during meetings, detects information needs from conversation, and triggers relevant tools. Results appear inline in the **MCP Results** panel.

## [ Privacy &amp; Data](#privacy-&-data)

**Local Database** - All data stored in SQLite at `~/Library/Application Support/call-md/`

**Secure Storage** - API keys encrypted, credentials protected

**User Control** - Delete recordings anytime, export transcripts

**Transcription via VideoDB** - AI features require internet connectivity

## Complete Setup Guide on GitHub

Detailed installation instructions, configuration options, and troubleshooting guide

## [ Related Tutorials](#related-tutorials)

## Bloom

Screen recorder with AI search for async video documentation

## Pair Programmer

AI coding assistant with real-time screen and audio context

## Focusd

AI-powered productivity tracking with automatic time insights

[OpenClaw Monitoring](\examples-and-tutorials\ai-copilots\openclaw-monitoring) [Bloom](\examples-and-tutorials\ai-copilots\bloom)

⌘ I