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

- [When to use Sandbox Compute](#when-to-use-sandbox-compute)
- [Create a sandbox](#create-a-sandbox)
- [Pick a model](#pick-a-model)
- [Route jobs to the sandbox](#route-jobs-to-the-sandbox)
- [Use Sandbox with Understanding and Indexing](#use-sandbox-with-understanding-and-indexing)
- [Use Sandbox for object detection](#use-sandbox-for-object-detection)
- [Use Sandbox for generation workflows](#use-sandbox-for-generation-workflows)
    - [OmniVoice text-to-speech](#omnivoice-text-to-speech)
    - [Voice design](#voice-design)
    - [Reusable voice clone](#reusable-voice-clone)
    - [FLUX image generation](#flux-image-generation)
    - [Text generation](#text-generation)
- [Validation and permissions](#validation-and-permissions)
- [Manage sandboxes](#manage-sandboxes)
- [Stop the sandbox](#stop-the-sandbox)
- [Pricing and limits](#pricing-and-limits)
- [Best practices](#best-practices)

[Core Concepts](\pages\core-concepts\overview)

# Sandbox Compute

Copy page

Run supported open-weight and specialized models in VideoDB workflows by starting a sandbox and passing sandbox\_id.

Copy page

Sandbox Compute is VideoDB's managed runtime for supported open-weight and specialized models. Create a sandbox, wait until it is active, then pass `sandbox_id` to supported APIs. VideoDB routes that job to your sandbox runtime instead of the default hosted path. Sandbox is not only an indexing feature. It can power understanding analyzers, indexing pipelines, and generation workflows such as text-to-speech, image generation, audio generation, and text generation. For hosted/default models, omit `sandbox_id` . For Sandbox Compute/open-weight models, pass `sandbox_id` explicitly.

## [ When to use Sandbox Compute](#when-to-use-sandbox-compute)

Use Sandbox Compute when you want:

- **Open-weight model access** for VLM, object detection, speech, audio, image, or text workflows.
- **Specialized models** such as Gemma, Qwen, Whisper, OmniVoice, FLUX, Stable Audio, or RT-DETR.
- **Predictable routing** by pinning a job to a specific sandbox ID.
- **Runtime-based pricing** for compatible workloads.

## [ Create a sandbox](#create-a-sandbox)

Choose a tier based on the largest model you plan to run. Creating a sandbox returns immediately while compute is provisioning.

```
import videodb
from videodb import SandboxTier

conn = videodb.connect()
coll = conn.get_collection()

sandbox = conn.create_sandbox(
tier = SandboxTier.medium,
models = [ "google/gemma-4-31B-it" ],
)

sandbox.wait_for_ready( timeout = 300 , interval = 5 )
print (sandbox.id)
```

You can prepare the sandbox by model category instead of exact model names:

```
sandbox = conn.create_sandbox(
tier = SandboxTier.medium,
model_categories = [ "vlm" , "object_detection" , "image_generation" ],
)

sandbox.wait_for_ready()
```

Supported category names include:

| Category           | Use for                                 |
|--------------------|-----------------------------------------|
| `vlm`              | visual scene understanding models       |
| `object_detection` | object detection models such as RT-DETR |
| `speech_to_text`   | speech recognition models               |
| `text_to_speech`   | speech generation models                |
| `image_generation` | image generation models                 |
| `audio_generation` | audio/music/sound generation models     |
| `text_generation`  | text generation models                  |

Submit sandbox-backed jobs only after the sandbox is active.

## [ Pick a model](#pick-a-model)

Sandbox supports VLMs, speech-to-text, text-to-speech, image generation, audio generation, object detection, and text generation models. Use the smallest sandbox tier that supports the largest model in your workflow.

## Sandbox Models

See the current model catalog and minimum tier for each model.

## [ Route jobs to the sandbox](#route-jobs-to-the-sandbox)

Pass `sandbox_id=sandbox.id` to supported APIs. If `sandbox_id` is omitted, VideoDB uses the hosted/default path. For production workflows with Sandbox models, pass the ID explicitly so routing is predictable.

## [ Use Sandbox with Understanding and Indexing](#use-sandbox-with-understanding-and-indexing)

Sandbox affects the **understanding** step: it controls where the model runs. The **indexing** step is unchanged: index the resulting artifact with `video.index(...)` .

```
sandbox = conn.create_sandbox(
tier = SandboxTier.medium,
models = [ "google/gemma-4-31B-it" ],
)
sandbox.wait_for_ready()

video = coll.get_video( "m-xxx" )

understanding = video.understand(
analyzers = [
{
"type" : "vlm" ,
"name" : "scene" ,
"config" : {
"model" : "google/gemma-4-31B-it" ,
"sandbox_id" : sandbox.id,
"prompt" : "Describe the scene in a clear, concise way." ,
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

Search the index like any other VideoDB index:

```
results = video.semantic_search(
query = "person presenting an AI demo" ,
index_name = "scene" ,
return_fields = [ "scene_description" , "activity" , "setting" ],
)
```

For complete indexing options, see [Create an Index](\pages\understand\indexing-pipelines\create-an-index) .

## [ Use Sandbox for object detection](#use-sandbox-for-object-detection)

For sandbox-backed object detection, choose the detection model in the analyzer config. Configure object filters and aggregations when you create the index.

```
sandbox = conn.create_sandbox(
tier = SandboxTier.small,
models = [ "rtdetr-v2-r50vd" ],
)
sandbox.wait_for_ready()

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

## [ Use Sandbox for generation workflows](#use-sandbox-for-generation-workflows)

Sandbox can also route supported generation jobs. These APIs use `model_name` plus `sandbox_id` .

### [ OmniVoice text-to-speech](#omnivoice-text-to-speech)

```
job = coll.generate_voice(
text = "Welcome to VideoDB Sandbox Compute." ,
model_name = "k2-fsa/OmniVoice" ,
sandbox_id = sandbox.id,
)

audio = job.wait( timeout = 900 , interval = 5 )
print (audio.id)
```

### [ Voice design](#voice-design)

Use `config.instructions` to guide the voice style.

```
job = coll.generate_voice(
text = "Breaking update: your video workflows now have dedicated inference compute." ,
model_name = "k2-fsa/OmniVoice" ,
sandbox_id = sandbox.id,
config = { "instructions" : "A deep, authoritative news anchor voice" },
)

audio = job.wait( timeout = 900 , interval = 5 )
```

### [ Reusable voice clone](#reusable-voice-clone)

Create a voice clone once from a reference audio asset, then reuse it by passing `voice_clone_id` .

```
ref_audio = coll.upload(
url = "https://www.youtube.com/shorts/8GrguhmR6oQ" ,
media_type = "audio" ,
)

voice_clone = coll.create_voice_clone(
ref_audio_id = ref_audio.id,
name = "Product Narrator" ,
description = "Reusable narration voice" ,
ref_text = "Sample reference text for the audio clip" ,
language = "en" ,
)

job = coll.generate_voice(
text = "This narration uses a reusable voice clone." ,
model_name = "k2-fsa/OmniVoice" ,
sandbox_id = sandbox.id,
voice_clone_id = voice_clone.id,
)

audio = job.wait( timeout = 900 , interval = 5 )
```

### [ FLUX image generation](#flux-image-generation)

```
job = coll.generate_image(
prompt = "A futuristic cityscape at sunset, cinematic lighting, high detail" ,
model_name = "black-forest-labs/FLUX.1-dev" ,
sandbox_id = sandbox.id,
config = {
"size" : "1280x720" ,
"num_inference_steps" : 28 ,
"guidance_scale" : 4.0 ,
},
)

image = job.wait( timeout = 900 , interval = 5 )
print (image.id)
```

### [ Text generation](#text-generation)

```
response = coll.generate_text(
prompt = "Summarize the key visual events from this scene description list." ,
model_name = "Qwen/Qwen3.5-9B" ,
sandbox_id = sandbox.id,
max_tokens = 300 ,
temperature = 0.2 ,
)

print (response)
```

## [ Validation and permissions](#validation-and-permissions)

When you pass `sandbox_id` , VideoDB validates that:

1. the sandbox exists and belongs to your workspace/account,
2. the sandbox is active,
3. the sandbox tier supports the requested model,
4. the sandbox was created with a matching `models` or `model_categories` value, when model selection was provided.

If validation fails, create or start a compatible sandbox and retry the job with that sandbox ID.

## [ Manage sandboxes](#manage-sandboxes)

```
# Refresh one sandbox
sandbox.refresh()
print (sandbox.status, sandbox.is_active)

# List sandboxes
for sb in conn.list_sandboxes():
print (sb.id, sb.name, sb.tier, sb.status)

# Get a sandbox by ID
sb = conn.get_sandbox(sandbox.id)
print (sb)
```

## [ Stop the sandbox](#stop-the-sandbox)

Sandbox billing is based on runtime. Stop the sandbox when your workload is complete.

```
sandbox.stop()
sandbox.wait_for_stop( timeout = 120 , interval = 5 )
print ( f "Sandbox { sandbox.id } final status: { sandbox.status } " )
```

## [ Pricing and limits](#pricing-and-limits)

Sandbox billing is runtime-based. Billing is recorded when the sandbox stops and is calculated from `started_at` to `stopped_at` , rounded to 2 decimal hours.

| Sandbox tier   | Price        |
|----------------|--------------|
| `small`        | `$1/hour`    |
| `medium`       | `$3.50/hour` |

| Sandbox tier   |   Concurrent sandbox limit | Max runtime   |
|----------------|----------------------------|---------------|
| `small`        |                          5 | 24 hours      |
| `medium`       |                          3 | 24 hours      |

## [ Best practices](#best-practices)

- Create one sandbox per workflow and reuse it across compatible jobs.
- Use the smallest tier that supports your largest model.
- Use `models=[...]` when you know the exact models your workflow needs.
- Use `model_categories=[...]` when your workflow may use several models in the same category.
- Wait until the sandbox is active before submitting jobs.
- Pass `sandbox_id=sandbox.id` explicitly for production indexing and generation jobs.
- Use `job.wait(timeout=900, interval=5)` for long-running generation jobs.
- Log `sandbox.id` with each job so runs can be debugged or retried.
- Stop the sandbox when work is complete.

## Sandbox Models

See supported models and minimum tiers.

## Understanding Artifacts

Configure analyzers and model selection.

## Create an Index

Index artifacts produced by hosted or sandbox models.

[Supported Languages](\pages\core-concepts\supported-languages) [Sandbox Models](\pages\core-concepts\sandbox-models)

⌘ I