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

- [The Platform Loop](#the-platform-loop)
- [See (Ingest)](#see-ingest)
- [Process](#process)
- [Understand (Indexes)](#understand-indexes)
- [Remember](#remember)
- [Retrieve (Search)](#retrieve-search)
- [Act](#act)
    - [Event Detection](#event-detection)
    - [Programmable Editing](#programmable-editing)
- [Architecture Patterns](#architecture-patterns)
- [Next Steps](#next-steps)

[Core Concepts](\pages\core-concepts\overview)

# Core Concepts Overview

Copy page

VideoDB is the perception, memory, and action layer for AI agents operating on video and audio. Every workflow follows the same loop, whether you're processing files, live streams, or desktop capture.

Copy page

## [ The Platform Loop](#the-platform-loop)

```
See (Ingest) → Process → Understand (Indexes) → Remember → Retrieve (Search) → Act
```

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()

# SEE: Ingest from any source
video = coll.upload( url = "https://example.com/video.mp4" )

# UNDERSTAND: Create an index
index_id = video.index_visuals( prompt = "Extract key moments" )

# RETRIEVE: Search with natural language
results = video.search( "important announcement" , index_id = index_id)

# ACT: Generate outputs, trigger actions
for shot in results.shots:
print ( f " { shot.start } s - { shot.end } s: { shot.text } " )
shot.play() # Playable evidence
```

## [ See (Ingest)](#see-ingest)

Get video and audio from anywhere into VideoDB.

| Source          | Method                                    |
|-----------------|-------------------------------------------|
| File URL        | `coll.upload(url="https://...")`          |
| Local file      | `coll.upload(file_path="./video.mp4")`    |
| RTSP stream     | `coll.connect_rtstream(url="rtsp://...")` |
| Desktop capture | Capture SDK (screen, mic, camera)         |

```
# File-based
video = coll.upload( url = "https://example.com/meeting.mp4" )

# Live stream
rtstream = coll.connect_rtstream(
name = "Security Camera" ,
url = "rtsp://user:pass@host:554/stream"
)
```

## [ Process](#process)

Built-in primitives convert raw media into processable units. This happens automatically when you create indexes.

- **Scene segmentation** - Time-based, shot-based, or prompt-guided
- **Frame sampling** - Control which frames to analyze
- **Audio chunking** - Word, sentence, or time-based segments

```
# Time-based: every 10 seconds
video.index_scenes(
extraction_type = "time_based" ,
extraction_config = { "time" : 10 }
)

# For RTStream: batch config
rtstream.index_visuals(
batch_config = { "type" : "time" , "value" : 5 , "frame_count" : 2 }
)
```

This is where cost control happens - sampling policies trade compute for recall.

## [ Understand (Indexes)](#understand-indexes)

Indexes are programmable interpretation layers. You define what to extract with prompts.

- **Prompt-driven** - Natural language instructions
- **Model-orchestrated** - LLMs and VLMs do the work
- **Additive** - Multiple indexes on same media
- **Multimodal** - Visual and spoken

```
# Visual understanding
visual_index = video.index_scenes(
prompt = "Identify key moments and describe activities"
)

# Spoken understanding
transcript = video.index_spoken_words()

# Multiple indexes = multiple perspectives
safety_index = video.index_scenes( prompt = "Identify safety issues" )
summary_index = video.index_scenes( prompt = "Summarize each segment" )
```

## [ Remember](#remember)

Indexes are stored as episodic memory. This is automatic by default. **What gets stored:**

- Transcripts and embeddings
- Scene descriptions and tags
- Structured metadata
- Retrieval structures

**Ephemeral mode** - For live sessions, you can choose not to persist:

```
rtstream.index_visuals(
prompt = "..." ,
ephemeral = True # Process but don't persist
)
```

## [ Retrieve (Search)](#retrieve-search)

Search across indexed content with natural language. Results include playable evidence.

```
# Single video
results = video.search( "product demo" )

# Single stream
results = rtstream.search( "intrusion" )

# Collection-wide
results = coll.search( "quarterly results" , index_type = "scene" )
```

**Results include:**

- **Timestamps** - Exact start/end times
- **Text** - What was detected
- **Score** - Relevance ranking
- **Stream URL** - Playable link

```
for shot in results.shots:
print ( f " { shot.start } s: { shot.text } (score: { shot.search_score } )" )
shot.play() # Verify the result
```

## [ Act](#act)

Go from understanding to automation and outputs.

### [ Event Detection](#event-detection)

React to conditions in real-time:

```
event_id = conn.create_event(
event_prompt = "Detect intruder" ,
label = "security_alert"
)

index.create_alert(
event_id = event_id,
callback_url = "https://your-backend.com/alerts"
)
```

### [ Programmable Editing](#programmable-editing)

Compose outputs using the 4-layer editor architecture:

```
from videodb.editor import Timeline, Track, Clip, VideoAsset

video_asset = VideoAsset( id = video.id, start = 10 )
clip = Clip( asset = video_asset, duration = 20 )

track = Track()
track.add_clip( 0 , clip)

timeline = Timeline(conn)
timeline.add_track(track)
output = timeline.generate_stream()
```

## [ Architecture Patterns](#architecture-patterns)

The loop applies to different use cases:

| Use Case         | See                | Understand                | Act               |
|------------------|--------------------|---------------------------|-------------------|
| Video Search     | Upload files       | Index with domain prompts | Search + retrieve |
| Monitoring       | Connect RTSP       | Real-time indexing        | Alerts + webhooks |
| Desktop Agent    | Capture SDK        | Index screen/mic          | Context for LLM   |
| Media Automation | Upload + transcode | Index for editing         | Timeline + export |

## [ Next Steps](#next-steps)

## Data Model

Collections, Videos, RTStreams, and other core objects

## Indexes

Turn media into searchable knowledge

## Search &amp; Retrieval

How search returns playable evidence

## Events &amp; Alerts

Real-time detection and automation

[Core Concepts in 5 Minutes](\pages\getting-started\core-concepts-in-5-min) [Data Model](\pages\core-concepts\data-model)

⌘ I