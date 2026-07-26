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
    - [Streams and Exports](\pages\act\output-and-delivery\streams-and-exports)
    - [Publishing Patterns](\pages\act\output-and-delivery\publishing-patterns)

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
- [Stream Generation](#stream-generation)
    - [From Search Results](#from-search-results)
    - [From Timestamps](#from-timestamps)
    - [From Timeline](#from-timeline)
- [Stream URL Format](#stream-url-format)
- [Download and Export](#download-and-export)
    - [Get Video URL](#get-video-url)
    - [Get Audio URL](#get-audio-url)
    - [Get Image URL](#get-image-url)
- [Embedding Streams](#embedding-streams)
    - [HTML5 Video](#html5-video)
    - [With HLS.js](#with-hls-js)
    - [React Component](#react-component)
    - [VideoDB Console Player](#videodb-console-player)
- [Clip Export Patterns](#clip-export-patterns)
    - [Export Search Results as Clips](#export-search-results-as-clips)
    - [Batch Export](#batch-export)
- [Combine Multiple Videos](#combine-multiple-videos)
    - [Merge Clips from Different Videos](#merge-clips-from-different-videos)
    - [Collection Highlights](#collection-highlights)
- [URL Lifecycle](#url-lifecycle)
    - [Refresh Expired URLs](#refresh-expired-urls)
- [Reframe and Aspect Ratio Conversion](#reframe-and-aspect-ratio-conversion)
    - [reframe()](#reframe)
    - [smart\_vertical\_reframe()](#smart_vertical_reframe)
- [Next Steps](#next-steps)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Output and Delivery](\pages\act\output-and-delivery\streams-and-exports)

# Streams and Exports

Copy page

Generate playable streams, downloadable clips, and export videos

Copy page

Generate playable HLS streams from search results, timestamps, or timeline compositions. Export clips for download or embed streams in your application.

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video( "m-xxx" )

# Stream from search results
results = video.search( "product demo" )
stream_url = results.compile()

# Stream from timestamps
stream_url = video.generate_stream([( 10 , 30 ), ( 45 , 60 )])

# Get download URL
download_url = video.download( name = "sample video" )
```

```
import { connect } from 'videodb' ;

const conn = connect ();
const coll = await conn . getCollection ();
const video = await coll . getVideo ( "m-xxx" );

// Stream from search results
const results = await video . search ( "product demo" );
const streamUrl = await results . compile ();

// Stream from timestamps
const streamUrl2 = await video . generateStream ([[ 10 , 30 ], [ 45 , 60 ]]);

// Get download URL
const downloadUrl = await video . download ( "sample video" );
```

## [ Stream Generation](#stream-generation)

### [ From Search Results](#from-search-results)

Search returns matching segments. Generate a stream to play them as a single video.

Python

Node.js

```
# Search for content
results = video.search( "key moments" )

# Generate playable stream
stream_url = results.compile()
# https://stream.videodb.io/v3/published/manifests/{id}.m3u8

# Play in browser
results.play()
```

```
// Search for content
const results = await video . search ( "key moments" );

// Generate playable stream
const streamUrl = await results . compile ();
// https://stream.videodb.io/v3/published/manifests/{id}.m3u8

// Play in browser
await results . play ();
```

### [ From Timestamps](#from-timestamps)

Create streams from specific time ranges.

Python

Node.js

```
# Define time segments (start, end) in seconds
timestamps = [
( 0 , 15 ), # Intro
( 120 , 180 ), # Main content
( 300 , 330 ) # Conclusion
]

stream_url = video.generate_stream(timestamps)
```

```
// Define time segments [start, end] in seconds
const timestamps = [
[ 0 , 15 ], // Intro
[ 120 , 180 ], // Main content
[ 300 , 330 ] // Conclusion
];

const streamUrl = await video . generateStream ( timestamps );
```

### [ From Timeline](#from-timeline)

Export composed timelines as streams.

Python

Node.js

```
from videodb.editor import Timeline, VideoAsset

# Build timeline
timeline = Timeline(conn)
timeline.add_inline(VideoAsset(video.id, start = 10 , end = 30 ))
timeline.add_inline(VideoAsset(video.id, start = 60 , end = 90 ))

# Generate stream
stream_url = timeline.generate_stream()
```

```
import { Timeline , VideoAsset } from 'videodb' ;

// Build timeline
const timeline = new Timeline ( conn );
timeline . addInline ( new VideoAsset ( video . id , 10 , 30 ));
timeline . addInline ( new VideoAsset ( video . id , 60 , 90 ));

// Generate stream
const streamUrl = await timeline . generateStream ();
```

## [ Stream URL Format](#stream-url-format)

All generated streams use HLS format:

```
https://stream.videodb.io/v3/published/manifests/{manifest-id}.m3u8
```

| Property      | Value                            |
|---------------|----------------------------------|
| Format        | HLS (HTTP Live Streaming)        |
| Container     | .m3u8 manifest with .ts segments |
| Compatibility | All modern browsers, native apps |

## [ Download and Export](#download-and-export)

### [ Get Video URL](#get-video-url)

Python

Node.js

```
# Full video download URL
download_url = video.download( name = "sample video" )
# https://cdn.videodb.io/v3/{collection}/{video}.mp4
```

```
// Full video download URL
const downloadUrl = await video . download ( "sample video" );
// https://cdn.videodb.io/v3/{collection}/{video}.mp4
```

### [ Get Audio URL](#get-audio-url)

Python

Node.js

```
# Audio-only download
audio_url = audio.generate_url()
```

```
// Audio-only download
const audioUrl = await audio . generateUrl ();
```

### [ Get Image URL](#get-image-url)

Python

Node.js

```
# Generated image URL
image_url = image.generate_url()
```

```
// Generated image URL
const imageUrl = await image . generateUrl ();
```

## [ Embedding Streams](#embedding-streams)

### [ HTML5 Video](#html5-video)

```
< video controls >
< source
src = "https://stream.videodb.io/v3/published/manifests/{id}.m3u8"
type = "application/x-mpegURL"
>
</ video >
```

### [ With HLS.js](#with-hls-js)

```
< script src = "https://cdn.jsdelivr.net/npm/hls.js@latest" ></ script >
< video id = "video" controls ></ video >

< script >
const video = document . getElementById ( 'video' );
const streamUrl = 'https://stream.videodb.io/v3/...' ;

if ( Hls . isSupported ()) {
const hls = new Hls ();
hls . loadSource ( streamUrl );
hls . attachMedia ( video );
}
</ script >
```

### [ React Component](#react-component)

```
import Hls from 'hls.js' ;
import { useRef , useEffect } from 'react' ;

function VideoPlayer ({ streamUrl }) {
const videoRef = useRef ( null );

useEffect (() => {
if ( Hls . isSupported ()) {
const hls = new Hls ();
hls . loadSource ( streamUrl );
hls . attachMedia ( videoRef . current );
return () => hls . destroy ();
}
}, [ streamUrl ]);

return < video ref = { videoRef } controls /> ;
}
```

### [ VideoDB Console Player](#videodb-console-player)

Use the built-in player:

```
https://console.videodb.io/player?url={encoded_stream_url}
```

## [ Clip Export Patterns](#clip-export-patterns)

### [ Export Search Results as Clips](#export-search-results-as-clips)

Python

Node.js

```
results = video.search( "highlight moments" )

# Export each match as separate stream
clips = []
for shot in results.get_shots():
clip_url = shot.generate_stream()
clips.append({
"start" : shot.start,
"end" : shot.end,
"url" : clip_url,
"text" : shot.text
})
```

```
const results = await video . search ( "highlight moments" );

// Export each match as separate stream
const clips = [];
for ( const shot of results . shots ) {
const clipUrl = await shot . generateStream ();
clips . push ({
start: shot . start ,
end: shot . end ,
url: clipUrl ,
text: shot . text
});
}
```

### [ Batch Export](#batch-export)

Python

Node.js

```
def export_clips ( video , timestamps , prefix = "clip" ):
"""Export multiple clips from a video"""
exports = []

for i, (start, end) in enumerate (timestamps):
stream_url = video.generate_stream([(start, end)])
exports.append({
"name" : f " { prefix } _ { i + 1 } " ,
"start" : start,
"end" : end,
"duration" : end - start,
"url" : stream_url
})

return exports

# Export intro, middle, outro
clips = export_clips(video, [
( 0 , 30 ),
( 120 , 180 ),
( 300 , 330 )
])
```

```
async function exportClips ( video , timestamps , prefix = "clip" ) {
const exports = [];

for ( let i = 0 ; i < timestamps . length ; i ++ ) {
const [ start , end ] = timestamps [ i ];
const streamUrl = await video . generateStream ([[ start , end ]]);
exports . push ({
name: ` ${ prefix } _ ${ i + 1 } ` ,
start ,
end ,
duration: end - start ,
url: streamUrl
});
}

return exports ;
}

// Export intro, middle, outro
const clips = await exportClips ( video , [
[ 0 , 30 ],
[ 120 , 180 ],
[ 300 , 330 ]
]);
```

## [ Combine Multiple Videos](#combine-multiple-videos)

### [ Merge Clips from Different Videos](#merge-clips-from-different-videos)

Python

Node.js

```
from videodb.editor import Timeline, VideoAsset

video1 = coll.get_video( "m-first" )
video2 = coll.get_video( "m-second" )
video3 = coll.get_video( "m-third" )

# Create combined timeline
timeline = Timeline(conn)
timeline.add_inline(VideoAsset(video1.id, start = 0 , end = 30 ))
timeline.add_inline(VideoAsset(video2.id, start = 10 , end = 40 ))
timeline.add_inline(VideoAsset(video3.id, start = 0 , end = 20 ))

# Generate merged stream
merged_url = timeline.generate_stream()
```

```
import { Timeline , VideoAsset } from 'videodb' ;

const video1 = await coll . getVideo ( "m-first" );
const video2 = await coll . getVideo ( "m-second" );
const video3 = await coll . getVideo ( "m-third" );

// Create combined timeline
const timeline = new Timeline ( conn );
timeline . addInline ( new VideoAsset ( video1 . id , 0 , 30 ));
timeline . addInline ( new VideoAsset ( video2 . id , 10 , 40 ));
timeline . addInline ( new VideoAsset ( video3 . id , 0 , 20 ));

// Generate merged stream
const mergedUrl = await timeline . generateStream ();
```

### [ Collection Highlights](#collection-highlights)

Python

Node.js

```
from videodb.editor import Timeline, VideoAsset

# Search across collection
results = coll.search( "best moments" )

# Build highlight reel from top results
timeline = Timeline(conn)
for shot in results.get_shots()[: 10 ]: # Top 10
video_asset = VideoAsset( id = shot.video_id, start = shot.start)
clip = Clip( asset = video_asset, duration = shot.end - shot.start)
track = Track()
track.add_clip( 0 , clip)
timeline.add_track(track)

highlight_url = timeline.generate_stream()
```

```
import { Timeline , VideoAsset } from 'videodb' ;

// Search across collection
const results = await coll . search ( "best moments" );

// Build highlight reel from top results
const timeline = new Timeline ( conn );
for ( const shot of results . shots . slice ( 0 , 10 )) { // Top 10
const videoAsset = new VideoAsset ( shot . videoId , { start: shot . start });
const clip = new Clip ({ asset: videoAsset , duration: shot . end - shot . start });
const track = new Track ();
track . addClip ( 0 , clip );
timeline . addTrack ( track );
}

const highlightUrl = await timeline . generateStream ();
```

## [ URL Lifecycle](#url-lifecycle)

| Stage        | Duration   | Notes                                  |
|--------------|------------|----------------------------------------|
| Generation   | Instant    | Stream URL returned immediately        |
| Playback     | 24 hours   | URL valid for playback                 |
| Regeneration | Anytime    | Call generate_stream again for new URL |

### [ Refresh Expired URLs](#refresh-expired-urls)

Python

Node.js

```
def get_fresh_stream ( video , timestamps , cache = {}):
"""Get stream URL, regenerating if needed"""
cache_key = f " { video.id } : { timestamps } "

# Check cache and expiry
if cache_key in cache:
cached = cache[cache_key]
if cached[ "expires" ] > time.time():
return cached[ "url" ]

# Generate fresh URL
url = video.generate_stream(timestamps)
cache[cache_key] = {
"url" : url,
"expires" : time.time() + 23 * 3600 # 23 hours
}

return url
```

```
const cache = new Map ();

async function getFreshStream ( video , timestamps ) {
const cacheKey = ` ${ video . id } : ${ JSON . stringify ( timestamps ) } ` ;

// Check cache and expiry
const cached = cache . get ( cacheKey );
if ( cached && cached . expires > Date . now ()) {
return cached . url ;
}

// Generate fresh URL
const url = await video . generateStream ( timestamps );
cache . set ( cacheKey , {
url ,
expires: Date . now () + 23 * 60 * 60 * 1000 // 23 hours
});

return url ;
}
```

## [ Reframe and Aspect Ratio Conversion](#reframe-and-aspect-ratio-conversion)

### [ reframe()](#reframe)

Convert a video to a different aspect ratio. Useful for repurposing landscape content to vertical formats for social media.

Python

```
# Reframe to vertical (9:16) for social media
vertical_video = video.reframe( target = "vertical" , mode = "smart" )

# Custom aspect ratio (square)
square_video = video.reframe( target = { "width" : 1 , "height" : 1 })

# Reframe a specific time range
clip = video.reframe( start = 10.0 , end = 60.0 , target = "vertical" )

# Async with callback
video.reframe(
start = 10.0 ,
end = 60.0 ,
target = "vertical" ,
callback_url = "https://example.com/webhook"
)
```

| Parameter      | Type            | Description                                                                    |
|----------------|-----------------|--------------------------------------------------------------------------------|
| `target`       | `str` or `dict` | `"vertical"` , `"square"` , `"landscape"` , or `{"width": int, "height": int}` |
| `mode`         | `str`           | `"simple"` or `"smart"` (default). Smart mode uses object-aware tracking.      |
| `start`        | `float`         | Optional start time in seconds                                                 |
| `end`          | `float`         | Optional end time in seconds                                                   |
| `callback_url` | `str`           | Optional URL for async completion callback                                     |

### [ smart\_vertical\_reframe()](#smart_vertical_reframe)

Convenience method that reframes to vertical (9:16) with smart object tracking in a single call:

```
vertical = video.smart_vertical_reframe()
```

## [ Next Steps](#next-steps)

## Publishing Patterns

Embed players and share content

## Timeline Architecture

Build complex compositions

[Translation and Dubbing](\pages\act\generative-media\translation-and-dubbing) [Publishing Patterns](\pages\act\output-and-delivery\publishing-patterns)

⌘ I