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
    - [Accuracy Tips](\pages\understand\quality-and-evaluation\accuracy-tips)
    - [Latency and Cost](\pages\understand\quality-and-evaluation\latency-and-cost)

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

- [Quick Reference](#quick-reference)
- [Indexing Cost Factors](#indexing-cost-factors)
    - [Frame Count](#frame-count)
    - [Scene Interval](#scene-interval)
- [Indexing Latency](#indexing-latency)
    - [Time-Based vs Shot-Based](#time-based-vs-shot-based)
    - [Async Processing](#async-processing)
- [Search Latency](#search-latency)
    - [Single Video vs Collection](#single-video-vs-collection)
    - [Reduce Search Space](#reduce-search-space)
    - [Limit Results](#limit-results)
- [Optimization Strategies](#optimization-strategies)
    - [Tiered Indexing](#tiered-indexing)
    - [Index on Demand](#index-on-demand)
    - [Batch Processing](#batch-processing)
- [Cost Estimation](#cost-estimation)
    - [Factors](#factors)
    - [Example Calculations](#example-calculations)
- [Recommendations by Use Case](#recommendations-by-use-case)
    - [Media Archive (Cost-Sensitive)](#media-archive-cost-sensitive)
    - [Security Monitoring (Quality-First)](#security-monitoring-quality-first)
    - [E-commerce (Balanced)](#e-commerce-balanced)
- [Monitoring](#monitoring)
- [Next Steps](#next-steps)

[Understand](\pages\understand\indexing-pipelines\create-an-index)

[Quality and Evaluation](\pages\understand\quality-and-evaluation\accuracy-tips)

# Latency and Cost

Copy page

Trade-offs between indexing speed, search performance, and API costs

Copy page

Indexing and search have trade-offs between speed, quality, and cost. This guide helps you optimize for your priorities.

## [ Quick Reference](#quick-reference)

| Factor            | Lower Cost    | Higher Quality   |
|-------------------|---------------|------------------|
| Frame count       | 1 frame/scene | 3-5 frames/scene |
| Scene interval    | 30+ seconds   | 5-10 seconds     |
| Extraction type   | Time-based    | Shot-based       |
| Prompt complexity | Simple        | Detailed         |

## [ Indexing Cost Factors](#indexing-cost-factors)

### [ Frame Count](#frame-count)

More frames = more vision API calls = higher cost.

Python

Node.js

```
from videodb import SceneExtractionType

# Economical: 1 frame per scene
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 30 , "frame_count" : 1 },
prompt = "Describe the scene"
)

# Premium: 5 frames per scene
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 10 , "frame_count" : 5 },
prompt = "Describe the activity and how it progresses"
)
```

```
// Economical: 1 frame per scene
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 30 , frame_count: 1 },
prompt: "Describe the scene"
});

// Premium: 5 frames per scene
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 10 , frame_count: 5 },
prompt: "Describe the activity and how it progresses"
});
```

| Config        |   Scenes/hour |   Frames/hour | Relative Cost   |
|---------------|---------------|---------------|-----------------|
| 30s, 1 frame  |           120 |           120 | 1x              |
| 10s, 1 frame  |           360 |           360 | 3x              |
| 10s, 3 frames |           360 |         1,080 | 9x              |
| 5s, 5 frames  |           720 |         3,600 | 30x             |

### [ Scene Interval](#scene-interval)

Shorter intervals = more scenes = more processing.

Python

Node.js

```
# Long interval: fewer scenes, lower cost
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 60 }, # 1 scene per minute
prompt = "Describe the main topic"
)

# Short interval: more scenes, higher cost
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 5 }, # 12 scenes per minute
prompt = "Describe what's happening"
)
```

```
// Long interval: fewer scenes, lower cost
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 60 }, // 1 scene per minute
prompt: "Describe the main topic"
});

// Short interval: more scenes, higher cost
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 5 }, // 12 scenes per minute
prompt: "Describe what's happening"
});
```

## [ Indexing Latency](#indexing-latency)

### [ Time-Based vs Shot-Based](#time-based-vs-shot-based)

| Method     | Latency     | Best For          |
|------------|-------------|-------------------|
| Time-based | Predictable | Long-form content |
| Shot-based | Variable    | Edited content    |

Shot-based detection adds processing overhead but produces more natural boundaries.

### [ Async Processing](#async-processing)

For long videos, use callbacks to avoid blocking:

Python

Node.js

```
# Non-blocking with callback
scene_index_id = video.index_scenes(
prompt = "Describe the scene" ,
callback_url = "https://your-backend.com/webhooks/index-complete"
)

# Check status later
scene_index = video.get_scene_index(scene_index_id)
print (scene_index.status) # "processing" or "completed"
```

```
// Non-blocking with callback
const sceneIndexId = await video . indexScenes ({
prompt: "Describe the scene" ,
callbackUrl: "https://your-backend.com/webhooks/index-complete"
});

// Check status later
const sceneIndex = await video . getSceneIndex ( sceneIndexId );
console . log ( sceneIndex . status ); // "processing" or "completed"
```

## [ Search Latency](#search-latency)

### [ Single Video vs Collection](#single-video-vs-collection)

| Scope            | Latency   | Use Case    |
|------------------|-----------|-------------|
| `video.search()` | Faster    | Known video |
| `coll.search()`  | Slower    | Discovery   |

### [ Reduce Search Space](#reduce-search-space)

Metadata filters improve performance:

Python

Node.js

```
# Slower: search everything
results = coll.search( "product demo" )

# Faster: filtered search
results = coll.search(
query = "product demo" ,
filter = [{ "category" : "marketing" }]
)
```

```
import { IndexTypeValues , SearchTypeValues } from 'videodb' ;

// Slower: search everything
const results = await coll . search ( "product demo" );

// Faster: filtered search
const results = await coll . search (
"product demo" ,
SearchTypeValues . semantic ,
IndexTypeValues . scene ,
[{ category: "marketing" }]
);
```

### [ Limit Results](#limit-results)

Python

Node.js

```
# Return fewer results for faster response
results = video.search(
query = "highlights" ,
result_threshold = 5 # Only top 5
)
```

```
// Return fewer results for faster response
const results = await video . search (
"highlights" ,
SearchTypeValues . semantic ,
IndexTypeValues . spoken ,
5 // Only top 5
);
```

## [ Optimization Strategies](#optimization-strategies)

### [ Tiered Indexing](#tiered-indexing)

Create multiple indexes at different quality levels:

Python

Node.js

```
# Fast, cheap index for preview/discovery
preview_index = video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 60 , "frame_count" : 1 },
prompt = "What is the main topic?" ,
name = "preview"
)

# Detailed index for deep search
detailed_index = video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 10 , "frame_count" : 3 },
prompt = "Describe people, objects, and actions in detail" ,
name = "detailed"
)
```

```
// Fast, cheap index for preview/discovery
const previewIndex = await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 60 , frame_count: 1 },
prompt: "What is the main topic?" ,
name: "preview"
});

// Detailed index for deep search
const detailedIndex = await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 10 , frame_count: 3 },
prompt: "Describe people, objects, and actions in detail" ,
name: "detailed"
});
```

### [ Index on Demand](#index-on-demand)

Only index what you need:

```
# Index spoken content immediately (cheap)
video.index_spoken_words()

# Index visuals only when needed (expensive)
if user_requests_visual_search:
video.index_scenes( prompt = "Describe the scene" )
```

### [ Batch Processing](#batch-processing)

For large libraries, process during off-peak hours:

```
# Queue videos for background indexing
for video in coll.get_videos():
video.index_scenes(
prompt = "Describe the scene" ,
callback_url = "https://your-backend.com/webhooks"
)
```

## [ Cost Estimation](#cost-estimation)

### [ Factors](#factors)

1. **Video duration** - Longer = more scenes
2. **Frame extraction** - More frames = more API calls
3. **Scene interval** - Shorter = more scenes
4. **Collection size** - More videos = more processing

### [ Example Calculations](#example-calculations)

| Video   | Config        |   Scenes |   Frames | Cost Factor   |
|---------|---------------|----------|----------|---------------|
| 1 hour  | 60s, 1 frame  |       60 |       60 | 1x            |
| 1 hour  | 30s, 1 frame  |      120 |      120 | 2x            |
| 1 hour  | 10s, 3 frames |      360 |    1,080 | 18x           |

## [ Recommendations by Use Case](#recommendations-by-use-case)

### [ Media Archive (Cost-Sensitive)](#media-archive-cost-sensitive)

```
video.index_spoken_words() # Always index speech (cheap)

video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 60 , "frame_count" : 1 },
prompt = "Describe the main content"
)
```

### [ Security Monitoring (Quality-First)](#security-monitoring-quality-first)

```
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 5 , "frame_count" : 3 },
prompt = "Identify all people, vehicles, and suspicious activity"
)
```

### [ E-commerce (Balanced)](#e-commerce-balanced)

```
video.index_scenes(
extraction_type = SceneExtractionType.shot_based,
extraction_config = { "threshold" : 20 , "frame_count" : 2 },
prompt = "Identify products, brands, and pricing"
)
```

## [ Monitoring](#monitoring)

Track indexing and search metrics:

```
import time

# Measure indexing time
start = time.time()
video.index_scenes( prompt = "Describe the scene" )
indexing_time = time.time() - start
print ( f "Indexing took { indexing_time :.2f} s" )

# Measure search time
start = time.time()
results = video.search( "query" )
search_time = time.time() - start
print ( f "Search took { search_time :.3f} s, found { len (results.get_shots()) } results" )
```

## [ Next Steps](#next-steps)

## Accuracy Tips

Improve search precision

## Create an Index

Get started with indexing

[Accuracy Tips](\pages\understand\quality-and-evaluation\accuracy-tips) [Timeline Architecture](\pages\act\programmable-editing\timeline-architecture)

⌘ I