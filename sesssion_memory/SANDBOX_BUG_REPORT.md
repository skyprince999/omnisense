# Bug report: `scene.describe(sandbox_id=…)` fails with a doubled frame-image URL (404)

## Summary

When routing a scene description to **Sandbox Compute** via
`Scene.describe(..., sandbox_id=<id>)`, the request fails. The sandbox worker
tries to fetch the scene's frame image from a **malformed URL that has the
storage bucket prefix duplicated**, so the fetch 404s and the describe call
returns HTTP 500.

The **same scenes describe successfully on the hosted path** (`Scene.describe`
with a hosted tier and no `sandbox_id`), so the defect is specific to the
sandbox routing / frame-URL construction, not the video, the frames, or the
account.

## Environment

- SDK: `videodb` **0.5.1** (Python 3.12, Windows)
- Reproduced on **both** sandbox tiers/models — the defect is tier- and
  model-independent:
  - tier **medium**, model **`Qwen/Qwen3.5-27B`** — active in ~14 s
  - tier **small**, model **`Qwen/Qwen3.5-9B`** — active in ~8 s
- Created with: `conn.create_sandbox(tier=SandboxTier.<tier>, models=[<model>])`
- Sandbox provisioned correctly in every case (reached `status="active"`), and
  `stop()`/`wait_for_stop()` succeeded; only the frame fetch inside describe fails.
- Account (`user_id`): `u-4d5c7ef5-87bd-4b13-8173-eca88323e817`
- Video (`video_id`): `m-z-019f8a58-9238-72e3-b9fa-c5552b3421bf`
  ("Good videos [2025-09-28 1342-1342] (silent)", 24 s)
- Sandbox IDs seen: `bx-d22e8af0770d4038`, `bx-43379c11cd204984`,
  `bx-d68dc6b0285a43c3` (medium), `bx-16db0c0a213c41d0` (small)
- Occurred: 2026-07-25 (UTC ~08:24 and re-confirmed ~09:01)

## Reproduction

```python
from videodb import connect, SceneExtractionType, SandboxTier

conn = connect(api_key=...)
coll = conn.get_collection()
video = coll.get_video("m-z-019f8a58-9238-72e3-b9fa-c5552b3421bf")

sandbox = conn.create_sandbox(tier=SandboxTier.medium, models=["Qwen/Qwen3.5-27B"])
sandbox.wait_for_ready(timeout=600, interval=5)   # -> active

sc = video.extract_scenes(
    extraction_type=SceneExtractionType.time_based,
    extraction_config={"time": 19, "frame_count": 2},
)
scene = sorted(sc.scenes, key=lambda s: s.start or 0)[0]   # tt19sff2-0.0-19.0

# This raises:
scene.describe(
    prompt="Describe the road, weather and vehicles.",
    model_name="Qwen/Qwen3.5-27B",
    sandbox_id=sandbox.id,
)

sandbox.stop()
```

## What happens

The call raises `InvalidRequestError` wrapping a 500, whose body is a 404 on the
frame image URL:

```json
{
  "code": 500,
  "message": "404, message='Not Found', url='https://storage.googleapis.com/videodbx1.appspot.com/https://storage.googleapis.com/videodbx1.appspot.com/media/u-4d5c7ef5-.../m-z-019f8a58-.../frames/frm-scn-tt19sff2-0.0-19.0-4.733/img-4a94b829-....png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=firebase-adminsdk-...&X-Goog-Expires=215999&...&X-Goog-Signature=...'",
  "success": false
}
```

## Root cause (the actual bug)

The fetched URL has the bucket base **prepended twice**. Broken down:

```
https://storage.googleapis.com/videodbx1.appspot.com/   <-- prefix #1 (added by the sandbox path)
https://storage.googleapis.com/videodbx1.appspot.com/   <-- prefix #2 (the value was ALREADY an absolute URL)
media/u-4d5c7ef5-.../m-z-019f8a58-.../frames/frm-scn-tt19sff2-0.0-19.0-4.733/img-....png?X-Goog-...
```

It looks like the sandbox frame-fetch does `base_url + frame_path` where
`frame_path` is already a fully-qualified absolute URL, so the base is
concatenated onto an absolute URL and the result 404s.

Note the frame object's own `.url` reported by the SDK is on a **different
host** entirely:

```
https://storage.videodb.io/media/u-4d5c7ef5-.../m-z-019f8a58-.../frames/...
```

So the sandbox path is not only doubling the prefix, it is also resolving frames
to `storage.googleapis.com/videodbx1.appspot.com/...` rather than the
`storage.videodb.io/...` host the frames actually report.

## Scope / what we ruled out

- **Not stale data.** Reproduced on a freshly `extract_scenes()`-ed collection
  (`tt19sff2`) as well as a previously-existing one (`st20m15f1`) — identical
  doubled-URL 404 both times.
