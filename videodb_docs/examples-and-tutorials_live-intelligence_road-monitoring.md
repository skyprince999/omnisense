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
    - [Part 1: Accident Detection at Toll Plaza](#part-1-accident-detection-at-toll-plaza)
    - [Part 2: Traffic Violation Detection at Toll Booth](#part-2-traffic-violation-detection-at-toll-booth)
    - [Part 3: Traffic Congestion Detection](#part-3-traffic-congestion-detection)
- [Alert Examples](#alert-examples)
    - [Accident Alert (Critical)](#accident-alert-critical)
    - [Violation Alert (Warning)](#violation-alert-warning)
    - [Congestion Alert (Advisory)](#congestion-alert-advisory)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Live Intelligence](\examples-and-tutorials\live-intelligence\index)

# Multi-Use Road Monitoring System

Copy page

Integrated road safety system detecting accidents, violations, and congestion in real-time

Copy page

Open In Colab

<!-- image -->

## [ The Story](#the-story)

Road accidents happen every single day - and many lives are lost not because of the severity of the crash itself, but because victims don't receive timely aid and medical attention. Often, there's no one around to report an incident, or bystanders take too long to respond - either from shock, panic, or the overwhelming nature of witnessing an accident. But in those critical moments, even a few seconds can make the difference between life and death. This is where AI can help. With VideoDB RTStream, we can deploy cameras at accident-prone locations and let AI constantly monitor live video streams. As soon as an accident occurs, AI will detect it and instantly send alerts to nearby emergency services or traffic authorities.

## [ What You'll Build](#what-you’ll-build)

In this guide, we'll build a comprehensive road monitoring system that addresses three critical traffic challenges:

- **Accident Detection** - Instant alerts for vehicle collisions
- **Violation Monitoring** - Real-time detection of traffic rule breaking
- **Congestion Detection** - Early warning for traffic jams

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

### [ Part 1: Accident Detection at Toll Plaza](#part-1-accident-detection-at-toll-plaza)

**Step 1: Connect to Toll Plaza Stream**

```
accident_stream = coll.connect_rtstream(
name = "Toll Plaza Accident Monitor" ,
url = "rtsp://samples.rts.videodb.io:8554/accident" ,
)
```

**Step 2: Index for Accident Detection**

```
accident_index = accident_stream.index_visuals(
batch_config = {
"type" : "time" ,
"value" : 10 ,
"frame_count" : 2 ,
},
prompt = """Monitor the toll plaza road carefully. Detect if a vehicle collides, crashes,
or a person falls. Describe the situation clearly if an accident occurs.""" ,
name = "Accident_Detection_Index" ,
)
```

**Step 3: Create Accident Event &amp; Alert**

```
accident_event_id = conn.create_event(
event_prompt = "Detect if an accident or vehicle collision takes place." ,
label = "road_accident" ,
)

webhook_url = "https://your-webhook-url.com"
accident_alert_id = accident_index.create_alert(accident_event_id, callback_url = webhook_url)
```

### [ Part 2: Traffic Violation Detection at Toll Booth](#part-2-traffic-violation-detection-at-toll-booth)

**Step 4: Create Violation Index on Same Stream** Create a separate index on the same stream with faster analysis:

```
violation_index = accident_stream.index_visuals(
batch_config = {
"type" : "time" ,
"value" : 3 ,
"frame_count" : 2 ,
},
prompt = """Monitor the toll plaza carefully. Detect if any vehicle breaks traffic rules -
for example, skipping the toll booth, crossing without stopping, driving in the
wrong lane, or ignoring the barrier. Describe such violations clearly.""" ,
name = "Toll_Violation_Index" ,
)
```

The faster batch config ( `value: 3` ) ensures violations aren't missed. **Step 5: Create Violation Event &amp; Alert**

```
violation_event_id = conn.create_event(
event_prompt = "Detect if a vehicle breaks traffic rules at the toll plaza." ,
label = "toll_rule_violation" ,
)

violation_alert_id = violation_index.create_alert(violation_event_id, callback_url = webhook_url)
```

### [ Part 3: Traffic Congestion Detection](#part-3-traffic-congestion-detection)

**Step 6: Connect to Highway Stream**

```
congestion_stream = coll.connect_rtstream(
name = "Highway Traffic Monitor" ,
url = "rtsp://3.6.198.206:8554/traffic" ,
)
```

**Step 7: Index for Congestion**

```
congestion_index = congestion_stream.index_visuals(
batch_config = {
"type" : "time" ,
"value" : 5 ,
"frame_count" : 3 ,
},
prompt = """Monitor the lanes of vehicles over several video frames. If the whole lane of
cars consistently moves very slowly or stops, classify the situation as 'traffic
congestion detected.' Otherwise, classify it as 'regular traffic flow'.""" ,
name = "Traffic_Congestion_Index" ,
)
```

**Step 8: Create Congestion Event &amp; Alert**

```
congestion_event_id = conn.create_event(
event_prompt = "Detect if traffic congestion or jam is forming." ,
label = "traffic_congestion" ,
)

congestion_alert_id = congestion_index.create_alert(congestion_event_id, callback_url = webhook_url)
```

## [ Alert Examples](#alert-examples)

### [ Accident Alert (Critical)](#accident-alert-critical)

```
{
"event_id" : "event-accident-001" ,
"label" : "road_accident" ,
"confidence" : 0.96 ,
"explanation" : "Vehicle collision detected at toll plaza. Two vehicles involved with visible impact." ,
"timestamp" : "2025-05-29T10:15:33.123456+00:00" ,
"start_time" : "2025-05-29T10:15:33.000000+05:30" ,
"end_time" : "2025-05-29T10:15:43.000000+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711a0-0fde-7911-b282-25bc0b4ecf65/1748485533000000-1748485543000000.m3u8"
}
```

### [ Violation Alert (Warning)](#violation-alert-warning)

```
{
"event_id" : "event-violation-001" ,
"label" : "toll_rule_violation" ,
"confidence" : 0.90 ,
"explanation" : "Vehicle crossing toll plaza without stopping, ignoring barrier." ,
"timestamp" : "2025-05-29T10:20:15.123456+00:00" ,
"start_time" : "2025-05-29T10:20:15.000000+05:30" ,
"end_time" : "2025-05-29T10:20:18.000000+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711a0-0fde-7911-b282-25bc0b4ecf65/1748485815000000-1748485818000000.m3u8"
}
```

### [ Congestion Alert (Advisory)](#congestion-alert-advisory)

```
{
"event_id" : "event-congestion-001" ,
"label" : "traffic_congestion" ,
"confidence" : 0.95 ,
"explanation" : "High vehicle density and slow movement observed across multiple lanes, indicating traffic congestion." ,
"timestamp" : "2025-05-29T13:41:20.123456+00:00" ,
"start_time" : "2025-05-29T13:41:08.000000+05:30" ,
"end_time" : "2025-05-29T13:41:13.000000+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711a0-0fde-7911-b282-25bc0b4ecf65/1748504468000000-1748504473000000.m3u8"
}
```

## [ The Result](#the-result)

With these systems in place, we built a smart AI-powered road monitoring system addressing two major challenges: **Accident Detection at toll plazas** - instantly spotting crashes and alerting emergency services without delay. **Traffic Congestion Detection on busy highways** - catching early signs of jams so authorities can act before things spiral. Together, these tools show how AI video monitoring can make roads safer, traffic smoother, and emergency responses faster - all in real time.

## Explore the Full Notebook

Open the complete implementation with multi-stream monitoring and advanced configuration.

## [ Related Tutorials](#related-tutorials)

## Traffic Violations Detection

Real-time detection of helmet violations, wrong-side driving, and red light violations

## Flash Flood Early Warning

Natural disaster monitoring with emergency alerts

[Flash Flood Early Warning System](\examples-and-tutorials\live-intelligence\flash-flood-detection) [Dashcam Monitoring of Traffic](\examples-and-tutorials\live-intelligence\roadcam-monitoring)

⌘ I