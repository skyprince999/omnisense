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

- [The Viral Inspiration](#the-viral-inspiration)
- [How It Works](#how-it-works)
- [The Setup](#the-setup)
    - [1. Connect Your Stream](#1-connect-your-stream)
    - [2. Create the Violation Detection Index](#2-create-the-violation-detection-index)
    - [3. Set Up Event &amp; Alert](#3-set-up-event-%26-alert)
- [What You Get](#what-you-get)
- [Automated Enforcement Pipeline: From Video to Inbox](#automated-enforcement-pipeline-from-video-to-inbox)
- [Email received via N8N Automation](#email-received-via-n8n-automation)
- [Try It Yourself](#try-it-yourself)
- [Related Tutorials](#related-tutorials)

[Live Intelligence](\examples-and-tutorials\live-intelligence\index)

# Traffic Violation Detection

Copy page

Detect and report real-time traffic rule violations

Copy page

Open In Colab

<!-- image -->

## [ The Viral Inspiration](#the-viral-inspiration)

You've seen the post. A guy got so fed up with daily traffic chaos that he automated his helmet camera to snap violations and send them straight to the traffic police - no manual intervention needed.

## View the inspiration

Check out the original post that sparked this idea

The internet loved it. And we thought - why not make this accessible to everyone? With **VideoDB RTStream** , you can do exactly this. Connect your dashcam or helmet cam, let AI monitor for violations, and auto-report them. Let's see how it works.

## [ How It Works](#how-it-works)

```
Helmet Cam / Dashcam
↓
🔗 RTSP Stream → VideoDB RTStream
↓
🤖 AI Scene Analysis (every 5 sec, 5 frames)
↓
🚨 Violation Detected? → Webhook Alert
↓
📧 n8n Workflow → Email to Traffic Police
```

Simple pipeline. Powerful impact.

## [ The Setup](#the-setup)

### [ 1. Connect Your Stream](#1-connect-your-stream)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()

rtsp_url = "rtsp://your-camera-stream-url"
roadcam_stream = coll.connect_rtstream(
name = "RoadCam Violation Stream" ,
url = rtsp_url,)
```

```
import { connect } from 'videodb' ;

const conn = await connect ();
const coll = await conn . getCollection ();

const rtspUrl = "rtsp://your-camera-stream-url" ;
const roadcamStream = await coll . connectRTStream (
rtspUrl ,
"RoadCam Violation Stream" );
```

### [ 2. Create the Violation Detection Index](#2-create-the-violation-detection-index)

This is where the magic happens. We tell the AI exactly what to look for:

Python

Node.js

```
from videodb import SceneExtractionType

violation_prompt = """
Focus on vehicles visible on the road and monitor them for the following traffic rule violations:

1. NO HELMET: Two-wheeler rider or pillion not wearing a helmet
2. MOBILE PHONE USE: Driver using mobile phone while operating the vehicle
3. WRONG SIDE DRIVING: Vehicle traveling against the designated traffic flow
4. RED LIGHT VIOLATION: Vehicle crossing when traffic signal is red
5. TRIPLE RIDING: More than two people on a single two-wheeler
6. NO SEATBELT: Driver or front passenger not wearing seatbelt

If you detect a violation, respond in this format:

Traffic Rule Violated
Vehicle: [vehicle type and color]
Plate Number: [license plate if visible, otherwise "Not Visible"]
Violation: [specific violation from the list]
Description: [brief description]

If NO violation is detected, respond ONLY with:
No Traffic Rule Violation Detected
"""

violation_scene_index = roadcam_stream.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = {
"time" : 5 ,
"frame_count" : 5 ,
},
prompt = violation_prompt,
name = "Traffic_Violation_Index" )
```

```
import { SceneExtractionType } from 'videodb' ;

const violationPrompt = `
Focus on vehicles visible on the road and monitor them for the following traffic rule violations:

1. NO HELMET: Two-wheeler rider or pillion not wearing a helmet
2. MOBILE PHONE USE: Driver using mobile phone while operating the vehicle
3. WRONG SIDE DRIVING: Vehicle traveling against the designated traffic flow
4. RED LIGHT VIOLATION: Vehicle crossing when traffic signal is red
5. TRIPLE RIDING: More than two people on a single two-wheeler
6. NO SEATBELT: Driver or front passenger not wearing seatbelt

If you detect a violation, respond in this format:

Traffic Rule Violated
Vehicle: [vehicle type and color]
Plate Number: [license plate if visible, otherwise "Not Visible"]
Violation: [specific violation from the list]
Description: [brief description]

If NO violation is detected, respond ONLY with:
No Traffic Rule Violation Detected
` ;

const violationSceneIndex = await roadcamStream . indexScenes ({
extractionType: SceneExtractionType . timeBased ,
extractionConfig: {
time: 5 ,
frameCount: 5 ,
},
prompt: violationPrompt ,
name: "Traffic_Violation_Index"
});
```

### [ 3. Set Up Event &amp; Alert](#3-set-up-event-&-alert)

Python

Node.js

```
# Create the violation event
violation_event_id = conn.create_event(
event_prompt = """
Detect when a traffic rule violation occurs, such as no helmet, mobile phone use, wrong side driving, red light violation, triple riding, or no seatbelt.
Your 'explanation' should not include any commentary, and should clearly mention the following things:
Traffic Rule Violated
Vehicle: [vehicle type and color, e.g., "Black motorcycle", "White sedan"]
Plate Number: [license plate number if visible, otherwise "Not Visible"]
Violation: [specific violation(s) from the list above]
Description: [brief description of what you observed]
""" ,
label = "traffic_violation" )

# Attach webhook alert
violation_alert_id = violation_scene_index.create_alert(
violation_event_id,
callback_url = "https://your-webhook-url.com" )
```

```
// Create the violation event
const violationEventId = await conn . createEvent (
`Detect when a traffic rule violation occurs, such as no helmet, mobile phone use, wrong side driving, red light violation, triple riding, or no seatbelt.
Your 'explanation' should not include any commentary, and should clearly mention the following things:
Traffic Rule Violated
Vehicle: [vehicle type and color, e.g., "Black motorcycle", "White sedan"]
Plate Number: [license plate number if visible, otherwise "Not Visible"]
Violation: [specific violation(s) from the list above]
Description: [brief description of what you observed]` ,
"traffic_violation" );

// Attach webhook alert
const violationAlertId = await violationSceneIndex . createAlert (
violationEventId ,
"https://your-webhook-url.com" );
```

## [ What You Get](#what-you-get)

When a violation is caught, your webhook receives:

```
{
"event_id" : "event-3fd4174feceb6162" ,
"label" : "traffic_violation" ,
"confidence" : 0.95 ,
"explanation" : """
Traffic Rule Violated: NO HELMET
Vehicle: Orange scooter
Plate Number: DL 3S CW 4952
Violation: NO HELMET
Description: The rider and the pillion rider on the orange scooter are not wearing helmets.
""" ,
"timestamp" : "2026-01-07T04:57:44.081850+00:00" ,
"start_time" : "2026-01-07T10:27:20.432151+05:30" ,
"end_time" : "2026-01-07T10:27:27.742309+05:30" ,
"stream_url" : "https://rt.stream.videodb.io/manifests/rts-019b929e-e004-72b0-94d6-b7582510934f/1767761840000000-1767761848000000.m3u8" ,
"player_url" : "https://console.videodb.io/player?url=https://rt.stream.videodb.io/manifests/rts-019b929e-e004-72b0-94d6-b7582510934f/1767761840000000-1767761848000000.m3u8"
}
```

The `stream_url` is a direct link to the violation clip - ready to attach to your report.

## [ Automated Enforcement Pipeline: From Video to Inbox](#automated-enforcement-pipeline-from-video-to-inbox)

This n8n workflow acts as the **Digital Dispatch Center** , transforming raw AI detections into professional traffic reports in real-time.

1. **Webhook Trigger** : Receives the raw event payload from the VideoDB Safety Agent immediately upon violation detection.
2. **AI Data Extraction** : A dedicated VideoDB node parses the unstructured explanation string into a structured JSON object containing the License Plate, Vehicle Description, and Violation Type.
3. **Report Formatting** : A code node generates a high-contrast, professional HTML email template that maps the AI observations to a formal report structure.
4. **Official Delivery** : The finalized report - complete with the dynamic subject line and a direct link to the video evidence - is dispatched instantly via the Gmail node to the Traffic Control Room.

N8N workflow automation showing the steps for traffic violation detection and email delivery

<!-- image -->

No more manual reporting. Just set it and forget it.

## [ Email received via N8N Automation](#email-received-via-n8n-automation)

Email received via N8N automation showing the professional report format

<!-- image -->

## [ Try It Yourself](#try-it-yourself)

## Open the Notebook

Run the complete implementation in Google Colab with step-by-step examples

n8n workflow JSON attached below, simply copy the code and paste in your N8N instance, and set up the credentials to get the automation running!

n8n Workflow JSON (Click to expand)

```
{
"nodes" : [
{
"parameters" : {
"path" : "traffic-violation-webhook" ,
"options" : {}
},
"type" : "n8n-nodes-base.webhook" ,
"typeVersion" : 2.1 ,
"position" : [ 0 , 80 ],
"id" : "34895f49-bcde-43cd-9112-60bbee8147a0" ,
"name" : "Webhook"
},
{
"parameters" : {
"operation" : "generateText" ,
"prompt" : "=You are a data extraction specialist. Your task is to parse a raw traffic violation string into a strict JSON format.|INPUT: \" {{ $json.explanation }} \" TASK:Extract the following fields. If a field is missing or unclear, use \" N/A \" as the value.1. vehicle_details2. license_plate: (The alpha-numeric plate number)3. violation_type: (The specific rule broken like no helmet, mobile phone use, wrong side driving, red light violation, triple riding, or no seatbelt)4. observation: (A short, clean summary of the evidence)STRICT RULES:- Output ONLY valid JSON.- No markdown formatting, no backticks, no preamble.- If the input is empty or invalid, return an object with all values set to \" Unknown \" .JSON STRUCTURE:{ \" vehicle_type \" : \"\" , \" license_plate \" : \"\" , \" violation_type \" : \"\" , \" observation \" : \"\" }" ,
"response_type" : "json"
},
"type" : "@videodb/n8n-nodes-videodb.videoDb" ,
"typeVersion" : 1 ,
"position" : [ 224 , 80 ],
"id" : "5a16a040-9ab9-4001-9281-8e6963cf5d6b" ,
"name" : "VideoDB"
},
{
"parameters" : {},
"type" : "n8n-nodes-base.wait" ,
"typeVersion" : 1.1 ,
"position" : [ 448 , 80 ],
"id" : "d04dff57-2b8b-4d5f-b96f-364349623c49" ,
"name" : "Wait"
},
{
"parameters" : {
"url" : "={{ $('VideoDB').item.json.data.output_url }}" ,
"authentication" : "predefinedCredentialType" ,
"nodeCredentialType" : "videoDBApi" ,
"options" : {}
},
"type" : "n8n-nodes-base.httpRequest" ,
"typeVersion" : 4.3 ,
"position" : [ 672 , 0 ],
"id" : "0048b380-50ac-4da0-a949-35d7ae0f3fe3" ,
"name" : "HTTP Request"
},
{
"parameters" : {
"conditions" : {
"options" : {
"caseSensitive" : true ,
"leftValue" : "" ,
"typeValidation" : "loose" ,
"version" : 2
},
"conditions" : [
{
"id" : "0ab68efa-a4ba-4235-b3e8-6c3967880aef" ,
"leftValue" : "={{ $json.status }}" ,
"rightValue" : "complete" ,
"operator" : {
"type" : "string" ,
"operation" : "equals"
}
}
],
"combinator" : "and"
},
"looseTypeValidation" : true ,
"options" : {}
},
"type" : "n8n-nodes-base.if" ,
"typeVersion" : 2.2 ,
"position" : [ 896 , 80 ],
"id" : "74645a4a-4ab0-4efe-84e9-052457fb2cb2" ,
"name" : "If"
},
{
"parameters" : {
"sendTo" : "={{ $json.to }}" ,
"subject" : "={{ $json.subject }}" ,
"message" : "={{ $json.html }}" ,
"options" : {}
},
"type" : "n8n-nodes-base.gmail" ,
"typeVersion" : 2.1 ,
"position" : [ 1344 , 80 ],
"id" : "17d26012-f389-40e9-be75-dcce6640d0dc" ,
"name" : "Send a message"
},
{
"parameters" : {
"jsCode": "const webhookData = $('Webhook').first().json;\nconst llmResult = $input.first().json.response.data.output;\n\nconst eventDate = new Date(webhookData.start_time).toLocaleString('en-IN', {\n  timeZone: 'Asia/Kolkata',\n  dateStyle: 'long',\n  timeStyle: 'medium'\n});\n\nconst htmlBody = `<div style=\"max-width:500px;margin:20px auto;border:2px solid #000;font-family:Arial,sans-serif;color:#000;padding:0;\"><div style=\"padding:20px;border-bottom:2px solid #000;text-align:center;\"><h2 style=\"margin:0;text-transform:uppercase;\">Traffic Violation Alert</h2><p style=\"margin:5px 0 0 0;font-size:14px;\">Automated Detection Report</p></div><div style=\"padding:20px;\"><table style=\"width:100%;border-collapse:collapse;color:#000;\"><tr><td style=\"padding:10px 0;border-bottom:1px solid #eee;\"><strong>Detected Violation</strong></td><td style=\"padding:10px 0;border-bottom:1px solid #eee;text-align:right;\">${llmResult.violation_type}</td></tr><tr><td style=\"padding:10px 0;border-bottom:1px solid #eee;\"><strong>Vehicle Description</strong></td><td style=\"padding:10px 0;border-bottom:1px solid #eee;text-align:right;\">${llmResult.vehicle_type}</td></tr><tr><td style=\"padding:10px 0;border-bottom:1px solid #eee;\"><strong>License Plate</strong></td><td style=\"padding:10px 0;border-bottom:1px solid #eee;text-align:right;\"><code style=\"font-size:16px;font-weight:bold;\">${llmResult.license_plate}</code></td></tr><tr><td style=\"padding:10px 0;border-bottom:1px solid #eee;\"><strong>Incident Time</strong></td><td style=\"padding:8px 0;border-bottom:1px solid #eee;text-align:right;\">${eventDate}</td></tr></table><div style=\"margin-top:20px;padding:15px;border:1px solid #000;background-color:#fcfcfc;\"><p style=\"margin:0;font-size:14px;\"><strong>AI Observation:</strong> ${llmResult.observation}</p></div><div style=\"margin-top:30px;text-align:center;\"><a href=\"${webhookData.player_url}\" style=\"display:inline-block;padding:12px 30px;border:2px solid #000;color:#000;text-decoration:none;font-weight:bold;text-transform:uppercase;font-size:14px;\">Click to View Evidence Clip</a></div></div></div>`;\n\nreturn {\n  to: \"control.room@dtp.nic.in\",\n  subject: `Violation Alert: ${llmResult.violation_type} [${llmResult.license_plate}]`,\n  html: htmlBody\n};"
},
"type" : "n8n-nodes-base.code" ,
"typeVersion" : 2 ,
"position" : [ 1120 , 80 ],
"id" : "342feeb0-a5b6-4e20-a4eb-e4e962539439" ,
"name" : "Format Report"
}
],
"connections" : {
"Webhook" : {
"main" : [[{ "node" : "VideoDB" , "type" : "main" , "index" : 0 }]]
},
"VideoDB" : {
"main" : [[{ "node" : "Wait" , "type" : "main" , "index" : 0 }]]
},
"Wait" : {
"main" : [[{ "node" : "HTTP Request" , "type" : "main" , "index" : 0 }]]
},
"HTTP Request" : {
"main" : [[{ "node" : "If" , "type" : "main" , "index" : 0 }]]
},
"If" : {
"main" : [
[{ "node" : "Format Report" , "type" : "main" , "index" : 0 }],
[{ "node" : "Wait" , "type" : "main" , "index" : 0 }]
]
},
"Format Report" : {
"main" : [[{ "node" : "Send a message" , "type" : "main" , "index" : 0 }]]
}
}
}
```

**Small cameras. Smart AI. Big change. Built with** [**VideoDB**](https://videodb.io/)

## [ Related Tutorials](#related-tutorials)

## Road Monitoring System

Multi-use road monitoring for accidents and congestion

## Automated Traffic Violation Detection

Dashcam-based violation detection and enforcement

[Dashcam Monitoring of Traffic](\examples-and-tutorials\live-intelligence\roadcam-monitoring) [Live Cricket Highlight Detection](\examples-and-tutorials\live-intelligence\cricket-match-monitoring)

⌘ I