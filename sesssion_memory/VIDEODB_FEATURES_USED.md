# VideoDB features used in this project

An inventory of every VideoDB SDK / platform feature this repo actually touches, where it is
used, and what we learned about it. Compiled from the project's Python scripts, session notes,
and plan documents.

SDK: `videodb` Python package (started on `0.4.5`, upgraded to `>= 0.5.1` for Sandbox Compute).
Auth: `VIDEODB_API_KEY` read from `.env`; note the SDK itself looks for `VIDEO_DB_API_KEY`
(underscore) when no key is passed explicitly, so every script passes `api_key=` directly.

---

## Summary table

| Area | Feature | Used in | Status |
|---|---|---|---|
| Connection | `videodb.connect()`, `conn.get_collection()` | every script | ✅ core |
| Billing | `conn.check_usage()` + `cost_metric` rate table | `videodb_cost.py`, all slice scripts | ✅ core |
| Ingest | `coll.upload(file_path=, name=)` | `stitch_and_upload.py`, `upload_stitched.py`, `check_and_upload.py` | ✅ core |
| Catalog | `coll.get_videos()`, `coll.get_video(id)` | most scripts | ✅ core |
| Indexing | `video.index_scenes(...)` (time-based + prompt) | `stitch_and_upload.py`, `upload_stitched.py`, `videodb_smoketest.py`, `videodb_prompt.py` | ✅ core |
| Indexing | `video.list_scene_index()`, `video.get_scene_index(id)` | `videodb_smoketest.py`, `videodb_prompt.py` | ⚠️ status API unreliable |
| Indexing | `video.index_scenes(scenes=[...])` — custom annotations | `videodb_slices*.py --index` | ✅ used |
| Scenes | `video.extract_scenes(...)`, `list/get_scene_collection()` | `videodb_slices.py` v1–v4, `videodb_error.py` | ✅ used |
| Vision | `scene.describe(prompt=, model_name=)` | `videodb_slices.py` v1–v4, `videodb_error.py` | ✅ used |
| Vision | `scene.describe(sandbox_id=)` | `videodb_sandbox_smoketest.py` | ❌ broken server-side |
| Search | `video.search()` / `coll.search()` with `IndexType.scene` | `videodb_query.py`, `videodb_smoketest.py`, `videodb_prompt.py` | ✅ core |
| Search | `results.get_shots()`, `results.compile()` (HLS URL) | `videodb_query.py`, `videodb_smoketest.py` | ✅ used |
| Understanding | `video.understand(segmentation=, analyzers=[vlm])` | `videodb_slices_v5.py`, `videodb_sandbox_understand_smoketest.py` | ✅ the v5 backbone |
| Sandbox | `conn.create_sandbox()`, `list/get_sandbox`, `stop`, `wait_for_*` | `videodb_sandbox_*.py`, `videodb_slices_v5.py`, `quickstart_generate_audio.py` | ✅ used |
| Generation | `coll.generate_voice()` + `audio.generate_url()` | `quickstart_generate_audio.py` | ✅ tried (prod TTS went to Sarvam) |
| Errors | `videodb.exceptions.InvalidRequestError`, `VideodbError` | most scripts | ✅ core |

---

## 1. Connection, collection, and account

```python
from videodb import connect
conn = connect(api_key=api_key)
coll = conn.get_collection()          # the default collection — no custom collections created
```

Everything in the project lives in the **default collection**. No use of
`create_collection` / `list_collections` / multiple collections.

### Usage & cost metering — `conn.check_usage()`

Used heavily because VideoDB exposes **no per-request cost or token metadata**. The response
carries account-level cumulative counters plus a `cost_metric` rate table (credits per unit), so
`videodb_cost.py` measures the cost of an operation by snapshotting before/after and diffing:

```bash
python videodb_cost.py --mark     # snapshot
... run an index / a batch of describes ...
python videodb_cost.py --diff     # per-line-item units, rate, credits spent
```

Fields consumed: `credit_balance`, `credit_used`, `plan_id`, `email`, `cost_metric`, and the
per-line-item counters (`llm_basic` / `llm_pro` / `llm_ultra`, `indexing_bundle_*`,
`sandbox_small` / `sandbox_medium`). The slice pipelines call `check_usage()` inline to enforce
a **dollar budget lock** mid-run, and the sandbox smoke tests use it to report the credit delta
of a single sandbox session.

Caveat noted in the script: counters are account-wide (concurrent activity pollutes a diff) and
lag slightly behind the request.

