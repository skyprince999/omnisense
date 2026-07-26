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
- [Implementation](#implementation)
    - [Step 1: Connect VideoDB](#step-1-connect-videodb)
    - [Step 2: Upload Videos](#step-2-upload-videos)
    - [Step 3: Create assets](#step-3-create-assets)
    - [Step 4: Create timeline](#step-4-create-timeline)
    - [Step 5: Play the generated video stream](#step-5-play-the-generated-video-stream)
- [Conclusion](#conclusion)
- [Related Tutorials](#related-tutorials)

[Programmatic Editing](\examples-and-tutorials\programmatic-editing\index)

# Intro/Outro

Copy page

Add opening and closing sequences to videos

Copy page

Open In Colab

<!-- image -->

## [ Overview](#overview)

Imagine a virtual DJ mixing deck where you can seamlessly blend multiple videos into one epic timeline. Whether you're adding flashy intros, snazzy outros, or even splicing in some behind-the-scenes footage, this feature lets you take your video content to the next level! In this tutorial, let's dive into how you can seamlessly integrate multiple videos onto a single timeline. Users can easily enhance their video content by appending intros, outros, or supplementary segments. The workflow is straightforward and scalable.

Intro and outro sequence example showing video composition with opening and closing segments

<!-- image -->

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

Before proceeding, ensure access to VideoDB. Get your API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) . Free for first 50 uploads, no credit card required.

## [ Implementation](#implementation)

### [ Step 1: Connect VideoDB](#step-1-connect-videodb)

Connect to VideoDB using your API key to establish a session for uploading and manipulating video files. Import the necessary modules from VideoDB library to access functionalities.

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

### [ Step 2: Upload Videos](#step-2-upload-videos)

First, we upload an introductory video ("intro.mp4") and an outro video ("outro.mp4") into the collection, followed by the base video ("sugar\_craving.mp4"). This approach allows us to efficiently reuse the intro and outro videos for other projects by simply changing the base video, thereby saving time and streamlining the video creation process. You can upload the video asset from your local device or from a YouTube URL to upload the video from its source.

Python

Node.js

```
intro = coll.upload( url = "https://github.com/video-db/videodb-cookbook-assets/raw/main/videos/intro.mp4" )
outro = coll.upload( url = "https://github.com/video-db/videodb-cookbook-assets/raw/main/videos/outro.mp4" )
base = coll.upload( url = "https://github.com/video-db/videodb-cookbook-assets/raw/main/videos/sugar_craving.mp4" )
```

```
const intro = await coll . uploadURL ({
url: "https://github.com/video-db/videodb-cookbook-assets/raw/main/videos/intro.mp4"
});
const outro = await coll . uploadURL ({
url: "https://github.com/video-db/videodb-cookbook-assets/raw/main/videos/outro.mp4"
});
const base = await coll . uploadURL ({
url: "https://github.com/video-db/videodb-cookbook-assets/raw/main/videos/sugar_craving.mp4"
});
```

### [ Step 3: Create assets](#step-3-create-assets)

Adjust parameters for all the video assets according to your preference, such as start and end times.

Python

Node.js

```
from videodb.editor import VideoAsset

intro_asset = VideoAsset( id = intro.id, start = 0 )
intro_duration = 3

base_asset = VideoAsset( id = base.id, start = 0 )
base_duration = 90

outro_asset = VideoAsset( id = outro.id, start = 0 )
outro_duration = 3
```

```
import { EditorVideoAsset } from 'videodb' ;

const introAsset = new EditorVideoAsset ({ id: intro . id , start: 0 });
const introDuration = 3 ;

const baseAsset = new EditorVideoAsset ({ id: base . id , start: 0 });
const baseDuration = 90 ;

const outroAsset = new EditorVideoAsset ({ id: outro . id , start: 0 });
const outroDuration = 3 ;
```

### [ Step 4: Create timeline](#step-4-create-timeline)

Create video assets using the Editor SDK. The `start` parameter in `VideoAsset` trims from the beginning, and the `duration` in `Clip` controls how long the clip plays.

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip

timeline = Timeline(conn)

# Create main track
track = Track()

# Add intro clip at 0 seconds
intro_clip = Clip( asset = intro_asset, duration = intro_duration)
track.add_clip( 0 , intro_clip)

# Add base video clip after intro
base_clip = Clip( asset = base_asset, duration = base_duration)
track.add_clip(intro_duration, base_clip)

# Add outro clip after base video
outro_clip = Clip( asset = outro_asset, duration = outro_duration)
track.add_clip(intro_duration + base_duration, outro_clip)

timeline.add_track(track)
```

```
import { EditorTimeline , Track , Clip } from 'videodb' ;

const timeline = new EditorTimeline ( conn );

// Create main track
const track = new Track ();

// Add intro clip at 0 seconds
const introClip = new Clip ({ asset: introAsset , duration: introDuration });
track . addClip ( 0 , introClip );

// Add base video clip after intro
const baseClip = new Clip ({ asset: baseAsset , duration: baseDuration });
track . addClip ( introDuration , baseClip );

// Add outro clip after base video
const outroClip = new Clip ({ asset: outroAsset , duration: outroDuration });
track . addClip ( introDuration + baseDuration , outroClip );

timeline . addTrack ( track );
```

### [ Step 5: Play the generated video stream](#step-5-play-the-generated-video-stream)

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

Preview the video to ensure it functions correctly. Once satisfied, generate a stream of the video and share the link for others to view and enjoy this wholesome creation! **Output:**

## [ Conclusion](#conclusion)

You can now efficiently manipulate and assemble video elements, resulting in professional-quality compositions.

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## Brand Elements

Add logos, text overlays, and custom styling to your videos

## Timeline Architecture

Learn the fundamentals of VideoDB's programmable video editing

[Overview](\examples-and-tutorials\programmatic-editing) [Brand Elements](\examples-and-tutorials\programmatic-editing\brand-elements)

⌘ I