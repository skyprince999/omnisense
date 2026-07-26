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

- [Start simple](#start-simple)
- [What should I use?](#what-should-i-use)
- [The mental model](#the-mental-model)
- [Inspect and manage runs](#inspect-and-manage-runs)
- [How video.understand() is structured](#how-video-understand-is-structured)
- [Run-level options](#run-level-options)
    - [segmentation: visual time ranges](#segmentation-visual-time-ranges)
    - [transform: media preparation](#transform-media-preparation)
- [Analyzer options](#analyzer-options)
    - [Analyzer type: choose the artifact](#analyzer-type-choose-the-artifact)
    - [Analyzer name: output keys](#analyzer-name-output-keys)
    - [Analyzer inputs: reuse earlier artifacts](#analyzer-inputs-reuse-earlier-artifacts)
    - [Analyzer sampling: frame selection](#analyzer-sampling-frame-selection)
    - [Analyzer config: models, prompts, and schemas](#analyzer-config-models-prompts-and-schemas)
    - [spoken\_words](#spoken_words)
    - [object\_detection](#object_detection)
    - [vlm](#vlm)
    - [Sandbox VLM models](#sandbox-vlm-models)
    - [Specialized VLM analyzers](#specialized-vlm-analyzers)
- [Putting it together](#putting-it-together)
- [Cost and quality tips](#cost-and-quality-tips)
- [Next steps](#next-steps)

[Understand](\pages\understand\indexing-pipelines\understanding-artifacts)

[Understanding &amp; Indexing Pipelines](\pages\understand\indexing-pipelines\understanding-artifacts)

[Understanding](\pages\understand\indexing-pipelines\understanding-artifacts)

# Understanding Artifacts

Copy page

Turn videos into structured artifacts for search, retrieval, and analysis.

Copy page

Understanding is the first step in the retrieval pipeline.

```
Understand → Index → Retrieve
```

An **understanding run** applies one or more **analyzers** to a video and creates reusable **artifacts** such as transcripts, object detections, OCR text, brand signals, activity/location signals, or VLM scene descriptions. You usually start with defaults, then add configuration only when you need more control.

## Try the understanding notebooks

Explore runnable examples for creating and inspecting understanding artifacts.

## [ Start simple](#start-simple)

For most use cases, only provide analyzer types.

```
understanding = video.understand(
analyzers = [
{ "type" : "spoken_words" },
{ "type" : "vlm" },
],
)

understanding.wait_until_complete()

transcript = understanding.get_analyzer( "transcript" ).get_output()
scene = understanding.get_analyzer( "scene" ).get_output()

print (scene[ "scenes" ][ 0 ][ "data" ])
```

That is enough for a first run. VideoDB automatically chooses the output names, video chunking, frame selection, and default analyzer settings. Each analyzer type has a default artifact name: `spoken_words` → `transcript` , `object_detection` → `objects` , and `vlm` → `scene` . That name is what you pass to `get_analyzer()` . Override it with `name` . See [Analyzer](#analyzer-type-choose-the-artifact) [`type`](#analyzer-type-choose-the-artifact) for the full list.

## [ What should I use?](#what-should-i-use)

VideoDB includes built-in analyzers for common video and audio signals. Use the table below to choose an analyzer based on what you want to retrieve.

| Analyzer                                            | Use when you want to...                           | Produces                                                                |
|-----------------------------------------------------|---------------------------------------------------|-------------------------------------------------------------------------|
| `spoken_words`                                      | Search spoken words, lectures, meetings, podcasts | Timed transcript text for semantic and full-text search.                |
| `vlm`                                               | Search what is visible or happening in the video  | Natural-language scene descriptions.                                    |
| `object_detection`                                  | Filter, count, or locate objects                  | Object labels, counts, confidence scores, and boxes.                    |
| `ocr`                                               | Search text visible on screen                     | Signs, slides, labels, captions, and UI text.                           |
| `brand_detection`                                   | Find logos or brands                              | Brand names, logos, product labels, and sponsorships.                   |
| `activity_recognition`                              | Detect actions or activities                      | Activity and behavior signals.                                          |
| `location_detection`                                | Detect setting or location                        | Place, setting, and scene context.                                      |
| `object_detection` + `spoken_words` + `ocr` + `vlm` | Build the richest scene understanding             | Separate object, speech, visible-text, and scene-description artifacts. |

`ocr` , `brand_detection` , `activity_recognition` , and `location_detection` are VLM-backed analyzers with task-specific output shapes. Use the generic `vlm` analyzer when you want to provide your own prompt or schema.

## [ The mental model](#the-mental-model)

An analyzer produces one named artifact. Stored artifacts can be inspected and reused independently.

| Step              | What happens                                        | Example                                            |
|-------------------|-----------------------------------------------------|----------------------------------------------------|
| Choose analyzers  | Decide which signals you want to extract            | `spoken_words` , `vlm`                             |
| Run understanding | Create artifacts from the video                     | `video.understand(analyzers=[...])`                |
| Inspect outputs   | Fetch artifact output from an analyzer              | `understanding.get_analyzer("scene").get_output()` |
| Refine            | Add configuration only when defaults are not enough | `name` , `sampling` , `config`                     |

## [ Inspect and manage runs](#inspect-and-manage-runs)

`video.understand(...)` returns an understanding run object with an `id` , `status` , and analyzer handles.

```
print (understanding.id, understanding.status)

understanding.refresh()

for analyzer in understanding.list_analyzers():
print (analyzer.name, analyzer.type, analyzer.status)
```

Use `wait_until_complete()` before fetching analyzer outputs or indexing artifacts. Run-level terminal statuses are `done` , `failed` , and `partial` .

```
understanding.wait_until_complete( timeout = 3600 , poll_interval = 15 )
scene = understanding.get_analyzer( "scene" ).get_output()
```

You can also reopen or list previous runs for the same video:

```
same_understanding = video.get_understanding(understanding.id)

for item in video.list_understandings():
print (item.id, item.status)
```

Only delete an understanding run when you no longer need its stored artifacts.

```
understanding.delete()
```

## [ How video.understand() is structured](#how-video-understand-is-structured)

`video.understand()` has two levels of configuration:

1. **run-level options** apply to the whole understanding run
2. **analyzer options** apply to one item inside `analyzers`

```
understanding = video.understand(
segmentation = { ... }, # run-level
transform = { ... }, # run-level
analyzers = [
{
"type" : "vlm" , # analyzer-level
"name" : "scene" ,
"inputs" : [ ... ],
"sampling" : { ... },
"config" : { ... },
}
],
)
```

## [ Run-level options](#run-level-options)

Run-level options belong directly on `video.understand(...)` and affect the whole understanding run.

| Option         | Type   | Required   | Default                             | Use when...                                                    |
|----------------|--------|------------|-------------------------------------|----------------------------------------------------------------|
| `analyzers`    | list   | yes        | n/a                                 | You want to define what artifacts to create.                   |
| `segmentation` | dict   | no         | `{"type": "shot", "threshold": 30}` | You need control over visual time ranges for visual analyzers. |
| `transform`    | dict   | no         | none                                | You want to resize or preprocess media for the run.            |
| `callback_url` | string | no         | none                                | You want async completion notifications.                       |

### [ segmentation : visual time ranges](#segmentation-visual-time-ranges)

`segmentation` controls how VideoDB splits the video into scenes, which are the timestamped ranges that visual analyzers run on and attach their outputs to. Use `time` for fixed-length ranges, or `shot` to split on the video's own scene changes.

| Segmentation type   | Options     | Best for                                                                   |
|---------------------|-------------|----------------------------------------------------------------------------|
| `time`              | `seconds`   | fixed-length time ranges, live streams, surveillance, long unedited videos |
| `shot`              | `threshold` | edited videos with cuts, films, ads, sports clips, trailers                |

Time-based segmentation:

```
segmentation = { "type" : "time" , "seconds" : 5 }
```

| Option    | Values   | Description              |
|-----------|----------|--------------------------|
| `type`    | `"time"` | Fixed-duration scenes.   |
| `seconds` | number   | Scene length in seconds. |

Shot-based segmentation:

```
segmentation = { "type" : "shot" , "threshold" : 30 }
```

| Option      | Values   | Description                                                                |
|-------------|----------|----------------------------------------------------------------------------|
| `type`      | `"shot"` | Scenes are based on visual scene changes.                                  |
| `threshold` | number   | Sensitivity for detecting cuts; higher values usually create fewer splits. |

### [ transform : media preparation](#transform-media-preparation)

`transform` applies preprocessing to the media before analyzers run, such as resizing the frames to reduce cost.

| Option       | Values                             | Use when...                         |
|--------------|------------------------------------|-------------------------------------|
| `resolution` | string such as `"480p"` , `"720p"` | You want to reduce cost or latency. |

Example:

```
understanding = video.understand(
analyzers = [{ "type" : "vlm" }],
transform = { "resolution" : "480p" },
)
```

## [ Analyzer options](#analyzer-options)

Each item in `analyzers` defines one analyzer and the artifact it should produce.

| Field      | Type            | Required   | Default               | Use when...                                                                                                         |
|------------|-----------------|------------|-----------------------|---------------------------------------------------------------------------------------------------------------------|
| `type`     | string          | yes        | n/a                   | You choose what analysis to run.                                                                                    |
| `name`     | string          | no         | type-specific default | You need a custom output key or multiple analyzers of the same type.                                                |
| `inputs`   | list of strings | no         | none                  | One analyzer should use artifacts from earlier analyzers. VLM prompts can reference them with `{{inputs.<name>}}` . |
| `sampling` | dict            | no         | type-specific default | Visual analyzers need specific frame selection.                                                                     |
| `config`   | dict            | no         | type-specific default | You need model, prompt, or schema control.                                                                          |

### [ Analyzer type : choose the artifact](#analyzer-type-choose-the-artifact)

`type` chooses which analyzer runs and which artifact shape is produced.

| Type                   | Default artifact name   | Produces                                           |
|------------------------|-------------------------|----------------------------------------------------|
| `spoken_words`         | `transcript`            | timed spoken text                                  |
| `object_detection`     | `objects`               | object labels, counts, scores, boxes               |
| `vlm`                  | `scene`                 | scene descriptions and structured visual reasoning |
| `ocr`                  | `ocr`                   | visible text                                       |
| `brand_detection`      | `brands`                | brand/logo signals                                 |
| `activity_recognition` | `activity`              | activities/actions                                 |
| `location_detection`   | `location`              | setting/location signals                           |

### [ Analyzer name : output keys](#analyzer-name-output-keys)

`name` controls the analyzer name used with `get_analyzer(name)` and `inputs` . It is optional. If you omit it, VideoDB uses the default artifact name for the [analyzer type](#analyzer-type-choose-the-artifact) . You need `name` when you want to:

1. choose a stable analyzer name for output lookup
2. reference another analyzer through `inputs`
3. run multiple analyzers of the same type
4. create readable artifact names for downstream steps

Example with two VLM analyzers:

```
understanding = video.understand(
analyzers = [
{
"type" : "vlm" ,
"name" : "scene_summary" ,
"config" : { "prompt" : "Summarize this scene." },
},
{
"type" : "vlm" ,
"name" : "safety_events" ,
"config" : { "prompt" : "Detect unsafe behavior and hazards." },
},
],
)

understanding.wait_until_complete()
summary = understanding.get_analyzer( "scene_summary" ).get_output()
safety = understanding.get_analyzer( "safety_events" ).get_output()
```

### [ Analyzer inputs : reuse earlier artifacts](#analyzer-inputs-reuse-earlier-artifacts)

`inputs` declares which earlier artifacts a VLM analyzer can use. Reference those artifacts in the VLM prompt with `{{inputs.<name>}}` , where `<name>` is the analyzer `name` .

```
{
"type" : "vlm" ,
"name" : "scene" ,
"inputs" : [ "objects" , "transcript" , "ocr" ],
"config" : {
"prompt" : (
"Describe this scene using video frames as primary evidence. \n\n "
"Spoken words: \n "
" {{ inputs.transcript }} \n\n "
"Detected objects: \n "
" {{ inputs.objects }} \n\n "
"Visible text: \n "
" {{ inputs.ocr }} "
),
},
}
```

VideoDB injects compact, scene-aligned context for each referenced input. For example, `{{inputs.transcript}}` renders spoken text for the scene, while `{{inputs.objects}}` renders object labels/counts from the matching object artifact. Rules:

- Input names must match earlier analyzer `name` values.
- A placeholder such as `{{inputs.transcript}}` must reference an input listed in `inputs` .
- If `inputs` are provided but the prompt has no `{{inputs.*}}` placeholders, VideoDB appends a compact input context block after the prompt.
- Treat injected inputs as evidence/context; write the prompt so frames remain the primary visual source when needed.

### [ Analyzer sampling : frame selection](#analyzer-sampling-frame-selection)

Sampling is per analyzer. It mainly applies to visual and VLM-backed analyzers such as `object_detection` , `vlm` , `ocr` , `brand_detection` , `activity_recognition` , and `location_detection` .

| Strategy   | Required fields   | Best for                                                  | Example                                     |
|------------|-------------------|-----------------------------------------------------------|---------------------------------------------|
| `uniform`  | `frame_count`     | a fixed number of representative frames across each scene | `{"strategy": "uniform", "frame_count": 8}` |
| `interval` | `every`           | monitoring motion or frequently changing scenes           | `{"strategy": "interval", "every": 1}`      |

`every` is in seconds. `{"strategy": "interval", "every": 1}` samples one frame per second within each scene. `frame_count` is the total number of frames distributed evenly inside each scene. Use `{"strategy": "uniform", "frame_count": 1}` when you want one representative frame from the middle of every scene. How to choose sampling:

| Content / goal                     | Recommended sampling                          |
|------------------------------------|-----------------------------------------------|
| one representative frame per scene | `uniform` with `frame_count: 1`               |
| general scene understanding        | `uniform` with 4-8 frames                     |
| motion-heavy content               | `uniform` with more frames                    |
| regular sampling within each scene | `interval` with the desired number of seconds |
| lower cost/latency                 | fewer frames or lower resolution              |

### [ Analyzer config : models, prompts, and schemas](#analyzer-config-models-prompts-and-schemas)

Use `"default"` or omit `model` unless you need a specific model. For understanding analyzers, model selection is primarily exposed for VLM-backed analyzers and object detection.

#### [ spoken\_words](#spoken_words)

| Config     | Values                                                                                                     | Description             |
|------------|------------------------------------------------------------------------------------------------------------|-------------------------|
| `language` | [supported language code](\pages\core-concepts\supported-languages) , such as `en` , `hi` , `ja` , or `zh` | Optional language hint. |

#### [ object\_detection](#object_detection)

| Config       | Values                        | Description                                                                                       |
|--------------|-------------------------------|---------------------------------------------------------------------------------------------------|
| `model`      | `default` , `rtdetr-v2-r50vd` | Object detection model.                                                                           |
| `sandbox_id` | string                        | Required when `model` is a sandbox-backed object detection model; omit for hosted/default models. |

Supported object labels

The default object detection model supports the COCO 80-label vocabulary. Outputs use label strings such as `person` , `car` , `cell phone` , and `laptop` . `person` , `bicycle` , `car` , `motorbike` , `aeroplane` , `bus` , `train` , `truck` , `boat` , `traffic light` , `fire hydrant` , `stop sign` , `parking meter` , `bench` , `bird` , `cat` , `dog` , `horse` , `sheep` , `cow` , `elephant` , `bear` , `zebra` , `giraffe` , `backpack` , `umbrella` , `handbag` , `tie` , `suitcase` , `frisbee` , `skis` , `snowboard` , `sports ball` , `kite` , `baseball bat` , `baseball glove` , `skateboard` , `surfboard` , `tennis racket` , `bottle` , `wine glass` , `cup` , `fork` , `knife` , `spoon` , `bowl` , `banana` , `apple` , `sandwich` , `orange` , `broccoli` , `carrot` , `hot dog` , `pizza` , `donut` , `cake` , `chair` , `sofa` , `pottedplant` , `bed` , `diningtable` , `toilet` , `tvmonitor` , `laptop` , `mouse` , `remote` , `keyboard` , `cell phone` , `microwave` , `oven` , `toaster` , `sink` , `refrigerator` , `book` , `clock` , `vase` , `scissors` , `teddy bear` , `hair drier` , `toothbrush`

#### [ vlm](#vlm)

| Config       | Values                                          | Description                                                                                                                                      |
|--------------|-------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| `model`      | `default` , hosted tier, or supported VLM model | VLM model or tier. See supported values below.                                                                                                   |
| `sandbox_id` | string                                          | Required when `model` is an open-weight/Sandbox Compute model; omit for hosted tiers such as `default` , `mini` , `base` , `pro` , and `ultra` . |
| `prompt`     | string                                          | Instruction for what the VLM should extract. Can include `{{inputs.<name>}}` placeholders for declared `inputs` .                                |
| `schema`     | object                                          | Optional structured output shape.                                                                                                                |

Supported hosted tiers:

| Tier    | Use when...               |
|---------|---------------------------|
| `mini`  | Lowest cost/latency.      |
| `base`  | Default balanced option.  |
| `pro`   | Higher quality reasoning. |
| `ultra` | Highest quality tier.     |

#### [ Sandbox VLM models](#sandbox-vlm-models)

For open-weight VLM models, start a compatible sandbox first and pass `sandbox_id` inside the analyzer `config` . Hosted tiers such as `default` , `mini` , `base` , `pro` , and `ultra` do not need `sandbox_id` .

```
{
"type" : "vlm" ,
"name" : "scene" ,
"config" : {
"model" : "google/gemma-4-31B-it-FP8" ,
"sandbox_id" : sandbox.id,
"prompt" : "Describe the scene, people, actions, and setting." ,
},
}
```

Sandbox setup, model tiers, and validation live in the dedicated Sandbox docs:

## Sandbox Compute

Create and manage sandbox runtimes.

## Sandbox Models

See supported models and minimum tiers.

#### [ Specialized VLM analyzers](#specialized-vlm-analyzers)

These analyzers use the same VLM model family as `vlm` , with task-specific output shapes.

| Analyzer               | Extracts                                           | Config options   |
|------------------------|----------------------------------------------------|------------------|
| `ocr`                  | visible text, signs, slides, labels, UI text       | `model`          |
| `brand_detection`      | logos, brand names, product labels, sponsorships   | `model`          |
| `activity_recognition` | actions, activities, events, behavior              | `model`          |
| `location_detection`   | setting, place type, indoor/outdoor, scene context | `model`          |

| Config       | Values                                                                 | Description                                                                           |
|--------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| `model`      | `default` , `mini` , `base` , `pro` , `ultra` , or supported VLM model | VLM model or tier used by the analyzer.                                               |
| `sandbox_id` | string                                                                 | Required when `model` is an open-weight/Sandbox Compute model; omit for hosted tiers. |

Use the generic `vlm` analyzer instead if you want to control the prompt or schema directly.

Model availability can vary by workspace and deployment. If a model is omitted, VideoDB uses the current default for that analyzer.

## [ Putting it together](#putting-it-together)

This example shows run-level options and analyzer-level options in the same understanding run.

```
understanding = video.understand(
segmentation = {
"type" : "shot" ,
"threshold" : 30 ,
},
transform = {
"resolution" : "480p" ,
},
analyzers = [
{
"type" : "object_detection" ,
"name" : "objects" ,
"sampling" : {
"strategy" : "interval" ,
"every" : 1 ,
},
"config" : {
"model" : "rtdetr-v2-r50vd" ,
},
},
{
"type" : "spoken_words" ,
"name" : "transcript" ,
"config" : {
"language" : "en" ,
},
},
{
"type" : "vlm" ,
"name" : "scene" ,
"inputs" : [ "objects" , "transcript" ],
"sampling" : {
"strategy" : "uniform" ,
"frame_count" : 8 ,
},
"config" : {
"model" : "base" ,
"prompt" : (
"Describe the scene and activity using the sampled frames, "
"spoken words, and detected objects. \n\n "
"Spoken words: \n "
" {{ inputs.transcript }} \n\n "
"Detected objects: \n "
" {{ inputs.objects }} "
),
"schema" : {
"scene_description" : "string" ,
"activity" : "string" ,
"setting" : "string" ,
},
},
},
],
callback_url = "https://example.com/webhooks/understanding-complete" ,
)
```

## [ Cost and quality tips](#cost-and-quality-tips)

| Goal                   | What to adjust                                                            |
|------------------------|---------------------------------------------------------------------------|
| lower cost             | fewer analyzers, fewer sampled frames, lower `resolution`                 |
| lower latency          | fewer frames, shorter scenes, lower model tier                            |
| better visual detail   | more sampled frames, higher resolution, or a higher model tier            |
| broader coverage       | combine speech, object, OCR, and VLM-backed analyzers                     |
| more structured output | use analyzers with task-specific output shapes, or provide a VLM `schema` |

## [ Next steps](#next-steps)

## Analyzer Outputs

See sample output shapes for each analyzer.

## Create an Index

Turn stored artifacts into retrieval-ready indexes.

## Search and Retrieval

Retrieve moments after artifacts have been prepared for search.

[Output Formats](\pages\ingest\transcoding\output-formats) [Analyzer Outputs](\pages\understand\indexing-pipelines\analyzer-outputs)

⌘ I