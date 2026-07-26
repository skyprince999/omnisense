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

- [How It Works](#how-it-works)
- [Skills: Native Agent Experiences](#skills-native-agent-experiences)
- [What You Can Build](#what-you-can-build)
- [Example: Real-time Alerting](#example-real-time-alerting)
- [Install the SDK](#install-the-sdk)
- [Philosophy](#philosophy)

[Start Here](\index)

# Welcome to VideoDB

Copy page

The perception, memory, and action for AI agents

Copy page

Your agents can read text and static images. But the real world is live, continuous, and always changing. To operate with real context, your agent needs real-time access to video calls, camera feeds, screen recordings, and live internet streams. VideoDB is the perception layer that lets agents see, hear, remember, and act on continuous media. Most AI development focuses on text and static images, but video remains a significant hurdle because of its density and lack of structure. VideoDB turns raw pixel data into structured context that agents can query, reason about, and act upon in real time. For agents to move beyond text boxes and interact with the physical or digital world via screens and cameras, they need a way to parse continuous visual and auditory data. VideoDB provides this through a specialized database that indexes video at the scene level - making it possible for an agent to "recall" specific events or "see" real-time occurrences without excessive compute costs.

## Quickstart

Give your agent perception in 5 minutes

## Core Concepts

Understand the platform architecture

### [ How It Works](#how-it-works)

The platform operates through three stages: **See** , **Understand** , and **Act** .

| Stage          | What Happens                                                                               |
|----------------|--------------------------------------------------------------------------------------------|
| **See**        | Capture SDK or live stream integration takes in media from files, desktops, or cameras     |
| **Understand** | Build specialized indexes for transcripts, visual scenes, or custom prompts                |
| **Act**        | Query, search, edit, and export - agents can generate summaries or clips based on findings |

Rather than merely storing video files, the platform indexes frames and audio to support semantic retrieval. This allows an agent to ask for a specific moment in a continuous stream without downloading or processing the entire file. The architecture sits above transport protocols and below the reasoning engine. This separation means you can use VideoDB with any Large Language Model or Large Video Model. By consolidating transcription, frame extraction, vector indexing, and video playback into a single platform, VideoDB addresses the high total cost of ownership typically associated with video AI.

### [ Skills: Native Agent Experiences](#skills-native-agent-experiences)

Since VideoDB handles server-side video processing, indexing, and retrieval, developers can use [skills](\pages\getting-started\agent-skills) to create agent workflows that feel native to their environment. Skills give agents like Claude Code and Codex structured perception primitives - capture, search, edit, stream - without writing infrastructure code.

```
npx skills add video-db/skills
```

## [ What You Can Build](#what-you-can-build)

## Desktop Agents

Stream screen, mic, and camera. Get real-time context about what the user is doing and saying. [Call.md →](\examples-and-tutorials\ai-copilots\call-md)

## Video Search

Search across hours of meetings, lectures, or archives. Get timestamped moments with playable evidence. [Multimodal Search →](\examples-and-tutorials\video-rag\multimodal-search)

## Real-time Monitoring

Connect RTSP cameras and drones. Detect events as they happen. Trigger alerts and automations. [Intrusion Detection →](\examples-and-tutorials\live-intelligence\intrusion-detection)

## Media Automation

Compose videos with code. Generate voice, music, and images. Export to any format. [Faceless Video Creator →](\examples-and-tutorials\content-factory\faceless-video-creator)

## Agent Skills

Add real-time perception to coding assistants and autonomous agents. Screen capture, audio indexing, and searchable context. [Agent Skills →](\pages\getting-started\agent-skills)

## Browse All Examples

Explore examples across AI Copilots, Video Search, Live Intelligence, Content Factory, and more

## [ Example: Real-time Alerting](#example-real-time-alerting)

Python

Node.js

```
import videodb

conn = videodb.connect()

# See: Get an active stream (from desktop capture or RTSP)
rtstream = conn.get_rtstream( "rts-abc123" )

# Understand: Create indexes on the live stream
visual_index = rtstream.index_visuals( prompt = "Describe what the user is doing" )
audio_index = rtstream.index_audio( prompt = "Extract key decisions and action items" )

# Act: Create an event and attach an alert
event = conn.create_event(
event_prompt = "Detect when someone mentions a deadline or due date"
)
alert = audio_index.create_alert(
webhook_url = "https://your-backend.com/webhooks/deadline-mentioned"
)

# Real-time events arrive via WebSocket or webhook
# { "channel": "alert", "timestamp": "2026-02-11T12:18:00.968810+00:00", "rtstream_id": "rts-xxx", "rtstream_name": "Meeting", "data": { "event_id": "event-77aae6b981970542", "label": "objection", "triggered": true, "confidence": 0.9, "start": 1770812246.3445818, "end": 1770812277.3488276 } }
```

```
import { connect } from 'videodb' ;

const conn = connect ();

// See: Get an active stream (from desktop capture or RTSP)
const rtstream = await conn . getRtstream ( "rts-abc123" );

// Understand: Create indexes on the live stream
const visualIndex = await rtstream . indexVisuals ({ prompt: "Describe what the user is doing" });
const audioIndex = await rtstream . indexAudio ({ prompt: "Extract key decisions and action items" });

// Act: Create an event and attach an alert
const event = await conn . createEvent ({
eventPrompt: "Detect when someone mentions a deadline or due date"
});
const alert = await audioIndex . createAlert ({
webhookUrl: "https://your-backend.com/webhooks/deadline-mentioned"
});

// Real-time events arrive via WebSocket or webhook
// { "channel": "alert", "timestamp": "2026-02-11T12:18:00.968810+00:00", "rtstream_id": "rts-xxx", "rtstream_name": "Meeting", "data": { "event_id": "event-77aae6b981970542", "label": "objection", "triggered": true, "confidence": 0.9, "start": 1770812246.3445818, "end": 1770812277.3488276 } }
```

## [ Install the SDK](#install-the-sdk)

Python

Node.js

```
pip install videodb
```

```
npm install videodb
```

## Python SDK

GitHub, PyPI, and setup guide

## Node.js SDK

npm, TypeScript, and setup guide

## [ Philosophy](#philosophy)

Why perception is the next frontier for AI agents.

## Why AI Agents Are Blind Today

The gap between human perception and agent perception

## Perception Is the Missing Layer

The stack that gives agents eyes and ears

## MP4 Is the Wrong Primitive

Why video files don't work for AI

## What Episodic Memory Means for Agents

Remember experiences, not just facts

[Quickstart](\pages\getting-started\quickstart)

⌘ I