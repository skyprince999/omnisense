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

- [The Idea](#the-idea)
- [What You'll Build](#what-you%E2%80%99ll-build)
- [Setup](#setup)
    - [Install Dependencies](#install-dependencies)
    - [Connect to VideoDB](#connect-to-videodb)
- [Implementation](#implementation)
    - [Step 1: Calculate Your Video Metrics](#step-1-calculate-your-video-metrics)
    - [Step 2: Upload Background Music](#step-2-upload-background-music)
    - [Step 3: Create Timeline with 5 Sections](#step-3-create-timeline-with-5-sections)
    - [Step 4: Build Intro Section (0-5s)](#step-4-build-intro-section-0-5s)
    - [Step 5: Build Upload Metrics Section (6-13s)](#step-5-build-upload-metrics-section-6-13s)
    - [Step 6: Build Search Analytics Section (13-19s)](#step-6-build-search-analytics-section-13-19s)
    - [Step 7: Build Automation Stats Section (19-25s)](#step-7-build-automation-stats-section-19-25s)
    - [Step 8: Build Intelligence Metrics Section (25-31s)](#step-8-build-intelligence-metrics-section-25-31s)
    - [Step 9: Add Outro and Render](#step-9-add-outro-and-render)
- [What You Get](#what-you-get)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Content Factory](\examples-and-tutorials\content-factory\index)

# Annual Video Statistics Recap

Copy page

Transform video analytics into a cinematic recap video with AI-powered visualizations

Copy page

Open In Colab

<!-- image -->

## [ The Idea](#the-idea)

You've uploaded hundreds of videos this year. You've run thousands of searches. Your automation has processed countless scenes. But how do you celebrate and share those numbers in a way that actually captivates people? Traditional dashboards and spreadsheets are boring. What if you could transform your video analytics into a shareable cinematic recap video?

## [ What You'll Build](#what-you’ll-build)

Turn your video analytics into a shareable recap video. This system creates a cinematic journey through your video stats:

- Total minutes uploaded with growth metrics
- Search activity visualization
- Clips generated via automation
- Scenes and frames analyzed
- All set to music with dynamic video grids and text overlays

All powered by **VideoDB's Editor SDK** - turning data into a visual story through code.

## [ Setup](#setup)

### [ Install Dependencies](#install-dependencies)

```
pip install videodb
```

### [ Connect to VideoDB](#connect-to-videodb)

```
import json
import random
import videodb
from videodb import MediaType, play_stream

# Connect to VideoDB
api_key = "your_api_key"
conn = videodb.connect( api_key = api_key)
coll = conn.get_collection()
```

## [ Implementation](#implementation)

### [ Step 1: Calculate Your Video Metrics](#step-1-calculate-your-video-metrics)

```
# Get all videos from your collection
videos = coll.get_videos()

TOTAL_SECONDS = 0
for v in videos:
TOTAL_SECONDS += v.length

# Core metrics
TOTAL_MINUTES = round ( TOTAL_SECONDS / 60 , 1 )
TOTAL_SEARCHES = 2573
CLIPS_GENERATED = 574
SCENES_ANALYZED = 248
FRAMES_ANALYZED = 3200

# Previous year comparison
PREV_YEAR_MINUTES = 6400

# Time conversions
TOTAL_HOURS = round ( TOTAL_MINUTES / 60 , 1 )
TOTAL_DAYS = round ( TOTAL_HOURS / 24 , 1 )

# Growth percentage
MINUTES_GROWTH = round ((( TOTAL_MINUTES - PREV_YEAR_MINUTES ) / PREV_YEAR_MINUTES ) * 100 )
```

### [ Step 2: Upload Background Music](#step-2-upload-background-music)

```
# Upload background music as audio
audio = coll.upload( "https://youtu.be/vIEi8AoP_Fw?si=AUVUt6Komqtt7rWI" , media_type = "audio" )
```

### [ Step 3: Create Timeline with 5 Sections](#step-3-create-timeline-with-5-sections)

Initialize the timeline and set up base configuration:

```
from videodb.editor import (
Timeline, Track, Clip, VideoAsset, AudioAsset, TextAsset,
Offset, Transition, Font, Filter,
)

# Use subset of videos
videos = videos[ 20 : 40 ]

# Create timeline
timeline = Timeline(conn)
timeline.background = "#E85E00"
track = Track()
video_track = Track()

# Add background music
b_music = Clip(
asset = AudioAsset( id = audio.id, start = 0 , volume = 1 ),
duration = 28 ,
)
track.add_clip( 4 , b_music)
```

### [ Step 4: Build Intro Section (0-5s)](#step-4-build-intro-section-0-5s)

Create a dynamic mosaic effect with 60 video clips:

```
# Intro text
intro_text = Clip(
asset = TextAsset(
text = "2025 was a blur. Let's index it." ,
font = Font( size = 60 , family = "Roboto Bold" ),
),
duration = 5 ,
transition = Transition( in_ = "fade" ),
)
track.add_clip( 1 , intro_text)

# Create 60 video clips with varying scales and random positioning
for i in range ( 60 ):
scale_value = 0.5 + (i * 0.025 ) # Scale: 0.5 to 0.975
start_time = random.randint( 0 , 4 )
volume = 0.5
if start_time == 3 :
volume = 0.3
elif start_time == 4 :
volume = 0.3

video = random.choice(videos)

video_clip = Clip(
asset = VideoAsset(
id = video.id,
start = random.randint( 10 , int (video.length - 10 )),
volume = volume,
),
duration = 1 ,
scale = scale_value,
fit = None ,
offset = Offset( x = random.uniform( - 0.5 , 0.5 ), y = random.uniform( - 0.5 , 0.5 )),
)

video_track.add_clip( start = start_time, clip = video_clip)
```

### [ Step 5: Build Upload Metrics Section (6-13s)](#step-5-build-upload-metrics-section-6-13s)

Display total minutes uploaded with zoom-out effect:

```
# Section 1 text
section1_text = Clip(
asset = TextAsset(
text = f "You uploaded { TOTAL_MINUTES :,} minutes \n of video content. \n\n That's { TOTAL_HOURS } hours. \n Or { TOTAL_DAYS } full days of footage. \n\n ↑ { MINUTES_GROWTH } % from 2024" ,
font = Font( size = 48 , family = "default" ),
),
duration = 7 ,
)
track.add_clip( 6 , section1_text)

# Zoom out effect with greyscale filter
for i in range ( 20 ):
scale_value = 0.5 + (i * 0.0263 ) # Scale: 0.5 to 1.0
start_time = 6 + (i * 0.175 )

video = random.choice(videos)
video_start = random.randint( 10 , max ( 11 , int (video.length - 10 )))

video_clip = Clip(
asset = VideoAsset(
id = video.id,
start = video_start,
volume = 0.15 ,
),
duration = 1 ,
scale = scale_value,
fit = "crop" ,
filter = Filter.greyscale,
)

video_track.add_clip( start = start_time, clip = video_clip)
```

### [ Step 6: Build Search Analytics Section (13-19s)](#step-6-build-search-analytics-section-13-19s)

Create 3 rows of horizontal scanning video clips:

```
# Section 2 text
section2_text = Clip(
asset = TextAsset(
text = f " { TOTAL_SEARCHES :,} questions asked. \n\n Your videos aren't just stored- \n they're understood." ,
font = Font( size = 58 , family = "default" ),
),
duration = 6 ,
)
track.add_clip( 13 , section2_text)

# Create horizontal scanning effect with 3 rows
rows = [
{ "y" : - 0.5 , "num_clips" : 20 , "duration" : 0.25 , "scale" : 0.35 }, # Top row
{ "y" : 0 , "num_clips" : 15 , "duration" : 0.33 , "scale" : 0.45 }, # Middle row
{ "y" : 0.5 , "num_clips" : 12 , "duration" : 0.42 , "scale" : 0.35 }, # Bottom row
]

clip_idx = 0
for row in rows:
for i in range (row[ "num_clips" ]):
x_pos = - 0.9 + (i * 0.1 )
video = videos[clip_idx % len (videos)]

video_start = 30 + (clip_idx % 10 )
if video_start > video.length - 10 :
video_start = 15

video_clip = Clip(
asset = VideoAsset(
id = video.id,
start = video_start,
volume = 0.15 ,
),
duration = row[ "duration" ],
scale = row[ "scale" ],
fit = "crop" ,
offset = Offset( x = x_pos, y = row[ "y" ]),
)
video_track.add_clip( start = 12 + (i * row[ "duration" ]), clip = video_clip)
clip_idx += 1
```

### [ Step 7: Build Automation Stats Section (19-25s)](#step-7-build-automation-stats-section-19-25s)

Large background clips with cycling effect:

```
# Section 3 text
section3_text = Clip(
asset = TextAsset(
text = f " { CLIPS_GENERATED :,} clips \n generated via code. \n\n Automation at its finest." ,
font = Font( size = 62 , family = "default" ),
),
duration = 6 ,
)
track.add_clip( 19 , section3_text)

# Cycling background effect
for i in range ( 3 ):
video = videos[(i + 5 ) % len (videos)]
video_start = 20 + (i * 15 )
if video_start > video.length - 10 :
video_start = 10

bg_clip = Clip(
asset = VideoAsset(
id = video.id,
start = video_start,
volume = 0.05 ,
),
duration = 2 ,
scale = 1.2 ,
fit = "crop" ,
filter = Filter.greyscale,
opacity = 0.2 ,
z_index = 0 ,
)
video_track.add_clip( start = 19 + (i * 2 ), clip = bg_clip)
```

### [ Step 8: Build Intelligence Metrics Section (25-31s)](#step-8-build-intelligence-metrics-section-25-31s)

3x3 grid with scanning animation:

```
# Section 4 text
section4_text = Clip(
asset = TextAsset(
text = f " { SCENES_ANALYZED :,} scenes analyzed \n { FRAMES_ANALYZED :,} Frames Analyzed \n\n Pure video intelligence. \n Powered by you." ,
font = Font( size = 52 , color = "#FFFFFF" , family = "Arial Bold" ),
),
duration = 5 ,
)
track.add_clip( 25 , section4_text)

# 3x3 grid with scanning effect
grid_positions = [
( - 0.4 , - 0.4 ), ( 0 , - 0.4 ), ( 0.4 , - 0.4 ), # Top row
( - 0.4 , 0 ), ( 0 , 0 ), ( 0.4 , 0 ), # Middle row
( - 0.4 , 0.4 ), ( 0 , 0.4 ), ( 0.4 , 0.4 ), # Bottom row
]

for idx, (x_pos, y_pos) in enumerate (grid_positions):
video = videos[idx % len (videos)]

video_start = 50 + (idx % 10 )
if video_start > video.length - 10 :
video_start = 20

video_clip = Clip(
asset = VideoAsset(
id = video.id,
start = video_start,
volume = 0.1 ,
),
duration = 0.6 ,
scale = 0.28 ,
fit = "crop" ,
offset = Offset( x = x_pos, y = y_pos),
transition = Transition( in_ = "fade" , duration = 0.15 ),
filter = Filter.contrast if idx % 2 == 0 else Filter.boost,
opacity = 0.9 ,
)

video_track.add_clip( start = 24.5 + (idx * 0.08 ), clip = video_clip)

# Add cascading columns
num_columns = 2
clips_per_column = 8
for col in range (num_columns):
x_pos = - 0.3 + (col * 0.6 )

for row in range (clips_per_column):
y_pos = - 0.7 + (row * 0.23 )
clip_idx = col * clips_per_column + row

video = videos[clip_idx % len (videos)]

video_start = 40 + (clip_idx % 8 )
if video_start > video.length - 10 :
video_start = 25

video_clip = Clip(
asset = VideoAsset(
id = video.id,
start = video_start,
volume = 0.15 ,
),
duration = 0.3 ,
scale = 0.3 ,
fit = "crop" ,
offset = Offset( x = x_pos, y = y_pos),
)
video_track.add_clip( start = 25.7 + (row * 0.3 ) + (col * 0.1 ), clip = video_clip)
```

### [ Step 9: Add Outro and Render](#step-9-add-outro-and-render)

```
# Outro text
outro_text = Clip(
asset = TextAsset(
text = "Ready for 2026? Build it." ,
font = Font( size = 60 , family = "Roboto Bold" )
),
duration = 2 ,
)
track.add_clip( 31 , outro_text)

# Add tracks to timeline
timeline.add_track(video_track)
timeline.add_track(track)

# Generate stream
stream_url = timeline.generate_stream()
```

## [ What You Get](#what-you-get)

A professional video that:

- Visualizes your video metrics in real-time
- Uses 100+ of your actual videos in the composition
- Creates dynamic animations and transitions
- Pairs everything with music
- Tells the story of your year in video data

Perfect for:

- Marketing your platform
- Celebrating milestones with users
- Annual reports
- Social media recap posts
- Team celebrations

Here's the final rendered recap video:

## [ The Result](#the-result)

With this system, you transform dry analytics into engaging visual stories. Your users see not just numbers, but a cinematic journey through what you've accomplished together. It's data visualization meets creative storytelling - all powered by code.

## Explore the Full Notebook

Open the complete implementation with procedural animation logic, timing calculations, and advanced effects.

## [ Related Tutorials](#related-tutorials)

## Faceless Video Creator

Generate complete videos from scripts

## TikTok Lyric Videos

Auto-sync lyrics to music with animations

[AI Storyteller for Kids](\examples-and-tutorials\content-factory\ai-storyteller-kids) [PromptClip](\pages\community\open-source\promptclip)

⌘ I