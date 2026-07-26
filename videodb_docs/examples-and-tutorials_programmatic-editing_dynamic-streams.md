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
- [Steps](#steps)
    - [Step 1: Connect to VideoDB](#step-1-connect-to-videodb)
    - [🗳️ Step 2: Upload Base Video](#-step-2-upload-base-video)
    - [Step 3: Fetch Data from a Random User API](#step-3-fetch-data-from-a-random-user-api)
    - [Step 4: Upload the image to VideoDB](#step-4-upload-the-image-to-videodb)
    - [Step 5: Create VideoDB Assets](#step-5-create-videodb-assets)
    - [↔️ Step 6: Create the VideoDB Timeline](#-step-6-create-the-videodb-timeline)
    - [▶️ Step 7: Generate and Play the Personalized Stream](#-step-7-generate-and-play-the-personalized-stream)
- [Conclusion](#conclusion)
- [Related Tutorials](#related-tutorials)

[Programmatic Editing](\examples-and-tutorials\programmatic-editing\index)

# Dynamic Streams

Copy page

Create personalized video streams with data overlays

Copy page

Open In Colab

<!-- image -->

## [ Introduction](#introduction)

Imagine you're watching a captivating keynote session from your favorite conference, and you're welcomed with a personalized stream just for you. This tutorial demonstrates how to create dynamic video streams by integrating data from custom databases and external APIs. We'll use a practical example: a recording of a [Config 2023](https://www.youtube.com/watch?v=Nmv8XdFiej0) keynote session. By using VideoDB, we'll show how companies like [Figma](https://www.figma.com/files/recents-and-sharing?fuid=940498258276625180) can personalize the viewing experience for their audience, delivering a richer and more engaging experience. We'll showcase how to:

- **Fetch data from a random user API** to represent a hypothetical viewer.
- Integrate this data into a **custom VideoDB timeline** .
- Create a **personalized stream** that dynamically displays relevant information alongside the keynote video.

This tutorial is your guide to unlocking the potential of dynamic video streams and transforming your video content with personalized experiences.

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

### [ 🗳️ Step 2: Upload Base Video](#-step-2-upload-base-video)

Upload and play the video to ensure it's correctly loaded. We'll be using [this video](https://www.youtube.com/watch?v=Nmv8XdFiej0) for the purpose of this tutorial.

Python

Node.js

```
# Upload and play a video from a URL
video = coll.upload( url = "https://www.youtube.com/watch?v=Nmv8XdFiej0" )
video.play()

# Alternatively, get a video from your VideoDB collection
# video = coll.get_video('VIDEO_ID_HERE')
# video.play()
```

```
// Upload and play a video from a URL
const video = await coll . uploadURL ({ url: "https://www.youtube.com/watch?v=Nmv8XdFiej0" });
console . log ( video . playerUrl );

// Alternatively, get a video from your VideoDB collection
// const video = await coll.getVideo('VIDEO_ID_HERE');
// console.log(video.playerUrl);
```

### [ Step 3: Fetch Data from a Random User API](#step-3-fetch-data-from-a-random-user-api)

This code fetches a random user's data (name and picture) from the "randomuser.me" API. You can adapt this to retrieve data from any relevant API (e.g., product data, news articles) for your use case.

Python

Node.js

```
import requests

# Make a request to the Randomizer API
response = requests.get( 'https://randomuser.me/api/?results=1&nat=us,ca,gb,au' )
data = response.json()

# Extract relevant information
first_name = data[ 'results' ][ 0 ][ 'name' ][ 'first' ]
medium_picture = data[ 'results' ][ 0 ][ 'picture' ][ 'medium' ]
```

```
// Make a request to the Randomizer API
const response = await fetch ( 'https://randomuser.me/api/?results=1&nat=us,ca,gb,au' );
const data = await response . json ();

// Extract relevant information
const firstName = data . results [ 0 ]. name . first ;
const mediumPicture = data . results [ 0 ]. picture . medium ;
```

### [ Step 4: Upload the image to VideoDB](#step-4-upload-the-image-to-videodb)

- First we download the image to local storage
- Then we use the local path to upload it to VideoDB

Python

Node.js

```
import requests

# 1. Download the image locally
local_path = "my_local_image.jpg"

response = requests.get(medium_picture)
if response.status_code == 200 :
with open (local_path, 'wb' ) as f:
f.write(response.content)
print ( f "Image downloaded successfully to: { local_path } " )
else :
print ( f "Failed to download image. Status code: { response.status_code } " )

# 2. Upload using the local file path

from videodb import play_stream, MediaType
image = coll.upload( file_path = local_path, media_type = MediaType.image)

print ( f "Image uploaded to VideoDB: { image.id } " )
```

```
import * as fs from 'fs' ;
import { MediaType } from 'videodb' ;

// 1. Download the image locally
const localPath = "my_local_image.jpg" ;

const imgResponse = await fetch ( mediumPicture );
if ( imgResponse . ok ) {
const buffer = Buffer . from ( await imgResponse . arrayBuffer ());
fs . writeFileSync ( localPath , buffer );
console . log ( `Image downloaded successfully to: ${ localPath } ` );
} else {
console . log ( `Failed to download image. Status code: ${ imgResponse . status } ` );
}

// 2. Upload using the local file path
const image = await coll . uploadFile ({
filePath: localPath ,
mediaType: MediaType . image
});

console . log ( `Image uploaded to VideoDB: ${ image . id } ` );
```

### [ Step 5: Create VideoDB Assets](#step-5-create-videodb-assets)

We create VideoDB assets for the base video, the user's name (text), and their picture (image) using the new Editor SDK. The `Font` and `Background` objects allow us to customize the appearance of text elements.

Python

Node.js

```
from videodb.editor import (
Timeline, Track, Clip,
VideoAsset, TextAsset, ImageAsset,
Font, Background, Alignment, HorizontalAlignment, VerticalAlignment,
Position, Offset, Fit)

# 1. Video Asset (Base background)
video_asset = VideoAsset( id = video.id, start = 0 )

# 2. Name Asset (Top)
name_asset = TextAsset(
text = f 'Hi { first_name } !' ,
font = Font( family = "Montserrat" , size = 60 , color = "#000000" ),
background = Background( color = "#D2C11D" , border_width = 20 , opacity = 1.0 ),
alignment = Alignment( horizontal = HorizontalAlignment.center, vertical = VerticalAlignment.top),)

# 3. Message Asset (Middle)
cmon_asset = TextAsset(
text = "Here are your favorite moments" ,
font = Font( family = "Montserrat" , size = 60 , color = "#D2C11D" ),
background = Background( color = "#000000" , border_width = 20 , opacity = 1.0 ),
alignment = Alignment( horizontal = HorizontalAlignment.center, vertical = VerticalAlignment.center),)

# 4. Image Asset (Bottom)
image_asset = ImageAsset( id = image.id)
```

```
import {
EditorTimeline , Track , Clip ,
EditorVideoAsset , EditorTextAsset , EditorImageAsset ,
Font , Background , Alignment , HorizontalAlignment , VerticalAlignment ,
Position , Offset
} from 'videodb' ;

// 1. Video Asset (Base background)
const videoAsset = new EditorVideoAsset ({ id: video . id , start: 0 });

// 2. Name Asset (Top)
const nameAsset = new EditorTextAsset ({
text: `Hi ${ firstName } !` ,
font: new Font ({ family: "Montserrat" , size: 60 , color: "#000000" }),
background: new Background ({ color: "#D2C11D" , borderWidth: 20 , opacity: 1.0 }),
alignment: new Alignment ({ horizontal: HorizontalAlignment . center , vertical: VerticalAlignment . top })
});

// 3. Message Asset (Middle)
const cmonAsset = new EditorTextAsset ({
text: "Here are your favorite moments" ,
font: new Font ({ family: "Montserrat" , size: 60 , color: "#D2C11D" }),
background: new Background ({ color: "#000000" , borderWidth: 20 , opacity: 1.0 }),
alignment: new Alignment ({ horizontal: HorizontalAlignment . center , vertical: VerticalAlignment . center })
});

// 4. Image Asset (Bottom)
const imageAsset = new EditorImageAsset ({ id: image . id });
```

### [ ↔️ Step 6: Create the VideoDB Timeline](#-step-6-create-the-videodb-timeline)

Using the `Track` and `Clip` pattern, we arrange and layer assets to create a dynamic video stream. The main video goes on one track, while overlays (name, message, image) go on separate tracks with their start times.

Python

Node.js

```
# Create the timeline
timeline = Timeline(conn)

# --- Track 1: Main Video ---
video_track = Track()
video_clip = Clip( asset = video_asset, duration = float (video.length))
video_track.add_clip( 0 , video_clip)
timeline.add_track(video_track)

# --- Track 2: Overlays ---
overlay_track = Track()

# 1. Add Name Overlay (Top)
name_clip = Clip(
asset = name_asset,
duration = 4 ,
position = Position.top,
offset = Offset( y = 0.15 ))
overlay_track.add_clip( 5 , name_clip)

# 2. Add Message Overlay (Center)
cmon_clip = Clip(
asset = cmon_asset,
duration = 4 ,
position = Position.center,)
overlay_track.add_clip( 5 , cmon_clip)

# 3. Add Image Overlay (Bottom)
image_clip = Clip(
asset = image_asset,
duration = 4 ,
position = Position.bottom,
scale = 2 ,
fit = Fit.none,
offset = Offset( y =- 0.15 ))
overlay_track.add_clip( 5 , image_clip)

timeline.add_track(overlay_track)
```

```
// Create the timeline
const timeline = new EditorTimeline ( conn );

// --- Track 1: Main Video ---
const videoTrack = new Track ();
const videoClip = new Clip ({ asset: videoAsset , duration: parseFloat ( video . length ) });
videoTrack . addClip ( 0 , videoClip );
timeline . addTrack ( videoTrack );

// --- Track 2: Overlays ---
const overlayTrack = new Track ();

// 1. Add Name Overlay (Top)
const nameClip = new Clip ({
asset: nameAsset ,
duration: 4 ,
position: Position . top ,
offset: new Offset ({ y: 0.15 })
});
overlayTrack . addClip ( 5 , nameClip );

// 2. Add Message Overlay (Center)
const cmonClip = new Clip ({
asset: cmonAsset ,
duration: 4 ,
position: Position . center
});
overlayTrack . addClip ( 5 , cmonClip );

// 3. Add Image Overlay (Bottom)
const imageClip = new Clip ({
asset: imageAsset ,
duration: 4 ,
position: Position . bottom ,
scale: 2 ,
offset: new Offset ({ y: - 0.15 })
});
overlayTrack . addClip ( 5 , imageClip );

timeline . addTrack ( overlayTrack );
```

### [ ▶️ Step 7: Generate and Play the Personalized Stream](#-step-7-generate-and-play-the-personalized-stream)

The `generate_stream()` method creates a streamable URL for your personalized video stream. You can then use `play_stream()` to preview it in your browser.

Python

Node.js

```
from videodb import play_stream

stream_url = timeline.generate_stream()
print (stream_url)
play_stream(stream_url)
```

```
const streamUrl = await timeline . generateStream ();
console . log ( streamUrl );
```

## [ Conclusion](#conclusion)

This tutorial showcased how to create personalized video streams using VideoDB. By integrating data from external APIs and custom databases, you can enhance your video content, personalize user experiences, and unlock new possibilities for engagement. Explore various data sources, experiment with different integrations, and customize your video streams to suit your specific needs.

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## Intro &amp; Outro

Auto-add opening and closing sequences

## Dynamic Ads

Insert personalized ads per viewer

[Dynamic Ads](\examples-and-tutorials\programmatic-editing\dynamic-ads) [Word Counter](\examples-and-tutorials\programmatic-editing\word-counter)

⌘ I