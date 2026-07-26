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
- [Output Formats](#output-formats)
- [Resolution Options](#resolution-options)
- [VideoConfig](#videoconfig)
    - [Quality Presets (CRF)](#quality-presets-crf)
    - [Framerate](#framerate)
- [Aspect Ratio Control](#aspect-ratio-control)
    - [ResizeMode](#resizemode)
- [AudioConfig](#audioconfig)
- [Common Configurations](#common-configurations)
    - [Web Delivery (720p, optimized)](#web-delivery-720p-optimized)
    - [Social Media Square (1:1)](#social-media-square-11)
    - [Archival (High Quality)](#archival-high-quality)
    - [Mobile Preview (Low Bandwidth)](#mobile-preview-low-bandwidth)
- [Job Output Details](#job-output-details)
- [Next Steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Transcoding](\pages\ingest\transcoding\when-to-transcode)

# Output Formats

Copy page

Configure transcoding output - formats, resolutions, quality presets, and aspect ratio control

Copy page

Configure transcoding output for your use case - streaming, archival, or web delivery.

## [ Quick Example](#quick-example)

Python

Node.js

```
from videodb import TranscodeMode, VideoConfig, AudioConfig, ResizeMode

job_id = conn.transcode(
source = "https://example.com/source.mov" ,
callback_url = "https://your-backend.com/webhooks" ,
mode = TranscodeMode.lightning,
video_config = VideoConfig(
resolution = 720 ,
quality = 23 ,
framerate = 30 ,
resize_mode = ResizeMode.fit
),
audio_config = AudioConfig( mute = False )
)
```

```
import { TranscodeMode , ResizeMode } from 'videodb' ;

const jobId = await conn . transcode (
"https://example.com/source.mov" ,
"https://your-backend.com/webhooks" ,
TranscodeMode . lightning ,
{
resolution: 720 ,
quality: 23 ,
framerate: 30 ,
resizeMode: ResizeMode . fit
},
{ mute: false }
);
```

## [ Output Formats](#output-formats)

| Format   | Use Case                        |
|----------|---------------------------------|
| MP4      | Download, archival, playback    |
| HLS      | Adaptive streaming, web players |

## [ Resolution Options](#resolution-options)

| Resolution   | Dimensions   | Use Case               |
|--------------|--------------|------------------------|
| 360p (SD)    | 640 × 360    | Mobile, low bandwidth  |
| 720p (HD)    | 1280 × 720   | General web delivery   |
| 1080p (FHD)  | 1920 × 1080  | High quality streaming |

## [ VideoConfig](#videoconfig)

| Field          | Type       | Default   | Notes                                     |
|----------------|------------|-----------|-------------------------------------------|
| `resolution`   | int        | 720       | Height in pixels (auto-calculates width)  |
| `quality`      | int        | 23        | CRF (lower = better quality, larger file) |
| `framerate`    | int        | Source    | Target framerate (max 100 fps)            |
| `aspect_ratio` | str        | Source    | e.g., "16:9", "1:1", None for original    |
| `resize_mode`  | ResizeMode | crop      | How to handle aspect ratio changes        |

### [ Quality Presets (CRF)](#quality-presets-crf)

| Quality           | CRF Range   | Use Case                 |
|-------------------|-------------|--------------------------|
| Visually Lossless | 18-20       | Archival, editing source |
| Good Quality      | 21-23       | General delivery         |
| Lower Quality     | 24-28       | Web previews, thumbnails |

Lower CRF = better quality but larger file size. Default 23 is a good balance.

### [ Framerate](#framerate)

Supported: 30fps and 60fps output.

Python

Node.js

```
VideoConfig(
resolution = 720 ,
framerate = 30 # or 60
)
```

```
{
resolution : 720 ,
framerate : 30 // or 60
}
```

## [ Aspect Ratio Control](#aspect-ratio-control)

### [ ResizeMode](#resizemode)

| Mode   | Behavior                  | Visual                            |
|--------|---------------------------|-----------------------------------|
| `crop` | Crop edges to fill target | No black bars, content may be cut |
| `fit`  | Scale uniformly           | May letterbox (black bars)        |
| `pad`  | Add black bars            | Content preserved, bars added     |

Python

Node.js

```
from videodb import ResizeMode, VideoConfig

# Crop to fill (may lose edges)
VideoConfig( aspect_ratio = "16:9" , resize_mode = ResizeMode.crop)

# Fit with letterbox
VideoConfig( aspect_ratio = "16:9" , resize_mode = ResizeMode.fit)

# Pad with black bars
VideoConfig( aspect_ratio = "1:1" , resize_mode = ResizeMode.pad)
```

```
import { ResizeMode } from 'videodb' ;

// Crop to fill (may lose edges)
{ aspectRatio : "16:9" , resizeMode : ResizeMode . crop }

// Fit with letterbox
{ aspectRatio : "16:9" , resizeMode : ResizeMode . fit }

// Pad with black bars
{ aspectRatio : "1:1" , resizeMode : ResizeMode . pad }
```

## [ AudioConfig](#audioconfig)

| Field   | Type   | Default   | Notes                      |
|---------|--------|-----------|----------------------------|
| `mute`  | bool   | false     | `true` removes audio track |

Python

Node.js

```
from videodb import AudioConfig

# Keep audio
AudioConfig( mute = False )

# Remove audio
AudioConfig( mute = True )
```

```
// Keep audio
{ mute : false }

// Remove audio
{ mute : true }
```

## [ Common Configurations](#common-configurations)

### [ Web Delivery (720p, optimized)](#web-delivery-720p-optimized)

Python

Node.js

```
VideoConfig(
resolution = 720 ,
quality = 23 ,
framerate = 30 ,
resize_mode = ResizeMode.fit
)
```

```
{
resolution : 720 ,
quality : 23 ,
framerate : 30 ,
resizeMode : ResizeMode . fit
}
```

### [ Social Media Square (1:1)](#social-media-square-11)

Python

Node.js

```
VideoConfig(
resolution = 720 ,
aspect_ratio = "1:1" ,
resize_mode = ResizeMode.crop
)
```

```
{
resolution : 720 ,
aspectRatio : "1:1" ,
resizeMode : ResizeMode . crop
}
```

### [ Archival (High Quality)](#archival-high-quality)

Python

Node.js

```
VideoConfig(
resolution = 1080 ,
quality = 18 ,
framerate = 60
)
```

```
{
resolution : 1080 ,
quality : 18 ,
framerate : 60
}
```

### [ Mobile Preview (Low Bandwidth)](#mobile-preview-low-bandwidth)

Python

Node.js

```
VideoConfig(
resolution = 360 ,
quality = 28 ,
framerate = 30
)
```

```
{
resolution : 360 ,
quality : 28 ,
framerate : 30
}
```

## [ Job Output Details](#job-output-details)

Completed jobs include detailed metadata:

```
{
"job_id" : "xxx" ,
"status" : "completed" ,
"output" : "https://transcoded-output.mp4" ,
"input_details" : {
"resolution" : "1920x1080" ,
"framerate" : 30 ,
"duration" : 634.53 ,
"size" : 263.34 ,
"video_codec" : "h264" ,
"audio_codec" : "mp3"
},
"output_details" : {
"resolution" : "1920x1080" ,
"framerate" : 30 ,
"duration" : 635.06 ,
"size" : 253.84 ,
"format" : "mp4" ,
"video_codec" : "h264" ,
"audio_codec" : "aac"
},
"cost" : 0.1058
}
```

## [ Next Steps](#next-steps)

## When to Transcode

Decision guide and processing modes

## Upload Video

Ingest media into VideoDB

[When to Transcode](\pages\ingest\transcoding\when-to-transcode) [Create an Index](\pages\understand\indexing-pipelines\create-an-index)

⌘ I