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

- [The Story](#the-story)
- [What You'll Build](#what-you%E2%80%99ll-build)
- [Setup](#setup)
    - [Install Dependencies](#install-dependencies)
    - [Connect to VideoDB](#connect-to-videodb)
- [Implementation](#implementation)
    - [Step 1: Connect to Your Property Stream](#step-1-connect-to-your-property-stream)
    - [Step 2: Index Scenes with Multi-Level Threat Analysis](#step-2-index-scenes-with-multi-level-threat-analysis)
    - [Step 3: Define Three-Tiered Events](#step-3-define-three-tiered-events)
    - [Step 4: Attach Alerts with Progressive Response](#step-4-attach-alerts-with-progressive-response)
- [Alert Examples](#alert-examples)
    - [Level 1: Loitering Alert (Advisory)](#level-1-loitering-alert-advisory)
    - [Level 2: Intrusion Attempt Alert (Warning)](#level-2-intrusion-attempt-alert-warning)
    - [Level 3: Property Entry Alert (Critical)](#level-3-property-entry-alert-critical)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Live Intelligence](\examples-and-tutorials\live-intelligence\index)

# Intelligent Property Intrusion Detection

Copy page

AI-powered property security system with tiered threat detection - loitering, attempts, and entry

Copy page

Open In Colab

<!-- image -->

## [ The Story](#the-story)

Have you ever felt anxious leaving your home, shop, or property unattended? What if someone's lurking around your property? What if someone's trying the door or peeking through windows? Sure - you could install IP cameras, but who has the time to watch them 24/7? Good news - you don't have to anymore. With VideoDB RTStream, you can build a smart, AI-powered property surveillance system that actively monitors live video streams, detects suspicious activity, and immediately sends alerts for escalating security breaches - all without human supervision.

## [ What You'll Build](#what-you’ll-build)

With VideoDB RTStream, you can build a tiered security system that:

- Monitors your property continuously
- Classifies threats into three levels: loitering, door interaction, and entry
- Sends escalating alerts based on threat severity
- Provides video evidence for each detection

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

### [ Step 1: Connect to Your Property Stream](#step-1-connect-to-your-property-stream)

```
rtsp_url = "rtsp://samples.rts.videodb.io:8554/intruder"
property_stream = coll.connect_rtstream(
name = "Property Security Stream" ,
url = rtsp_url,
)
```

### [ Step 2: Index Scenes with Multi-Level Threat Analysis](#step-2-index-scenes-with-multi-level-threat-analysis)

Create a scene index that monitors for all threat levels:

```
property_scene_index = property_stream.index_visuals(
batch_config = {
"type" : "time" ,
"value" : 5 ,
"frame_count" : 2 ,
},
prompt = """Monitor the area around the house closely. Detect and classify human presence
around the house as either loitering, interacting with the door/lock, or entering
the house; otherwise, consider the area safe.""" ,
name = "Property_Security_Index" ,
)
```

### [ Step 3: Define Three-Tiered Events](#step-3-define-three-tiered-events)

Create events for each threat level:

```
# Level 1: Loitering (Low Threat)
loitering_event_id = conn.create_event(
event_prompt = "Detect if a person is loitering near the house perimeter." ,
label = "loitering_near_property" ,
)

# Level 2: Door Interaction (Medium Threat)
intrusion_attempt_event_id = conn.create_event(
event_prompt = "Detect if a person is interacting with the door or visibly checking the lock." ,
label = "intrusion_attempt" ,
)

# Level 3: Property Entry (Critical Threat)
entry_event_id = conn.create_event(
event_prompt = "Detect if a person enters the house or crosses the property boundary unlawfully." ,
label = "property_entry" ,
)
```

### [ Step 4: Attach Alerts with Progressive Response](#step-4-attach-alerts-with-progressive-response)

```
webhook_url = "https://your-webhook-url.com"

# All three alerts routed to the same webhook with different priority labels
loitering_alert_id = property_scene_index.create_alert(loitering_event_id, callback_url = webhook_url)
intrusion_alert_id = property_scene_index.create_alert(intrusion_attempt_event_id, callback_url = webhook_url)
entry_alert_id = property_scene_index.create_alert(entry_event_id, callback_url = webhook_url)
```

## [ Alert Examples](#alert-examples)

### [ Level 1: Loitering Alert (Advisory)](#level-1-loitering-alert-advisory)

```
{
"event_id" : "event-loitering-001" ,
"label" : "loitering_near_property" ,
"confidence" : 0.88 ,
"explanation" : "Person detected loitering near property perimeter. Not showing signs of intent to breach." ,
"timestamp" : "2025-05-27T20:24:39.123456+00:00" ,
"start_time" : "2025-05-27T20:24:39.000000+05:30" ,
"end_time" : "2025-05-27T20:24:44.000000+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711a0-0fde-7911-b282-25bc0b4ecf65/1748444679000000-1748444684000000.m3u8"
}
```

### [ Level 2: Intrusion Attempt Alert (Warning)](#level-2-intrusion-attempt-alert-warning)

```
{
"event_id" : "event-intrusion-attempt-001" ,
"label" : "intrusion_attempt" ,
"confidence" : 0.92 ,
"explanation" : "Person is directly interacting with the door, checking the lock mechanism." ,
"timestamp" : "2025-05-27T20:30:15.123456+00:00" ,
"start_time" : "2025-05-27T20:30:15.000000+05:30" ,
"end_time" : "2025-05-27T20:30:20.000000+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711a0-0fde-7911-b282-25bc0b4ecf65/1748445015000000-1748445020000000.m3u8"
}
```

### [ Level 3: Property Entry Alert (Critical)](#level-3-property-entry-alert-critical)

```
{
"event_id" : "event-entry-breach-001" ,
"label" : "property_entry" ,
"confidence" : 0.96 ,
"explanation" : "Unauthorized entry detected! Person has crossed the property boundary and is entering the house." ,
"timestamp" : "2025-05-27T20:35:42.123456+00:00" ,
"start_time" : "2025-05-27T20:35:42.000000+05:30" ,
"end_time" : "2025-05-27T20:35:47.000000+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711a0-0fde-7911-b282-25bc0b4ecf65/1748445342000000-1748445347000000.m3u8"
}
```

## [ The Result](#the-result)

With this in place, property owners can leave home without anxiety, knowing they'll be immediately notified if anyone is:

- Loitering nearby
- Interacting with the door
- Or breaking in

The tiered alert system lets you respond appropriately:

- **Level 1 alerts** → Stay informed and monitor
- **Level 2 alerts** → Increase vigilance, contact neighbors
- **Level 3 alerts** → Contact emergency services immediately

## Explore the Full Notebook

Open the complete implementation with advanced configuration and customization options.

## [ Related Tutorials](#related-tutorials)

## Baby Crib Monitoring

AI-powered safety monitoring for home environments

## Road Safety Monitoring

Real-time traffic and accident detection system

[Baby Crib Monitoring with AI](\examples-and-tutorials\live-intelligence\baby-crib-monitoring) [Flash Flood Early Warning System](\examples-and-tutorials\live-intelligence\flash-flood-detection)

⌘ I