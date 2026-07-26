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

- [Storytime: Why This Matters](#storytime-why-this-matters)
- [Enter VideoDB RTStream](#enter-videodb-rtstream)
- [What You'll Learn](#what-you%E2%80%99ll-learn)
- [Setup](#setup)
    - [Install Dependencies](#install-dependencies)
    - [Connect to VideoDB](#connect-to-videodb)
- [Implementation](#implementation)
    - [Step 1: Connect to the RTSP Stream](#step-1-connect-to-the-rtsp-stream)
    - [Step 2: Index Scenes with AI Descriptions](#step-2-index-scenes-with-ai-descriptions)
    - [Step 3: Define an Event for Baby Escape](#step-3-define-an-event-for-baby-escape)
    - [Step 4: Attach an Alert for Real-Time Notifications](#step-4-attach-an-alert-for-real-time-notifications)
- [What You Receive](#what-you-receive)
- [Wrapping Up: Peace of Mind](#wrapping-up-peace-of-mind)
- [Related Tutorials](#related-tutorials)

[Live Intelligence](\examples-and-tutorials\live-intelligence\index)

# Baby Crib Monitoring with AI

Copy page

AI-powered baby safety monitoring system that detects escape attempts and sends real-time alerts

Copy page

Open In Colab

<!-- image -->

## [ Storytime: Why This Matters](#storytime-why-this-matters)

Meet **Vidit** and **Meghna** - a young couple juggling demanding jobs and household responsibilities. After a long, exhausting day, all they hope for is a peaceful night's sleep. But their energetic little one has other plans. Their child, once safely tucked into his crib, has recently discovered how to climb out. While the parents sleep, unaware, the baby risks injury by wandering unsupervised at night. How can they keep him safe without losing their much-needed rest?

## [ Enter VideoDB RTStream](#enter-videodb-rtstream)

**VideoDB** offers the perfect solution for this problem. Using **RTStream** , we can let AI continuously monitor a live video feed, index scenes, detect specific events like **baby attempting to climb out of the crib** , and instantly send alerts to the parents when something risky happens. In this guide, **Vidit and Meghna install an IP camera near the crib** and use **VideoDB RTStream** to power an AI monitoring system. As soon as the baby makes a move to climb out, AI detects it, triggers an event, and fires a real-time alert so the parents can step in.

## [ What You'll Learn](#what-you’ll-learn)

By the end of this guide, you'll learn how to:

- Connect a live RTSP video stream to VideoDB
- Continuously analyze video scenes using AI-generated natural language descriptions
- Detect specific events like *"baby escaping crib"*
- Trigger real-time alerts on such events

## [ Setup](#setup)

### [ Install Dependencies](#install-dependencies)

```
pip install videodb
```

### [ Connect to VideoDB](#connect-to-videodb)

```
import videodb

api_key = "your_api_key"
conn = videodb.connect( api_key = api_key)
coll = conn.get_collection()
```

## [ Implementation](#implementation)

### [ Step 1: Connect to the RTSP Stream](#step-1-connect-to-the-rtsp-stream)

Connect to the live video stream of the crib using its RTSP URL. In this demo, the stream is running at `rtsp://samples.rts.videodb.io:8554/crib` .

```
rtsp_url = "rtsp://samples.rts.videodb.io:8554/crib"
crib_stream = coll.connect_rtstream(
name = "Baby Crib Monitor" ,
url = rtsp_url,
)
```

### [ Step 2: Index Scenes with AI Descriptions](#step-2-index-scenes-with-ai-descriptions)

Create a real-time scene index that periodically analyzes the video and generates natural language descriptions of what's happening in the crib. The AI model watches for activity such as the baby moving, sitting, or attempting to climb out.

```
crib_scene_index = crib_stream.index_visuals(
batch_config = {
"type" : "time" ,
"value" : 10 ,
"frame_count" : 1 ,
},
prompt = "Describe the activity of the baby kept inside a baby crib. Notice if baby climbs out or attempts to escape." ,
name = "Baby_Crib_Index" ,
)
```

The `batch_config` defines how frequently the AI analyzes the stream:

- `value: 10` - Analyze every 10 seconds
- `frame_count: 1` - Extract 1 frame per analysis window

### [ Step 3: Define an Event for Baby Escape](#step-3-define-an-event-for-baby-escape)

Create an event in VideoDB to detect when the AI spots the baby attempting to climb out.

```
event_id = conn.create_event(
event_prompt = "Detect if the baby is trying to escape or climbing out of the crib." ,
label = "baby_escape" ,
)
```

The event acts as a filter - when the AI's scene description matches this prompt, it triggers the event.

### [ Step 4: Attach an Alert for Real-Time Notifications](#step-4-attach-an-alert-for-real-time-notifications)

Link a real-time alert to this event, which will notify the parents instantly through a webhook.

```
webhook_url = "https://your-webhook-url.com"

alert_id = crib_scene_index.create_alert(
event_id,
callback_url = webhook_url,
)
```

## [ What You Receive](#what-you-receive)

When a baby escape attempt is detected, your webhook receives a detailed alert payload:

```
{
"event_id" : "event-3adc40d26d6fed0d" ,
"label" : "baby_escape" ,
"confidence" : 0.95 ,
"explanation" : "The baby is actively trying to climb out of the crib by holding onto the top rail and attempting to pull itself up, which indicates an escape attempt." ,
"timestamp" : "2025-05-28T23:36:39.979133+00:00" ,
"start_time" : "2025-05-29T05:06:36.612197+05:30" ,
"end_time" : "2025-05-29T05:06:46.612197+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711a0-0fde-7911-b282-25bc0b4ecf65/1748475396000000-1748475407000000.m3u8"
}
```

## [ Wrapping Up: Peace of Mind](#wrapping-up-peace-of-mind)

With this system in place, Vidit and Meghna can finally sleep peacefully, knowing their child is being safely monitored through AI-driven surveillance. But this is just one story. What if the same system could:

- Monitor an elderly parent at home - detecting falls or prolonged inactivity?
- Watch over a pet while the family is away, alerting them if it leaves a safe zone?
- Notify parents when a toddler approaches dangerous areas like staircases or kitchen counters?

The possibilities of real-time video intelligence at home are endless. **What would you monitor next?**

## Explore the Full Notebook

Open the complete implementation with additional features like WebSocket connections, audio indexing, and helper functions for stream visualization.

## [ Related Tutorials](#related-tutorials)

## Property Intrusion Detection

Intelligent security system with tiered threat detection

## Flash Flood Early Warning

Natural disaster monitoring with emergency alerts

[Overview](\examples-and-tutorials\live-intelligence) [Intelligent Property Intrusion Detection](\examples-and-tutorials\live-intelligence\intrusion-detection)

⌘ I