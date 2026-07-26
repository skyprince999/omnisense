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
- [Supported Languages](\pages\core-concepts\supported-languages)
- [Sandbox Compute](\pages\core-concepts\sandbox-compute)
- [Sandbox Models](\pages\core-concepts\sandbox-models)
- [Events &amp; Real-time](\pages\core-concepts\events-and-realtime)
- [Programmable Editing](\pages\core-concepts\programmable-editing)
- [Security &amp; Privacy](\pages\core-concepts\security-privacy)

### Ingest

- Files and Collections
- Live Streams
    - [RTSP Ingest](\pages\ingest\live-streams\rtsp-ingest)
    - [Understand &amp; Index RTStreams](\pages\ingest\live-streams\rtstream-understand-index)
    - [Real-time APIs](\pages\ingest\live-streams\realtime-apis)
    - [Stream Lifecycle](\pages\ingest\live-streams\stream-lifecycle)
- Capture SDKs
- Transcoding

### Understand

- Understanding &amp; Indexing Pipelines
- Search and Retrieval
- Legacy Indexing &amp; Search
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

- [What is supported](#what-is-supported)
- [Quick example](#quick-example)
- [1. Understand the stream](#1-understand-the-stream)
    - [Parameters](#parameters)
- [2. Get the continuous output](#2-get-the-continuous-output)
- [3. Index the output](#3-index-the-output)
- [4. Manage the continuous jobs](#4-manage-the-continuous-jobs)
- [5. Retrieve and play results](#5-retrieve-and-play-results)
- [6. Add alerts](#6-add-alerts)
- [How this differs from videos](#how-this-differs-from-videos)
- [Compatibility with existing helpers](#compatibility-with-existing-helpers)
- [Target API routes](#target-api-routes)
- [Next steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Live Streams](\pages\ingest\live-streams\rtsp-ingest)

# Understand &amp; Index RTStreams

Copy page

Use the new Understand → Index interface with RTStreams for continuous VLM analysis and search.

Copy page

RTStreams use the same retrieval model as videos:

```
Understand → Index → Retrieve
```

The difference is lifecycle. A video understanding job finishes when the file is processed. An RTStream understanding job is continuous: it keeps processing new windows while the stream and job are running.

Initial RTStream support for the new interface is limited to **VLM visual understanding** with **time-based segmentation** . Other analyzers and segmentation modes will be added later.

## [ What is supported](#what-is-supported)

| Capability   | Initial RTStream support             |
|--------------|--------------------------------------|
| Analyzer     | `vlm` only                           |
| Segmentation | `{"type": "time"}` only              |
| Sampling     | Frames per time window               |
| Index source | VLM understanding output             |
| Job mode     | Continuous                           |
| Retrieval    | RTStream search over indexed windows |
| Alerts       | Alerts attached to RTStream indexes  |

Unsupported analyzer types such as `spoken_words` , `object_detection` , `ocr` , `faces` , `brands` , `activity_recognition` , and `location_detection` should return a validation error until support is rolled out.

## [ Quick example](#quick-example)

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()
rtstream = coll.get_rtstream( "rts-xxx" )

# 1. Continuously understand the live stream with a VLM
understanding = rtstream.understand(
segmentation = { "type" : "time" , "window" : "10s" },
analyzers = [
{
"type" : "vlm" ,
"name" : "scene" ,
"sampling" : { "frame_count" : 5 },
"config" : {
"prompt" : "Describe the scene, people, activity, and unusual events." ,
"model" : "base" ,
},
}
],
store = True ,
)

# 2. Continuously index the VLM output for retrieval
index = rtstream.index(
name = "scene_search" ,
source = understanding.outputs[ "scene" ],
use_for = [ "semantic" ],
)

# 3. Search indexed stream windows
results = rtstream.search(
query = "person entering with a package" ,
index_id = index.id,
)

for shot in results.shots:
print (shot.start, shot.end, shot.text)
shot.play()
```

## [ 1. Understand the stream](#1-understand-the-stream)

Use `rtstream.understand(...)` to start a continuous understanding job. It returns an `RTStreamUnderstanding` object containing the job ID, status, outputs, and lifecycle methods.

```
understanding = rtstream.understand(
segmentation = { "type" : "time" , "window" : "5s" },
analyzers = [
{
"type" : "vlm" ,
"name" : "scene" ,
"sampling" : { "frame_count" : 2 },
"config" : {
"prompt" : "Describe what is happening in this time window."
},
}
],
store = True ,
ws_connection_id = ws.connection_id, # optional
)
```

### [ Parameters](#parameters)

| Field                              | Description                                                     |
|------------------------------------|-----------------------------------------------------------------|
| `segmentation.type`                | Must be `"time"` in the initial rollout.                        |
| `segmentation.window`              | Duration of each stream window, for example `"5s"` or `"10s"` . |
| `analyzers`                        | Must contain one `vlm` analyzer in the initial rollout.         |
| `analyzers[].name`                 | Output name. Use `"scene"` unless you need a custom key.        |
| `analyzers[].sampling.frame_count` | Number of frames sampled per time window.                       |
| `analyzers[].config.prompt`        | Prompt used to describe or structure each window.               |
| `store`                            | Use `True` when you plan to index the output.                   |
| `ws_connection_id`                 | Optional WebSocket connection for real-time updates.            |

## [ 2. Get the continuous output](#2-get-the-continuous-output)

The object returned by `rtstream.understand(...)` already contains the output descriptors:

```
scene_output = understanding.outputs[ "scene" ]
```

To reopen the job later, fetch it by its string ID:

```
understanding = rtstream.get_understanding( "und-xxx" )
```

For videos, an understanding output can be a finite artifact. For RTStreams, the output is a continuous source descriptor that points to records produced over time.

```
{
"type" : "understanding" ,
"asset_type" : "rtstream" ,
"rtstream_id" : "rts-xxx" ,
"understanding_id" : "und-xxx" ,
"output" : "scene" ,
"extract_type" : "vlm" ,
"mode" : "continuous"
}
```

You can inspect produced records by time range:

```
records = understanding.get_records(
start = 1711000000 ,
end = 1711000600 ,
page = 1 ,
page_size = 100 ,
)
```

## [ 3. Index the output](#3-index-the-output)

Use `rtstream.index(...)` to materialize the continuous VLM output for search. It returns an `RTStreamIndex` object with its ID and lifecycle methods.

```
index = rtstream.index(
name = "front_door_activity" ,
source = understanding.outputs[ "scene" ],
use_for = [ "semantic" ],
)
```

If `use_for` is omitted, VideoDB chooses the default capabilities for the VLM scene output. In the initial RTStream rollout, the primary capability is semantic search over scene descriptions.

## [ 4. Manage the continuous jobs](#4-manage-the-continuous-jobs)

RTStream understanding and index jobs have continuous lifecycle controls.

```
# Reopen jobs later when you only have their string IDs
understanding = rtstream.get_understanding( "und-xxx" )
index = rtstream.get_index( "idx-xxx" )

# Pause or resume understanding
understanding.stop()
understanding.start()

# Pause or resume indexing
index.stop()
index.start()
```

| State     | Meaning                                                                  |
|-----------|--------------------------------------------------------------------------|
| `running` | The job processes new stream windows.                                    |
| `stopped` | The job stops processing new windows. Existing records remain available. |
| `failed`  | The job stopped because of an error.                                     |

Stopping the RTStream itself disconnects the media source. Stopping understanding or indexing only pauses that processing layer.

## [ 5. Retrieve and play results](#5-retrieve-and-play-results)

Search works like existing RTStream search: results are timestamped stream shots.

```
results = rtstream.search(
query = "delivery person at the entrance" ,
index_id = index.id,
score_threshold = 0.5 ,
)

for shot in results.shots:
print (shot.start, shot.end, shot.text)
stream_url = shot.generate_stream()
```

Each shot includes Unix timestamps. Use `shot.generate_stream()` or `shot.play()` to create a playable stream for that time range.

## [ 6. Add alerts](#6-add-alerts)

Alerts remain attached to RTStream indexes.

```
event_id = conn.create_event(
event_prompt = "Detect when someone enters the restricted area" ,
label = "restricted_area_entry" ,
)

alert_id = index.create_alert(
event_id = event_id,
callback_url = "https://your-backend.com/webhooks/alerts" ,
ws_connection_id = ws.connection_id, # optional
)
```

Manage alerts from the index:

```
alerts = index.list_alerts()
index.disable_alert(alert_id)
index.enable_alert(alert_id)
```

## [ How this differs from videos](#how-this-differs-from-videos)

| Video                                                     | RTStream                                               |
|-----------------------------------------------------------|--------------------------------------------------------|
| Finite media asset                                        | Continuous live source                                 |
| `video.understand(...)` eventually completes              | `rtstream.understand(...)` keeps running               |
| `video.index(...)` indexes a completed or stored artifact | `rtstream.index(...)` continuously indexes new records |
| Timestamps are relative seconds in the video              | Timestamps are Unix timestamps                         |
| Alerts are not part of the initial video index lifecycle  | Alerts are supported on RTStream indexes               |

## [ Compatibility with existing helpers](#compatibility-with-existing-helpers)

Existing RTStream helpers remain supported during migration:

```
scene_index = rtstream.index_visuals(
prompt = "Describe activity and detect unusual behavior" ,
batch_config = { "type" : "time" , "value" : 5 , "frame_count" : 2 },
)
```

The new interface separates that flow into two explicit steps:

```
understanding = rtstream.understand(
segmentation = { "type" : "time" , "window" : "5s" },
analyzers = [
{
"type" : "vlm" ,
"name" : "scene" ,
"sampling" : { "frame_count" : 2 },
"config" : { "prompt" : "Describe activity and detect unusual behavior" },
}
],
store = True ,
)

index = rtstream.index( source = understanding.outputs[ "scene" ])
```

Use the new interface for new VLM-based RTStream workloads. Use the existing helpers while migrating older applications.

## [ Target API routes](#target-api-routes)

The SDK methods map to these RTStream routes:

| SDK method                                           | Route                                                                    |
|------------------------------------------------------|--------------------------------------------------------------------------|
| `rtstream.understand(...)`                           | `POST /rtstream/{stream_id}/understand`                                  |
| `rtstream.list_understanding()`                      | `GET /rtstream/{stream_id}/understand`                                   |
| `rtstream.get_understanding(id)`                     | `GET /rtstream/{stream_id}/understand/{understanding_id}`                |
| `understanding.start()` / `understanding.stop()`     | `PATCH /rtstream/{stream_id}/understand/{understanding_id}/status`       |
| `understanding.get_records(...)`                     | `GET /rtstream/{stream_id}/understand/{understanding_id}/records`        |
| `rtstream.index(...)`                                | `POST /rtstream/{stream_id}/indexes`                                     |
| `rtstream.list_indexes()`                            | `GET /rtstream/{stream_id}/indexes`                                      |
| `rtstream.get_index(id)`                             | `GET /rtstream/{stream_id}/indexes/{index_id}`                           |
| `index.start()` / `index.stop()`                     | `PATCH /rtstream/{stream_id}/indexes/{index_id}/status`                  |
| `index.get_records(...)`                             | `GET /rtstream/{stream_id}/indexes/{index_id}/records`                   |
| `index.create_alert(...)`                            | `POST /rtstream/{stream_id}/indexes/{index_id}/alert`                    |
| `index.list_alerts()`                                | `GET /rtstream/{stream_id}/indexes/{index_id}/alert`                     |
| `index.enable_alert(id)` / `index.disable_alert(id)` | `PATCH /rtstream/{stream_id}/indexes/{index_id}/alert/{alert_id}/status` |

## [ Next steps](#next-steps)

## Real-time APIs

Existing RTStream transcription, search, alerts, and stream playback APIs.

## Events &amp; Real-time

Build event rules and deliver alerts over webhooks or WebSocket.

[RTSP Ingest](\pages\ingest\live-streams\rtsp-ingest) [Real-time APIs](\pages\ingest\live-streams\realtime-apis)

⌘ I