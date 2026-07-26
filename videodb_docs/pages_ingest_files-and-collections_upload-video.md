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
    - [Upload Video](\pages\ingest\files-and-collections\upload-video)
    - [Create Collection](\pages\ingest\files-and-collections\create-collection)
    - [Collection Patterns](\pages\ingest\files-and-collections\collection-patterns)
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

- [Quick Example](#quick-example)
- [Upload Methods](#upload-methods)
    - [From URL](#from-url)
    - [From Local File](#from-local-file)
- [Media Types](#media-types)
- [Upload Response](#upload-response)
- [Async Uploads with Callbacks](#async-uploads-with-callbacks)
- [What You Can Build](#what-you-can-build)
- [Next Steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Files and Collections](\pages\ingest\files-and-collections\upload-video)

# Upload Video

Copy page

Ingest video, audio, and images from URLs or local files into VideoDB collections

Copy page

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()

video = coll.upload( "https://example.com/video.mp4" )
print (video.id) # m-xxx
```

```
import { connect } from 'videodb' ;

const conn = await connect ();
const coll = await conn . getCollection ();

const video = await coll . uploadURL ( "https://example.com/video.mp4" );
console . log ( video . id ); // m-xxx
```

## [ Upload Methods](#upload-methods)

### [ From URL](#from-url)

Upload directly from any accessible URL (S3, YouTube, public links):

Python

Node.js

```
# Video
video = coll.upload( url = "https://youtu.be/a9__D53WsUs" )

# Audio
from videodb import MediaType
audio = coll.upload(
url = "https://example.com/podcast.mp3" ,
media_type = MediaType.audio
)

# Image
image = coll.upload(
url = "https://example.com/frame.jpg" ,
media_type = MediaType.image
)
```

```
import { MediaType } from 'videodb' ;

// Video
const video = await coll . uploadURL ({ url: "https://youtu.be/a9__D53WsUs" });

// Audio
const audio = await coll . uploadURL ({
url: "https://example.com/podcast.mp3" ,
mediaType: MediaType . audio
});

// Image
const image = await coll . uploadURL ({
url: "https://example.com/frame.jpg" ,
mediaType: MediaType . image
});
```

### [ From Local File](#from-local-file)

Upload files from your local filesystem:

Python

Node.js

```
video = coll.upload( file_path = "./meeting-recording.mp4" )
```

```
const video = await coll . uploadFile ({ filePath: "./meeting-recording.mp4" });
```

## [ Media Types](#media-types)

| Type   | ID Prefix   | Use Case                       |
|--------|-------------|--------------------------------|
| Video  | `m-xxx`     | Primary content, full playback |
| Audio  | `a-xxx`     | Podcasts, voice recordings     |
| Image  | `img-xxx`   | Thumbnails, frames             |

## [ Upload Response](#upload-response)

After upload, you receive a media object with:

| Property        | Description                               |
|-----------------|-------------------------------------------|
| `id`            | Unique identifier (m-xxx, a-xxx, img-xxx) |
| `collection_id` | Parent collection ID                      |
| `name`          | File name                                 |
| `length`        | Duration in seconds (video/audio)         |
| `stream_url`    | HLS stream URL (video)                    |
| `player_url`    | Web player URL (video)                    |

## [ Async Uploads with Callbacks](#async-uploads-with-callbacks)

For production workflows, use callbacks to handle upload completion:

Python

Node.js

```
video = coll.upload(
url = "https://example.com/large-video.mp4" ,
callback_url = "https://your-backend.com/webhooks/upload"
)
```

```
const video = await coll . uploadURL ({
url: "https://example.com/large-video.mp4" ,
callbackUrl: "https://your-backend.com/webhooks/upload"
});
```

Your webhook receives:

```
{
"success" : true ,
"data" : {
"id" : "m-xxx" ,
"collection_id" : "c-xxx" ,
"name" : "large-video.mp4" ,
"stream_url" : "https://stream.videodb.io/..." ,
"player_url" : "https://console.videodb.io/player?url=..."
}
}
```

## [ What You Can Build](#what-you-can-build)

## Faceless Video Creator

Upload assets and compose complete AI-generated videos

## TikTok Lyric Videos

Upload music and create viral vertical clips with synced lyrics

## Intro &amp; Outro Automation

Upload brand assets and automatically add to all videos

## [ Next Steps](#next-steps)

## Create Collection

Organize uploads into collections

## Collection Patterns

Batching, retries, and production patterns

[Security &amp; Privacy](\pages\core-concepts\security-privacy) [Create Collection](\pages\ingest\files-and-collections\create-collection)

⌘ I