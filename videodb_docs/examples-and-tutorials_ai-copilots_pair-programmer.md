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
- [Why This Is Useful](#why-this-is-useful)
- [Use Cases](#use-cases)
- [Getting Started with Pair Programmer](#getting-started-with-pair-programmer)
- [Installation](#installation)
- [Setup](#setup)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [Real-World Examples](#real-world-examples)
- [How It Works](#how-it-works)
- [Related Tutorials](#related-tutorials)

[Agentic Workflows](\examples-and-tutorials\ai-copilots\index)

# Pair Programmer

Copy page

Turn your coding agent into a screen aware, voice aware, context rich collaborator

Copy page

## Pair Programmer on GitHub

Complete source code, installation guide, and configuration examples

## [ What Is It?](#what-is-it)

Pair Programmer is an **agentic skill** that gives your AI coding assistant real time perception. It captures:

- **Screen** for visual context like terminals, editors, browser tabs, errors, and UI state
- **Microphone** for your spoken intent, ideas, and debugging notes
- **System audio** for tutorials, meetings, demos, and anything else your computer is playing

Once captured, that context becomes searchable. So instead of re explaining what was on screen, copy pasting logs, or summarizing a 20 minute debugging session, you can ask:

- *What was I doing when the auth flow broke?*
- *What did I say about the database migration?*
- *Show me what was on screen when the test failed*
- *What happened in the last 10 minutes?*

**The Missing Piece** : This is the missing perception layer for coding agents. Works with Claude Code, Cursor, Codex, and other skill compatible agents.

**Why this changes everything** : Most coding agents operate in a text-only world. They can read your files and write code, but they can't see your terminal output, your browser's error messages, your Figma mockups, or hear you explaining the problem out loud. That means you spend half your time copy-pasting context, describing what's on screen, or re-explaining what you already said 5 minutes ago. Pair Programmer closes this gap. It gives your agent the same sensory context you have-screen, mic, system audio-making collaboration feel natural instead of fragmented.

## [ Why This Is Useful](#why-this-is-useful)

- Context Aware
- Natural Search
- Real-Time Recording

### [ Stay Grounded](#stay-grounded)

Most coding agents can write code. Very few can stay grounded in the same context as you. Pair Programmer helps your agent stay on the same page by giving it access to what you saw, what you said, and what your machine was playing.

### [ Ask in Plain Language](#ask-in-plain-language)

Search your session in natural language:

- "What was I working on when I mentioned the auth bug?"
- "What did I say in the last 5 minutes?"
- "Show me what was on screen when the test failed"

No more copy-pasting or repeated explanations.

### [ Continuous Capture](#continuous-capture)

A lightweight overlay shows recording status, active channels, and elapsed time. Record your screen, mic, and system audio in real time, then search what happened when you need it.

## [ Use Cases](#use-cases)

Pair Programmer is perfect for:

- **Debugging sessions** - Track what you tried and where it went wrong
- **Tutorial driven development** - Build while following video tutorials
- **Bug reproduction** - Capture exact steps that triggered the issue
- **Meeting follow ups** - Search conversations and screen activity
- **Architecture walkthroughs** - Review code with full context
- **Voice first coding workflows** - Speak your thoughts and code together

## [ Getting Started with Pair Programmer](#getting-started-with-pair-programmer)

The most common workflow:

1. **Start recording when you begin work** - just run `/pair-programmer record` and choose your screen. Let it capture in the background.
2. **Work normally** - code, debug, browse Stack Overflow, watch tutorials. Don't think about the recording.
3. **Ask for context when you need it** - stuck on a bug? Run `/pair-programmer search "when did the build error first appear?"` Your agent sees the exact moment with full terminal output and code context.
4. **Let your agent act on spoken instructions** - said "refactor this function to use async/await" into your mic 5 minutes ago? Run `/pair-programmer act` and your agent will do it, using your own words as the spec.
5. **Stop recording when done** - run `/pair-programmer stop` . All context is saved and searchable.

Over time, you'll develop your own patterns-maybe you record only during debugging sessions, or maybe you keep it running all day for complete work memory.

## [ Installation](#installation)

**Prerequisites**

- Node.js 18+
- macOS 12+ or Windows 10+
- [VideoDB API key](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) (free, no credit card required)

If you have an older version installed, remove it first before upgrading.

- Option 1: NPX
- Option 2: Marketplace

### [ Install with npx (Recommended)](#install-with-npx-recommended)

```
npx skills add video-db/pair-programmer
```

### [ Install from marketplace](#install-from-marketplace)

```
/plugin marketplace add video-db/pair-programmer
/plugin install pair-programmer
```

## [ Setup](#setup)

1

Get API Key

Get a free VideoDB API key from [console.videodb.io](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) No credit card required.

2

Set API Key

Export your API key in your shell:

```
export VIDEO_DB_API_KEY = your-key
```

Or add it to a `.env` file in your project root

3

Run Setup

Install dependencies and complete local setup:

```
/pair-programmer setup
```

## [ Quick Start](#quick-start)

1

Start Recording

Start recording your screen, mic, and system audio:

```
/pair-programmer record
```

A source picker will open so you can choose what to capture. Once recording starts, a lightweight overlay shows recording status, active channels, and elapsed time.

2

Work Normally

Continue your coding session. Pair Programmer captures everything in the background.

3

Search Your Session

Search your session in natural language:

```
/pair-programmer search "what was I working on when I mentioned the auth bug?"
```

```
/pair-programmer search "what did I say in the last 5 minutes?"
```

```
/pair-programmer search "show me what was on screen when the test failed"
```

4

Get Summary

Get a summary of recent activity:

```
/pair-programmer what-happened
```

5

Stop Recording

Stop recording when you're done:

```
/pair-programmer stop
```

## [ Commands](#commands)

| Command                             | Description                                                  |
|-------------------------------------|--------------------------------------------------------------|
| `/pair-programmer record`           | Start recording and open the source picker                   |
| `/pair-programmer stop`             | Stop the active recording                                    |
| `/pair-programmer search "<query>"` | Search screen, mic, and audio context using natural language |
| `/pair-programmer what-happened`    | Summarize recent activity                                    |
| `/pair-programmer setup`            | Install dependencies and complete local setup                |
| `/pair-programmer config`           | Update indexing and recording settings                       |

## [ Real-World Examples](#real-world-examples)

Debugging Complex Issues

You're chasing a bug across multiple files and terminals. Instead of documenting every step, just keep coding. Later, run:

```
/pair-programmer search "what was on screen when the test failed"
```

Get instant context about terminal output, error messages, and which files you had open.

Learning From Tutorials

Following a video tutorial while coding? Pair Programmer captures both the tutorial (system audio) and your implementation (screen).

```
/pair-programmer search "build me the project from the video I was just watching"
```

Your agent sees what was on screen and heard what was being said in the tutorial.

Pair Programming Sessions

In a meeting discussing code? Pair Programmer captures your screen and the conversation.

```
/pair-programmer what-happened
```

Get a summary of what was discussed, what code was reviewed, and action items.

Voice-Driven Development

Speaking your thoughts while coding? Your microphone captures your debugging notes and ideas.

```
/pair-programmer search "what did I say about the database migration?"
```

Find moments where you verbally explained your thinking.

## [ How It Works](#how-it-works)

Pair Programmer uses VideoDB's Capture SDK to:

1. **Record** - Continuously capture screen, microphone, and system audio
2. **Process** - Stream to VideoDB for real-time AI indexing
3. **Search** - Query across all captured context with natural language
4. **Retrieve** - Get timestamped results with relevant clips

All context is searchable in real-time, giving your coding agent full perception of your workflow.

## Complete Setup Guide on GitHub

Detailed installation instructions, troubleshooting tips, and configuration examples

## [ Related Tutorials](#related-tutorials)

## Bloom

Local-first screen recorder with AI-ready search and indexing

## Focusd Productivity Tracker

AI-powered productivity tracking with automatic time insights

## Call.md

Real-time AI meeting assistant with live coaching

[Overview](\examples-and-tutorials\ai-copilots) [OpenClaw Monitoring](\examples-and-tutorials\ai-copilots\openclaw-monitoring)

⌘ I