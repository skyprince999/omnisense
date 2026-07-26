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
    - Understanding
        - [Understanding Artifacts](\pages\understand\indexing-pipelines\understanding-artifacts)
        - [Analyzer Outputs](\pages\understand\indexing-pipelines\analyzer-outputs)
    - Indexing
- Search and Retrieval
- Legacy Indexing &amp; Search
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

- [Common output envelope](#common-output-envelope)
- [Spoken words: spoken\_words](#spoken-words-spoken_words)
- [Objects: object\_detection](#objects-object_detection)
- [OCR: ocr](#ocr-ocr)
- [Brands: brand\_detection](#brands-brand_detection)
- [Activity: activity\_recognition](#activity-activity_recognition)
- [Location: location\_detection](#location-location_detection)
- [Scene: vlm](#scene-vlm)
- [How outputs map to indexes](#how-outputs-map-to-indexes)
- [Next steps](#next-steps)

[Understand](\pages\understand\indexing-pipelines\understanding-artifacts)

[Understanding &amp; Indexing Pipelines](\pages\understand\indexing-pipelines\understanding-artifacts)

[Understanding](\pages\understand\indexing-pipelines\understanding-artifacts)

# Analyzer Outputs

Copy page

Sample output shapes for VideoDB understanding analyzers.

Copy page

After an [understanding run](\pages\understand\indexing-pipelines\understanding-artifacts) completes, each analyzer has produced a named **artifact** containing timestamped records. Use `get_output()` to inspect the artifact and see which fields the analyzer produced.

```
understanding.wait_until_complete()

analyzer = understanding.get_analyzer( "scene" )
output = analyzer.get_output()

print (output[ "scenes" ][ 0 ][ "data" ])
```

Artifact output is organized into **scenes** . Each scene covers a range of video defined by `start` and `end` , in seconds. Scenes may come from visual cuts or fixed time windows. Some analyzers also include frame-level observations inside a scene; those use a single `timestamp` . The contents of `data` depend on the analyzer. When configuring [index fields](\pages\understand\indexing-pipelines\multiple-indexes) , paths are relative to `data` , so use `text` or `frames.detections.label` rather than `scenes.data.text` . `get_output()` is for inspecting the artifact. To [create an index](\pages\understand\indexing-pipelines\create-an-index) , pass the analyzer directly so the output does not need to travel through your client:

```
video.index( source = analyzer)
```

The sections below show the output shape and useful [indexing fields](\pages\understand\indexing-pipelines\multiple-indexes) for each analyzer.

## [ Common output envelope](#common-output-envelope)

All analyzer artifacts follow the same high-level shape:

```
{
"name" : "scene" ,
"type" : "vlm" ,
"status" : "done" ,
"metadata" : {},
"scenes" : [
{
"scene_id" : "scene-0.000-3.420" ,
"start" : 0.0 ,
"end" : 3.42 ,
"data" : {},
"metadata" : {}
}
]
}
```

The `data` object is analyzer-specific. The top-level and scene-level `metadata` objects contain additional analyzer or scene details when available; either object may be empty.

Some fields can vary by model, schema version, or workspace configuration. Built-in analyzers keep stable top-level fields for indexing wherever possible.

The [indexing recommendations](\pages\understand\indexing-pipelines\create-an-index#declare-index-capabilities-with-use-for) use these capabilities:

| Capability      | What it does                                                                                            |
|-----------------|---------------------------------------------------------------------------------------------------------|
| `semantic`      | Finds records with similar meaning.                                                                     |
| `filter`        | Restricts results by field values.                                                                      |
| `aggregate`     | Groups or counts field values.                                                                          |
| `sort`          | Orders results by a field.                                                                              |
| `return_fields` | Includes stored fields in retrieval results; it is a retrieval option rather than an index field group. |

## [ Spoken words: spoken\_words](#spoken-words-spoken_words)

Default artifact name: `transcript`

```
{
"name" : "transcript" ,
"type" : "spoken_words" ,
"status" : "done" ,
"metadata" : {},
"scenes" : [
{
"scene_id" : "scene-0.000-11.762" ,
"start" : 0.0 ,
"end" : 11.762 ,
"data" : {
"text" : "In 1941, in German occupied Poland, the Nazis" ,
"words" : [
{
"text" : "In" ,
"start" : 7.04 ,
"end" : 7.2 ,
"confidence" : 0.99560547 ,
"speaker" : "A"
},
{
"text" : "1941," ,
"start" : 7.2 ,
"end" : 8.4 ,
"confidence" : 0.99902 ,
"speaker" : "A"
}
]
},
"metadata" : {}
}
]
}
```

Useful indexing fields:

| Field              | Use for                                         |
|--------------------|-------------------------------------------------|
| `text`             | semantic search, retrieval with `return_fields` |
| `words.speaker`    | filter, aggregate                               |
| `words.confidence` | filter, sort                                    |
| `words`            | retrieval with `return_fields`                  |

Each item in `words` contains word-level timing and may include `confidence` and `speaker` values.

## [ Objects: object\_detection](#objects-object_detection)

Default artifact name: `objects`

```
{
"name" : "objects" ,
"type" : "object_detection" ,
"status" : "done" ,
"metadata" : {},
"scenes" : [
{
"scene_id" : "scene-0.000-8.634" ,
"start" : 0.0 ,
"end" : 8.634 ,
"data" : {
"frames" : [
{
"frame_id" : "frame-scene-0.000-8.634-0.000" ,
"timestamp" : 0.0 ,
"detections" : []
},
{
"frame_id" : "frame-scene-0.000-8.634-1.000" ,
"timestamp" : 1.0 ,
"detections" : [
{
"label" : "stop sign" ,
"score" : 0.6835 ,
"box" : {
"box" : [ 0.2836 , 0.378 , 0.6965 , 0.5823 ],
"unit" : "normalized"
}
}
]
}
]
},
"metadata" : {}
}
]
}
```

A frame can have an empty `detections` list. Each detection contains a label, confidence score, and bounding-box object. The inner `box` array contains the coordinates, while `unit` describes their coordinate system. Useful indexing fields:

| Field                        | Use for                                                  |
|------------------------------|----------------------------------------------------------|
| `frames.detections.label`    | filter, aggregate                                        |
| `frames.detections.score`    | filter, sort                                             |
| `frames.detections.box.box`  | stored bounding-box coordinates for overlays             |
| `frames.detections.box.unit` | stored coordinate unit, such as `normalized`             |
| `frames`                     | complete stored frame detail for retrieval and debugging |

## [ OCR: ocr](#ocr-ocr)

Default artifact name: `ocr ocr` extracts visible text from frames, such as signs, slides, labels, captions, and UI text.

```
{
"name" : "ocr" ,
"type" : "ocr" ,
"status" : "done" ,
"metadata" : {
"model" : "default" ,
"prompt_version" : "ocr_v1" ,
"schema_version" : "v1"
},
"scenes" : [
{
"scene_id" : "scene-000001" ,
"start" : 0.0 ,
"end" : 3.42 ,
"data" : {
"text" : "EXIT 25% OFF"
},
"metadata" : {}
}
]
}
```

Useful indexing fields:

| Field   | Use for                                         |
|---------|-------------------------------------------------|
| `text`  | semantic search, retrieval with `return_fields` |

## [ Brands: brand\_detection](#brands-brand_detection)

Default artifact name: `brands brand_detection` extracts logos, brand names, product labels, and sponsorships.

```
{
"name" : "brands" ,
"type" : "brand_detection" ,
"status" : "done" ,
"metadata" : {
"model" : "default" ,
"prompt_version" : "brand_detection_v1" ,
"schema_version" : "v1"
},
"scenes" : [
{
"scene_id" : "scene-000002" ,
"start" : 3.42 ,
"end" : 7.10 ,
"data" : {
"brand_names" : [ "Nike" ]
},
"metadata" : {}
}
]
}
```

Useful indexing fields:

| Field         | Use for                                           |
|---------------|---------------------------------------------------|
| `brand_names` | filter, aggregate, retrieval with `return_fields` |

## [ Activity: activity\_recognition](#activity-activity_recognition)

Default artifact name: `activity activity_recognition` extracts actions and activities.

```
{
"name" : "activity" ,
"type" : "activity_recognition" ,
"status" : "done" ,
"metadata" : {
"model" : "default" ,
"prompt_version" : "activity_recognition_v1" ,
"schema_version" : "v1"
},
"scenes" : [
{
"scene_id" : "scene-000002" ,
"start" : 3.42 ,
"end" : 7.10 ,
"data" : {
"activity" : "checking phone"
},
"metadata" : {}
}
]
}
```

Useful indexing fields:

| Field      | Use for                                                            |
|------------|--------------------------------------------------------------------|
| `activity` | semantic search, filter, aggregate, retrieval with `return_fields` |

## [ Location: location\_detection](#location-location_detection)

Default artifact name: `location location_detection` extracts setting and place context.

```
{
"name" : "location" ,
"type" : "location_detection" ,
"status" : "done" ,
"metadata" : {
"model" : "default" ,
"prompt_version" : "location_detection_v1" ,
"schema_version" : "v1"
},
"scenes" : [
{
"scene_id" : "scene-000003" ,
"start" : 7.10 ,
"end" : 12.0 ,
"data" : {
"location" : "outdoor street outside a retail shop in daylight"
},
"metadata" : {}
}
]
}
```

Useful indexing fields:

| Field      | Use for                                                            |
|------------|--------------------------------------------------------------------|
| `location` | semantic search, filter, aggregate, retrieval with `return_fields` |

## [ Scene: vlm](#scene-vlm)

Default artifact name: `scene` Here, `scene` is the default artifact name for the `vlm` analyzer. Its output can contain multiple timestamped scene records. Use `vlm` when you want general scene descriptions or a custom prompt/schema. Without a custom schema, each scene's description is returned in `data.text` :

```
{
"name" : "scene" ,
"type" : "vlm" ,
"status" : "done" ,
"metadata" : {},
"scenes" : [
{
"scene_id" : "scene-120.000-180.000" ,
"start" : 120.0 ,
"end" : 180.0 ,
"data" : {
"text" : "The scene is a paper-cutout style animation set against a textured wall and a long wooden conference table."
},
"metadata" : {}
}
]
}
```

When you provide a `schema` , the fields inside `data` follow that schema instead. For example:

```
{
"scene_description" : "string" ,
"activity" : "string" ,
"setting" : "string"
}
```

produces scene data shaped like:

```
{
"scene_description" : "A man stands near a parked car while looking at his phone." ,
"activity" : "checking phone" ,
"setting" : "outdoor street"
}
```

Useful indexing fields:

| Field                          | Use for                                            |
|--------------------------------|----------------------------------------------------|
| `text`                         | semantic search, retrieval with `return_fields`    |
| fields from your custom schema | depends on the field type and your retrieval needs |

For object labels, brand names, OCR text, activities, or location signals, use the dedicated analyzers unless your VLM prompt/schema explicitly emits those fields.

## [ How outputs map to indexes](#how-outputs-map-to-indexes)

When you [index an artifact](\pages\understand\indexing-pipelines\create-an-index) , choose which fields become retrieval fields. A scene is the retrieval unit. Some artifacts have one scene-level value, such as `activity` , `location` , or OCR `text` . Others contain repeated values, such as `brand_names` or `frames[].detections[]` . When indexing repeated values:

- one scene can emit multiple filter or aggregate signals
- the index may flatten those signals internally, such as one row per brand, object label, or detection
- retrieval still returns the scene with its `scene_id` , `start` , and `end`

```
scene = understanding.get_analyzer( "scene" )
objects = understanding.get_analyzer( "objects" )

video.index(
name = "scene" ,
source = scene,
use_for = [ "semantic" , "query" ],
fields = {
"semantic" : [ "scene_description" ],
},
)

video.index(
name = "objects" ,
source = objects,
use_for = [ "query" , "aggregate" ],
fields = {
"filter" : [ "frames.detections.label" , "frames.detections.score" ],
"aggregate" : [ "frames.detections.label" ],
},
)
```

General rule:

| Output field shape                            | Use as                                           |
|-----------------------------------------------|--------------------------------------------------|
| descriptions, summaries, transcript text      | `semantic`                                       |
| labels, names, enums, booleans                | `filter` , `aggregate`                           |
| confidence scores and other numeric fields    | `filter` , `aggregate` , `sort`                  |
| frames, boxes, raw responses, detailed arrays | requested at retrieval time with `return_fields` |

## [ Next steps](#next-steps)

## Create an Index

Turn artifacts into searchable indexes.

## Index Fields

Choose which fields become searchable, filterable, aggregatable, or sortable.

[Understanding Artifacts](\pages\understand\indexing-pipelines\understanding-artifacts) [Create an Index](\pages\understand\indexing-pipelines\create-an-index)

⌘ I