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
    - [Timeline Architecture](\pages\act\programmable-editing\timeline-architecture)
    - [Aspect Ratio Control](\pages\act\programmable-editing\aspect-ratio-control)
    - [Trimming Vs Timing](\pages\act\programmable-editing\trimming-vs-timing)
    - [Clip Parameters](\pages\act\programmable-editing\clip-parameters)
    - [Caption Asset](\pages\act\programmable-editing\caption-asset)
    - [Text Asset](\pages\act\programmable-editing\text-asset)
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

- [The Two Start Parameters](#the-two-start-parameters)
    - [Asset.start - Source Trimming](#asset-start-source-trimming)
    - [track.add\_clip(start=...) - Timeline Positioning](#track-add_clip-start%3D%E2%80%A6-timeline-positioning)
- [Key Concept: Independent Control](#key-concept-independent-control)
- [Asset Parameters](#asset-parameters)
    - [VideoAsset](#videoasset)
    - [AudioAsset](#audioasset)
- [Common Patterns](#common-patterns)
    - [Sequential Clips (No Gaps)](#sequential-clips-no-gaps)
    - [Clips with Gaps](#clips-with-gaps)
    - [Overlapping Clips (Different Tracks)](#overlapping-clips-different-tracks)
- [Complete Example](#complete-example)
- [Next Steps](#next-steps)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Programmable Editing](\pages\act\programmable-editing\timeline-architecture)

# Trimming Vs Timing

Copy page

VideoDB Editor uses two separate start parameters that control different aspects of video composition. Understanding these parameters is key to controlling what plays and when.

Copy page

Open In Colab

<!-- image -->

VideoDB Editor uses two separate "start" parameters that control different aspects of video composition. This trips up almost everyone at first - you set start=10 and expect the video to play 10 seconds into your timeline, but it actually just skips the first 10 seconds of the source video. Understanding these two parameters is key to controlling both what plays and when it plays.

## [ The Two Start Parameters](#the-two-start-parameters)

### [ Asset.start - Source Trimming](#asset-start-source-trimming)

`VideoAsset(start=...)` skips the beginning of the source file.

Python

Node.js

```
asset = VideoAsset(
id = video.id,
start = 10 # Skip first 10 seconds of source video
)
```

```
const asset = new VideoAsset ( video . id , {
start: 10 // Skip first 10 seconds of source video
});
```

This controls which part of your source material gets used. Think of it like fast-forwarding to a specific timestamp before hitting play - you're extracting a segment from your original video.

### [ track.add\_clip(start=...) - Timeline Positioning](#track-add_clip-start=…-timeline-positioning)

Positions when the clip appears in the final timeline.

Python

Node.js

```
track.add_clip(
start = 5 , # Place clip at 5-second mark in final video
clip = clip
)
```

```
track . addClip (
5 , // Place clip at 5-second mark in final video
clip
);
```

This controls when your clip plays in the composed output - like dragging a clip to a specific position on an editing timeline. It's completely independent of what part of the source is playing.

## [ Key Concept: Independent Control](#key-concept-independent-control)

These parameters are completely independent, operating in two different coordinate systems. `Asset.start` works in "source video time" (which part of the original file), while `track.add_clip(start=...)` works in "output timeline time" (when it appears in the final video). You can extract any segment from your source and place it anywhere on your timeline.

Python

Node.js

```
# Extract seconds 10-20 from source, place at 5-second mark in timeline
clip = Clip(
asset = VideoAsset( id = video.id, start = 10 ), # TRIMMING: skip first 10s
duration = 10 # Play for 10 seconds
)

track = Track()
track.add_clip( start = 5 , clip = clip) # TIMING: appears at 5s in final
```

```
// Extract seconds 10-20 from source, place at 5-second mark in timeline
const clip = new Clip ({
asset: new VideoAsset ( video . id , { start: 10 }), // TRIMMING: skip first 10s
duration: 10 // Play for 10 seconds
});

const track = new Track ();
track . addClip ( 5 , clip ); // TIMING: appears at 5s in final
```

Timeline structure:

- 0-5 seconds: Blank (background color)
- 5-15 seconds: Video plays (showing seconds 10-20 from source)

## [ Asset Parameters](#asset-parameters)

### [ VideoAsset](#videoasset)

| Parameter   | Type   | Description                                                             |
|-------------|--------|-------------------------------------------------------------------------|
| id          | str    | Video ID from VideoDB collection                                        |
| start       | int    | Timestamp (seconds) where playback begins in source file. Default: `0`  |
| volume      | float  | Audio volume multiplier. `1.0` = original, `0.0` = mute, `2.0` = double |
| crop        | Crop   | Crop edges of source video                                              |

### [ AudioAsset](#audioasset)

| Parameter   | Type   | Description                                              |
|-------------|--------|----------------------------------------------------------|
| id          | str    | Audio ID from VideoDB collection                         |
| start       | int    | Timestamp (seconds) where playback begins in source file |
| volume      | float  | Audio volume multiplier ( `0.0` - `2.0` )                |

## [ Common Patterns](#common-patterns)

### [ Sequential Clips (No Gaps)](#sequential-clips-no-gaps)

Python

Node.js

```
# Clips play one after another
track.add_clip( 0 , clip1) # 0-10s
track.add_clip( 10 , clip2) # 10-20s
track.add_clip( 20 , clip3) # 20-30s
```

```
// Clips play one after another
track . addClip ( 0 , clip1 ); // 0-10s
track . addClip ( 10 , clip2 ); // 10-20s
track . addClip ( 20 , clip3 ); // 20-30s
```

### [ Clips with Gaps](#clips-with-gaps)

Python

Node.js

```
# Intentional pauses between clips
track.add_clip( 0 , clip1) # 0-10s
track.add_clip( 15 , clip2) # 15-25s (5s gap)
track.add_clip( 35 , clip3) # 35-45s (10s gap)
```

```
// Intentional pauses between clips
track . addClip ( 0 , clip1 ); // 0-10s
track . addClip ( 15 , clip2 ); // 15-25s (5s gap)
track . addClip ( 35 , clip3 ); // 35-45s (10s gap)
```

### [ Overlapping Clips (Different Tracks)](#overlapping-clips-different-tracks)

Python

Node.js

```
main_track = Track()
main_track.add_clip( 0 , main_clip)

# Overlay appears at specific time
overlay_track = Track()
overlay_track.add_clip( 20 , overlay_clip) # Appears at 20s

timeline.add_track(main_track)
timeline.add_track(overlay_track)
```

```
const mainTrack = new Track ();
mainTrack . addClip ( 0 , mainClip );

// Overlay appears at specific time
const overlayTrack = new Track ();
overlayTrack . addClip ( 20 , overlayClip ); // Appears at 20s

timeline . addTrack ( mainTrack );
timeline . addTrack ( overlayTrack );
```

## [ Complete Example](#complete-example)

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip, VideoAsset

timeline = Timeline(conn)

# Extract 15 seconds starting at 30s from source
clip1 = Clip(
asset = VideoAsset(
id = video.id,
start = 30 # Skip first 30s of source
),
duration = 15 # Play for 15 seconds (shows 30s-45s of source)
)

track = Track()
track.add_clip( start = 10 , clip = clip1) # Place at 10s in final timeline

timeline.add_track(track)
stream_url = timeline.generate_stream()
```

```
import { Timeline , Track , Clip , VideoAsset } from 'videodb' ;

const timeline = new Timeline ( conn );

// Extract 15 seconds starting at 30s from source
const clip1 = new Clip ({
asset: new VideoAsset ( video . id , {
start: 30 // Skip first 30s of source
}),
duration: 15 // Play for 15 seconds (shows 30s-45s of source)
});

const track = new Track ();
track . addClip ( 10 , clip1 ); // Place at 10s in final timeline

timeline . addTrack ( track );
const streamUrl = await timeline . generateStream ();
```

Result: Final video has blank 0-10s, then shows seconds 30-45 from source at 10-25s position.

## [ Next Steps](#next-steps)

## Trimming vs Timing

Hands-on practice with trimming and timing patterns, multi-clip workflows, and timing precision.

[Aspect Ratio Control](\pages\act\programmable-editing\aspect-ratio-control) [Clip Parameters](\pages\act\programmable-editing\clip-parameters)

⌘ I