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
    - [When to Transcode](\pages\ingest\transcoding\when-to-transcode)
    - [Output Formats](\pages\ingest\transcoding\output-formats)

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
- [When You Need Transcoding](#when-you-need-transcoding)
- [Input Limits](#input-limits)
- [Processing Modes](#processing-modes)
- [Job Lifecycle](#job-lifecycle)
    - [Check Status](#check-status)
- [Webhook Callbacks](#webhook-callbacks)
    - [Success](#success)
    - [Failure](#failure)
- [Error Codes](#error-codes)
- [Decision Flowchart](#decision-flowchart)
- [Next Steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Transcoding](\pages\ingest\transcoding\when-to-transcode)

# When to Transcode

Copy page

Decide when transcoding is needed, understand input limits, and choose the right processing mode

Copy page

Transcoding converts video to standardized formats for playback and processing. Not all uploads need transcoding - use this guide to decide.

## [ Quick Example](#quick-example)

Python

Node.js

```
from videodb import TranscodeMode, VideoConfig

job_id = conn.transcode(
source = "https://example.com/source.mov" ,
callback_url = "https://your-backend.com/webhooks" ,
mode = TranscodeMode.lightning
)
print ( f "Job queued: { job_id } " )
```

```
import { TranscodeMode } from 'videodb' ;

const jobId = await conn . transcode (
"https://example.com/source.mov" ,
"https://your-backend.com/webhooks" ,
TranscodeMode . lightning
);
console . log ( `Job queued: ${ jobId } ` );
```

## [ When You Need Transcoding](#when-you-need-transcoding)

| Scenario                        | Transcode?   | Why                             |
|---------------------------------|--------------|---------------------------------|
| MOV, MKV, AVI input             | Yes          | Convert to MP4/HLS for playback |
| 4K source → 720p delivery       | Yes          | Reduce size and bandwidth       |
| High framerate (120fps) → 30fps | Yes          | Normalize for web               |
| Custom aspect ratio             | Yes          | Crop or letterbox               |
| MP4 already in target format    | No           | Upload directly                 |
| Already optimized for web       | No           | Save processing cost            |

## [ Input Limits](#input-limits)

| Capability     | Limit             |
|----------------|-------------------|
| Max Resolution | 4K (3840 × 2160)  |
| Max Frame Rate | 100 fps           |
| Max File Size  | 8 GB              |
| Audio Support  | AAC, MP3, or mute |

Need larger files or custom pipelines? Contact [Sales](mailto:engg@videodb.io) or reach out on [Discord](https://discord.gg/py9P639jGz) .

## [ Processing Modes](#processing-modes)

Choose based on your latency and cost requirements:

| Mode        | Best For            | Trade-off           |
|-------------|---------------------|---------------------|
| `lightning` | Real-time workflows | Faster, higher cost |
| `economy`   | Batch processing    | Slower, lower cost  |

Python

Node.js

```
from videodb import TranscodeMode

# Fast - for user-facing flows
job_id = conn.transcode(
source = url,
callback_url = callback,
mode = TranscodeMode.lightning
)

# Economical - for batch jobs
job_id = conn.transcode(
source = url,
callback_url = callback,
mode = TranscodeMode.economy
)
```

```
import { TranscodeMode } from 'videodb' ;

// Fast - for user-facing flows
const jobId = await conn . transcode (
url ,
callback ,
TranscodeMode . lightning
);

// Economical - for batch jobs
const jobId = await conn . transcode (
url ,
callback ,
TranscodeMode . economy
);
```

## [ Job Lifecycle](#job-lifecycle)

1. **Submit Job** - `conn.transcode()` → Status: `pending`
2. **Processing** - Fetch &amp; encode → Status: `processing`
3. **Complete** - Webhook triggers with output URL

### [ Check Status](#check-status)

Python

Node.js

```
job = conn.get_transcode_details(job_id)
print (job.status) # pending | processing | completed | failed
print (job.output) # URL when completed
```

```
const job = await conn . getTranscodeDetails ( jobId );
console . log ( job . status ); // pending | processing | completed | failed
console . log ( job . output ); // URL when completed
```

## [ Webhook Callbacks](#webhook-callbacks)

### [ Success](#success)

```
{
"success" : true ,
"data" : {
"job_id" : "xxx" ,
"output" : "https://transcoded-output-url.mp4"
},
"message" : "Transcode job completed"
}
```

### [ Failure](#failure)

```
{
"success" : false ,
"job_id" : "xxx" ,
"code" : "invalid_source" ,
"message" : "Failed to download source media" ,
"reason" : "HTTP 403 Forbidden"
}
```

## [ Error Codes](#error-codes)

| Code                    | Meaning                  | Fix                         |
|-------------------------|--------------------------|-----------------------------|
| `invalid_video_config`  | Resolution/FPS/CRF error | Check ≤4K, ≤100 fps         |
| `invalid_audio_config`  | Conflicting audio params | Adjust audio config         |
| `invalid_source`        | URL not accessible       | Check URL permissions       |
| `invalid_media`         | Unsupported format       | Convert to supported format |
| `internal_server_error` | Unexpected error         | Retry or contact support    |

## [ Decision Flowchart](#decision-flowchart)

```
Source file arrives
│
▼
Is it MP4/HLS at target resolution? ──Yes──► Upload directly
│
No
▼
Need resolution change? ──────────────────► Transcode
│
No
▼
Need format conversion? ──────────────────► Transcode
│
No
▼
Need framerate adjustment? ────────────────► Transcode
│
No
▼
Upload directly
```

## [ Next Steps](#next-steps)

## Output Formats

MP4/HLS, resolutions, quality settings

## Upload Video

Ingest media into VideoDB

[Privacy Controls](\pages\ingest\capture-sdks\privacy-controls) [Output Formats](\pages\ingest\transcoding\output-formats)

⌘ I