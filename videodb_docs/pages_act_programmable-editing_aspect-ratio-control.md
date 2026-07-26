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

- [Fit Modes](#fit-modes)
    - [Fit.crop (default)](#fit-crop-default)
    - [Fit.contain](#fit-contain)
    - [Fit.cover](#fit-cover)
    - [Fit.none](#fit-none)
    - [Code Example](#code-example)
- [Position](#position)
    - [Code Example](#code-example-2)
- [Offset](#offset)
    - [Code Example](#code-example-3)
- [Parameter Reference](#parameter-reference)
- [What You Can Build](#what-you-can-build)
- [Next Steps](#next-steps)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Programmable Editing](\pages\act\programmable-editing\timeline-architecture)

# Aspect Ratio Control

Copy page

Control how assets scale when dimensions don't match the timeline. The fit parameter handles the mismatch (crop, letterbox, stretch), while position and offset control placement.

Copy page

Open In Colab

<!-- image -->

## [ Fit Modes](#fit-modes)

The fit parameter determines how an asset scales to match the timeline resolution.

### [ Fit.crop (default)](#fit-crop-default)

- Scales asset to fill viewport while maintaining aspect ratio
- Edges are cropped if aspect ratios differ

This is the default because it creates clean, full-frame compositions without black bars. The tradeoff is you might lose some content at the edges, but everything stays proportional and the frame stays filled.

### [ Fit.contain](#fit-contain)

- Scales asset to fit entirely within viewport while maintaining aspect ratio
- May add letterboxing (black bars) if aspect ratios differ

Use this when you need to guarantee that all of your content is visible, even if it means having black bars on the sides or top and bottom. Nothing gets cropped, but you sacrifice the full-frame look.

### [ Fit.cover](#fit-cover)

- Stretches asset to fill viewport, ignoring aspect ratio
- May cause distortion

This mode stretches the content to fill the frame regardless of proportions. You'll rarely need this unless you specifically want the stretched effect, or you're working with content that already matches your timeline's aspect ratio exactly.

### [ Fit.none](#fit-none)

- Preserves original pixel dimensions
- No scaling applied

This keeps your asset at its exact original size, which is useful for things like logos, overlays, or picture-in-picture effects where you want pixel-perfect control. The content appears at its native resolution regardless of timeline size.

### [ Code Example](#code-example)

Python

Node.js

```
from videodb.editor import Fit

clip = Clip(
asset = VideoAsset( id = video.id),
duration = 10 ,
fit = Fit.crop # or Fit.contain, Fit.cover, Fit.none
)
```

```
import { Fit , Clip , VideoAsset } from 'videodb' ;

const clip = new Clip ({
asset: new VideoAsset ( video . id ),
duration: 10 ,
fit: Fit . crop // or Fit.contain, Fit.cover, Fit.none
});
```

Note: You can also use fit=None (Python None) which is equivalent to `Fit.none` .

## [ Position](#position)

The position parameter places the asset in one of 9 preset zones on the viewport. Think of your screen divided into a 3x3 grid - you can anchor your content to any of these zones, from corners to edges to dead center.

```
Position.top_left      Position.top        Position.top_right
Position.left          Position.center     Position.right
Position.bottom_left   Position.bottom     Position.bottom_right
```

**Example with** **`Position.left`**

### [ Code Example](#code-example-2)

Python

Node.js

```
from videodb.editor import Position

clip = Clip(
asset = VideoAsset( id = video.id),
duration = 10 ,
position = Position.top_left,
fit = None
)
```

```
import { Position , Clip , VideoAsset } from 'videodb' ;

const clip = new Clip ({
asset: new VideoAsset ( video . id ),
duration: 10 ,
position: Position . topLeft ,
fit: null
});
```

## [ Offset](#offset)

The offset parameter provides fine-grained position control using relative coordinates. Sometimes the 9 preset zones aren't quite right - maybe you want something centered but nudged slightly to the left, or positioned with a specific margin. That's where offset comes in, letting you tweak positions with precision. **Example** **`Offset(x=-0.25)`**

### [ Code Example](#code-example-3)

Python

Node.js

```
from videodb.editor import Offset

clip = Clip(
asset = VideoAsset( id = video.id),
duration = 10 ,
position = Position.center,
offset = Offset( x = 0.15 , y = 0.1 ) # x: horizontal, y: vertical
)
```

```
import { Offset , Clip , VideoAsset , Position } from 'videodb' ;

const clip = new Clip ({
asset: new VideoAsset ( video . id ),
duration: 10 ,
position: Position . center ,
offset: new Offset ({ x: 0.15 , y: 0.1 }) // x: horizontal, y: vertical
});
```

Coordinate System:

- `x` : Horizontal shift ( `-1.0` to `1.0` )
    - Positive values move right
    - Negative values move left
- `y` : Vertical shift ( `-1.0` to `1.0` )
    - Positive values move down
    - Negative values move up
- Values are relative to viewport dimensions

Example: `offset=Offset(x=0.1, y=0)` on a 1080px wide viewport moves the clip 108px to the right.

## [ Parameter Reference](#parameter-reference)

| Parameter   | Type     | Description                                                              |
|-------------|----------|--------------------------------------------------------------------------|
| fit         | Fit      | Scaling behavior: `Fit.crop` , `Fit.contain` , `Fit.cover` , `Fit.none`  |
| position    | Position | Anchor point: `Position.top_left` , `Position.center` , etc. (9 options) |
| offset      | Offset   | Fine-tuning position with `x` / `y` coordinates                          |

Python

Node.js

```
from videodb.editor import Clip, VideoAsset, Fit, Position, Offset

clip = Clip(
asset = VideoAsset( id = video.id),
duration = 10 ,
fit = Fit.crop,
position = Position.right,
offset = Offset( x =- 0.1 , y = 0 )
)
```

```
import { Clip , VideoAsset , Fit , Position , Offset } from 'videodb' ;

const clip = new Clip ({
asset: new VideoAsset ( video . id ),
duration: 10 ,
fit: Fit . crop ,
position: Position . right ,
offset: new Offset ({ x: - 0.1 , y: 0 })
});
```

## [ What You Can Build](#what-you-can-build)

## TikTok Lyric Videos

Create vertical 9:16 videos optimized for TikTok and Reels

## Brand Elements

Position logos and overlays precisely using fit and offset

## Faceless Video Creator

Control aspect ratios for multi-platform content

## [ Next Steps](#next-steps)

## Fit, Position &amp; Aspect Ratios

Hands-on experimentation with all fit modes, 9-zone positioning, and aspect ratio handling.

[Timeline Architecture](\pages\act\programmable-editing\timeline-architecture) [Trimming Vs Timing](\pages\act\programmable-editing\trimming-vs-timing)

⌘ I