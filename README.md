# OmniSense CoPilot

A comprehensive driver behavior monitoring system that provides real-time video understanding and intelligent feedback for dashcam footage. OmniSense processes raw dashcam clips, extracts deep insights through computer vision and video indexing, and delivers contextual audio nudges to guide safer driving behavior.

# [LIVE DEMO LINK](https://omnisense.thinkevolvelabs.com/)

Follow the above link for the LIVE DEMO. Note that the app is hosted on a "cheap" infra so concurrency or cross-device may not work 😊

The live demo has been tested on Windows 11 (Chrome) & Mac (Chrome & Safari)

In case some videos/audios are not playing -- wait for sometime for the video to buffer. Watch the Youtube video below to understand the functionality

# YOUTUBE VIDEO WALKTHROUGH
[![Watch OmniSense Demo](https://img.youtube.com/vi/QDaKcqfJdfM/maxresdefault.jpg)](https://youtu.be/Ui6XwxdK2a8)


## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Data Ingestion Pipeline](#data-ingestion-pipeline)
- [Video Understanding & Inference](#video-understanding--inference)
- [Audio Feedback System](#audio-feedback-system)
- [Setup & Environment](#setup--environment)
- [Common Commands](#common-commands)
- [Data Conventions](#data-conventions)
- [VideoDB Integration](#videodb-integration)
- [Development Notes](#development-notes)
- [Links & References](#links--references)

![OmniSense Logo](assets/OMNI%20SENSE%20.png)

## Project Overview

OmniSense is built around a corpus of Indian dashcam footage and operates three main workstreams:

1. **VideoDB Pipeline** — Ingests raw 1-minute dashcam clips, stitches them into coherent trip videos, uploads them to VideoDB, and creates scene indices for natural-language video search (video-RAG)
2. **Local Computer Vision Pipeline** — Precomputes depth maps (Depth Anything V2) and object detections (YOLOv8) on local GPU, enabling real-time overlay and analysis
3. **Real-time Feedback System** — Monitors driving patterns and delivers contextual audio nudges at moments when the driver can benefit from guidance

There is no build system or test suite—OmniSense is a collection of standalone CLI scripts and self-contained HTML viewers that operate on a directory-based data flow.

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                     Raw Dashcam Footage                         │
│              original_videos/<trip>/YYYYMMDDHHMMSS.mp4         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                ┌──────────▼──────────┐
                │  Stitch & Upload    │
                │   (ffmpeg concat)   │
                └──────────┬──────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│        Stitched Trip Videos (Pipeline Unit of Work)             │
│        stitched/<Trip [date HHMM-HHMM]>.mp4                    │
└────┬──────────────────┬──────────────────────┬──────────────────┘
     │                  │                      │
     │        ┌─────────▼────────┐    ┌────────▼────────┐
     │        │ Depth Extraction │    │ Object Detection│
     │        │ (Depth Anything) │    │ (YOLOv8)        │
     │        └─────────┬────────┘    └────────┬────────┘
     │                  │                      │
     │    ┌─────────────▼──┐    ┌──────────────▼──┐
     │    │ depth/          │    │ detections/     │
     │    │ <stem>.depth.mp4│    │ <stem>.json     │
     │    └─────────────────┘    └─────────────────┘
     │
     │        ┌──────────────────┐
     │        │ VideoDB Upload   │
     │        │ + Scene Index    │
     │        └──────────────────┘
     │
     │    ┌──────────────────────────────┐
     └────▶ Behavior Analysis & Audio    │
          │ Feedback Generation          │
          └──────────────────────────────┘
                      │
                ┌─────▼──────┐
                │ Audio Nudge │
                │ Playback    │
                └─────────────┘
```

### Directory Structure

```
omnisense/
├── original_videos/          # Raw 1-minute dashcam clips by trip
│   └── <trip_name>/
│       ├── YYYYMMDDHHMMSS_SSSS.mp4  # <timestamp>_<duration_sec>.mp4
│       └── ...
│
├── stitched/                 # Per-trip videos (main processing unit)
│   ├── Trip [date HHMM-HHMM].mp4
│   └── ...
│
├── depth/                    # Depth map videos & metadata
│   ├── <stem>.depth.mp4
│   ├── <stem>.depth.metadata.json
│   ├── videos.js             # Dropdown manifest for viewers
│   └── ...
│
├── detections/               # Object detection annotations
│   ├── <stem>.detections.json  # Normalized (0..1) xyxy boxes per frame
│   ├── manifest.json         # Detection index for viewers
│   └── ...
│
├── analysis/                 # Behavioral analysis results
│   ├── <stem>.behavior.json  # Extracted patterns & metrics
│   ├── <stem>.timeline.json  # Timestamped events & opportunities
│   └── ...
│
├── audio_nudges/             # Generated audio feedback
│   ├── <stem>/
│   │   ├── nudge_HHMMSS_TYPE.wav  # Timestamp_category nudge
│   │   └── manifest.json          # Nudge metadata & timing
│   └── ...
│
└── viewers/
    ├── depth_detection_viewer.html    # Depth + YOLO overlay
    ├── trip_dist_viewer_v6.html       # Advanced analytics viewer
    └── serve.py                       # Local dev server (Range support)
```

### Key Abstraction: The Stem

The **`<stem>`** (stitched filename without extension) is the join key across every pipeline stage:

- Source: `stitched/<stem>.mp4`
- Depth data: `depth/<stem>.depth.mp4`
- Detections: `detections/<stem>.detections.json`
- Behavioral analysis: `analysis/<stem>.behavior.json`
- Audio nudges: `audio_nudges/<stem>/nudge_*.wav`

All downstream viewers and processors locate data purely through naming convention.

## Data Ingestion Pipeline

### Stage 1: Raw Clip Collection

Raw dashcam footage arrives as 1-minute clips with standardized naming:

```
YYYYMMDDHHMMSS_SSSS.mp4
└─ Timestamp (UTC) + Duration in seconds
```

Clips are organized into trip folders based on date and route. Multiple trips per day are supported.

### Stage 2: Segment Grouping & Stitching

`stitch_and_upload.py` groups raw clips into logical segments (trips):

- **Segment detection**: Clips are grouped until a gap > `GAP_TOLERANCE_S` (60 seconds) is detected
- **Segment naming**: `<folder> [<date> <start>-<end>]` (e.g., `Bangalore route [2025-06-15 10:30-12:45]`)
- **Stitching**: Uses `ffmpeg` concat demuxer with stream copy (no re-encoding), preserving frame count and FPS exactly
- **Atomic output**: Writes to `.part` temp file, atomically renamed on success—interrupted runs never produce truncated files

**Completeness check**: An output counts as "done" only if it covers ≥ `COMPLETE_FRAC` (98%) of source frames. This guards against silent truncation in multi-hour videos.

### Stage 3: Metadata Extraction

```bash
python stitch_and_upload.py --dry-run           # Show segment plan across all trips
python stitch_and_upload.py --stitch-only       # Stitch only; skip upload
python stitch_and_upload.py                     # Full pipeline: stitch + upload + index
```

### Idempotency & Resumability

All batch scripts follow the same resilience pattern:

- Write to `.part.<ext>` temp file, atomically rename on success
- Track `frames_processed` and validate completeness (≥ 98%)
- `--all` processes every stitched video smallest-first, skipping completed work
- `--force` re-runs even if complete

## Video Understanding & Inference

### Depth Map Extraction

**Tool**: `make_depth_video.py`  
**Model**: Depth Anything V2 (transformer-based monocular depth)  
**Output**: Per-frame depth prediction, normalized and temporally smoothed

```bash
python make_depth_video.py --all                        # Process all videos, smallest first
python make_depth_video.py "<file>.mp4" --model base   # Single file with base model variant
```

**Processing**:

1. Decode source video via piped `ffmpeg` (handles corrupt frames better than OpenCV)
2. Pass RGB frames through Depth Anything V2 pipeline
3. Normalize depth values using **temporal EMA** (`EMA_ALPHA=0.05`) on per-frame min/max bounds
   - Naive per-frame normalization causes strobing; EMA smooths temporal variation
4. Apply INFERNO colormap (near = bright) for visual clarity
5. Encode output as `.depth.mp4` with frame-exact parity to source

**Output**: `depth/<stem>.depth.mp4` + metadata JSON with min/max statistics per-frame

### Object Detection

**Tool**: `make_detections.py`  
**Model**: YOLOv8 (real-time object detection)  
**Classes Tracked**: Person + road vehicles (car, bus, truck, motorcycle)  
**Output**: Normalized bounding boxes, frame-indexed

```bash
python make_detections.py --all                  # Detect on all stitched videos
python make_detections.py --all --render         # Also generate annotated preview MP4s
```

![Detection Example](assets/detection%20ONLY.png)

**Processing**:

1. Decode source via piped `ffmpeg` with frame-drop resilience
2. Run YOLOv8 inference on every Nth frame (configurable stride)
3. Normalize boxes to (0..1) range (resolution-independent)
4. Store as:
   - `detections/<stem>.detections.json`: Array of frame objects
   - `frames[i]`: Boxes for i-th processed frame (source frame = `i * stride`)
   - Per-box: `[x_min, y_min, x_max, y_max, confidence, class_id]`

5. Regenerate `detections/manifest.json` dropdown index after each file

**Frame-Perfect Indexing**: Detections reference frame numbers directly. A dropped frame desynchronizes overlays, so `make_web_videos.py` validates frame parity before atomic replace.

## Audio Feedback System

### Purpose

OmniSense delivers contextual audio nudges—brief, non-intrusive voice messages—at moments when the driver can benefit from guidance. Rather than generic warnings, nudges are timed to specific events and driving patterns.

### Nudge Categories

| Category | Trigger | Message Type |
|----------|---------|--------------|
| **Speed Advisory** | Excessive speed in residential area | Gentle reminder to slow down |
| **Following Distance** | Unsafe tailgating detected | Increase following distance |
| **Lane Discipline** | Drifting between lanes | Maintain lane position |
| **Hazard Awareness** | Pedestrian/cyclist in blind spot | Alert to presence |
| **Intersection Safety** | Approaching intersection without slowing | Prepare to stop if needed |


### Generation Pipeline

```
Detections + Depth + GPS/IMU Data
         │
         ▼
  Behavioral Analysis
  ├─ Relative distances (depth + YOLO boxes)
  ├─ Collision risk scoring
  ├─ Lane position tracking
  ├─ Speed/acceleration patterns
         │
         ▼
  Timeline Extraction
  ├─ Extract risky moments with frame precision
  ├─ Score nudge appropriateness (relevance + safety)
         │
         ▼
  Audio Synthesis
  ├─ Generate nudge script for each moment
  ├─ TTS (Text-to-Speech) with natural tone
  ├─ Append gentle notification chime
         │
         ▼
  audio_nudges/<stem>/nudge_HHMMSS_TYPE.wav
  + manifest.json (metadata & timing)
```


### Playback

Nudges are delivered in-vehicle through:

1. **Immediate notification**: Audio plays when threshold crossed during active driving
2. **Post-trip review**: Driver can review all nudges on the viewer dashboard
3. **Adaptive timing**: Nudges placed at moments when driver attention is available (not during active lane change, etc.)

### Customization

Nudge behavior is tunable via config:

- **Sensitivity thresholds** (e.g., min following distance for alert)
- **Cooldown periods** (avoid nagging—don't repeat same nudge within N seconds)
- **Priority filtering** (show only high-confidence nudges during peak hours)
- **TTS voice/speed** (prefer calm, conversational tone over robotic)

## Setup & Environment

### Python & Dependencies

**Python**: 3.12 in `.venv/` (activate: `.venv\Scripts\activate` on Windows)

**GPU**: RTX 3090 (24 GB), CUDA 12.6
- `torch==2.13.0+cu126` + `torchvision` (from cu126 wheel index)
- `torchvision` is required even if unused—`AutoImageProcessor` imports it internally

**System Dependencies**:
- `ffmpeg` v6.1+ (must be on PATH)
- `ffprobe` (for frame counting and validation)

**Key Dependencies**:

```bash
# VideoDB pipeline
pip install videodb

# Depth extraction
pip install torch torchvision transformers opencv-python pillow accelerate

# Object detection
pip install ultralytics opencv-python

# Audio synthesis (if generating nudges locally)
pip install pyttsx3  # or gTTS for cloud TTS

# Doc scraping (reference only)
pip install docling
```

### Environment Setup

```bash
# Activate venv
.venv\Scripts\activate

# Create .env file in project root
echo VIDEODB_API_KEY=your_api_key_here > .env
```

**⚠️ Security Note**: `.env` contains live API keys. Never commit it, never echo it, and never expose the folder with a plain static server.

## Common Commands

### Data Ingestion

```bash
# Plan stitching—see segment grouping logic
python stitch_and_upload.py --dry-run

# Stitch only (no upload)
python stitch_and_upload.py --stitch-only

# Full pipeline (stitch + upload + scene-index)
python stitch_and_upload.py

# Upload missing videos (VideoDB is source of truth)
python check_and_upload.py

# Retry scene indexing
python upload_stitched.py --index-only
```

### Video Understanding

```bash
# Generate depth maps for all stitched videos
python make_depth_video.py --all

# Single video with model selection
python make_depth_video.py "Trip [2025-06-15 10:30].mp4" --model base

# Run YOLOv8 detection on all videos
python make_detections.py --all

# Also generate annotated preview videos
python make_detections.py --all --render

# Force re-run (skip cache)
python make_detections.py --all --force
```

### Viewers & Playback

```bash
# Start local dev server (supports HTTP Range requests for seeking)
python serve.py
# Then open:
# - http://localhost:8000/depth_detection_viewer.html   (depth + YOLO overlay)
# - http://localhost:8000/trip_dist_viewer_v6.html      (advanced analytics)
```

### Audio Feedback

```bash
# Generate nudge timeline from detections & analysis
python analyze_behavior.py "<stem>.mp4" --output analysis/

# Synthesize audio nudges
python generate_audio_nudges.py "<stem>.mp4" --tts gcloud
# or for local TTS:
python generate_audio_nudges.py "<stem>.mp4" --tts pyttsx3

# Review nudges for a trip
python serve.py
# open http://localhost:8000/trip_dist_viewer_v6.html  (nudge tab)
```

## Data Conventions

### Coordinate Systems

**Bounding Box Format**: Normalized (0..1) XYXY
- `[x_min, y_min, x_max, y_max]` where (0,0) is top-left, (1,1) is bottom-right
- Resolution-independent; frontend scales to display size
- Stored in `detections/<stem>.detections.json`

### Frame Indexing

**Depth & Detection Alignment**: Both pipelines must preserve frame count and FPS exactly:

- `make_depth_video.py` outputs `.depth.mp4` with frame-for-frame parity
- `make_detections.py` stores `frames[i]` for i-th processed frame (source frame = `i * stride`)
- `make_web_videos.py` validates frame parity before atomic replace
- Dropped frames desynchronize overlays—idempotent re-runs are safer than partial fixes

![Depth Estimation](assets/depth%20estimation.png)

### File Naming

- **Raw clips**: `YYYYMMDDHHMMSS_SSSS.mp4` (start time + duration seconds)
- **Stitched**: `Trip [YYYY-MM-DD HH:MM-HH:MM] (silent).mp4`
- **Processed**: `<stem>.depth.mp4`, `<stem>.detections.json`, `<stem>.behavior.json`
- **Audio nudges**: `nudge_HHMMSS_CATEGORY.wav` in `audio_nudges/<stem>/`

## Development Notes

### Debugging Tips

- **ffmpeg decoding issues**: Dashcam footage may have corrupt frames. OmniSense decodes via piped ffmpeg (which skips bad access units) rather than OpenCV's `VideoCapture` (which treats one bad frame as end-of-stream).
- **VideoDB API**: Docs are scraped in `videodb_docs/`. Check there before guessing method signatures. Sample code is in `Sample Code.ipynb`.
- **Depth strobing**: If depth video flickers, check `EMA_ALPHA` value—too high = responsiveness, too low = lag.
- **Detection fps mismatch**: Always verify stride matches source FPS. Mismatched stride causes frame indexing errors.

### Performance Considerations

- **Depth extraction**: ~2-3 min per hour of video on RTX 3090 (depends on model size)
- **YOLO detection**: ~1-2 min per hour (real-time inference, but batched processing)
- **Streaming budget**: Viewer plays original + depth simultaneously; sum of bitrates must fit uplink. `make_web_videos.py` transcodes 1080p→720p for public serving (~3.6 Mbps peak vs 12.7 Mbps original)

## VideoDB Integration

OmniSense leverages a curated subset of VideoDB's platform features for video ingest, indexing, and scene-level analysis. See `VIDEODB_FEATURES_USED.md` for a complete inventory with status and gotchas.

### Core Features in Use

| Feature | Purpose | Status |
|---------|---------|--------|
| **Connection & Collection** | `videodb.connect()`, `conn.get_collection()` | ✅ Core—all scripts authenticate here |
| **Ingest** | `coll.upload(file_path=, name=)` | ✅ Core—upload stitched trip videos |
| **Scene Indexing** | `video.index_scenes(extraction_type=time_based, prompt=, model_name=)` | ✅ Core—video-RAG backbone; enables natural-language scene search |
| **Scene Extraction** | `video.extract_scenes(...)` + `scene.describe(prompt=, model_name=)` | ✅ Used in v1–v4 slice pipelines; replaced by `video.understand()` in v5 for cost |
| **Batch Video Understanding** | `video.understand(segmentation=, analyzers=[vlm, ...])` | ✅ v5 backbone—single-pass multi-modal analysis with structured output |
| **Semantic Search** | `video.search() / coll.search(query, index_type=IndexType.scene)` | ✅ Core—query indexed scenes; returns clip reel via `results.compile()` |
| **Sandbox Compute** | `conn.create_sandbox(tier=, models=[...])`, open-weight VLM inference | ✅ Used—Qwen3.5 for batch analysis, OmniVoice for TTS |
| **Audio Generation** | `coll.generate_voice(text=, model_name=, sandbox_id=)` | ⚠️ Tried (OmniVoice TTS); production pipeline uses Sarvam AI instead |
| **Usage Metering** | `conn.check_usage()` + `cost_metric` rate table | ✅ Core—enforce budget locks; cost tracking per operation |

### Projected Project Costs

**Estimated Total: ~$69.61** (Current usage: $49.61 + $20.00 projected)

**Cost Breakdown by Service**:

| Service | Units | Rate | Cost |
|---------|-------|------|------|
| Transcription | 2,165.00 | $0.01/unit | $21.65 |
| Sandbox Medium Compute | 3.54 hrs | $3.50/hr | $12.39 |
| LLM (Basic) | 6,250.24 | $0.0016/unit | $10.00 |
| LLM (Pro) | 1,541.90 | $0.0065/unit | $10.02 |
| LLM (Ultra) | 670.72 | $0.00875/unit | $5.87 |
| Indexing Bundle (Basic) | 9.66 | $0.80/unit | $7.73 |
| File Upload | 19.11 | $0.09/unit | $1.72 |
| Streaming | 11.58 | $0.07/unit | $0.81 |
| Media Storage | 15.82 | $0.03/unit | $0.47 |
| Timeline Overlay | 22.26 | $0.01/unit | $0.22 |
| Indexing Bundle (Pro) | 0.09 | $1.60/unit | $0.14 |
| Sandbox Small Compute | 0.14 hrs | $1.00/hr | $0.14 |
| Spoken Index | 6.48 | $0.02/unit | $0.13 |
| Search Queries | 85.00 | $0.0015/unit | $0.13 |
| **Other Services** | — | — | $0.02 |
| **Current Total Used** | — | — | **$49.61** |
| **Projected with Buffer** | — | — | **$69.61** |

**Cost Drivers**: Transcription (43.7%), Sandbox compute (24.9%), LLM inference (41.1% combined)

### Key Workflows

#### Video Ingest & Indexing
```python
# 1. Upload stitched trip video
video = coll.upload(file_path=str(stitched_path), name=stem)

# 2. Scene index with dashcam-targeted prompt
index_id = video.index_scenes(
    extraction_type=SceneExtractionType.time_based,
    extraction_config={"time": 10, "select_frames": ["first"]},
    prompt="Describe road type, traffic volume, weather, hazards, and vehicle behavior…",
    model_name="pro",  # basic|pro|ultra; costs vary
    name=f"dashcam-index {stem}",
)

# 3. Query by natural language
results = video.search("heavy traffic near pedestrians", index_type=IndexType.scene)
for shot in results.get_shots():
    print(f"Found: {shot.text} at {shot.start}–{shot.end}s")
hls_reel = results.compile()  # → playable clip reel
```

#### Batch Video Understanding (v5 Pipeline)
```python
# Single-pass multi-modal analysis with structured output
understanding = video.understand(
    segmentation={"type": "time", "seconds": 10},
    analyzers=[{
        "type": "vlm",
        "name": "driving",
        "config": {
            "model": "Qwen/Qwen3.5-27B",
            "sandbox_id": sandbox.id,
            "prompt": "Rate driving safety: green (excellent), amber (caution), red (unsafe). Return JSON.",
            "schema": {
                "type": "object",
                "properties": {
                    "safety_level": {"type": "string", "enum": ["green", "amber", "red"]},
                    "coaching": {"type": "string"}
                }
            },
        },
    }],
)
understanding.wait_until_complete()
output = understanding.get_analyzer("driving").get_output()
```

#### Sandbox Compute for TTS & Custom Models
```python
# Provision on-demand GPU sandbox
sandbox = conn.create_sandbox(
    tier=SandboxTier.medium,     # $3.50/hr, 3 concurrent
    models=["Qwen/Qwen3.5-27B", "k2-fsa/OmniVoice"]
)
sandbox.wait_for_ready(timeout=300)

# Generate voice on sandbox
audio = coll.generate_voice(
    text="Increase your following distance",
    model_name="k2-fsa/OmniVoice",
    sandbox_id=sandbox.id,
    wait=True
)
url = audio.generate_url()

# Always stop to avoid runaway charges (24h auto-expire)
sandbox.stop(grace=True)
```

### Notable Quirks & Workarounds

1. **Scene Index Status API is Unreliable**
   - Indexes report `processing → failed`, yet descriptions were generated and *are* searchable
   - Workaround: treat the create endpoint's duplicate-check message as authoritative; parse index id via regex
   - `get_scene_index()` refuses "failed" indexes; fall back to search results instead

2. **Custom Scene Annotations**
   - After extracting scenes with `video.extract_scenes()`, you can overwrite `scene.description` with your own analysis
   - Push via `video.index_scenes(scenes=indexable, name=...)` to make local analysis searchable through VideoDB
   - Used in v1–v4 slices for per-slice coaching text

3. **Search Limitations**
   - Empty result sets raise `InvalidRequestError` instead of returning `[]`—wrap all search calls in try/except
   - `index_id` filter parameter is not honored server-side; filter client-side on `shot.scene_index_id` if needed
   - Results limited to ~15 top shots; fire multiple queries with different wording to recover all answers

4. **Sandbox `scene.describe()` Bug**
   - Routing scene descriptions to a sandbox produces a malformed frame URL (doubled base path) and 404s
   - This affects `scene.describe(sandbox_id=…)` only
   - **Workaround**: Use `video.understand(analyzers=[...])` instead; it works fine on sandboxes
   - See `SANDBOX_BUG_REPORT.md` for reproduction and full details

5. **Upload Size Limit**
   - Max upload ≈ 1000 MB per tier
   - Larger files must be split first via `split_video.py`, which produces a `<stem> parts/` subfolder + sidecar JSON
   - 14 stitched videos were rejected with "Transcode failed" and moved to `stitched_reject/`

### Cost Optimization

**`videodb_cost.py`** tracks per-operation expenses because VideoDB exposes no per-request metadata:

```bash
python videodb_cost.py --mark              # Snapshot credit balance
python videodb_cost.py --diff              # Compare before/after; show per-unit costs
```

Available rate metrics from `conn.check_usage()`:
- `llm_basic`, `llm_pro`, `llm_ultra` — VLM inference tiers
- `indexing_bundle_*` — scene indexing
- `sandbox_small`, `sandbox_medium` — GPU sandbox compute (billed on wall-clock runtime)

**Pipeline v5 adoption** (single-pass `video.understand()` instead of chained `scene.describe()`) reduced per-video analysis cost by ~85% while maintaining output quality.

### Features Not Used

Several VideoDB capabilities are available but not adopted in this project:

- **`index_spoken_words()`** — Dashcam footage is silent; scene indexing covers visual content
- **Timeline/Editor API** (`Timeline`, `Track`, `Clip`) — `results.compile()` covers clip-reel needs
- **Live streams** (`RTStream`) — No live camera source in this project
- **Events & Alerts**, **CaptureSession**, **Dub/Translate** — Not applicable to recorded dashcam footage
- **`generate_image` / `generate_video`** — Only `generate_voice` was evaluated
- **Multiple collections** — Everything lives in the default collection

## Links & References

- **VideoDB Docs**: See `videodb_docs/` folder (scraped from docs.videodb.io); **note: Sandbox Compute postdates this scrape**—see `sandbox_experiments.md` for up-to-date Sandbox docs
- **Features Inventory**: `session_memory/VIDEODB_FEATURES_USED.md` — complete usage table, status, gotchas, and workarounds
- **Sample Code**: `session_memory/Sample Code.ipynb` — runnable VideoDB SDK snippets (upload, index, search, `results.play()`)
- **Sandbox Details**: `session_memory/sandbox_experiments.md`, `SANDBOX_BUG_REPORT.md` (scene.describe sandbox routing bug + workaround)
- **Cost Tracking**: `session_memory/videodb_cost.py` — measure per-operation expenses; design notes in script
- **Architecture Details**: `session_memory/DEPTH_VIEWER_PLAN.md`, `SESSION_NOTES.md`
- **Distance Benchmark**: `session_memory/dashcam_distance_benchmark.md` — calibration notes for depth accuracy
