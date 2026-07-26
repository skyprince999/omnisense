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

- [Quick Example](#quick-example)
- [TextAsset Parameters](#textasset-parameters)
- [Font](#font)
- [Background](#background)
- [Alignment](#alignment)
- [Complete Example](#complete-example)
- [Next Steps](#next-steps)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Programmable Editing](\pages\act\programmable-editing\timeline-architecture)

# Text Asset

Copy page

Overlay text elements on videos with customizable fonts, colors, and positioning

Copy page

## [ Quick Example](#quick-example)

Python

Node.js

```
from videodb.editor import (
TextAsset, Font, Background,
Alignment, HorizontalAlignment, VerticalAlignment, TextAlignment
)

text_asset = TextAsset(
text = "BREAKING NEWS" ,
font = Font( family = "Inter" , size = 48 , color = "#FFFFFF" ),
background = Background(
color = "#FF0000" ,
width = 400 ,
height = 80 ,
text_alignment = TextAlignment.center
),
alignment = Alignment(
horizontal = HorizontalAlignment.center,
vertical = VerticalAlignment.center
)
)
```

```
import {
TextAsset , Font , Background ,
Alignment , HorizontalAlignment , VerticalAlignment , TextAlignment
} from 'videodb' ;

const textAsset = new TextAsset ({
text: "BREAKING NEWS" ,
font: new Font ({ family: "Inter" , size: 48 , color: "#FFFFFF" }),
background: new Background ({
color: "#FF0000" ,
width: 400 ,
height: 80 ,
textAlignment: TextAlignment . center
}),
alignment: new Alignment ({
horizontal: HorizontalAlignment . center ,
vertical: VerticalAlignment . center
})
});
```

## [ TextAsset Parameters](#textasset-parameters)

| Parameter      | Type       | Description                                 |
|----------------|------------|---------------------------------------------|
| `text`         | str        | The text to display                         |
| `font`         | Font       | Font styling (family, size, color, opacity) |
| `background`   | Background | Background box styling                      |
| `alignment`    | Alignment  | Position on screen                          |
| `border`       | Border     | Border styling                              |
| `shadow`       | Shadow     | Shadow styling                              |
| `tabsize`      | int        | Tab size for text formatting                |
| `line_spacing` | float      | Spacing between lines                       |
| `width`        | int        | Width of text box in pixels                 |
| `height`       | int        | Height of text box in pixels                |

## [ Font](#font)

Controls text appearance.

| Parameter   | Type   | Default     | Description               |
|-------------|--------|-------------|---------------------------|
| `family`    | str    | `"Sans"`    | Font family name          |
| `size`      | int    | `24`        | Font size in pixels       |
| `color`     | str    | `"#000000"` | Text color (hex)          |
| `opacity`   | float  | `1.0`       | Text opacity (0.0 to 1.0) |

Python

Node.js

```
from videodb.editor import Font

font = Font(
family = "Inter" ,
size = 56 ,
color = "#FFFFFF"
)
```

```
const font = new Font ({
family: "Inter" ,
size: 56 ,
color: "#FFFFFF"
});
```

**Supported fonts:** Sans, Inter, Roboto, Open Sans, Lato, Montserrat, Oswald, Raleway, Poppins, Ubuntu, Clear Sans, Arial, Times New Roman, Courier New, Georgia, Verdana

## [ Background](#background)

Controls the background box behind text.

| Parameter        | Type          | Default     | Description                     |
|------------------|---------------|-------------|---------------------------------|
| `color`          | str           | `"#FFFFFF"` | Background color (hex)          |
| `opacity`        | float         | `1.0`       | Background opacity (0.0 to 1.0) |
| `width`          | int           | auto        | Box width in pixels             |
| `height`         | int           | auto        | Box height in pixels            |
| `border_width`   | float         | `0`         | Border thickness                |
| `text_alignment` | TextAlignment | center      | Text alignment within box       |

Python

Node.js

```
from videodb.editor import Background, TextAlignment

background = Background(
color = "#000000" ,
width = 600 ,
height = 120 ,
border_width = 2.0 ,
text_alignment = TextAlignment.center
)
```

```
const background = new Background ({
color: "#000000" ,
width: 600 ,
height: 120 ,
borderWidth: 2.0 ,
textAlignment: TextAlignment . center
});
```

## [ Alignment](#alignment)

Controls where the text appears on screen.

| Parameter    | Type                | Description                 |
|--------------|---------------------|-----------------------------|
| `horizontal` | HorizontalAlignment | `left` , `center` , `right` |
| `vertical`   | VerticalAlignment   | `top` , `center` , `bottom` |

Python

Node.js

```
from videodb.editor import Alignment, HorizontalAlignment, VerticalAlignment

# Center of screen
alignment = Alignment(
horizontal = HorizontalAlignment.center,
vertical = VerticalAlignment.center
)

# Bottom-left corner
alignment = Alignment(
horizontal = HorizontalAlignment.left,
vertical = VerticalAlignment.bottom
)
```

```
// Center of screen
const alignment = new Alignment ({
horizontal: HorizontalAlignment . center ,
vertical: VerticalAlignment . center
});

// Bottom-left corner
const alignment = new Alignment ({
horizontal: HorizontalAlignment . left ,
vertical: VerticalAlignment . bottom
});
```

## [ Complete Example](#complete-example)

Python

Node.js

```
from videodb.editor import (
Timeline, Track, Clip, VideoAsset, TextAsset,
Font, Background, Alignment,
HorizontalAlignment, VerticalAlignment, TextAlignment
)

# Create text asset
intro_text = TextAsset(
text = "Let the Match Begin" ,
font = Font( family = "Clear Sans" , size = 56 , color = "#FFFFFF" ),
background = Background(
width = 600 ,
height = 120 ,
color = "#000000" ,
border_width = 2.0 ,
text_alignment = TextAlignment.center
),
alignment = Alignment(
horizontal = HorizontalAlignment.center,
vertical = VerticalAlignment.center
)
)

# Add to timeline
timeline = Timeline(conn)

video_clip = Clip( asset = VideoAsset( asset_id = video.id), duration = 30 )
text_clip = Clip( asset = intro_text, duration = 5 )

video_track = Track()
video_track.add_clip( clip = video_clip, start = 0 )

text_track = Track()
text_track.add_clip( clip = text_clip, start = 0 )

timeline.add_track(video_track)
timeline.add_track(text_track)

stream_url = timeline.generate_stream()
```

```
import {
Timeline , Track , Clip , VideoAsset , TextAsset ,
Font , Background , Alignment ,
HorizontalAlignment , VerticalAlignment , TextAlignment
} from 'videodb' ;

// Create text asset
const introText = new TextAsset ({
text: "Let the Match Begin" ,
font: new Font ({ family: "Clear Sans" , size: 56 , color: "#FFFFFF" }),
background: new Background ({
width: 600 ,
height: 120 ,
color: "#000000" ,
borderWidth: 2.0 ,
textAlignment: TextAlignment . center
}),
alignment: new Alignment ({
horizontal: HorizontalAlignment . center ,
vertical: VerticalAlignment . center
})
});

// Add to timeline
const timeline = new Timeline ( conn );

const videoClip = new Clip ({ asset: new VideoAsset ({ assetId: video . id }), duration: 30 });
const textClip = new Clip ({ asset: introText , duration: 5 });

const videoTrack = new Track ();
videoTrack . addClip ({ clip: videoClip , start: 0 });

const textTrack = new Track ();
textTrack . addClip ({ clip: textClip , start: 0 });

timeline . addTrack ( videoTrack );
timeline . addTrack ( textTrack );

const streamUrl = await timeline . generateStream ();
```

## [ Next Steps](#next-steps)

## CaptionAsset

Auto-generated subtitles synced to speech

## Timeline Architecture

Complete guide to the 4-layer editing system

[Caption Asset](\pages\act\programmable-editing\caption-asset) [Event Detection Patterns](\pages\act\live-action\event-detection-patterns)

⌘ I