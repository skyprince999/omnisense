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

- [The Problem](#the-problem)
- [What You'll Build](#what-you%E2%80%99ll-build)
- [Setup](#setup)
    - [Install Dependencies](#install-dependencies)
    - [Connect to VideoDB](#connect-to-videodb)
- [Implementation](#implementation)
    - [Step 1: Index Your Portfolio Videos](#step-1-index-your-portfolio-videos)
    - [Step 2: Upload Suspect Video for Analysis](#step-2-upload-suspect-video-for-analysis)
    - [Step 3: Perform Similarity Comparison](#step-3-perform-similarity-comparison)
    - [Step 4: Detect Sequential Patterns](#step-4-detect-sequential-patterns)
    - [Step 5: Generate Evidence Clips](#step-5-generate-evidence-clips)
    - [Step 6: Generate Plagiarism Report](#step-6-generate-plagiarism-report)
- [What You Get](#what-you-get)
- [How It Works](#how-it-works)
- [Similarity Thresholds](#similarity-thresholds)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Safety &amp; Compliance](\examples-and-tutorials\safety-compliance\index)

# AI Video Copyright Detection

Copy page

Production-ready plagiarism detection system using semantic similarity and scene analysis

Copy page

Open In Colab

<!-- image -->

## [ The Problem](#the-problem)

Your original video content gets stolen, re-uploaded, and monetized by others. By the time you notice, it's already viral. Traditional manual checking doesn't scale - you need AI. This guide shows you how to build a production-ready system that detects when your videos are stolen, even with edits, and generates evidence for DMCA takedowns.

## [ What You'll Build](#what-you’ll-build)

Build a system that:

- Indexes your video portfolio as searchable "fingerprints"
- Detects visual similarity in suspect videos (even with edits)
- Generates side-by-side comparison clips for DMCA evidence
- Identifies sequential matching (stronger proof of plagiarism)
- Creates comprehensive reports with confidence scores

All powered by **VideoDB's Editor SDK** and semantic search.

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

### [ Step 1: Index Your Portfolio Videos](#step-1-index-your-portfolio-videos)

```
from videodb import SceneExtractionType, IndexType

# Upload your original videos
portfolio_videos = []
portfolio_videos.append(coll.upload( url = "https://example.com/original-video-1.mp4" ))
portfolio_videos.append(coll.upload( url = "https://example.com/original-video-2.mp4" ))

# Create scene indexes for all portfolio videos
portfolio_indexes = {}
for video in portfolio_videos:
index_id = video.index_scenes(
extraction_type = SceneExtractionType.shot_based,
extraction_config = { "threshold" : 20 }
)
portfolio_indexes[video.id] = index_id
```

### [ Step 2: Upload Suspect Video for Analysis](#step-2-upload-suspect-video-for-analysis)

```
# Upload the video you suspect is plagiarized
suspect_video = coll.upload( url = "https://example.com/suspect-video.mp4" )

# Create scene index for suspect video (shot-based for better detection)
suspect_index_id = suspect_video.index_scenes(
extraction_type = SceneExtractionType.shot_based,
extraction_config = { "threshold" : 20 }
)
```

### [ Step 3: Perform Similarity Comparison](#step-3-perform-similarity-comparison)

```
from videodb import IndexType

matches = []
similarity_threshold = 0.70

# Get suspect video scenes
suspect_scenes = suspect_video.get_scene_index(suspect_index_id)

for portfolio_vid_id, portfolio_index_id in portfolio_indexes.items():
portfolio_video = coll.get_video(portfolio_vid_id)

# Compare each suspect scene against portfolio
for suspect_scene in suspect_scenes:
# Use VideoDB's semantic search
results = portfolio_video.search(
query = suspect_scene[ 'description' ],
search_type = "semantic" ,
index_type = IndexType.scene,
index_id = portfolio_index_id
)

# Process results
for shot in results.shots:
if shot.search_score > similarity_threshold:
matches.append({
"suspect_time" : suspect_scene[ 'start' ],
"portfolio_video" : portfolio_vid_id,
"portfolio_time" : shot.start,
"similarity" : shot.search_score
})

# Sort by highest similarity
matches = sorted (matches, key = lambda x : x[ "similarity" ], reverse = True )
```

### [ Step 4: Detect Sequential Patterns](#step-4-detect-sequential-patterns)

```
# Check for sequential matching (stronger evidence)
sequential_matches = []
consecutive_count = 0
last_similarity = 0

for match in matches:
if match[ "similarity" ] > 0.80 and consecutive_count < 5 :
consecutive_count += 1
sequential_matches.append(match)
else :
if consecutive_count >= 3 : # 3+ consecutive = strong evidence
sequential_matches.extend(sequential_matches[ - consecutive_count:])
consecutive_count = 0

plagiarism_confidence = min ( 1.0 , len (sequential_matches) / 10 )
```

### [ Step 5: Generate Evidence Clips](#step-5-generate-evidence-clips)

```
from videodb.editor import Timeline, Track, Clip, VideoAsset, Position, Fit

# Create side-by-side comparison timeline
timeline = Timeline(conn)

# Add matching segments side-by-side
for match in matches[: 5 ]: # Top 5 matches as evidence
track = Track()

# Portfolio video (left side)
portfolio_asset = VideoAsset(
id = match[ "portfolio_video" ],
start = match[ "portfolio_time" ]
)
portfolio_clip = Clip(
asset = portfolio_asset,
duration = 5 ,
position = Position.left,
fit = Fit.crop,
scale = 0.5
)
track.add_clip( 0 , portfolio_clip)

# Suspect video (right side)
suspect_asset = VideoAsset(
id = suspect_video.id,
start = match[ "suspect_time" ]
)
suspect_clip = Clip(
asset = suspect_asset,
duration = 5 ,
position = Position.right,
fit = Fit.crop,
scale = 0.5
)
track.add_clip( 0 , suspect_clip)

timeline.add_track(track)

# Generate evidence video
evidence_stream_url = timeline.generate_stream()
```

### [ Step 6: Generate Plagiarism Report](#step-6-generate-plagiarism-report)

```
# Create comprehensive report
report = {
"suspect_video_id" : suspect_video.id,
"total_matches" : len (matches),
"sequential_matches" : len (sequential_matches),
"plagiarism_confidence" : plagiarism_confidence,
"high_confidence_matches" : len ([m for m in matches if m[ "similarity" ] > 0.95 ]),
"medium_confidence_matches" : len ([m for m in matches if 0.85 < m[ "similarity" ] <= 0.95 ]),
"evidence_video_url" : evidence_stream_url,
"timestamp" : "2025-01-20T12:00:00Z"
}

# If confidence > 0.80, recommend DMCA takedown
if plagiarism_confidence > 0.80 :
report[ "recommendation" ] = "STRONG PLAGIARISM DETECTED - Ready for DMCA takedown"
report[ "action" ] = "prepare_dmca_evidence"
```

## [ What You Get](#what-you-get)

A production-ready detection system with:

- Scene-by-scene visual fingerprinting
- Semantic similarity matching (catches edits/crops)
- Sequential pattern detection (strengthens evidence)
- Side-by-side comparison clips
- Confidence scoring for legal action
- Automated DMCA-ready reports

Here's the side-by-side evidence video:

## [ How It Works](#how-it-works)

1. **Portfolio Indexing** - Convert your original videos into searchable scene embeddings
2. **Suspect Upload** - Upload suspected plagiarized video
3. **Similarity Scan** - Compare each scene using semantic similarity (catches edits)
4. **Sequential Detection** - Look for multiple consecutive matches (stronger evidence)
5. **Evidence Generation** - Create side-by-side comparison clips
6. **DMCA Ready** - Generate professional report for takedown

## [ Similarity Thresholds](#similarity-thresholds)

- **0.95+** = Nearly identical (very likely plagiarism)
- **0.85-0.95** = High similarity (suspicious)
- **0.70-0.85** = Medium similarity (may be coincidence)
- **&lt;0.70** = Low similarity (likely not plagiarism)

Adjust thresholds based on your tolerance for false positives.

## [ The Result](#the-result)

With this system, you can:

- Protect your intellectual property at scale
- Detect plagiarism even with edits and filters
- Generate professional DMCA evidence automatically
- Monitor multiple suspect videos efficiently
- Respond to theft quickly with automated reports

Your content is your property. Protect it with AI.

## Explore the Full Notebook

Open the complete implementation with advanced embedding techniques, batch processing, and database management.

## [ Related Tutorials](#related-tutorials)

## Profanity Beeper

Auto-detect and beep curse words in audio

## Content Removal

Skip inappropriate visual content in streams

[AI-Powered Content Moderation](\examples-and-tutorials\safety-compliance\remove-content)

⌘ I