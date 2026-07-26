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
- [Embed Player](#embed-player)
    - [Basic HTML Embed](#basic-html-embed)
    - [React Component](#react-component)
    - [Vue Component](#vue-component)
- [Embed Code Generation](#embed-code-generation)
    - [get\_embed\_code()](#get_embed_code)
    - [Video Embed](#video-embed)
    - [Search Result Embed](#search-result-embed)
    - [RTStream Note](#rtstream-note)
    - [build\_iframe\_embed\_code() Utility](#build_iframe_embed_code-utility)
- [Thumbnail Generation](#thumbnail-generation)
    - [Get Video Thumbnail](#get-video-thumbnail)
    - [Multiple Thumbnails for Preview](#multiple-thumbnails-for-preview)
- [Share Links](#share-links)
    - [VideoDB Console Player](#videodb-console-player)
    - [Share Specific Clips](#share-specific-clips)
- [Social Media Metadata](#social-media-metadata)
    - [Open Graph Tags](#open-graph-tags)
    - [Twitter Card](#twitter-card)
    - [Generate Metadata Object](#generate-metadata-object)
- [CDN Delivery](#cdn-delivery)
    - [Stream URL Structure](#stream-url-structure)
    - [URL Caching Strategy](#url-caching-strategy)
- [Player Features](#player-features)
    - [Autoplay with Mute](#autoplay-with-mute)
    - [Loop Playback](#loop-playback)
    - [Custom Controls](#custom-controls)
- [Responsive Embed](#responsive-embed)
    - [Aspect Ratio Container](#aspect-ratio-container)
    - [Multiple Aspect Ratios](#multiple-aspect-ratios)
- [Best Practices](#best-practices)
    - [Error Handling](#error-handling)
- [Next Steps](#next-steps)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Output and Delivery](\pages\act\output-and-delivery\streams-and-exports)

# Publishing Patterns

Copy page

Embed players, share content, and deliver video to end users

Copy page

Deliver video content to end users through embedded players, shareable links, and social media integrations.

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video( "m-xxx" )

# Get streaming URL
stream_url = video.generate_stream()

# Get thumbnail
thumbnail_url = video.generate_thumbnail()

# Get download link
download_url = video.download( name = "sample video" )
```

```
import { connect } from 'videodb' ;

const conn = connect ();
const coll = await conn . getCollection ();
const video = await coll . getVideo ( "m-xxx" );

// Get streaming URL
const streamUrl = await video . generateStream ();

// Get thumbnail URL
const thumbnailUrl = await video . generateThumbnail ();

// Get download link
const downloadUrl = await video . download ( "sample video" );
```

## [ Embed Player](#embed-player)

### [ Basic HTML Embed](#basic-html-embed)

```
< video
id = "player"
controls
width = "100%"
poster = "{thumbnail_url}"
>
< source
src = "{stream_url}"
type = "application/x-mpegURL"
>
</ video >

< script src = "https://cdn.jsdelivr.net/npm/hls.js@latest" ></ script >
< script >
const video = document . getElementById ( 'player' );
const src = video . querySelector ( 'source' ). src ;

if ( Hls . isSupported ()) {
const hls = new Hls ();
hls . loadSource ( src );
hls . attachMedia ( video );
}
</ script >
```

### [ React Component](#react-component)

```
import Hls from 'hls.js' ;
import { useRef , useEffect } from 'react' ;

function VideoPlayer ({ streamUrl , thumbnailUrl , title }) {
const videoRef = useRef ( null );

useEffect (() => {
const video = videoRef . current ;
if ( ! video ) return ;

if ( Hls . isSupported ()) {
const hls = new Hls ();
hls . loadSource ( streamUrl );
hls . attachMedia ( video );

return () => hls . destroy ();
} else if ( video . canPlayType ( 'application/vnd.apple.mpegurl' )) {
// Safari native HLS
video . src = streamUrl ;
}
}, [ streamUrl ]);

return (
< video
ref = { videoRef }
controls
poster = { thumbnailUrl }
title = { title }
style = { { width: '100%' } }
/>
);
}
```

### [ Vue Component](#vue-component)

```
< template >
< video
ref = "videoPlayer"
controls
: poster = " thumbnailUrl "
style = " width : 100 % "
/ >
</ template >

< script setup >
import Hls from 'hls.js' ;
import { ref , onMounted , onUnmounted } from 'vue' ;

const props = defineProps ([ 'streamUrl' , 'thumbnailUrl' ]);
const videoPlayer = ref ( null );
let hls = null ;

onMounted (() => {
if ( Hls . isSupported ()) {
hls = new Hls ();
hls . loadSource ( props . streamUrl );
hls . attachMedia ( videoPlayer . value );
}
});

onUnmounted (() => {
if ( hls ) hls . destroy ();
});
</ script >
```

## [ Embed Code Generation](#embed-code-generation)

### [ get\_embed\_code()](#get_embed_code)

Generate an HTML iframe embed string directly from SDK objects. Available on `Video` , `Shot` , `SearchResult` , `Timeline` , `RTStream` , `RTStreamShot` , `RTStreamExportResult` , and `Editor Timeline` .

```
embed_html = obj.get_embed_code(
width = "100%" , # iframe width
height = 405 , # iframe height in pixels
title = "VideoDB Player" , # iframe title attribute
allow_fullscreen = True , # allow fullscreen
auto_generate = True # auto-call generate_stream() if player_url missing
)
```

Returns an HTML `<iframe>` string. Raises `ValueError` if `player_url` is not available and cannot be auto-generated.

### [ Video Embed](#video-embed)

```
video = coll.get_video( "m-xxx" )

# Auto-generates stream URL if needed
embed_html = video.get_embed_code()
print (embed_html)
# <iframe src="https://console.videodb.io/player?url=..." width="100%" height="405" ...></iframe>

# Custom dimensions
embed_html = video.get_embed_code( width = "640px" , height = 360 , title = "My Video" )
```

### [ Search Result Embed](#search-result-embed)

```
results = video.search( "product demo" )

# Embed the compiled search results
embed_html = results.get_embed_code( height = 480 )
```

### [ RTStream Note](#rtstream-note)

`RTStream` does **not** support `auto_generate` . You must call `generate_stream(start, end)` explicitly before calling `get_embed_code()` :

```
rt_stream.generate_stream( start = 0 , end = 120 )
embed_html = rt_stream.get_embed_code( auto_generate = False )
```

### [ build\_iframe\_embed\_code() Utility](#build_iframe_embed_code-utility)

A standalone helper when you already have a player URL:

```
from videodb import build_iframe_embed_code

embed_html = build_iframe_embed_code(player_url, width = "100%" , height = 405 )
```

## [ Thumbnail Generation](#thumbnail-generation)

### [ Get Video Thumbnail](#get-video-thumbnail)

Python

Node.js

```
# Default thumbnail (first frame)
thumbnail_url = video.generate_thumbnail()

# Thumbnail at specific time
thumbnail_url = video.generate_thumbnail( time = 30.5 )
```

```
// Default thumbnail (first frame)
const thumbnailUrl = await video . generateThumbnail ();

// Thumbnail at specific time
const thumbnailUrl = await video . generateThumbnail ( 30.5 );
```

### [ Multiple Thumbnails for Preview](#multiple-thumbnails-for-preview)

Python

Node.js

```
def generate_preview_thumbnails ( video , count = 5 ):
"""Generate evenly spaced thumbnails across video"""
duration = video.duration
interval = duration / (count + 1 )

thumbnails = []
for i in range ( 1 , count + 1 ):
time = interval * i
url = video.generate_thumbnail( time = time)
thumbnails.append({
"time" : time,
"url" : url
})

return thumbnails

previews = generate_preview_thumbnails(video, count = 5 )
```

```
async function generatePreviewThumbnails ( video , count = 5 ) {
const duration = video . duration ;
const interval = duration / ( count + 1 );

const thumbnails = [];
for ( let i = 1 ; i <= count ; i ++ ) {
const time = interval * i ;
const url = await video . generateThumbnail ( time );
thumbnails . push ({ time , url });
}

return thumbnails ;
}

const previews = await generatePreviewThumbnails ( video , 5 );
```

## [ Share Links](#share-links)

### [ VideoDB Console Player](#videodb-console-player)

Generate shareable links using the console player:

Python

Node.js

```
import urllib.parse

stream_url = video.generate_stream()
encoded_url = urllib.parse.quote(stream_url, safe = '' )

share_link = f "https://console.videodb.io/player?url= { encoded_url } "
```

```
const streamUrl = await video . generateStream ();
const encodedUrl = encodeURIComponent ( streamUrl );

const shareLink = `https://console.videodb.io/player?url= ${ encodedUrl } ` ;
```

### [ Share Specific Clips](#share-specific-clips)

Python

Node.js

```
# Share a specific segment
clip_url = video.generate_stream([( 120 , 180 )])
share_clip = f "https://console.videodb.io/player?url= { urllib.parse.quote(clip_url) } "
```

```
// Share a specific segment
const clipUrl = await video . generateStream ([[ 120 , 180 ]]);
const shareClip = `https://console.videodb.io/player?url= ${ encodeURIComponent ( clipUrl ) } ` ;
```

## [ Social Media Metadata](#social-media-metadata)

### [ Open Graph Tags](#open-graph-tags)

```
<!-- Video metadata for social sharing -->
< meta property = "og:type" content = "video.other" />
< meta property = "og:title" content = "{video_title}" />
< meta property = "og:description" content = "{video_description}" />
< meta property = "og:image" content = "{thumbnail_url}" />
< meta property = "og:video" content = "{stream_url}" />
< meta property = "og:video:type" content = "application/x-mpegURL" />
< meta property = "og:video:width" content = "1920" />
< meta property = "og:video:height" content = "1080" />
```

### [ Twitter Card](#twitter-card)

```
< meta name = "twitter:card" content = "player" />
< meta name = "twitter:title" content = "{video_title}" />
< meta name = "twitter:description" content = "{video_description}" />
< meta name = "twitter:image" content = "{thumbnail_url}" />
< meta name = "twitter:player" content = "{embed_url}" />
< meta name = "twitter:player:width" content = "1280" />
< meta name = "twitter:player:height" content = "720" />
```

### [ Generate Metadata Object](#generate-metadata-object)

Python

Node.js

```
def generate_social_metadata ( video , title , description ):
"""Generate metadata for social sharing"""
stream_url = video.generate_stream()
thumbnail_url = video.generate_thumbnail()

return {
"title" : title,
"description" : description,
"thumbnail" : thumbnail_url,
"video_url" : stream_url,
"og" : {
"type" : "video.other" ,
"title" : title,
"description" : description,
"image" : thumbnail_url,
"video" : stream_url
},
"twitter" : {
"card" : "player" ,
"title" : title,
"description" : description,
"image" : thumbnail_url
}
}
```

```
async function generateSocialMetadata ( video , title , description ) {
const streamUrl = await video . generateStream ();
const thumbnailUrl = await video . generateThumbnail ();

return {
title ,
description ,
thumbnail: thumbnailUrl ,
videoUrl: streamUrl ,
og: {
type: "video.other" ,
title ,
description ,
image: thumbnailUrl ,
video: streamUrl
},
twitter: {
card: "player" ,
title ,
description ,
image: thumbnailUrl
}
};
}
```

## [ CDN Delivery](#cdn-delivery)

### [ Stream URL Structure](#stream-url-structure)

VideoDB serves content through a global CDN:

```
https://stream.videodb.io/v3/published/manifests/{manifest-id}.m3u8
```

| Endpoint            | Purpose               |
|---------------------|-----------------------|
| `stream.videodb.io` | HLS streaming         |
| `cdn.videodb.io`    | Direct file downloads |

### [ URL Caching Strategy](#url-caching-strategy)

Python

Node.js

```
import time
from functools import lru_cache

class VideoURLCache :
def __init__ ( self , ttl = 23 * 3600 ): # 23 hours
self .cache = {}
self .ttl = ttl

def get_stream_url ( self , video , timestamps = None ):
key = f " { video.id } : { timestamps } "

if key in self .cache:
url, expires = self .cache[key]
if time.time() < expires:
return url

# Generate new URL
if timestamps:
url = video.generate_stream(timestamps)
else :
url = video.generate_stream()

self .cache[key] = (url, time.time() + self .ttl)
return url

# Usage
url_cache = VideoURLCache()
stream_url = url_cache.get_stream_url(video)
```

```
class VideoURLCache {
constructor ( ttl = 23 * 60 * 60 * 1000 ) { // 23 hours
this . cache = new Map ();
this . ttl = ttl ;
}

async getStreamUrl ( video , timestamps = null ) {
const key = ` ${ video . id } : ${ JSON . stringify ( timestamps ) } ` ;

if ( this . cache . has ( key )) {
const { url , expires } = this . cache . get ( key );
if ( Date . now () < expires ) {
return url ;
}
}

// Generate new URL
const url = timestamps
? await video . generateStream ( timestamps )
: await video . generateStream ();

this . cache . set ( key , {
url ,
expires: Date . now () + this . ttl
});

return url ;
}
}

// Usage
const urlCache = new VideoURLCache ();
const streamUrl = await urlCache . getStreamUrl ( video );
```

## [ Player Features](#player-features)

### [ Autoplay with Mute](#autoplay-with-mute)

```
< video
id = "player"
autoplay
muted
playsinline
poster = "{thumbnail_url}"
>
< source src = "{stream_url}" type = "application/x-mpegURL" >
</ video >
```

### [ Loop Playback](#loop-playback)

```
< video id = "player" loop controls >
< source src = "{stream_url}" type = "application/x-mpegURL" >
</ video >
```

### [ Custom Controls](#custom-controls)

```
function CustomPlayer ({ streamUrl }) {
const videoRef = useRef ( null );
const [ playing , setPlaying ] = useState ( false );
const [ progress , setProgress ] = useState ( 0 );

const togglePlay = () => {
if ( playing ) {
videoRef . current . pause ();
} else {
videoRef . current . play ();
}
setPlaying ( ! playing );
};

return (
< div className = "player-container" >
< video
ref = { videoRef }
onTimeUpdate = { ( e ) => {
const pct = ( e . target . currentTime / e . target . duration ) * 100 ;
setProgress ( pct );
} }
/>
< div className = "controls" >
< button onClick = { togglePlay } >
{ playing ? 'Pause' : 'Play' }
</ button >
< div className = "progress-bar" style = { { width: ` ${ progress } %` } } />
</ div >
</ div >
);
}
```

## [ Responsive Embed](#responsive-embed)

### [ Aspect Ratio Container](#aspect-ratio-container)

```
.video-container {
position : relative ;
width : 100 % ;
padding-bottom : 56.25 % ; /* 16:9 aspect ratio */
}

.video-container video {
position : absolute ;
top : 0 ;
left : 0 ;
width : 100 % ;
height : 100 % ;
}
```

```
< div class = "video-container" >
< video controls >
< source src = "{stream_url}" type = "application/x-mpegURL" >
</ video >
</ div >
```

### [ Multiple Aspect Ratios](#multiple-aspect-ratios)

```
.video-16-9 { padding-bottom : 56.25 % ; }
.video-4-3 { padding-bottom : 75 % ; }
.video-1-1 { padding-bottom : 100 % ; }
.video-9-16 { padding-bottom : 177.78 % ; }
```

## [ Best Practices](#best-practices)

| Practice             | Reason                                 |
|----------------------|----------------------------------------|
| Cache stream URLs    | Avoid regenerating on every request    |
| Use thumbnails       | Improve perceived load time            |
| Preload metadata     | `preload="metadata"` for faster starts |
| Lazy load off-screen | Defer loading until visible            |
| Handle errors        | Show fallback on stream failure        |

### [ Error Handling](#error-handling)

```
function VideoPlayer ({ streamUrl , fallbackUrl }) {
const [ error , setError ] = useState ( false );

if ( error && fallbackUrl ) {
return < img src = { fallbackUrl } alt = "Video unavailable" /> ;
}

return (
< video
controls
onError = { () => setError ( true ) }
>
< source src = { streamUrl } type = "application/x-mpegURL" />
</ video >
);
}
```

## [ Next Steps](#next-steps)

## Streams and Exports

Generate clips and export video

## Timeline Architecture

Compose video programmatically

[Streams and Exports](\pages\act\output-and-delivery\streams-and-exports) [Integrations Overview](\pages\automate\integrations-overview)

⌘ I