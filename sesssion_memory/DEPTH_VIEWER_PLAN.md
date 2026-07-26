# Depth-Perception Viewer for Dashcam Footage

## Context

The VideoDB Demo Day project has stitched dashcam videos in `stitched/`. The user wants an
interface showing the **original video on top and a depth-perception map of the same footage
below**, playing in sync. Decisions made with the user:

- **Approach**: precompute the depth-map video once on the local GPU, then view both videos in
  a synced stacked HTML player (chosen over live inference / OpenCV window).
- **Source**: one full stitched video. The user didn't name one, so the script takes the input
  path as a CLI argument; default to `stitched/Car Dashcam [2026-07-10 0741-0743] (silent).mp4`
  (a complete ~2-minute stitched video, 189 MB — processes in a couple of minutes and is the
  natural first end-to-end run). Any other stitched file can be processed the same way.

Environment verified: Python 3.12 venv at `.venv/`, **RTX 3090 (24 GB)**, ffmpeg 6.1 on PATH.
Depth model: **Depth Anything V2 Small** via Hugging Face `transformers` (fp16 on CUDA;
~60–100 fps at 518 px on a 3090). `--model base` flag for higher quality if wanted.

## Deliverables (2 new files in project root)

### 1. `make_depth_video.py` — one-time depth render

CLI: `python make_depth_video.py "stitched/<file>.mp4" [--model small|base] [--width 960]`
Output: `depth/<same name>.depth.mp4` (same fps and duration as source).

Pipeline per frame batch:
1. **Decode** with `cv2.VideoCapture` (read fps, frame count for tqdm progress — tqdm already installed).
2. **Infer** depth with `transformers` pipeline `depth-anything/Depth-Anything-V2-Small-hf`,
   fp16, batched (e.g. 8 frames), input resized to 518 px.
3. **Normalize with temporal smoothing** — per-frame min/max normalization flickers badly on
   video; keep an EMA (e.g. α=0.05) of the min/max bounds across frames so brightness is stable.
4. **Colorize** with `cv2.COLORMAP_INFERNO` (near = bright), resize to `--width` (default 960,
   keeps file small; the player scales it to match the original).
5. **Encode H.264** by piping raw BGR frames to the system `ffmpeg` (`-c:v libx264 -pix_fmt
   yuv420p -crf 23`) — cv2's VideoWriter can't produce browser-playable H.264 on Windows.
6. Resumable-not-required; on completion print the output path and a reminder to open the viewer.

New dependencies to install into `.venv`:
`torch` (CUDA wheel, cu121/cu126 index), `transformers`, `opencv-python`, `pillow`, `accelerate`.

### 2. `depth_viewer.html` — the interface (no server needed)

A single self-contained HTML file opened directly in the browser (file:// video playback and
seeking work fine in Chrome/Edge; both videos referenced by relative paths).

- Layout: dark page, original `<video>` on top, depth `<video>` below, same width
  (max ~90vw), stacked with a small gap and labels ("Original" / "Depth map").
- **One shared control bar** (play/pause, seek slider, time readout, playback-speed select)
  drives the top video; the depth video has no native controls.
- **Sync logic**: mirror play/pause/seek/ratechange events from master to depth video, plus a
  `requestAnimationFrame` drift-correction loop — if `|masterTime − depthTime| > 0.05s`, snap
  the depth video's `currentTime`.
- Video sources set via two constants at the top of the file's script (defaulting to the Car
  Dashcam pair) so switching footage is a one-line edit; also accept `?video=<name>` query
  param that fills in both paths by convention (`stitched/<name>.mp4` + `depth/<name>.depth.mp4`).

## Verification

1. `pip install` the deps into `.venv`; confirm `torch.cuda.is_available()` is True.
2. Run `python make_depth_video.py "stitched/Car Dashcam [2026-07-10 0741-0743] (silent).mp4"`;
   confirm `depth/…depth.mp4` exists, plays, has the same duration as the source, and the
   depth map is temporally stable (no strobing).
