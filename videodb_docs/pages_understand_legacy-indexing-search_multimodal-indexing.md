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
- [Extraction Strategies](#extraction-strategies)
    - [Time-Based Extraction](#time-based-extraction)
    - [Shot-Based Extraction](#shot-based-extraction)
- [Prompt Engineering](#prompt-engineering)
    - [Basic Prompts](#basic-prompts)
    - [Domain-Specific Prompts](#domain-specific-prompts)
    - [Structured Output Prompts](#structured-output-prompts)
- [Frame Selection Strategy](#frame-selection-strategy)
    - [Static Content (1 frame)](#static-content-1-frame)
    - [Motion and Activity (3-5 frames)](#motion-and-activity-3-5-frames)
    - [Key Moment Selection](#key-moment-selection)
- [Combining Modalities](#combining-modalities)
- [Extraction Examples](#extraction-examples)
    - [Traffic Monitoring](#traffic-monitoring)
    - [Educational Content](#educational-content)
- [Next Steps](#next-steps)

[Understand](\pages\understand\indexing-pipelines\understanding-artifacts)

[Legacy Indexing &amp; Search](\pages\understand\legacy-indexing-search\indexes-and-search)

# Frame Processing Primitives

Copy page

Video carries information in multiple modalities: what's said, what's shown, and how it changes over time. Multimodal indexing extracts meaning from all of these through extraction strategies for combining visual and spoken content analysis.

Copy page

## [ Quick Example](#quick-example)

Python

Node.js

```
from videodb import SceneExtractionType

# Index spoken content
video.index_spoken_words()

# Index visual content with extraction strategy
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 5 , "frame_count" : 3 },
prompt = "Describe the scene, people, and any visible text"
)
```

```
// Index spoken content
await video . indexSpokenWords ();

// Index visual content with extraction strategy
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 5 , frame_count: 3 },
prompt: "Describe the scene, people, and any visible text"
});
```

## [ Extraction Strategies](#extraction-strategies)

### [ Time-Based Extraction](#time-based-extraction)

Split video into fixed intervals. Simple and predictable.

Time-based extraction example showing consistent frame sampling at regular intervals

<!-- image -->

Python

Node.js

```
from videodb import SceneExtractionType

video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = {
"time" : 10 , # Scene length in seconds
"frame_count" : 2 # Frames to analyze per scene
},
prompt = "Describe what's happening"
)
```

```
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: {
time: 10 , // Scene length in seconds
frame_count: 2 // Frames to analyze per scene
},
prompt: "Describe what's happening"
});
```

| Parameter       | Type   | Default     | Description                                     |
|-----------------|--------|-------------|-------------------------------------------------|
| `time`          | int    | 10          | Interval in seconds                             |
| `frame_count`   | int    | 1           | Frames per scene                                |
| `select_frames` | list   | `["first"]` | Which frames: `"first"` , `"middle"` , `"last"` |

Use either `frame_count` or `select_frames` , not both.

**Best for:**

- Surveillance and monitoring
- Live streams
- Content with no clear scene boundaries
- Consistent sampling across long videos

### [ Shot-Based Extraction](#shot-based-extraction)

Detect visual transitions (cuts, fades) to identify natural scene boundaries.

Shot-based extraction example showing automatic detection of visual transitions and scene boundaries

<!-- image -->

Python

Node.js

```
from videodb import SceneExtractionType

video.index_scenes(
extraction_type = SceneExtractionType.shot_based,
extraction_config = {
"threshold" : 20 , # Sensitivity (lower = more sensitive)
"frame_count" : 1 # Frames per detected shot
},
prompt = "Describe the scene"
)
```

```
await video . indexScenes ({
extractionType: 'shot' ,
extractionConfig: {
threshold: 20 , // Sensitivity (lower = more sensitive)
frame_count: 1 // Frames per detected shot
},
prompt: "Describe the scene"
});
```

| Parameter     | Type   |   Default | Description           |
|---------------|--------|-----------|-----------------------|
| `threshold`   | int    |        20 | Detection sensitivity |
| `frame_count` | int    |         1 | Frames per shot       |

**Best for:**

- Movies and TV shows
- Edited content with clear cuts
- Music videos
- Commercials

## [ Prompt Engineering](#prompt-engineering)

The prompt shapes what gets extracted. Think of it as telling the vision model what to look for.

### [ Basic Prompts](#basic-prompts)

```
# General description
prompt = "Describe what's happening in this scene"

# Object-focused
prompt = "Identify all objects and people visible"

# Action-focused
prompt = "Describe the activities and movements"
```

### [ Domain-Specific Prompts](#domain-specific-prompts)

Python

Node.js

```
# Retail / E-commerce
video.index_scenes(
prompt = "Identify products, brands, and pricing visible on screen"
)

# Sports
video.index_scenes(
prompt = "Describe the play, players involved, and outcome"
)

# Security
video.index_scenes(
prompt = "Identify people, vehicles, and any unusual activity"
)

# Education
video.index_scenes(
prompt = "Describe the topic being taught and any diagrams or text shown"
)
```

```
// Retail / E-commerce
await video . indexScenes ({
prompt: "Identify products, brands, and pricing visible on screen"
});

// Sports
await video . indexScenes ({
prompt: "Describe the play, players involved, and outcome"
});

// Security
await video . indexScenes ({
prompt: "Identify people, vehicles, and any unusual activity"
});

// Education
await video . indexScenes ({
prompt: "Describe the topic being taught and any diagrams or text shown"
});
```

### [ Structured Output Prompts](#structured-output-prompts)

Guide the model to produce consistent, parseable output:

```
prompt = """
Describe this scene with the following structure:
- Setting: Where is this taking place?
- People: Who is present and what are they doing?
- Objects: What notable items are visible?
- Action: What is happening?
"""
```

## [ Frame Selection Strategy](#frame-selection-strategy)

More frames = more detail but higher cost. Choose based on your content.

### [ Static Content (1 frame)](#static-content-1-frame)

For content where a single frame captures the scene:

Python

Node.js

```
# One frame is enough for static shots
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 10 , "frame_count" : 1 },
prompt = "Describe the scene"
)
```

```
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 10 , frame_count: 1 },
prompt: "Describe the scene"
});
```

### [ Motion and Activity (3-5 frames)](#motion-and-activity-3-5-frames)

For understanding movement and temporal changes:

Python

Node.js

```
# Multiple frames to capture motion
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 5 , "frame_count" : 5 },
prompt = "Describe the activity and how it progresses"
)
```

```
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 5 , frame_count: 5 },
prompt: "Describe the activity and how it progresses"
});
```

### [ Key Moment Selection](#key-moment-selection)

Select specific frames within each scene:

Python

Node.js

```
# First and last frames only
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 10 , "select_frames" : [ "first" , "last" ]},
prompt = "Describe how the scene changes from start to end"
)
```

```
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 10 , select_frames: [ "first" , "last" ] },
prompt: "Describe how the scene changes from start to end"
});
```

## [ Combining Modalities](#combining-modalities)

Index both spoken and visual content, then search across both:

Python

Node.js

```
from videodb import IndexType, SearchType

# Index both modalities
video.index_spoken_words()
video.index_scenes( prompt = "Describe the visual content" )

# Search spoken content
spoken_results = video.search(
query = "discusses climate change" ,
index_type = IndexType.spoken_word
)

# Search visual content
visual_results = video.search(
query = "shows melting glaciers" ,
index_type = IndexType.scene
)
```

```
import { IndexTypeValues , SearchTypeValues } from 'videodb' ;

// Index both modalities
await video . indexSpokenWords ();
await video . indexScenes ({ prompt: "Describe the visual content" });

// Search spoken content
const spokenResults = await video . search (
"discusses climate change" ,
SearchTypeValues . semantic ,
IndexTypeValues . spoken
);

// Search visual content
const visualResults = await video . search (
"shows melting glaciers" ,
SearchTypeValues . semantic ,
IndexTypeValues . scene
);
```

## [ Extraction Examples](#extraction-examples)

### [ Traffic Monitoring](#traffic-monitoring)

Python

Node.js

```
# Detect vehicle colors (single frame sufficient)
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 1 , "frame_count" : 1 },
prompt = "Identify the color and type of each vehicle"
)

# Detect stopped vehicles (need multiple frames)
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 4 , "frame_count" : 5 },
prompt = "Identify if any vehicle has stopped or is moving slowly"
)
```

```
// Detect vehicle colors (single frame sufficient)
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 1 , frame_count: 1 },
prompt: "Identify the color and type of each vehicle"
});

// Detect stopped vehicles (need multiple frames)
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 4 , frame_count: 5 },
prompt: "Identify if any vehicle has stopped or is moving slowly"
});
```

### [ Educational Content](#educational-content)

Python

Node.js

```
# Combine visual and spoken indexing
video.index_spoken_words()

video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 30 , "select_frames" : [ "first" , "middle" , "last" ]},
prompt = "Describe diagrams, equations, or visual aids shown"
)
```

```
// Combine visual and spoken indexing
await video . indexSpokenWords ();

await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 30 , select_frames: [ "first" , "middle" , "last" ] },
prompt: "Describe diagrams, equations, or visual aids shown"
});
```

## [ Next Steps](#next-steps)

## Multiple Indexes

Layer different perspectives on the same media

## Accuracy Tips

Improve precision and recall

[Create an Index](\pages\understand\legacy-indexing-search\create-an-index) [Multiple Indexes](\pages\understand\legacy-indexing-search\multiple-indexes)

⌘ I