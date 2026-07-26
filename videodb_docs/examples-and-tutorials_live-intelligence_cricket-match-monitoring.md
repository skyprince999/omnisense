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
    - [Step 1: Connect to the Cricket Stream](#step-1-connect-to-the-cricket-stream)
    - [Step 2: Index Scenes with Cricket Analysis](#step-2-index-scenes-with-cricket-analysis)
    - [Step 3: Define Four Highlight Events](#step-3-define-four-highlight-events)
    - [Step 4: Attach Alerts for Each Highlight](#step-4-attach-alerts-for-each-highlight)
- [What You Receive](#what-you-receive)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Live Intelligence](\examples-and-tutorials\live-intelligence\index)

# Live Cricket Highlight Detection

Copy page

AI-powered real-time detection of cricket highlights - sixes, fours, wickets, and catches

Copy page

Open In Colab

<!-- image -->

## [ The Story](#the-story)

Tonight is the ICC World Cup finals between India and Pakistan. Millions are watching the match live, and the competition to post match highlights - sixes, wickets, and spectacular catches - on social media is fiercer than ever. In the usual workflow, someone watches the match, waits for a moment to happen, then clips the video manually and uploads it online - often several minutes too late. But we have a smarter way. What if AI could monitor the match for you, detect key moments in real-time, and instantly send alerts when something exciting happens - giving you a headstart on posting highlights while everyone else scrambles?

## [ What You'll Build](#what-you’ll-build)

With VideoDB RTStream, you can build a system that:

- Monitors live cricket feeds continuously
- Detects key moments: sixes, fours, catches, and wickets
- Sends real-time alerts when highlights happen
- Provides instant video clips for social media sharing

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

### [ Step 1: Connect to the Cricket Stream](#step-1-connect-to-the-cricket-stream)

```
rtsp_url = "rtsp://samples.rts.videodb.io:8554/cricket"
cricket_stream = coll.connect_rtstream(
name = "Cricket Match Stream" ,
url = rtsp_url,
)
```

### [ Step 2: Index Scenes with Cricket Analysis](#step-2-index-scenes-with-cricket-analysis)

Create a scene index that analyzes the cricket match continuously. The batch config is tuned to capture the fast-paced nature of cricket - analyzing every 7 seconds with 7 frames for detailed action detection.

```
cricket_scene_index = cricket_stream.index_visuals(
batch_config = {
"type" : "time" ,
"value" : 7 ,
"frame_count" : 7 ,
},
prompt = """Identify and mention when a batsman hits a SIX (ball flying over the boundary rope),
a FOUR (ball crosses boundary rope after bouncing), a CATCH OUT (fielder catches
the ball mid-air before it touches ground) or a WICKET (when the wicket stumps
are put down by the ball).""" ,
name = "Cricket_Highlights_Index" ,
)
```

The higher `frame_count: 7` captures the rapid action of cricket, ensuring key moments aren't missed.

### [ Step 3: Define Four Highlight Events](#step-3-define-four-highlight-events)

Create events for each type of highlight that matches your indexing prompt:

```
# Six Hit
six_event_id = conn.create_event(
event_prompt = "Detect when a batsman hits a SIX - ball flying over the boundary rope." ,
label = "six_hit" ,
)

# Four Hit
four_event_id = conn.create_event(
event_prompt = "Detect when a batsman hits a FOUR - ball crosses boundary rope after bouncing." ,
label = "four_hit" ,
)

# Catch Out
catch_event_id = conn.create_event(
event_prompt = "Detect when a fielder takes a CATCH OUT - catching the ball mid-air." ,
label = "catch_out" ,
)

# Wicket
wicket_event_id = conn.create_event(
event_prompt = "Detect when a WICKET occurs - wicket stumps are put down." ,
label = "wicket" ,
)
```

### [ Step 4: Attach Alerts for Each Highlight](#step-4-attach-alerts-for-each-highlight)

Create alerts for all four events on the same webhook:

```
webhook_url = "https://your-webhook-url.com"

# Attach alerts for each event type
six_alert_id = cricket_scene_index.create_alert(six_event_id, callback_url = webhook_url)
four_alert_id = cricket_scene_index.create_alert(four_event_id, callback_url = webhook_url)
catch_alert_id = cricket_scene_index.create_alert(catch_event_id, callback_url = webhook_url)
wicket_alert_id = cricket_scene_index.create_alert(wicket_event_id, callback_url = webhook_url)
```

All alerts go to the same webhook, with the `label` field indicating which highlight was detected.

## [ What You Receive](#what-you-receive)

When a highlight is detected, your webhook receives an alert with the exact moment and video clip:

```
{
"event_id" : "event-3bfdd25d9239861b" ,
"label" : "four_hit" ,
"confidence" : 0.95 ,
"explanation" : "The ball is crossing the boundary after bouncing, indicating a FOUR has been scored." ,
"timestamp" : "2025-05-29T00:11:09.256447+00:00" ,
"start_time" : "2025-05-29T05:40:32.544547+05:30" ,
"end_time" : "2025-05-29T05:40:39.730362+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019711db-1086-7750-ba79-8f47a4fed603/1748477432000000-1748477440000000.m3u8"
}
```

## [ The Result](#the-result)

With this setup in place, broadcasters and content creators no longer have to wait, clip, and scramble. They can stay ahead of the crowd, instantly catching and sharing match-defining moments as they happen - turning every six, four, wicket, and catch into social media gold within seconds.

## Explore the Full Notebook

Open the complete implementation with additional features and helper functions for match analysis.

## [ Related Tutorials](#related-tutorials)

## Multi-Camera Basketball Analytics

Real-time sports analysis across multiple synchronized camera angles

## Multi-Camera Public Surveillance

Enterprise-scale multi-camera monitoring and event detection

[Traffic Violation Detection](\examples-and-tutorials\live-intelligence\traffic-violations) [Multi-Camera Basketball Analytics](\examples-and-tutorials\live-intelligence\multicam-basketball-analysis)

⌘ I