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

- [Quick Example](#quick-example)
- [Collection Operations](#collection-operations)
    - [Create](#create)
    - [List All](#list-all)
    - [Get by ID](#get-by-id)
    - [Update](#update)
    - [Delete](#delete)
- [List Media in Collection](#list-media-in-collection)
- [Collection Search](#collection-search)
- [Public Collections](#public-collections)
    - [Create Public Collection](#create-public-collection)
    - [Toggle Visibility](#toggle-visibility)
    - [Access Public Collection](#access-public-collection)
- [What You Can Build](#what-you-can-build)
- [Next Steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Files and Collections](\pages\ingest\files-and-collections\upload-video)

# Create Collection

Copy page

Collections group your media for organization and scoped search. Think of them as folders that also enable searching across all videos within.

Copy page

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()

# Create a collection
coll = conn.create_collection(
name = "Q4 Meetings" ,
description = "All Q4 2024 team meetings"
)
print (coll.id) # c-xxx
```

```
import { connect } from 'videodb' ;

const conn = await connect ();

// Create a collection
const coll = await conn . createCollection (
"Q4 Meetings" ,
"All Q4 2024 team meetings"
);
console . log ( coll . id ); // c-xxx
```

## [ Collection Operations](#collection-operations)

### [ Create](#create)

Python

Node.js

```
coll = conn.create_collection(
name = "Security Footage" ,
description = "Warehouse camera feeds"
)
```

```
const coll = await conn . createCollection (
"Security Footage" ,
"Warehouse camera feeds"
);
```

### [ List All](#list-all)

Python

Node.js

```
collections = conn.get_collections()
for c in collections:
print ( f " { c.id } : { c.name } " )
```

```
const collections = await conn . getCollections ();
for ( const c of collections ) {
console . log ( ` ${ c . id } : ${ c . name } ` );
}
```

### [ Get by ID](#get-by-id)

Python

Node.js

```
coll = conn.get_collection( "c-xxx-xxx" )
```

```
const coll = await conn . getCollection ( "c-xxx-xxx" );
```

### [ Update](#update)

Python

Node.js

```
coll = conn.update_collection(
"c-xxx-xxx" ,
"New Name" ,
"Updated description"
)
```

```
const coll = await conn . updateCollection (
"c-xxx-xxx" ,
"New Name" ,
"Updated description"
);
```

### [ Delete](#delete)

Python

Node.js

```
coll.delete()
```

```
await coll . delete ();
```

## [ List Media in Collection](#list-media-in-collection)

Python

Node.js

```
# List videos
videos = coll.get_videos()
for v in videos:
print ( f " { v.id } : { v.name } " )

# List audios
audios = coll.get_audios()

# List images
images = coll.get_images()
```

```
// List videos
const videos = await coll . getVideos ();
for ( const v of videos ) {
console . log ( ` ${ v . id } : ${ v . name } ` );
}

// List audios
const audios = await coll . getAudios ();

// List images
const images = await coll . getImages ();
```

## [ Collection Search](#collection-search)

Search restricts results to videos in that collection - essential for RAG applications:

Python

Node.js

```
from videodb import SearchType

# Index videos first
video.index_spoken_words()

# Search within collection
results = coll.search( "quarterly results" , search_type = SearchType.semantic)
for shot in results.shots:
print ( f " { shot.start } s: { shot.text } " )
```

```
import { SearchTypeValues } from 'videodb' ;

// Index videos first
await video . indexSpokenWords ();

// Search within collection
const results = await coll . search ( "quarterly results" , SearchTypeValues . semantic );
for ( const shot of results . shots ) {
console . log ( ` ${ shot . start } s: ${ shot . text } ` );
}
```

## [ Public Collections](#public-collections)

Share collections publicly for read-only access. Anyone with the collection ID can access media and indexes.

### [ Create Public Collection](#create-public-collection)

Python

Node.js

```
public_coll = conn.create_collection(
name = "Demo Videos" ,
description = "Public demo collection" ,
is_public = True
)
```

```
const publicColl = await conn . createCollection (
"Demo Videos" ,
"Public demo collection" ,
true // isPublic
);
```

### [ Toggle Visibility](#toggle-visibility)

Python

Node.js

```
# Make private
coll.make_private()
print (coll.is_public) # False

# Make public
coll.make_public()
print (coll.is_public) # True
```

```
// Make private
await coll . makePrivate ();
console . log ( coll . isPublic ); // false

// Make public
await coll . makePublic ();
console . log ( coll . isPublic ); // true
```

### [ Access Public Collection](#access-public-collection)

Anyone can access with the collection ID:

Python

Node.js

```
# Access VideoDB's OCR Benchmark Collection
public_coll = conn.get_collection( "c-c0a2c223-e377-4625-94bf-910501c2a31c" )
videos = public_coll.get_videos()
```

```
// Access VideoDB's OCR Benchmark Collection
const publicColl = await conn . getCollection ( "c-c0a2c223-e377-4625-94bf-910501c2a31c" );
const videos = await publicColl . getVideos ();
```

## [ What You Can Build](#what-you-can-build)

## Keyword Search Compilation

Organize videos in collections and search across all of them

## Multimodal Search

Build searchable video libraries with text and visual queries

## Character Clips

Search collections to extract clips featuring specific people

## [ Next Steps](#next-steps)

## Upload Video

Add media to your collections

## Collection Patterns

Batching, retries, and production patterns

[Upload Video](\pages\ingest\files-and-collections\upload-video) [Collection Patterns](\pages\ingest\files-and-collections\collection-patterns)

⌘ I