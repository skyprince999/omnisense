# VideoDB Sandbox Compute — Experiments & Notes

_Investigated 2026-07-25. Sandbox Compute is **not** in the local `videodb_docs/` scrape (the
feature postdates it). Live docs:
[sandbox-compute](https://docs.videodb.io/pages/core-concepts/sandbox-compute),
[sandbox-models](https://docs.videodb.io/pages/core-concepts/sandbox-models)._

## What it is

Sandbox Compute is a **persistent GPU pool** you provision on demand to run **open-weight models**
(VLMs, Whisper, FLUX, TTS, object detection) inside VideoDB workflows. You create a sandbox, wait
for it to go `active`, then pass its `sandbox_id` to supported generation / understanding APIs so the
job is routed to your dedicated pool instead of the shared hosted models.

Lifecycle: `provisioning → active → stopped` (also `alert` = ready-with-warning, `failed` =
terminal). In this session a medium sandbox went from `provisioning` to `active` in **~11 seconds**.

## Tiers & pricing

| Tier   | Price     | Concurrent | Max runtime | Billing                                    |
|--------|-----------|-----------|-------------|--------------------------------------------|
| small  | $1.00/hr  | 5         | 24 h        | runtime-based, computed on stop, 2-dp hours |
| medium | $3.50/hr  | 3         | 24 h        | same                                       |

Pricing/concurrency is per **tier**, not per model. Sandboxes auto-expire 24 h after creation
(`expires_at`). Billing surfaces under `sandbox_small` / `sandbox_medium` in `GET /billing/usage`.

## Available models

**Small tier**
- Text: `google/gemma-4-E2B-it`, `Qwen/Qwen3-4B`
- Text + vision (VLM): `Qwen/Qwen3.5-9B`
- Speech-to-text: `openai/whisper-large-v3-turbo`
- Text-to-speech: `k2-fsa/OmniVoice`
- Audio generation: `stabilityai/stable-audio-open-1.0`
- Object detection: `rtdetr-v2-r50vd`

**Medium tier**
- Text + vision (VLM): `google/gemma-4-26B-A4B-it`, `Qwen/Qwen3.5-27B`, `google/gemma-4-31B-it`
- Image generation: `black-forest-labs/FLUX.1-dev`

You can pin exact `models=[...]` or request by `model_categories=[...]` (e.g. `"vlm"`,
`"object_detection"`) at creation time.

## SDK usage (requires `videodb >= 0.5.1`)

> The repo `.venv` shipped with `0.4.5`, which has **no** sandbox support and whose
> `generate_image` / `generate_voice` lack the `model_name` / `sandbox_id` params. Upgrade first:
> `pip install -U videodb` (confirm with `pip show videodb` → 0.5.1).

```python
import videodb
from videodb import SandboxTier

conn = videodb.connect()  # SDK reads VIDEO_DB_API_KEY (underscore); repo .env uses VIDEODB_API_KEY

# Create + wait
sandbox = conn.create_sandbox(
    tier=SandboxTier.medium,
    models=["google/gemma-4-31B-it"],      # or: model_categories=["vlm", "object_detection"]
)
sandbox.wait_for_ready(timeout=300, interval=5)
print(sandbox.id, sandbox.status)

# Manage
sandbox.refresh()
for sb in conn.list_sandboxes():
    print(sb.id, sb.status)
sb = conn.get_sandbox(sandbox.id)

# Use it — pass sandbox_id + model_name into the normal APIs
coll = conn.get_collection()

img = coll.generate_image(
    prompt="A dashcam view of an Indian highway at golden hour",
    aspect_ratio="16:9",
    model_name="black-forest-labs/FLUX.1-dev",
    sandbox_id=sandbox.id,
)

understanding = video.understand(analyzers=[{
    "type": "vlm",
    "config": {"model": "google/gemma-4-31B-it", "sandbox_id": sandbox.id,
               "prompt": "Describe the road and traffic"},
}])

# ALWAYS stop when done — you are billed for wall-clock runtime until stopped.
sandbox.stop(grace=True)          # grace=True lets running jobs finish first
sandbox.wait_for_stop(timeout=180, interval=5)
```

## REST API (what the SDK calls under the hood)

Base: `https://api.videodb.io`, header `x-access-token: <API_KEY>`.

| Method & path                       | Purpose                              | Notes |
|-------------------------------------|--------------------------------------|-------|
| `GET  /sandbox`                     | List (paginated: page, page_size)    | `data.sandboxes[]`, `data.total` |
| `POST /sandbox`                     | Create                               | Body `{tier, models[] \| model_categories[]}` |
| `GET  /sandbox/{id}`                | Fetch status                         | |
| `POST /sandbox/{id}/stop`           | Stop                                 | **Body `{"grace": true}` is required** |
| `POST /collection/{cid}/generate/image/` | Image gen on sandbox            | Body adds `model_name`, `sandbox_id` |

Generation is async: the response returns an `output_url` /async-response id; poll it, then poll the
resulting `/job/{id}` until `status: "done"`.

## Gotchas (learned the hard way)

- **`POST /sandbox` with an empty body silently succeeds and creates a _medium_ ($3.50/hr) sandbox.**
  There's no "tier required" error — always pass `tier` explicitly.
- **`POST /sandbox/{id}/stop` returns HTTP 500 if you send no body.** It needs `{"grace": true|false}`.
  Raw `requests.post(..., json={})` is _not_ enough — the key must be present. The 0.5.1 SDK's
  `sandbox.stop()` sends this correctly; a bare REST call without it will spin on 500s.
- The SDK env var is **`VIDEO_DB_API_KEY`** (underscore). The repo `.env` and docs use
  `VIDEODB_API_KEY`. Set both before `connect()`.
- `videodb 0.4.5` (the version originally in `.venv`) has none of the sandbox methods and older
  generation signatures — the upgrade to 0.5.1 is mandatory for everything above.

## Session experiment log (2026-07-25)

Ran end-to-end against the live account (`aakash@thinkevolveconsulting.com`, plan `Free_v1`):

1. Discovered the feature via `GET /billing/usage` (cost_metric listed `sandbox_small` / `sandbox_medium`).
2. `POST /sandbox {}` → created **`bx-746fc8b7f66244a1`** ("titanium-nexus-1eae"), **medium** tier,
   region `us-east-1`, models `[gemma-4-26B-A4B-it, Qwen3.5-27B, FLUX.1-dev, gemma-4-31B-it]`.
   `provisioning → active` in ~11 s.
3. Ran **FLUX.1-dev** image generation on it via `POST /collection/{id}/generate/image/` with
   `model_name` + `sandbox_id`. Produced **"Indian Highway Golden Hour Dashcam"**, a 3.1 MB PNG
   (`img-z-019f97e4-4892-75c3-84c1-705c5ed33472`) now in the default collection.
4. Stopped the sandbox cleanly (after finding the `grace` body requirement). Ran **~0.22 h**
   (`started 06:06:43Z → stopped 06:19:52Z`).

**Cost:** credit balance 996.94 → **994.47** (~2.5 credits total for the session, of which
`sandbox_medium` = 0.22 h). Final state: sandbox **stopped**, nothing left running (1 sandbox on
account, terminal).

## Why this matters for this project

- **`rtdetr-v2-r50vd` (small tier) = cloud-side object detection** — an alternative/complement to the
  local YOLO26 pipeline in `make_detections.py`, no local GPU needed.
- **`whisper-large-v3-turbo`** for transcription of any non-silent footage.
- **Medium VLMs (`gemma-4-31B`, `Qwen3.5-27B`)** can be pointed at the stitched dashcam videos via
  `video.understand(analyzers=[{"type": "vlm", ...}])` for structured scene description — a strong
  demo-day angle beyond the current depth/detection overlay.
