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
    - [Generative Media Overview](\pages\act\generative-media)
    - [Translation and Dubbing](\pages\act\generative-media\translation-and-dubbing)
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

- [Capabilities](#capabilities)
- [Quick Example](#quick-example)
- [Cheat Sheet](#cheat-sheet)
- [Async Processing](#async-processing)
    - [Callback Payload](#callback-payload)
- [Guide Index](#guide-index)
- [What You Can Build](#what-you-can-build)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Generative Media](\pages\act\generative-media\index)

# Generative Media Overview

Copy page

Generate media assets programmatically: images, music, sound effects, voices, and video clips. Translate and dub existing content into new languages.

Copy page

## [ Capabilities](#capabilities)

| Category         | What You Can Create                     |
|------------------|-----------------------------------------|
| **Images**       | Text-to-image with aspect ratio control |
| **Audio**        | Music, sound effects, text-to-speech    |
| **Video**        | Short AI-generated clips (5-8 seconds)  |
| **Localization** | Dubbing, transcript translation         |

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()

# Generate an image
image = coll.generate_image(
prompt = "Futuristic city skyline at sunset" ,
aspect_ratio = "16:9"
)
print (image.generate_url())

# Generate a voiceover
voice = coll.generate_voice(
text = "Welcome to our product demo" ,
voice_name = "Sarah"
)

# Dub a video to Spanish
dubbed = coll.dub_video(
video_id = "m-xxx" ,
language_code = "es"
)
```

```
import { connect } from 'videodb' ;

const conn = connect ();
const coll = await conn . getCollection ();

// Generate an image
const image = await coll . generateImage (
"Futuristic city skyline at sunset" ,
"16:9"
);
console . log ( await image . generateUrl ());

// Generate a voiceover
const voice = await coll . generateVoice (
"Welcome to our product demo" ,
"Sarah"
);

// Dub a video to Spanish
const dubbed = await coll . dubVideo ( "m-xxx" , "es" );
```

## [ Cheat Sheet](#cheat-sheet)

Python

Node.js

```
# Image
coll.generate_image(prompt, aspect_ratio = '1:1' , callback_url = None )

# Music
coll.generate_music(prompt, duration = 5 , callback_url = None )

# Sound Effect
coll.generate_sound_effect(prompt, duration = 2 , callback_url = None )

# Voice
coll.generate_voice(text, voice_name = 'Default' , config = {}, callback_url = None )

# Video
coll.generate_video(prompt, duration = 5 , callback_url = None )

# Dub
coll.dub_video(video_id, language_code, callback_url = None )

# Translate
video.translate_transcript(language, additional_notes = '' , callback_url = None )
```

```
// Image
await coll . generateImage ( prompt , '1:1' , null );

// Music
await coll . generateMusic ( prompt , 5 , null );

// Sound Effect
await coll . generateSoundEffect ( prompt , 2 , null );

// Voice
await coll . generateVoice ( text , 'Default' , {}, null );

// Video
await coll . generateVideo ( prompt , 5 , null );

// Dub
await coll . dubVideo ( videoId , languageCode , null );

// Translate
await video . translateTranscript ( language , '' , null );
```

## [ Async Processing](#async-processing)

All generative calls support asynchronous processing:

1. When `callback_url` is not provided: SDK returns an asset object once the process is done (synchronous processing)
2. When `callback_url` is provided: SDK returns immediately and sends a webhook when complete (asynchronous processing)
3. Call `.generate_url()` to get the finished file URL

### [ Callback Payload](#callback-payload)

```
{
"success" : true ,
"data" : {
"id" : "img-z-019c4cb6-207c-7d23-aab1-e8ef7a5fcde1" ,
"collection_id" : "c-3b0a66f2-fac5-4816-b29e-e606986c0490" ,
"name" : "Futuristic City Sunset Skyline" ,
"extension" : "png" ,
"size" : "1607220"
}
}
```

## [ Guide Index](#guide-index)

## Images, Audio &amp; Video

Generate images, music, SFX, voices, and video

## Translation &amp; Dubbing

Localize content into 20+ languages

## [ What You Can Build](#what-you-can-build)

## AI Voiceovers

Add narration to silent footage with AI-generated voices

## Video Dubbing

Localize videos into multiple languages

## Voice Cloning

Replace voices with cloned audio preserving tone and style

## Trailer Narration

Create dramatic trailers with compelling voiceovers

[Webhooks and Reliability](\pages\act\live-action\webhooks-and-reliability) [Translation and Dubbing](\pages\act\generative-media\translation-and-dubbing)

⌘ I