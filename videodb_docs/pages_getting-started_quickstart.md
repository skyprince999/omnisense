### Start Here

- [Welcome to VideoDB](\)
- [Quickstart](\pages\getting-started\quickstart)
- SDK Installation
- [AI Agent Skills](\pages\getting-started\agent-skills)
- [Core Concepts in 5 Minutes](\pages\getting-started\core-concepts-in-5-min)

### Core Concepts

- [Core Concepts Overview](\pages\core-concepts\overview)
- [Data Model](\pages\core-concepts\data-model)
- [Indexes &amp; Search](\pages\core-concepts\indexes-and-search)
- [Events &amp; Real-time](\pages\core-concepts\events-and-realtime)
- [Programmable Editing](\pages\core-concepts\programmable-editing)
- [Security &amp; Privacy](\pages\core-concepts\security-privacy)

### Ingest

- Files and Collections
- Live Streams
- Capture SDKs
- Transcoding

### Understand

- Indexing Pipelines
- Search and Retrieval
- Quality and Evaluation

### Act

- Programmable Editing
- Live Action
- Generative Media
- Output and Delivery

### Automate

- [Integrations Overview](\pages\automate\integrations-overview)
- n8n Workflows
- Zapier Workflows

### Open Source Frameworks

- [MCP Server](\pages\build-with-agents\mcp-server)
- [LlamaIndex Retriever](\pages\community\open-source\llamaindex-retriever)
- Director Framework

## On this page

