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
- [Workflow](#workflow)
- [Setup](#setup)
    - [Installing VideoDB in your environment](#installing-videodb-in-your-environment)
    - [Setting Up a connection](#setting-up-a-connection)
- [Timeline Data](#timeline-data)
- [Creating instant clips using VideoDB](#creating-instant-clips-using-videodb)
- [Results](#results)
- [Related Tutorials](#related-tutorials)

[Video Search and Understanding](\examples-and-tutorials\video-rag\index)

# Character Extraction

Copy page

Extract clips featuring specific people or characters

Copy page

Open In Colab

<!-- image -->

## [ Overview](#overview)

We all have our favorite characters in TV shows that we love. What if you could create the clips of the scenes when they appear? You can use it in your content creation, analysis workflow or simply observe how they talk, dress or act in an episode. **VideoDB** is the database for your AI applications and enables it with ease. No need for fancy editing software or waiting around - you get to view your video right away. ⚡️

Face recognition and character extraction example using AWS Rekognition

<!-- image -->

## [ Workflow](#workflow)

Here's a [15-minute video](https://www.youtube.com/watch?v=NNAgJ5p4CIY) from HBO's Silicon Valley show. We've already identified instances when `Gilfoyle` , `Jian Yang` , `Erlich` , `Jared` , `Dinesh` and `Richard` make appearances with the help of [AWS Rekognition API](https://docs.aws.amazon.com/rekognition/) . We've pinpointed the timestamps of the characters' appearances in the video and mapped out where they appear in `persons_data` Next, we'll upload the video to VideoDB and use these timestamps to clip the video. It's as easy as querying a database⚡️

## [ Setup](#setup)

### [ Installing VideoDB in your environment](#installing-videodb-in-your-environment)

`VideoDB` is available as a [python package](https://pypi.org/project/videodb) and [npm package](https://www.npmjs.com/package/videodb)

Python

Node.js

```
! pip install videodb
```

```
npm install videodb
```

### [](#)

### [ Setting Up a connection](#setting-up-a-connection)

To connect to **VideoDB** , simply create a `Connection` object. This can be done by either providing your VideoDB API key directly to the constructor or by setting the `VIDEO_DB_API_KEY` environment variable with your API key. Get your API key from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) . ( Free for first 50 uploads, No credit card required)

Python

Node.js

```
from videodb import connect
conn = connect( api_key = "YOUR_API_KEY" )
```

```
import { connect } from 'videodb' ;

const conn = await connect ({ apiKey: process . env . VIDEO_DB_API_KEY });
```

## [ Timeline Data](#timeline-data)

Here's the json we compiled with the timestamps of appearances of each character. The **persons\_data** contains **timeline** for each character, representing the timestamps of shots when they were present in the video.

```
persons_data = {
"gilfoyle" : {
"timeline" : [[ 0 , 4 ], [ 160 , 185 ], [ 330 , 347 ], [ 370 , 378 ], [ 382 , 391 ], [ 391 , 400 ]]
},
"jianyang" : {
"timeline" : [[ 232 , 271 ], [ 271 , 283 ], [ 284 , 308 ], [ 312 , 343 ], [ 398 , 407 ]]
},
"erlich" : {
"timeline" : [[ 0 , 8 ], [ 12 , 30 ], [ 31 , 41 ], [ 44 , 52 ], [ 56 , 97 ], [ 97 , 124 ], [ 147 , 165 ], [ 185 , 309 ], [ 316 , 336 ], [ 336 , 345 ], [ 348 , 398 ], [ 398 , 408 ]]
},
"jarad" : {
"timeline" : [[ 0 , 15 ], [ 148 , 165 ], [ 182 , 190 ], [ 343 , 355 ], [ 358 , 381 ], [ 384 , 393 ]]
},
"dinesh" : {
"timeline" : [[ 0 , 4 ], [ 160 , 189 ], [ 343 , 354 ], [ 374 , 383 ], [ 392 , 402 ]]
},
"richard" : {
"timeline" : [[ 12 , 41 ], [ 127 , 137 ], [ 137 , 154 ], [ 159 , 167 ], [ 360 , 378 ], [ 381 , 398 ], [ 399 , 407 ]]
}
}
```

## [ Creating instant clips using VideoDB](#creating-instant-clips-using-videodb)

The idea behind `VideoDB` is straightforward: it functions as a database specifically for videos. Similar to uploading tables or JSON data to a standard database, you can upload your videos to VideoDB. You can also retrieve your videos through queries, much like accessing regular data from a database. You can pass timeline of each person in `video.generate_stream()` and get the streaming link almost instantly.

Python

Node.js

```
v_url = "https://www.youtube.com/watch?v=NNAgJ5p4CIY"
coll = conn.get_collection()
video = coll.upload( url = v_url)

# store stream of each person
for person in persons_data:
person_data = persons_data[person]
stream_link = video.generate_stream( timeline = person_data[ "timeline" ])
person_data[ "clip" ] = stream_link
```

```
const vUrl = "https://www.youtube.com/watch?v=NNAgJ5p4CIY" ;
const coll = await conn . getCollection ();
const video = await coll . uploadURL ({ url: vUrl });

// store stream of each person
for ( const person in personsData ) {
const personData = personsData [ person ];
const streamLink = await video . generateStream ({ timeline: personData . timeline });
personData . clip = streamLink ;
}
```

## [ Results](#results)

We effortlessly uploaded our video to VideoDB and generated clips for each character in just 30 seconds. Now, it's time to check out our results. Let's take a look at a clip featuring `Erlich Bachman` (feel free to choose your favorite character by changing the name field below)

Python

Node.js

```
from videodb import play_stream

name = "erlich"
play_stream(persons_data[name][ "clip" ])
```

```
const name = "erlich" ;
console . log ( personsData [ name ]. clip );
```

## Explore Full Notebook

Open the complete implementation in Google Colab with all code examples.

## [ Related Tutorials](#related-tutorials)

## Keyword Search

Create custom compilations by searching for spoken words

## Multimodal Search

Combine visual and spoken content for comprehensive queries

[Keyword Search](\examples-and-tutorials\video-rag\keyword-search) [Multimodal Search](\examples-and-tutorials\video-rag\multimodal-search)

⌘ I