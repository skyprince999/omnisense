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

- [Quick Example](#quick-example)
- [Video Dubbing](#video-dubbing)
    - [Parameters](#parameters)
    - [Supported Languages](#supported-languages)
- [Transcript Translation](#transcript-translation)
    - [Step 1: Index Spoken Words](#step-1-index-spoken-words)
    - [Step 2: Translate](#step-2-translate)
    - [Parameters](#parameters-2)
    - [Style Guidance Examples](#style-guidance-examples)
- [Use Cases](#use-cases)
    - [Global Product Launch](#global-product-launch)
    - [Educational Content](#educational-content)
    - [Customer Support](#customer-support)
- [Best Practices](#best-practices)
    - [Pre-Dubbing Checklist](#pre-dubbing-checklist)
    - [Language Expansion](#language-expansion)
    - [Quality Review](#quality-review)
- [Async Processing](#async-processing)
    - [Webhook Response](#webhook-response)
- [What You Can Build](#what-you-can-build)
- [Next Steps](#next-steps)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Generative Media](\pages\act\generative-media\index)

# Translation and Dubbing

Copy page

Localize videos with automated dubbing and transcript translation

Copy page

Dub videos into new languages or translate transcripts for subtitles. Support for 20+ languages with automated voice matching.

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video( "m-xxx" )

# Dub video to Spanish
dubbed = coll.dub_video(
video_id = video.id,
language_code = "es"
)
dubbed.play()

# Translate transcript to French
video.index_spoken_words()
french_transcript = video.translate_transcript( language = "fr" )
```

```
import { connect } from 'videodb' ;

const conn = connect ();
const coll = await conn . getCollection ();
const video = await coll . getVideo ( "m-xxx" );

// Dub video to Spanish
const dubbed = await coll . dubVideo ( video . id , "es" );
await dubbed . play ();

// Translate transcript to French
await video . indexSpokenWords ();
const frenchTranscript = await video . translateTranscript ( "fr" );
```

## [ Video Dubbing](#video-dubbing)

Replace the audio track with AI-generated voices in another language.

Python

Node.js

```
dubbed = coll.dub_video(
video_id = video.id,
language_code = "hi" , # Hindi
callback_url = "https://your-backend.com/webhooks/dubbing"
)

# Returns a new video object
dubbed.play()
```

```
const dubbed = await coll . dubVideo (
video . id ,
"hi" , // Hindi
"https://your-backend.com/webhooks/dubbing"
);

// Returns a new video object
await dubbed . play ();
```

### [ Parameters](#parameters)

| Parameter       | Type   | Default   | Description                 |
|-----------------|--------|-----------|-----------------------------|
| `video_id`      | str    | required  | Source video ID             |
| `language_code` | str    | required  | Target language (ISO 639-1) |
| `callback_url`  | str    | None      | Webhook URL when complete   |

### [ Supported Languages](#supported-languages)

| Language   | Code   | Language   | Code   |
|------------|--------|------------|--------|
| Spanish    | `es`   | Hindi      | `hi`   |
| French     | `fr`   | Japanese   | `ja`   |
| German     | `de`   | Korean     | `ko`   |
| Italian    | `it`   | Chinese    | `zh`   |
| Portuguese | `pt`   | Arabic     | `ar`   |
| Dutch      | `nl`   | Russian    | `ru`   |
| Polish     | `pl`   | Turkish    | `tr`   |

## [ Transcript Translation](#transcript-translation)

Translate the spoken content for subtitles or text-based use cases.

### [ Step 1: Index Spoken Words](#step-1-index-spoken-words)

Python

Node.js

```
# Required before translation
video.index_spoken_words()
```

```
// Required before translation
await video . indexSpokenWords ();
```

### [ Step 2: Translate](#step-2-translate)

Python

Node.js

```
# Translate to French
french_text = video.translate_transcript(
language = "fr" ,
additional_notes = "Use formal tone"
)

print (french_text)
```

```
// Translate to French
const frenchText = await video . translateTranscript (
"fr" ,
"Use formal tone"
);

console . log ( frenchText );
```

### [ Parameters](#parameters-2)

| Parameter          | Type   | Default   | Description                    |
|--------------------|--------|-----------|--------------------------------|
| `language`         | str    | required  | Target language (ISO 639-1)    |
| `additional_notes` | str    | `""`      | Style guidance for translation |
| `callback_url`     | str    | None      | Webhook URL                    |

### [ Style Guidance Examples](#style-guidance-examples)

```
# Formal business content
additional_notes = "Use formal business language appropriate for corporate presentations"

# Casual content
additional_notes = "Use casual, conversational tone"

# Technical content
additional_notes = "Preserve technical terms in English where no equivalent exists"

# Marketing content
additional_notes = "Adapt cultural references for the target audience"
```

## [ Use Cases](#use-cases)

### [ Global Product Launch](#global-product-launch)

```
# Upload marketing video
video = coll.upload( url = "https://example.com/product-launch.mp4" )

# Create versions for key markets
languages = [ "es" , "fr" , "de" , "ja" , "zh" ]

for lang in languages:
dubbed = coll.dub_video(
video_id = video.id,
language_code = lang,
callback_url = f "https://backend.com/webhooks/dubbing/ { lang } "
)
```

### [ Educational Content](#educational-content)

```
# Upload lecture video
lecture = coll.upload( url = "https://example.com/lecture.mp4" )
lecture.index_spoken_words()

# Generate subtitles in multiple languages
for lang in [ "es" , "fr" , "pt" , "zh" ]:
translated = lecture.translate_transcript(
language = lang,
additional_notes = "Educational content, maintain academic tone"
)
# Use with CaptionAsset for subtitles
```

### [ Customer Support](#customer-support)

```
# Dub support video for regional markets
support_video = coll.get_video( "m-support-tutorial" )

# Create localized versions
regional_versions = {
"LATAM" : "es" ,
"Brazil" : "pt" ,
"France" : "fr" ,
"Germany" : "de"
}

for region, lang in regional_versions.items():
coll.dub_video(
video_id = support_video.id,
language_code = lang,
callback_url = f "https://backend.com/webhooks/ { region } "
)
```

## [ Best Practices](#best-practices)

### [ Pre-Dubbing Checklist](#pre-dubbing-checklist)

| Check                    | Why                           |
|--------------------------|-------------------------------|
| Clear audio              | Reduces transcription errors  |
| Single speaker           | Better voice matching         |
| Minimal background music | Cleaner dubbing result        |
| Proper pacing            | Allows for language expansion |

### [ Language Expansion](#language-expansion)

Different languages have different word counts for the same content:

| Original (English)   | Expansion   |
|----------------------|-------------|
| German               | +15-20%     |
| French               | +15-20%     |
| Spanish              | +10-15%     |
| Japanese             | -10-15%     |
| Chinese              | -20-30%     |

Plan for this when timing is critical.

### [ Quality Review](#quality-review)

After dubbing:

1. Check lip sync on close-ups
2. Verify tone matches content
3. Review technical term pronunciation
4. Test with native speakers

## [ Async Processing](#async-processing)

Dubbing is a long-running operation. Use callbacks:

Python

Node.js

```
# Start dubbing (returns immediately when callback_url is provided)
dubbed = coll.dub_video(
video_id = video.id,
language_code = "ja" ,
callback_url = "https://your-backend.com/webhooks/dubbing"
)

print ( f "Processing video ID: { dubbed.id } " )

# When callback_url is not provided, SDK returns video object once process is done
dubbed = coll.dub_video(
video_id = video.id,
language_code = "ja"
)
# This will wait and return the completed video object
```

```
// Start dubbing (returns immediately when callback_url is provided)
const dubbed = await coll . dubVideo (
video . id ,
"ja" ,
"https://your-backend.com/webhooks/dubbing"
);

console . log ( `Processing video ID: ${ dubbed . id } ` );

// When callback_url is not provided, SDK returns video object once process is done
const dubbedSync = await coll . dubVideo (
video . id ,
"ja"
);
// This will wait and return the completed video object
```

### [ Webhook Response](#webhook-response)

When the dubbing process completes, your webhook receives:

```
{
"success" : true ,
"data" : {
"id" : "m-dubbed-xxx" ,
"collection_id" : "c-xxx" ,
"name" : "dubbed_video" ,
"extension" : "mp4" ,
"size" : "12345678"
}
}
```

## [ What You Can Build](#what-you-can-build)

## Video Dubbing

Localize videos into multiple languages automatically

## AI Voiceovers

Generate narration in different languages

## [ Next Steps](#next-steps)

## Safety &amp; Approvals

Review workflows before publishing

## Subtitles Guide

Add styled subtitles to videos

[Generative Media Overview](\pages\act\generative-media) [Streams and Exports](\pages\act\output-and-delivery\streams-and-exports)

⌘ I