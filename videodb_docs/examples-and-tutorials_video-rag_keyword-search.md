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
    - [Step 3: Index Spoken Words](#step-3-index-spoken-words)
    - [Step 4: Search for any keyword](#step-4-search-for-any-keyword)
    - [Step 5: Preview and Share](#step-5-preview-and-share)
    - [Bonus: Refining Keyword Search results by adding padding](#bonus-refining-keyword-search-results-by-adding-padding)
    - [Here's the result for the same video, but improved using padding control.](#here%E2%80%99s-the-result-for-the-same-video-but-improved-using-padding-control)
    - [Conclusion](#conclusion)
- [More Examples](#more-examples)
- [Next Steps](#next-steps)
- [Related Tutorials](#related-tutorials)

[Video Search and Understanding](\examples-and-tutorials\video-rag\index)

# Keyword Search

Copy page

Create custom video compilations by searching for keywords and phrases

Copy page

Open In Colab

<!-- image -->

From an hour long video, want to create a fun compilation of every moment Mark Zuckerberg says 'metaverse'?

## [ Overview](#overview)

In this tutorial, let's explore the powerful functionality of Keyword Search in VideoDB. This feature enables users to efficiently locate any keyword or phrase within their video assets, streamlining the process of content discovery.

Fun keyword search example with Mark Zuckerberg metaverse compilation

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

Before proceeding, ensure access to [VideoDB](https://videodb.io/) Get your API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) . ( Free for first 50 uploads, No credit card required)

## [ Steps](#steps)

### [ Step 1: Connect to VideoDB](#step-1-connect-to-videodb)

Begin by establishing a connection to VideoDB using your API key

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

Upload the video to your VideoDB collection. You can upload the video asset from your local device or from a YouTube URL to upload the video from its source. This works as the base video for all the Keyword Search queries.

Python

Node.js

```
video = coll.upload( url = "https://www.youtube.com/watch?v=Uvufun6xer8" )
video.play()
```

```
const video = await coll . uploadURL ({
url: "https://www.youtube.com/watch?v=Uvufun6xer8"
});
console . log ( video . playerUrl );
```

You can upload from your local file system too by passing `file_path` in `upload()` For this tutorial, we'll run a Keyword Search on the following video:

### [ Step 3: Index Spoken Words](#step-3-index-spoken-words)

Index the spoken words in your video to enable accurate keyword search.

Python

Node.js

```
video.index_spoken_words()
```

```
await video . indexSpokenWords ();
```

### [ Step 4: Search for any keyword](#step-4-search-for-any-keyword)

Utilize the keyword search by using `video.search()` method with following parameters.

- pass search query in `query` parameter
- pass `SearchType.keyword` in `search_type`

Note: You will need to import `SearchType` first to enable this function

Python

Node.js

```
from videodb import SearchType

results = video.search( query = 'metaverse' , search_type = SearchType.keyword)
```

```
import { SearchTypeValues } from 'videodb' ;

const results = await video . search ({
query: 'metaverse' ,
searchType: SearchTypeValues . keyword
});
```

### [ Step 5: Preview and Share](#step-5-preview-and-share)

Preview your video with a compilation of all the clips matching your search query. You can access the stream link alongside the preview to share the Keyword Search result with others.

Python

Node.js

```
results.play()
```

```
console . log ( results . playerUrl );
```

### [ Bonus: Refining Keyword Search results by adding padding](#bonus-refining-keyword-search-results-by-adding-padding)

Some keyword search results/ compilations may appear slightly choppy, or the cuts may feel abrupt. We can solve this issue by using VideoDB's padding controls. Here's how it works: The resulting shots can be made smoother by including a little more context from before and after the matching timestamps. That's exactly what padding controls enable: Using the Editor SDK's `Track` and `Clip` pattern, we can create a timeline with padding:

1. Create a timeline and track using `Timeline()` and `Track()`
2. Create a `VideoAsset` with `id` and `start` parameters (where `start` is adjusted by subtracting padding)
3. Wrap each asset in a `Clip` with the appropriate duration (adding padding on both ends)
4. Add clips to the track sequentially using `track.add_clip(start_time, clip)`

Python

Node.js

```
from videodb import play_stream
from videodb.editor import Timeline, Track, Clip, VideoAsset

timeline = Timeline(conn)

# Add padding for smoother cuts
padding = 0.4

# Create main track
track = Track()
seeker = 0

# Compile Video from search results
for shot in results.shots:
start_with_padding = max ( 0 , shot.start - padding)
duration = (shot.end + padding) - start_with_padding

asset = VideoAsset( id = shot.video_id, start = start_with_padding)
clip = Clip( asset = asset, duration = duration)
track.add_clip(seeker, clip)

seeker += duration

timeline.add_track(track)

stream_url = timeline.generate_stream()
play_stream(stream_url)
```

```
import { EditorTimeline , Track , Clip , EditorVideoAsset } from 'videodb' ;

const timeline = new EditorTimeline ( conn );

// Add padding for smoother cuts
const padding = 0.4 ;

// Create main track
const track = new Track ();
let seeker = 0 ;

// Compile Video from search results
for ( const shot of results . shots ) {
const startWithPadding = Math . max ( 0 , shot . start - padding );
const duration = ( shot . end + padding ) - startWithPadding ;

const asset = new EditorVideoAsset ({
id: shot . videoId ,
start: startWithPadding
});
const clip = new Clip ({ asset , duration });
track . addClip ( seeker , clip );

seeker += duration ;
}

timeline . addTrack ( track );

const streamUrl = await timeline . generateStream ();
console . log ( streamUrl );
```

### [ Here's the result for the same video, but improved using padding control.](#here’s-the-result-for-the-same-video-but-improved-using-padding-control)

### [ Conclusion](#conclusion)

Keyword Search in VideoDB empowers users to extract valuable insights from their video assets with ease.

## [ More Examples](#more-examples)

Checkout these fun experiments with Keyword search 👇

1. So basically it's "basically"

2. The untold story of "generative" AI

## [ Next Steps](#next-steps)

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## Multimodal Search

Combine spoken word and visual search for comprehensive queries

## Character Extraction

Extract clips featuring specific characters or people instantly

[Overview](\examples-and-tutorials\video-rag) [Character Extraction](\examples-and-tutorials\video-rag\character-clips)

⌘ I