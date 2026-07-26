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

- [The Challenge](#the-challenge)
- [What You'll Build](#what-you%E2%80%99ll-build)
- [Setup](#setup)
    - [Install Dependencies](#install-dependencies)
    - [Connect to VideoDB](#connect-to-videodb)
- [Implementation](#implementation)
    - [Step 1: Upload Chess Video and Music](#step-1-upload-chess-video-and-music)
    - [Step 2: Index Scenes with Move Detection](#step-2-index-scenes-with-move-detection)
    - [Step 3: Extract Move Timestamps Using AI](#step-3-extract-move-timestamps-using-ai)
    - [Step 5: Add Video Clips with Transitions](#step-5-add-video-clips-with-transitions)
    - [Step 6: Add Background Music](#step-6-add-background-music)
    - [Step 7: Render Montage](#step-7-render-montage)
- [What You Get](#what-you-get)
- [Perfect For](#perfect-for)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Programmatic Editing](\examples-and-tutorials\programmatic-editing\index)

# Chess Match Montage Generator

Copy page

Automatically create highlight reels from long chess matches with AI-powered move detection

Copy page

Open In Colab

<!-- image -->

## [ The Challenge](#the-challenge)

A chess match can last 4+ hours. As a content creator, you want to turn that into a punchy highlight reel, but manually scrubbing through and identifying key moments is tedious. What if AI could watch the entire match, detect every move, and automatically compile a highlight montage?

## [ What You'll Build](#what-you’ll-build)

Turn a long chess match into a **punchy highlight reel** - automatically! You'll:

1. Upload chess video + background music
2. Index scenes with simple move detection
3. Extract timestamps automatically using AI
4. Build a montage with transitions and effects
5. Output a professional highlight reel

All powered by **VideoDB's Editor SDK** - no manual frame-by-frame editing needed.

## [ Setup](#setup)

### [ Install Dependencies](#install-dependencies)

```
pip install videodb
```

### [ Connect to VideoDB](#connect-to-videodb)

```
import videodb

# Connect to VideoDB
api_key = "your_api_key"
conn = videodb.connect( api_key = api_key)
coll = conn.get_collection()
```

## [ Implementation](#implementation)

### [ Step 1: Upload Chess Video and Music](#step-1-upload-chess-video-and-music)

```
from videodb import MediaType

# Upload the chess match video
chess_video = coll.upload( url = "https://www.youtube.com/watch?v=dhDe-RcoyAU" )

# Upload background music for the montage
bg_music = coll.upload(
url = "https://www.youtube.com/watch?v=S19UcWdOA-I" ,
media_type = MediaType.audio
)
```

### [ Step 2: Index Scenes with Move Detection](#step-2-index-scenes-with-move-detection)

Create a scene index with a **binary prompt** to detect moves:

```
from videodb import SceneExtractionType

moves_index_id = chess_video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 8 , "frame_count" : 5 },
prompt = """Look at this chess scene and focus on the chess board. Your task is to detect when pieces are moved.

Respond with ONLY one of these two keywords:
- "Player Moved" - if a chess piece was moved
- "No Move" - if no move occurred (same position, paused, talking, etc.)

Be strict. Only say "Player Moved" if you clearly see a chess piece moved.""" ,
name = "Chess_Move_Detection"
)

# Get all scenes with descriptions
moves_scenes = chess_video.get_scene_index(moves_index_id)
```

### [ Step 3: Extract Move Timestamps Using AI](#step-3-extract-move-timestamps-using-ai)

Feed the scene index to the LLM to extract timestamps:

```
import json

prompt = f """Analyze the scene descriptions from this chess video.

Find EVERY scene where the description says "Player Moved".

Return a JSON array containing ONLY the start timestamps (in seconds) of those scenes.

Example output format:
[0, 8, 16, 24, 40, 48]

Rules:
- Return ONLY the JSON array, nothing else
- No descriptions, no explanations, just timestamps

Moves Index : " { moves_scenes } "
"""

response = coll.generate_text(
prompt = prompt,
response_type = "json" ,
model_name = "pro"
)

# Parse timestamps from LLM response
timestamps = response[ "output" ]
if isinstance (timestamps, str ):
timestamps = json.loads(timestamps)
```

Initialize timeline and sample moves:

```
from videodb.editor import (
Timeline, Track, Clip, VideoAsset, AudioAsset,
Filter, Transition, TextAsset, Font
)

CLIP_DURATION = 5 # seconds per clip
TARGET_CLIPS = 10 # how many clips we want

# Sample timestamps evenly
total_detected = len (timestamps)
step = max ( 1 , total_detected // TARGET_CLIPS )
sampled_timestamps = timestamps[::step][: TARGET_CLIPS ]

# Initialize timeline
timeline = Timeline(conn)
timeline.background = "#000000"

# Create intro text
intro_text = TextAsset(
text = "Let the Match Begin" ,
font = Font( family = "Clear Sans" , size = 56 , color = "#FFFFFF" ),
)

intro_clip = Clip(
asset = intro_text,
duration = 3 ,
transition = Transition( in_ = "fade" , out = "fade" , duration = 0.5 )
)

intro_track = Track()
intro_track.add_clip( 0 , intro_clip)
timeline.add_track(intro_track)
```

### [ Step 5: Add Video Clips with Transitions](#step-5-add-video-clips-with-transitions)

```
# Add video clips
video_track = Track()
timeline_position = 3

for i, start_time in enumerate (sampled_timestamps):
clip = Clip(
asset = VideoAsset(
id = chess_video.id,
start = start_time - 1 ,
volume = 0 # Muting the original audio
),
duration = CLIP_DURATION ,
filter = Filter.contrast,
transition = Transition( in_ = "fade" , out = "fade" , duration = 1 )
)

video_track.add_clip(timeline_position, clip)
timeline_position += CLIP_DURATION

timeline.add_track(video_track)

total_duration = len (sampled_timestamps) * CLIP_DURATION + 3
```

### [ Step 6: Add Background Music](#step-6-add-background-music)

```
# Add music track
music_clip = Clip(
asset = AudioAsset(
id = bg_music.id,
start = 0 ,
volume = 0.7
),
duration = total_duration
)

audio_track = Track()
audio_track.add_clip( 0 , music_clip)
timeline.add_track(audio_track)
```

### [ Step 7: Render Montage](#step-7-render-montage)

```
# Generate final montage stream
stream_url = timeline.generate_stream()
```

## [ What You Get](#what-you-get)

A professional highlight reel with:

- AI-detected key moves
- Evenly sampled clips for pacing
- Smooth fade transitions
- Enhanced contrast for visual impact
- Background music
- Professional polish in seconds

Here's the final chess montage:

## [ Perfect For](#perfect-for)

- **Tournament Highlights** - Post-tournament recap videos
- **Streamer Clips** - Highlight reels for streaming communities
- **Educational Analysis** - Study videos from master games
- **Social Media** - Short-form clips from longer matches
- **Archive Content** - Transform library of matches into reels

## [ The Result](#the-result)

What took hours of manual editing now takes minutes. Your audience gets punchy, professional highlight reels. You get back your time. No more endless scrubbing. Just AI-powered chess analysis and automatic montages.

## Explore the Full Notebook

Open the complete implementation with advanced filtering, custom transitions, and batch processing.

## [ Related Tutorials](#related-tutorials)

## Intro &amp; Outro

Auto-add opening and closing sequences

## Word Counter

Add analytical text overlays

[Word Counter](\examples-and-tutorials\programmatic-editing\word-counter) [Overview](\examples-and-tutorials\safety-compliance)

⌘ I