## 2. Ingest — upload

```python
video = coll.upload(file_path=str(path), name=path.stem)
video.id      # m-xxxxx
```

Three scripts upload, all sharing the same idempotency approach:

- **`stitch_and_upload.py`** — stitches raw 1-minute dashcam clips into per-trip segments with
  ffmpeg, then uploads each segment.
- **`upload_stitched.py`** — uploads whatever is already in `stitched/`.
- **`check_and_upload.py`** — treats VideoDB as the source of truth: calls `coll.get_videos()`,
  diffs the remote name set against local `stitched/*.mp4` stems, uploads only what's missing.

Practical constraints discovered:

- **Upload size limit** ≈ 1000 MB on the current tier (`MAX_UPLOAD_MB`). Larger files must be
  split first (`split_video.py`), which produces a `<stem> parts/` folder plus a
  `<stem>.parts.json` offset sidecar.
- **Transcode failures**: 14 stitched videos were rejected by VideoDB with "Transcode failed"
  and were moved to `stitched_reject/`.
- `--strip-audio` exists in `check_and_upload.py` because the dashcam clips are uploaded silent.
- `coll.upload(url=...)` (YouTube / S3 / direct URL ingest) is documented in `SESSION_NOTES.md`
  but **never used** — all ingest here is local files.
- The notebook also passes `description=` on upload.

## 3. Scene indexing — the core "video-RAG" step

```python
from videodb import SceneExtractionType

index_id = video.index_scenes(
    extraction_type=SceneExtractionType.time_based,
    extraction_config={"time": 10, "select_frames": ["first"]},
    prompt=SCENE_PROMPT,           # dashcam-targeted: road type, traffic, weather, hazards…
    model_name=model,              # "basic" | "pro" | "ultra" (server default: ultra)
    name=f"dashcam-index {stem}",
)
```

Sampling used across scripts: `time` of **10 s** (upload pipelines), **25 s**
(`videodb_smoketest.py`), configurable via `--time` in `videodb_prompt.py`; always
`select_frames: ["first"]`.

Related calls:

- `video.list_scene_index()` → list of `{scene_index_id, status, name}` — used to find and reuse
  an existing index instead of paying to rebuild.
- `video.get_scene_index(idx_id)` → the scene records themselves (`start`, `end`, `description`).
- **Custom scene annotation**: `videodb_slices*.py --index` sets `scene.description = <our own
  analysis text>` on extracted scenes and pushes them with
  `video.index_scenes(scenes=indexable, name=...)`, making locally computed analysis searchable
  through VideoDB's own semantic search.

### Two significant quirks

1. **The status API lies.** Indexes routinely report `processing → failed`, yet the scene
   descriptions were generated, embedded, and *are* searchable — search returns hits for them,
   and re-running `index_scenes` gets back `"Scene index with id X already exists … status:
   done"` from the create endpoint, directly contradicting `list_scene_index()`. The scripts
   therefore treat the **create endpoint's duplicate-check message as authoritative**, parsing
   the index id out of the exception text with a regex. `get_scene_index()` refuses to return
   records for a "failed" index, so `videodb_prompt.py` has a fallback path that recovers the
   answers via search instead.
2. **De-duplication is by (llm_tier, prompt)** — running the same prompt on the same video again
   returns the existing index rather than re-billing.

### `index_spoken_words()` — evaluated, deliberately skipped

Listed as Phase-1 item 1.4 in the roadmap, but every dashcam clip is silent (audio stripped at
ingest), so it's a no-op here. It returns `None` rather than an index id.

## 4. Scene extraction + per-scene VLM description

The slice pipelines (v1–v4) work at a finer granularity than indexing, by extracting scenes and
running a synchronous vision call per scene:

```python
sc = video.extract_scenes(
    extraction_type=SceneExtractionType.time_based,
    extraction_config={"time": slice_s, "frame_count": frames},
)
sc.id, sc.scenes                       # SceneCollection
scene.start, scene.end, scene.description

text = scene.describe(prompt=prompt, model_name="basic")   # synchronous VLM call
```

- `video.list_scene_collection()` / `video.get_scene_collection(cid)` are used to **reuse** an
  existing collection whose `config` matches (`time`, `frame_count`) instead of re-extracting.
- `scene.describe()` is synchronous and has **no batch form** — this is what made v1–v4
  expensive: a *chained* prompt design (prompt 1 → response 1 substituted into prompt 2 → …)
  meant 2+ vision calls per slice, per video.
