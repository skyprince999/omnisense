### Start Here

- [Welcome to VideoDB](\)
- [Quickstart](\pages\getting-started\quickstart)
- SDK Installation
    - [Python SDK](\pages\getting-started\python)
    - [Node.js SDK](\pages\getting-started\node)
    - [Node.js SDK v0.2.0 Migration](\pages\getting-started\node-migration)
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

- [What Changed](#what-changed)
- [Breaking Change 1: Direct Property Access](#breaking-change-1-direct-property-access)
    - [Video](#video)
    - [Audio](#audio)
    - [Image](#image)
    - [Collection](#collection)
    - [Shot (Search Results)](#shot-search-results)
- [Breaking Change 2: Async/Await Pattern](#breaking-change-2-async%2Fawait-pattern)
    - [Getting Transcripts](#getting-transcripts)
    - [Indexing Spoken Words](#indexing-spoken-words)
    - [Uploading Media](#uploading-media)
    - [Error Handling](#error-handling)
- [Removed Exports](#removed-exports)
- [Migration Checklist](#migration-checklist)
    - [Property Access](#property-access)
    - [Job Pattern](#job-pattern)
- [Complete Example](#complete-example)
- [Need Help?](#need-help)

[Start Here](\index)

[SDK Installation](\pages\getting-started\python)

# Node.js SDK Migration

Copy page

Upgrade from v0.1.3 to v0.2.0: a cleaner API with direct property access and async/await

Copy page

If you're upgrading from v0.1.3, this guide walks you through the two breaking changes you need to address. The migration is straightforward (mostly find-and-replace).

## [ What Changed](#what-changed)

| Pattern          | Before (v0.1.3)                     | After (v0.2.0)                               |
|------------------|-------------------------------------|----------------------------------------------|
| Property Access  | `video.meta.id`                     | `video.id`                                   |
| Async Operations | `waitForJob(video.getTranscript())` | `await video.getTranscript()`                |
| Uploads          | Returns `UploadJob`                 | Returns `Video` / `Audio` / `Image` directly |
| Error Handling   | `.on('error', callback)`            | Standard `try/catch`                         |

## [ Breaking Change 1: Direct Property Access](#breaking-change-1-direct-property-access)

In v0.1.3, all properties were wrapped in a `.meta` object. In v0.2.0, properties are accessed directly on the instance.

### [ Video](#video)

Before (v0.1.3)

After (v0.2.0)

```
const video = await collection . getVideo ( 'm-123' );

console . log ( video . meta . id ); // 'm-123'
console . log ( video . meta . name ); // 'My Video'
console . log ( video . meta . streamUrl ); // 'https://stream.videodb.io/...'
console . log ( video . meta . playerUrl ); // 'https://console.videodb.io/player?...'
console . log ( video . meta . length ); // 120.5
console . log ( video . meta . collectionId ); // 'c-123'

const url = `https://example.com/video/ ${ video . meta . id } ` ;
```

```
const video = await collection . getVideo ( 'm-123' );

console . log ( video . id ); // 'm-123'
console . log ( video . name ); // 'My Video'
console . log ( video . streamUrl ); // 'https://stream.videodb.io/...'
console . log ( video . playerUrl ); // 'https://console.videodb.io/player?...'
console . log ( video . length ); // 120.5
console . log ( video . collectionId ); // 'c-123'

const url = `https://example.com/video/ ${ video . id } ` ;
```

### [ Audio](#audio)

Before (v0.1.3)

After (v0.2.0)

```
const audio = await collection . getAudio ( 'a-123' );

console . log ( audio . meta . id ); // 'a-123'
console . log ( audio . meta . name ); // 'podcast.mp3'
console . log ( audio . meta . length ); // 3600.0
console . log ( audio . meta . collectionId ); // 'c-123'
```

```
const audio = await collection . getAudio ( 'a-123' );

console . log ( audio . id ); // 'a-123'
console . log ( audio . name ); // 'podcast.mp3'
console . log ( audio . length ); // 3600.0
console . log ( audio . collectionId ); // 'c-123'
```

### [ Image](#image)

Before (v0.1.3)

After (v0.2.0)

```
const image = await collection . getImage ( 'img-123' );

console . log ( image . meta . id ); // 'img-123'
console . log ( image . meta . name ); // 'thumbnail.png'
console . log ( image . meta . url ); // 'https://...'
console . log ( image . meta . collectionId ); // 'c-123'
```

```
const image = await collection . getImage ( 'img-123' );

console . log ( image . id ); // 'img-123'
console . log ( image . name ); // 'thumbnail.png'
console . log ( image . url ); // 'https://...'
console . log ( image . collectionId ); // 'c-123'
```

### [ Collection](#collection)

Before (v0.1.3)

After (v0.2.0)

```
const collection = await conn . getCollection ( 'c-123' );

console . log ( collection . meta . id ); // 'c-123'
console . log ( collection . meta . name ); // 'My Videos'
console . log ( collection . meta . description ); // 'Collection description'

const videos = await fetchVideos ( collection . meta . id );
```

```
const collection = await conn . getCollection ( 'c-123' );

console . log ( collection . id ); // 'c-123'
console . log ( collection . name ); // 'My Videos'
console . log ( collection . description ); // 'Collection description'

const videos = await fetchVideos ( collection . id );
```

### [ Shot (Search Results)](#shot-search-results)

Before (v0.1.3)

After (v0.2.0)

```
const results = await video . search ( 'hello world' );

for ( const shot of results . shots ) {
console . log ( shot . meta . videoId ); // 'm-123'
console . log ( shot . meta . start ); // 10.5
console . log ( shot . meta . end ); // 15.2
console . log ( shot . meta . text ); // 'hello world example'
console . log ( shot . meta . searchScore ); // 0.95
}
```

```
const results = await video . search ( 'hello world' );

for ( const shot of results . shots ) {
console . log ( shot . videoId ); // 'm-123'
console . log ( shot . start ); // 10.5
console . log ( shot . end ); // 15.2
console . log ( shot . text ); // 'hello world example'
console . log ( shot . searchScore ); // 0.95
}
```

**Migration shortcut:** Search your codebase for `.meta.` and replace with `.` for each class type.

## [ Breaking Change 2: Async/Await Pattern](#breaking-change-2-async\await-pattern)

In v0.1.3, long-running operations returned `Job` objects that required callback registration. In v0.2.0, these are standard async functions. The SDK handles polling internally, errors propagate through `try/catch` , and there's no risk of silent failures from unregistered error handlers.

### [ Getting Transcripts](#getting-transcripts)

Before (v0.1.3)

After (v0.2.0)

```
import { waitForJob } from 'videodb' ;

// Option 1: Using callbacks
const job = video . getTranscript ();

job . on ( 'success' , ( transcript ) => {
console . log ( 'Transcript:' , transcript );
});

job . on ( 'error' , ( err ) => {
console . error ( 'Failed:' , err );
});

await job . start ();

// Option 2: Using waitForJob helper
const transcript = await waitForJob ( video . getTranscript ( true ));
```

```
// No imports needed - async/await is built-in

// Just await the method directly
// SDK handles polling internally
const transcript = await video . getTranscript ();

// Success! Use the result immediately
console . log ( 'Transcript:' , transcript );

// Errors? Use standard try/catch (see Error Handling section)
```

### [ Indexing Spoken Words](#indexing-spoken-words)

Before (v0.1.3)

After (v0.2.0)

```
import { waitForJob } from 'videodb' ;

const indexJob = video . indexSpokenWords ();

indexJob . on ( 'success' , ( result ) => {
console . log ( 'Indexing complete:' , result . success );
});

indexJob . on ( 'error' , ( err ) => {
console . error ( 'Indexing failed:' , err );
});

await indexJob . start ();
```

```
// No imports needed

// Await the indexing operation directly
const result = await video . indexSpokenWords ();

// SDK polls until complete, then returns
console . log ( 'Indexing complete:' , result . success );
```

### [ Uploading Media](#uploading-media)

Before (v0.1.3)

After (v0.2.0)

```
import { waitForJob } from 'videodb' ;

const uploadJob = await collection . uploadFile ({
filePath: '/path/to/video.mp4' ,
name: 'My Video' ,
});

uploadJob . on ( 'success' , ( video ) => {
console . log ( 'Video ID:' , video . meta . id );
});

uploadJob . on ( 'error' , ( err ) => {
console . error ( 'Upload failed:' , err );
});

await uploadJob . start ();
```

```
// No imports needed

// Upload returns the Video object directly
const video = await collection . uploadFile ({
filePath: '/path/to/video.mp4' ,
name: 'My Video' ,
});

// Video is ready to use immediately
console . log ( 'Video ID:' , video . id );
```

### [ Error Handling](#error-handling)

Before (v0.1.3)

After (v0.2.0)

```
import { waitForJob } from 'videodb' ;

const job = video . getTranscript ();

job . on ( 'success' , ( transcript ) => {
console . log ( 'Got transcript:' , transcript );
});

job . on ( 'error' , ( err ) => {
// If you forget this handler, errors are silently logged
console . error ( 'Transcript failed:' , err );
notifyUser ( 'Could not generate transcript' );
});

await job . start ();
```

```
// No imports needed

// Standard try/catch - errors can't be silently ignored
try {
const transcript = await video . getTranscript ();
console . log ( 'Got transcript:' , transcript );
} catch ( err ) {
// Errors bubble up naturally
console . error ( 'Transcript failed:' , err );
notifyUser ( 'Could not generate transcript' );
}
```

## [ Removed Exports](#removed-exports)

The following exports no longer exist in v0.2.0:

```
// These imports will fail in v0.2.0
import {
Job , // REMOVED
TranscriptJob , // REMOVED
UploadJob , // REMOVED
IndexJob , // REMOVED
waitForJob , // REMOVED
} from "videodb" ;
```

If your code imports any of these, remove the imports and refactor to use `await` directly on the method calls.

## [ Migration Checklist](#migration-checklist)

### [ Property Access](#property-access)

1

Search for .meta. patterns

Use your IDE or grep to find all occurrences of `.meta.` in your codebase.

2

Replace with direct access

- `video.meta.*` → `video.*` - `audio.meta.*` → `audio.*` - `image.meta.*` → `image.*` - `collection.meta.*` → `collection.*` - `shot.meta.*` → `shot.*`

### [ Job Pattern](#job-pattern)

1

Remove Job imports

Delete imports for `Job` , `TranscriptJob` , `UploadJob` , `IndexJob` , `waitForJob`

2

Remove callback registrations

Delete `.on('success', ...)` and `.on('error', ...)` blocks

3

Remove .start() calls

Delete any `job.start()` or `await job.start()` calls

4

Add await to method calls

Change `const job = video.getTranscript()` to `const transcript = await         video.getTranscript()`

5

Update error handling

Wrap calls in `try/catch` instead of using `.on('error', ...)`

## [ Complete Example](#complete-example)

Before (v0.1.3)

After (v0.2.0)

```
import { connect , waitForJob } from 'videodb' ;

async function processVideo () {
const conn = connect ( process . env . VIDEO_DB_API_KEY );
const collection = await conn . getCollection ();

// Upload
const uploadJob = await collection . uploadFile ({
filePath: './video.mp4' ,
name: 'My Video' ,
});
const video = await waitForJob ( uploadJob );
console . log ( 'Uploaded:' , video . meta . id );

// Transcript
const transcriptJob = video . getTranscript ();
const transcript = await waitForJob ( transcriptJob );

// Index
const indexJob = video . indexSpokenWords ();
await waitForJob ( indexJob );

// Search
const results = await video . search ( 'keyword' );
for ( const shot of results . shots ) {
console . log ( ` ${ shot . meta . start } s: ${ shot . meta . text } ` );
}
}
```

```
import { connect } from 'videodb' ;

async function processVideo () {
const conn = connect ( process . env . VIDEO_DB_API_KEY );
const collection = await conn . getCollection ();

// Upload - returns Video directly
const video = await collection . uploadFile ({
filePath: './video.mp4' ,
name: 'My Video' ,
});
console . log ( 'Uploaded:' , video . id );

// Transcript - just await
const transcript = await video . getTranscript ();

// Index - just await
await video . indexSpokenWords ();

// Search
const results = await video . search ( 'keyword' );
for ( const shot of results . shots ) {
console . log ( ` ${ shot . start } s: ${ shot . text } ` );
}
}
```

## [ Need Help?](#need-help)

## GitHub Issues

Report bugs or ask questions

## Discord Community

Get help from the community

[Node.js SDK](\pages\getting-started\node) [AI Agent Skills](\pages\getting-started\agent-skills)

⌘ I