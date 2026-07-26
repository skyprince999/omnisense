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
- [Violations Detected](#violations-detected)
- [Setup](#setup)
    - [Install Dependencies](#install-dependencies)
    - [Connect to VideoDB](#connect-to-videodb)
- [Implementation](#implementation)
    - [Step 1: Connect to Your Roadcam Stream](#step-1-connect-to-your-roadcam-stream)
    - [Step 2: Index Scenes with Violation Analysis](#step-2-index-scenes-with-violation-analysis)
    - [Step 3: Create Violation Event](#step-3-create-violation-event)
    - [Step 4: Attach Alert for Automated Reporting](#step-4-attach-alert-for-automated-reporting)
- [Alert Example](#alert-example)
- [Integration with Enforcement Systems](#integration-with-enforcement-systems)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Live Intelligence](\examples-and-tutorials\live-intelligence\index)

# Dashcam Monitoring of Traffic

Copy page

Real-time traffic enforcement system detecting violations like no helmet, red lights, and unsafe driving

Copy page

Open In Colab

<!-- image -->

## [ The Challenge](#the-challenge)

Traffic violations cause preventable accidents and deaths every day. From riders without helmets to drivers using mobile phones, unsafe behavior on roads puts lives at risk. Traditional enforcement requires traffic police to manually monitor roads - costly, limited in coverage, and often reactive rather than preventive. What if AI could automatically detect violations in real-time and generate evidence for enforcement? This is where AI-powered dashcam monitoring comes in.

## [ What You'll Build](#what-you’ll-build)

With VideoDB RTStream, you can build an automated traffic violation detection system that:

- Monitors live road feeds continuously
- Detects multiple violation types automatically
- Generates video evidence for enforcement
- Sends real-time alerts to traffic authorities
- Works 24/7 without manual supervision

## [ Violations Detected](#violations-detected)

The system monitors for six critical violations:

- **No Helmet** - Two-wheeler riders without proper head protection
- **Mobile Phone Use** - Drivers operating vehicles while using phones
- **Wrong Side Driving** - Vehicles traveling against traffic flow
- **Red Light Violation** - Vehicles crossing intersections during red signals
- **Triple Riding** - More than two people on a single two-wheeler
- **No Seatbelt** - Drivers or passengers without seatbelt protection

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

### [ Step 1: Connect to Your Roadcam Stream](#step-1-connect-to-your-roadcam-stream)

```
rtsp_url = "rtsp://your-dashcam-or-roadcam-url"
roadcam_stream = coll.connect_rtstream(
name = "Traffic Violation Detector" ,
url = rtsp_url,
)
```

### [ Step 2: Index Scenes with Violation Analysis](#step-2-index-scenes-with-violation-analysis)

Create a scene index tuned for capturing traffic violations with focused frame sampling:

```
violation_index = roadcam_stream.index_visuals(
batch_config = {
"type" : "time" ,
"value" : 7 ,
"frame_count" : 5 ,
},
prompt = """Analyze this roadcam footage and identify traffic violations by monitoring:
- Helmet compliance for two-wheelers
- Mobile phone usage while driving
- Vehicle positioning on correct lanes
- Seatbelt usage
- Occupancy violations
- Signal compliance

Focus on the following violations:
1. NO HELMET: Two-wheeler rider or pillion not wearing a helmet
2. MOBILE PHONE USE: Driver using mobile phone while operating the vehicle
3. WRONG SIDE DRIVING: Vehicle traveling against the designated traffic flow
4. RED LIGHT VIOLATION: Vehicle crossing when traffic signal is red
5. TRIPLE RIDING: More than two people on a single two-wheeler
6. NO SEATBELT: Driver or front passenger not wearing seatbelt""" ,
name = "Traffic_Violation_Detection_Index" ,
)
```

The `frame_count: 5` captures multiple angles of each violation for clear evidence.

### [ Step 3: Create Violation Event](#step-3-create-violation-event)

```
violation_event_id = conn.create_event(
event_prompt = """Detect when a traffic rule violation occurs, such as no helmet, mobile phone use,
wrong side driving, red light violation, triple riding, or no seatbelt.
Your explanation should clearly mention:
- Traffic Rule Violated
- Vehicle type and color
- License plate number if visible
- Violation type
- Brief description of what was observed""" ,
label = "traffic_violation" ,
)
```

### [ Step 4: Attach Alert for Automated Reporting](#step-4-attach-alert-for-automated-reporting)

```
webhook_url = "https://your-traffic-authority-webhook.com"
violation_alert_id = violation_index.create_alert(violation_event_id, callback_url = webhook_url)
```

## [ Alert Example](#alert-example)

When a violation is detected, the system sends structured evidence:

```
{
"event_id" : "event-violation-no-helmet" ,
"label" : "traffic_violation" ,
"confidence" : 0.95 ,
"explanation" : "Traffic Rule Violated: NO HELMET
Vehicle: Orange scooter
License Plate: DL 3S CW 4952
Violation: Both rider and pillion not wearing helmets
Description: The rider and pillion rider on the orange scooter are clearly not wearing helmets, which is a critical safety violation." ,
"timestamp" : "2025-05-29T04:57:44.123456+00:00" ,
"start_time" : "2025-05-29T10:27:20.000000+05:30" ,
"end_time" : "2025-05-29T10:27:27.000000+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711a0-0fde-7911-b282-25bc0b4ecf65/1748475396000000-1748475407000000.m3u8"
}
```

The structured explanation makes it easy to automatically process violations for enforcement.

## [ Integration with Enforcement Systems](#integration-with-enforcement-systems)

The alerts can be integrated with existing traffic enforcement workflows: **Automated Report Generation:**

- Extract vehicle details and license plate
- Generate violation evidence video
- Create standardized enforcement notice
- Route to appropriate authority

**Data-Driven Enforcement:**

- Track violation hotspots
- Identify repeat offenders
- Optimize traffic enforcement resources
- Measure safety improvements

## [ The Result](#the-result)

This system enables automated enforcement of traffic rules, reducing need for manual traffic police monitoring and improving road safety through instant violation detection and alerts. Key benefits:

- **24/7 Monitoring** - No breaks, always watching
- **Instant Evidence** - Video proof for every violation
- **Consistent Enforcement** - AI doesn't have bias or fatigue
- **Data Insights** - Analytics on violation patterns and hotspots
- **Deterrent Effect** - Known monitoring discourages violations

## Explore the Full Notebook

Open the complete implementation with additional configuration and integration examples.

## [ Related Tutorials](#related-tutorials)

## Traffic Violations Detection

Real-time detection of helmet violations and traffic rule breaking

## Road Monitoring System

Multi-use road monitoring for accidents and congestion

[Multi-Use Road Monitoring System](\examples-and-tutorials\live-intelligence\road-monitoring) [Traffic Violation Detection](\examples-and-tutorials\live-intelligence\traffic-violations)

⌘ I