- [Get Your API Key](#get-your-api-key)
- [Install the SDK or Skill](#install-the-sdk-or-skill)
- [Real-time Perception (Desktop Capture)](#real-time-perception-desktop-capture)
- [What You Get](#what-you-get)
- [Now, It's Your Turn](#now-it%E2%80%99s-your-turn)
- [Working with Video Files](#working-with-video-files)
    - [Upload a video](#upload-a-video)
    - [Update video metadata](#update-video-metadata)
    - [Index spoken words](#index-spoken-words)
    - [Search with natural language](#search-with-natural-language)
- [Index Visual Scenes](#index-visual-scenes)
- [Search Across Collections](#search-across-collections)
- [What's Next](#what%E2%80%99s-next)

[Start Here](\index)

# Quickstart

Copy page

Give your AI agent eyes and ears in 5 minutes

Copy page

Your agent can reason about text. Now give it the ability to perceive - screen, microphone, camera, and video files.

## [ Get Your API Key](#get-your-api-key)

1. Go to [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs)
2. Copy your API key (free tier: 50 uploads, no credit card)
3. Set it in your environment:

```
export VIDEODB_API_KEY = "your-api-key"
```

## [ Install the SDK or Skill](#install-the-sdk-or-skill)

Python

Node.js

```
pip install videodb
```

```
npm install videodb
```

For agents like Claude Code, Codex, or Cursor:

```
npx skills add video-db/skills
```

## [ Real-time Perception (Desktop Capture)](#real-time-perception-desktop-capture)

Stream what your agent sees and hears. Get structured context back in real-time.

Desktop capture currently supports **macOS** and **Windows** .

To help you understand desktop perception in under a minute, before you install the SDK, we've hosted a live desktop running our **OpenClaw** agent. Its screen and microphone are streaming into VideoDB, where we generate structured context in real time. Here's the live feed of that agent.

This is the same workflow you'll use with your own agents and your own desktop - real-time visual and audio context, out of the box.

## [ What You Get](#what-you-get)

Your backend receives AI-ready events in real-time:

```
{ "type" : "transcript" , "text" : "Let's schedule the meeting for Thursday" , "is_final" : true }
```

```
{ "type" : "index" , "index_type" : "visual" , "text" : "User is viewing a Slack conversation with 3 unread messages" }
```

```
{ "type" : "index" , "index_type" : "audio" , "text" : "Discussion about scheduling a team meeting" }
```

```
{ "type" : "alert" , "label" : "sensitive_content" , "triggered" : true , "confidence" : 0.92 }
```

## [ Now, It's Your Turn](#now-it’s-your-turn)

Use the code below to connect to our OpenClaw's live visual and audio feeds, get real-time context, define events, and create alerts. You'll receive transcript updates and structured screen context in your WebSocket listener, plus you can attach event rules for alerts.

Python

Node.js

```
import asyncio
import signal
import videodb
from dotenv import load_dotenv

load_dotenv()

AUDIO_URL = "rtsp://matrix.videodb.io:8554/audio"
SCREEN_URL = "rtsp://matrix.videodb.io:8554/screen"


async def main ():
conn = videodb.connect()
coll = conn.get_collection()
print ( f "connected to collection: { coll.id } " )

ws = conn.connect_websocket()
ws = await ws.connect()

# Connect streams
audio = coll.connect_rtstream( url = AUDIO_URL , name = "Audio" , media_types = [ "audio" ])
screen = coll.connect_rtstream( url = SCREEN_URL , name = "Screen" , media_types = [ "video" ])
print ( f "audio stream: { audio.id } ( { audio.status } )" )
print ( f "screen stream: { screen.id } ( { screen.status } )" )

# Start pipelines
audio.start_transcript( ws_connection_id = ws.connection_id)
print ( "transcript started" )

audio.index_audio(
prompt = "Summarize what is being said or heard." ,
batch_config = { "type" : "time" , "value" : 30 },
ws_connection_id = ws.connection_id,
)
print ( "audio indexing started (30s window)" )

screen.index_visuals(
prompt = "In one sentence, describe the active application and what the agent is doing on screen. Note the current time if a clock is visible." ,
batch_config = { "type" : "time" , "value" : 30 , "frame_count" : 5 },
ws_connection_id = ws.connection_id,
)
print ( "visual indexing started (30s window, 5 frames)" )

# Listen for events - Ctrl+C to stop
print ( " \n listening for events... \n " )
stop = asyncio.Event()
for sig in (signal. SIGINT , signal. SIGTERM ):
asyncio.get_event_loop().add_signal_handler(sig, stop.set)

async def listen ():
async for msg in ws.receive():
ch = msg.get( "channel" , "?" )
if ch == "capture_session" :
continue
data = msg.get( "data" , msg)
if ch == "transcript" and not data.get( "is_final" , False ):
continue
text = data.get( "text" , "" ) if isinstance (data, dict ) else ""
print ( f "  [ { ch } ] { text } " )

task = asyncio.create_task(listen())
await asyncio.wait([task, asyncio.create_task(stop.wait())], return_when = asyncio. FIRST_COMPLETED )
task.cancel()

# Cleanup
print ( " \n stopping streams..." )
audio.stop()
screen.stop()
await ws.close()
print ( "done." )


if __name__ == "__main__" :
asyncio.run(main())
```

```
const videodb = require ( "videodb" );

const AUDIO_URL = "rtsp://matrix.videodb.io:8554/audio" ;
const SCREEN_URL = "rtsp://matrix.videodb.io:8554/screen" ;

async function main () {
const conn = videodb . connect ();
const coll = await conn . getCollection ();
console . log ( `connected to collection: ${ coll . id } ` );

const ws = await conn . connectWebsocket ();
await ws . connect ();
console . log ( `websocket connected: ${ ws . connectionId } ` );

// Connect streams
// Python media_types=["audio"] → audio=true, video=false
const audio = await coll . connectRTStream (
AUDIO_URL ,
"Audio" ,
undefined , // sampleRate
false , // video
true // audio
);
// Python media_types=["video"] → video=true, audio=false
const screen = await coll . connectRTStream (
SCREEN_URL ,
"Screen" ,
undefined , // sampleRate
true , // video
false // audio
);
console . log ( `audio stream: ${ audio . id } ( ${ audio . status } )` );
console . log ( `screen stream: ${ screen . id } ( ${ screen . status } )` );

// Start pipelines
await audio . startTranscript ( ws . connectionId );
console . log ( "transcript started" );

await audio . indexAudio ({
prompt: "Summarize what is being said or heard." ,
batchConfig: { type: "time" , value: 30 },
socketId: ws . connectionId ,
});
console . log ( "audio indexing started (30s window)" );

await screen . indexVisuals ({
prompt:
"In one sentence, describe the active application and what the agent is doing on screen. Note the current time if a clock is visible." ,
batchConfig: { type: "time" , value: 30 , frameCount: 5 },
socketId: ws . connectionId ,
});
console . log ( "visual indexing started (30s window, 5 frames)" );

// Listen for events - Ctrl+C to stop
console . log ( " \n listening for events... \n " );

let stopping = false ;

const onSignal = async () => {
if ( stopping ) return ;
stopping = true ;
console . log ( " \n stopping streams..." );
await audio . stop ();
await screen . stop ();
await ws . close ();
console . log ( "done." );
process . exit ( 0 );
};

process . on ( "SIGINT" , onSignal );
process . on ( "SIGTERM" , onSignal );

for await ( const msg of ws . receive ()) {
if ( stopping ) break ;

const ch = msg . channel || "?" ;
if ( ch === "capture_session" ) continue ;

const data = msg . data || msg ;
if ( ch === "transcript" && ! data . is_final ) continue ;

const text =
data && typeof data === "object" ? data . text || "" : "" ;
console . log ( `  [ ${ ch } ] ${ text } ` );
}
}

main (). catch (( err ) => {
console . error ( err );
process . exit ( 1 );
});
```

Try the interactive quickstart: [Real-time Perception Quickstart on GitHub](https://github.com/video-db/openclaw-monitoring/blob/main/try_without_setup.py)

## Full Capture Guide

Deep dive: channels, permissions, client code, and event handling

## [ Working with Video Files](#working-with-video-files)

Upload, index, and search existing recordings.

### [ Upload a video](#upload-a-video)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()
video = coll.upload( url = "https://www.youtube.com/watch?v=WDv4AWk0J3U" )

# Get an embeddable stream URL
stream_url = video.generate_stream()
print (stream_url) # HLS link you can embed anywhere
```

```
import { connect } from 'videodb' ;

const conn = connect ();
const video = await conn . uploadURL ( "default" , {
url: "https://www.youtube.com/watch?v=WDv4AWk0J3U"
});

// Get an embeddable stream URL
const streamUrl = await video . generateStream ();
console . log ( streamUrl ); // HLS link you can embed anywhere
```

Upload from YouTube, S3, any public URL, or local files.

### [ Update video metadata](#update-video-metadata)

Python

Node.js

```
video.update( name = "New Video Title" )
```

```
await video . update ({ name: "New Video Title" });
```

### [ Index spoken words](#index-spoken-words)

Create a searchable transcript:

Python

Node.js

```
video.index_audio( prompt = "Extract key topics, decisions, and action items" )
```

```
await video . indexAudio ({ prompt: "Extract key topics, decisions, and action items" });
```

### [ Search with natural language](#search-with-natural-language)

Python

Node.js

```
results = video.search( "What are the key benefits?" )

for shot in results.shots:
print ( f " { shot.start } s - { shot.end } s: { shot.text } " )

# Play the matching moments
results.play()
```

```
const results = await video . search ( "What are the key benefits?" );

for ( const shot of results . shots ) {
console . log ( ` ${ shot . start } s - ${ shot . end } s: ${ shot . text } ` );
}

// Play the matching moments
await results . play ();
```

Search returns timestamps and playable links - verifiable evidence your agent can use.

## [ Index Visual Scenes](#index-visual-scenes)

For video where visuals matter (security footage, tutorials, presentations):

Python

Node.js

```
# Index with a prompt describing what to look for
video.index_visuals( prompt = "Identify key moments and activities" )

# Search visual content
results = video.search( "person entering the room" , index_type = "scene" )
results.play()
```

```
// Index with a prompt describing what to look for
await video . indexVisuals ({ prompt: "Identify key moments and activities" });

// Search visual content
const results = await video . search ( "person entering the room" , { indexType: "scene" });
await results . play ();
```

## [ Search Across Collections](#search-across-collections)

Scale to thousands of videos:

Python

Node.js

```
# Get your collection
coll = conn.get_collection()

# Upload multiple videos
coll.upload( url = "https://youtube.com/watch?v=video1" )
coll.upload( url = "https://youtube.com/watch?v=video2" )
coll.upload( url = "https://youtube.com/watch?v=video3" )

# Index all
for video in coll.get_videos():
video.indexAudio()

# Search across everything
results = coll.search( "quarterly revenue discussion" )
results.play() # Plays matching moments from any video
```

```
// Get your collection
const coll = await conn . getCollection ();

// Upload multiple videos
await coll . uploadURL ({ url: "https://youtube.com/watch?v=video1" });
await coll . uploadURL ({ url: "https://youtube.com/watch?v=video2" });
await coll . uploadURL ({ url: "https://youtube.com/watch?v=video3" });

// Index all
const videos = await coll . getVideos ();
for ( const video of videos ) {
await video . indexAudio ();
}

// Search across everything
const results = await coll . search ( "quarterly revenue discussion" );
await results . play (); // Plays matching moments from any video
```

## [ What's Next](#what’s-next)

## Core Concepts in 5 Min

The mental model: See → Understand → Act

## Ingesting Files

Upload videos, audio, and images from URLs or local files

## RTSP Ingest

Connect live camera streams and feeds

## Create an Index

Make your media searchable with indexes

[Welcome to VideoDB](\) [Python SDK](\pages\getting-started\python)

⌘ I