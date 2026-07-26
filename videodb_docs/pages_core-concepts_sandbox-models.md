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

- [Model catalog](#model-catalog)
- [Choose a tier](#choose-a-tier)
- [Where to pass the model name](#where-to-pass-the-model-name)
- [Use a model in Understanding and Indexing](#use-a-model-in-understanding-and-indexing)
- [Use a model in generation APIs](#use-a-model-in-generation-apis)
- [Pricing and limits](#pricing-and-limits)

[Core Concepts](\pages\core-concepts\overview)

# Sandbox Models

Copy page

Available models for VideoDB Sandbox Compute and their minimum tiers.

Copy page

Sandbox models run on VideoDB Sandbox Compute. Pick a model, create a sandbox on a compatible tier, wait until it is active, and pass the sandbox ID to a supported workflow. Sandbox models can be used across VideoDB workflows, including understanding analyzers, indexing pipelines, text-to-speech, image generation, audio generation, and text generation.

Use model names exactly as listed unless your VideoDB team contact gives you an alias.

## [ Model catalog](#model-catalog)

| Model                               | Use case         | Minimum tier   | Good for                                 |
|-------------------------------------|------------------|----------------|------------------------------------------|
| `google/gemma-4-E2B-it`             | text generation  | `small`        | lightweight text generation              |
| `Qwen/Qwen3-4B`                     | text generation  | `small`        | lightweight text generation              |
| `Qwen/Qwen3.5-9B`                   | text and vision  | `small`        | lightweight visual and text reasoning    |
| `openai/whisper-large-v3-turbo`     | speech-to-text   | `small`        | transcription and speech recognition     |
| `k2-fsa/OmniVoice`                  | text-to-speech   | `small`        | TTS, voice design, and voice cloning     |
| `stabilityai/stable-audio-open-1.0` | audio generation | `small`        | text-to-audio and sound generation       |
| `rtdetr-v2-r50vd`                   | object detection | `small`        | object detection workflows               |
| `google/gemma-4-26B-A4B-it`         | text and vision  | `medium`       | higher-quality visual and text reasoning |
| `Qwen/Qwen3.5-27B`                  | text and vision  | `medium`       | larger visual and text reasoning         |
| `black-forest-labs/FLUX.1-dev`      | image generation | `medium`       | text-to-image generation                 |
| `google/gemma-4-31B-it`             | text and vision  | `medium`       | advanced visual and text reasoning       |

## [ Choose a tier](#choose-a-tier)

Use the smallest tier that supports the largest model in your workflow.

```
from videodb import SandboxTier

# Small-tier models: OmniVoice, Whisper, Qwen 9B, lightweight VLMs, and object detection
small_sandbox = conn.create_sandbox(
tier = SandboxTier.small,
model_categories = [ "vlm" , "text_to_speech" , "speech_to_text" , "object_detection" ],
)

# Medium-tier models: FLUX and larger VLMs
medium_sandbox = conn.create_sandbox(
tier = SandboxTier.medium,
model_categories = [ "vlm" , "image_generation" ],
)
```

If a workflow uses both small and medium models, create a `medium` sandbox and reuse it across those jobs.

## [ Where to pass the model name](#where-to-pass-the-model-name)

| Workflow                | Model field             | Sandbox field                |
|-------------------------|-------------------------|------------------------------|
| Understanding analyzers | analyzer `config.model` | analyzer `config.sandbox_id` |
| Generation APIs         | `model_name`            | `sandbox_id`                 |

For hosted/default models, omit `sandbox_id` . For models listed on this page, pass a compatible sandbox ID.

## [ Use a model in Understanding and Indexing](#use-a-model-in-understanding-and-indexing)

Use the sandbox model during understanding, then index the produced artifact with the standard `video.index(...)` interface.

```
sandbox = conn.create_sandbox(
tier = SandboxTier.medium,
models = [ "google/gemma-4-31B-it" ],
)
sandbox.wait_for_ready()

understanding = video.understand(
analyzers = [
{
"type" : "vlm" ,
"name" : "scene" ,
"config" : {
"model" : "google/gemma-4-31B-it" ,
"sandbox_id" : sandbox.id,
"prompt" : "Describe each scene in detail." ,
"schema" : {
"scene_description" : "string" ,
"activity" : "string" ,
"setting" : "string" ,
},
},
}
],
)

understanding.wait_until_complete()
scene = understanding.get_analyzer( "scene" )

video.index(
name = "scene" ,
source = scene,
use_for = [ "semantic" , "query" ],
fields = {
"semantic" : [ "scene_description" , "activity" , "setting" ],
"filter" : [ "activity" , "setting" ],
},
)
```

For object detection, configure the model and sandbox in the analyzer, then choose filter and aggregation fields at indexing time:

```
understanding = video.understand(
analyzers = [
{
"type" : "object_detection" ,
"name" : "objects" ,
"config" : {
"model" : "rtdetr-v2-r50vd" ,
"sandbox_id" : sandbox.id,
},
}
],
)

understanding.wait_until_complete()
objects = understanding.get_analyzer( "objects" )

video.index(
name = "objects" ,
source = objects,
use_for = [ "query" , "aggregate" ],
fields = {
"filter" : [ "object_labels" , "object_counts" ],
"aggregate" : [ "object_labels" ],
},
)
```

## [ Use a model in generation APIs](#use-a-model-in-generation-apis)

Generation APIs use `model_name` and `sandbox_id` .

```
job = coll.generate_image(
prompt = "A cinematic product photo of a smart camera" ,
model_name = "black-forest-labs/FLUX.1-dev" ,
sandbox_id = sandbox.id,
)

image = job.wait( timeout = 900 , interval = 5 )
```

```
job = coll.generate_voice(
text = "Welcome to VideoDB Sandbox Compute." ,
model_name = "k2-fsa/OmniVoice" ,
sandbox_id = sandbox.id,
)

audio = job.wait( timeout = 900 , interval = 5 )
```

## [ Pricing and limits](#pricing-and-limits)

Sandbox pricing and concurrency limits are based on the sandbox tier, not the individual model. See [Sandbox Compute](\pages\core-concepts\sandbox-compute#pricing-and-limits) for current pricing and limits.

## Sandbox Compute

Create, use, and stop sandbox compute.

## Understanding Artifacts

Configure analyzers and model selection.

## Create an Index

Index artifacts produced by sandbox models.

[Sandbox Compute](\pages\core-concepts\sandbox-compute) [Events &amp; Real-time](\pages\core-concepts\events-and-realtime)

⌘ I