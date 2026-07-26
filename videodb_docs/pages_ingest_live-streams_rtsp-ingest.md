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
- [Connection Methods](#connection-methods)
    - [RTSP URL Format](#rtsp-url-format)
    - [Connect from Camera](#connect-from-camera)
- [RTStream Object](#rtstream-object)
- [Retrieve Existing Streams](#retrieve-existing-streams)
    - [Get by ID](#get-by-id)
    - [List All Streams](#list-all-streams)
- [Playback URLs](#playback-urls)
- [Supported Sources](#supported-sources)
- [Connection Notes](#connection-notes)
- [What You Can Build](#what-you-can-build)
- [Next Steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Live Streams](\pages\ingest\live-streams\rtsp-ingest)

# RTSP Ingest

Copy page

Connect any RTSP/RTMP video source to VideoDB. Cameras, encoders, and live feeds become instantly searchable and actionable.

Copy page

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()

# Connect a live stream
rtstream = coll.connect_rtstream(
name = "Lobby Camera" ,
url = "rtsp://user:pass@192.168.1.100:554/stream"
)
print (rtstream.id) # rts-xxx
```

```
import { connect } from 'videodb' ;

const conn = await connect ();
const coll = await conn . getCollection ();

// Connect a live stream
const rtstream = await coll . connectRtstream ({
name: "Lobby Camera" ,
rtspUrl: "rtsp://user:pass@192.168.1.100:554/stream"
});
console . log ( rtstream . id ); // rts-xxx
```

## [ Connection Methods](#connection-methods)

### [ RTSP URL Format](#rtsp-url-format)

```
rtsp://[username:password@]host[:port]/path
```

**Examples:**

```
rtsp://admin:pass123@192.168.1.100:554/live
rtsp://camera.example.com:554/stream1
rtsp://user:pass@10.0.0.50/cam/realmonitor
```

### [ Connect from Camera](#connect-from-camera)

Python

Node.js

```
# IP Camera
rtstream = coll.connect_rtstream(
name = "Warehouse Camera 1" ,
url = "rtsp://admin:password@192.168.1.50:554/live"
)

# Encoder/NVR
rtstream = coll.connect_rtstream(
name = "NVR Channel 3" ,
url = "rtsp://admin:admin@nvr.local:554/ch3"
)
```

```
// IP Camera
const rtstream = await coll . connectRtstream ({
name: "Warehouse Camera 1" ,
rtspUrl: "rtsp://admin:password@192.168.1.50:554/live"
});

// Encoder/NVR
const rtstreamNVR = await coll . connectRtstream ({
name: "NVR Channel 3" ,
rtspUrl: "rtsp://admin:admin@nvr.local:554/ch3"
});
```

## [ RTStream Object](#rtstream-object)

After connecting, you receive an RTStream object:

| Attribute       | Type   | Description                    |
|-----------------|--------|--------------------------------|
| `id`            | str    | Unique identifier (rts-xxx)    |
| `name`          | str    | Label you supplied             |
| `collection_id` | str    | Parent collection              |
| `status`        | str    | `connected` , `stopped` , etc. |
| `sample_rate`   | float  | Frame rate (default: 1 fps)    |
| `audio`         | bool   | Audio ingestion enabled        |

## [ Retrieve Existing Streams](#retrieve-existing-streams)

### [ Get by ID](#get-by-id)

Python

Node.js

```
rtstream = coll.get_rtstream( "rts-xxx" )
```

```
const rtstream = await coll . getRtstream ( "rts-xxx" );
```

### [ List All Streams](#list-all-streams)

Python

Node.js

```
rtstreams = coll.list_rtstreams(
limit = 10 ,
offset = 0 ,
status = "connected" ,
name = "Lobby" ,
ordering = "-created_at"
)
```

```
const rtstreams = await coll . listRtstreams ({
limit: 10 ,
offset: 0 ,
status: "connected" ,
name: "Lobby" ,
ordering: "-created_at"
});
```

| Parameter   | Description                            |
|-------------|----------------------------------------|
| `limit`     | Number of results                      |
| `offset`    | Skip N results                         |
| `status`    | Filter by status                       |
| `name`      | Filter by name                         |
| `ordering`  | Sort field (prefix `-` for descending) |

## [ Playback URLs](#playback-urls)

Generate HLS/MP4 URLs for any time range using Unix timestamps:

Python

Node.js

```
import time

# Get playback URL for last 60 seconds
now = int (time.time())
start = now - 60
stream_url = rtstream.generate_stream( start = start, end = now)
```

```
// Get playback URL for last 60 seconds
const now = Math . floor ( Date . now () / 1000 );
const start = now - 60 ;
const streamUrl = await rtstream . generateStream ({ start , end: now });
```

The `start` and `end` parameters expect Unix timestamps (seconds since epoch), not relative time offsets.

## [ Supported Sources](#supported-sources)

| Source            | Format    | Notes                          |
|-------------------|-----------|--------------------------------|
| IP Cameras        | RTSP      | Most common, H.264/H.265       |
| NVR/DVR           | RTSP      | Per-channel streams            |
| Encoders          | RTSP/RTMP | OBS, FFmpeg, hardware encoders |
| Streaming Servers | RTSP      | Wowza, nginx-rtmp              |

## [ Connection Notes](#connection-notes)

- **Secure Storage** - All video feeds are securely stored and accessible anytime
- **Default Sample Rate** - Streams are ingested at 1 fps by default
- **Network** - Ensure your RTSP source is accessible from VideoDB's servers

## [ What You Can Build](#what-you-can-build)

## Baby Crib Monitoring

Real-time infant monitoring with AI-powered alerts

## Intrusion Detection

Detect unauthorized access to restricted areas

## Traffic Violations

Monitor traffic cameras for red light and stop sign violations

## [ Next Steps](#next-steps)

## Real-time APIs

Index, transcribe, and set up alerts

## Stream Lifecycle

Start, stop, and reconnect patterns

[Collection Patterns](\pages\ingest\files-and-collections\collection-patterns) [Real-time APIs](\pages\ingest\live-streams\realtime-apis)

⌘ I