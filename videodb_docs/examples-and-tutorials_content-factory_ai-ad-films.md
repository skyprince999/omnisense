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
- [Setup](#setup)
    - [Installing VideoDB](#installing-videodb)
    - [API Key](#api-key)
- [Implementation](#implementation)
    - [Step 1: Connect to VideoDB](#step-1-connect-to-videodb)
    - [Step 2: Upload Product Footage](#step-2-upload-product-footage)
    - [Step 3: Analyze Visuals](#step-3-analyze-visuals)
    - [Step 4: Generate Ad Script](#step-4-generate-ad-script)
    - [Step 5: Generate Voiceover](#step-5-generate-voiceover)
    - [Step 6: Compose the Advertisement](#step-6-compose-the-advertisement)
    - [Step 7: Review and Share](#step-7-review-and-share)
    - [Conclusion](#conclusion)
- [Related Tutorials](#related-tutorials)

[Content Factory](\examples-and-tutorials\content-factory\index)

# AI-Generated Ads

Copy page

Generate professional product advertisements from raw footage

Copy page

**Automatically Creating a professional quality advertisement from product videography B-Roll**

Open In Colab

<!-- image -->

## [ Overview](#overview)

Creating professional product advertisements typically requires a team: copywriters for the script, voice actors for the narration, and editors to stitch it all together. **VideoDB** streamlines this into a single, automated workflow. In this tutorial, we will:

1. **Upload** raw product footage (a jewelry shoot).
2. **Analyze** the visual content automatically.
3. **Generate** a professional ad script based on the visuals.
4. **Synthesize** a high-quality voiceover.
5. **Publish** the final commercial.

## [ Setup](#setup)

### [ Installing VideoDB](#installing-videodb)

Python

Node.js

```
! pip install videodb
```

```
npm install videodb
```

### [ API Key](#api-key)

You only need your VideoDB API Key. Get your API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) . Free for first 50 uploads, no credit card required.

## [ Implementation](#implementation)

### [ Step 1: Connect to VideoDB](#step-1-connect-to-videodb)

Establish a connection to your VideoDB project.

Python

Node.js

```
import videodb

# Set your API key
api_key = "your_api_key"

# Connect to VideoDB
conn = videodb.connect( api_key = api_key)
coll = conn.get_collection()
```

```
import { connect } from 'videodb' ;

// Connect to VideoDB
const conn = await connect ({ apiKey: process . env . VIDEO_DB_API_KEY });
const coll = await conn . getCollection ();
```

### [ Step 2: Upload Product Footage](#step-2-upload-product-footage)

We'll upload a raw video clip of a jewelry product shoot from YouTube.

Python

Node.js

```
# Upload a video by URL
video = coll.upload( url = 'https://www.youtube.com/watch?v=2DcAMbmmYNM' )
```

```
// Upload a video by URL
const video = await coll . uploadURL ({ url: 'https://www.youtube.com/watch?v=2DcAMbmmYNM' });
```

### [ Step 3: Analyze Visuals](#step-3-analyze-visuals)

To write a relevant script, we first need to understand what's in the video. We'll use `index_scenes()` to extract detailed descriptions of the visual content.

Python

Node.js

```
scene_id = video.index_scenes()
```

```
const sceneId = await video . indexScenes ();
```

Let's view the description of first scene from the video

Python

Node.js

```
import json
scenes = video.get_scene_index(scene_id)

print (json.dumps(scenes[ 0 ], indent = 2 ))
```

```
const scenes = await video . getSceneIndex ( sceneId );

console . log ( JSON . stringify ( scenes [ 0 ], null , 2 ));
```

**Output:**

```
{
"description" : "The entire series of images presents a uniform and absolute darkness, an unbroken expanse of pure black. There are no discernible shapes, colors, or details to be found, suggesting a complete absence of light or any visual information whatsoever across the whole sequence." ,
"end" : 1.401 ,
"metadata" : {},
"scene_metadata" : {},
"start" : 0.0
}
```

### [ Step 4: Generate Ad Script](#step-4-generate-ad-script)

Now we use VideoDB's text generation to write the commercial. We feed the visual descriptions into the prompt to ensure the script perfectly matches the mood of the footage.

Python

Node.js

```
# Construct a prompt with the scene context
scene_context = " \n " .join([ f "- { scene[ 'description' ] } " for scene in scenes])

prompt = f """
Here is a visual description of a jewelry product video:
{ scene_context }

Write a short, elegant, and luxurious voiceover script for this video advertisement.
- Tone: Sophisticated, calming, premium.
- Length: Short (approx 20 seconds of speech).
- Content: Focus on beauty, craftsmanship, and elegance.
- Format: Return ONLY the raw narration text.
"""

# Generate script
text_response = coll.generate_text(
prompt = prompt,
model_name = "pro" )

ad_script = text_response[ "output" ]

print ( "--- Generated Ad Script ---" )
print (ad_script)
```

```
// Construct a prompt with the scene context
const sceneContext = scenes . map ( scene => `- ${ scene . description } ` ). join ( ' \n ' );

const prompt = `
Here is a visual description of a jewelry product video:
${ sceneContext }

Write a short, elegant, and luxurious voiceover script for this video advertisement.
- Tone: Sophisticated, calming, premium.
- Length: Short (approx 20 seconds of speech).
- Content: Focus on beauty, craftsmanship, and elegance.
- Format: Return ONLY the raw narration text.
` ;

// Generate script
const textResponse = await coll . generateText ({
prompt: prompt ,
modelName: "pro"
});

const adScript = textResponse . output ;

console . log ( "--- Generated Ad Script ---" );
console . log ( adScript );
```

### [ Step 5: Generate Voiceover](#step-5-generate-voiceover)

We'll turn the script into audio.

Python

Node.js

```
# Generate speech directly as a VideoDB Audio Asset
audio = coll.generate_voice(
text = ad_script,
voice_name = "Default" )
```

```
// Generate speech directly as a VideoDB Audio Asset
const audio = await coll . generateVoice ( adScript , "Default" );
```

### [ Step 6: Compose the Advertisement](#step-6-compose-the-advertisement)

We'll overlay the generated voiceover onto the original video using the Timeline editor.

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip, VideoAsset, AudioAsset

# Create a timeline
timeline = Timeline(conn)

# 1. Video Track (Background)
video_track = Track()
video_asset = VideoAsset( id = video.id)
video_clip = Clip( asset = video_asset, duration = float (video.length))
video_track.add_clip( 0 , video_clip)
timeline.add_track(video_track)

# 2. Audio Track (Voiceover Overlay)
audio_track = Track()
audio_asset = AudioAsset( id = audio.id)
audio_clip = Clip( asset = audio_asset, duration = float (audio.length))
audio_track.add_clip( 0 , audio_clip)
timeline.add_track(audio_track)
```

```
import { EditorTimeline , Track , Clip , VideoAsset , AudioAsset } from 'videodb' ;

// Create a timeline
const timeline = new EditorTimeline ( conn );

// 1. Video Track (Background)
const videoTrack = new Track ();
const videoAsset = new VideoAsset ({ id: video . id });
const videoClip = new Clip ({ asset: videoAsset , duration: parseFloat ( video . length ) });
videoTrack . addClip ( 0 , videoClip );
timeline . addTrack ( videoTrack );

// 2. Audio Track (Voiceover Overlay)
const audioTrack = new Track ();
const audioAsset = new AudioAsset ({ id: audio . id });
const audioClip = new Clip ({ asset: audioAsset , duration: parseFloat ( audio . length ) });
audioTrack . addClip ( 0 , audioClip );
timeline . addTrack ( audioTrack );
```

### [ Step 7: Review and Share](#step-7-review-and-share)

Generate the stream URL to watch your AI-created commercial.

Python

Node.js

```
from videodb import play_stream

stream_url = timeline.generate_stream()
play_stream(stream_url)
```

```
const streamUrl = await timeline . generateStream ();
console . log ( streamUrl );
```

**Output:**

### [ Conclusion](#conclusion)

You have successfully automated the production of a product advertisement. By replacing multiple external tools with VideoDB's unified SDK, you can now build scalable video generation engines that turn raw footage into polished content automatically.

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## Faceless Video Creator

Generate complete videos from scripts without camera

## AI Voiceovers

Add professional narration to silent footage

[Faceless Video Creator](\examples-and-tutorials\content-factory\faceless-video-creator) [TikTok Style Lyric Video Creator](\examples-and-tutorials\content-factory\tiktok-lyric-video)

⌘ I