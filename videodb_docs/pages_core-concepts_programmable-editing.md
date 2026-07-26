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

- [When to Use Programmable Editing](#when-to-use-programmable-editing)
- [Quick Example](#quick-example)
- [Next Steps](#next-steps)
- [The 4-Layer Architecture](#the-4-layer-architecture)
- [Layer 1: Assets](#layer-1-assets)
- [Layer 2: Clips](#layer-2-clips)
- [Layer 3: Tracks](#layer-3-tracks)
    - [Sequencing Rules](#sequencing-rules)
    - [Z-Order](#z-order)
- [Layer 4: Timeline](#layer-4-timeline)
- [Common Patterns](#common-patterns)
    - [Highlight Reel from Search Results](#highlight-reel-from-search-results)
    - [Video with Logo Overlay](#video-with-logo-overlay)
    - [Auto-Captioned Video](#auto-captioned-video)
- [What You Can Build](#what-you-can-build)
- [Best Practices](#best-practices)

[Core Concepts](\pages\core-concepts\overview)

# Programmable Editing

Copy page

VideoDB Editor lets you create videos programmatically using code instead of clicking timelines. Build videos using the 4-layer architecture: Asset → Clip → Track → Timeline.

Copy page

## [ When to Use Programmable Editing](#when-to-use-programmable-editing)

Use the editor when you need to:

- Generate personalized videos at scale
- Build automated content pipelines
- Create video variations for A/B testing
- Compose clips from search results
- Add overlays, captions, and effects programmatically

## [ Quick Example](#quick-example)

```
from videodb.editor import Timeline, Track, Clip, VideoAsset

# 1. Asset - your raw content
video_asset = VideoAsset( id = video.id, start = 0 )

# 2. Clip - how it appears
clip = Clip( asset = video_asset, duration = 10 )

# 3. Track - when it plays
track = Track()
track.add_clip( 0 , clip)

# 4. Timeline - the final canvas
timeline = Timeline(conn)
timeline.add_track(track)
stream_url = timeline.generate_stream()
```

## [ Next Steps](#next-steps)

## Timeline Architecture

Complete guide to the 4-layer architecture

## Clip Parameters

Filters, transitions, and effects

## [ The 4-Layer Architecture](#the-4-layer-architecture)

Think of video composition like building with LEGO:

```
Asset → Clip → Track → Timeline
```

| Layer        | Purpose            | Example                        |
|--------------|--------------------|--------------------------------|
| **Asset**    | Raw content (what) | `VideoAsset(id=video.id)`      |
| **Clip**     | Presentation (how) | `Clip(asset=..., duration=10)` |
| **Track**    | Sequencing (when)  | `track.add_clip(0, clip)`      |
| **Timeline** | Canvas (output)    | `timeline.generate_stream()`   |

## [ Layer 1: Assets](#layer-1-assets)

Assets reference your content but don't define timing or effects.

```
from videodb.editor import VideoAsset, AudioAsset, ImageAsset, TextAsset

# Video content
video_asset = VideoAsset( id = video.id, start = 0 , volume = 1.0 )

# Audio (music, voiceover)
audio_asset = AudioAsset( id = audio.id, start = 0 , volume = 0.8 )

# Images (logos, watermarks)
image_asset = ImageAsset( id = image.id)

# Custom text
text_asset = TextAsset( text = "Hello World" )
```

**Key parameters:**

- `id` - The VideoDB media ID
- `start` - Trim point in source (skip first N seconds)
- `volume` - Audio level (0.0 to 2.0)

## [ Layer 2: Clips](#layer-2-clips)

Clips wrap assets and define **how** and **how long** they appear.

```
from videodb.editor import Clip, Fit, Position

clip = Clip(
asset = video_asset,
duration = 10 , # How long it plays
fit = Fit.crop, # How it scales to canvas
position = Position.center, # Where it appears
scale = 1.0 , # Size multiplier
opacity = 1.0 # Transparency (0-1)
)
```

**Fit modes:**

- `Fit.crop` - Fill canvas, crop edges if needed
- `Fit.contain` - Fit inside, add bars if needed
- `Fit.cover` - Stretch to fill (may distort)

**Position options:**

- 9-zone grid: `top_left` , `top` , `top_right` , `center_left` , `center` , `center_right` , `bottom_left` , `bottom` , `bottom_right`

## [ Layer 3: Tracks](#layer-3-tracks)

Tracks are timeline lanes that control **when** clips play.

```
from videodb.editor import Track

track = Track()
track.add_clip( 0 , clip1) # Starts at 0s
track.add_clip( 10 , clip2) # Starts at 10s
```

### [ Sequencing Rules](#sequencing-rules)

**Same track** = sequential playback:

```
track.add_clip( 0 , clip1) # 0s-5s
track.add_clip( 5 , clip2) # 5s-10s
```

**Different tracks** = simultaneous playback (layered):

```
track1.add_clip( 0 , video_clip) # Background
track2.add_clip( 0 , logo_clip) # Overlay (on top)
```

### [ Z-Order](#z-order)

Later tracks render **on top** of earlier tracks:

```
timeline.add_track(background_track) # Bottom layer
timeline.add_track(overlay_track) # Renders above
timeline.add_track(caption_track) # Top layer
```

## [ Layer 4: Timeline](#layer-4-timeline)

Timeline is your final canvas and export settings.

```
from videodb.editor import Timeline

timeline = Timeline(conn)
timeline.resolution = "1280x720" # WIDTHxHEIGHT
timeline.background = "#000000" # Hex color

timeline.add_track(track)
stream_url = timeline.generate_stream()
```

**Common resolutions:**

- `"1280x720"` - 16:9 landscape (YouTube)
- `"608x1080"` - 9:16 vertical (TikTok, Reels)
- `"1080x1080"` - 1:1 square (Instagram)

## [ Common Patterns](#common-patterns)

### [ Highlight Reel from Search Results](#highlight-reel-from-search-results)

```
from videodb.editor import Timeline, Track, Clip, VideoAsset

# Search for moments
results = video.search( "key announcement" )

# Build highlight reel
timeline = Timeline(conn)
track = Track()
current_time = 0

for shot in results.shots[: 5 ]:
asset = VideoAsset( id = video.id, start = shot.start)
clip = Clip( asset = asset, duration = shot.end - shot.start)
track.add_clip(current_time, clip)
current_time += shot.end - shot.start

timeline.add_track(track)
highlights = timeline.generate_stream()
```

### [ Video with Logo Overlay](#video-with-logo-overlay)

```
from videodb.editor import Timeline, Track, Clip, VideoAsset, ImageAsset, Position

# Main video
video_asset = VideoAsset( id = video.id)
video_clip = Clip( asset = video_asset, duration = 30 )
video_track = Track()
video_track.add_clip( 0 , video_clip)

# Logo overlay
logo_asset = ImageAsset( id = logo.id)
logo_clip = Clip(
asset = logo_asset,
duration = 30 ,
position = Position.top_right,
scale = 0.2 ,
opacity = 0.8
)
logo_track = Track()
logo_track.add_clip( 0 , logo_clip)

# Combine (video first, logo on top)
timeline = Timeline(conn)
timeline.add_track(video_track)
timeline.add_track(logo_track)
output = timeline.generate_stream()
```

### [ Auto-Captioned Video](#auto-captioned-video)

```
from videodb.editor import Timeline, Track, Clip, VideoAsset, CaptionAsset

# Index speech first (required for auto-captions)
video.index_spoken_words()

# Video track
video_asset = VideoAsset( id = video.id)
video_clip = Clip( asset = video_asset, duration = 60 )
video_track = Track()
video_track.add_clip( 0 , video_clip)

# Caption track
caption_asset = CaptionAsset( src = "auto" , animation = "karaoke" )
caption_clip = Clip( asset = caption_asset, duration = 60 )
caption_track = Track()
caption_track.add_clip( 0 , caption_clip)

# Combine
timeline = Timeline(conn)
timeline.add_track(video_track)
timeline.add_track(caption_track)
output = timeline.generate_stream()
```

## [ What You Can Build](#what-you-can-build)

## TikTok Lyric Videos

Vertical videos with synced lyrics and AI backgrounds

## Faceless Video Creator

Complete AI-generated videos with scripts and voiceovers

## Intro &amp; Outro Automation

Add branded intros and outros to all videos automatically

## Brand Elements

Overlay logos, watermarks, and lower thirds programmatically

## [ Best Practices](#best-practices)

1. **Think in layers** - Background video first, overlays on top
2. **Use Asset.start for trimming** - Skip to the interesting part of source media
3. **Match clip durations** - Overlays should match or exceed video duration
4. **Test with generate\_stream()** - Preview before expensive exports
5. **Reuse assets** - One VideoAsset can be used in multiple clips

[Events &amp; Real-time](\pages\core-concepts\events-and-realtime) [Security &amp; Privacy](\pages\core-concepts\security-privacy)

⌘ I