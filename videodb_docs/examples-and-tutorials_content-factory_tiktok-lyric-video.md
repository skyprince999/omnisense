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
    - [Step 1: Upload Your Music Video](#step-1-upload-your-music-video)
    - [Step 2: Generate Transcript with Word-Level Timestamps](#step-2-generate-transcript-with-word-level-timestamps)
    - [Step 3: Identify the Best Segment](#step-3-identify-the-best-segment)
    - [Step 4: Generate Vertical Background Images with AI](#step-4-generate-vertical-background-images-with-ai)
    - [Step 5: Build Multi-Layer Timeline](#step-5-build-multi-layer-timeline)
- [What You Get](#what-you-get)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Content Factory](\examples-and-tutorials\content-factory\index)

# TikTok Style Lyric Video Creator

Copy page

Transform full-length music videos into viral 15-60 second clips with AI-generated backgrounds and synced lyrics

Copy page

Open In Colab

<!-- image -->

## [ The Challenge](#the-challenge)

You have a beautiful music video, but it's 4 minutes long. Social media demands are different - TikTok, Reels, and Shorts want 15-60 second vertical clips that stop people mid-scroll. Manually identifying the best segment, extracting it, generating backgrounds, adding lyrics, and exporting for vertical format is tedious and time-consuming. What if AI could do all of that for you?

## [ What You'll Build](#what-you’ll-build)

Turn any music video into viral-ready vertical clips optimized for social media. This system automates the complete workflow:

- AI identifies the catchiest segments (chorus with build-up)
- Generates vertical 9:16 backgrounds for mobile viewing
- Creates mobile-optimized captions with high contrast
- Adds pre-roll, CTA, and post-roll for professional polish
- Outputs 15-60 second clips ready to upload

All powered by **VideoDB's Editor SDK** - built for social media from the ground up.

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

### [ Step 1: Upload Your Music Video](#step-1-upload-your-music-video)

```
# Upload from URL
video = coll.upload( url = "https://www.youtube.com/watch?v=gtnD0eCcCC8" )
```

### [ Step 2: Generate Transcript with Word-Level Timestamps](#step-2-generate-transcript-with-word-level-timestamps)

```
# Generate transcript
transcript = video.generate_transcript( force = True )

# Retrieve timed transcript (word-level timestamps)
transcript_timed = video.get_transcript()

# Retrieve plain text transcript
transcript_text = video.get_transcript_text()
```

### [ Step 3: Identify the Best Segment](#step-3-identify-the-best-segment)

The AI analyzes the transcript to find the catchiest chorus with proper build-up and wind-down:

```
import json

# Define visual aesthetic
user_request = "Calm and serene vibe. Ocean, beach, sunsets and peace"

prompt = f """
You are a viral social media content strategist specializing in short-form vertical video. Your task is to identify the most engaging, catchy, and shareable segments from a music video to create TikTok/Reels/Shorts content.

# INPUT DATA

1. Full Transcript Text (may contain ASR errors/missing punctuation):
{ transcript_text }

2. Word-Level Timed Transcript (JSON array with start/end/text/speaker fields):
{ json.dumps(transcript_timed, ensure_ascii = False ) }

3. Video Metadata:
- Name: { video.name }
- Duration: { video.length } seconds
- User Style Request: { user_request }

# SEGMENT SELECTION CRITERIA

Identify **1-3 high-quality segments** (prioritize quality over quantity). Each segment should:

## What Makes a Segment "Catchy"?

**PRIMARY FOCUS: Chorus/Hook with Proper Framing**

Segments MUST be built around the chorus with these components:
1. **Build-up (Pre-Chorus/Verse End)**: 2-4 lines leading into the chorus that create anticipation
2. **The Chorus/Hook**: The main catchy, repetitive, memorable section
3. **Wind-down (Post-Chorus)**: 2-4 lines after the chorus that provide resolution

The segment structure should be: **Ramp Up → Peak (Chorus) → Ramp Down**

Additional qualities that enhance a chorus segment:
- **Emotional Peak**: Most intense, emotionally charged moment (climax, drop, powerful vocals)
- **Quotable Lines**: Lyrics that are relatable, funny, profound, or highly shareable
- **Viral Potential**: Lyrics that could inspire trends, dances, duets, or memes
- **Energy Shift**: Dramatic beat drop, tempo change, or dynamic transition in/around the chorus
- **Memorable Moment**: Distinctive vocal run, ad-lib, or production element that makes the chorus special

**Non-Negotiable Rules:**
- The chorus is the centerpiece - always include it
- Never start directly on the first chorus line - include the approach
- Never end directly after the last chorus line - include the exit
- Build-up and wind-down are MANDATORY for professional feel

## Segment Requirements
- **Duration**: 15-60 seconds per segment (optimal: 20-45 seconds for retention)
- **Focus on Chorus**: Segments should CENTER around the chorus/hook - this is the primary target
- **Build-up REQUIRED**: MUST include the build-up/lead-in before the chorus (last 2-4 lines of pre-chorus or verse)
- **Wind-down REQUIRED**: MUST include the wind-down/resolution after the chorus (first 2-4 lines after chorus ends)
- **No Abrupt Starts**: Never start directly on the main chorus line - include runway space before it
- **No Abrupt Ends**: Never cut immediately when the chorus ends - include graceful exit
- **Ramp Up & Ramp Down**: The segment should feel like a complete emotional arc with natural entry and exit
- **Completeness**: Each segment should feel like a complete mini-story with beginning, climax (chorus), and resolution
- **Standalone Quality**: Segment must work independently and feel professionally edited, not chopped
- **Quality Over Quantity**: If only 1 truly excellent segment exists, return only that one

## Lyric Processing

### Text Handling
- Lightly fix obvious ASR errors ONLY when strongly implied by context
- Do NOT invent new lyrics beyond what is clearly present
- Merge words into natural phrases suitable for vertical video display
- Target 3-8 words per line (shorter than full videos due to vertical format)
- Split long lines for mobile readability

### Timing
- Each stanza's start = earliest word start time
- Each stanza's end = latest word end time
- Each line must have precise start/end timestamps from word-level data
- Ensure NO time gaps within a segment

### Speaker Handling
- Preserve speaker labels
- If stanza mixes speakers, set speaker="Mixed"
- Assign consistent hex colors per speaker

# IMAGE GENERATION REQUIREMENTS

For EACH stanza within EACH segment, create an "image_prompt" following these rules:

## Short-Form Specific Considerations
- **Vertical aspect ratio**: 9:16 (portrait orientation for mobile)
- **Mobile-first design**: Images should look compelling on small phone screens
- **Attention-grabbing**: Short-form content needs more visual impact than full videos
- **Text readability**: Even more critical in vertical format with limited screen space

## Independence & Self-Containment
- Each prompt must be FULLY SELF-CONTAINED with complete scene descriptions
- NEVER use references like "previous image", "same as before", "similar to", or "continue from"
- Each prompt must work standalone if generated in isolation

## Content & Style
- Honor the user's style request: { user_request }
- Reflect the mood, theme, and emotional tone of the current stanza
- Create visual progression within each segment
- **CRITICAL**: Prompts must NEVER include text, lyrics, words, letters, names, or any written language in the generated image

## Composition for Vertical Video Text Overlay
- **Vertical framing**: Design for 9:16 portrait orientation
- Keep **center vertical strip** relatively clear for text overlay
- Text typically appears in middle-to-upper-middle area on mobile
- Avoid busy details in the central vertical zone
- Can have more detail at top/bottom edges where text is less likely
- Use balanced, mobile-optimized compositions
- Images should be visually striking but NOT overly distracting

## Visual Consistency Within Each Segment
Each segment should have internal visual consistency:
- **Color palette**: Harmonious colors within the segment
- **Artistic style**: Consistent style throughout the segment
- **Mood/atmosphere**: Unified emotional tone
- **Composition approach**: Similar framing strategy

## Prompt Structure
Each image_prompt should specify:
1. Scene/subject matter relevant to the stanza
2. Emotional mood and atmosphere matching the segment's energy
3. Lighting conditions and color tone
4. Artistic style (aligned with user_request)
5. **Vertical composition notes** (e.g., "portrait orientation, centered vertical negative space, detailed top and bottom thirds")
6. Mobile-optimized visual impact

# FONT COLOR SELECTION

For EACH stanza, select a "font_color" ensuring optimal mobile readability:

## Available Colors
Choose from this list ONLY:
- White: #FFFFFF (for dark backgrounds)
- Black: #000000 (for light backgrounds)
- Yellow: #FFFF00 (for dark backgrounds, extremely high visibility on mobile)
- Dark Blue: #00008B (for light backgrounds)
- Dark Green: #006400 (for light backgrounds)

## Selection Guidelines
- **Light/bright backgrounds** → Black (#000000), Dark Blue (#00008B), or Dark Green (#006400)
- **Dark/dim backgrounds** → White (#FFFFFF) or Yellow (#FFFF00)
- **Mobile priority**: Ensure MAXIMUM CONTRAST for small screen readability
- Consider that users often view in bright outdoor lighting or dim rooms
- Yellow (#FFFF00) works exceptionally well for high-energy viral content on dark backgrounds

# SEGMENT METADATA

For each segment, provide:

## segment_title
- A catchy, descriptive title for the segment (3-6 words)
- Should hint at what makes this segment special
- Examples: "Explosive Chorus Drop", "Emotional Bridge Moment", "Viral Hook Section"

## start_time & end_time
- Precise timestamps from the original full music video
- These will be used to extract the video segment

# OUTPUT FORMAT

Return ONLY a valid JSON array with this exact structure:

[
{{
"segment_title": "string (catchy 3-6 word title)",
"start_time": float (seconds from original video start),
"end_time": float (seconds from original video start),
"duration": float (end_time - start_time, for verification),
"why_catchy": "string (1-2 sentence explanation of what makes this segment viral-worthy)",
"stanzas": [
{{
"stanza_start": float,
"stanza_end": float,
"image_prompt": "string (detailed, self-contained, vertical 9:16 image generation prompt)",
"font_color": "string (hex code from approved list)",
"lines": [
{{
"text": "string (lyric line)",
"start": float,
"end": float
}}
]
}}
]
}}
]

# CRITICAL REMINDERS

1. **CHORUS-CENTERED STRUCTURE**: Every segment must be built around a chorus with proper build-up and wind-down
2. **NO ABRUPT STARTS**: Always include 2-4 lines BEFORE the chorus begins (pre-chorus/verse ending)
3. **NO ABRUPT ENDS**: Always include 2-4 lines AFTER the chorus ends (post-chorus beginning)
4. **PROFESSIONAL RAMP UP/DOWN**: The segment should feel like a complete emotional journey, not a choppy cut
5. **Quality over quantity**: 1 amazing segment > 3 mediocre ones
6. **Each image_prompt is independent**: No cross-references between prompts
7. **Vertical format**: All image prompts must specify 9:16 portrait orientation
8. **No text in images**: Never include lyrics, words, or letters in image generation prompts
9. **Complete coverage**: No time gaps within each segment
10. **Mobile-first**: Optimize everything for small screen viewing
11. **Honor style request**: All creative decisions must align with: { user_request }
12. Each text line cannot exceed beyond 20 characters [ Highly Important ]

Output the JSON array only, no additional text.
"""

stanzas = coll.generate_text(
prompt = prompt,
model_name = "pro" ,
response_type = "json" ,
)

segments = stanzas.get( "output" )
```

### [ Step 4: Generate Vertical Background Images with AI](#step-4-generate-vertical-background-images-with-ai)

Create AI-generated background images for each lyric stanza:

```
from concurrent.futures import ThreadPoolExecutor, as_completed

# Helper function to optimize segment stanzas
def optimize_segment_stanzas ( stanzas ):
if not stanzas: return []
optimized = []
for i in range ( len (stanzas)):
current = stanzas[i]
is_music = current.get( "lines" ) and "[Music...]" in current[ "lines" ][ 0 ].get( "text" , "" )
if is_music and i > 0 :
prev = optimized[ - 1 ]
music_duration = current[ "stanza_end" ] - current[ "stanza_start" ]
if music_duration < 2.0 :
prev[ "stanza_end" ] = current[ "stanza_end" ]
if prev.get( "lines" ): prev[ "lines" ][ - 1 ][ "end" ] = current[ "stanza_end" ]
continue
optimized.append(current)
return optimized

# Prepare image generation tasks
image_tasks = []
for seg_idx, segment in enumerate (segments):
segment[ "optimized_stanzas" ] = optimize_segment_stanzas(segment[ "stanzas" ])

for stan_idx, s in enumerate (segment[ "optimized_stanzas" ]):
image_tasks.append({
"seg_idx" : seg_idx,
"stan_idx" : stan_idx,
"prompt" : s[ "image_prompt" ]
})

def generate_worker ( task ):
img = coll.generate_image( prompt = task[ "prompt" ], aspect_ratio = "9:16" )
return task[ "seg_idx" ], task[ "stan_idx" ], img.id

# Generate images in parallel
MAX_WORKERS = 10
with ThreadPoolExecutor( max_workers = MAX_WORKERS ) as executor:
futures = [executor.submit(generate_worker, task) for task in image_tasks]

for future in as_completed(futures):
seg_i, stan_i, img_id = future.result()
segments[seg_i][ "optimized_stanzas" ][stan_i][ "image_id" ] = img_id
```

### [ Step 5: Build Multi-Layer Timeline](#step-5-build-multi-layer-timeline)

Create a timeline with audio, backgrounds, and animated lyrics:

```
import math
from videodb.editor import (
VideoAsset, ImageAsset, TextAsset, Font,
Clip, Track, Timeline, Transition,
Position, Fit, Offset, Alignment, HorizontalAlignment, VerticalAlignment, Border
)

def calculate_y_offsets ( num_lines , line_height = 45 , timeline_height = 1080 ):
offsets = []
start_pixel_offset = - ((num_lines - 1 ) * line_height) / 2
half_height = timeline_height / 2
for i in range (num_lines):
pixel_y = start_pixel_offset + (i * line_height)
offsets.append(pixel_y / half_height)
return offsets

# Timeline configuration
TIMELINE_WIDTH = 608
TIMELINE_HEIGHT = 1080
PRE_ROLL = 5.0
POST_ROLL = 5.0
CTA_DURATION = 5.0

# Render each segment
for idx, segment in enumerate (segments):
# Calculate timing
actual_seg_start = segment[ "start_time" ]
actual_seg_end = segment[ "end_time" ]

timeline_start_og = max ( 0 , actual_seg_start - PRE_ROLL )
intro_duration = actual_seg_start - timeline_start_og
total_audio_duration = (actual_seg_end - timeline_start_og) + CTA_DURATION + POST_ROLL

stanza_items = segment[ "optimized_stanzas" ]

# Initialize timeline
timeline = Timeline(conn)
timeline.resolution = f " { TIMELINE_WIDTH } x { TIMELINE_HEIGHT } "
timeline.background = "#000000"

# Layer 1: Audio Track (opacity=0 for audio only)
audio_track = Track( z_index = 0 )
audio_track.add_clip(
start = 0.0 ,
clip = Clip(
asset = VideoAsset( id = video.id, start = timeline_start_og, volume = 1.0 ),
duration = total_audio_duration,
fit = Fit.crop,
position = Position.center,
opacity = 0.0 ,
transition = Transition( in_ = "fade" , out = "fade" , duration = 5.0 )
),
)
timeline.add_track(audio_track)

# Layer 2: Background Images Track
images_track = Track( z_index = 1 )
for i, s in enumerate (stanza_items):
local_start = s[ "stanza_start" ] - timeline_start_og
local_end = s[ "stanza_end" ] - timeline_start_og

if i == 0 :
local_start = 0.0
trans_in = Transition( in_ = "fade" , duration = intro_duration)
else :
trans_in = Transition( in_ = "fade" , out = "fade" , duration = 0.35 )

duration = max ( 0.1 , local_end - local_start)

images_track.add_clip(
start = local_start,
clip = Clip(
asset = ImageAsset( id = s[ "image_id" ]),
duration = duration,
fit = Fit.crop,
position = Position.center,
transition = trans_in
),
)
timeline.add_track(images_track)

# Layer 3: Lyrics Track
lyrics_track = Track( z_index = 2 )
LINE_HEIGHT = 45
lyrics_border = Border( color = "#000000" , width = 1.5 )

for s in stanza_items:
lines = s.get( "lines" , [])
y_offsets = calculate_y_offsets( len (lines), LINE_HEIGHT , TIMELINE_HEIGHT )
local_stanza_end = s[ "stanza_end" ] - timeline_start_og

for l_idx, line in enumerate (lines):
local_line_start = line[ "start" ] - timeline_start_og
line_duration = max ( 0.1 , local_stanza_end - local_line_start)

text_asset = TextAsset(
text = line[ "text" ],
font = Font( family = "Bebas Neue" , size = 48 , color = "#FFFFFF" , weight = 700 ),
border = lyrics_border,
alignment = Alignment( horizontal = HorizontalAlignment.center, vertical = VerticalAlignment.center)
)

lyrics_track.add_clip(
start = local_line_start,
clip = Clip(
asset = text_asset,
duration = line_duration,
position = Position.center,
offset = Offset( x = 0 , y = y_offsets[l_idx]),
transition = Transition( in_ = "fade" , duration = 0.5 )
)
)

# Layer 4: CTA (Call to Action)
cta_start_time = (actual_seg_end - timeline_start_og)
cta_lines = [ "Visit the channel" , "for the full video" ]
cta_y_offsets = calculate_y_offsets( len (cta_lines), line_height = 60 , timeline_height = TIMELINE_HEIGHT )

for c_idx, cta_text in enumerate (cta_lines):
cta_asset = TextAsset(
text = cta_text,
font = Font( family = "Bebas Neue" , size = 42 , color = "#FFFFFF" , weight = 700 ),
border = lyrics_border,
alignment = Alignment( horizontal = HorizontalAlignment.center, vertical = VerticalAlignment.center)
)

lyrics_track.add_clip(
start = cta_start_time,
clip = Clip(
asset = cta_asset,
duration = CTA_DURATION ,
position = Position.center,
offset = Offset( x = 0 , y = cta_y_offsets[c_idx]),
transition = Transition( in_ = "fade" , duration = 0.5 )
)
)

timeline.add_track(lyrics_track)

# Generate final stream
stream_url = timeline.generate_stream()
```

## [ What You Get](#what-you-get)

A professional-looking short-form video ready for social media:

- Perfectly timed to the music
- AI-generated matching visuals
- Synced lyrics on screen
- Professional pre-roll and CTA
- Vertical format (608x1080)
- Ready to upload to TikTok, Reels, or Shorts

Here's the final rendered video:

## [ The Result](#the-result)

With this system, you can:

- Process music videos in minutes instead of hours
- Generate unlimited vertical clips from one source video
- Maintain consistency across all clips with the same visual style
- Stay on top of social media trends with fast production

No more manual editing. Just music, lyrics, AI-generated visuals, and viral potential.

## Explore the Full Notebook

Open the complete implementation with parallel processing, custom effects, and advanced styling options.

## [ Related Tutorials](#related-tutorials)

## Faceless Video Creator

Build complete faceless videos with AI scripts and voiceovers

## Year in Frames

Create personalized year recap videos from photo collections

[AI-Generated Ads](\examples-and-tutorials\content-factory\ai-ad-films) [Video Dubbing](\examples-and-tutorials\content-factory\dubbing)

⌘ I