- **Not the video/frames.** The exact same scenes describe fine via the hosted
  path: `scene.describe(prompt=..., model_name="basic")` (no `sandbox_id`)
  returns normal descriptions. **Directly confirmed the frame is fetchable:**
  a plain `requests.get()` of the scene frame's own signed URL
  (`frames[0].url`) returns **HTTP 200 with a 514,400-byte PNG** — so the image
  exists and is reachable; only the sandbox path's *doubled* URL 404s.
- **Not the tier or the model.** Reproduced identically on medium/`Qwen3.5-27B`
  and small/`Qwen3.5-9B`. Same doubled-prefix 404 in both — rules out a
  model-specific or tier-specific worker.
- **Not sandbox provisioning.** The sandbox reaches `active` quickly and
  `stop()`/`wait_for_stop()` work; only the frame fetch inside describe fails.
- Reproduced with `frame_count` = 1, 2, and 3.

## Impact

Sandbox Compute cannot currently be used for VLM scene description via
`Scene.describe(sandbox_id=…)` — every call fails at the frame-fetch step. This
blocks moving a describe-based workflow off the hosted per-tier LLM budget onto
sandbox compute.

## Workaround confirmed: `video.understand()` is NOT affected

The documented `video.understand(analyzers=[{"type": "vlm", "config": {"model",
"sandbox_id"}}])` path **works** — it does not go through the broken frame-URL
construction. Verified 2026-07-25 on the same 24 s clip
(`m-z-019f8a58-...`), both sandbox tiers, run to `status="done"`:

| Tier   | Model             | Sandbox            | Run       | Result |
|--------|-------------------|--------------------|-----------|--------|
| small  | `Qwen/Qwen3.5-9B` | `bx-0f104d26d2b4496a` | `und_9dd3a68923cf40ee` | done (110 s) — but the 9B model **hallucinated** the frame ("speaker grille panels"), so output was wrong despite the pipeline succeeding |
| medium | `Qwen/Qwen3.5-27B`| `bx-4c84f91d150f4c35` | `und_9335bfba612d48ab` | done (143 s) — **accurate** description (rural rainy road, white van ahead, DDPAI-mini watermark, correct timestamp) |

So the interim route onto Sandbox Compute for VLM work is
`video.understand(...)`, not `scene.describe(sandbox_id=...)`. Use **medium /
Qwen3.5-27B** for usable quality; small / 9B produced a clearly wrong description
on this frame. Cost was ~0.03 credits (small) and ~0.14 credits (medium); both
sandboxes stopped cleanly. Repro script: `videodb_sandbox_understand_smoketest.py`.

## Ask

1. Fix the sandbox-side frame URL construction in `scene.describe(sandbox_id=…)`
   so it uses the frame's actual (single, correct-host) signed URL instead of
   prepending a bucket base to an already-absolute URL. `video.understand()`
   already does this correctly and can serve as the reference implementation.

## Session log — 2026-07-25

Investigation timeline for this session, on video
`m-z-019f8a58-...` ("Good videos [2025-09-28 1342-1342] (silent)", 24 s).
Every sandbox below was stopped after use; a final `list_sandboxes()` check
showed **0 active** at the end.

1. **`scene.describe()` — medium / `Qwen/Qwen3.5-27B`** (sandbox
   `bx-d68dc6b0285a43c3`). Sandbox active in 14 s; describe **failed** with the
   doubled-prefix frame-URL 404. Ran via `videodb_sandbox_smoketest.py`.
2. **`scene.describe()` — small / `Qwen/Qwen3.5-9B`** (sandbox
   `bx-16db0c0a213c41d0`). Sandbox active in 8 s; **same** doubled-prefix 404 —
   confirming the defect is tier- and model-independent.
3. **Frame-reachability check.** Fetched the scene frame's own signed URL
   (`frames[0].url`) with a plain `requests.get()` → **HTTP 200, 514,400-byte
   PNG**. The frame exists and is reachable; only `describe()`'s doubled URL 404s.
4. **`video.understand()` (VLM analyzer) — small / `Qwen/Qwen3.5-9B`** (sandbox
   `bx-0f104d26d2b4496a`, run `und_9dd3a68923cf40ee`). Completed `done` in 110 s —
   **no URL error**. Output was wrong (9B hallucinated "speaker grille panels"),
   i.e. a model-quality issue, not a pipeline failure.
5. **`video.understand()` (VLM analyzer) — medium / `Qwen/Qwen3.5-27B`** (sandbox
   `bx-4c84f91d150f4c35`, run `und_9335bfba612d48ab`). Completed `done` in 143 s
   with an **accurate** scene description. Ran steps 4–5 via
   `videodb_sandbox_understand_smoketest.py`.

**Conclusion:** `scene.describe(sandbox_id=…)` is broken on all tiers/models;
`video.understand(analyzers=[{"type":"vlm", "config":{…"sandbox_id"}}])` is the
working path — use medium / `Qwen3.5-27B` for usable quality.

**Session cost:** ~0.40 credits total across all five sandbox runs
(describe attempts ~0.02 + ~0.004; understand ~0.03 small + ~0.14 medium).
Balance ended at ~983.76.
