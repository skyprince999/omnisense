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

- [The Problem](#the-problem)
- [The Platform Loop](#the-platform-loop)
- [Quick Example](#quick-example)
- [See: Three Input Types](#see-three-input-types)
- [Understand: Indexes Are Everything](#understand-indexes-are-everything)
    - [Spoken Index](#spoken-index)
    - [Visual Index](#visual-index)
    - [Multiple Indexes](#multiple-indexes)
- [Search Returns Evidence](#search-returns-evidence)
- [Act: Events, Alerts, Editing](#act-events-alerts-editing)
    - [Trigger on conditions](#trigger-on-conditions)
    - [Compose with code](#compose-with-code)
- [Objects at a Glance](#objects-at-a-glance)
- [Next Steps](#next-steps)

[Start Here](\index)

# Core Concepts in 5 Minutes

Copy page

The entire VideoDB mental model in one scroll - perception, memory, and action for AI agents.

Copy page

## [ The Problem](#the-problem)

AI agents can reason about text brilliantly. But show them a 30-minute meeting recording and ask "what did the client say about pricing?" - they fail. Video files are opaque blobs. Your agent can't query them, can't search them, can't get timestamped answers from them.

## [ The Platform Loop](#the-platform-loop)

Every VideoDB workflow follows the same pattern:

```
See → Understand → Act
```

| Stage          | What Happens                                   | Returns                                     |
|----------------|------------------------------------------------|---------------------------------------------|
| **See**        | Ingest from files, streams, or desktop capture | `Video` , `RTStream` , or `CaptureSession`  |
| **Understand** | Create indexes. Search with natural language.  | Timestamped moments with playable evidence  |
| **Act**        | Trigger alerts. Compose edits. Export streams. | Webhooks, playable URLs, downloadable files |

## [ Quick Example](#quick-example)

```
import videodb

conn = videodb.connect()

# SEE: Ingest
coll = conn.get_collection()
video = coll.upload( url = "https://example.com/meeting.mp4" )

# UNDERSTAND: Index and search
video.index_spoken_words()
results = video.search( "pricing discussion" )

# ACT: Use the results
for shot in results.shots:
print ( f " { shot.start } s - { shot.end } s: { shot.text } " )
shot.play() # Playable proof
```

## [ See: Three Input Types](#see-three-input-types)

| Source              | Method                             | Returns                       |
|---------------------|------------------------------------|-------------------------------|
| **Files**           | `coll.upload(url="...")`           | `Video`                       |
| **Live streams**    | `conn.connect_rtstream(url="...")` | `RTStream`                    |
| **Desktop capture** | `conn.create_capture_session(...)` | `CaptureSession` → `RTStream` |

```
# Files
coll = conn.get_collection()
video = coll.upload( url = "https://youtube.com/watch?v=..." )

# Live RTSP
rtstream = conn.connect_rtstream( url = "rtsp://camera.local/stream" )

# Desktop capture
cap = conn.create_capture_session( end_user_id = "user_123" )
```

Same APIs work downstream. Index a `Video` or an `RTStream` the same way.

## [ Understand: Indexes Are Everything](#understand-indexes-are-everything)

Indexes are what transform opaque media into searchable knowledge. You create them with prompts.

### [ Spoken Index](#spoken-index)

Transcribes audio and makes it searchable:

```
video.index_spoken_words()
# or for live:
rtstream.start_transcript()
```

### [ Visual Index](#visual-index)

Understands what's happening on screen:

```
video.index_visuals( prompt = "Describe key activities and events" )
# or for live:
rtstream.index_visuals( prompt = "Describe what user is doing" )
```

### [ Multiple Indexes](#multiple-indexes)

Create different perspectives on the same media:

```
# Same video, different questions
safety_index = video.index_visuals( prompt = "Identify safety violations" )
summary_index = video.index_visuals( prompt = "Summarize each segment" )
```

Indexes are additive. Add new ones without reprocessing. Remove old ones without affecting others.

## [ Search Returns Evidence](#search-returns-evidence)

Search returns timestamps and playable links - not just "found" but verifiable.

```
results = video.search( "product demo" )

for shot in results.shots:
print ( f " { shot.start } s - { shot.end } s" ) # Timestamps
print ( f "Content: { shot.text } " ) # What was found
print ( f "Score: { shot.search_score } " ) # Relevance
shot.play() # Play it to verify
```

Every result maps to a playable moment. Your agent can cite its sources.

## [ Act: Events, Alerts, Editing](#act-events-alerts-editing)

### [ Trigger on conditions](#trigger-on-conditions)

```
# Create a reusable event
event_id = conn.create_event(
event_prompt = "Detect when someone mentions 'budget'" ,
label = "budget_mention"
)

# Wire it to an index
index.create_alert( event_id = event_id, callback_url = "https://..." )
```

### [ Compose with code](#compose-with-code)

```
from videodb.editor import Timeline, Track, Clip, VideoAsset

timeline = Timeline(conn)
track = Track()
track.add_clip( 0 , Clip( asset = VideoAsset( id = video.id), duration = 30 ))
timeline.add_track(track)

stream_url = timeline.generate_stream()
```

## [ Objects at a Glance](#objects-at-a-glance)

| Object         | What It Represents              |
|----------------|---------------------------------|
| `Connection`   | Your authenticated session      |
| `Collection`   | Container for organizing media  |
| `Video`        | Uploaded video                  |
| `RTStream`     | Live stream (RTSP or capture)   |
| `Index`        | Searchable interpretation layer |
| `SearchResult` | Query results with shots        |
| `Shot`         | Single timestamped match        |
| `Event`        | Reusable detection rule         |
| `Alert`        | Event + delivery config         |
| `Timeline`     | Programmatic edit composition   |

## [ Next Steps](#next-steps)

## Quickstart

Try it hands-on

## Core Concepts (Full)

Deep dive with examples

## Data Model

All objects and relationships

## Indexes &amp; Search

How indexing and retrieval work

[AI Agent Skills](\pages\getting-started\agent-skills) [Core Concepts Overview](\pages\core-concepts\overview)

⌘ I