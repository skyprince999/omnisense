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

- [Programmatic Editing](#programmatic-editing)
    - [When to Use This](#when-to-use-this)
    - [What You'll Build](#what-you%E2%80%99ll-build)
- [Timeline Architecture](#timeline-architecture)
- [How It Works](#how-it-works)
- [Related Documentation](#related-documentation)
- [Explore Use Cases by Category](#explore-use-cases-by-category)
    - [Video Enhancement](#video-enhancement)
    - [Dynamic Content](#dynamic-content)
    - [Analysis &amp; Compilation](#analysis-%26-compilation)

[Programmatic Editing](\examples-and-tutorials\programmatic-editing\index)

# Overview

Copy page

Edit and compose videos with code - no manual editing tools required

Copy page

## [ Programmatic Editing](#programmatic-editing)

**Edit videos with code, not clicks.** Compose, overlay, trim, and transform videos using the Timeline API.

### [ When to Use This](#when-to-use-this)

- You need to add intros/outros to hundreds of videos
- You want to insert dynamic ads based on viewer data
- You're building a tool that adds branded elements automatically
- You need multi-version output (different aspect ratios, subtitles)

### [ What You'll Build](#what-you’ll-build)

## Intro &amp; Outro

Automatically add opening/closing sequences

## Brand Elements

Overlay logos, watermarks, and graphics

## Audio Overlay

Add background music and sound effects

## Dynamic Ads

Insert personalized ads per viewer

## Dynamic Streams

Generate multiple versions from one source

## Word Counter

Add analytical text overlays

## Chess Montage

Auto-compile highlight reels from long videos

## [ Timeline Architecture](#timeline-architecture)

Timeline Architecture Diagram

<!-- image -->

**4 Layers:**

- **Asset** - The media file (video, audio, image)
- **Clip** - A segment with timing and parameters
- **Track** - A layer in the composition
- **Timeline** - The complete output

## [ How It Works](#how-it-works)

```
from videodb.editor import Timeline, Track, Clip, VideoAsset

timeline = Timeline(conn)
track = Track()
track.add_clip( 0 , Clip( asset = VideoAsset( id = video.id), duration = 30 ))
timeline.add_track(track)

stream_url = timeline.generate_stream() # Instant, no rendering
```

## [ Related Documentation](#related-documentation)

## Timeline Architecture

Deep dive into the 4-layer model

## Clip Parameters

All available clip options

## Aspect Ratio Control

Handle different video dimensions

## Caption Asset

Add text overlays and subtitles

## [ Explore Use Cases by Category](#explore-use-cases-by-category)

### [ Video Enhancement](#video-enhancement)

## Intro &amp; Outro

Auto-add opening and closing sequences

## Brand Elements

Add logos, watermarks, and graphics

## Audio Overlay

Add background music and sound effects

### [ Dynamic Content](#dynamic-content)

## Dynamic Ads

Insert personalized ads per viewer

## Dynamic Streams

Generate multiple versions from one source

### [ Analysis &amp; Compilation](#analysis-&-compilation)

## Word Counter

Add analytical text overlays

## Chess Montage

Auto-compile highlight reels from videos

[PromptClip](\pages\community\open-source\promptclip) [Intro/Outro](\examples-and-tutorials\programmatic-editing\intro-outro)

⌘ I