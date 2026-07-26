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
    - [Step 1: Connect to the Flood Monitoring Stream](#step-1-connect-to-the-flood-monitoring-stream)
    - [Step 2: Create Primary Index - Flash Flood Detection](#step-2-create-primary-index-flash-flood-detection)
    - [Step 3: Create Secondary Index - Early Warning System](#step-3-create-secondary-index-early-warning-system)
    - [Step 4: Define Three Events](#step-4-define-three-events)
    - [Step 5: Attach Alerts](#step-5-attach-alerts)
- [Alert Payloads](#alert-payloads)
    - [Flash Flood Alert (Critical Priority)](#flash-flood-alert-critical-priority)
    - [Heavy Rainfall Alert (Warning Priority)](#heavy-rainfall-alert-warning-priority)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Live Intelligence](\examples-and-tutorials\live-intelligence\index)

# Flash Flood Early Warning System

Copy page

AI-powered real-time detection of flash floods for emergency early warning

Copy page

Open In Colab

<!-- image -->

## [ The Story](#the-story)

The stunning Arizona deserts, known for their dry riverbeds and scenic beauty, hide a deadly risk. During the summer monsoon, sudden torrential rains can trigger flash floods in these seemingly harmless dry zones - with little or no warning. Conventional alert systems relying on rain gauges or weather satellites often fail to deliver timely, location-specific warnings. By the time a danger alert is sent, it might already be too late. But we have a smarter way. With VideoDB RTStream, we can install real-time cameras near flood-prone areas and let AI continuously monitor the visuals. As soon as the AI detects signs of a flash flood - like a sudden surge of water through dry land - it can instantly send alerts, giving local authorities and tourists precious moments to act.

## [ What You'll Build](#what-you’ll-build)

With VideoDB RTStream, you can build a two-layer monitoring system that:

- Continuously monitors dry riverbeds and surrounding areas
- Detects flash floods immediately upon occurrence
- Identifies heavy rainfall as early warning signals
- Alerts for people in distress requiring rescue
- Sends real-time notifications to emergency services

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

### [ Step 1: Connect to the Flood Monitoring Stream](#step-1-connect-to-the-flood-monitoring-stream)

```
rtsp_url = "rtsp://samples.rts.videodb.io:8554/floods"
flood_stream = coll.connect_rtstream(
name = "Flood Detection Stream" ,
url = rtsp_url,
)
```

### [ Step 2: Create Primary Index - Flash Flood Detection](#step-2-create-primary-index-flash-flood-detection)

Create the primary scene index focused on immediate flood detection with more frequent analysis:

```
flood_scene_index = flood_stream.index_visuals(
batch_config = {
"type" : "time" ,
"value" : 5 ,
"frame_count" : 3 ,
},
prompt = """Monitor the dry riverbed and surrounding area. If moving water is detected
across the land, identify it as a flash flood and describe the scene.""" ,
name = "Flash_Flood_Detection_Index" ,
)
```

The `frame_count: 3` captures 3 frames every 5 seconds for detailed water movement analysis.

### [ Step 3: Create Secondary Index - Early Warning System](#step-3-create-secondary-index-early-warning-system)

Create a second index on the same stream for early warning detection:

```
early_warning_index = flood_stream.index_visuals(
batch_config = {
"type" : "time" ,
"value" : 15 ,
"frame_count" : 1 ,
},
prompt = """Monitor the dry riverbed and surrounding area. In case you detect heavy rainfall
mention 'heavy rainfall detected'. If you detect a person stuck in the area during
rainfall or flash flood mention 'person detected, rescue needed'""" ,
name = "Early_Warning_Index" ,
)
```

The longer interval ( `value: 15` ) and single frame are sufficient for general rainfall and rescue detection.

### [ Step 4: Define Three Events](#step-4-define-three-events)

Create events for the three alert types:

```
# Flash Flood Event
flood_event_id = conn.create_event(
event_prompt = "Detect a flash flood - sudden water surge across the riverbed." ,
label = "flash_flood" ,
)

# Heavy Rainfall Event (early warning)
rainfall_event_id = conn.create_event(
event_prompt = "Detect heavy rainfall - potential precursor to flooding." ,
label = "heavy_rainfall" ,
)

# Rescue Needed Event
rescue_event_id = conn.create_event(
event_prompt = "Detect a person in distress or stuck - rescue needed." ,
label = "person_rescue_needed" ,
)
```

### [ Step 5: Attach Alerts](#step-5-attach-alerts)

```
webhook_url = "https://your-webhook-url.com"

# Primary flood detection alerts
flood_alert_id = flood_scene_index.create_alert(flood_event_id, callback_url = webhook_url)

# Early warning alerts
rainfall_alert_id = early_warning_index.create_alert(rainfall_event_id, callback_url = webhook_url)
rescue_alert_id = early_warning_index.create_alert(rescue_event_id, callback_url = webhook_url)
```

## [ Alert Payloads](#alert-payloads)

### [ Flash Flood Alert (Critical Priority)](#flash-flood-alert-critical-priority)

When a flood is detected, the system sends an immediate alert with the exact location and video:

```
{
"event_id" : "event-flood-detection" ,
"label" : "flash_flood" ,
"confidence" : 0.95 ,
"explanation" : "Flash flood detected! Water is flowing rapidly and forcefully through the riverbed. The water appears muddy, carrying sediment and debris. Multiple people visible on rocky banks." ,
"timestamp" : "2025-05-29T07:17:51.123456+00:00" ,
"start_time" : "2025-05-29T07:17:51.000000+05:30" ,
"end_time" : "2025-05-29T07:17:56.000000+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711a0-0fde-7911-b282-25bc0b4ecf65/1748475471000000-1748475476000000.m3u8"
}
```

### [ Heavy Rainfall Alert (Warning Priority)](#heavy-rainfall-alert-warning-priority)

Early warning alerts help authorities respond proactively:

```
{
"event_id" : "event-rainfall-warning" ,
"label" : "heavy_rainfall" ,
"confidence" : 0.85 ,
"explanation" : "Heavy rainfall detected in the monitoring area. Conditions favorable for flash flooding." ,
"timestamp" : "2025-05-29T07:10:00.000000+00:00" ,
"start_time" : "2025-05-29T07:10:00.000000+05:30" ,
"end_time" : "2025-05-29T07:10:15.000000+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711a0-0fde-7911-b282-25bc0b4ecf65/1748475000000000-1748475015000000.m3u8"
}
```

## [ The Result](#the-result)

With this system in place, communities, tourists, and local authorities in Arizona's desert regions can receive immediate alerts when a dangerous flash flood occurs - gaining critical seconds to take cover, clear routes, or initiate rescues. The two-layer system ensures:

- **Real-time flood detection** for immediate response
- **Early rainfall warnings** for proactive preparation
- **Rescue alerts** for people in distress

## Explore the Full Notebook

Open the complete implementation with advanced monitoring features and configuration options.

## [ Related Tutorials](#related-tutorials)

## Baby Crib Monitoring with AI

Real-time safety monitoring for infants with instant alerts

## Property Intrusion Detection

Intelligent security system with tiered threat detection

[Intelligent Property Intrusion Detection](\examples-and-tutorials\live-intelligence\intrusion-detection) [Multi-Use Road Monitoring System](\examples-and-tutorials\live-intelligence\road-monitoring)

⌘ I