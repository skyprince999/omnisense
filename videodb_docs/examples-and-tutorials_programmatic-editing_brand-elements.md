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
    - [Installing packages](#installing-packages)
    - [API Keys](#api-keys)
- [Implementation](#implementation)
    - [Step 1: Connect to VideoDB](#step-1-connect-to-videodb)
    - [Step 2: Upload Video and Image Assets](#step-2-upload-video-and-image-assets)
    - [Step 3: Add Brand Elements to Video](#step-3-add-brand-elements-to-video)
    - [Step 4: Add Brand Elements to Video](#step-4-add-brand-elements-to-video)
    - [Step 5: Review and Share](#step-5-review-and-share)
    - [Conclusion](#conclusion)
- [Related Tutorials](#related-tutorials)

[Programmatic Editing](\examples-and-tutorials\programmatic-editing\index)

# Brand Elements

Copy page

Add logos, text overlays, and custom styling

Copy page

Open In Colab

<!-- image -->

### [ Introduction](#introduction)

Adding brand elements like logos and overlay styles elevates your video content to new levels of professionalism. This tutorial will guide you through the process of integrating logos and custom text assets, ensuring your brand shines through in every frame. For this tutorial, we'll add Kyvos' branding to a video through image and text assets and see how those can be modified to enhance the content of raw footage. Although this is a quick example, the possibilities are endless! We look forward to seeing your experiments with these building blocks.

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

## [ Implementation](#implementation)

### [ Step 1: Connect to VideoDB](#step-1-connect-to-videodb)

Begin by establishing a connection to VideoDB using your API key:

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

### [ Step 2: Upload Video and Image Assets](#step-2-upload-video-and-image-assets)

Begin the branding process by uploading your video and image assets (base video and logo image) to VideoDB:

Python

Node.js

```
from videodb import MediaType

# Upload Video to VideoDB
video = coll.upload( url = "https://youtu.be/ps3cNAcPEMs" )

# Upload Image asset for branding
image = coll.upload( url = "https://raw.githubusercontent.com/video-db/videodb-cookbook-assets/main/images/examples/Kyvos_Logo.png" , media_type = MediaType.image)

print ( f "Video ID: { video.id } " )
print ( f "Image ID: { image.id } " )
```

```
import { MediaType } from 'videodb' ;

// Upload Video to VideoDB
const video = await coll . uploadURL ({ url: "https://youtu.be/ps3cNAcPEMs" });

// Upload Image asset for branding
const image = await coll . uploadURL ({
url: "https://raw.githubusercontent.com/video-db/videodb-cookbook-assets/main/images/examples/Kyvos_Logo.png" ,
mediaType: MediaType . image
});

console . log ( `Video ID: ${ video . id } ` );
console . log ( `Image ID: ${ image . id } ` );
```

Original Video:

Here's the logo (image asset) we will be using for this tutorial:

Kyvos logo example for brand elements tutorial

<!-- image -->

### [ Step 3: Add Brand Elements to Video](#step-3-add-brand-elements-to-video)

We'll define the text asset with styling parameters and create video/image assets for use in our timeline. The new Editor SDK uses a `Track` and `Clip` pattern for composing video. Each asset is wrapped in a `Clip` with duration and positioning controls.

Python

Node.js

```
from videodb.editor import (
Timeline, Track, Clip,
VideoAsset, ImageAsset, TextAsset,
Font, Border, Shadow, Background,
Alignment, HorizontalAlignment, VerticalAlignment, TextAlignment,
Position, Offset, Fit)

# Create the text asset with new styling parameters
text_asset = TextAsset(
text = "Visit kyvosinsights.com today!" ,
font = Font( family = "PT Sans" , size = 38 , color = "#F58C29" ),
border = Border( color = "#1D1C21" , width = 1 ),
background = Background( color = "#29272D" , border_width = 6 , opacity = 1.0 ),
alignment = Alignment(
horizontal = HorizontalAlignment.center,
vertical = VerticalAlignment.top),)

# Specify the video asset (trimmed from 0 to 44 seconds)
video_asset = VideoAsset( id = video.id, start = 0 )
video_duration = 44

# Image asset with positioning via Clip parameters
image_asset = ImageAsset( id = image.id)
```

```
import {
EditorTimeline , Track , Clip ,
EditorVideoAsset , EditorImageAsset , EditorTextAsset ,
Font , Border , Background ,
Alignment , HorizontalAlignment , VerticalAlignment , Position , Offset
} from 'videodb' ;

// Create the text asset with styling parameters
const textAsset = new EditorTextAsset ({
text: "Visit kyvosinsights.com today!" ,
font: new Font ({
family: "PT Sans" ,
size: 38 ,
color: "#F58C29"
}),
border: new Border ({ color: "#1D1C21" , width: 1 }),
background: new Background ({
color: "#29272D" ,
borderWidth: 6 ,
opacity: 1.0
}),
alignment: new Alignment ({
horizontal: HorizontalAlignment . center ,
vertical: VerticalAlignment . top
})
});

// Specify the video asset (trimmed from 0 to 44 seconds)
const videoAsset = new EditorVideoAsset ({ id: video . id , start: 0 });
const videoDuration = 44 ;

// Image asset with positioning via Clip parameters
const imageAsset = new EditorImageAsset ({ id: image . id });
```

### [ Step 4: Add Brand Elements to Video](#step-4-add-brand-elements-to-video)

Now we'll bring all assets together using the `Timeline` , `Track` , and `Clip` pattern. The video goes on the main track, while overlays (logo and text) go on a separate track with their start times.

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip, Position

timeline = Timeline(conn)

# Create the main video track
video_track = Track()
video_clip = Clip( asset = video_asset, duration = video_duration)
video_track.add_clip( 0 , video_clip)
timeline.add_track(video_track)

# Create overlay track for logo & text
overlay_track = Track()

# Add logo overlay (starts at 2.5s, duration 36s)
logo_clip = Clip(
asset = image_asset,
duration = 36 ,
fit = Fit.none,
scale = 0.15 ,
position = Position.top_right,
offset = Offset( x =- 0.02 , y = 0.02 ))
overlay_track.add_clip( 2.5 , logo_clip)

# Add text overlay (starts at 42s, duration 2s)
text_clip = Clip(
asset = text_asset,
duration = 2 ,
position = Position.top,
offset = Offset( y = 0.05 ))
overlay_track.add_clip( 42 , text_clip)

timeline.add_track(overlay_track)
```

```
const timeline = new EditorTimeline ( conn );

// Create the main video track
const videoTrack = new Track ();
const videoClip = new Clip ({ asset: videoAsset , duration: videoDuration });
videoTrack . addClip ( 0 , videoClip );
timeline . addTrack ( videoTrack );

// Create overlay track for logo & text
const overlayTrack = new Track ();

// Add logo overlay (starts at 2.5s, duration 36s)
const logoClip = new Clip ({
asset: imageAsset ,
duration: 36 ,
scale: 0.15 ,
position: Position . topRight ,
offset: new Offset ({ x: - 0.02 , y: 0.02 })
});
overlayTrack . addClip ( 2.5 , logoClip );

// Add text overlay (starts at 42s, duration 2s)
const textClip = new Clip ({
asset: textAsset ,
duration: 2 ,
position: Position . top ,
offset: new Offset ({ y: 0.05 })
});
overlayTrack . addClip ( 42 , textClip );

timeline . addTrack ( overlayTrack );
```

### [ Step 5: Review and Share](#step-5-review-and-share)

Review your branded video to ensure it aligns perfectly with your brand identity, then share it with your audience:

Python

Node.js

```
from videodb import play_stream

# Preview the branded video
stream_url = timeline.generate_stream()
play_stream(stream_url)
```

```
// Preview the branded video
const streamUrl = await timeline . generateStream ();
console . log ( streamUrl );
```

Let's have a look at the output!

### [ Conclusion](#conclusion)

Congratulations on mastering the art of branding with VideoDB! By seamlessly integrating brand elements into your videos, you've enhanced their professionalism and engagement. Experiment with different branding techniques to ensure your brand shines through in every frame.

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## Intro/Outro

Add opening and closing sequences to your videos

## Audio Overlay

Add background music and sound effects to your compositions

[Intro/Outro](\examples-and-tutorials\programmatic-editing\intro-outro) [Audio Overlay](\examples-and-tutorials\programmatic-editing\audio-overlay)

⌘ I