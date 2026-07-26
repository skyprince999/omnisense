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

- [Process](#process)
- [Download PromptClip](#download-promptclip)
- [PromptClip in Action](#promptclip-in-action)
    - [1. Spoken Content Analysis](#1-spoken-content-analysis)
    - [2. Visual/Scene Analysis](#2-visual%2Fscene-analysis)
    - [3. Using both Visual and Spoken](#3-using-both-visual-and-spoken)
    - [Why PromptClip Will Transform Your Work](#why-promptclip-will-transform-your-work)
- [Watch PromptClip in Action](#watch-promptclip-in-action)
- [The Magic Behind PromptClip: VideoDB's Indexing Methods](#the-magic-behind-promptclip-videodb%E2%80%99s-indexing-methods)
- [Join the VideoDB Community](#join-the-videodb-community)

[Content Factory](\examples-and-tutorials\content-factory\index)

# PromptClip

Copy page

AI-powered video editing with natural language prompts - find perfect moments in videos instantly using spoken and visual content analysis.

Copy page

## Try PromptClip

Open source repo for AI-driven video editing

PromptClip is your new superpower for video editing with prompts. While editing, we all wanted to find that perfect moment in a video with ease. Say goodbye to manually skimming and seeking through video, and say hello to instant, AI-driven video consumption and creation. LLMs are great with text, but they don't help you consume or create video clips. We've built [PromptClip](https://github.com/video-db/PromptClip) , an open source repo to get you started on AI driven video editing. For example, you can just say: " *Find the moment where Mr. Bean is attempting to cheat by peeking at the answer sheet of the man beside him* "

### [ Process](#process)

1

Describe what you want

Use natural language to describe what you want.

2

Run prompts

Run prompts on the visual scenes and spoken content with the choice of your LLM.

3

Get video stream

Instantly get video compilation stream from VideoDB.

PromptClip architecture showing the process of describing prompts, running analysis, and getting video streams

<!-- image -->

## [ Download PromptClip](#download-promptclip)

1

Get your API key

Get your API key from the [VideoDB console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) (Free for first 50 uploads, no credit card required)

2

Set up your environment

- Add your `VIDEO_DB_API_KEY` to the `.env` file
- Include your preferred LLM API key ( `OPENAI_API_KEY` or `ANTHROPIC_KEY` ) in `.env`

3

Install dependencies

Run `pip install -r requirements.txt`

4

Explore notebooks

Launch the Jupyter notebooks to start experimenting:

- Create clips using only spoken content: [PromptClip Spoken Notebook](https://github.com/video-db/PromptClip/blob/scene-support/PromptClip_spoken.ipynb)
- Create clips by analysing visual content: [PromptClip Visual Notebook](https://github.com/video-db/PromptClip/blob/scene-support/PromptClip_visual.ipynb)
- Using combined audio-visual analysis: [PromptClip Multimodal Notebook](https://github.com/video-db/PromptClip/blob/scene-support/PromptClip_multimodal.ipynb)

## [ PromptClip in Action](#promptclip-in-action)

### [ 1. Spoken Content Analysis](#1-spoken-content-analysis)

**Prompt: Find every moment where a deal was offered**

**Source:** [Shark Tank](https://www.youtube.com/watch?v=HpUR7-Oe1ss) **Prompt: Show me moments in the video where the host discusses or reveals the pricing of the gadgets.**

**Source:** [Useful Gadgets](https://www.youtube.com/watch?v=bGmXrMW9ucU)

### [ 2. Visual/Scene Analysis](#2-visual\scene-analysis)

**Prompt: Find the moment where Mr. Bean is attempting to cheat by peeking at the answer sheet of the man beside him**

### [ 3. Using both Visual and Spoken](#3-using-both-visual-and-spoken)

**Prompt: Find scenes explaining cricket rules using infographics**

### [ Why PromptClip Will Transform Your Work](#why-promptclip-will-transform-your-work)

## Efficiency

Reduce hours of manual video searching to mere seconds.

## Creativity

Generate fresh perspectives and ideas from your existing content.

## Precision

Extract exactly what you need, not just approximate matches.

## Flexibility

Works with various video types, topics, and [languages](\pages\understand\indexing-pipelines\multimodal-indexing) .

PromptClip is more than a tool; it's a new way of content interaction - The natural language way! Whether you're a content creator, researcher, or developer, PromptClip empowers you to unlock the full potential of your video content.

## [ Watch PromptClip in Action](#watch-promptclip-in-action)

Here you can check more PromptClip examples **Prompt: "Find details about every sponsor"**

**Prompt: "Find sentences where anxiety is discussed"**

**Prompt: "How to control sugar cravings"**

## [ The Magic Behind PromptClip: VideoDB's Indexing Methods](#the-magic-behind-promptclip-videodb’s-indexing-methods)

PromptClip leverages VideoDB's advanced indexing techniques and Large Language Models (LLMs) to analyze and manipulate video content with unmatched power.

Spoken Word Indexing

- **Process** : VideoDB transcribes the audio content and creates a searchable index of spoken words.
- **Implementation** : Uses advanced speech recognition algorithms to generate accurate transcripts.

Visual/Scene Indexing

- **Process** : Analyzes video frames to identify objects, actions, and scene compositions.
- **Implementation** : Employs sophisticated scene extraction algorithms and vision models for comprehensive visual understanding.
- **Customization** : Allows for different extraction algorithms and custom prompts for scene description. Find detailed documentation in our [Scene Indexing Guide](\pages\understand\indexing-pipelines\create-an-index) .

## [ Join the VideoDB Community](#join-the-videodb-community)

Your ideas drive PromptClip's evolution. Get involved:

## GitHub

Report issues, suggest features, or contribute code via pull requests

## Discord

Share your innovative use cases and connect with the community

For more information and support, refer to the [VideoDB documentation](https://docs.videodb.io/)

[Annual Video Statistics Recap](\examples-and-tutorials\content-factory\year-in-frames) [Overview](\examples-and-tutorials\programmatic-editing)

⌘ I