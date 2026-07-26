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
    - [Capture SDK Overview](\pages\ingest\capture-sdks\overview)
    - [Real-time Context](\pages\ingest\capture-sdks\realtime-context)
    - [Storage &amp; Search](\pages\ingest\capture-sdks\storage-and-search)
    - [Privacy Controls](\pages\ingest\capture-sdks\privacy-controls)
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

- [1. Backend Setup](#1-backend-setup)
    - [Install](#install)
    - [Create a Capture Session](#create-a-capture-session)
- [2. Client Setup](#2-client-setup)
    - [Install](#install-2)
    - [Start Capture](#start-capture)
- [3. Backend Starts AI](#3-backend-starts-ai)
- [4. What You Get](#4-what-you-get)
    - [Architecture](#architecture)
    - [Two Runtimes](#two-runtimes)
- [5. Example Applications](#5-example-applications)
- [6. Core Concepts](#6-core-concepts)
    - [CaptureSession (cap-xxx)](#capturesession-cap-xxx)
    - [RTStream (rts-xxx)](#rtstream-rts-xxx)
    - [Channel](#channel)
    - [Multi-Screen Capture](#multi-screen-capture)
- [Explore More](#explore-more)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Capture SDKs](\pages\ingest\capture-sdks\overview)

# Capture SDK Overview

Copy page

Real-time desktop capture for AI agents - stream screen, microphone, and system audio

Copy page

Desktop capture currently supports **macOS** and **Windows** .

## [ 1. Backend Setup](#1-backend-setup)

### [ Install](#install)

```
pip install videodb
```

### [ Create a Capture Session](#create-a-capture-session)

Your backend creates a session and generates a short-lived token for the desktop client:

Python

Node.js

```
import videodb

conn = videodb.connect()

# Create session for a user
cap = conn.create_capture_session(
end_user_id = "user_abc" ,
callback_url = "https://your-backend.com/webhooks/videodb" ,
metadata = { "app" : "my-ai-copilot" }
)

# Generate token for desktop client (never share API key)
token = conn.generate_client_token( expires_in = 600 )

# Send session ID and token to desktop client
print ( f "Session: { cap.id } , Token: { token } " )
```

```
import { connect } from 'videodb' ;

const conn = connect ();

// Create session for a user
const cap = await conn . createCaptureSession ({
endUserId: "user_abc" ,
callbackUrl: "https://your-backend.com/webhooks/videodb" ,
metadata: { app: "my-ai-copilot" }
});

// Generate token for desktop client (never share API key)
const token = await conn . generateClientToken ( 600 );

// Send session ID and token to desktop client
console . log ( `Session: ${ cap . id } , Token: ${ token } ` );
```

## [ 2. Client Setup](#2-client-setup)

### [ Install](#install-2)

```
pip install "videodb[capture]"
```

### [ Start Capture](#start-capture)

The desktop client uses the token to stream screen and audio:

Python

Node.js

```
import asyncio
from videodb.capture import CaptureClient

async def capture ( capture_session_id : str , client_token : str ):
client = CaptureClient( client_token = client_token)

# Request permissions
await client.request_permission( "microphone" )
await client.request_permission( "screen_capture" )

# Discover available sources
channels = await client.list_channels()
mic = channels.mics.default
display = channels.displays.primary or channels.displays[ 1 ]
system_audio = channels.system_audio.default
selected = [c for c in [mic, display, system_audio] if c]

# Start capture
await client.start_session(
capture_session_id = capture_session_id,
channels = selected,
primary_video_channel_id = display.name if display else None
)

# Listen for events
async for ev in client.events():
print ( f " { ev.event } : { ev.payload } " )
if ev.event in ( "recording-complete" , "error" ):
break

await client.stop_session()
await client.shutdown()

# Run the capture
if __name__ == "__main__" :
asyncio.run(capture(
capture_session_id = "cap-xxx" , # From backend
client_token = "token-xxx" # From backend
))
```

```
import { CaptureClient } from 'videodb/capture' ;

async function capture ( captureSessionId , clientToken ) {
const client = new CaptureClient ({ sessionToken: clientToken });

// Request permissions
await client . requestPermission ( 'microphone' );
await client . requestPermission ( 'screen-capture' );

// Discover available sources
const channels = await client . listChannels ();
const mic = channels . find ( c => c . channelId === 'mic:default' );
const display = channels . find ( c => c . channelId === 'display:1' );
const systemAudio = channels . find ( c => c . channelId === 'system_audio:default' );

const selectedChannels = [ mic , display , systemAudio ]
. filter ( Boolean )
. map ( c => ({ channelId: c . channelId , type: c . type , record: true , store: true }));

// Start capture
await client . startCaptureSession ({
sessionId: captureSessionId ,
channels: selectedChannels
});

// Listen for events
client . on ( 'transcript' , ( data ) => console . log ( `Transcript: ${ data . text } ` ));
client . on ( 'recording:stopped' , () => client . shutdown ());
}

// Run the capture
capture (
"cap-xxx" , // From backend
"token-xxx" // From backend
);
```

## [ 3. Backend Starts AI](#3-backend-starts-ai)

When capture begins, your backend receives a webhook and starts AI processing:

Python

Node.js

```
def on_webhook ( payload : dict ):
if payload[ "event" ] == "capture_session.active" :
cap_id = payload[ "capture_session_id" ]
cap = conn.get_capture_session(cap_id)

# Get RTStreams (one per channel)
mics = cap.get_rtstream( "mic" )
displays = cap.get_rtstream( "display" )

# Start real-time AI processing
if mics:
mic = mics[ 0 ]
mic.start_transcript()
mic.index_audio( prompt = "Extract key decisions and action items" )

if displays:
display = displays[ 0 ]
display.index_visuals( prompt = "Describe what the user is doing" )
```

```
async function onWebhook ( payload ) {
if ( payload . event === "capture_session.active" ) {
const capId = payload . capture_session_id ;
const cap = await conn . getCaptureSession ( capId );

// Get RTStreams
const mics = cap . getRtstream ( "mics" );
const displays = cap . getRtstream ( "displays" );

// Start real-time AI processing
if ( mics ?. length > 0 ) {
const mic = mics [ 0 ];
await mic . startTranscript ();
await mic . indexAudio ({ prompt: "Extract key decisions and action items" });
}

if ( displays ?. length > 0 ) {
const display = displays [ 0 ];
await display . indexVisuals ({ prompt: "Describe what the user is doing" });
}
}
}
```

## [ 4. What You Get](#4-what-you-get)

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

**Build with these:**

- Screen-aware AI agents
- Live meeting copilots
- In-call assistance
- Semantic search and replay

### [ Architecture](#architecture)

Diagram showing the architecture of the system

<!-- image -->

1. **Backend** creates a CaptureSession and mints a short-lived token
2. **Desktop client** uses the token to stream screen + audio (never sees API key)
3. **VideoDB** creates RTStreams (one per channel) when capture starts
4. **Backend** receives webhook, starts transcript and indexing on RTStreams
5. **AI events** flow back via WebSocket (real-time) or can be polled

### [ Two Runtimes](#two-runtimes)

| Backend           | Desktop Client         |
|-------------------|------------------------|
| Holds API key     | Receives session token |
| Creates sessions  | Captures media         |
| Runs AI pipelines | Streams to VideoDB     |
| Receives events   | Emits local UX events  |

**Rule of thumb:** Webhooks for correctness (durable, at-least-once). WebSocket for live UI (best-effort).

## [ 5. Example Applications](#5-example-applications)

## Claude Pair Programmer

AI coding assistant with screen and audio context

## Bloom

Local-first screen recorder with AI indexing

## Focusd

AI-powered productivity tracking

## Call.md

Real-time meeting intelligence

## [ 6. Core Concepts](#6-core-concepts)

### [ CaptureSession (cap-xxx)](#capturesession-cap-xxx)

The lifecycle container for one capture run. Created by backend, activated by desktop client. **States:** `created → starting → active → stopping → stopped → exported`

### [ RTStream (rts-xxx)](#rtstream-rts-xxx)

A real-time media stream, one per captured channel. This is where you run AI:

Python

Node.js

```
rtstream.start_transcript()
rtstream.index_audio( prompt = "Extract key decisions" )
rtstream.index_visuals( prompt = "Describe what user is doing" )
rtstream.search( "budget discussion" )
```

```
await rtstream . startTranscript ();
await rtstream . indexAudio ({ prompt: "Extract key decisions" });
await rtstream . indexVisuals ({ prompt: "Describe what user is doing" });
await rtstream . search ({ query: "budget discussion" });
```

### [ Channel](#channel)

A recordable source on the desktop:

| Channel                   | Description         |
|---------------------------|---------------------|
| `mic:default`             | Default microphone  |
| `system_audio:default`    | System audio output |
| `display:1` , `display:2` | Connected displays  |

### [ Multi-Screen Capture](#multi-screen-capture)

When multiple monitors are connected, each appears as a separate `display:N` channel. Use `cap.displays` on the backend to inspect available video channels:

Python

```
cap = conn.get_capture_session( "cap-xxx" )

# List all video (display) channels
for d in cap.displays:
print ( f " { d.channel_id } primary= { d.is_primary } " )
# display:1  primary=True
# display:2  primary=False
```

`cap.displays` returns a list of video channel objects. Each object includes an `is_primary` field that indicates which display was set as the primary video channel when capture started (via `primary_video_channel_id` ). To capture multiple screens, pass all desired display channels to the desktop client:

Python

```
channels = await client.list_channels()

# Select both displays
display1 = channels.displays[ 1 ] # display:1
display2 = channels.displays[ 2 ] # display:2

await client.start_session(
capture_session_id = cap_id,
channels = [
mic,
display1,
display2,
system_audio,
],
primary_video_channel_id = display1.name,
)
```

Each display produces its own RTStream on the backend. The primary display is used for the default muxed export video; non-primary displays are available as raw channel assets or can be exported separately (see [Storage &amp; Search](\pages\ingest\capture-sdks\storage-and-search) ).

## [ Explore More](#explore-more)

## View All Examples on GitHub

Complete source code with quickstart guides, example apps, and implementation patterns

## Real-time Context

Events you receive from capture

## Storage &amp; Search

Optional persistence and semantic search

[Stream Lifecycle](\pages\ingest\live-streams\stream-lifecycle) [Real-time Context](\pages\ingest\capture-sdks\realtime-context)

⌘ I