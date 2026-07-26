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
    - [Step 2: Upload Video](#step-2-upload-video)
    - [Step 3: Indexing Spoken Words](#step-3-indexing-spoken-words)
    - [Step 4: Keyword Search](#step-4-keyword-search)
    - [Step 5: Setup Timeline and Audio](#step-5-setup-timeline-and-audio)
    - [Step 6: Overlay Text and Audio](#step-6-overlay-text-and-audio)
    - [Step 7: Generate and Play the Stream](#step-7-generate-and-play-the-stream)
    - [Conclusion](#conclusion)
    - [Tips and Tricks](#tips-and-tricks)
- [Related Tutorials](#related-tutorials)

[Programmatic Editing](\examples-and-tutorials\programmatic-editing\index)

# Word Counter

Copy page

Visualize keyword occurrences in videos

Copy page

Open In Colab

<!-- image -->

### [ Introduction](#introduction)

With an endless stream of new video content on our feeds, engaging the audience with dynamic visual elements can make educational and promotional videos much more impactful. VideoDB's suite of features allows you to enhance videos with programmatic editing. In this tutorial, we'll explore how to create a video that visually counts and displays instances of a specified word as it's spoken. We'll use VideoDB's [Keyword Search](\examples-and-tutorials\video-rag\keyword-search) to index spoken words, and then apply audio and [text overlays](\pages\act\programmable-editing\text-asset) to show a counter updating in real-time with synchronized audio cues.

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

Before proceeding, ensure access to [VideoDB](https://videodb.io/) and set up Get your API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) . ( Free for first 50 uploads, No credit card required)

## [ Steps](#steps)

### [ Step 1: Connect to VideoDB](#step-1-connect-to-videodb)

Establish a session for uploading videos. Import the necessary modules from VideoDB library to access functionalities.

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

Upload and play the video to ensure it's correctly loaded. We'll be using [this video](https://www.youtube.com/watch?v=Js4rTM2Z1Eg) for the purpose of this tutorial.

Python

Node.js

```
video = coll.upload( url = "https://www.youtube.com/watch?v=Js4rTM2Z1Eg" )
video.play()
```

```
const video = await coll . uploadURL ({ url: "https://www.youtube.com/watch?v=Js4rTM2Z1Eg" });
console . log ( video . playerUrl );
```

### [ Step 3: Indexing Spoken Words](#step-3-indexing-spoken-words)

Index the video to identify and timestamp all spoken words.

Python

Node.js

```
video.index_spoken_words()
```

```
await video . indexSpokenWords ();
```

### [ Step 4:  Keyword Search](#step-4-keyword-search)

Search within the video for the keyword *("education" in this example)* , and note each occurrence.

Python

Node.js

```
from videodb import SearchType

result = video.search( query = "education" , search_type = SearchType.keyword)
```

```
import { SearchTypeValues } from 'videodb' ;

const result = await video . search ({
query: "education" ,
searchType: SearchTypeValues . keyword
});
```

### [ Step 5:  Setup Timeline and Audio](#step-5-setup-timeline-and-audio)

Initialize the timeline and prepare an audio asset to use for each word occurrence.

Python

Node.js

```
from videodb.editor import Timeline, Track, Clip, AudioAsset, VideoAsset, TextAsset
from videodb.editor import Font, Background, Alignment, HorizontalAlignment, VerticalAlignment, Position, Offset
from videodb import MediaType

timeline = Timeline(conn)

# Upload the twink sound effect
audio = coll.upload( url = "https://github.com/video-db/videodb-cookbook-assets/raw/main/audios/twink.mp3" , media_type = MediaType.audio)
```

```
import {
EditorTimeline , Track , Clip , EditorAudioAsset , EditorVideoAsset , EditorTextAsset ,
Font , Background , Alignment , HorizontalAlignment , VerticalAlignment , Position , Offset
} from 'videodb' ;
import { MediaType } from 'videodb' ;

const timeline = new EditorTimeline ( conn );

// Upload the twink sound effect
const audio = await coll . uploadURL ({
url: "https://github.com/video-db/videodb-cookbook-assets/raw/main/audios/twink.mp3" ,
mediaType: MediaType . audio
});
```

### [ Step 6:  Overlay Text and Audio](#step-6-overlay-text-and-audio)

Add text and audio overlays at each instance where the word is spoken using the `Track` and `Clip` pattern. Note: Adding the 'padding' is an optional step. It helps in adding a little more context to the exact instance identified, thus resulting in a better compiled output.

Python

Node.js

```
video_duration = min ( 300 , int (video.length)) # First 5 minutes only
audio_offset = 1 # Delay audio/text update by 1 second for better sync

# Create timeline and tracks
timeline = Timeline(conn)
video_track = Track()
text_track = Track()
audio_track = Track()

# Add video clip (first 5 minutes)
video_clip = Clip(
asset = VideoAsset( id = video.id, start = 0 ),
duration = video_duration)
video_track.add_clip( 0 , video_clip)

# Filter shots within our duration
shots_in_range = [s for s in result.shots if int (s.start) + audio_offset < video_duration]

# Add text overlays that update at each word occurrence
for i, shot in enumerate (shots_in_range):
trigger_time = int (shot.start) + audio_offset

# Initial "Count-0" from start until first word
if i == 0 and trigger_time > 0 :
text_asset = TextAsset(
text = "Count-0" ,
font = Font( family = "Do Hyeon" , size = 72 , color = "#000100" ),
background = Background( color = "#F702A4" , opacity = 1.0 ),
alignment = Alignment( horizontal = HorizontalAlignment.right, vertical = VerticalAlignment.top),)
text_clip = Clip( asset = text_asset, duration = trigger_time,
position = Position.top_right, offset = Offset( x =- 0.05 , y = 0.05 ))
text_track.add_clip( 0 , text_clip)

# Duration until next word or end of video
if i + 1 < len (shots_in_range):
next_trigger = int (shots_in_range[i + 1 ].start) + audio_offset
else :
next_trigger = video_duration

text_dur = next_trigger - trigger_time

# Text overlay with updated count
text_asset = TextAsset(
text = f "Count- { i + 1 } " ,
font = Font( family = "Do Hyeon" , size = 72 , color = "#000100" ),
background = Background( color = "#F702A4" , opacity = 1.0 ),
alignment = Alignment( horizontal = HorizontalAlignment.right, vertical = VerticalAlignment.top),)
text_clip = Clip( asset = text_asset, duration = text_dur, position = Position.top_right, offset = Offset( x =- 0.05 , y = 0.05 ))
text_track.add_clip(trigger_time, text_clip)

# Audio cue at same trigger time
if trigger_time < video_duration - 2 :
audio_clip = Clip( asset = AudioAsset( id = audio.id), duration = 2 )
audio_track.add_clip(trigger_time, audio_clip)

# Add all tracks to timeline
timeline.add_track(video_track)
timeline.add_track(text_track)
timeline.add_track(audio_track)
```

```
const videoDuration = Math . min ( 300 , parseInt ( video . length )); // First 5 minutes only
const audioOffset = 1 ; // Delay audio/text update by 1 second for better sync

// Create timeline and tracks
const timeline = new EditorTimeline ( conn );
const videoTrack = new Track ();
const textTrack = new Track ();
const audioTrack = new Track ();

// Add video clip (first 5 minutes)
const videoClip = new Clip ({
asset: new EditorVideoAsset ({ id: video . id , start: 0 }),
duration: videoDuration
});
videoTrack . addClip ( 0 , videoClip );

// Filter shots within our duration
const shotsInRange = result . shots . filter ( s => parseInt ( s . start ) + audioOffset < videoDuration );

// Add text overlays that update at each word occurrence
shotsInRange . forEach (( shot , i ) => {
const triggerTime = parseInt ( shot . start ) + audioOffset ;

// Initial "Count-0" from start until first word
if ( i === 0 && triggerTime > 0 ) {
const textAsset = new EditorTextAsset ({
text: "Count-0" ,
font: new Font ({ family: "Do Hyeon" , size: 72 , color: "#000100" }),
background: new Background ({ color: "#F702A4" , opacity: 1.0 }),
alignment: new Alignment ({ horizontal: HorizontalAlignment . right , vertical: VerticalAlignment . top })
});
const textClip = new Clip ({
asset: textAsset ,
duration: triggerTime ,
position: Position . topRight ,
offset: new Offset ({ x: - 0.05 , y: 0.05 })
});
textTrack . addClip ( 0 , textClip );
}

// Duration until next word or end of video
const nextTrigger = i + 1 < shotsInRange . length
? parseInt ( shotsInRange [ i + 1 ]. start ) + audioOffset
: videoDuration ;

const textDur = nextTrigger - triggerTime ;

// Text overlay with updated count
const textAsset = new EditorTextAsset ({
text: `Count- ${ i + 1 } ` ,
font: new Font ({ family: "Do Hyeon" , size: 72 , color: "#000100" }),
background: new Background ({ color: "#F702A4" , opacity: 1.0 }),
alignment: new Alignment ({ horizontal: HorizontalAlignment . right , vertical: VerticalAlignment . top })
});
const textClip = new Clip ({
asset: textAsset ,
duration: textDur ,
position: Position . topRight ,
offset: new Offset ({ x: - 0.05 , y: 0.05 })
});
textTrack . addClip ( triggerTime , textClip );

// Audio cue at same trigger time
if ( triggerTime < videoDuration - 2 ) {
const audioClip = new Clip ({
asset: new EditorAudioAsset ({ id: audio . id }),
duration: 2
});
audioTrack . addClip ( triggerTime , audioClip );
}
});

// Add all tracks to timeline
timeline . addTrack ( videoTrack );
timeline . addTrack ( textTrack );
timeline . addTrack ( audioTrack );
```

### [ Step 7: Generate and Play the Stream](#step-7-generate-and-play-the-stream)

Finally, generate a streaming URL for your edited video and play it.

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

Here's a preview of showing occurrence of the word **Education**

### [ Conclusion](#conclusion)

This tutorial showcases VideoDB's capabilities to create a video that programmatically counts and displays the frequency of a specific keyword spoken throughout the video. This method can be adapted for various applications where dynamic text overlays add significant value to video content.

### [ Tips and Tricks](#tips-and-tricks)

- Use different text styles and positions based on your video's theme.
- Add background sounds or effects to enhance the viewer's experience.

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## Brand Elements

Add logos, watermarks, and graphics

## Audio Overlay

Add background music and sound effects

[Dynamic Streams](\examples-and-tutorials\programmatic-editing\dynamic-streams) [Chess Match Montage Generator](\examples-and-tutorials\programmatic-editing\chess-montage)

⌘ I