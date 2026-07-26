### Overview

- [Examples &amp; Tutorials](\examples-and-tutorials)

### Agentic Workflows

- [Overview](\examples-and-tutorials\ai-copilots)
- [Pair Programmer](\examples-and-tutorials\ai-copilots\pair-programmer)
- [OpenClaw Monitoring](\examples-and-tutorials\ai-copilots\openclaw-monitoring)
- [Call.md](\examples-and-tutorials\ai-copilots\call-md)
- [Bloom](\examples-and-tutorials\ai-copilots\bloom)
- [Focusd](\examples-and-tutorials\ai-copilots\focusd)

### Video Search and Understanding

- [Overview](\examples-and-tutorials\video-rag)
- [Keyword Search](\examples-and-tutorials\video-rag\keyword-search)
- [Character Extraction](\examples-and-tutorials\video-rag\character-clips)
- [Multimodal Search](\examples-and-tutorials\video-rag\multimodal-search)
- [Case Study: NFL Game Analysis](\examples-and-tutorials\video-rag\case-study-nfl)
- [Use Case: Conference Slide Extraction](\examples-and-tutorials\video-rag\use-case-conference-slides)

### Live Intelligence

- [Overview](\examples-and-tutorials\live-intelligence)
- [Baby Crib Monitoring with AI](\examples-and-tutorials\live-intelligence\baby-crib-monitoring)
- [Intelligent Property Intrusion Detection](\examples-and-tutorials\live-intelligence\intrusion-detection)
- [Flash Flood Early Warning System](\examples-and-tutorials\live-intelligence\flash-flood-detection)
- [Multi-Use Road Monitoring System](\examples-and-tutorials\live-intelligence\road-monitoring)
- [Dashcam Monitoring of Traffic](\examples-and-tutorials\live-intelligence\roadcam-monitoring)
- [Traffic Violation Detection](\examples-and-tutorials\live-intelligence\traffic-violations)
- [Live Cricket Highlight Detection](\examples-and-tutorials\live-intelligence\cricket-match-monitoring)
- [Multi-Camera Basketball Analytics](\examples-and-tutorials\live-intelligence\multicam-basketball-analysis)
- [Multi-Camera Public Safety Surveillance](\examples-and-tutorials\live-intelligence\multicam-public-surveillance)
- [TwelveLabs Integration](\examples-and-tutorials\live-intelligence\twelvelabs-integration)

### Content Factory

- [Overview](\examples-and-tutorials\content-factory)
- [Faceless Video Creator](\examples-and-tutorials\content-factory\faceless-video-creator)
- [AI-Generated Ads](\examples-and-tutorials\content-factory\ai-ad-films)
- [TikTok Style Lyric Video Creator](\examples-and-tutorials\content-factory\tiktok-lyric-video)
- [Video Dubbing](\examples-and-tutorials\content-factory\dubbing)
- [AI Voiceovers](\examples-and-tutorials\content-factory\voiceovers)
- [Trailer Narration](\examples-and-tutorials\content-factory\trailer-narration)
- [Voice Cloning](\examples-and-tutorials\content-factory\voice-cloning)
- [Text to Video](\examples-and-tutorials\content-factory\text-prompts)
- [AI Storyteller for Kids](\examples-and-tutorials\content-factory\ai-storyteller-kids)
- [Annual Video Statistics Recap](\examples-and-tutorials\content-factory\year-in-frames)
- [PromptClip](\pages\community\open-source\promptclip)

### Programmatic Editing

- [Overview](\examples-and-tutorials\programmatic-editing)
- [Intro/Outro](\examples-and-tutorials\programmatic-editing\intro-outro)
- [Brand Elements](\examples-and-tutorials\programmatic-editing\brand-elements)
- [Audio Overlay](\examples-and-tutorials\programmatic-editing\audio-overlay)
- [Dynamic Ads](\examples-and-tutorials\programmatic-editing\dynamic-ads)
- [Dynamic Streams](\examples-and-tutorials\programmatic-editing\dynamic-streams)
- [Word Counter](\examples-and-tutorials\programmatic-editing\word-counter)
- [Chess Match Montage Generator](\examples-and-tutorials\programmatic-editing\chess-montage)

### Safety &amp; Compliance

- [Overview](\examples-and-tutorials\safety-compliance)
- [Profanity Detection](\examples-and-tutorials\safety-compliance\beep-profanity)
- [AI-Powered Content Moderation](\examples-and-tutorials\safety-compliance\remove-content)
- [AI Video Copyright Detection](\examples-and-tutorials\safety-compliance\copyright-detection)

