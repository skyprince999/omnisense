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
    - [Step 1: Connect to VideoDB](#step-1-connect-to-videodb)
    - [Step 2: Upload the Video](#step-2-upload-the-video)
    - [Step 3: Index the Video on Different Modalities](#step-3-index-the-video-on-different-modalities)
    - [Indexing Spoken Content](#indexing-spoken-content)
    - [Find Right Configuration for Scene Indexing](#find-right-configuration-for-scene-indexing)
    - [Index Scenes With The Finalized Config and Prompt](#index-scenes-with-the-finalized-config-and-prompt)
    - [Step 4: Search Pipeline Implementation](#step-4-search-pipeline-implementation)
    - [Step 5: Viewing the Search Results](#step-5-viewing-the-search-results)
    - [The content written on the slide is](#the-content-written-on-the-slide-is)
    - [Search for "stripe api review"](#search-for-%E2%80%9Cstripe-api-review%E2%80%9D)
    - [API REVIEW CHECKLIST](#api-review-checklist)
    - [Search for "Friction Log"](#search-for-%E2%80%9Cfriction-log%E2%80%9D)
    - [Internal Terminal Dogfooding Instructions](#internal-terminal-dogfooding-instructions)
- [Conclusion](#conclusion)
- [Further Resources](#further-resources)
- [Get Support](#get-support)

[Video Search and Understanding](\examples-and-tutorials\video-rag\index)

# Use Case: Conference Slide Extraction

Copy page

Extract and search slide content from conference videos by combining spoken word search with visual scene indexing for instant information retrieval.

Copy page

Open In Colab

<!-- image -->

When watching a talk or presentation, it's common to take notes or share interesting points with others. Often, the content on the slides captures our attention. At VideoDB, we follow many top engineering processes and regularly take notes from talks and conferences, which we share internally on our Slack channel. However, when trying to recall specific parts of these talks, only a few keywords might come to mind. To address this, we built an internal tool that stores all these talks in VideoDB, allowing us to find and share the content on the screen in text form using a search query. Let's explore the problem: What was on the screen when the speaker discussed the "hard and fast rule" in the following video?

This notebook is a step towards creating a Slack bot that posts valuable engineering practices from top tech talks daily. Stay Tuned!

## [ Introduction](#introduction)

In this tutorial, we'll explore an advanced yet accessible technique for retrieving visual information from video content based on what the speaker was discussing. Specifically, we'll focus on finding information on slides in a video recording of a speech. As video content continues to grow in volume and importance, being able to quickly find specific information within videos becomes crucial. Imagine being able to locate a particular statistic mentioned in an hour-long presentation without watching the entire video. That's the power of multimodal video search! This approach combines VideoDB's powerful scene indexing capabilities with spoken word search to create a robust, multimodal search pipeline. Don't worry if these terms sound complex - we'll break everything down step by step!

## [ Setup](#setup)

### [ Installing packages](#installing-packages)

```
!pip install videodb
```

### [ API Keys](#api-keys)

Before proceeding, ensure access to [VideoDB](https://videodb.io/) . If not, sign up for API access on the respective platforms. Get your API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) (Free for first 50 uploads, No credit card required).

### [ Step 1: Connect to VideoDB](#step-1-connect-to-videodb)

Gear up by establishing a connection to VideoDB.

```
import videodb

# Set your API key
api_key = "your_api_key"

# Connect to VideoDB
conn = videodb.connect( api_key = api_key)
coll = conn.get_collection()
```

### [ Step 2: Upload the Video](#step-2-upload-the-video)

Next, let's upload our sample video:

```
# Upload a video by URL
video = coll.upload( url = "https://www.youtube.com/watch?v=libKVRa01L8" )
```

### [ Step 3: Index the Video on Different Modalities](#step-3-index-the-video-on-different-modalities)

Now comes the exciting part - we're going to index our video in two ways:

1. Indexing spoken content (what's being said in the video)
2. Indexing visual content (what's being shown in the video)

### [ Indexing Spoken Content](#indexing-spoken-content)

```
# Index spoken content

video.index_spoken_words()
```

This function transcribes the speech in the video and indexes it, making it searchable.

### [ Find Right Configuration for Scene Indexing](#find-right-configuration-for-scene-indexing)

To learn more about Scene Index, explore the following guides:

- [Quickstart Guide](https://github.com/video-db/videodb-cookbook/blob/main/quickstart/Scene%20Index%20QuickStart.ipynb) guide provides a step-by-step introduction to Scene Index. It's ideal for getting started quickly and understanding the primary functions.
- [Scene Extraction Options Guide](https://github.com/video-db/videodb-cookbook/blob/main/guides/scene-index/playground_scene_extraction.ipynb) delves deeper into the various options available for scene extraction within Scene Index. It covers advanced settings, customization features, and tips for optimizing scene extraction based on different needs and preferences.

1. **Finding the Best Configuration for Scene Extraction**

```
from IPython.display import Image, display
import requests


# Helper function that will help us view the Scene Collection Images
def display_scenes ( scenes , images = True ):
for scene in scenes:
print ( f " { scene.id } : { scene.start } - { scene.end } " )
if images:
for frame in scene.frames:
im = Image(requests.get(frame.url, stream = True ).content)
display(im)
print ( "----" )


scene_collection_default = video.extract_scenes()
display_scenes(scene_collection_default.scenes)
```

For conference videos, we would like to lower threshold to capture all slides. Let's run the scene extraction again and see the results.

```
from videodb import SceneExtractionType

scene_collection = video.extract_scenes(
extraction_type = SceneExtractionType.shot_based,
extraction_config = {
"threshold" : 10 ,
},
)
display_scenes(scene_collection.scenes)
```

**2. Finding the Right prompt for Indexing** Testing the `prompt` on some sample scenes first is a sensible approach. It allows you to experiment and make adjustments without committing to the entire video, which can help manage costs. The `prompt` guides the visual model to identify and describe the content of slides in each scene, outputting "None" if no slides are visible. This targeted testing can help fine-tune the model's performance before applying it to the entire video.

```
for scene in scene_collection.scenes[ 20 : 23 ]:
description = scene.describe(
"Give the content writen on the slides, output None if it isn't the slides."
)
print ( f " { scene.id } : { scene.start } - { scene.end } " )
print (description)
print ( "-----" )
```

Now that we have found the right configuration for Scene Indexing, it's like we've found the perfect match-let's commit to indexing those scenes!

### [ Index Scenes With The Finalized Config and Prompt](#index-scenes-with-the-finalized-config-and-prompt)

This function fits all the steps above into a single cell and processes the entire video accordingly:

1. It breaks the video into scenes using a shot-based approach
2. For each scene, it analyzes the visual content based on the given `prompt`
3. It creates an index of these scene descriptions

```
# Help function to View the Scene Index
def display_scene_index ( scene_index ):
for scene in scene_index:
print ( f " { scene[ 'start' ] } - { scene[ 'end' ] } " )
print (scene[ "description" ])
print ( "----" )


scene_index_id = video.index_scenes(
prompt = "Give the content writen on the slides, output None if it isn't the slides." ,
name = "slides_index" ,
extraction_type = SceneExtractionType.shot_based,
extraction_config = {
"threshold" : 10 ,
},
)
print (scene_index_id)
scene_index = video.get_scene_index(scene_index_id)
display_scene_index(scene_index)
```

### [ Step 4: Search Pipeline Implementation](#step-4-search-pipeline-implementation)

The heart of this approach is the search pipeline, which combines spoken word search with scene indexing. This pipeline does the following:

1. Performs a keyword search on the spoken word index
2. Extracts time ranges from the search results
3. Retrieves the scenes
4. Filters scenes based on overlaps with the time ranges from the spoken word search
5. Returns the descriptions of these scenes (our slide content) and their time ranges

```
def simple_filter_scenes ( time_ranges , scene_dicts ):
def is_in_range ( scene , range_start , range_end ):
scene_start = scene[ "start" ]
scene_end = scene[ "end" ]
return (
(range_start <= scene_start <= range_end)
or (range_start <= scene_end <= range_end)
or (scene_start <= range_start and scene_end >= range_end)
)

filtered_scenes = []
for start, end in time_ranges:
filtered_scenes.extend(
[scene for scene in scene_dicts if is_in_range(scene, start, end)]
)

# Remove duplicates while preserving order
seen = set ()
return [
scene
for scene in filtered_scenes
if not ( tuple (scene.items()) in seen or seen.add( tuple (scene.items())))
]
```

```
from videodb import IndexType, SearchType


def search_pipeline ( query , video ):
# Search Query in Spoken Word Index
search_result = video.search(
query = query,
index_type = IndexType.spoken_word,
search_type = SearchType.keyword
)
time_ranges = [(shot.start, shot.end) for shot in search_result.get_shots()]

scenes = scene_index

for scene in scenes:
scene[ "start" ] = float (scene[ "start" ])
scene[ "end" ] = float (scene[ "end" ])

# Filter Scene on the basis of Spoken results
final_result = simple_filter_scenes(time_ranges, scenes)

# Return Scene descriptions and Video Timelines of result
result_text = " \n\n " .join(
result_entry[ "description" ]
for result_entry in final_result
if result_entry.get( "description" , "" ).lower().strip() != "none"
)
result_timeline = [
(result_entry.get( "start" ), result_entry.get( "end" ))
for result_entry in final_result
]

return result_text, result_timeline
```

### [ Step 5: Viewing the Search Results](#step-5-viewing-the-search-results)

Finally, let's use our search pipeline:

```
from videodb import play_stream

query = "hard and fast rule"

result_text, result_timeline = search_pipeline(query, video)

stream_link = video.generate_stream(result_timeline)
play_stream(stream_link)

print (result_text)
```

It returns scenes where the spoken words match your query, along with the content of any slides visible in those scenes. Here's the result for this particular search query "hard and fast rule":

### [ The content written on the slide is](#the-content-written-on-the-slide-is)

```
IT'S ALL IN THE DETAILS

- Prefer American English for naming
- Avoid payment-industry jargon
- Timestamp fields should use <verbed_at>
- Amount properties should also provide a currency
- API resources with IDs are top-level
- New API resources should be retrieved and listed one way
- API resource mutations should be reflected in API responses
- Use nested structures for future extensibility
- Prefer enums to booleans for new properties
- Use a type field for polymorphic objects
- Use verbs for properties with side effects
- Use top-level namespaces for product APIs
- Evaluate new features in the Dashboard before building an API
- Use simple, unambiguous language
- Always paginate unbounded lists
- Iterate on designs with beta users with the feature behind a gate
```

Here are some other query outputs using the same search pipeline:

### [ Search for "stripe api review"](#search-for-“stripe-api-review”)

### [ API REVIEW CHECKLIST](#api-review-checklist)

```
API Review: [Insert Title Here]
Ziec: Gavel jar, link for API review join creation

Gavel block
To ping PM when Q/A and other stakeholders have

Summary
(Please include a short description of the change you would like to make...)
```

### [ Search for "Friction Log"](#search-for-“friction-log”)

### [ Internal Terminal Dogfooding Instructions](#internal-terminal-dogfooding-instructions)

```
https://go/terminal-dogfooding-instructions

Stripe! Thanks a ton for your help in dogfooding ahead of our Terminal GA launch!

We're very close to launching Terminal in public beta and then GA.

And we could use your help! There are a ton of different use cases of these integrations to test and polish, and we want to stress test what we've made and ship these paths and accompanying docs and dashboard flows in a developer-friendly as possible in the time we have before the Terminal GA launch.

If you're arriving at this doc after having signed up to dogfood, continue to Steps below.
If you haven't signed up yet, please signup here, and we'll get back to you when you have a slot your test.

Steps
1. If you're dogfooding remotely and haven't received instructions on ordering hardware or attending demos, please email terminal-dogfooding@stripe.com or ping in #terminal-dogfooding

2. If you're dogfooding the iOS or Android SDK, you'll need to set up your environment as described in the links...
```

## [ Conclusion](#conclusion)

This document has outlined a sophisticated approach to multimodal video search, combining spoken word indexing with scene-based visual analysis. By leveraging VideoDB's powerful indexing and search capabilities, we've created a pipeline that can find specific visual content (in this case, slide information) based on spoken queries. This technique has broad applications beyond just searching for slides in speeches. It could be adapted for various use cases where visual information needs to be retrieved based on audio content, such as:

- Finding product demonstrations in long-form video content
- Identifying key moments in educational videos
- Searching for specific visual elements in recorded meetings or presentations

As video content continues to grow in importance and volume, tools and techniques like these will become increasingly valuable for efficient information retrieval and analysis.

## [ Further Resources](#further-resources)

To learn more about Scene Index, explore the following guides:

## Scene Index Quickstart

Step-by-step introduction to Scene Index for quick setup and primary functions.

## Scene Extraction Options

Deep dive into various options for scene extraction, advanced settings, and optimization.

## Advanced Visual Search

Advanced techniques for visual content retrieval and complex search scenarios.

## Custom Annotation Pipelines

Build custom annotation pipelines for specialized video analysis workflows.

## [ Get Support](#get-support)

If you have any questions or feedback, feel free to reach out to us:

## Discord Community

Connect with the VideoDB community for support and discussions

## GitHub

Explore our open source projects and contribute

## VideoDB

Visit our main website for more information

[Case Study: NFL Game Analysis](\examples-and-tutorials\video-rag\case-study-nfl) [Overview](\examples-and-tutorials\live-intelligence)

⌘ I