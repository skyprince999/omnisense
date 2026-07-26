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

- [Setup](#setup)
    - [Installing VideoDB in your environment](#installing-videodb-in-your-environment)
    - [Setting Up a connection to VideoDB](#setting-up-a-connection-to-videodb)
- [Uploading the videos to VideoDB](#uploading-the-videos-to-videodb)
- [Inserting Ad in our Base Video](#inserting-ad-in-our-base-video)
- [Play Modified Video](#play-modified-video)
- [No Limitations](#no-limitations)
- [Related Tutorials](#related-tutorials)

[Programmatic Editing](\examples-and-tutorials\programmatic-editing\index)

# Dynamic Ads

Copy page

Insert advertisements into video streams

Copy page

Open In Colab

<!-- image -->

Video files are not very flexible if we want to change the flow and insert another video at a certain place. Imagine putting a video advertisement on your video stream for your customers. You don't need to edit the video file and create another one. VideoDB simplifies it for you. It gives you power to build contextual Ad insertion and personalized Ad insertion on your videos.

Dynamic advertisement insertion example showing ad placement in video streams

<!-- image -->

## [ Setup](#setup)

### [ Installing VideoDB in your environment](#installing-videodb-in-your-environment)

`VideoDB` is available as a [python package](https://pypi.org/project/videodb)

Python

Node.js

```
! pip install videodb
```

```
npm install videodb
```

### [ Setting Up a connection to VideoDB](#setting-up-a-connection-to-videodb)

To connect to VideoDB, simply create a Connection object, and connect to the collection. This can be done by either providing your VideoDB API key directly to the constructor or by setting the `VIDEO_DB_API_KEY` environment variable with your API key. Get your API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) . Free for first 50 uploads, no credit card required.

Python

Node.js

```
import videodb

# Connect to VideoDB
api_key = "your_api_key"
conn = videodb.connect( api_key = api_key)
coll = conn.get_collection()
```

```
import { connect } from 'videodb' ;

const conn = await connect ({ apiKey: process . env . VIDEO_DB_API_KEY });
const coll = await conn . getCollection ();
```

## [ Uploading the videos to VideoDB](#uploading-the-videos-to-videodb)

Let's have a base video as Sam Altman's conversation on OpenAI and AGI. We'll choose another video to insert in this 👉 (let's get IBM's Advertisement). We are going to insert the Ad video into the base video at a specific timestamp. For this, we will need to first upload both the videos to `VideoDB` .

Python

Node.js

```
base_video_url = "https://www.youtube.com/watch?v=e1cf58VWzt8"
ad_video_url = "https://www.youtube.com/watch?v=jtwduf2lh08"

base_video = coll.upload( url = base_video_url)
ad_video = coll.upload( url = ad_video_url)
```

```
const baseVideoUrl = "https://www.youtube.com/watch?v=e1cf58VWzt8" ;
const adVideoUrl = "https://www.youtube.com/watch?v=jtwduf2lh08" ;

const baseVideo = await coll . uploadURL ({ url: baseVideoUrl });
const adVideo = await coll . uploadURL ({ url: adVideoUrl });
```

## [ Inserting Ad in our Base Video](#inserting-ad-in-our-base-video)

Now that we have both videos uploaded, we'll use VideoDB's Editor SDK to create a timeline with multiple clips. We'll break the base video into segments and insert the ad at the 10-second mark:

1. **Clip 1** : Base video from 0 to 10 seconds
2. **Clip 2** : Full ad video
3. **Clip 3** : Base video continues from 10 seconds to end

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip, VideoAsset
from videodb import play_stream

# Define timing
insert_time = 10 # Insert ad at 10 seconds
base_duration = int (base_video.length)
ad_duration = int (ad_video.length)

# Create timeline and track
timeline = Timeline(conn)
track = Track()

# Clip 1: Base video from 0 to insert_time
clip1 = Clip(
asset = VideoAsset( id = base_video.id),
duration = insert_time)
track.add_clip( 0 , clip1)

# Clip 2: Full ad video
clip2 = Clip(
asset = VideoAsset( id = ad_video.id),
duration = ad_duration)
track.add_clip(insert_time, clip2)

# Clip 3: Base video continues from insert_time to end
clip3 = Clip(
asset = VideoAsset( id = base_video.id, start = insert_time),
duration = base_duration - insert_time)
track.add_clip(insert_time + ad_duration, clip3)

# Generate stream
timeline.add_track(track)
stream_link = timeline.generate_stream()
```

```
import { EditorTimeline , Track , Clip , EditorVideoAsset } from 'videodb' ;

// Define timing
const insertTime = 10 ; // Insert ad at 10 seconds
const baseDuration = parseInt ( baseVideo . length );
const adDuration = parseInt ( adVideo . length );

// Create timeline and track
const timeline = new EditorTimeline ( conn );
const track = new Track ();

// Clip 1: Base video from 0 to insertTime
const clip1 = new Clip ({
asset: new EditorVideoAsset ({ id: baseVideo . id }),
duration: insertTime
});
track . addClip ( 0 , clip1 );

// Clip 2: Full ad video
const clip2 = new Clip ({
asset: new EditorVideoAsset ({ id: adVideo . id }),
duration: adDuration
});
track . addClip ( insertTime , clip2 );

// Clip 3: Base video continues from insertTime to end
const clip3 = new Clip ({
asset: new EditorVideoAsset ({ id: baseVideo . id , start: insertTime }),
duration: baseDuration - insertTime
});
track . addClip ( insertTime + adDuration , clip3 );

// Generate stream
timeline . addTrack ( track );
const streamLink = await timeline . generateStream ();
```

`stream_link` is a streaming link that offers instant playback capability - no rendering necessary. ⚡️

## [ Play Modified Video](#play-modified-video)

Let's check the results:

Python

Node.js

```
from videodb import play_stream
play_stream(stream_link)
```

```
console . log ( streamLink );
```

You can generate as many streaming links as needed for your use-case. This gives you power to personalize your video content for each user.

## [ No Limitations](#no-limitations)

The inserted video doesn't have to be solely for advertisements; it can be a disclaimer or announcement for the person watching the video. Furthermore, your stream is dynamic, enabling you to adjust the timestamp and insertion video based on your business logic. This is an incredible power to have for any product hosting videos. Let's master video content manipulation like a pro!

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## Brand Elements

Add logos, watermarks, and graphics

## Dynamic Streams

Generate multiple versions from one source

[Audio Overlay](\examples-and-tutorials\programmatic-editing\audio-overlay) [Dynamic Streams](\examples-and-tutorials\programmatic-editing\dynamic-streams)

⌘ I