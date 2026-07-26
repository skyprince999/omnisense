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

- [The Challenge](#the-challenge)
- [What You'll Build](#what-you%E2%80%99ll-build)
- [Multi-Camera Setup](#multi-camera-setup)
- [Setup](#setup)
    - [Install Dependencies](#install-dependencies)
    - [Connect to VideoDB](#connect-to-videodb)
- [Implementation](#implementation)
    - [Step 1: Connect All Three Camera Feeds](#step-1-connect-all-three-camera-feeds)
    - [Step 2: Create Shared Indexes on All Cameras](#step-2-create-shared-indexes-on-all-cameras)
    - [Step 3: Define Shared Events](#step-3-define-shared-events)
    - [Step 4: Attach Alerts to All Cameras](#step-4-attach-alerts-to-all-cameras)
- [Alert Example](#alert-example)
- [Synchronized Playback](#synchronized-playback)
- [Advanced: Webhook Integration with ngrok](#advanced-webhook-integration-with-ngrok)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Live Intelligence](\examples-and-tutorials\live-intelligence\index)

# Multi-Camera Basketball Analytics

Copy page

Real-time 3-camera basketball monitoring with synchronized multi-angle highlight detection

Copy page

Open In Colab

<!-- image -->

## [ The Challenge](#the-challenge)

Modern sports analysis faces growing challenges in providing real-time insights. From fast-paced plays to subtle player movements, monitoring every aspect of the game is tough. Traditional broadcasters use multiple camera angles but lack AI intelligence to automatically detect key moments and generate synchronized multi-angle highlights in real-time. What if AI could monitor all feeds, detect key plays instantly, and generate highlights automatically?

## [ What You'll Build](#what-you’ll-build)

VideoDB RTStream brings AI-powered intelligence to multi-camera sports systems. In this guide, you'll build a system that:

- Connects 3 synchronized camera feeds (main court + two baskets)
- Detects key basketball events in real-time
- Sends alerts for every highlight across all angles
- Generates synchronized multi-angle video clips for playback

## [ Multi-Camera Setup](#multi-camera-setup)

```
🏀 Basketball Arena - 3 Camera System

├── CAM 1: Main Court Field (Wide Angle)
│   └── rtsp://samples.rts.videodb.io:8554/bb-cam1
│
├── CAM 2: North Basket Area Field (Close Up)
│   └── rtsp://samples.rts.videodb.io:8554/bb-cam2
│
└── CAM 3: South Basket Area Field (Close Up)
└── rtsp://samples.rts.videodb.io:8554/bb-cam3
```

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

### [ Step 1: Connect All Three Camera Feeds](#step-1-connect-all-three-camera-feeds)

```
# Camera URLs
cameras = {
"main_court" : "rtsp://samples.rts.videodb.io:8554/bb-cam1" ,
"north_basket" : "rtsp://samples.rts.videodb.io:8554/bb-cam2" ,
"south_basket" : "rtsp://samples.rts.videodb.io:8554/bb-cam3"
}

# Connect all streams
rtstreams = {}
for cam_name, rtsp_url in cameras.items():
rtstreams[cam_name] = coll.connect_rtstream(
name = f "Basketball { cam_name.replace( '_' , ' ' ).title() } " ,
url = rtsp_url,
)
```

### [ Step 2: Create Shared Indexes on All Cameras](#step-2-create-shared-indexes-on-all-cameras)

Define one analysis prompt and create indexes on all streams:

```
analysis_prompt = """Analyze this basketball game footage and describe:
1. Player positions and movements on the court
2. Ball location and which team has possession
3. Any significant events (baskets scored, fouls, free throws, timeouts)
4. Defensive and offensive plays being executed
5. Crowd reactions or unusual activities"""

# Create scene indexes for all cameras
scene_indexes = {}
for cam_name, rtstream in rtstreams.items():
scene_indexes[cam_name] = rtstream.index_visuals(
batch_config = {
"type" : "time" ,
"value" : 15 ,
"frame_count" : 1 ,
},
prompt = analysis_prompt,
name = f "Basketball_Analytics_ { cam_name.upper() } " ,
)
```

### [ Step 3: Define Shared Events](#step-3-define-shared-events)

Create three events that apply across all camera angles:

```
# Basket Scored
basket_event_id = conn.create_event(
event_prompt = "Detect when a basket is scored - ball through hoop, celebrations, score change." ,
label = "basket_scored" ,
)

# Foul Detected
foul_event_id = conn.create_event(
event_prompt = "Detect fouls, aggressive behavior, or rule violations." ,
label = "player_foul" ,
)

# Timeout Called
timeout_event_id = conn.create_event(
event_prompt = "Detect when a timeout is called - players huddle or referee signals." ,
label = "timeout_called" ,
)
```

### [ Step 4: Attach Alerts to All Cameras](#step-4-attach-alerts-to-all-cameras)

```
webhook_url = "https://your-webhook-url.com"

# Create alerts for all events on all cameras
for cam_name, scene_index in scene_indexes.items():
scene_index.create_alert(basket_event_id, callback_url = webhook_url)
scene_index.create_alert(foul_event_id, callback_url = webhook_url)
scene_index.create_alert(timeout_event_id, callback_url = webhook_url)
```

Now you have 9 total alerts (3 events × 3 cameras).

## [ Alert Example](#alert-example)

When a basket is scored, each camera sends an alert:

```
{
"event_id" : "event-basket-scored" ,
"label" : "basket_scored" ,
"confidence" : 0.95 ,
"explanation" : "The ball is directly above the rim and net, descending through the hoop, indicating a basket is being scored." ,
"timestamp" : "2025-09-10T11:21:16.614553+00:00" ,
"start_time" : "2025-09-10T16:50:45.698108+05:30" ,
"end_time" : "2025-09-10T16:51:00.698108+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711db-1086-7750-ba79-8f47a4fed603/1757503245000000-1757503261000000.m3u8"
}
```

The same event triggers on all 3 cameras, giving you synchronized multi-angle evidence.

## [ Synchronized Playback](#synchronized-playback)

Generate synchronized clips from all cameras for the same moment:

```
# When you receive a basket alert with timestamp, extract it
alert_timestamp = "2025-09-10T16:50:45.698108+05:30"
import datetime
epoch_time = int (datetime.datetime.fromisoformat(alert_timestamp.replace( "Z" , "+00:00" )).timestamp())

# Generate streams from all cameras for same time window (±5 seconds)
time_window = 5
synchronized_streams = {}

for cam_name, rtstream in rtstreams.items():
stream_url = rtstream.generate_stream(
start = epoch_time - time_window,
end = epoch_time + time_window
)
synchronized_streams[cam_name] = stream_url
```

Now you have 3 synchronized video clips from different angles for the same moment.

## [ Advanced: Webhook Integration with ngrok](#advanced-webhook-integration-with-ngrok)

For real-time event handling, set up ngrok tunneling:

```
# Terminal: Start ngrok tunnel
ngrok http 5000
# Get public URL: https://xxxx-xxxx-xxxx.ngrok.io
```

Then use this public webhook URL when creating alerts for instant event notifications.

## [ The Result](#the-result)

This demo shows how AI turns raw game feeds into actionable sports intelligence, enabling:

- **Real-time game analysis** across multiple angles
- **Instant highlight generation** with synchronized playback
- **Multi-angle replay** for coaches and analysts
- **Automated event detection** across multiple viewpoints
- **Forensic evidence** for rule reviews and disputes

## Explore the Full Notebook

Open the complete implementation with webhook setup, ngrok tunneling, and data processing.

## [ Related Tutorials](#related-tutorials)

## Cricket Highlights Detection

Auto-detect sports highlights in real-time

## Multi-Camera Public Surveillance

Enterprise-scale multi-camera monitoring system

[Live Cricket Highlight Detection](\examples-and-tutorials\live-intelligence\cricket-match-monitoring) [Multi-Camera Public Safety Surveillance](\examples-and-tutorials\live-intelligence\multicam-public-surveillance)

⌘ I