## On this page

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Connect to VideoDB](#connect-to-videodb)
- [Upload Your Video](#upload-your-video)
    - [Preview the Original](#preview-the-original)
- [Dub Your Video](#dub-your-video)
- [View the Dubbed Video](#view-the-dubbed-video)
- [Supported Languages](#supported-languages)
    - [Example: Dub into Spanish](#example-dub-into-spanish)
- [Use Cases](#use-cases)
- [Wrap-up](#wrap-up)
- [Related Tutorials](#related-tutorials)

[Content Factory](\examples-and-tutorials\content-factory\index)

# Video Dubbing

Copy page

Dub videos into multiple languages with AI voice synthesis

Copy page

Open In Colab

<!-- image -->

## [ Overview](#overview)

VideoDB makes video dubbing incredibly simple with AI-powered translation and voice synthesis. With just **one function call** , you can dub your videos into multiple languages while preserving the original speaking style and timing. No need for complex audio editing, timeline manipulation, or third-party tools. VideoDB's `coll.dub_video()` handles everything automatically.

## [ Prerequisites](#prerequisites)

Ensure you have VideoDB installed in your environment and an API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) . The first 50 uploads are free with no credit card required!

```
! pip install videodb
```

## [ Connect to VideoDB](#connect-to-videodb)

Connect to VideoDB using your API key:

Python

Node.js

```
import videodb

# Connect to VideoDB
api_key = "your_api_key"
conn = videodb.connect( api_key = api_key)
coll = conn.get_collection()
```

```
import { connect } from 'videodb' ;

const conn = await connect ({ apiKey: process . env . VIDEO_DB_API_KEY });
const coll = await conn . getCollection ();

console . log ( "Connected to VideoDB" );
```

## [ Upload Your Video](#upload-your-video)

Upload the video you want to dub. For this example, we'll use an English video:

Python

Node.js

```
# Upload the original video (English)
video_url = "https://www.youtube.com/watch?v=0e3GPea1Tyg"
video = coll.upload( url = video_url)

print ( f "Video uploaded: { video.id } " )
```

```
// Upload the original video (English)
const videoUrl = "https://www.youtube.com/watch?v=0e3GPea1Tyg" ;
const video = await coll . uploadURL ({ url: videoUrl });

console . log ( `Video uploaded: ${ video . id } ` );
```

### [ Preview the Original](#preview-the-original)

Python

```
video.play()
```

## [ Dub Your Video](#dub-your-video)

Here's where the magic happens! Dub your video into any supported language with a single function call:

Python

Node.js

```
# Dub the video into Hindi
dubbed_video = coll.dub_video(
video_id = video.id,
language_code = "hi" # Hindi
)

print ( f "Video dubbed successfully: { dubbed_video.id } " )
```

```
// Dub the video into Hindi
const dubbedVideo = await coll . dubVideo (
video . id ,
"hi" // Hindi
);

console . log ( `Video dubbed successfully: ${ dubbedVideo . id } ` );
```

That's it! VideoDB automatically dubbed your video.

## [ View the Dubbed Video](#view-the-dubbed-video)

Generate and play your dubbed video:

Python

```
dubbed_video.play()
```

## [ Supported Languages](#supported-languages)

VideoDB supports dubbing into many languages. Simply change the `language_code` parameter:

| Language   | Code   | Language             | Code   |
|------------|--------|----------------------|--------|
| Spanish    | `es`   | Japanese             | `ja`   |
| French     | `fr`   | Korean               | `ko`   |
| German     | `de`   | Chinese (Simplified) | `zh`   |
| Italian    | `it`   | Arabic               | `ar`   |
| Portuguese | `pt`   | Russian              | `ru`   |
| Hindi      | `hi`   | ... and more!        |        |

### [ Example: Dub into Spanish](#example-dub-into-spanish)

Python

```
# Dub the same video into Spanish
spanish_dubbed = coll.dub_video(
video_id = video.id,
language_code = "es" # Spanish
)

print ( f "Spanish version created: { spanish_dubbed.id } " )

# Play the Spanish version
spanish_dubbed.play()
```

## [ Use Cases](#use-cases)

## Content Localization

Reach global audiences by dubbing your content into multiple languages

## Educational Content

Make learning materials accessible in students' native languages

## Marketing Videos

Create localized versions of promotional content

## Entertainment

Dub movies, shows, or vlogs for international viewers

## Accessibility

Provide dubbed versions for audiences who prefer audio in their native language

## [ Wrap-up](#wrap-up)

With VideoDB's `coll.dub_video()` , video dubbing is as simple as querying a database. No complex audio editing, no timeline manipulation - just one function call to create professional multilingual content.

Start dubbing your videos today and reach audiences worldwide!

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## AI Voiceovers

Add professional narration to silent footage with AI voice synthesis

## Translation &amp; Dubbing Guide

Deep dive into VideoDB's dubbing architecture and language support

[TikTok Style Lyric Video Creator](\examples-and-tutorials\content-factory\tiktok-lyric-video) [AI Voiceovers](\examples-and-tutorials\content-factory\voiceovers)

⌘ I