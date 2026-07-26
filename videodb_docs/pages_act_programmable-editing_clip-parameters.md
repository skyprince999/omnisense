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

- [Editor Architecture](#editor-architecture)
- [Clip Parameters](#clip-parameters)
    - [Core Parameters](#core-parameters)
    - [Geometry Parameters](#geometry-parameters)
    - [Visual Effect Parameters](#visual-effect-parameters)
- [Scale Parameter](#scale-parameter)
- [Opacity Parameter](#opacity-parameter)
- [Filter Parameter](#filter-parameter)
- [Transition Parameter](#transition-parameter)
- [Complete Example](#complete-example)
- [Parameter Reference](#parameter-reference)
- [What You Can Build](#what-you-can-build)
- [Next Steps](#next-steps)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Programmable Editing](\pages\act\programmable-editing\timeline-architecture)

# Clip Parameters

Copy page

The Clip object wraps an Asset and controls how it appears on screen. Complete reference for duration, geometry, visual effects, filters, transitions, and layering.

Copy page

The Clip object wraps an Asset and controls how it appears on screen. Think of the Asset as your raw content (the video file, image, or text), and the Clip as all the presentation decisions - where it appears, how big it is, what color effects it has, how it fades in and out. This guide documents all available Clip parameters and their interactions.

## [ Editor Architecture](#editor-architecture)

Asset → Clip → Track → Timeline

- Asset: Raw content (what to show)
- Clip: Presentation control (how to show it)
- Track: Layering container (for stacking multiple clips)
- Timeline: Final composition (the output video)

This separation lets you reuse the same asset in multiple clips with different visual treatments - same video, but one clip shows it full-screen while another shows it as a small picture-in-picture overlay.

## [ Clip Parameters](#clip-parameters)

### [ Core Parameters](#core-parameters)

| Parameter   | Type   | Description                                                                                          |
|-------------|--------|------------------------------------------------------------------------------------------------------|
| asset       | Asset  | The content to display ( `VideoAsset` , `ImageAsset` , `AudioAsset` , `TextAsset` , `CaptionAsset` ) |
| duration    | float  | Clip length in seconds                                                                               |

### [ Geometry Parameters](#geometry-parameters)

| Parameter   | Type     | Description                                                             |
|-------------|----------|-------------------------------------------------------------------------|
| fit         | Fit      | Scaling behavior: `Fit.crop` , `Fit.contain` , `Fit.cover` , `Fit.none` |
| position    | Position | Anchor point (9 zones: `top_left` , `center` , `bottom_right` , etc.)   |
| offset      | Offset   | Fine-tune position with `x` / `y` coordinates                           |
| scale       | float    | Size multiplier ( `0.0` to `10.0` , default: `1.0` )                    |

### [ Visual Effect Parameters](#visual-effect-parameters)

| Parameter   | Type       | Description                                                 |
|-------------|------------|-------------------------------------------------------------|
| filter      | Filter     | Color treatment ( `greyscale` , `blur` , `contrast` , etc.) |
| opacity     | float      | Transparency ( `0.0` = invisible, `1.0` = opaque)           |
| transition  | Transition | Fade `in_` / `out` effects                                  |

## [ Scale Parameter](#scale-parameter)

The scale parameter is a size multiplier applied after fit mode. First, the fit mode handles the aspect ratio and scales your content to match the timeline, then scale multiplies that result. This is useful for creating picture-in-picture effects (scale=0.3 for a tiny corner video) or zoom effects (scale=1.5 to enlarge).

Python

Node.js

```
from videodb.editor import Clip, VideoAsset, Position

clip = Clip(
asset = VideoAsset( id = video.id),
duration = 10 ,
scale = 0.5 , # 50% of original size
position = Position.top_left
)
```

```
import { Clip , EditorVideoAsset , Position } from 'videodb' ;

const clip = new Clip ({
asset: new EditorVideoAsset ({ id: video . id }),
duration: 10 ,
scale: 0.5 , // 50% of original size
position: Position . topLeft
});
```

Range: `0.0` to `10.0` (default: `1.0` ) Example with `scale=0.5` and `Position.top_left`

## [ Opacity Parameter](#opacity-parameter)

The opacity parameter controls transparency, letting you create semi-transparent overlays, subtle watermarks, or fade effects. At `1.0` your clip is fully solid, at `0.5` it's half-transparent, and at `0.0` it's completely invisible.

Python

Node.js

```
from videodb.editor import Clip, VideoAsset

clip = Clip(
asset = VideoAsset( id = video.id),
duration = 10 ,
opacity = 0.5 # 50% transparent
)
```

```
import { Clip , EditorVideoAsset } from 'videodb' ;

const clip = new Clip ({
asset: new EditorVideoAsset ({ id: video . id }),
duration: 10 ,
opacity: 0.5 // 50% transparent
});
```

Range: `0.0` (invisible) to `1.0` (opaque) Example with `opacity=0.3`

## [ Filter Parameter](#filter-parameter)

The filter parameter applies color and visual treatments to your clip. These are global effects that change the entire clip's appearance - you can make it black and white, blur it for backgrounds, adjust contrast, or create stylistic looks. Each clip can have one filter applied.

Python

Node.js

```
Filter.greyscale # Remove color (black and white)
Filter.blur # Blur the video
Filter.contrast # Increase contrast
Filter.boost # Boost contrast and saturation
Filter.muted # Reduce saturation and contrast
Filter.darken # Darken the scene
Filter.lighten # Lighten the scene
Filter.negative # Invert colors
```

```
Filter . greyscale // Remove color (black and white)
Filter . blur // Blur the video
Filter . contrast // Increase contrast
Filter . boost // Boost contrast and saturation
Filter . muted // Reduce saturation and contrast
Filter . darken // Darken the scene
Filter . lighten // Lighten the scene
Filter . negative // Invert colors
```

Python

Node.js

```
from videodb.editor import Clip, VideoAsset, Filter

clip = Clip(
asset = VideoAsset( id = video.id),
duration = 10 ,
filter = Filter.greyscale
)
```

```
import { Clip , EditorVideoAsset , Filter } from 'videodb' ;

const clip = new Clip ({
asset: new EditorVideoAsset ({ id: video . id }),
duration: 10 ,
filter: Filter . greyscale
});
```

Example with `Filter.greyscale`

## [ Transition Parameter](#transition-parameter)

The transition parameter controls fade in/out effects, making your clips appear and disappear smoothly instead of cutting abruptly. The fade happens over the first and last N seconds of your clip - so a 2-second fade means the first 2 seconds gradually appear, and the last 2 seconds gradually disappear.

Python

Node.js

```
from videodb.editor import Clip, VideoAsset, Transition

clip = Clip(
asset = VideoAsset( id = video.id),
duration = 10 ,
transition = Transition(
in_ = "fade" , # Fade in effect (note the underscore)
out = "fade" , # Fade out effect
duration = 2 # Transition duration in seconds
)
)
```

```
import { Clip , EditorVideoAsset , Transition } from 'videodb' ;

const clip = new Clip ({
asset: new EditorVideoAsset ({ id: video . id }),
duration: 10 ,
transition: new Transition ({
in: "fade" , // Fade in effect
out: "fade" , // Fade out effect
duration: 2 // Transition duration in seconds
})
});
```

Example:

Parameters:

- `in_` : Transition type for entry (use `in_` with underscore because `in` is a Python keyword)
- `out` : Transition type for exit
- `duration` : Length of transition in seconds

## [ Complete Example](#complete-example)

Here's a clip using multiple parameters:

Python

Node.js

```
from videodb.editor import Clip, VideoAsset, Position, Filter, Transition

clip = Clip(
asset = VideoAsset( id = video.id),
duration = 10 ,
position = Position.bottom_left,
scale = 0.7 ,
opacity = 0.3 ,
filter = Filter.greyscale,
transition = Transition( in_ = "fade" , out = "fade" , duration = 3 ),
fit = None
)
```

```
import { Clip , EditorVideoAsset , Position , Filter , Transition , Fit } from 'videodb' ;

const clip = new Clip ({
asset: new EditorVideoAsset ({ id: video . id }),
duration: 10 ,
position: Position . bottomLeft ,
scale: 0.7 ,
opacity: 0.3 ,
filter: Filter . greyscale ,
transition: new Transition ({ in: "fade" , out: "fade" , duration: 3 }),
fit: Fit . none
});
```

## [ Parameter Reference](#parameter-reference)

| Parameter   | Type       | Default   | Description                        |
|-------------|------------|-----------|------------------------------------|
| asset       | Asset      | Required  | Content to display                 |
| duration    | float      | Required  | Clip length in seconds             |
| fit         | Fit        | Fit.crop  | Scaling mode                       |
| position    | Position   | None      | Anchor point (9 zones)             |
| offset      | Offset     | None      | Fine position adjustment           |
| scale       | float      | 1.0       | Size multiplier ( `0.0` - `10.0` ) |
| opacity     | float      | 1.0       | Transparency ( `0.0` - `1.0` )     |
| filter      | Filter     | None      | Color treatment                    |
| transition  | Transition | None      | Fade effects                       |

## [ What You Can Build](#what-you-can-build)

## Intro &amp; Outro Automation

Use clip positioning and transitions for seamless brand intros

## Brand Elements

Overlay logos and watermarks with opacity and positioning

## TikTok Lyric Videos

Combine clips with text overlays and visual effects

## Faceless Video Creator

Layer multiple clips with filters and transitions

## [ Next Steps](#next-steps)

## Clip Control Layer

Hands-on experimentation with all Clip parameters, effects, and transitions.

[Trimming Vs Timing](\pages\act\programmable-editing\trimming-vs-timing) [Caption Asset](\pages\act\programmable-editing\caption-asset)

⌘ I