- `model_name` tiers for describe: `basic` / `pro` / `ultra` (default `basic` in these scripts
  for cost). `videodb_error.py` exists specifically to probe all three tiers and dump the raw
  error when a tier runs out of budget.

## 5. Search — semantic scene search

```python
from videodb import IndexType

res = video.search(query, index_type=IndexType.scene,
                   score_threshold=0.45, result_threshold=8)   # single video
res = coll.search(query, index_type=IndexType.scene, ...)      # whole collection

for shot in res.get_shots():
    shot.start, shot.end, shot.text, shot.search_score
    shot.video_id, shot.video_title, shot.scene_index_id

res.compile()      # -> stream.videodb.io/….m3u8 — a playable reel of just the matching moments
```

- Both **per-video** (`videodb_query.py`) and **collection-wide** (`videodb_smoketest.py`)
  search are used.
- `res.compile()` producing an HLS URL of the matched shots is the demo money-shot: type a
  question, get a playable clip reel. (`results.play()` and `shot.play()` appear in
  `Sample Code.ipynb`.)
- `score_threshold` ≈ **0.45** was found to be the right strictness for demos — the default
  surfaced generic urban scenes for queries like "toll plaza".

### Search gotchas found

- **An empty result set raises `InvalidRequestError`** instead of returning `[]`. Every call
  site wraps search in a try/except that maps that exception to "no matches".
- **The `index_id` search parameter is not honored server-side** — shots from other indexes come
  back anyway, so `videodb_prompt.py` filters client-side on `shot.scene_index_id`.
- **Each query returns only the top ~15 shots.** To recover *all* answers of a prompt-index,
  `videodb_prompt.py` fires several differently-worded queries and merges results until every
  expected time window is covered.
- `filter=[{"trip_id": ...}]` metadata filtering appears in `Sample Code.ipynb` only; not used
  in the pipelines.

## 6. `video.understand()` — batch multi-modal analysis

This is what **v5 of the slice pipeline** is built on, and it replaced the chained
`scene.describe()` design entirely (v1–v4 blew the budget; understand() is one pass).

```python
understanding = video.understand(
    segmentation={"type": "time", "seconds": slice_seconds},
    analyzers=[{
        "type": "vlm",
        "name": "driving",
        "sampling": {"strategy": "uniform", "frame_count": n},
        "config": {
            "model": "Qwen/Qwen3.5-27B",
            "sandbox_id": sandbox.id,
            "prompt": ANALYZER_PROMPT,
            "schema": ANALYZER_SCHEMA,     # structured JSON output
        },
    }],
)
understanding.id
understanding.wait_until_complete(timeout=…, poll_interval=10)
analyzer = understanding.get_analyzer("driving")
analyzer.is_successful, analyzer.status
output = analyzer.get_output()
```

Notable properties, as documented in `videodb_slices_v5.py`'s own header: it is a **batch,
whole-video, single-pass** API — one prompt applies to every segment, so per-slice chained
reasoning isn't possible, but it is dramatically cheaper and it's the **only working route onto
Sandbox Compute for VLM work**. The `schema` field gives structured JSON per segment, which the
project parses into `driving_signal` (green/amber/red) + coaching text per slice.

## 7. Sandbox Compute (open-weight models on dedicated GPUs)

Documented in `sandbox_experiments.md`; exercised by `videodb_sandbox_smoketest.py`,
`videodb_sandbox_understand_smoketest.py`, `videodb_sandbox_stop.py`, `videodb_slices_v5.py`,
and `quickstart_generate_audio.py --sandbox`.

```python
from videodb import SandboxTier

sandbox = conn.create_sandbox(tier=SandboxTier.medium, models=["Qwen/Qwen3.5-27B"])
                              # or model_categories=["vlm", "object_detection"]
sandbox.wait_for_ready(timeout=300, interval=5)
sandbox.id, sandbox.status, sandbox.tier
sandbox.refresh()

conn.list_sandboxes()
conn.get_sandbox(sandbox_id)

sandbox.stop(grace=True)
sandbox.wait_for_stop(timeout=180, interval=5)
```

- **Tiers used**: `small` ($1.00/hr, 5 concurrent) and `medium` ($3.50/hr, 3 concurrent).
  Billed on wall-clock runtime, computed at stop, surfacing as `sandbox_small` /
  `sandbox_medium` in usage. Auto-expire 24 h after creation.
