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
- [Storage Control](#storage-control)
    - [Per-Channel Storage](#per-channel-storage)
- [What Gets Exported](#what-gets-exported)
    - [Muxed Video](#muxed-video)
    - [Raw Channel Assets](#raw-channel-assets)
- [Accessing Exports](#accessing-exports)
    - [Via Webhook](#via-webhook)
    - [Via RTStream](#via-rtstream)
    - [Using cap.export()](#using-cap-export)
    - [Multi-Screen Export](#multi-screen-export)
    - [Checking Export Status](#checking-export-status)
- [Editing with Raw Assets](#editing-with-raw-assets)
    - [Display Video + Mic Audio Only](#display-video-%2B-mic-audio-only)
- [Semantic Search](#semantic-search)
- [Which Asset to Use?](#which-asset-to-use)
- [Next Steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Capture SDKs](\pages\ingest\capture-sdks\overview)

# Storage &amp; Search

Copy page

Optional persistence, export workflows, and semantic search for captured content

Copy page

Capture sessions can optionally persist media for later search and playback. Control storage per-channel and access exported assets.

Desktop capture currently supports **macOS** and **Windows** .

## [ Quick Example](#quick-example)

Python

Node.js

```
# After capture_session.exported webhook
cap = conn.get_capture_session( "cap-xxx" )

# Get the muxed video
video_id = cap.exported_video_id
video = coll.get_video(video_id)

# Search the captured content
video.index_spoken_words()
results = video.search( "budget discussion" )
for shot in results.shots:
print ( f " { shot.start } s: { shot.text } " )
shot.play()
```

```
// After capture_session.exported webhook
const cap = await conn . getCaptureSession ( "cap-xxx" );

// Get the muxed video
const videoId = cap . exportedVideoId ;
const video = await coll . getVideo ( videoId );

// Search the captured content
await video . indexSpokenWords ();
const results = await video . search ( "budget discussion" );
for ( const shot of results . shots ) {
console . log ( ` ${ shot . start } s: ${ shot . text } ` );
await shot . play ();
}
```

## [ Storage Control](#storage-control)

### [ Per-Channel Storage](#per-channel-storage)

Enable/disable storage for each channel:

Python

Node.js

```
# In desktop client
await client.start_session(
capture_session_id = cap_id,
channels = [
{ "name" : "mic:default" , "store" : True }, # Will persist
{ "name" : "display:1" , "store" : True }, # Will persist
{ "name" : "system_audio:default" , "store" : False } # Ephemeral
]
)
```

```
// In desktop client
await client . startCaptureSession ({
sessionId: capId ,
channels: [
{ channelId: "mic:default" , store: true }, // Will persist
{ channelId: "display:1" , store: true }, // Will persist
{ channelId: "system_audio:default" , store: false } // Ephemeral
]
});
```

| Setting        | Behavior                                              |
|----------------|-------------------------------------------------------|
| `store: true`  | Media persisted, available for search and playback    |
| `store: false` | Ephemeral - real-time processing only, no persistence |

Export only runs if at least one channel has `store: true` .

## [ What Gets Exported](#what-gets-exported)

### [ Muxed Video](#muxed-video)

The default "playable recording" containing:

- **Video:** Primary display (set via `primary_video_channel_id` )
- **Audio:** All recorded audio channels mixed together

**Use for:**

- Playback and sharing
- Downstream indexing and search
- Simple "trim and publish" workflows

### [ Raw Channel Assets](#raw-channel-assets)

Individual assets for each stored channel:

| Channel                | Asset Type   |
|------------------------|--------------|
| `display:1`            | Raw video    |
| `mic:default`          | Raw audio    |
| `system_audio:default` | Raw audio    |

**Use for:**

- Separate audio stems (mic vs system audio)
- Multi-track editing
- Custom muxing strategies
- Picture-in-picture composites

## [ Accessing Exports](#accessing-exports)

### [ Via Webhook](#via-webhook)

The `capture_session.exported` webhook includes the muxed video ID:

```
{
"event" : "capture_session.exported" ,
"capture_session_id" : "cap-xxx" ,
"status" : "exported" ,
"data" : {
"exported_video_id" : "m-xxx"
}
}
```

### [ Via RTStream](#via-rtstream)

Each RTStream has an `exported_asset_id` after export:

Python

Node.js

```
def on_exported ( payload : dict ):
cap = conn.get_capture_session(payload[ "capture_session_id" ])

# Muxed video
video_id = payload[ "data" ][ "exported_video_id" ]

# Raw channel assets
mics = cap.get_rtstream( "mic" )
if mics:
mic_asset_id = mics[ 0 ].exported_asset_id

displays = cap.get_rtstream( "display" )
if displays:
display_asset_id = displays[ 0 ].exported_asset_id
```

```
async function onExported ( payload ) {
const cap = await conn . getCaptureSession ( payload . capture_session_id );

// Muxed video
const videoId = payload . data . exported_video_id ;

// Raw channel assets
const mics = cap . getRtstream ( "mics" );
if ( mics ?. length > 0 ) {
const micAssetId = mics [ 0 ]. exportedAssetId ;
}

const displays = cap . getRtstream ( "displays" );
if ( displays ?. length > 0 ) {
const displayAssetId = displays [ 0 ]. exportedAssetId ;
}
}
```

### [ Using cap.export()](#using-cap-export)

You can trigger or check an export programmatically with `cap.export()` :

Python

```
cap = conn.get_capture_session( "cap-xxx" )

result = cap.export(
video_channel_id = None , # Optional - defaults to primary video channel
ws_connection_id = None , # Optional - for push notification on completion
)
```

| Parameter          | Type            | Description                                                                                                                |
|--------------------|-----------------|----------------------------------------------------------------------------------------------------------------------------|
| `video_channel_id` | `str` or `None` | The video channel to export. Defaults to the primary video channel when omitted.                                           |
| `ws_connection_id` | `str` or `None` | A WebSocket connection ID. When provided, VideoDB sends a push notification over that connection when the export finishes. |

The returned dict contains:

| Field              | Description                                            |
|--------------------|--------------------------------------------------------|
| `session_id`       | The capture session ID                                 |
| `video_channel_id` | The video channel being exported                       |
| `export_status`    | Current status ( `exporting` , `exported` , `failed` ) |
| `video_id`         | Available once export completes                        |
| `stream_url`       | Playback stream URL (available once exported)          |
| `player_url`       | Embeddable player URL (available once exported)        |

#### [ Multi-Screen Export](#multi-screen-export)

When capturing multiple displays, each display can be exported individually by passing its `video_channel_id` . Use `cap.displays` to discover available video channels:

Python

```
cap = conn.get_capture_session( "cap-xxx" )

for d in cap.displays:
print ( f " { d.channel_id } primary= { d.is_primary } " )

# Export a specific (non-primary) display
result = cap.export( video_channel_id = "display:2" )
print (result)
# {
#   "session_id": "cap-xxx",
#   "video_channel_id": "display:2",
#   "export_status": "exporting"
# }
```

#### [ Checking Export Status](#checking-export-status)

You can track export completion via webhook or by polling:

Python

```
# Option 1: Webhook - your callback_url receives:
# {
#   "event": "capture_session.exported",
#   "capture_session_id": "cap-xxx",
#   "data": { "exported_video_id": "m-xxx" }
# }

# Option 2: Push notification via WebSocket
result = cap.export( ws_connection_id = "ws-conn-xxx" )

# Option 3: Poll export status
result = cap.export( video_channel_id = "display:1" )
while result[ "export_status" ] == "exporting" :
time.sleep( 5 )
result = cap.export( video_channel_id = "display:1" )

print (result[ "video_id" ]) # "m-xxx"
print (result[ "stream_url" ]) # Playback URL
print (result[ "player_url" ]) # Embeddable player URL
```

## [ Editing with Raw Assets](#editing-with-raw-assets)

Use raw assets when you need control over individual tracks.

### [ Display Video + Mic Audio Only](#display-video-+-mic-audio-only)

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip, VideoAsset, AudioAsset

cap = conn.get_capture_session( "cap-xxx" )
display_asset_id = cap.get_rtstream( "display" )[ 0 ].exported_asset_id
mic_asset_id = cap.get_rtstream( "mic" )[ 0 ].exported_asset_id

timeline = Timeline(conn)
timeline.resolution = "1280x720"

# Video track
video_track = Track()
video_track.add_clip( 0 , Clip( asset = VideoAsset( id = display_asset_id), duration = 60 ))
timeline.add_track(video_track)

# Audio track (mic only)
audio_track = Track()
audio_track.add_clip( 0 , Clip( asset = AudioAsset( id = mic_asset_id, volume = 1.0 ), duration = 60 ))
timeline.add_track(audio_track)

stream_url = timeline.generate_stream()
```

```
import { Timeline , Track , Clip , VideoAsset , AudioAsset } from 'videodb' ;

const cap = await conn . getCaptureSession ( "cap-xxx" );
const displayAssetId = cap . getRtstream ( "displays" )[ 0 ]. exportedAssetId ;
const micAssetId = cap . getRtstream ( "mics" )[ 0 ]. exportedAssetId ;

const timeline = new Timeline ( conn );
timeline . resolution = "1280x720" ;

// Video track
const videoTrack = new Track ();
videoTrack . addClip ( 0 , new Clip ({ asset: new VideoAsset ({ id: displayAssetId }), duration: 60 }));
timeline . addTrack ( videoTrack );

// Audio track (mic only)
const audioTrack = new Track ();
audioTrack . addClip ( 0 , new Clip ({ asset: new AudioAsset ({ id: micAssetId , volume: 1.0 }), duration: 60 }));
timeline . addTrack ( audioTrack );

const streamUrl = await timeline . generateStream ();
```

## [ Semantic Search](#semantic-search)

After export, captured content is searchable:

Python

Node.js

```
video = coll.get_video(exported_video_id)

# Index for search
video.index_spoken_words()

# Search
results = video.search( "action items from the meeting" )
for shot in results.shots:
print ( f " { shot.start } s: { shot.text } " )
shot.play()
```

```
const video = await coll . getVideo ( exportedVideoId );

// Index for search
await video . indexSpokenWords ();

// Search
const results = await video . search ( "action items from the meeting" );
for ( const shot of results . shots ) {
console . log ( ` ${ shot . start } s: ${ shot . text } ` );
await shot . play ();
}
```

## [ Which Asset to Use?](#which-asset-to-use)

| Use Case                     | Asset                               |
|------------------------------|-------------------------------------|
| Quick playback, sharing      | Muxed video ( `exported_video_id` ) |
| Separate mic vs system audio | Raw channel assets                  |
| Multi-track editing          | Raw channel assets                  |
| Custom audio mix             | Raw channel assets                  |
| Picture-in-picture           | Raw channel assets                  |

## [ Next Steps](#next-steps)

## Privacy Controls

Consent and redaction patterns

## Capture Overview

Architecture and quickstart

[Real-time Context](\pages\ingest\capture-sdks\realtime-context) [Privacy Controls](\pages\ingest\capture-sdks\privacy-controls)

⌘ I