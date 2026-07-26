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

- [The Context Transfer Problem](#the-context-transfer-problem)
- [Built for Agents](#built-for-agents)
- [What's Possible](#what%E2%80%99s-possible)
- [Install VideoDB Skills](#install-videodb-skills)
- [Example Workflows](#example-workflows)
- [Architecture](#architecture)
- [Related Documentation](#related-documentation)

[Agentic Workflows](\examples-and-tutorials\ai-copilots\index)

# Overview

Copy page

Plug video understanding into your agents - meetings, recordings, tutorials, cameras, and desktop perception

Copy page

## [ The Context Transfer Problem](#the-context-transfer-problem)

You are surrounded by videos - meetings, recordings, tutorials, channels, cameras, and even your desktop. The real bottleneck isn't processing power or model capability. It's **context transfer** . Your agents are blind to the visual world you navigate every day. They can't see your Zoom calls, understand your Loom recordings, or follow along as you watch a tutorial. VideoDB changes that.

## [ Built for Agents](#built-for-agents)

VideoDB is built from the ground up for agents. Your AI assistants can now acquire context from:

- **Meetings** - Understand discussions, decisions, and action items
- **Recordings** - Search and reference Loom-style videos, demos, and walkthroughs
- **Desktop perception** - See what you see in real-time
- **Tutorials** - Watch and learn alongside you
- **Cameras** - Monitor physical environments and events

Real-time understanding of your environment changes how you act in the real world.

## [ What's Possible](#what’s-possible)

Imagine **Claude Code** with complete understanding of your meetings and Loom recordings. Start a sharing session and watch a tutorial together - your agent follows along, ready to help implement what you're learning. Imagine **OpenClaw-style agents** recording demos of any app, capturing their autonomous workflows for review and debugging. Imagine **research agents** navigating the internet, producing informative video summaries that cut through the noise - saving you from misinformation and clickbait.

## [ Install VideoDB Skills](#install-videodb-skills)

Add video capabilities to your agent in seconds:

```
npx skills add video-db/skills
```

Then run the setup command in your agent:

```
/videodb setup
```

The setup guides you through obtaining a VideoDB API key (includes $20 free credits, no credit card required), installing the SDK, and verifying the connection.

## View Skills Repository

Complete installation guide and skill documentation

## [ Example Workflows](#example-workflows)

## Pair Programmer

AI coding assistant with real-time screen and audio context

## OpenClaw Monitoring

CCTV for AI agents - monitor, record, and search autonomous agent activity

## Call.md

Real-time AI meeting assistant with dual-channel transcription

## Bloom

Local-first screen recorder with AI processing and natural language search

## Focusd

Productivity tracking with automatic session summaries

## [ Architecture](#architecture)

Capture SDK Architecture showing two-runtime design with backend API key and desktop client token

<!-- image -->

API keys never touch the desktop. Tokens are short-lived. Enterprise-ready security.

## [ Related Documentation](#related-documentation)

## Capture SDK Overview

Full architecture and capabilities

## Real-Time Context

How real-time AI context works

## Privacy Controls

User consent and data protection

## Storage &amp; Search

Persist and search captured content

## MCP Server

Connect VideoDB to Claude and other agents

## Director Framework

Build custom AI agents with VideoDB

[Examples &amp; Tutorials](\examples-and-tutorials) [Pair Programmer](\examples-and-tutorials\ai-copilots\pair-programmer)

⌘ I