- **Models used**: `Qwen/Qwen3.5-9B` (small VLM), `Qwen/Qwen3.5-27B` (medium VLM),
  `k2-fsa/OmniVoice` (TTS).
- Provisioning is fast — `provisioning → active` in ~8–14 s across every run.
- Because an idle sandbox keeps billing, **every script stops its sandbox in a `finally` block**,
  and `videodb_sandbox_stop.py` / `--list-stop` exist as emergency cleanup that stops every live
  sandbox on the account.

### Bug found and reported: `scene.describe(sandbox_id=…)` is broken

`SANDBOX_BUG_REPORT.md` documents it in full: routing a scene description to a sandbox produces
a **doubled frame-image URL** (a storage bucket base prepended to an already-absolute URL) and
404s. Reproduced on **every tier and model** tested. The same sandbox works fine via
`video.understand()`, and `scene.describe()` without `sandbox_id` works fine — so the defect is
in the sandbox-side frame URL construction. `video.understand(analyzers=[{"type": "vlm", …}])`
is the confirmed workaround and is what v5 uses.

## 8. Generation APIs

```python
audio = coll.generate_voice(
    text=text, voice_name="Default", wait=True, timeout=600,
    model_name="k2-fsa/OmniVoice", sandbox_id=sandbox.id,   # optional: route to a sandbox
)
audio.id
url = audio.generate_url()      # playable / downloadable URL for the generated Audio asset
```

`quickstart_generate_audio.py` exercises text-to-speech both ways: the default **hosted
ElevenLabs** model, and a self-hosted **OmniVoice** model on a small sandbox. The generated
audio is stored as an Asset in the collection.

Note: the shipped voiceover pipeline (`make_slice_audio.py`, `sarvam_tts.py`) ultimately uses
**Sarvam AI's bulbul** rather than VideoDB's generate_voice for the per-slice coaching nudges —
VideoDB TTS was evaluated, not adopted.

`coll.generate_image(prompt=…, aspect_ratio=…, model_name="black-forest-labs/FLUX.1-dev",
sandbox_id=…)` is documented in `sandbox_experiments.md` as the image-generation route onto a
sandbox, but no script in the repo calls it.

## 9. Error handling

```python
from videodb.exceptions import InvalidRequestError, VideodbError
```

Both are caught throughout. The project leans on **parsing exception message text** in two
places where the API's happy path is unreliable: recovering an existing `scene_index_id` from
`"index with id X already exists"`, and detecting `"status: done"` in that same message.
`videodb_error.py` is a dedicated diagnostic that dumps the full error payload per model tier.

---

## Features considered but not used

Surveyed in `SESSION_NOTES.md` and the `Good use case — dashcam footage.md` roadmap, but not
implemented in this repo:

| Feature | Why not |
|---|---|
| `index_spoken_words()` / `index_visuals()` | Footage is silent; scene indexing covers the visual side |
| **Timeline / editor API** (`Timeline`, `Track`, `Clip`, `VideoAsset`) | Programmatic highlight-reel editing — never built; `res.compile()` covered the clip-reel need |
| **RTStream** (live streams, `create_rtstream`, rtstream scene indexing) | No live camera source in this project |
| **Events & Alerts** (`conn.create_event`, `index.create_alert`, webhooks) | Belongs to the live-intelligence path we didn't take |
| **CaptureSession** (desktop/screen capture) | Not relevant to recorded dashcam footage |
| **Dub / translate video** (`dub_video`, `translate_video`) | Content-factory use case, not this one |
| `generate_image` / `generate_video` / `generate_text` | Only `generate_voice` was exercised |
| **Director** (agent framework, vendored in `Director/`) | Cloned for reference; no integration built |
| **Multiple collections**, metadata `filter=` search | Everything lives in the default collection |

---

## Reference material in the repo

- `videodb_docs/` — 266 scraped markdown pages of docs.videodb.io (via `scrape_videosdb_docs.py`).
  Grep this for API/SDK signatures rather than guessing. **Sandbox Compute postdates the scrape**
  and is not in it — see `sandbox_experiments.md` and the live docs instead.
- `Sample Code.ipynb` — runnable VideoDB snippets (upload, index, search, `results.play()`).
- `SANDBOX_BUG_REPORT.md` — the `scene.describe(sandbox_id=…)` defect, with repro and workaround.
- `PHASE1_SEARCH_PLAN.md` / `SESSION_NOTES_2026-07-24.md` — the search pipeline design and the
  "status API lies" discovery.
