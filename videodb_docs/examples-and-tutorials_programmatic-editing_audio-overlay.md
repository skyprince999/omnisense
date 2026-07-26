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
    - [Installing packages](#installing-packages)
    - [API Keys](#api-keys)
- [Steps](#steps)
    - [Step 1: Connect to VideoDB](#step-1-connect-to-videodb)
    - [Step 2: Upload Video](#step-2-upload-video)
    - [Step 3: Upload Audio](#step-3-upload-audio)
    - [Step 4: Create assets](#step-4-create-assets)
    - [Step 5: Create a Timeline](#step-5-create-a-timeline)
    - [Final Step: Review and Share](#final-step-review-and-share)
- [Conclusion](#conclusion)
- [Related Tutorials](#related-tutorials)

[Programmatic Editing](\examples-and-tutorials\programmatic-editing\index)

# Audio Overlay

Copy page

Combine multiple audio tracks with video

Copy page

Open In Colab

<!-- image -->

## [ Overview](#overview)

Welcome to the groovy world of audio overlays with VideoDB! 🎶 In this tutorial, we're diving into the magic of adding audio overlays to your video assets. Picture this: you've got your video content all set, but it's missing that extra oomph. That's where audio overlay swoops in to save the day! With VideoDB's easy-to-use feature, you can seamlessly weave in background music, voiceovers, or funky sound effects, transforming your videos from ordinary to extraordinary. Let's crank up the volume and get ready to rock and roll!

## [ Setup](#setup)

### [ Installing packages](#installing-packages)

Python

Node.js

```
! pip install videodb
```

```
npm install videodb
```

### [ API Keys](#api-keys)

Before proceeding, ensure access to [VideoDB](https://videodb.io/) Get your API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) . ( Free for first 50 uploads, No credit card required)

## [ Steps](#steps)

### [ Step 1: Connect to VideoDB](#step-1-connect-to-videodb)

Connect to VideoDB to establish a session for uploading and manipulating video files. Import the necessary modules from VideoDB library to access functionalities.

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

const conn = await connect ({ apiKey: process . env . VIDEO_DB_API_KEY });
const coll = await conn . getCollection ();
```

### [ Step 2: Upload Video](#step-2-upload-video)

Upload the video to VideoDB collection. You can upload the video asset from your local device or from a YouTube URL to upload the video from its source.

Python

Node.js

```
video = coll.upload( url = "https://youtu.be/e49VEpWg61M" )
video.play()
```

```
const video = await coll . uploadURL ({
url: "https://youtu.be/e49VEpWg61M"
});
console . log ( video . playerUrl );
```

You can upload from your local file system too by passing `file_path` in `upload()` Here's the video we'll be using for this tutorial:

### [ Step 3: Upload Audio](#step-3-upload-audio)

Upload the audio file to VideoDB collection. You can upload the audio asset from your local device or from a YouTube URL to upload the audio from its source. Make sure to mention `media_type` if you want to use audio track of a video.

Python

Node.js

```
audio = coll.upload( url = "https://youtu.be/_Gd8mbQ3-mI" , media_type = "audio" )
```

```
import { MediaType } from 'videodb' ;

const audio = await coll . uploadURL ({
url: "https://youtu.be/_Gd8mbQ3-mI" ,
mediaType: MediaType . audio
});
```

### [ Step 4: Create assets](#step-4-create-assets)

Create assets for Audio and Video using `VideoAsset` and `AudioAsset` from the Editor SDK.

Python

Node.js

```
from videodb.editor import VideoAsset, AudioAsset

video_asset = VideoAsset( id = video.id, volume = 0.5 ) # Reducing volume of the original video

audio_asset = AudioAsset( id = audio.id)
```

```
import { EditorVideoAsset , EditorAudioAsset } from 'videodb' ;

const videoAsset = new EditorVideoAsset ({
id: video . id ,
volume: 0.5 // Reducing volume of the original video
});

const audioAsset = new EditorAudioAsset ({
id: audio . id
});
```

### [ Step 5: Create a Timeline](#step-5-create-a-timeline)

Create a timeline using the `Track` and `Clip` pattern. Add the video clip and audio clip to a track, then add the track to the timeline.

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip

# Create a new timeline
timeline = Timeline(conn)

# Create a track with video and audio clips
track = Track()

# Add video clip (full duration)
video_clip = Clip( asset = video_asset, duration = float (video.length))
track.add_clip( 0 , video_clip)

# Add audio overlay clip starting at 0
audio_clip = Clip( asset = audio_asset, duration = float (video.length))
track.add_clip( 0 , audio_clip)

timeline.add_track(track)
```

```
import { EditorTimeline , Track , Clip } from 'videodb' ;

// Create a new timeline
const timeline = new EditorTimeline ( conn );

// Create a track with video and audio clips
const track = new Track ();

// Add video clip (full duration)
const videoDuration = parseFloat ( video . length );
const videoClip = new Clip ({ asset: videoAsset , duration: videoDuration });
track . addClip ( 0 , videoClip );

// Add audio overlay clip starting at 0
const audioClip = new Clip ({ asset: audioAsset , duration: videoDuration });
track . addClip ( 0 , audioClip );

timeline . addTrack ( track );
```

### [ Final Step: Review and Share](#final-step-review-and-share)

Preview the video with the integrated voiceover to ensure it functions correctly. Once satisfied, generate a stream of the video and share the link for others to view and enjoy this wholesome creation!

Python

Node.js

```
from videodb import play_stream

stream = timeline.generate_stream()
play_stream(stream)
```

```
const stream = await timeline . generateStream ();
console . log ( stream );
```

## [ Conclusion](#conclusion)

And there you have it, folks! We've unlocked the door to audio awesomeness with VideoDB's audio overlay feature. By seamlessly integrating background music, voiceovers, or sound effects into your videos, you're not just adding layers of sound - you're adding layers of engagement, emotion, and excitement!

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## AI Voiceovers

Generate professional narration with AI voice synthesis

## Intro/Outro

Add polished opening and closing sequences

[Brand Elements](\examples-and-tutorials\programmatic-editing\brand-elements) [Dynamic Ads](\examples-and-tutorials\programmatic-editing\dynamic-ads)

⌘ I