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
    - [Capture SDK Overview](\pages\ingest\capture-sdks\overview)
    - [Real-time Context](\pages\ingest\capture-sdks\realtime-context)
    - [Storage &amp; Search](\pages\ingest\capture-sdks\storage-and-search)
    - [Privacy Controls](\pages\ingest\capture-sdks\privacy-controls)
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
- [Event Types](#event-types)
    - [Transcript Events](#transcript-events)
    - [Visual Index Events](#visual-index-events)
    - [Audio Index Events](#audio-index-events)
    - [Alert Events](#alert-events)
- [WebSocket Channels](#websocket-channels)
    - [Connecting](#connecting)
- [Webhooks](#webhooks)
    - [Webhook Envelope](#webhook-envelope)
    - [Session Lifecycle Events](#session-lifecycle-events)
    - [Key Webhook: capture\_session.active](#key-webhook-capture_session-active)
- [Delivery Semantics](#delivery-semantics)
- [Next Steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Capture SDKs](\pages\ingest\capture-sdks\overview)

# Real-time Context

Copy page

Events you receive from capture - transcripts, visual indexes, audio indexes, and alerts

Copy page

Capture sessions emit structured events in real-time. Use webhooks for durable delivery, WebSockets for live UI.

Desktop capture currently supports **macOS** and **Windows** .

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
ws = conn.connect_websocket()
await ws.connect()

# Listen for events
async for ev in ws.stream():
channel = ev.get( "channel" )

if channel == "transcript" :
print ( f "TRANSCRIPT: { ev[ 'data' ][ 'text' ] } " )
elif channel == "scene_index" :
print ( f "SCENE: { ev[ 'data' ][ 'text' ] } " )
elif channel == "audio_index" :
print ( f "AUDIO: { ev[ 'data' ][ 'text' ] } " )
```

```
import { connect } from 'videodb' ;

const conn = connect ();
const ws = conn . connectWebsocket ();
await ws . connect ();

// Listen for events
for await ( const ev of ws . stream ()) {
const channel = ev . channel ;

if ( channel === "transcript" ) {
console . log ( `TRANSCRIPT: ${ ev . data . text } ` );
} else if ( channel === "scene_index" ) {
console . log ( `SCENE: ${ ev . data . text } ` );
} else if ( channel === "audio_index" ) {
console . log ( `AUDIO: ${ ev . data . text } ` );
}
}
```

## [ Event Types](#event-types)

### [ Transcript Events](#transcript-events)

Real-time speech-to-text from audio channels:

```
{
"channel" : "transcript" ,
"rtstream_id" : "rts-xxx" ,
"rtstream_name" : "mic:default" ,
"data" : {
"text" : "Let's schedule the meeting for Thursday" ,
"is_final" : true ,
"start" : 1710000001234 ,
"end" : 1710000002345
}
}
```

| Field       | Description                           |
|-------------|---------------------------------------|
| `text`      | Transcribed speech                    |
| `is_final`  | `true` for final, `false` for interim |
| `start/end` | Timestamps (ms)                       |

### [ Visual Index Events](#visual-index-events)

Scene descriptions from screen capture:

```
{
"channel" : "visual_index" ,
"rtstream_id" : "rts-xxx" ,
"rtstream_name" : "display:1" ,
"data" : {
"text" : "User is viewing a Slack conversation with 3 unread messages" ,
"start" : 1710000012340 ,
"end" : 1710000018900
}
}
```

### [ Audio Index Events](#audio-index-events)

Semantic understanding of audio:

```
{
"channel" : "audio_index" ,
"rtstream_id" : "rts-xxx" ,
"rtstream_name" : "mic:default" ,
"data" : {
"text" : "Discussion about scheduling a team meeting" ,
"start" : 1710000021500 ,
"end" : 1710000029200
}
}
```

### [ Alert Events](#alert-events)

Custom detection rules firing:

```
{
"channel" : "alert" ,
"rtstream_id" : "rts-xxx" ,
"data" : {
"label" : "sensitive_content" ,
"triggered" : true ,
"confidence" : 0.92 ,
"start" : 1710000045100 ,
"end" : 1710000047800
}
}
```

## [ WebSocket Channels](#websocket-channels)

| Channel           | Source               | Content             |
|-------------------|----------------------|---------------------|
| `capture_session` | Session lifecycle    | Status changes      |
| `transcript`      | `start_transcript()` | Speech-to-text      |
| `scene_index`     | `index_visuals()`    | Visual analysis     |
| `audio_index`     | `index_audio()`      | Audio analysis      |
| `alert`           | `create_alert()`     | Alert notifications |

### [ Connecting](#connecting)

Python

Node.js

```
conn = videodb.connect()
ws = conn.connect_websocket()
await ws.connect()

# Pass ws.connection_id when starting AI operations
rtstream.start_transcript( ws_connection_id = ws.connection_id)
rtstream.index_visuals( prompt = "..." , ws_connection_id = ws.connection_id)
rtstream.index_audio( prompt = "..." , ws_connection_id = ws.connection_id)
```

```
const conn = connect ();
const ws = conn . connectWebsocket ();
await ws . connect ();

// Pass wsConnectionId when starting AI operations
await rtstream . startTranscript ( ws . connectionId );
await rtstream . indexVisuals ({ prompt: "..." , wsConnectionId: ws . connectionId });
await rtstream . indexAudio ({ prompt: "..." , wsConnectionId: ws . connectionId });
```

## [ Webhooks](#webhooks)

Durable, at-least-once delivery for session lifecycle events.

### [ Webhook Envelope](#webhook-envelope)

```
{
"version" : "2" ,
"event" : "capture_session.active" ,
"timestamp" : "2026-01-20T12:34:56Z" ,
"capture_session_id" : "cap-xxx" ,
"end_user_id" : "user_abc" ,
"status" : "active" ,
"data" : {}
}
```

### [ Session Lifecycle Events](#session-lifecycle-events)

| Event                      | Status     | Key Data            |
|----------------------------|------------|---------------------|
| `capture_session.created`  | `created`  | -                   |
| `capture_session.starting` | `starting` | -                   |
| `capture_session.active`   | `active`   | `rtstreams[]`       |
| `capture_session.stopping` | `stopping` | -                   |
| `capture_session.stopped`  | `stopped`  | -                   |
| `capture_session.exported` | `exported` | `exported_video_id` |
| `capture_session.failed`   | `failed`   | `error` object      |

### [ Key Webhook: capture\_session.active](#key-webhook-capture_session-active)

This is where you start AI pipelines:

```
{
"event" : "capture_session.active" ,
"capture_session_id" : "cap-xxx" ,
"status" : "active" ,
"data" : {
"rtstreams" : [
{ "rtstream_id" : "rts-1" , "name" : "mic:default" , "media_types" : [ "audio" ] },
{ "rtstream_id" : "rts-2" , "name" : "system_audio:default" , "media_types" : [ "audio" ] },
{ "rtstream_id" : "rts-3" , "name" : "display:1" , "media_types" : [ "video" ] }
]
}
}
```

Python

Node.js

```
def on_active_webhook ( payload ):
cap = conn.get_capture_session(payload[ "capture_session_id" ])

for rts_info in payload[ "data" ][ "rtstreams" ]:
rts_id = rts_info[ "rtstream_id" ]
rts_name = rts_info[ "name" ]

if "audio" in rts_info[ "media_types" ]:
rtstream = conn.get_rtstream(rts_id)
rtstream.start_transcript()
rtstream.index_audio( prompt = "Extract key decisions" )

if "video" in rts_info[ "media_types" ]:
rtstream = conn.get_rtstream(rts_id)
rtstream.index_visuals( prompt = "Describe what user is doing" )
```

```
async function onActiveWebhook ( payload ) {
const cap = await conn . getCaptureSession ( payload . capture_session_id );

for ( const rtsInfo of payload . data . rtstreams ) {
const rtsId = rtsInfo . rtstream_id ;
const rtsName = rtsInfo . name ;

if ( rtsInfo . media_types . includes ( "audio" )) {
const rtstream = await conn . getRtstream ( rtsId );
await rtstream . startTranscript ();
await rtstream . indexAudio ({ prompt: "Extract key decisions" });
}

if ( rtsInfo . media_types . includes ( "video" )) {
const rtstream = await conn . getRtstream ( rtsId );
await rtstream . indexVisuals ({ prompt: "Describe what user is doing" });
}
}
}
```

## [ Delivery Semantics](#delivery-semantics)

| Method    | Guarantee     | Handle                  |
|-----------|---------------|-------------------------|
| WebSocket | Best-effort   | Reconnect on disconnect |
| Webhook   | At-least-once | Deduplicate by event ID |

Webhooks may deliver duplicates. Respond 2xx quickly, process asynchronously, implement idempotency.

## [ Next Steps](#next-steps)

## Capture Overview

Architecture and quickstart

## Storage &amp; Search

Export and persistence patterns

[Capture SDK Overview](\pages\ingest\capture-sdks\overview) [Storage &amp; Search](\pages\ingest\capture-sdks\storage-and-search)

⌘ I