3. Open `depth_viewer.html` in the browser: both videos load stacked, play/pause/seek/speed
   stay in lockstep (scrub mid-video and confirm frames correspond — e.g. a passing truck
   appears in both panes at the same moment).

---

## Implementation log (2026-07-22)

What was actually built, including deviations from the plan above.

### Dependencies installed into `.venv`
- `torch==2.13.0+cu126`, `torchvision==0.28.0+cu126` (CUDA 12.6 wheels), plus `transformers`,
  `opencv-python`, `pillow`, `accelerate`.
- **`torchvision` was missing from the original plan** — `AutoImageProcessor` requires it;
  the first render crashed with `ImportError: AutoImageProcessor requires the Torchvision
  library` until it was installed from the same cu126 index.
- CUDA verified: `torch.cuda.is_available()` → True on the RTX 3090.

### `make_depth_video.py` — built, then hardened
Loads Depth Anything V2 Small (fp16, CUDA), infers in batches of 8, EMA-smooths the depth
range (α=0.05) to stop strobing, colorizes with `COLORMAP_INFERNO`, and encodes browser-safe
H.264 via a piped `ffmpeg` writer. Output → `depth/<stem>.depth.mp4`, written to a `.part.mp4`
first and renamed on success so an interrupted run never leaves a "complete" but corrupt file.

Deviations / additions beyond the original single-file plan:
- **Decoding moved from `cv2.VideoCapture` to a piped `ffmpeg` reader.** OpenCV stops at the
  first corrupt frame and reports it as end-of-stream; one dashcam clip
  (`Good videos [2025-09-28 1347-1350]`) has corruption near the start and rendered **1 frame**
  instead of 5406. `ffmpeg` skips bad access units and keeps decoding — the same clip now
  renders all 5406 frames. This also removed the per-frame BGR→RGB convert (ffmpeg emits
  rgb24 directly at the inference resolution).
- **`--all` batch mode**: renders every top-level `stitched/*.mp4` smallest-first, skipping
  ones already done. Safe to re-run / resume.
- **Output validation (`output_is_complete`)**: an existing depth file only counts as "done"
  if its frame count is ≥ 98% of the source's (via `ffprobe`). Guards against silently
  truncated renders — critical for the multi-hour commute videos. A truncation `WARNING` is
  also printed if fewer frames decode than expected.
- **`--force`** flag to re-render regardless.
- Actual throughput on the 3090: **~35 fps** (a bit faster than real-time), not the 60–100 fps
  estimated in the plan.

### `depth_viewer.html` — built, then two follow-up changes
Dark stacked player with one shared control bar (play/pause, scrub, speed, space + ←/→ keys)
and a `requestAnimationFrame` drift-correction loop (snaps depth video if it strays > 50 ms).

Changes made after the first build, on user request:
- **Single-screen / no-scroll layout**: page is locked to `100vh` with `overflow:hidden`; the
  two panes `flex:1` and split the viewport evenly, each video scaled with
  `max-height:100%` (letterboxed rather than forcing the page taller). Header/controls slimmed;
  layout widened to `min(96vw, 1400px)`.
- **Video dropdown**: the control bar now has a `<select>` populated from `depth/videos.js`
  (`window.DEPTH_VIDEOS = [...]`), a manifest `make_depth_video.py` regenerates after each
  render. Choosing a video reloads via `?video=<stem>`. Refresh the tab to see newly finished
  videos appear in the dropdown.

### Batch status
Ran `python make_depth_video.py --all`. All 8 short clips (Car Dashcam + 7 "Good videos")
rendered and validated. The long commute videos
(`VN to PIC Pashan` ×2, `Nigdi to Yerwada`, `Pune to Velhe`) were still rendering at the end
of the session — re-run `--all` to resume; completed ones are skipped automatically.

### New / changed files
- `make_depth_video.py` (new)
- `depth_viewer.html` (new)
- `depth/*.depth.mp4` (rendered outputs), `depth/videos.js` (dropdown manifest)
