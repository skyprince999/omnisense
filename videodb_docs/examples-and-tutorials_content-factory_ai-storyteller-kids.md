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
- [Setup](#setup)
    - [Install Dependencies](#install-dependencies)
    - [Connect to VideoDB](#connect-to-videodb)
- [Implementation](#implementation)
    - [Step 1: Generate Script and Title](#step-1-generate-script-and-title)
    - [Step 2: Generate Background Prompts](#step-2-generate-background-prompts)
    - [Step 3: Generate All Assets](#step-3-generate-all-assets)
    - [Step 4: Generate Word-Level Transcript](#step-4-generate-word-level-transcript)
    - [Step 5: Generate Custom Captions File](#step-5-generate-custom-captions-file)
    - [Step 6: Build Multi-Layer Timeline](#step-6-build-multi-layer-timeline)
    - [Step 7: Add Outro Card](#step-7-add-outro-card)
    - [Step 8: Render Final Video](#step-8-render-final-video)
- [What You Get](#what-you-get)
- [Perfect For](#perfect-for)
- [What Topics Can You Cover?](#what-topics-can-you-cover)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Content Factory](\examples-and-tutorials\content-factory\index)

# AI Storyteller for Kids

Copy page

Generate complete animated educational videos for kids with AI scripts, voiceovers, and captions

Copy page

Open In Colab

<!-- image -->

## [ The Idea](#the-idea)

Ever wished you could create fun, educational videos for kids with just a single topic? Tell the system "explain the solar system" and get back a complete animated video with:

- Kid-friendly voiceover narration
- Fun background music
- Loopable animated backgrounds
- Timed subject videos (cartoons of planets, stars, etc.)
- Animated captions that kids can follow along

This workflow takes a topic and magically transforms it into a complete learning video. All powered by **VideoDB's Editor SDK** - pure automation magic.

## [ Setup](#setup)

### [ Install Dependencies](#install-dependencies)

```
pip install videodb
```

### [ Connect to VideoDB](#connect-to-videodb)

```
import os
import math
import videodb

# Connect to VideoDB
api_key = "your_api_key"
conn = videodb.connect( api_key = api_key)
coll = conn.get_collection()
```

## [ Implementation](#implementation)

### [ Step 1: Generate Script and Title](#step-1-generate-script-and-title)

```
import json

# Define the learning topic
topic = "Explain the solar system"

script_prompt = f """You are a friendly children's educational content writer.

Write a fun, simple explanation about: " { topic } "

Requirements:
- Target audience: 5-year-old children
- Length: 250 words
- Use simple words and short sentences
- Make it fun and engaging

Return a JSON with:
- "title": A fun, catchy title for the video (max 5 words)
- "script": The complete narration script

Example format:
{{ "title": "The Amazing Sun!", "script": "Hey friends! Today we're going to learn about..." }}
"""

script_response = coll.generate_text(
prompt = script_prompt,
model_name = "pro" ,
response_type = "json"
)

# Handle nested output structure
if 'output' in script_response and isinstance (script_response[ 'output' ], dict ):
video_title = script_response[ "output" ][ "title" ]
video_script = script_response[ "output" ][ "script" ]
else :
video_title = script_response[ "title" ]
video_script = script_response[ "script" ]
```

### [ Step 2: Generate Background Prompts](#step-2-generate-background-prompts)

```
bg_prompt = f """Based on this children's educational video topic: " { topic } "

Create prompts for background media.

Return JSON with:
- "background_video_prompt": Detailed prompt for generating background video
- "music_prompt": Prompt for generating background music

Example: {{ "background_video_prompt": "...", "music_prompt": "..." }}
"""

bg_response = coll.generate_text(
prompt = bg_prompt,
model_name = "pro" ,
response_type = "json"
)

# Handle nested output structure
if isinstance (bg_response, dict ) and "output" in bg_response:
background_video_prompt = bg_response[ "output" ][ "background_video_prompt" ]
music_prompt = bg_response[ "output" ][ "music_prompt" ]
else :
background_video_prompt = bg_response[ "background_video_prompt" ]
music_prompt = bg_response[ "music_prompt" ]
```

### [ Step 3: Generate All Assets](#step-3-generate-all-assets)

```
# Generate voiceover from script
voiceover = coll.generate_voice(
text = video_script,
voice_name = "Default"
)

# Generate background music (loopable)
bg_music = coll.generate_music(
prompt = music_prompt,
duration = 10
)

# Generate background video (loopable)
bg_video = coll.generate_video(
prompt = background_video_prompt,
duration = 5
)
```

### [ Step 4: Generate Word-Level Transcript](#step-4-generate-word-level-transcript)

```
# Generate and fetch timestamped transcript
voiceover.generate_transcript()
transcript = voiceover.get_transcript()
```

### [ Step 5: Generate Custom Captions File](#step-5-generate-custom-captions-file)

```
# Create ASS (Advanced SubStation Alpha) captions with styling
def create_ass_captions ( transcript , voiceover_duration ):
ass_header = """[Script Info]
Title: Kids Educational Video
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour
Style: Default,Arial,48,&H00FFFF00,&H000000FF,&H00000000,&H00000000

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
events = []

for word_info in transcript:
start_ms = int (word_info[ "start" ] * 100 ) # Convert to centiseconds
end_ms = int (word_info[ "end" ] * 100 )
word = word_info[ "text" ]

# Format: Hh:Mm:Ss.Cc
start_time = f "0: { start_ms // 6000 :02d} : { (start_ms % 6000 ) // 100 :02d} . { start_ms % 100 :02d} "
end_time = f "0: { end_ms // 6000 :02d} : { (end_ms % 6000 ) // 100 :02d} . { end_ms % 100 :02d} "

event = f "Dialogue: 0, { start_time } , { end_time } ,Default,,0,0,0,, {{\\ c&HFF00FF& }} { word } "
events.append(event)

return ass_header + " \n " .join(events)

ass_captions = create_ass_captions(transcript, voiceover.length)
```

### [ Step 6: Build Multi-Layer Timeline](#step-6-build-multi-layer-timeline)

```
from videodb.editor import (
Timeline, Track, Clip, VideoAsset, AudioAsset, TextAsset,
Font, Background, Alignment, HorizontalAlignment, VerticalAlignment
)

# Create timeline
timeline = Timeline(conn)

# Intro title card (5 seconds)
intro_track = Track()
intro_text = TextAsset(
text = video_title,
font = Font( size = 56 , color = "#FFFFFF" ),
background = Background( color = "rgba(100, 50, 200, 0.8)" ),
alignment = Alignment( horizontal = HorizontalAlignment.center, vertical = VerticalAlignment.center)
)
intro_track.add_clip( 0 , Clip( asset = intro_text, duration = 5 ))
timeline.add_track(intro_track)

# Background video track (looped)
bg_track = Track()
bg_asset = VideoAsset( id = bg_video.id, start = 0 )
bg_clip = Clip(
asset = bg_asset,
duration = float (voiceover.length),
opacity = 0.7 ,
scale = 1.1 # Slight zoom for visual interest
)
bg_track.add_clip( 5 , bg_clip) # Start after intro
timeline.add_track(bg_track)

# Voiceover track
voice_track = Track()
voice_asset = AudioAsset( id = voiceover.id)
voice_clip = Clip( asset = voice_asset, duration = float (voiceover.length), volume = 1.0 )
voice_track.add_clip( 5 , voice_clip)
timeline.add_track(voice_track)

# Background music track (looped)
music_track = Track()
music_asset = AudioAsset( id = bg_music.id)
music_clip = Clip(
asset = music_asset,
duration = float (voiceover.length),
volume = 0.3 # Low volume - voiceover is primary
)
music_track.add_clip( 5 , music_clip)
timeline.add_track(music_track)

# Captions track (rendered as overlay)
caption_track = Track()
# Apply ASS captions to timeline
# (Implementation depends on VideoDB's caption support)
```

### [ Step 7: Add Outro Card](#step-7-add-outro-card)

```
# Outro "Happy Learning!" card (5 seconds)
# Calculate outro start time (after intro + voiceover)
outro_start = 5 + float (voiceover.length)

outro_track = Track()
outro_text = TextAsset(
text = "Happy Learning! 🎉" ,
font = Font( size = 52 , color = "#FFFFFF" ),
background = Background( color = "rgba(50, 200, 100, 0.8)" ),
alignment = Alignment( horizontal = HorizontalAlignment.center, vertical = VerticalAlignment.center)
)
outro_track.add_clip(outro_start, Clip( asset = outro_text, duration = 5 ))
timeline.add_track(outro_track)
```

### [ Step 8: Render Final Video](#step-8-render-final-video)

```
# Generate the complete educational video
stream_url = timeline.generate_stream()

# Calculate total duration
total_duration = 5 + float (voiceover.length) + 5 # intro + voiceover + outro

print ( f "Video created successfully!" )
print ( f "Title: { video_title } " )
print ( f "Duration: { total_duration } seconds" )
print ( f "Stream: { stream_url } " )
```

## [ What You Get](#what-you-get)

A complete 70-80 second educational video with:

- Kid-friendly AI-written script
- Natural voiceover narration (kids' voice)
- Loopable animated background
- Timed subject videos (cartoon illustrations)
- Synchronized animated captions
- Upbeat background music
- Professional intro and outro cards

Here's the final educational video:

## [ Perfect For](#perfect-for)

- **Home Learning** - Parents teaching kids at home
- **Educational Channels** - YouTube Kids content creators
- **School Supplements** - Teachers augmenting classroom lessons
- **Language Learning** - Kids' language learning videos
- **Skill Development** - Tutorial videos for children

## [ What Topics Can You Cover?](#what-topics-can-you-cover)

- The Solar System
- Ocean Animals
- Ancient Civilizations
- How Photosynthesis Works
- The Water Cycle
- Math Basics
- History Stories
- Science Experiments
- Geography
- And anything else!

## [ The Result](#the-result)

What used to take weeks of scriptwriting, voiceover recording, animation, and editing now takes minutes. Teachers and parents can create engaging, professional educational content instantly. Kids get to learn with animated characters, fun music, and engaging visuals. Everyone wins. **Pure learning magic - powered by VideoDB.**

## Explore the Full Notebook

Open the complete implementation with advanced subject video generation, caption styling, and content customization.

## [ Related Tutorials](#related-tutorials)

## Faceless Video Creator

Generate complete videos from scripts

## Text-to-Video

Create video directly from text prompts

[Text to Video](\examples-and-tutorials\content-factory\text-prompts) [Annual Video Statistics Recap](\examples-and-tutorials\content-factory\year-in-frames)

⌘ I