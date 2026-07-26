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

- [Why Code-First Video Editing?](#why-code-first-video-editing)
- [The 4-Layer Architecture](#the-4-layer-architecture)
    - [Installing VideoDB in your environment](#installing-videodb-in-your-environment)
- [Layer 1: Assets - Your Raw Materials](#layer-1-assets-%E2%80%93-your-raw-materials)
    - [VideoAsset](#videoasset)
    - [AudioAsset](#audioasset)
    - [ImageAsset](#imageasset)
    - [TextAsset](#textasset)
    - [CaptionAsset](#captionasset)
    - [Supported Fonts for Text and Caption Assets](#supported-fonts-for-text-and-caption-assets)
- [Layer 2: Clips - The Presentation Engine](#layer-2-clips-%E2%80%93-the-presentation-engine)
    - [Duration - How Long It Plays](#duration-%E2%80%93-how-long-it-plays)
    - [Fit - How It Scales to Canvas](#fit-%E2%80%93-how-it-scales-to-canvas)
    - [Position - Where It Appears](#position-%E2%80%93-where-it-appears)
    - [Offset - For fine-tuned positioning](#offset-%E2%80%93-for-fine-tuned-positioning)
    - [Scale - Size Adjustment](#scale-%E2%80%93-size-adjustment)
    - [Opacity - Transparency](#opacity-%E2%80%93-transparency)
    - [Filter - Visual Effects](#filter-%E2%80%93-visual-effects)
    - [Transition](#transition)
- [Layer 3: Tracks - Sequencing and Layering](#layer-3-tracks-%E2%80%93-sequencing-and-layering)
    - [The Track Object](#the-track-object)
    - [Sequential Playback (Same Track)](#sequential-playback-same-track)
    - [Simultaneous Playback (Different Tracks)](#simultaneous-playback-different-tracks)
    - [Z-Order (Layering)](#z-order-layering)
    - [The "Double Start" Concept](#the-%E2%80%9Cdouble-start%E2%80%9D-concept)
- [Layer 4: Timeline - The Final Canvas](#layer-4-timeline-%E2%80%93-the-final-canvas)
    - [Resolution](#resolution)
    - [Background](#background)
    - [Adding Tracks](#adding-tracks)
    - [Rendering](#rendering)
    - [Complete example :](#complete-example-)
    - [Concept Guides (Detailed Explanations)](#concept-guides-detailed-explanations)
- [What You Can Build](#what-you-can-build)
- [Get Started](#get-started)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Programmable Editing](\pages\act\programmable-editing\timeline-architecture)

# Timeline Architecture

Copy page

Imagine building videos like coding - declarative, composable, and infinitely reusable. A comprehensive guide to VideoDB's code-first video editing architecture.

Copy page

VideoDB Editor lets you create videos programmatically using code instead of clicking timelines. You define what you want (assets, effects, timing), and the engine handles the rendering. This guide is your complete conceptual introduction. By the end, you'll understand how to compose anything from simple clips to complex multi-layer productions - all through code.

## [ Why Code-First Video Editing?](#why-code-first-video-editing)

Traditional video editors are built for one-off productions. But what if you need to:

- Generate 100 personalized videos from a template
- Build a TikTok content pipeline that runs daily
- Create video variations for A/B testing
- Automate highlight reels from live streams

**Code changes everything:**

- **Reusability** - One video asset, infinite variations
- **Scalability** - Loop over data to generate hundreds of videos
- **Version control** - Git-track your compositions
- **Automation** - Integrate with AI, databases, APIs

## [ The 4-Layer Architecture](#the-4-layer-architecture)

VideoDB Editor uses a hierarchy where each layer has one job. Understanding this structure is the key to mastering composition: **Asset → Clip → Track → Timeline**

Timeline architecture overview showing the 4-layer hierarchy: Asset, Clip, Track, and Timeline

<!-- image -->

Let's walk through each layer using the simplest possible example: **one video asset playing for 10 seconds** . This is the "Hello World" of Editor - understanding this foundation lets you build anything.

### [ Installing VideoDB in your environment](#installing-videodb-in-your-environment)

`VideoDB` is available as a [Python package](https://pypi.org/project/videodb) and [Node.js package](https://www.npmjs.com/package/videodb) .

Python

Node.js

```
pip install videodb
```

```
npm install videodb
```

## [ Layer 1: Assets - Your Raw Materials](#layer-1-assets-–-your-raw-materials)

**Assets are your content library.** They reference media that exists in your VideoDB collection but don't define how or when it plays.

### [ VideoAsset](#videoasset)

Your main video content. Each `VideoAsset` points to a video file via its ID. **Key parameters:**

- `id` (required) - The VideoDB media ID
- `start` (optional) - Trim point in seconds (e.g., `start=10` skips first 10s of source)
- `volume` (optional) - Audio level: `0.0` (muted) to `2.0` (200%), default `1.0`
- `crop` (optional) - Crop the sides of an asset by a relative amount. The size of the crop is specified using a scale between `0` and `1` . A left crop of `0.5` will crop half of the asset from the left, a top crop of `0.25` will crop the top by quarter of the asset.

Real example:

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip, VideoAsset

video_asset = VideoAsset(
# Create a VideoAsset pointing to a video file in your collection
id = video.id,
start = 0 ,
volume = 1
)
# Ready to use in a Clip
```

```
import { VideoAsset } from 'videodb' ;

const videoAsset = new VideoAsset ( video . id , {
// Create a VideoAsset pointing to a video file in your collection
start: 0 ,
volume: 1
});
// Ready to use in a Clip
```

This says: "Use the video from your VideoDB collection, start from the beginning ( `start=0` ), and keep original volume ( `volume=1` )." **Important distinction:** `VideoAsset.start` trims the *source file* . Where it appears on the timeline is controlled later at the Track layer. This "double start" concept is critical - we'll explore it more in Layer 3 (Tracks).

### [ AudioAsset](#audioasset)

Background music, voiceovers, or sound effects. Works exactly like `VideoAsset` . **Key parameters:**

- `id` (required) - The VideoDB audio file ID
- `start` (optional) - Same trim behavior as VideoAsset
- `volume` (optional) - `0.0` - `2.0` range (0.2 = 20% volume)

### [ ImageAsset](#imageasset)

Logos, watermarks, title cards, or static backgrounds. **Key parameters:**

- `id` (required) - The VideoDB image ID

Images are static by nature - duration, position, and size are controlled at the [Clip layer](\pages\act\programmable-editing\clip-parameters) .

### [ TextAsset](#textasset)

Custom text overlays with full typography control. **Key parameters:**

- `text` (required) - The string to display
- `font` (optional) - Font object with family, size, color, opacity
- `border` , `shadow` , `background` (optional) - Styling objects
- `alignment` (optional) - Position on screen
- `tabsize` (optional) - Tab size for text formatting
- `line_spacing` (optional) - Spacing between lines
- `width` (optional) - Width of text box in pixels
- `height` (optional) - Height of text box in pixels

**Color format:** ASS-style `&HAABBGGRR` in hex (e.g., `&H00FFFFFF` = white)

TextAsset example showing custom text overlays with typography control

<!-- image -->

### [ CaptionAsset](#captionasset)

Auto-generated subtitles synced to speech. **This is where VideoDB gets magical. Important:** `CaptionAsset` is a separate asset type from `TextAsset` . While `TextAsset` is for custom text overlays you write yourself, `CaptionAsset` automatically generates subtitles from video speech. **Key parameters:**

- `src` (required) - Set to `"auto"` to generate captions from video speech
- `animation` (optional) - How words appear: `reveal` , `karaoke` , `supersize` , `box_highlight` , `impact` , `color_highlight`
- `primary_color` , `secondary_color` (optional) - ASS-style colors
- `font` , positioning, border, shadow styling (optional)

**Critical requirement:** Before using `CaptionAsset(src="auto")` , you must call `video.index_spoken_words()` on the source video. This indexes the speech for auto-caption generation. Without it, captions won't generate.

CaptionAsset example showing auto-generated subtitles synced to speech with animation

<!-- image -->

### [ Supported Fonts for Text and Caption Assets](#supported-fonts-for-text-and-caption-assets)

Chart showing all supported fonts for text and caption assets

<!-- image -->

**Supported Indic fonts:**

- Noto Sans Kannada
- Noto Sans Devanagari
- Noto Sans Gujarati
- Noto Sans Gurmukhi

**Recap:** Assets answer "What content exists?" They don't yet define timing, size, position, or effects. That's the Clip layer's job.

## [ Layer 2: Clips - The Presentation Engine](#layer-2-clips-–-the-presentation-engine)

**Clips wrap Assets and define** ***how*** **and** ***how long*** **they appear.** This is your effects layer.

Clip layer showing how assets are wrapped with effects, positioning, and duration

<!-- image -->

Every Clip must have an `asset` and a `duration` . Everything else is optional.

### [ Duration - How Long It Plays](#duration-–-how-long-it-plays)

`duration` is a float in seconds. It defines how long the clip plays on the timeline. Real example:

Python

Node.js

```
from videodb import Clip
clip = Clip(
asset = video_asset,
duration = 10
)
```

```
import { Clip } from 'videodb' ;
const clip = new Clip ({
asset: videoAsset ,
duration: 10
});
```

"Play this VideoAsset for 10 seconds." **Key insight:** Duration is *independent* of the source file's length. If your source is 2 minutes but you set `duration=10` , only 10 seconds play (starting from `VideoAsset.start` ).

### [ Fit - How It Scales to Canvas](#fit-–-how-it-scales-to-canvas)

When your asset's aspect ratio doesn't match the timeline's, `fit` controls scaling behavior. **Four modes:**

- `Fit.crop` (most common) - Fills the canvas completely, cropping edges if needed
    - Use when: Filling the frame is priority, cropping is acceptable
    - Example: 16:9 video on a 9:16 (vertical) timeline
- `Fit.contain` - Fits the entire asset inside the canvas, adding bars if needed
    - Use when: Showing all content is priority, bars are acceptable
    - Example: Preserving widescreen footage in a square format
- `Fit.cover` - Stretches to fill canvas (distortion possible)
    - Use when: Artistic effect or abstract content
- `Fit.none` - Uses native pixel dimensions (no scaling)
    - Use when: Precise pixel control needed (e.g., 1:1 pixel mapping)

Real example:

Python

Node.js

```
clip = Clip(
asset = video_asset,
duration = 10 ,
fit = Fit.crop
)
```

```
import { Fit } from 'videodb' ;
const clip = new Clip ({
asset: videoAsset ,
duration: 10 ,
fit: Fit . crop
});
```

"Fill the canvas completely, crop edges if aspect ratios don't match."

### [ Position - Where It Appears](#position-–-where-it-appears)

Position uses a 9-zone grid system:

```
top_left      top        top_right
center_left   center     center_right
bottom_left   bottom     bottom_right
```

Position 9-zone grid system showing placement options for clips

<!-- image -->

Real example:

Python

Node.js

```
logo_clip = Clip(
asset = logo,
duration = 30 ,
position = Position.top_right
)
```

```
import { Position } from 'videodb' ;
const logoClip = new Clip ({
asset: logo ,
duration: 30 ,
position: Position . topRight
});
```

"Place the logo in the top-right corner."

### [* Offset - For fine-tuned positioning*](#offset-–-for-fine-tuned-positioning)

Python

Node.js

```
from videodb.editor import Offset

clip = Clip(
asset = logo,
duration = 30 ,
position = Position.center,
offset = Offset( x = 0.3 , y =- 0.2 )
)
```

```
import { Offset } from 'videodb' ;

const clip = new Clip ({
asset: logo ,
duration: 30 ,
position: Position . center ,
offset: new Offset ({ x: 0.3 , y: - 0.2 })
});
```

This shifts the logo 30% right, 20% up from center.

Offset fine-tuning positioning with x and y adjustments

<!-- image -->

### [ Scale - Size Adjustment](#scale-–-size-adjustment)

`scale` is a multiplier applied *after* fit. Default is `1.0` . Real example:

Python

Node.js

```
pip_clip = Clip(
asset = overlay_video,
duration = 15 ,
scale = 0.3
)
```

```
const pipClip = new Clip ({
asset: overlayVideo ,
duration: 15 ,
scale: 0.3
});
```

"Shrink this video to 30% of its fitted size" (perfect for picture-in-picture).

### [ Opacity - Transparency](#opacity-–-transparency)

`opacity` ranges from `0.0` (invisible) to `1.0` (opaque). Real example:

Python

Node.js

```
watermark_clip = Clip(
asset = logo,
duration = 30 ,
opacity = 0.6
)
```

```
const watermarkClip = new Clip ({
asset: logo ,
duration: 30 ,
opacity: 0.6
});
```

"Make the logo 60% opaque (semi-transparent)."

### [ Filter - Visual Effects](#filter-–-visual-effects)

Apply color/blur effects:

Python

Node.js

```
from videodb.editor import Filter

clip = Clip(
asset = VideoAsset( id = video.id),
duration = 10 ,
filter = Filter.greyscale
)
```

```
import { Filter } from 'videodb' ;

const clip = new Clip ({
asset: new VideoAsset ( video . id ),
duration: 10 ,
filter: Filter . greyscale
});
```

Available filters: `greyscale` , `blur` , `boost` (saturation), `contrast` , `darken` , `lighten` , `muted` , `negative` .

| Filter             | Effect                                                     |
|--------------------|------------------------------------------------------------|
| `Filter.greyscale` | Removes all color, creating a black-and-white look         |
| `Filter.blur`      | Blurs the scene for artistic or privacy effects            |
| `Filter.contrast`  | Increases contrast, making darks darker and lights lighter |
| `Filter.darken`    | Darkens the entire scene                                   |
| `Filter.lighten`   | Lightens the entire scene                                  |
| `Filter.boost`     | Boosts both contrast and saturation for vibrant colors     |
| `Filter.muted`     | Reduces saturation and contrast for a subdued look         |
| `Filter.negative`  | Inverts colors for a surreal, negative effect              |

### [ Transition](#transition)

Apply a transition effect at the start ( `in_` ) and/or end ( `out` ) of a clip:

Python

Node.js

```
from videodb.editor import Transition

clip = Clip(
asset = VideoAsset( id = video.id),
duration = 10 ,
transition = Transition(
in_ = "fade" ,
out = "fade" ,
duration = 2
)
)
```

```
import { Transition } from 'videodb' ;

const clip = new Clip ({
asset: new VideoAsset ( video . id ),
duration: 10 ,
transition: new Transition ({
in: "fade" ,
out: "fade" ,
duration: 2
})
});
```

**Available transition types:**

| Value                  | Description                      |
|------------------------|----------------------------------|
| `fade`                 | Fade to/from black               |
| `reveal`               | Slide reveal from edge           |
| `shuffle`              | Shuffle from center              |
| `shuffle_top_right`    | Shuffle from top-right corner    |
| `shuffle_bottom_right` | Shuffle from bottom-right corner |
| `shuffle_bottom_left`  | Shuffle from bottom-left corner  |
| `shuffle_top_left`     | Shuffle from top-left corner     |

**Recap:** A Clip wraps an Asset and defines *how long* it plays ( `duration` ) and *how* it appears (fit, position, scale, opacity, filter, transition). Now let's see how to place clips on the timeline.

## [ Layer 3: Tracks - Sequencing and Layering](#layer-3-tracks-–-sequencing-and-layering)

**Tracks are timeline lanes.** They control *when* clips play and *how* they stack.

Track layer showing timeline lanes for sequencing and layering clips

<!-- image -->

### [ The Track Object](#the-track-object)

A Track is a container you add clips to:

Python

Node.js

```
from videodb import Track

track = Track()
track.add_clip( 0 , clip) # Add clip at 0 seconds
```

```
import { Track } from 'videodb' ;

const track = new Track ();
track . addClip ( 0 , clip ); // Add clip at 0 seconds
```

`track.add_clip(start, clip)` has two parameters:

- `start` (float, seconds) - When the clip begins on the timeline
- `clip` (Clip object) - The clip to add

### [ Sequential Playback (Same Track)](#sequential-playback-same-track)

Clips on the *same track* play **one after another** :

Python

Node.js

```
track = Track()
track.add_clip( 0 , clip1) # 0s-5s
track.add_clip( 5 , clip2) # 5s-10s
track.add_clip( 10 , clip3) # 10s-15s
```

```
const track = new Track ();
track . addClip ( 0 , clip1 ); // 0s-5s
track . addClip ( 5 , clip2 ); // 5s-10s
track . addClip ( 10 , clip3 ); // 10s-15s
```

This creates a montage - three clips in sequence.

### [ Simultaneous Playback (Different Tracks)](#simultaneous-playback-different-tracks)

Clips on *different tracks* at the same timestamp play **simultaneously** :

Simultaneous playback showing clips on different tracks playing at the same time

<!-- image -->

Python

Node.js

```
track1 = Track()
track1.add_clip( 0 , clip1) # First layer

track2 = Track()
track2.add_clip( 0 , clip2) # Second layer (plays at same time)
```

```
const track1 = new Track ();
track1 . addClip ( 0 , clip1 ); // First layer

const track2 = new Track ();
track2 . addClip ( 0 , clip2 ); // Second layer (plays at same time)
```

Both start at 0 seconds, so they play together. This is how you create layered compositions.

### [ Z-Order (Layering)](#z-order-layering)

**Later tracks render** ***on top*** **of earlier tracks.**

Z-order layering showing tracks rendered on top of each other

<!-- image -->

Python

Node.js

```
timeline.add_track(track1) # Bottom layer
timeline.add_track(track2) # Renders above track1
timeline.add_track(track3) # Renders above track2
```

```
timeline . addTrack ( track1 ); // Bottom layer
timeline . addTrack ( track2 ); // Renders above track1
timeline . addTrack ( track3 ); // Renders above track2
```

This is how you create overlays: put background content on track1, overlays on track2.

### [ The "Double Start" Concept](#the-“double-start”-concept)

There are **two separate "start" parameters** :

- `Asset.start` - Trims the *source file*
- `track.add_clip(start=...)` - Places clip on the *timeline*

Real example:

Python

Node.js

```
# Source video is 2 minutes long

video_asset = VideoAsset(
id = video.id,
start = 30
) # Skip first 30s of source

clip = Clip(
asset = video_asset,
duration = 40
) # Use 40s (from 0:30 to 1:10 of source)

track = Track()
track.add_clip( 5 , clip) # Place it at 5-second mark on timeline
```

```
// Source video is 2 minutes long

const videoAsset = new VideoAsset ( video . id , {
start: 30
}); // Skip first 30s of source

const clip = new Clip ({
asset: videoAsset ,
duration: 40
}); // Use 40s (from 0:30 to 1:10 of source)

const track = new Track ();
track . addClip ( 5 , clip ); // Place it at 5-second mark on timeline
```

Result: The timeline plays seconds 0:30-01:10 of the source video, but it appears at the 5-second mark of the final output. **Why this matters:** You can extract any segment from source media and place it anywhere on the timeline, independently. *For multi-track layering examples (video + music + captions + overlays), see the Advanced Clip Control guide and creative tutorials.*

## [ Layer 4: Timeline - The Final Canvas](#layer-4-timeline-–-the-final-canvas)

**Timeline is your export settings.** It defines resolution, background color, and combines all tracks.

Timeline layer showing the final canvas combining all tracks and export settings

<!-- image -->

Python

Node.js

```
from videodb.editor import Timeline

timeline = Timeline(conn) # conn is your VideoDB connection
timeline.background = "#808080" # Grey background (hex color)
timeline.resolution = "600x1060" # Custom resolution
```

```
import { Timeline } from 'videodb' ;

const timeline = new Timeline ( conn ); // conn is your VideoDB connection
timeline . background = "#808080" ; // Grey background (hex color)
timeline . resolution = "600x1060" ; // Custom resolution
```

### [ Resolution](#resolution)

Format: `"WIDTHxHEIGHT"` Common presets:

- `"1280x720"` - 16:9 horizontal (YouTube, landscape)
- `"608x1080"` - 9:16 vertical (TikTok, Shorts, Reels)
- `"1080x1080"` - 1:1 square (Instagram feed)
- `"600x1060"` - Custom dimensions

### [ Background](#background)

The color shown behind/around clips when they don't fill the canvas (e.g., when using `Fit.contain` ). Format: hex color string.

Background color shown behind clips when they don't fill the entire canvas

<!-- image -->

### [ Adding Tracks](#adding-tracks)

Python

Node.js

```
timeline.add_track(track)
```

```
timeline . addTrack ( track );
```

For multiple tracks, order matters - this sets the z-order (layering). Later tracks render on top.

### [ Rendering](#rendering)

Python

Node.js

```
stream_url = timeline.generate_stream()
print (stream_url)
```

```
const streamUrl = await timeline . generateStream ();
console . log ( streamUrl );
```

This sends your composition to VideoDB's rendering engine and returns a playable stream URL.

### [ Complete example :](#complete-example-)

Complete timeline example showing all layers working together

<!-- image -->

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip, VideoAsset

# Create timeline
timeline = Timeline(conn)
timeline.background = "#FFA629"
timeline.resolution = "600x1060"

# Create asset
video_asset = VideoAsset( id = video.id, start = 0 , volume = 1 )

# Wrap in clip
clip = Clip( asset = video_asset, duration = 10 )

# Add to track
track = Track()
track.add_clip( 0 , clip)

# Add track to timeline
timeline.add_track(track)

# Render
stream_url = timeline.generate_stream()
```

```
import { Timeline , Track , Clip , VideoAsset } from 'videodb' ;

// Create timeline
const timeline = new Timeline ( conn );
timeline . background = "#FFA629" ;
timeline . resolution = "600x1060" ;

// Create asset
const videoAsset = new VideoAsset ( video . id , { start: 0 , volume: 1 });

// Wrap in clip
const clip = new Clip ({ asset: videoAsset , duration: 10 });

// Add to track
const track = new Track ();
track . addClip ( 0 , clip );

// Add track to timeline
timeline . addTrack ( track );

// Render
const streamUrl = await timeline . generateStream ();
```

You've just composed your first video programmatically: one video asset playing for 10 seconds. This simple pattern scales to any complexity - just add more assets, clips, and tracks.

### [ Concept Guides (Detailed Explanations)](#concept-guides-detailed-explanations)

These guides expand on specific concepts with design principles, edge cases, and best practices:

## Fit and Position

Deep dive into aspect ratios, 9-zone positioning, offset mechanics, and framing patterns

## Trimming vs Timing

Complete explanation of the "double start" concept with formulas and multi-clip workflows

## Caption Asset

Animation styles, ASS color format, positioning, accessibility, and styling best practices

## Clip Parameters

Filters, transitions, opacity patterns, and complex multi-layer compositions

## [ What You Can Build](#what-you-can-build)

See real-world applications of timeline composition and programmatic video creation:

## TikTok Lyric Videos

Transform music into viral vertical clips with AI backgrounds and synced lyrics

## Video Statistics Recaps

Turn analytics into cinematic recaps with dynamic animations

## Faceless Video Creator

Build complete faceless videos with AI scripts and voiceovers

## Chess Match Montages

Automatically extract highlights with AI move detection

## [ Get Started](#get-started)

## Timeline Basics

See all concepts in action with hands-on examples and interactive code.

[Latency and Cost](\pages\understand\quality-and-evaluation\latency-and-cost) [Aspect Ratio Control](\pages\act\programmable-editing\aspect-ratio-control)

⌘ I