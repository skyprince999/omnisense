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
    - [RTSP Ingest](\pages\ingest\live-streams\rtsp-ingest)
    - [Real-time APIs](\pages\ingest\live-streams\realtime-apis)
    - [Stream Lifecycle](\pages\ingest\live-streams\stream-lifecycle)
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

- [Quick Example](#quick-example)
- [Visual Indexing](#visual-indexing)
    - [batch\_config Options](#batch_config-options)
    - [Managing Indexes](#managing-indexes)
- [Audio Indexing](#audio-indexing)
    - [Audio batch\_config](#audio-batch_config)
- [Transcription](#transcription)
- [Search](#search)
    - [Search Results](#search-results)
- [Stream Generation](#stream-generation)
    - [player\_url vs stream\_url](#player_url-vs-stream_url)
    - [player\_config](#player_config)
    - [Embed Code](#embed-code)
- [Events and Alerts](#events-and-alerts)
    - [Create Event](#create-event)
    - [Create Alert](#create-alert)
    - [Alert Delivery](#alert-delivery)
    - [Manage Alerts](#manage-alerts)
- [WebSocket Events](#websocket-events)
    - [Event Channels](#event-channels)
- [Next Steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Live Streams](\pages\ingest\live-streams\rtsp-ingest)

# Real-time APIs

Copy page

RTStreams offer real-time indexing, transcription, search, and event-based alerts. Convert live video into structured, searchable data.

Copy page

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()
rtstream = coll.get_rtstream( "rts-xxx" )

# Index visuals with a prompt
scene_index = rtstream.index_visuals(
prompt = "Describe activity and detect unusual behavior" ,
batch_config = { "type" : "time" , "value" : 5 , "frame_count" : 2 }
)

# Create a reusable event
event_id = conn.create_event(
event_prompt = "Detect when someone enters restricted area" ,
label = "intrusion_detected"
)

# Set up alert
alert_id = scene_index.create_alert(
event_id = event_id,
callback_url = "https://your-backend.com/webhooks/alerts"
)
```

```
import { connect } from 'videodb' ;

const conn = await connect ();
const coll = await conn . getCollection ();
const rtstream = await coll . getRtstream ( "rts-xxx" );

// Index visuals with a prompt
const sceneIndex = await rtstream . indexVisuals ({
prompt: "Describe activity and detect unusual behavior" ,
batchConfig: { type: "time" , value: 5 , frameCount: 2 }
});

// Create a reusable event
const eventId = await conn . createEvent (
"Detect when someone enters restricted area" ,
"intrusion_detected"
);

// Set up alert
const alertId = await sceneIndex . createAlert (
eventId ,
"https://your-backend.com/webhooks/alerts"
);
```

## [ Visual Indexing](#visual-indexing)

Convert video frames into structured descriptions using prompts.

Python

Node.js

```
scene_index = rtstream.index_visuals(
prompt = "Describe the scene and highlight congestion" ,
batch_config = { "type" : "time" , "value" : 5 , "frame_count" : 2 },
name = "traffic_monitor" ,
ws_connection_id = ws.connection_id # optional, for real-time events
)
```

```
const sceneIndex = await rtstream . indexVisuals ({
prompt: "Describe the scene and highlight congestion" ,
batchConfig: { type: "time" , value: 5 , frameCount: 2 },
name: "traffic_monitor" ,
wsConnectionId: ws . connectionId // optional
});
```

### [ batch\_config Options](#batch_config-options)

| Field         | Type   | Description                  |
|---------------|--------|------------------------------|
| `type`        | str    | Only `"time"` is supported   |
| `value`       | int    | Window size in seconds       |
| `frame_count` | int    | Frames to extract per window |

**Examples:**

```
# Every 5 seconds, extract 2 frames
{ "type" : "time" , "value" : 5 , "frame_count" : 2 }

# Every 10 seconds, extract 5 frames
{ "type" : "time" , "value" : 10 , "frame_count" : 5 }
```

### [ Managing Indexes](#managing-indexes)

Python

Node.js

```
# List all indexes
indexes = rtstream.list_scene_indexes()

# Get specific index
scene_index = rtstream.get_scene_index(index_id)

# Poll scenes
scenes = scene_index.get_scenes(
start = 0 , end = None , page = 1 , page_size = 100
)
```

```
// List all indexes
const indexes = await rtstream . listSceneIndexes ();

// Get specific index
const sceneIndex = await rtstream . getSceneIndex ( indexId );

// Poll scenes
const scenes = await sceneIndex . getScenes ({
start: 0 , end: null , page: 1 , pageSize: 100
});
```

## [ Audio Indexing](#audio-indexing)

Extract insights from audio tracks:

Python

Node.js

```
audio_index = rtstream.index_audio(
prompt = "Identify key speakers and main topics" ,
batch_config = { "type" : "word" , "value" : 50 }
)
```

```
const audioIndex = await rtstream . indexAudio ({
prompt: "Identify key speakers and main topics" ,
batchConfig: { type: "word" , value: 50 }
});
```

### [ Audio batch\_config](#audio-batch_config)

| Type         | Value   | Description               |
|--------------|---------|---------------------------|
| `"word"`     | count   | Segment every N words     |
| `"sentence"` | count   | Segment every N sentences |
| `"time"`     | seconds | Segment every N seconds   |

## [ Transcription](#transcription)

Real-time speech-to-text:

Python

Node.js

```
# Start transcription
rtstream.start_transcript( ws_connection_id = ws.connection_id)

# Stop transcription
rtstream.stop_transcript( mode = "graceful" )

# Poll transcripts
transcript = rtstream.get_transcript(
start = 0 , page = 1 , page_size = 100
)
```

```
// Start transcription
await rtstream . startTranscript ( ws . connectionId );

// Stop transcription
await rtstream . stopTranscript ( "graceful" );

// Poll transcripts
const transcript = await rtstream . getTranscript ({
start: 0 , page: 1 , pageSize: 100
});
```

## [ Search](#search)

Query indexed content with natural language:

Python

Node.js

```
results = rtstream.search(
query = "white car moving fast" ,
score_threshold = 0.5
)

for shot in results.shots:
print ( f "Match at { shot.start } : { shot.text } " )
shot.play() # Opens in browser
```

```
const results = await rtstream . search ({
query: "white car moving fast" ,
scoreThreshold: 0.5
});

for ( const shot of results . shots ) {
console . log ( `Match at ${ shot . start } : ${ shot . text } ` );
await shot . play ();
}
```

### [ Search Results](#search-results)

Each shot contains:

| Attribute      | Description           |
|----------------|-----------------------|
| `start`        | Start timestamp       |
| `end`          | End timestamp         |
| `text`         | Content description   |
| `search_score` | Relevance score (0-1) |
| `stream_url`   | Playback URL          |

## [ Stream Generation](#stream-generation)

Use `generate_stream()` to create a playable stream for a time range. You can optionally pass `player_config` to attach metadata to a shareable player URL.

Python

Node.js

```
# Generate stream with player metadata
player_url = rtstream.generate_stream(
start = 1711000000 ,
end = 1711003600 ,
player_config = {
"title" : "Live Feed Recording" ,
"description" : "Camera 1 - Front entrance" ,
"slug" : "cam1-front"
}
)

# generate_stream() returns the player_url
# Both URLs are also stored on the instance
print (rtstream.player_url) # Shareable player URL (same as return value)
print (rtstream.stream_url) # Raw HLS stream URL (.m3u8)
```

```
// Generate stream with player metadata
const playerUrl = await rtstream . generateStream ({
start: 1711000000 ,
end: 1711003600 ,
playerConfig: {
title: "Live Feed Recording" ,
description: "Camera 1 - Front entrance" ,
slug: "cam1-front"
}
});

// generateStream() returns the playerUrl
// Both URLs are also stored on the instance
console . log ( rtstream . playerUrl ); // Shareable player URL (same as return value)
console . log ( rtstream . streamUrl ); // Raw HLS stream URL (.m3u8)
```

### [ player\_url vs stream\_url](#player_url-vs-stream_url)

| URL          | Format                                    | Use case                                             |
|--------------|-------------------------------------------|------------------------------------------------------|
| `player_url` | `https://console.videodb.io/player?v=...` | Shareable link with built-in player UI               |
| `stream_url` | `https://stream.videodb.io/.../.m3u8`     | Raw HLS stream for custom players (HLS.js, Video.js) |

`generate_stream()` **returns** **`player_url`** and stores both URLs on the instance. Use `player_url` for sharing and embedding, `stream_url` for custom player integrations.

### [ player\_config](#player_config)

| Key           | Type   | Description                           |
|---------------|--------|---------------------------------------|
| `title`       | str    | Title displayed in the player         |
| `description` | str    | Description for the player page       |
| `slug`        | str    | URL-friendly slug for the player link |

`player_config` is optional. When provided, the player URL includes the metadata for sharing.

### [ Embed Code](#embed-code)

After generating a stream, you can produce embeddable HTML:

Python

Node.js

```
# Generate embed code (requires generate_stream() first)
rtstream.generate_stream( start = start_ts, end = end_ts)
embed_html = rtstream.get_embed_code()
```

```
// Generate embed code (requires generateStream() first)
await rtstream . generateStream ({ start: startTs , end: endTs });
const embedHtml = rtstream . getEmbedCode ();
```

RTStream does **not** support `auto_generate` because `generate_stream()` requires explicit `start` and `end` parameters.

## [ Events and Alerts](#events-and-alerts)

Events are reusable detection rules. Alerts wire events to indexes for notifications.

### [ Create Event](#create-event)

Python

Node.js

```
event_id = conn.create_event(
event_prompt = "Detect pedestrians crossing the zebra" ,
label = "pedestrian_detected"
)
```

```
const eventId = await conn . createEvent (
"Detect pedestrians crossing the zebra" ,
"pedestrian_detected"
);
```

### [ Create Alert](#create-alert)

Python

Node.js

```
alert_id = scene_index.create_alert(
event_id = event_id,
callback_url = "https://your-backend.com/webhooks/alerts" ,
ws_connection_id = ws.connection_id # optional
)
```

```
const alertId = await sceneIndex . createAlert (
eventId ,
"https://your-backend.com/webhooks/alerts" ,
ws . connectionId // optional
);
```

### [ Alert Delivery](#alert-delivery)

| Method    | Latency   | Use Case              |
|-----------|-----------|-----------------------|
| Webhook   | Under 1s  | Server-to-server POST |
| WebSocket | Real-time | Frontend dashboards   |

### [ Manage Alerts](#manage-alerts)

Python

Node.js

```
# List alerts
alerts = scene_index.list_alerts()

# Enable/disable
scene_index.enable_alert(alert_id)
scene_index.disable_alert(alert_id)
```

```
// List alerts
const alerts = await sceneIndex . listAlerts ();

// Enable/disable
await sceneIndex . enableAlert ( alertId );
await sceneIndex . disableAlert ( alertId );
```

## [ WebSocket Events](#websocket-events)

Receive real-time events by passing `ws_connection_id` :

Python

Node.js

```
ws = conn.connect_websocket()
await ws.connect()

# Pass ws_connection_id to methods
rtstream.start_transcript( ws_connection_id = ws.connection_id)

# Receive events
async for ev in ws.stream():
channel = ev.get( "channel" )

if channel == "transcript" :
print ( f "TRANSCRIPT: { ev[ 'data' ][ 'text' ] } " )
elif channel == "scene_index" :
print ( f "SCENE: { ev[ 'data' ][ 'text' ] } " )
elif channel == "alert" :
print ( f "ALERT: { ev[ 'data' ] } " )
```

```
const ws = conn . connectWebsocket ();
await ws . connect ();

// Pass wsConnectionId to methods
await rtstream . startTranscript ( ws . connectionId );

// Receive events
for await ( const ev of ws . stream ()) {
const channel = ev . channel ;

if ( channel === "transcript" ) {
console . log ( `TRANSCRIPT: ${ ev . data . text } ` );
} else if ( channel === "scene_index" ) {
console . log ( `SCENE: ${ ev . data . text } ` );
} else if ( channel === "alert" ) {
console . log ( `ALERT: ${ ev . data } ` );
}
}
```

### [ Event Channels](#event-channels)

| Channel       | Source               | Content                  |
|---------------|----------------------|--------------------------|
| `transcript`  | `start_transcript()` | Real-time speech-to-text |
| `scene_index` | `index_visuals()`    | Visual analysis          |
| `audio_index` | `index_audio()`      | Audio analysis           |
| `alert`       | `create_alert()`     | Alert notifications      |

## [ Next Steps](#next-steps)

## Stream Lifecycle

Start, stop, and reconnect patterns

## RTSP Ingest

Connect RTSP sources

[RTSP Ingest](\pages\ingest\live-streams\rtsp-ingest) [Stream Lifecycle](\pages\ingest\live-streams\stream-lifecycle)

⌘ I