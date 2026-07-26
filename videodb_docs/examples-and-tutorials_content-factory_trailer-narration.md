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

- [Introduction](#introduction)
- [Setup](#setup)
    - [Installing VideoDB](#installing-videodb)
    - [API Keys](#api-keys)
- [Step 1: Connect to VideoDB](#step-1-connect-to-videodb)
- [Step 2: Upload the Trailer](#step-2-upload-the-trailer)
- [Step 3: Analyze Scenes](#step-3-analyze-scenes)
- [Step 4: Generate Narration Script](#step-4-generate-narration-script)
- [Step 5: Generate Voiceover Audio](#step-5-generate-voiceover-audio)
- [Step 6: Edit the Timeline](#step-6-edit-the-timeline)
- [Step 7: Review and Share](#step-7-review-and-share)
- [Bonus - Add Movie Poster](#bonus-add-movie-poster)
- [Conclusion](#conclusion)
- [Related Tutorials](#related-tutorials)

[Content Factory](\examples-and-tutorials\content-factory\index)

# Trailer Narration

Copy page

Create dramatic trailers with automated narration

Copy page

Open In Colab

<!-- image -->

## [ Introduction](#introduction)

Narration is the heartbeat of trailers, injecting excitement and intrigue into every frame. With **VideoDB** , adding narration becomes a seamless, creative process. In this tutorial, we will:

1. **Analyze** a movie trailer to understand its scenes.
2. **Generate** a dramatic script using VideoDB's text generation.
3. **Synthesize** a deep, trailer-style voiceover using VideoDB's voice generation.
4. **Edit** the narration into specific time slots to match the video's pacing.
5. **Overlay** a movie poster at the end.

All using a single SDK. Here's an example of weaving a thrilling storyline from a reel of unrelated, but valuable cinematic shots:

## [ Setup](#setup)

### [ Installing VideoDB](#installing-videodb)

```
!pip install videodb
```

### [ API Keys](#api-keys)

You only need your VideoDB API Key. Get your API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) . Free for first 50 uploads, no credit card required.

## [ Step 1: Connect to VideoDB](#step-1-connect-to-videodb)

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

## [ Step 2: Upload the Trailer](#step-2-upload-the-trailer)

We'll upload a sample movie trailer (Chase) to VideoDB. This creates the base video asset we will edit.

Python

Node.js

```
video = coll.upload( url = 'https://www.youtube.com/watch?v=WQmGwmc-XUY' )
```

```
const video = await coll . uploadURL ({ url: 'https://www.youtube.com/watch?v=WQmGwmc-XUY' });
```

## [ Step 3: Analyze Scenes](#step-3-analyze-scenes)

We need to understand the visual pacing of the trailer to write a good script. `index_scenes()` will generate descriptions and timestamps for every shot.

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
"description" : "The scene is engulfed in a vast, tumultuous blaze, with vibrant yellow and fiery orange flames swirling and dancing across the entire frame. The intense heat radiating from the inferno creates a mesmerizing, dynamic spectacle, casting a reddish-brown glow that fills the atmosphere. Darker, smoky elements are intermittently visible through the brilliant light, suggesting objects being consumed within the heart of this powerful, destructive force. The fire is alive, constantly shifting and reaching, conveying both destructive power and captivating motion." ,
"end" : 1.043 ,
"metadata" : {},
"scene_metadata" : {},
"start" : 0.0
}
```

## [ Step 4: Generate Narration Script](#step-4-generate-narration-script)

We'll use VideoDB's `generate_text` to write a dramatic script. We feed the scene descriptions into the prompt to ensure the narration matches the visual action.

Python

Node.js

```
# Construct prompt with scene context
scene_context = " \n " .join([ f "- { scene[ 'description' ] } " for scene in video_scenes])

prompt = f """
Craft a dynamic, dramatic narration script for a movie trailer based on these visual descriptions:
{ scene_context }

Requirements:
- Style: Intense, gritty, like a blockbuster action movie trailer.
- Output: Only provide the script for direct voice generation, no stage directions or narration.
"""

script_response = coll.generate_text(
prompt = prompt,
model_name = "pro" )

script_text = script_response[ "output" ]

print ( "--- Generated Script ---" )
print (script_text)
```

```
// Construct prompt with scene context
const sceneContext = videoScenes . map ( scene => `- ${ scene . description } ` ). join ( ' \n ' );

const prompt = `
Craft a dynamic, dramatic narration script for a movie trailer based on these visual descriptions:
${ sceneContext }

Requirements:
- Style: Intense, gritty, like a blockbuster action movie trailer.
- Output: Only provide the script for direct voice generation, no stage directions or narration.
` ;

const scriptResponse = await coll . generateText (
prompt ,
"pro"
);

const scriptText = scriptResponse . output ;

console . log ( "--- Generated Script ---" );
console . log ( scriptText );
```

You can refine the narration script prompt to ensure synchronization with timestamps in the scene index, optimizing the storytelling experience.

## [ Step 5: Generate Voiceover Audio](#step-5-generate-voiceover-audio)

Now we synthesize the audio.

Python

Node.js

```
# Generate speech directly as an Audio Asset
audio = coll.generate_voice(
text = script_text,
voice_name = "Brian" )

print ( f "Generated Audio ID: { audio.id } " )
```

```
// Generate speech directly as an Audio Asset
const audio = await coll . generateVoice (
scriptText ,
"Brian"
);

console . log ( `Generated Audio ID: ${ audio . id } ` );
```

## [ Step 6: Edit the Timeline](#step-6-edit-the-timeline)

Now we combine the video and audio.

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip, VideoAsset, AudioAsset

timeline = Timeline(conn)

# --- 1. Main Video Track ---
main_track = Track()
video_asset = VideoAsset( id = video.id, volume = 0.5 )
video_clip = Clip( asset = video_asset, duration = float (video.length))
main_track.add_clip( 0 , video_clip)
timeline.add_track(main_track)

# --- 2. Narration Track---
audio_track = Track()
audio_asset1 = AudioAsset( id = audio.id, start = 0 , volume = 2.0 )
audio_clip1 = Clip( asset = audio_asset1, duration = float (audio.length))
audio_track.add_clip( 4 , audio_clip1)

timeline.add_track(audio_track)
```

```
import { EditorTimeline , Track , Clip , EditorVideoAsset , EditorAudioAsset } from 'videodb' ;

const timeline = new EditorTimeline ( conn );

// --- 1. Main Video Track ---
const mainTrack = new Track ();
const videoAsset = new EditorVideoAsset ({ id: video . id , volume: 0.5 });
const videoClip = new Clip ({ asset: videoAsset , duration: parseFloat ( video . length ) });
mainTrack . addClip ( 0 , videoClip );
timeline . addTrack ( mainTrack );

// --- 2. Narration Track ---
const audioTrack = new Track ();
const audioAsset1 = new EditorAudioAsset ({ id: audio . id , start: 0 , volume: 2.0 });
const audioClip1 = new Clip ({ asset: audioAsset1 , duration: parseFloat ( audio . length ) });
audioTrack . addClip ( 4 , audioClip1 );

timeline . addTrack ( audioTrack );
```

## [ Step 7: Review and Share](#step-7-review-and-share)

Preview the trailer with the integrated narration to ensure it aligns with your vision. Once satisfied, share the trailer with others to experience the enhanced storytelling.

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

## [ Bonus - Add Movie Poster](#bonus-add-movie-poster)

Let's add a "Coming Soon" style movie poster at the very end of the trailer. We'll upload an image URL and overlay it on the video.

Python

Node.js

```
from videodb import MediaType

# Upload movie poster
poster_url = "https://img.freepik.com/free-photo/darkly-atmospheric-retail-environment-rendering_23-2151153755.jpg"
image = coll.upload( url = poster_url, media_type = MediaType.image)
```

```
import { MediaType } from 'videodb' ;

// Upload movie poster
const posterUrl = "https://img.freepik.com/free-photo/darkly-atmospheric-retail-environment-rendering_23-2151153755.jpg" ;
const image = await coll . uploadURL ({ url: posterUrl , mediaType: MediaType . image });
```

Python

Node.js

```
from videodb.editor import ImageAsset

# Create an overlay track for the poster
image_track = Track()

# Show poster at the 10 seconds of the trailer
image_asset = ImageAsset( id = image.id)
image_clip = Clip(
asset = image_asset,
duration = 10.0 ,
fit = "contain" )

image_track.add_clip( float (video.length) - 10 , image_clip)
timeline.add_track(image_track)

stream_url = timeline.generate_stream()
play_stream(stream_url)
```

```
import { EditorImageAsset } from 'videodb' ;

// Create an overlay track for the poster
const imageTrack = new Track ();

// Show poster at the 10 seconds of the trailer
const imageAsset = new EditorImageAsset ({ id: image . id });
const imageClip = new Clip ({
asset: imageAsset ,
duration: 10.0 ,
fit: "contain"
});

imageTrack . addClip ( parseFloat ( video . length ) - 10 , imageClip );
timeline . addTrack ( imageTrack );

const finalStreamUrl = await timeline . generateStream ();
console . log ( finalStreamUrl );
```

## [ Conclusion](#conclusion)

You've successfully built a sophisticated video editing workflow:

- **Analysis:** Automated scene understanding.
- **Generation:** AI Scripting and Voice synthesis.
- **Composition:** Non-linear editing with multi-track audio and image overlays.

Here's another interesting experiment to generate automatic voiceovers for silent footages. In this example, we've added the classic David Attenborough styled documentary narration to this footage of the underwater world. Check out the complete tutorial [here](\examples-and-tutorials\content-factory\voiceovers)

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## AI Voiceovers

Add professional narration to silent footage

## Voice Cloning

Clone voices for consistent brand audio

[AI Voiceovers](\examples-and-tutorials\content-factory\voiceovers) [Voice Cloning](\examples-and-tutorials\content-factory\voice-cloning)

⌘ I