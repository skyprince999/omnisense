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
    - [Create an Index](\pages\understand\indexing-pipelines\create-an-index)
    - [Frame Processing Primitives](\pages\understand\indexing-pipelines\multimodal-indexing)
    - [Multiple Indexes](\pages\understand\indexing-pipelines\multiple-indexes)
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
- [Spoken Word Index](#spoken-word-index)
    - [Language Support](#language-support)
- [Scene Index](#scene-index)
    - [Prompt Shapes the Index](#prompt-shapes-the-index)
    - [Extraction Configuration](#extraction-configuration)
- [Managing Indexes](#managing-indexes)
    - [List All Scene Indexes](#list-all-scene-indexes)
    - [Get Index Details](#get-index-details)
    - [Delete an Index](#delete-an-index)
- [Async Processing with Callbacks](#async-processing-with-callbacks)
- [What You Can Build](#what-you-can-build)
- [Next Steps](#next-steps)

[Understand](\pages\understand\indexing-pipelines\create-an-index)

[Indexing Pipelines](\pages\understand\indexing-pipelines\create-an-index)

# Create an Index

Copy page

Transform video into searchable data with spoken word and visual indexes

Copy page

Indexes turn raw video into structured, searchable data. Create a spoken word index for dialogue and narration, or a scene index for visual content.

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video( "m-xxx" )

# Index spoken content (dialogue, narration)
video.index_spoken_words()

# Index visual content (scenes, objects, actions)
scene_index_id = video.index_scenes(
prompt = "Describe what's happening in the scene"
)

# Search both
results = video.search( "car chase through the city" )
results.play()
```

```
import { connect } from 'videodb' ;

const conn = connect ();
const coll = await conn . getCollection ();
const video = await coll . getVideo ( "m-xxx" );

// Index spoken content (dialogue, narration)
await video . indexSpokenWords ();

// Index visual content (scenes, objects, actions)
const sceneIndexId = await video . indexScenes ({
prompt: "Describe what's happening in the scene"
});

// Search both
const results = await video . search ( "car chase through the city" );
await results . play ();
```

## [ Spoken Word Index](#spoken-word-index)

Transcribes audio into timestamped text using automatic speech recognition (ASR).

Python

Node.js

```
video.index_spoken_words()
```

```
await video . indexSpokenWords ();
```

**What it captures:**

- Dialogue and conversations
- Narration and voiceovers
- Lectures and presentations
- Interviews and podcasts

### [ Language Support](#language-support)

Major languages are auto-detected. For others, pass the language code:

Python

Node.js

```
# Auto-detect (English, Spanish, French, German, Italian, Portuguese, Dutch)
video.index_spoken_words()

# Explicit language code
video.index_spoken_words( language_code = "hi" ) # Hindi
video.index_spoken_words( language_code = "ja" ) # Japanese
video.index_spoken_words( language_code = "zh" ) # Chinese
```

```
// Auto-detect (English, Spanish, French, German, Italian, Portuguese, Dutch)
await video . indexSpokenWords ();

// Explicit language code
await video . indexSpokenWords ({ languageCode: "hi" }); // Hindi
await video . indexSpokenWords ({ languageCode: "ja" }); // Japanese
await video . indexSpokenWords ({ languageCode: "zh" }); // Chinese
```

| Language           | Code                        |
|--------------------|-----------------------------|
| English (Global)   | `en`                        |
| English (US/UK/AU) | `en_us` , `en_uk` , `en_au` |
| Spanish            | `es`                        |
| French             | `fr`                        |
| German             | `de`                        |
| Hindi              | `hi`                        |
| Japanese           | `ja`                        |
| Chinese            | `zh`                        |
| Korean             | `ko`                        |
| Russian            | `ru`                        |

## [ Scene Index](#scene-index)

Analyzes video frames using vision models to describe visual content.

Python

Node.js

```
scene_index_id = video.index_scenes(
prompt = "Describe the scene in detail"
)
```

```
const sceneIndexId = await video . indexScenes ({
prompt: "Describe the scene in detail"
});
```

**What it captures:**

- Objects and people
- Actions and activities
- Environments and settings
- Visual transitions

### [ Prompt Shapes the Index](#prompt-shapes-the-index)

The prompt you provide determines what gets indexed:

Python

Node.js

```
# Focus on people
video.index_scenes( prompt = "Describe the people and their actions" )

# Focus on environment
video.index_scenes( prompt = "Describe the location and setting" )

# Focus on specific objects
video.index_scenes( prompt = "Identify all vehicles and their colors" )
```

```
// Focus on people
await video . indexScenes ({ prompt: "Describe the people and their actions" });

// Focus on environment
await video . indexScenes ({ prompt: "Describe the location and setting" });

// Focus on specific objects
await video . indexScenes ({ prompt: "Identify all vehicles and their colors" });
```

### [ Extraction Configuration](#extraction-configuration)

Control how frames are sampled - choose between frame segmentation (regular intervals) and scene segmentation (automatic transitions):

Comparison of frame segmentation and scene segmentation extraction types

<!-- image -->

Python

Node.js

```
from videodb import SceneExtractionType

# Time-based: every N seconds
video.index_scenes(
extraction_type = SceneExtractionType.time_based,
extraction_config = { "time" : 10 , "frame_count" : 2 },
prompt = "Describe the scene"
)

< img
src = "/assets/indexing/time-based-extraction.avif"
style = {{width: "auto" , height: "auto" }}
alt = "Time-based extraction example showing consistent frame sampling at regular intervals"
/>

# Shot-based: detect visual transitions
video.index_scenes(
extraction_type = SceneExtractionType.shot_based,
extraction_config = { "threshold" : 20 , "frame_count" : 1 },
prompt = "Describe the scene"
)
```

```
// Time-based: every N seconds
await video . indexScenes ({
extractionType: 'time' ,
extractionConfig: { time: 10 , frame_count: 2 },
prompt: "Describe the scene"
});

// Shot-based: detect visual transitions
await video . indexScenes ({
extractionType: 'shot' ,
extractionConfig: { threshold: 20 , frame_count: 1 },
prompt: "Describe the scene"
});
```

| Method     | Best For                               |
|------------|----------------------------------------|
| Time-based | Consistent sampling, dynamic content   |
| Shot-based | Edited videos with clear scene changes |

## [ Managing Indexes](#managing-indexes)

### [ List All Scene Indexes](#list-all-scene-indexes)

Python

Node.js

```
indexes = video.list_scene_index()
for idx in indexes:
print ( f " { idx.id } : { idx.name } - { idx.status } " )
```

```
const indexes = await video . listSceneIndex ();
for ( const idx of indexes ) {
console . log ( ` ${ idx . id } : ${ idx . name } - ${ idx . status } ` );
}
```

List of scene indexes showing id, name, and status

<!-- image -->

### [ Get Index Details](#get-index-details)

Python

Node.js

```
scene_index = video.get_scene_index(scene_index_id)
for scene in scene_index:
print ( f " { scene.start } - { scene.end } : { scene.description } " )
```

```
const sceneIndex = await video . getSceneIndex ( sceneIndexId );
for ( const scene of sceneIndex ) {
console . log ( ` ${ scene . start } - ${ scene . end } : ${ scene . description } ` );
}
```

### [ Delete an Index](#delete-an-index)

Python

Node.js

```
video.delete_scene_index(scene_index_id)
```

```
await video . deleteSceneIndex ( sceneIndexId );
```

## [ Async Processing with Callbacks](#async-processing-with-callbacks)

For long videos, use callbacks to get notified when indexing completes:

Python

Node.js

```
scene_index_id = video.index_scenes(
prompt = "Describe the scene" ,
callback_url = "https://your-backend.com/webhooks/index-complete"
)
```

```
const sceneIndexId = await video . indexScenes ({
prompt: "Describe the scene" ,
callbackUrl: "https://your-backend.com/webhooks/index-complete"
});
```

## [ What You Can Build](#what-you-can-build)

## Keyword Search Compilation

Index spoken words, then search to create highlight reels

## Multimodal Search

Combine spoken word and scene indexes for powerful queries

## Baby Crib Monitoring

Scene indexing enables real-time infant monitoring

## Intrusion Detection

Index camera feeds to detect unauthorized access

## [ Next Steps](#next-steps)

## Multimodal Indexing

Extraction strategies for video + audio

## Multiple Indexes

Layer different perspectives on the same media

[Output Formats](\pages\ingest\transcoding\output-formats) [Frame Processing Primitives](\pages\understand\indexing-pipelines\multimodal-indexing)

⌘ I