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
- [7-Camera Surveillance Network](#7-camera-surveillance-network)
- [Setup](#setup)
    - [Install Dependencies](#install-dependencies)
    - [Connect to VideoDB](#connect-to-videodb)
- [Implementation](#implementation)
    - [Step 1: Define All 7 Camera Streams](#step-1-define-all-7-camera-streams)
    - [Step 2: Create Shared Indexes on All Cameras](#step-2-create-shared-indexes-on-all-cameras)
    - [Step 3: Define 5 Shared Security Events](#step-3-define-5-shared-security-events)
    - [Step 4: Attach Alerts to All 7 Cameras](#step-4-attach-alerts-to-all-7-cameras)
- [Alert Examples](#alert-examples)
    - [Unattended Luggage Alert (Critical Priority)](#unattended-luggage-alert-critical-priority)
    - [Large Crowd Formation Alert](#large-crowd-formation-alert)
    - [Person with Trolley Alert (Tracking)](#person-with-trolley-alert-tracking)
- [Synchronized Multi-Angle Evidence](#synchronized-multi-angle-evidence)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Live Intelligence](\examples-and-tutorials\live-intelligence\index)

# Multi-Camera Public Safety Surveillance

Copy page

AI-powered 7-camera surveillance system for city-wide public safety monitoring with synchronized alerting

Copy page

Open In Colab

<!-- image -->

## [ The Challenge](#the-challenge)

Modern cities face growing challenges in ensuring public safety. From crowded metros to busy intersections, monitoring many locations in real-time is tough. Traditional systems rely on humans watching multiple screens - costly, error-prone, and unable to correlate events across cameras. What if AI could monitor all feeds, detect incidents instantly, and alert authorities automatically?

## [ What You'll Build](#what-you’ll-build)

VideoDB RTStream brings AI-powered intelligence to multi-camera systems. In this guide, you'll build a surveillance network that:

- Connects 7 synchronized camera feeds across a public space
- Detects 5 types of security incidents simultaneously
- Monitors 35 event streams (7 cameras × 5 events)
- Generates synchronized multi-angle evidence for forensic analysis
- Sends real-time alerts to security authorities

## [ 7-Camera Surveillance Network](#7-camera-surveillance-network)

```
🏙️ City Public Square - 7 Camera System

├── CAM 1: Plaza Overview (High Angle - East)
│   └── rtsp://samples.rts.videodb.io:8554/pub-cam1
│
├── CAM 2: Main Walkway (Close Up)
│   └── rtsp://samples.rts.videodb.io:8554/pub-cam2
│
├── CAM 3: Stairway Junction
│   └── rtsp://samples.rts.videodb.io:8554/pub-cam3
│
├── CAM 4: Central Plaza (Mid Angle)
│   └── rtsp://samples.rts.videodb.io:8554/pub-cam4
│
├── CAM 5: Building Entrance (Eye Level)
│   └── rtsp://samples.rts.videodb.io:8554/pub-cam5
│
├── CAM 6: Wide Plaza View (West)
│   └── rtsp://samples.rts.videodb.io:8554/pub-cam6
│
└── CAM 7: Ground-Level Cross View (Center)
└── rtsp://samples.rts.videodb.io:8554/pub-cam7
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

### [ Step 1: Define All 7 Camera Streams](#step-1-define-all-7-camera-streams)

```
cameras = {
"plaza_overview" : "rtsp://samples.rts.videodb.io:8554/pub-cam1" ,
"main_walkway" : "rtsp://samples.rts.videodb.io:8554/pub-cam2" ,
"stairway_junction" : "rtsp://samples.rts.videodb.io:8554/pub-cam3" ,
"central_plaza" : "rtsp://samples.rts.videodb.io:8554/pub-cam4" ,
"building_entrance" : "rtsp://samples.rts.videodb.io:8554/pub-cam5" ,
"wide_plaza_view" : "rtsp://samples.rts.videodb.io:8554/pub-cam6" ,
"ground_level_cross" : "rtsp://samples.rts.videodb.io:8554/pub-cam7" ,
}

# Connect all camera streams
rtstreams = {}
for cam_name, rtsp_url in cameras.items():
rtstreams[cam_name] = coll.connect_rtstream(
name = f "Surveillance: { cam_name.replace( '_' , ' ' ).title() } " ,
url = rtsp_url,
)
```

### [ Step 2: Create Shared Indexes on All Cameras](#step-2-create-shared-indexes-on-all-cameras)

Define one comprehensive analysis prompt and create indexes on all 7 streams:

```
analysis_prompt = """Analyze this public surveillance footage and identify key activities:
1. Individuals or groups with notable items (suspicious gatherings, unusual luggage)
2. Crowd behavior (large groups, sudden dispersal, running, congestion)
3. Vehicle activity (unusual stopping, idling, vans/trucks in pedestrian areas)
4. Unusual object detection (unattended bags, boxes in public spaces, abandoned items)
5. General patterns of movement and deviations from norm
6. Notable appearances or characteristics (distinctive clothing, unusual behavior)

Be specific about appearance and location of events within camera's view."""

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
name = f "Surveillance_Analytics_ { cam_name.upper() } " ,
)
```

### [ Step 3: Define 5 Shared Security Events](#step-3-define-5-shared-security-events)

Create events that apply across all cameras:

```
# Unattended Luggage (High Priority)
luggage_event_id = conn.create_event(
event_prompt = "Detect luggage, backpacks, or packages left unattended." ,
label = "unattended_luggage" ,
)

# Large Crowd Formation (Alert)
crowd_event_id = conn.create_event(
event_prompt = "Identify when >4 people gather quickly in a concentrated area." ,
label = "large_crowd_formation" ,
)

# Person with Trolley (Tracking)
trolley_event_id = conn.create_event(
event_prompt = "Detect any person with trolley bag or rolling suitcase." ,
label = "person_with_trolley" ,
)

# Person in Red Coat (Tracking)
red_coat_event_id = conn.create_event(
event_prompt = "Identify person wearing a distinct red coat or jacket." ,
label = "person_in_red_coat" ,
)

# Suspicious Loitering (Advisory)
loitering_event_id = conn.create_event(
event_prompt = "Detect individuals loitering without clear purpose or unusual positioning." ,
label = "suspicious_loitering" ,
)
```

### [ Step 4: Attach Alerts to All 7 Cameras](#step-4-attach-alerts-to-all-7-cameras)

```
webhook_url = "https://your-security-center-webhook.com"

event_ids = {
"luggage" : luggage_event_id,
"crowd" : crowd_event_id,
"trolley" : trolley_event_id,
"red_coat" : red_coat_event_id,
"loitering" : loitering_event_id,
}

# Create alerts for all 5 events on all 7 cameras (35 total alerts)
for cam_name, scene_index in scene_indexes.items():
for event_type, event_id in event_ids.items():
scene_index.create_alert(event_id, callback_url = webhook_url)
```

Now you have a comprehensive 7-camera × 5-event surveillance grid (35 alert streams).

## [ Alert Examples](#alert-examples)

### [ Unattended Luggage Alert (Critical Priority)](#unattended-luggage-alert-critical-priority)

```
{
"event_id" : "event-luggage-001" ,
"label" : "unattended_luggage" ,
"confidence" : 0.96 ,
"explanation" : "A black backpack is detected on the plaza ground with no person visibly attached to it. Has been stationary for >1 minute." ,
"timestamp" : "2025-09-10T17:02:15.811085+00:00" ,
"start_time" : "2025-09-10T22:31:50.886736+05:30" ,
"end_time" : "2025-09-10T22:32:05.886736+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711db-1086-7750-ba79-8f47a4fed603/1757523710000000-1757523726000000.m3u8"
}
```

### [ Large Crowd Formation Alert](#large-crowd-formation-alert)

```
{
"event_id" : "event-crowd-001" ,
"label" : "large_crowd_formation" ,
"confidence" : 0.92 ,
"explanation" : "Multiple individuals (8+) rapidly gathering in central plaza area. Unusual congregation pattern." ,
"timestamp" : "2025-09-10T17:15:42.123456+00:00" ,
"start_time" : "2025-09-10T22:45:30.000000+05:30" ,
"end_time" : "2025-09-10T22:45:45.000000+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711db-1086-7750-ba79-8f47a4fed603/1757524530000000-1757524545000000.m3u8"
}
```

### [ Person with Trolley Alert (Tracking)](#person-with-trolley-alert-tracking)

```
{
"event_id" : "event-trolley-001" ,
"label" : "person_with_trolley" ,
"confidence" : 0.95 ,
"explanation" : "Female with black rolling suitcase detected moving through plaza." ,
"timestamp" : "2025-09-10T17:02:15.811085+00:00" ,
"start_time" : "2025-09-10T22:31:50.886736+05:30" ,
"end_time" : "2025-09-10T22:32:05.886736+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711db-1086-7750-ba79-8f47a4fed603/1757523710000000-1757523726000000.m3u8"
}
```

## [ Synchronized Multi-Angle Evidence](#synchronized-multi-angle-evidence)

When an incident is detected, you can retrieve synchronized clips from all 7 cameras:

```
# Extract incident timestamp from alert
incident_epoch = 1757523730 # from alert data

# Generate 7-angle synchronized clip (±10 seconds)
time_window = 10
evidence_clips = {}

for cam_name, rtstream in rtstreams.items():
stream_url = rtstream.generate_stream(
start = incident_epoch - time_window,
end = incident_epoch + time_window
)
evidence_clips[cam_name] = stream_url

# Now have complete multi-angle evidence for forensic analysis
```

## [ The Result](#the-result)

This demo shows how AI turns raw surveillance feeds into actionable intelligence for:

- **Public safety monitoring** across wide areas
- **Crowd management** and anomaly detection
- **Security threat detection** in real-time
- **Forensic investigation** with multi-angle evidence
- **Real-time incident response** with synchronized playback

Key capabilities:

- **35 Event Streams** - Comprehensive coverage of 7 camera angles with 5 security events each
- **Sub-Second Alerts** - Instant notification when incidents occur
- **Multi-Angle Evidence** - Synchronized clips from all cameras for investigations
- **Scalability** - Pattern can extend to 10, 20, or 100+ cameras
- **24/7 Monitoring** - Fully automated, no human fatigue

## Explore the Full Notebook

Open the complete implementation with webhook setup, ngrok integration, and forensic analysis.

## [ Related Tutorials](#related-tutorials)

## Property Intrusion Detection

Intelligent security system with tiered threat detection

## Multi-Camera Basketball Analytics

Real-time sports analysis with synchronized playback

[Multi-Camera Basketball Analytics](\examples-and-tutorials\live-intelligence\multicam-basketball-analysis) [TwelveLabs Integration](\examples-and-tutorials\live-intelligence\twelvelabs-integration)

⌘ I