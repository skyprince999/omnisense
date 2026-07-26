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
    - [API Keys](#api-keys)
- [Implementation](#implementation)
    - [Step 1: Connect to VideoDB](#step-1-connect-to-videodb)
    - [Step 2: Upload Video](#step-2-upload-video)
    - [Step 3: Analyze Visuals](#step-3-analyze-visuals)
    - [Step 4: Generate Script](#step-4-generate-script)
    - [Step 5: Generate Voiceover Audio](#step-5-generate-voiceover-audio)
    - [Step 6: Compose the Video](#step-6-compose-the-video)
    - [Step 7: Review and Share](#step-7-review-and-share)
- [Conclusion](#conclusion)
- [Related Tutorials](#related-tutorials)

[Content Factory](\examples-and-tutorials\content-factory\index)

# AI Voiceovers

Copy page

Add professional narration to silent footage

Copy page

**Case: Automatically Creating Voiceover for Silent Footage of the Underwater World**

Open In Colab

<!-- image -->

## [ Overview](#overview)

Voiceovers are the secret sauce that turns silent footage into captivating stories. They add depth, emotion, and excitement, elevating the viewing experience. Traditionally, this workflow required stitching together multiple tools: one for script writing (LLM), one for voice generation (TTS), and another for video editing. **VideoDB** simplifies this by bringing everything under one roof. In this tutorial, we will:

1. **Upload** a silent video.
2. **Analyze** the video to understand its visual content.
3. **Generate** a narration script using VideoDB's text generation.
4. **Generate** a professional AI voiceover using VideoDB's voice generation.
5. **Merge** them instantly into a final video.

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

### [ API Keys](#api-keys)

You only need your VideoDB API Key. Get your API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) . Free for first 50 uploads, no credit card required.

## [ Implementation](#implementation)

### [ Step 1: Connect to VideoDB](#step-1-connect-to-videodb)

Connect to VideoDB using your API key to establish a session.

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

### [ Step 2: Upload Video](#step-2-upload-video)

We'll upload the silent underwater footage directly from YouTube.

Python

Node.js

```
# Upload a video by URL
video = coll.upload( url = 'https://youtu.be/RcRjY5kzia8' )
```

```
// Upload a video by URL
const video = await coll . uploadURL ({ url: 'https://youtu.be/RcRjY5kzia8' });
```

### [ Step 3: Analyze Visuals](#step-3-analyze-visuals)

We need to know what is happening in the video to write a script for it. We'll use `index_scenes()` to analyze the visual content.

Python

Node.js

```
video_scenes_id = video.index_scenes()
```

```
const videoScenesId = await video . indexScenes ();
```

Let's view the description of first scene from the video

Python

Node.js

```
video_scenes = video.get_scene_index(video_scenes_id)

import json
print (json.dumps(video_scenes[ 0 ], indent = 2 ))
```

```
const videoScenes = await video . getSceneIndex ( videoScenesId );

console . log ( JSON . stringify ( videoScenes [ 0 ], null , 2 ));
```

**Output:**

```
{
"description" : "The scene immerses the viewer in a vibrant, fluid expanse dominated by myriad blue and aqua forms. These countless, somewhat irregular shapes are densely packed, giving the impression of an immense, teeming mass in constant, gentle motion. Each form possesses a darker core that gradually lightens towards its edges, creating a translucent, almost glowing effect, as if illuminated from within. The varying shades, ranging from deep sapphire to brilliant turquoise, blend and shift across the frame, conjuring the image of a vast underwater environment. It evokes a colossal school of luminous marine creatures, perhaps fish or jellyfish, drifting together in a mesmerizing, organic dance, filling the visual field with their shimmering presence and dynamic, watery energy." ,
"end" : 15.033 ,
"metadata" : {},
"scene_metadata" : {},
"start" : 0.0
}
```

### [ Step 4: Generate Script](#step-4-generate-script)

Now, we use VideoDB's `generate_text` method to write a voiceover script based on the scene descriptions we just retrieved.

Python

Node.js

```
# Construct a prompt with the scene context
scene_context = " \n " .join([ f "- { scene[ 'description' ] } " for scene in video_scenes])

prompt = f """
Here is a visual description of a video about the underwater world:
{ scene_context }

Based on this, write a short, engaging voiceover script in the style of a nature documentary narrator (like David Attenborough).
Keep it synced to the flow of the visuals described.
Return ONLY the raw text of the narration, no stage directions or titles.
"""

# Generate the script using VideoDB
script_response = coll.generate_text(
prompt = prompt,
model_name = "pro" )

script_text = script_response[ "output" ]

print ( "--- Generated Script ---" )
print (script_text)
```

```
// Construct a prompt with the scene context
const sceneContext = videoScenes . map ( scene => `- ${ scene . description } ` ). join ( ' \n ' );

const prompt = `
Here is a visual description of a video about the underwater world:
${ sceneContext }

Based on this, write a short, engaging voiceover script in the style of a nature documentary narrator (like David Attenborough).
Keep it synced to the flow of the visuals described.
Return ONLY the raw text of the narration, no stage directions or titles.
` ;

// Generate the script using VideoDB
const scriptResponse = await coll . generateText (
prompt ,
"pro"
);

const scriptText = scriptResponse . output ;

console . log ( "--- Generated Script ---" );
console . log ( scriptText );
```

### [ Step 5: Generate Voiceover Audio](#step-5-generate-voiceover-audio)

We can now turn that text into speech using `generate_voice` . This returns an Audio object directly, so we don't need to save or upload files manually.

Python

Node.js

```
# Generate speech directly as a VideoDB Audio Asset
audio = coll.generate_voice(
text = script_text,
voice_name = "Default" )

print ( f "Generated Audio Asset ID: { audio.id } " )
```

```
// Generate speech directly as a VideoDB Audio Asset
const audio = await coll . generateVoice (
scriptText ,
"Default"
);

console . log ( `Generated Audio Asset ID: ${ audio . id } ` );
```

### [ Step 6: Compose the Video](#step-6-compose-the-video)

We have the video and the generated voiceover. Now we merge them using the Timeline Editor.

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip, VideoAsset, AudioAsset

# Create a timeline
timeline = Timeline(conn)

# 1. Create a Video Track
video_track = Track()
video_asset = VideoAsset( id = video.id)
# Add the video clip
video_clip = Clip( asset = video_asset, duration = float (video.length))
video_track.add_clip( 0 , video_clip)

# 2. Create an Audio Track for the voiceover
audio_track = Track()
# Use the audio object we generated in Step 5
audio_asset = AudioAsset( id = audio.id)
audio_clip = Clip( asset = audio_asset, duration = float (audio.length))
audio_track.add_clip( 0 , audio_clip)

# Add tracks to timeline
timeline.add_track(video_track)
timeline.add_track(audio_track)
```

```
import { EditorTimeline , Track , Clip , EditorVideoAsset , EditorAudioAsset } from 'videodb' ;

// Create a timeline
const timeline = new EditorTimeline ( conn );

// 1. Create a Video Track
const videoTrack = new Track ();
const videoAsset = new EditorVideoAsset ({ id: video . id });
// Add the video clip
const videoClip = new Clip ({ asset: videoAsset , duration: parseFloat ( video . length ) });
videoTrack . addClip ( 0 , videoClip );

// 2. Create an Audio Track for the voiceover
const audioTrack = new Track ();
// Use the audio object we generated in Step 5
const audioAsset = new EditorAudioAsset ({ id: audio . id });
const audioClip = new Clip ({ asset: audioAsset , duration: parseFloat ( audio . length ) });
audioTrack . addClip ( 0 , audioClip );

// Add tracks to timeline
timeline . addTrack ( videoTrack );
timeline . addTrack ( audioTrack );
```

### [ Step 7: Review and Share](#step-7-review-and-share)

Generate the final stream URL and watch your AI-narrated video!

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

## [ Conclusion](#conclusion)

Congratulations! You have successfully automated the process of creating custom and personalized voiceovers based on a simple prompt and raw video footage using VideoDB. By leveraging advanced AI technologies, you can enhance the storytelling and immersive experience of your video content. Experiment with different prompts and scene analysis techniques to further improve the quality and accuracy of the voiceovers. Enjoy creating captivating narratives with AI-powered voiceovers using VideoDB!

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## Video Dubbing

Dub videos into multiple languages with AI voice synthesis

## Faceless Video Creator

Build complete faceless videos with AI scripts, voiceovers, and multi-layer composition

[Video Dubbing](\examples-and-tutorials\content-factory\dubbing) [Trailer Narration](\examples-and-tutorials\content-factory\trailer-narration)

⌘ I