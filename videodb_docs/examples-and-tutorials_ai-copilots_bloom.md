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
- [When to Use Bloom](#when-to-use-bloom)
- [Why You Need This](#why-you-need-this)
- [How It Works](#how-it-works)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Privacy &amp; Data](#privacy-%26-data)
- [Related Tutorials](#related-tutorials)

[Agentic Workflows](\examples-and-tutorials\ai-copilots\index)

# Bloom

Copy page

Open-source, local-first screen recorder with AI processing - record, upload to VideoDB, and query with natural language

Copy page

## Bloom on GitHub

Complete source code, installation guide, and configuration

## [ What Is It?](#what-is-it)

Your local-first screen recorder, built for AI workflows. Bloom records on your machine (no lock-in), automatically uploads to VideoDB for transcription and indexing, then lets you search any moment with natural language. It's Loom meets agent-ready infrastructure.

**The Power** : Your recordings become queryable data. Search "when did I mention the deadline?" or "show me the deployment steps" - get timestamped clips with context.

## [ When to Use Bloom](#when-to-use-bloom)

Bloom shines in scenarios where you need recordings to become searchable data:

- **Sales demos** : Record product demos once, search forever. "Show me when we explained the pricing model to enterprise clients last month."
- **Bug reproduction** : Capture exact steps that trigger issues, then let teammates search "when did the error first appear?"
- **Tutorial learning** : Following along with video courses? Record your implementation so AI assistants can reference both the tutorial and your work.
- **Async team updates** : Record your screen while explaining complex work. Teammates can search the recording instead of watching the whole thing.
- **Personal knowledge base** : Capture important calls and workshops. Search months later when you need to remember "what did we decide about the API design?"

## [ Why You Need This](#why-you-need-this)

- Local-First
- AI-Ready
- Agent Integration

### [ No Lock-In](#no-lock-in)

Your files stay on your machine:

- Record locally, no forced cloud upload
- Pay only for AI processing (when you need it)
- Export and own your recordings
- No subscription, no storage limits

### [ Make Recordings Searchable](#make-recordings-searchable)

Transform video into queryable data:

- Automatic transcription of spoken words
- Visual embeddings for scene understanding
- Metadata extraction from content
- Natural language search across all recordings

### [ Built for Agents](#built-for-agents)

Access recordings from AI workflows:

- Query via VideoDB API
- Compatible with Claude Code and agent frameworks
- Structured data output for automation
- Shareable links for team access

## [ How It Works](#how-it-works)

1

Record Locally

Capture screen, microphone, system audio, and camera with a floating control bar. Multi-monitor support lets you choose which display to record.

2

Upload to VideoDB (Optional but Powerful)

As you record, Bloom can sync chunks to VideoDB Cloud in real-time. Why? Processing video on your local machine would drain battery and CPU. By streaming to VideoDB, the heavy lifting-transcription, visual indexing, embedding generation-happens server-side while you keep working. You keep the local file, VideoDB keeps the intelligence.

3

Process with AI

VideoDB indexes spoken words, generates transcripts, and creates subtitled streams. Visual embeddings make every frame searchable.

4

Query Anywhere

Search your recordings with natural language. "Show me when I explained the architecture" returns timestamped clips with full context.

5

Share or Integrate

One-click shareable links, VideoDB Chat for questions, or API access for agent frameworks. Download MP4 files anytime.

## [ Key Features](#key-features)

Recording &amp; Capture

**Complete Desktop Capture**

- Screen recording with multi-monitor support
- Microphone and system audio capture
- Draggable camera bubble overlay
- Display picker to choose which screen
- Global keyboard shortcut: `Cmd+Shift+R`
- Always-on-top floating control bar

Library Management

**Organize Your Recordings**

- Browse all recordings with search
- Sort by date (newest/oldest)
- Rename recordings in-place
- Delete with confirmation
- Download recordings as MP4
- Keyboard navigation (arrow keys, delete key)

AI Processing

**Automatic Intelligence**

- Transcription of spoken words via VideoDB
- Subtitle generation for video playback
- HLS streaming with in-app player
- Visual indexing for scene search
- Metadata extraction from content

Sharing &amp; Integration

**Connect with Workflows**

- One-click shareable links for any recording
- VideoDB Chat to query recordings with AI
- Download MP4 files for offline use
- API access for agent frameworks
- Integration with Claude Code and other tools

Developer Experience

**Open Source &amp; Customizable**

- Full UI source code available (MIT license)
- System tray integration with status indicator
- Light/dark theme support
- Permission management for mic, screen, camera
- Local SQLite database for metadata

## [ Tech Stack](#tech-stack)

Built for performance and reliability:

## Electron 39.7

Desktop application shell

## Node.js 18+

JavaScript runtime

## VideoDB SDK 0.2.4

Recording and AI processing

## SQLite (sql.js)

Local metadata storage

## HLS.js

In-app video playback

## Universal Binary

Apple Silicon + Intel support

## [ Getting Started](#getting-started)

**Prerequisites**

- macOS 12+ or Windows 10+ (Linux support coming soon)
- [VideoDB API key](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) (free tier available)

1

Install Bloom

**Automated installation** (recommended):

```
curl -fsSL https://artifacts.videodb.io/bloom/install | bash
```

**Manual installation:**

- **Apple Silicon (M1/M2/M3/M4)** : [bloom-2.2.0-arm64.dmg](https://artifacts.videodb.io/bloom/bloom-2.2.0-arm64.dmg)
- **Apple Intel** : [bloom-2.2.0-x64.dmg](https://artifacts.videodb.io/bloom/bloom-2.2.0-x64.dmg)
- **Windows** : [bloom-2.2.0-x64.exe](https://artifacts.videodb.io/bloom/bloom-2.2.0-x64.exe)

For manual install: mount the DMG and drag Bloom to Applications, then run:

```
xattr -cr /Applications/Bloom.app
```

2

Launch and Register

1. Launch Bloom from Applications or Spotlight
2. Enter your VideoDB API key ( [get one free](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) )
3. Grant system permissions when prompted

3

Grant Permissions

Bloom needs access to:

- **Microphone** - For voice recording
- **Screen Recording** - For screen capture
- **Camera** (optional) - For camera bubble overlay

Grant these in **System Settings &gt; Privacy &amp; Security** .

4

Start Recording

1. Press `Cmd+Shift+R` or click the Bloom icon in system tray
2. Choose your display from the picker
3. Toggle camera, mic, and system audio as needed
4. Click **Start Recording**

**macOS Permissions Required** Grant in **System Settings &gt; Privacy &amp; Security** :

- Microphone (for voice recording)
- Screen Recording (for screen capture)
- Camera (for camera overlay, optional)

## [ Configuration](#configuration)

All features are configurable through the Bloom interface:

| Feature           | Customizable                                             |
|-------------------|----------------------------------------------------------|
| Recording sources | Enable/disable mic, system audio, camera                 |
| Display selection | Choose which screen to record                            |
| Camera position   | Drag camera bubble anywhere on screen                    |
| Keyboard shortcut | Default: `Cmd+Shift+R`                                   |
| Theme             | Light or dark mode                                       |
| Storage location  | Local database at `~/Library/Application Support/bloom/` |

## [ Privacy &amp; Data](#privacy-&-data)

**Local Recording** - Files saved on your machine first, cloud upload is optional

**No Lock-In** - Download recordings anytime, export as MP4

**Encrypted Storage** - API keys encrypted, credentials protected

**User Control** - Delete recordings locally and from cloud independently

## Complete Setup Guide on GitHub

Detailed installation instructions, troubleshooting guide, and development setup

## [ Related Tutorials](#related-tutorials)

## Pair Programmer

AI coding assistant with screen and audio context

## Focusd

AI-powered productivity tracking with automatic insights

## Call.md

Real-time AI meeting assistant with live intelligence

[Call.md](\examples-and-tutorials\ai-copilots\call-md) [Focusd](\examples-and-tutorials\ai-copilots\focusd)

⌘ I