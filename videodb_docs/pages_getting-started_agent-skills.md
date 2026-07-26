### Start Here

- [Welcome to VideoDB](\)
- [Quickstart](\pages\getting-started\quickstart)
- SDK Installation
- [AI Agent Skills](\pages\getting-started\agent-skills)
- [Core Concepts in 5 Minutes](\pages\getting-started\core-concepts-in-5-min)

### Core Concepts

- [Core Concepts Overview](\pages\core-concepts\overview)
- [Data Model](\pages\core-concepts\data-model)
- [Indexes &amp; Search](\pages\core-concepts\indexes-and-search)
- [Events &amp; Real-time](\pages\core-concepts\events-and-realtime)
- [Programmable Editing](\pages\core-concepts\programmable-editing)
- [Security &amp; Privacy](\pages\core-concepts\security-privacy)

### Ingest

- Files and Collections
- Live Streams
- Capture SDKs
- Transcoding

### Understand

- Indexing Pipelines
- Search and Retrieval
- Quality and Evaluation

### Act

- Programmable Editing
- Live Action
- Generative Media
- Output and Delivery

### Automate

- [Integrations Overview](\pages\automate\integrations-overview)
- n8n Workflows
- Zapier Workflows

### Open Source Frameworks

- [MCP Server](\pages\build-with-agents\mcp-server)
- [LlamaIndex Retriever](\pages\community\open-source\llamaindex-retriever)
- Director Framework

## On this page

- [Install VideoDB Skills](#install-videodb-skills)
- [Prerequisites](#prerequisites)
- [What It Does](#what-it-does)
    - [Why Use It](#why-use-it)
    - [Quick Start](#quick-start)
    - [Capabilities](#capabilities)
- [Example: OpenClaw Monitoring](#example-openclaw-monitoring)
- [Next Steps](#next-steps)

[Start Here](\index)

# AI Agent Skills

Copy page

Add video and audio perception to your AI agents - capture, upload, search, edit, and stream

Copy page

Your AI agents can write code and automate tasks brilliantly. But they're missing one critical capability: the ability to work with video and audio - capturing screens, searching through recordings, editing clips, and streaming results. VideoDB Skills give agents like Claude Code and Codex the power to execute server-side video workflows, turning text-only agents into multimodal collaborators.

## [ Install VideoDB Skills](#install-videodb-skills)

Get video and audio perception in your agent with one command:

- NPX (Recommended)
- Claude Code Plugin

```
npx skills add video-db/skills
```

```
/plugin marketplace add video-db/skills
/plugin install videodb@videodb-skills
```

Then run `/videodb setup` to configure your API key and verify connectivity.

## VideoDB Skills on GitHub

Complete source code, installation guide, and configuration examples

## [ Prerequisites](#prerequisites)

1

VideoDB API Key

Get a free API key from [console.videodb.io](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) No credit card required. Free tier includes 50 uploads.

2

System Requirements

- **Python 3.9+**
- **Platform** : macOS, Linux, Windows (PowerShell)

3

Set Your API Key

Export your API key in your shell:

```
export VIDEO_DB_API_KEY = your-key-here
```

Or add it to a `.env` file in your project root.

## [ What It Does](#what-it-does)

VideoDB Skills is a perception capability that enables **See → Understand → Act, as an API, for video and audio** . It gives agents like Claude Code, Codex, and Cursor the ability to execute server-side video workflows. One unified interface for:

- **See** - Capture desktop screens, microphone/system audio, RTSP streams, and ingest files, URLs, and YouTube content
- **Understand** - Visual analysis, transcription, indexing, and searching moments with playable clips
- **Act** - Stream results, trigger alerts, edit timelines, generate subtitles/overlays, and export clips

### [ Why Use It](#why-use-it)

- Video Workflows
- Real-Time Perception
- Search &amp; Intelligence

Execute video operations without local ffmpeg installation:

- Upload from YouTube, URLs, or local files
- Trim, merge, clip, overlay text/images/audio
- Transcode, reframe, adjust resolution and aspect ratio
- Get instant playable HLS links via built-in CDN

Capture and analyze live feeds:

- Desktop screen, microphone, and system audio recording
- Monitor RTSP camera feeds with event detection
- Generate structured context from desktop streams
- Log alerts with timestamps for person detection

Find moments by speech, scenes, or metadata:

- "Identify all scenes showing 'phone close-up'"
- "Capture my screen and report activities with insights"
- Timestamped transcripts and subtitles
- Playable evidence clips with exact timestamps

### [ Quick Start](#quick-start)

Ask your agent to execute video tasks:

```
Upload [YouTube URL] and provide a shareable stream link
```

```
Extract clips from 10s-30s and 45s-60s and merge them
```

```
Generate background music and add to this clip
```

```
Add white text on black background subtitles to the original video
```

```
Capture my screen for two minutes and report my activities with insights
```

```
Monitor my IP Camera RTSP stream and log person detection alerts with timestamps
```

### [ Capabilities](#capabilities)

| Capability            | What It Does                                                          |
|-----------------------|-----------------------------------------------------------------------|
| **Capture**           | Desktop screen, microphone, and system audio for real-time processing |
| **Upload**            | Ingest from YouTube, URLs, or local files                             |
| **Context**           | Generate structured context from RTSP feeds or desktop streams        |
| **Search**            | Locate moments by speech, scenes, or metadata with playable evidence  |
| **Transcripts**       | Generate timestamped transcripts                                      |
| **Subtitles**         | Auto-generate, style, and burn-in subtitles                           |
| **Edit**              | Trim, merge, clip, overlay text/images/audio; add dubbing/translation |
| **AI Generate**       | Create images, video, music, sound effects, voiceovers                |
| **Transcode/Reframe** | Adjust resolution, quality, aspect ratio, social crops server-side    |
| **Stream**            | Obtain instant playable HLS links via built-in CDN                    |

## [ Example: OpenClaw Monitoring](#example-openclaw-monitoring)

VideoDB Skills powers [OpenClaw Monitoring](https://github.com/video-db/openclaw-monitoring) - "CCTV for AI agents" that monitors, records, and audits autonomous agent sessions. Every agent run becomes a live stream, replayable recording, and searchable archive.

## OpenClaw Monitoring on GitHub

See how VideoDB Skills enables visual observability for autonomous agents

## [ Next Steps](#next-steps)

## Capture SDK Overview

Deep dive: channels, permissions, client code, and event handling

## Real-time Context

How real-time indexing and search works

## AI Copilot Examples

Explore more AI copilot projects and use cases

## Quickstart

Try desktop perception with a hosted OpenClaw agent

[Node.js SDK v0.2.0 Migration](\pages\getting-started\node-migration) [Core Concepts in 5 Minutes](\pages\getting-started\core-concepts-in-5-min)

⌘ I