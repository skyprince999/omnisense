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
    - [Step 1: Upload Video](#step-1-upload-video)
    - [Step 2: Index Scenes with Moderator Prompt](#step-2-index-scenes-with-moderator-prompt)
    - [Step 3: Review Scene Indexes (Optional)](#step-3-review-scene-indexes-optional)
    - [Step 4: Filter for Safe Content](#step-4-filter-for-safe-content)
    - [Step 5: Play the Clean Version](#step-5-play-the-clean-version)
- [What You Get](#what-you-get)
- [Perfect For](#perfect-for)
- [The Result](#the-result)
- [Related Tutorials](#related-tutorials)

[Safety &amp; Compliance](\examples-and-tutorials\safety-compliance\index)

# AI-Powered Content Moderation

Copy page

Moderate video content using AI scene indexing with no external APIs required

Copy page

Open In Colab

<!-- image -->

## [ The Idea](#the-idea)

Content moderation can be complex, often requiring multiple tools, manual timestamp extraction, and intricate integration work. Setting up these pipelines involves managing credentials, parsing responses, and stitching everything together. VideoDB simplifies this into a **"Prompt-and-Filter"** workflow using native AI scene indexing. No external credentials needed. No manual timestamp extraction. Just **prompt engineering** that creates structured labels ( **CONTENT\_SAFE** / **CONTENT\_UNSAFE** ) from unstructured video content. The innovation is simple: instead of generic video descriptions, we give the AI a **strict moderation role** with deterministic output labels. This turns unstructured video into structured, searchable data that can be filtered instantly. Want stricter moderation? **Update the prompt** . Need different criteria? Change a few lines. It's content moderation reimagined for the prompt engineering era.

## [ Setup](#setup)

### [ Install Dependencies](#install-dependencies)

Python

Node.js

```
pip install videodb
```

```
npm install videodb
```

### [ Connect to VideoDB](#connect-to-videodb)

Get your API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) . Free for first 50 uploads, no credit card required.

Python

Node.js

```
from videodb import connect

conn = connect( api_key = "YOUR_API_KEY" )
coll = conn.get_collection()
```

```
import { connect } from 'videodb' ;

const conn = await connect ({ apiKey: process . env . VIDEO_DB_API_KEY });
const coll = await conn . getCollection ();
```

## [ Implementation](#implementation)

### [ Step 1: Upload Video](#step-1-upload-video)

We'll use a Breaking Bad clip with mixed content to test the moderation workflow.

Python

Node.js

```
# Upload video from YouTube
video = coll.upload( url = 'https://www.youtube.com/watch?v=Xa7UaHgOGfM' )
print ( f "Uploaded Video ID: { video.id } " )

# Preview the video
video.play()
```

```
// Upload video from YouTube
const video = await coll . upload ({ url: 'https://www.youtube.com/watch?v=Xa7UaHgOGfM' });
console . log ( `Uploaded Video ID: ${ video . id } ` );

// Get the player URL
const playerUrl = video . playerUrl ;
console . log ( playerUrl );
```

### [ Step 2: Index Scenes with Moderator Prompt](#step-2-index-scenes-with-moderator-prompt)

This is the core innovation. We give the AI a strict role as a Content Moderator with deterministic output labels. The prompt instructs the AI to analyze visual content for specific inappropriate elements and respond with either `CONTENT_SAFE` or `CONTENT_UNSAFE` . This structured labeling transforms unstructured video into searchable, filterable data.

Python

Node.js

```
from videodb import SceneExtractionType

# Define strict moderation instructions
moderation_prompt = """
You are a Content Moderator. Analyze the visual content for inappropriate elements:
1. Violence (fighting, hitting, shooting)
2. Weapons (guns, knives)
3. Blood or Gore
4. Drug use
5. Sexual content

If ANY of these are detected, your response must start with:
"CONTENT_UNSAFE: [brief reason]"

If the scene is clean and safe, your response must start with:
"CONTENT_SAFE: [brief description]"
"""

# Index video in 5-second chunks for granular moderation
scene_index_id = video.index_scenes(
prompt = moderation_prompt,
extraction_type = SceneExtractionType.time_based,
extraction_config = {
"time" : 5 , # Check every 5 seconds
"frame_count" : 3 # Analyze 3 frames per segment
}
)

print ( "Moderation indexing complete!" )
```

```
import { SceneExtractionTypeValues } from 'videodb' ;

// Define strict moderation instructions
const moderationPrompt = `
You are a Content Moderator. Analyze the visual content for inappropriate elements:
1. Violence (fighting, hitting, shooting)
2. Weapons (guns, knives)
3. Blood or Gore
4. Drug use
5. Sexual content

If ANY of these are detected, your response must start with:
"CONTENT_UNSAFE: [brief reason]"

If the scene is clean and safe, your response must start with:
"CONTENT_SAFE: [brief description]"
` ;

// Index video in 5-second chunks for granular moderation
const sceneIndexId = await video . indexScenes ({
prompt: moderationPrompt ,
extractionType: SceneExtractionTypeValues . timeBased ,
extractionConfig: {
time: 5 , // Check every 5 seconds
frameCount: 3 // Analyze 3 frames per segment
}
});

console . log ( "Moderation indexing complete!" );
```

**Why this works:** By enforcing strict output formats ( `CONTENT_SAFE` / `CONTENT_UNSAFE` ), we can use simple keyword searches to filter content. No complex parsing or external API integration needed.

### [ Step 3: Review Scene Indexes (Optional)](#step-3-review-scene-indexes-optional)

Want to see what the AI detected? Check the scene indexes to understand how content was labeled.

Python

Node.js

```
# Fetch scene indexes
scene_indexes = video.get_scene_index(scene_index_id)

# Print first 5 scenes
for i, scene in enumerate (scene_indexes[: 5 ]):
print ( f "Scene { i + 1 } :" )
print ( f "  Time: { scene[ 'start' ] } s - { scene[ 'end' ] } s" )
print ( f "  Status: { scene[ 'description' ] } \n " )
```

```
// Fetch scene indexes
const sceneIndexes = await video . getSceneIndex ( sceneIndexId );

// Print first 5 scenes
sceneIndexes . slice ( 0 , 5 ). forEach (( scene , i ) => {
console . log ( `Scene ${ i + 1 } :` );
console . log ( `  Time: ${ scene . start } s - ${ scene . end } s` );
console . log ( `  Status: ${ scene . description } \n ` );
});
```

**Sample output:**

```
Scene 1:
Time: 0.0s - 5.005s
Status: CONTENT_SAFE: The images display title cards with a smoky background...

Scene 2:
Time: 5.005s - 10.01s
Status: CONTENT_SAFE: Two men in indoor settings, no inappropriate elements...

Scene 5:
Time: 20.02s - 25.025s
Status: CONTENT_UNSAFE: Implied physical confrontation and aggressive interaction...
```

### [ Step 4: Filter for Safe Content](#step-4-filter-for-safe-content)

Now the magic happens. Because we structured the AI's responses with `CONTENT_SAFE` labels, we can use a simple keyword search to filter the entire video.

Python

Node.js

```
from videodb import SearchType, IndexType

# Search for safe content using keyword search
safe_results = video.search(
query = "CONTENT_SAFE" ,
search_type = SearchType.keyword,
index_type = IndexType.scene,
scene_index_id = scene_index_id
)

# Get the safe segments
safe_shots = safe_results.get_shots()
print ( f "Found { len (safe_shots) } safe segments" )

# Inspect first few segments
for i, shot in enumerate (safe_shots[: 3 ]):
print ( f "Segment { i + 1 } ( { shot.start } s - { shot.end } s): { shot.text } " )
```

```
import { SearchTypeValues , IndexTypeValues } from 'videodb' ;

// Search for safe content using keyword search
const safeResults = await video . search ({
query: "CONTENT_SAFE" ,
searchType: SearchTypeValues . keyword ,
indexType: IndexTypeValues . scene ,
sceneIndexId: sceneIndexId
});

// Get the safe segments
const safeShots = safeResults . getShots ();
console . log ( `Found ${ safeShots . length } safe segments` );

// Inspect first few segments
safeShots . slice ( 0 , 3 ). forEach (( shot , i ) => {
console . log ( `Segment ${ i + 1 } ( ${ shot . start } s - ${ shot . end } s): ${ shot . text } ` );
});
```

### [ Step 5: Play the Clean Version](#step-5-play-the-clean-version)

The filtered results come with a stream URL ready for instant playback. No rendering, no waiting.

Python

Node.js

```
# Get the stream URL
print ( "Stream URL:" , safe_results.stream_url)

# Play in notebook/browser
safe_results.play()
```

```
// Get the stream URL
console . log ( "Stream URL:" , safeResults . streamUrl );

// Use this URL in any video player
```

Here's the result - a clean version with all inappropriate content removed:

## [ What You Get](#what-you-get)

- No external APIs or credentials required
- Full control over moderation criteria through prompts
- Instant filtering without video re-encoding
- Granular 5-second scene analysis
- Real-time playback of cleaned content
- Customizable: change prompt to adjust moderation standards instantly

## [ Perfect For](#perfect-for)

- Educational platforms serving minor audiences
- Family-friendly streaming services
- Corporate training content libraries
- Social media platforms with content policies
- Broadcasting companies creating TV-safe edits
- User-generated content platforms with safety requirements

## [ The Result](#the-result)

What used to require multiple integrations, manual timestamp extraction, and complex video editing pipelines now works with just prompt engineering. Change your moderation criteria instantly by updating the prompt-no re-processing needed. Pure simplicity powered by VideoDB's native AI indexing.

## Explore Full Notebook

Open the complete implementation in Google Colab with detailed explanations and working code.

## [ Related Tutorials](#related-tutorials)

## Profanity Detection

Detect and censor curse words with audio overlays

## Keyword Search

Find and extract specific content from your videos

[Profanity Detection](\examples-and-tutorials\safety-compliance\beep-profanity) [AI Video Copyright Detection](\examples-and-tutorials\safety-compliance\copyright-detection)

⌘ I