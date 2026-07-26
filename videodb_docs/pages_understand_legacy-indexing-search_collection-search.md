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
- [Supported Languages](\pages\core-concepts\supported-languages)
- [Sandbox Compute](\pages\core-concepts\sandbox-compute)
- [Sandbox Models](\pages\core-concepts\sandbox-models)
- [Events &amp; Real-time](\pages\core-concepts\events-and-realtime)
- [Programmable Editing](\pages\core-concepts\programmable-editing)
- [Security &amp; Privacy](\pages\core-concepts\security-privacy)

### Ingest

- Files and Collections
- Live Streams
- Capture SDKs
- Transcoding

### Understand

- Understanding &amp; Indexing Pipelines
- Search and Retrieval
- Legacy Indexing &amp; Search
    - [Indexes &amp; Search](\pages\understand\legacy-indexing-search\indexes-and-search)
    - [Create an Index](\pages\understand\legacy-indexing-search\create-an-index)
    - [Frame Processing Primitives](\pages\understand\legacy-indexing-search\multimodal-indexing)
    - [Multiple Indexes](\pages\understand\legacy-indexing-search\multiple-indexes)
    - [Natural Language Query](\pages\understand\legacy-indexing-search\natural-language-query)
    - [Timestamps, Clips, Streams](\pages\understand\legacy-indexing-search\timestamps-clips-streams)
    - [Collection Search](\pages\understand\legacy-indexing-search\collection-search)
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
- [Collection vs Video Search](#collection-vs-video-search)
- [Search All Videos](#search-all-videos)
    - [Spoken Content](#spoken-content)
    - [Visual Content](#visual-content)
- [Metadata Filtering](#metadata-filtering)
    - [Index with Metadata](#index-with-metadata)
    - [Search with Filters](#search-with-filters)
    - [Metadata Guidelines](#metadata-guidelines)
- [Scene-Level Metadata](#scene-level-metadata)
- [Use Cases](#use-cases)
    - [Media Archive](#media-archive)
    - [Training Library](#training-library)
    - [Surveillance](#surveillance)
- [Performance Considerations](#performance-considerations)
    - [Index Before Searching](#index-before-searching)
    - [Use Metadata Filters](#use-metadata-filters)
- [Search Examples](#search-examples)
- [Next Steps](#next-steps)

[Understand](\pages\understand\indexing-pipelines\understanding-artifacts)

[Legacy Indexing &amp; Search](\pages\understand\legacy-indexing-search\indexes-and-search)

# Collection Search

Copy page

Search across your entire video library with a single query

Copy page

Search across all videos in a collection with a single query. Apply metadata filters to narrow results.

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()

# Search entire collection
results = coll.search( "product announcement" )

for shot in results.get_shots():
print ( f "Video: { shot.video_id } " )
print ( f "Time: { shot.start } s - { shot.end } s" )
print ( f "Content: { shot.text } " )
```

```
import { connect } from 'videodb' ;

const conn = connect ();
const coll = await conn . getCollection ();

// Search entire collection
const results = await coll . search ( "product announcement" );

for ( const shot of results . shots ) {
console . log ( `Video: ${ shot . videoId } ` );
console . log ( `Time: ${ shot . start } s - ${ shot . end } s` );
console . log ( `Content: ${ shot . text } ` );
}
```

## [ Collection vs Video Search](#collection-vs-video-search)

| Scope          | Method           | Use Case                         |
|----------------|------------------|----------------------------------|
| Single video   | `video.search()` | Find moments in a specific video |
| Entire library | `coll.search()`  | Find content across all videos   |

## [ Search All Videos](#search-all-videos)

### [ Spoken Content](#spoken-content)

Python

Node.js

```
# Search spoken content across all videos
results = coll.search( "discusses artificial intelligence" )

# Results include video IDs
for shot in results.get_shots():
print ( f "Found in video { shot.video_id } at { shot.start } s" )
```

```
// Search spoken content across all videos
const results = await coll . search ( "discusses artificial intelligence" );

// Results include video IDs
for ( const shot of results . shots ) {
console . log ( `Found in video ${ shot . videoId } at ${ shot . start } s` );
}
```

### [ Visual Content](#visual-content)

Python

Node.js

```
from videodb import IndexType

# Search scene indexes across collection
results = coll.search(
query = "person speaking at podium" ,
index_type = IndexType.scene
)
```

```
import { IndexTypeValues , SearchTypeValues } from 'videodb' ;

// Search scene indexes across collection
const results = await coll . search (
"person speaking at podium" ,
SearchTypeValues . semantic ,
IndexTypeValues . scene
);
```

## [ Metadata Filtering](#metadata-filtering)

Narrow search to specific categories using metadata filters.

### [ Index with Metadata](#index-with-metadata)

Python

Node.js

```
from videodb import SceneExtractionType

# Add metadata during indexing
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 30 },
prompt = "Describe the scene" ,
metadata = { "category" : "news" , "topic" : "technology" }
)
```

```
// Add metadata during indexing
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 30 },
prompt: "Describe the scene" ,
metadata: { category: "news" , topic: "technology" }
});
```

### [ Search with Filters](#search-with-filters)

Python

Node.js

```
from videodb import IndexType

# Filter by metadata
results = coll.search(
query = "product launch" ,
filter = [{ "category" : "news" }],
index_type = IndexType.scene
)

# Multiple filters (AND logic)
results = coll.search(
query = "keynote speech" ,
filter = [
{ "category" : "conference" },
{ "year" : "2024" }
],
index_type = IndexType.scene
)
```

```
import { IndexTypeValues , SearchTypeValues } from 'videodb' ;

// Filter by metadata
const results = await coll . search (
"product launch" ,
SearchTypeValues . semantic ,
IndexTypeValues . scene ,
[{ category: "news" }]
);

// Multiple filters (AND logic)
const results = await coll . search (
"keynote speech" ,
SearchTypeValues . semantic ,
IndexTypeValues . scene ,
[
{ category: "conference" },
{ year: "2024" }
]
);
```

### [ Metadata Guidelines](#metadata-guidelines)

| Rule                | Limit         |
|---------------------|---------------|
| Max key-value pairs | 5             |
| Max key length      | 20 characters |
| Max value length    | 20 characters |
| Value types         | string or int |

## [ Scene-Level Metadata](#scene-level-metadata)

Tag individual scenes for fine-grained filtering.

Python

Node.js

```
from videodb.scene import Scene

# Create scenes with metadata
scenes = [
Scene(
video_id = video.id,
start = 0 ,
end = 60 ,
description = "Opening segment with logo" ,
metadata = { "segment_type" : "intro" }
),
Scene(
video_id = video.id,
start = 60 ,
end = 300 ,
description = "Main presentation content" ,
metadata = { "segment_type" : "content" }
),
Scene(
video_id = video.id,
start = 300 ,
end = 360 ,
description = "Q&A session" ,
metadata = { "segment_type" : "qa" }
)
]

# Index with scene-level metadata
video.index_scenes( scenes = scenes, name = "segmented_index" )

# Search only Q&A segments
results = video.search(
query = "questions about pricing" ,
filter = [{ "segment_type" : "qa" }],
index_type = IndexType.scene
)
```

```
import { Scene } from 'videodb' ;

// Create scenes with metadata
const scenes = [
new Scene ({
videoId: video . id ,
start: 0 ,
end: 60 ,
description: "Opening segment with logo" ,
metadata: { segment_type: "intro" }
}),
new Scene ({
videoId: video . id ,
start: 60 ,
end: 300 ,
description: "Main presentation content" ,
metadata: { segment_type: "content" }
}),
new Scene ({
videoId: video . id ,
start: 300 ,
end: 360 ,
description: "Q&A session" ,
metadata: { segment_type: "qa" }
})
];

// Index with scene-level metadata
await video . indexScenes ({ scenes , name: "segmented_index" });

// Search only Q&A segments
const results = await video . search (
"questions about pricing" ,
SearchTypeValues . semantic ,
IndexTypeValues . scene ,
[{ segment_type: "qa" }]
);
```

## [ Use Cases](#use-cases)

### [ Media Archive](#media-archive)

```
# Tag videos by topic
for video in news_videos:
video.index_scenes(
prompt = "Describe the news segment" ,
metadata = { "channel" : "CNN" , "category" : "politics" }
)

# Search political news only
results = coll.search(
query = "election coverage" ,
filter = [{ "category" : "politics" }],
index_type = IndexType.scene
)
```

### [ Training Library](#training-library)

```
# Tag by skill level
beginner_videos.index_scenes(
prompt = "Describe the tutorial content" ,
metadata = { "level" : "beginner" , "topic" : "python" }
)

# Find beginner Python content
results = coll.search(
query = "how to define a function" ,
filter = [{ "level" : "beginner" }, { "topic" : "python" }],
index_type = IndexType.scene
)
```

### [ Surveillance](#surveillance)

```
# Tag by camera location
camera_footage.index_scenes(
prompt = "Identify people and vehicles" ,
metadata = { "location" : "entrance" , "camera_id" : "cam_01" }
)

# Search specific camera
results = coll.search(
query = "person in red jacket" ,
filter = [{ "location" : "entrance" }],
index_type = IndexType.scene
)
```

## [ Performance Considerations](#performance-considerations)

### [ Index Before Searching](#index-before-searching)

Collection search only finds content that has been indexed:

Python

Node.js

```
# Index all videos first
for video in coll.get_videos():
video.index_spoken_words()
video.index_scenes( prompt = "Describe the scene" )

# Now search across all
results = coll.search( "quarterly results" )
```

```
// Index all videos first
const videos = await coll . getVideos ();
for ( const video of videos ) {
await video . indexSpokenWords ();
await video . indexScenes ({ prompt: "Describe the scene" });
}

// Now search across all
const results = await coll . search ( "quarterly results" );
```

### [ Use Metadata Filters](#use-metadata-filters)

Filters reduce the search space and improve speed:

```
# Fast: filtered search
results = coll.search(
query = "product demo" ,
filter = [{ "category" : "marketing" }]
)

# Slower: unfiltered search across everything
results = coll.search( "product demo" )
```

## [ Search Examples](#search-examples)

Explore practical search implementations:

## Character Clips

Extract specific characters or people from video collections

## Multimodal Search

Combine text, visual, and audio search for powerful results

## [ Next Steps](#next-steps)

## Accuracy Tips

Improve search precision and recall

## Latency and Cost

Optimize for speed and efficiency

[Timestamps, Clips, Streams](\pages\understand\legacy-indexing-search\timestamps-clips-streams) [Accuracy Tips](\pages\understand\quality-and-evaluation\accuracy-tips)

⌘ I