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
    - [Upload Video](\pages\ingest\files-and-collections\upload-video)
    - [Create Collection](\pages\ingest\files-and-collections\create-collection)
    - [Collection Patterns](\pages\ingest\files-and-collections\collection-patterns)
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

- [When to Use This](#when-to-use-this)
- [Async Upload Pattern](#async-upload-pattern)
- [Webhook Handler](#webhook-handler)
    - [Callback Payloads](#callback-payloads)
- [Batch Upload with Tracking](#batch-upload-with-tracking)
- [Retry Pattern](#retry-pattern)
- [Indexing Callbacks](#indexing-callbacks)
- [Error Handling](#error-handling)
- [Next Steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Files and Collections](\pages\ingest\files-and-collections\upload-video)

# Collection Patterns

Copy page

Production-ready patterns for ingesting media at scale. Handle async operations, batch uploads, and error recovery.

Copy page

## [ When to Use This](#when-to-use-this)

- Uploading many files in a batch
- Building production pipelines
- Handling failures gracefully
- Processing webhook callbacks

## [ Async Upload Pattern](#async-upload-pattern)

For large files or many uploads, use callbacks instead of waiting:

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()

# Fire-and-forget uploads
for url in video_urls:
coll.upload(
url = url,
callback_url = "https://your-backend.com/webhooks/upload"
)
```

```
import { connect } from 'videodb' ;

const conn = await connect ();
const coll = await conn . getCollection ();

// Fire-and-forget uploads
for ( const url of videoUrls ) {
await coll . uploadURL ({
url ,
callbackUrl: "https://your-backend.com/webhooks/upload"
});
}
```

## [ Webhook Handler](#webhook-handler)

Handle upload callbacks in your backend:

Python

```
from fastapi import FastAPI, Request

app = FastAPI()

@app.post ( "/webhooks/upload" )
async def handle_upload ( request : Request):
event = await request.json()

if event[ "success" ]:
video_id = event[ "data" ][ "id" ]
# Trigger next step (indexing, processing, etc.)
await start_indexing(video_id)
else :
# Handle failure
await log_failure(event[ "message" ])

return { "status" : "ok" }
```

### [ Callback Payloads](#callback-payloads)

**Success:**

```
{
"success" : true ,
"data" : {
"id" : "m-xxx" ,
"collection_id" : "c-xxx" ,
"name" : "video.mp4" ,
"length" : "191.14" ,
"stream_url" : "https://stream.videodb.io/..." ,
"player_url" : "https://console.videodb.io/player?..."
}
}
```

**Failure:**

```
{
"success" : false ,
"message" : "Download failed."
}
```

## [ Batch Upload with Tracking](#batch-upload-with-tracking)

Track multiple uploads and wait for all to complete:

Python

Node.js

```
import asyncio
from collections import defaultdict

# Track pending uploads
pending = defaultdict(asyncio.Event)

async def upload_batch ( urls ):
for url in urls:
upload_id = generate_id()
pending[upload_id] = asyncio.Event()

coll.upload(
url = url,
callback_url = f "https://backend.com/webhooks?id= { upload_id } "
)

# Wait for all callbacks
await asyncio.gather( * [e.wait() for e in pending.values()])

# In webhook handler
@app.post ( "/webhooks" )
async def handle ( request : Request, id : str ):
event = await request.json()
if id in pending:
pending[ id ].set()
return { "status" : "ok" }
```

```
// Track pending uploads
const pending = new Map ();

async function uploadBatch ( urls ) {
const promises = urls . map ( async ( url ) => {
const uploadId = generateId ();

return new Promise (( resolve ) => {
pending . set ( uploadId , resolve );

coll . uploadURL ({
url ,
callbackUrl: `https://backend.com/webhooks?id= ${ uploadId } `
});
});
});

await Promise . all ( promises );
}

// In webhook handler
app . post ( "/webhooks" , ( req , res ) => {
const { id } = req . query ;
if ( pending . has ( id )) {
pending . get ( id )();
pending . delete ( id );
}
res . json ({ status: "ok" });
});
```

## [ Retry Pattern](#retry-pattern)

Handle transient failures with exponential backoff:

Python

Node.js

```
import time
from functools import wraps

def retry_upload ( max_attempts = 3 , base_delay = 1 ):
def decorator ( func ):
@wraps (func)
def wrapper ( * args , ** kwargs ):
for attempt in range (max_attempts):
try :
return func( * args, ** kwargs)
except Exception as e:
if attempt == max_attempts - 1 :
raise
delay = base_delay * ( 2 ** attempt)
time.sleep(delay)
return wrapper
return decorator

@retry_upload ( max_attempts = 3 )
def upload_with_retry ( coll , url ):
return coll.upload( url = url)
```

```
async function retryUpload ( coll , url , maxAttempts = 3 ) {
for ( let attempt = 0 ; attempt < maxAttempts ; attempt ++ ) {
try {
return await coll . uploadURL ({ url });
} catch ( e ) {
if ( attempt === maxAttempts - 1 ) throw e ;
const delay = 1000 * Math . pow ( 2 , attempt );
await new Promise ( r => setTimeout ( r , delay ));
}
}
}
```

## [ Indexing Callbacks](#indexing-callbacks)

Chain indexing after upload completes:

Python

Node.js

```
# Upload callback triggers indexing
@app.post ( "/webhooks/upload" )
async def handle_upload ( request : Request):
event = await request.json()

if event[ "success" ]:
video_id = event[ "data" ][ "id" ]
coll = conn.get_collection(event[ "data" ][ "collection_id" ])
video = coll.get_video(video_id)

# Trigger async indexing
video.index_spoken_words(
callback_url = "https://backend.com/webhooks/index"
)

return { "status" : "ok" }

# Index callback
@app.post ( "/webhooks/index" )
async def handle_index ( request : Request):
event = await request.json()

if event[ "success" ]:
# Video is now searchable
await notify_ready(event[ "data" ][ "id" ])

return { "status" : "ok" }
```

```
// Upload callback triggers indexing
app . post ( "/webhooks/upload" , async ( req , res ) => {
const event = req . body ;

if ( event . success ) {
const coll = await conn . getCollection ( event . data . collection_id );
const video = await coll . getVideo ( event . data . id );

// Trigger async indexing
await video . indexSpokenWords ({
callbackUrl: "https://backend.com/webhooks/index"
});
}

res . json ({ status: "ok" });
});

// Index callback
app . post ( "/webhooks/index" , async ( req , res ) => {
const event = req . body ;

if ( event . success ) {
// Video is now searchable
await notifyReady ( event . data . id );
}

res . json ({ status: "ok" });
});
```

## [ Error Handling](#error-handling)

Common error responses and how to handle them:

| Error                  | Cause                | Action                        |
|------------------------|----------------------|-------------------------------|
| `Download failed`      | URL inaccessible     | Verify URL, check permissions |
| `Invalid media type`   | Wrong MediaType enum | Match MediaType to file       |
| `Something went wrong` | Corrupted file       | Re-encode source file         |

## [ Next Steps](#next-steps)

## Upload Video

Upload methods reference

## Live Streams

Ingest from RTSP sources

[Create Collection](\pages\ingest\files-and-collections\create-collection) [RTSP Ingest](\pages\ingest\live-streams\rtsp-ingest)

⌘ I