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
- [Lifecycle Control](#lifecycle-control)
    - [Start/Stop](#start%2Fstop)
    - [Status Values](#status-values)
- [Export a Stopped Stream](#export-a-stopped-stream)
    - [Export Parameters](#export-parameters)
    - [RTStreamExportResult](#rtstreamexportresult)
- [Index Lifecycle](#index-lifecycle)
- [Meeting Recording](#meeting-recording)
    - [Start Recording](#start-recording)
    - [Recording to Collection](#recording-to-collection)
    - [Track Recording Status](#track-recording-status)
    - [Recording Status Values](#recording-status-values)
    - [Callback Payload](#callback-payload)
    - [Access Recording](#access-recording)
- [Supported Platforms](#supported-platforms)
- [Meeting Features](#meeting-features)
- [Next Steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Live Streams](\pages\ingest\live-streams\rtsp-ingest)

# Stream Lifecycle

Copy page

Manage RTStream lifecycle - start, stop, resume, and handle live stream sources including meeting recordings.

Copy page

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()

# Get existing stream
rtstream = coll.get_rtstream( "rts-xxx" )

# Control lifecycle
rtstream.stop() # Pause ingestion
rtstream.start() # Resume ingestion
```

```
import { connect } from 'videodb' ;

const conn = await connect ();
const coll = await conn . getCollection ();

// Get existing stream
const rtstream = await coll . getRtstream ( "rts-xxx" );

// Control lifecycle
await rtstream . stop (); // Pause ingestion
await rtstream . start (); // Resume ingestion
```

## [ Lifecycle Control](#lifecycle-control)

### [ Start/Stop](#start\stop)

Python

Node.js

```
# Pause ingestion (stream remains configured)
rtstream.stop()

# Resume ingestion
rtstream.start()
```

```
// Pause ingestion
await rtstream . stop ();

// Resume ingestion
await rtstream . start ();
```

### [ Status Values](#status-values)

| Status      | Description        |
|-------------|--------------------|
| `connected` | Actively ingesting |
| `stopped`   | Paused, can resume |
| `error`     | Connection issue   |

## [ Export a Stopped Stream](#export-a-stopped-stream)

After stopping a stream, you can export it as a video or audio asset in your collection using `export()` .

Python

Node.js

```
# Export a stopped stream as a video/audio asset
result = rtstream.export( name = "my_recording" )

# RTStreamExportResult attributes
print (result.video_id) # "m-xxx"
print (result.stream_url) # HLS stream URL
print (result.player_url) # Player URL (None for audio-only)
print (result.duration) # Duration in seconds

# Generate embed code from export
embed_html = result.get_embed_code()
```

```
// Export a stopped stream as a video/audio asset
const result = await rtstream . export ({ name: "my_recording" });

// RTStreamExportResult attributes
console . log ( result . videoId ); // "m-xxx"
console . log ( result . streamUrl ); // HLS stream URL
console . log ( result . playerUrl ); // Player URL (null for audio-only)
console . log ( result . duration ); // Duration in seconds

// Generate embed code from export
const embedHtml = result . getEmbedCode ();
```

### [ Export Parameters](#export-parameters)

| Parameter   | Type           | Description                                                            |
|-------------|----------------|------------------------------------------------------------------------|
| `name`      | str (optional) | Name for the exported asset. Defaults to `"{stream_name} - Recording"` |

### [ RTStreamExportResult](#rtstreamexportresult)

| Attribute    | Description                                            |
|--------------|--------------------------------------------------------|
| `video_id`   | The ID of the exported video/audio asset               |
| `stream_url` | HLS stream URL for playback                            |
| `player_url` | Shareable player URL ( `None` for audio-only channels) |
| `name`       | Name of the exported asset                             |
| `duration`   | Duration of the recording in seconds                   |

## [ Index Lifecycle](#index-lifecycle)

Indexes can also be started/stopped independently:

Python

Node.js

```
scene_index = rtstream.get_scene_index(index_id)

# Pause indexing (stream continues)
scene_index.stop()

# Resume indexing
scene_index.start()
```

```
const sceneIndex = await rtstream . getSceneIndex ( indexId );

// Pause indexing
await sceneIndex . stop ();

// Resume indexing
await sceneIndex . start ();
```

## [ Meeting Recording](#meeting-recording)

Record from Zoom, Google Meet, or Microsoft Teams. A bot joins your meeting, records, and uploads directly to VideoDB.

Roadmap to AI teammates showing the meeting recording workflow

<!-- image -->

### [ Start Recording](#start-recording)

Python

Node.js

```
meeting = conn.record_meeting(
meeting_url = "https://meet.google.com/abc-defg-hij" ,
bot_name = "Meeting Recorder" ,
bot_image_url = "https://your-domain.com/bot-avatar.jpg" ,
meeting_title = "Weekly Standup" ,
callback_url = "https://your-backend.com/webhooks/meeting" ,
callback_data = { "internal_id" : "123" }
)
print ( f "Recording started: { meeting.id } " )
```

```
const meeting = await conn . recordMeeting ({
meetingUrl: "https://meet.google.com/abc-defg-hij" ,
botName: "Meeting Recorder" ,
botImageUrl: "https://your-domain.com/bot-avatar.jpg" ,
meetingTitle: "Weekly Standup" ,
callbackUrl: "https://your-backend.com/webhooks/meeting" ,
callbackData: { internalId: "123" }
});
console . log ( `Recording started: ${ meeting . id } ` );
```

### [ Recording to Collection](#recording-to-collection)

Python

Node.js

```
coll = conn.get_collection( "your-collection-id" )

meeting = coll.record_meeting(
meeting_url = "https://zoom.us/j/123456789" ,
bot_name = "Team Recorder" ,
meeting_title = "Sprint Planning" ,
callback_url = "https://your-backend.com/webhooks"
)
```

```
const coll = await conn . getCollection ( "your-collection-id" );

const meeting = await coll . recordMeeting ({
meetingUrl: "https://zoom.us/j/123456789" ,
botName: "Team Recorder" ,
meetingTitle: "Sprint Planning" ,
callbackUrl: "https://your-backend.com/webhooks"
});
```

### [ Track Recording Status](#track-recording-status)

Python

Node.js

```
# Poll status
meeting.refresh()
print ( f "Status: { meeting.status } " )

# Wait for completion
if meeting.wait_for_status( "done" , timeout = 3600 , interval = 60 ):
print ( "Recording complete!" )
video = coll.get_video(meeting.video_id)
```

```
// Poll status
await meeting . refresh ();
console . log ( `Status: ${ meeting . status } ` );

// Wait for completion
const success = await meeting . waitForStatus ( "done" , 3600 , 60 );
if ( success ) {
console . log ( "Recording complete!" );
const video = await coll . getVideo ( meeting . videoId );
}
```

### [ Recording Status Values](#recording-status-values)

| Status         | Description         |
|----------------|---------------------|
| `initializing` | Bot is being set up |
| `processing`   | Actively recording  |
| `done`         | Recording complete  |
| `failed`       | Recording failed    |

### [ Callback Payload](#callback-payload)

**Success:**

```
{
"success" : true ,
"message" : "Meeting recording completed." ,
"data" : {
"video_id" : "m-xxx" ,
"speaker_timeline" : [
{ "speaker_name" : "Alice" , "start_time_seconds" : 9.94 }
],
"stream_url" : "..." ,
"player_url" : "..."
}
}
```

**Failure:**

```
{
"success" : false ,
"message" : "Failed to record meeting."
}
```

### [ Access Recording](#access-recording)

Python

Node.js

```
meeting = coll.get_meeting( "meeting-id" )

# Get the recorded video
video = coll.get_video(meeting.video_id)

# Now searchable, indexable, etc.
video.index_spoken_words()
```

```
const meeting = await coll . getMeeting ( "meeting-id" );

// Get the recorded video
const video = await coll . getVideo ( meeting . videoId );

// Now searchable, indexable, etc.
await video . indexSpokenWords ();
```

## [ Supported Platforms](#supported-platforms)

| Platform        | URL Format                             |
|-----------------|----------------------------------------|
| Google Meet     | `https://meet.google.com/xxx-xxxx-xxx` |
| Zoom            | `https://zoom.us/j/123456789`          |
| Microsoft Teams | Teams meeting link                     |

## [ Meeting Features](#meeting-features)

- **Brand-able Bot** - Custom name and avatar
- **Speaker Timeline** - Per-speaker timestamps (Google Meet)
- **Webhook Callbacks** - Get notified on completion
- **Collection Storage** - Video lands directly in your collection

Upcoming features for meeting recorder

<!-- image -->

## [ Next Steps](#next-steps)

## RTSP Ingest

Connect camera streams

## Real-time APIs

Index and search live streams

[Real-time APIs](\pages\ingest\live-streams\realtime-apis) [Capture SDK Overview](\pages\ingest\capture-sdks\overview)

⌘ I