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

- [When to Use This Reference](#when-to-use-this-reference)
- [Quick Example](#quick-example)
- [Core Objects](#core-objects)
    - [Connection](#connection)
    - [Collection](#collection)
    - [Video](#video)
    - [RTStream](#rtstream)
    - [CaptureSession](#capturesession)
    - [Index (SceneIndex)](#index-sceneindex)
    - [SearchResult](#searchresult)
    - [Shot](#shot)
    - [Event](#event)
    - [Alert](#alert)
    - [Editor Module (Programmable Editing)](#editor-module-programmable-editing)
- [Object Hierarchy](#object-hierarchy)
- [Next Steps](#next-steps)

[Core Concepts](\pages\core-concepts\overview)

# Data Model

Copy page

Core objects in VideoDB: Collections, Videos, RTStreams, Indexes, and more. Understanding these objects helps you navigate the SDK and API.

Copy page

## [ When to Use This Reference](#when-to-use-this-reference)

Use this page when you need to:

- Understand what each SDK class represents
- Know which object to use for your use case
- Map between the SDK, API, and documentation

## [ Quick Example](#quick-example)

```
import videodb
from videodb.editor import Timeline, Track, Clip, VideoAsset

conn = videodb.connect() # Connection
coll = conn.get_collection() # Collection
video = coll.upload( url = "..." ) # Video (file-based)
rtstream = coll.connect_rtstream( ... ) # RTStream (live)
index = video.index_scenes( ... ) # Index
results = video.search( "query" ) # SearchResult

# Editor (separate module)
timeline = Timeline(conn) # Timeline
```

## [ Core Objects](#core-objects)

### [ Connection](#connection)

The entry point to VideoDB. Holds your API key and provides access to collections, events, and WebSocket connections.

```
conn = videodb.connect() # Uses VIDEODB_API_KEY env var
conn = videodb.connect( api_key = "your-key" )
```

**Key methods:**

- `get_collection()` - Get default or specific collection
- `create_event()` - Create reusable detection rules
- `connect_websocket()` - Establish real-time connection

### [ Collection](#collection)

A container for organizing media assets. Every video and stream belongs to a collection.

```
coll = conn.get_collection()
coll = conn.get_collection( collection_id = "c-xxx" )
```

**Key methods:**

- `upload(url=...)` - Upload video from URL
- `upload(file_path=...)` - Upload local file
- `connect_rtstream(...)` - Connect live stream
- `search(...)` - Search across all assets in collection
- `list_videos()` - List video assets
- `list_rtstreams()` - List live streams

### [ Video](#video)

A file-based media asset. Represents uploaded videos that can be indexed, searched, and edited.

```
video = coll.upload( url = "https://example.com/video.mp4" )
video = coll.get_video( video_id = "v-xxx" )
```

**Key attributes:**

- `id` - Unique identifier (v-xxx)
- `name` - Display name
- `length` - Duration in seconds
- `stream_url` - Playback URL

**Key methods:**

- `index_scenes(prompt=...)` - Create visual index
- `index_spoken_words()` - Create transcript index
- `search(query, index_id=...)` - Search this video
- `generate_stream(...)` - Get playback URL for time range
- `play()` - Open in browser

### [ RTStream](#rtstream)

A real-time media stream. Represents live video from RTSP feeds, cameras, or desktop capture.

```
rtstream = coll.connect_rtstream(
name = "Lobby Camera" ,
url = "rtsp://user:pass@host:554/stream"
)
```

**Key attributes:**

- `id` - Unique identifier (rts-xxx)
- `name` - Display name
- `status` - connected, stopped, etc.

**Key methods:**

- `index_visuals(prompt=...)` - Create visual index
- `index_audio(prompt=...)` - Create audio index
- `start_transcript()` - Begin transcription
- `search(query, index_id=...)` - Search this stream
- `generate_stream(start, end)` - Get playback URL

### [ CaptureSession](#capturesession)

Desktop capture for AI agents. Stream screen, mic, and system audio from any desktop with real-time AI events.

```
# Backend creates session (holds API key)
cap = conn.create_capture_session(
end_user_id = "user_abc" ,
callback_url = "https://your-backend.com/webhooks" ,
metadata = { "app" : "my-ai-copilot" }
)

# Generate short-lived token for desktop client
token = conn.generate_client_token( expires_in = 600 )
```

**Key attributes:**

- `id` - Unique identifier (cap-xxx)
- `status` - pending, active, completed, stopped
- `end_user_id` - Your user identifier

**Key concepts:**

- **Two-component architecture** - Backend holds API key, desktop client uses tokens
- **Creates RTStreams** - Each active channel (mic, screen, audio) creates an RTStream
- **Real-time events** - Transcripts, visual indexes, and alerts delivered via webhook/WebSocket

**Capture channels:**

- Microphone - User's voice
- Screen/Display - Visual content
- System Audio - Audio from apps
- Camera - Webcam feed

### [ Index (SceneIndex)](#index-sceneindex)

A programmable interpretation layer that produces timestamped scene records. The key abstraction for turning raw media into searchable knowledge.

```
# On Video
index = video.index_scenes(
prompt = "Describe the scene and identify key moments"
)

# On RTStream
index = rtstream.index_visuals(
prompt = "Monitor for safety violations" ,
batch_config = { "type" : "time" , "value" : 5 , "frame_count" : 2 }
)
```

**Key concepts:**

- Indexes are **prompt-driven** - you define what to extract
- Indexes are **additive** - create multiple indexes on the same media
- Indexes are **non-destructive** - add or remove without affecting source
- Indexes support **visual and spoken** modalities

**Key methods:**

- `get_scenes()` - Retrieve indexed scenes
- `create_alert(event_id, ...)` - Attach alert trigger
- `start()` / `stop()` - Control indexing

### [ SearchResult](#searchresult)

The result of a search query. Contains shots (moments) with timestamps and playable evidence.

```
index_id = video.index_scenes(
prompt = "Describe the scene and identify key moments"
)
results = video.search( "important announcement" , index_id = index_id)

for shot in results.shots:
print ( f " { shot.start } s - { shot.end } s: { shot.text } " )
print ( f "Score: { shot.search_score } " )
shot.play() # Verify the result
```

**Key attributes:**

- `shots` - List of matching moments
- `collection_id` - Source collection

### [ Shot](#shot)

A single moment from search results. Contains timestamps, text, and playable stream URL. **Key attributes:**

- `start` - Start timestamp (seconds or Unix time)
- `end` - End timestamp
- `text` - Content/description at this moment
- `search_score` - Relevance score (0-1)
- `stream_url` - Direct playback URL

**Key methods:**

- `generate_stream()` - Get playback URL
- `play()` - Open in browser

### [ Event](#event)

A reusable detection rule defined in plain English. Events describe what to detect; alerts define where and how to deliver.

```
event_id = conn.create_event(
event_prompt = "Detect when someone enters restricted area" ,
label = "intrusion_detected"
)
```

### [ Alert](#alert)

Wires an event to an index and defines delivery. When the event condition is detected, the alert fires.

```
alert_id = index.create_alert(
event_id = event_id,
callback_url = "https://your-backend.com/webhooks/alerts" ,
ws_connection_id = ws.connection_id # Optional for real-time
)
```

**Delivery options:**

- `callback_url` - Webhook for automation
- `ws_connection_id` - WebSocket for real-time

### [ Editor Module (Programmable Editing)](#editor-module-programmable-editing)

The action layer for programmable video editing lives in `videodb.editor` . It uses a 4-layer architecture: **Asset → Clip → Track → Timeline**

```
from videodb.editor import Timeline, Track, Clip, VideoAsset

# 1. Asset - your raw content
video_asset = VideoAsset( id = video.id, start = 0 )

# 2. Clip - how it appears (duration, position, effects)
clip = Clip( asset = video_asset, duration = 10 )

# 3. Track - when it plays (timeline lane)
track = Track()
track.add_clip( 0 , clip) # Start at 0 seconds

# 4. Timeline - the final canvas
timeline = Timeline(conn)
timeline.add_track(track)
stream_url = timeline.generate_stream()
```

**Asset types:**

- `VideoAsset` - Video content
- `AudioAsset` - Music, voiceover, sound effects
- `ImageAsset` - Logos, watermarks, backgrounds
- `TextAsset` - Custom text overlays
- `CaptionAsset` - Auto-generated subtitles

**Key concepts:**

- Clips on the **same track** play sequentially
- Clips on **different tracks** play simultaneously (layered)
- Later tracks render **on top** of earlier tracks

## [ Object Hierarchy](#object-hierarchy)

```
videodb
├── Connection (videodb.connect())
│   ├── Collection
│   │   ├── Video (file-based media)
│   │   │   ├── Index (SceneIndex)
│   │   │   │   └── Alert
│   │   │   ├── Transcript
│   │   │   └── search() → SearchResult → Shot[]
│   │   ├── RTStream (live media)
│   │   │   ├── Index (SceneIndex / AudioIndex)
│   │   │   │   └── Alert
│   │   │   ├── Transcript
│   │   │   └── search() → SearchResult → Shot[]
│   │   └── search() → SearchResult (collection-wide)
│   ├── CaptureSession (desktop capture)
│   │   ├── creates RTStreams (mic, screen, system audio)
│   │   └── generate_client_token() → short-lived token
│   ├── Event (reusable detection rules)
│   └── WebSocket (real-time events)
│
videodb.editor (programmable editing)
├── Timeline (final canvas, resolution, rendering)
├── Track (timeline lanes, sequencing)
├── Clip (duration, position, effects)
└── Assets
├── VideoAsset
├── AudioAsset
├── ImageAsset
├── TextAsset
└── CaptionAsset
```

## [ Next Steps](#next-steps)

## Indexes Deep Dive

Learn how to create and use indexes effectively

## Search &amp; Retrieval

Master search patterns and result handling

[Core Concepts Overview](\pages\core-concepts\overview) [Indexes &amp; Search](\pages\core-concepts\indexes-and-search)

⌘ I