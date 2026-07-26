# Session Notes — VideoDB Demo Day

Date: 2026-07-21

## Context

Explored `videodb_docs/` (266 scraped markdown pages from docs.videodb.io, produced by
`scrape_videosdb_docs.py`) to identify demo-worthy use cases and the fastest way to get a
working VideoDB demo running.

## Use case options (by docs folder)

| Category (folder) | Demo-day idea | Effort |
|---|---|---|
| `examples-and-tutorials_video-rag*` | "Ask your meeting/lecture archive anything" — upload a talk, search in natural language, get timestamped clips back | Lowest — ~10 lines |
| `examples-and-tutorials_live-intelligence*` | Live camera/stream alerting (intrusion, crowd, traffic) — wire an `Event` + `Alert` to a webhook that fires in real time | Medium — needs an RTSP/webcam source |
| `examples-and-tutorials_ai-copilots*` | OpenClaw-style "agent with eyes" — stream desktop screen+mic, get structured JSON context back over a websocket | Medium — good visual wow-factor |
| `examples-and-tutorials_content-factory*` | Auto-dub or AI-voiceover a video into another language in one call | Low |
| `examples-and-tutorials_programmatic-editing*` | Compose a branded highlight reel (intro/outro + clips) via the `Timeline` API, no video editor needed | Medium |
| `examples-and-tutorials_safety-compliance*` | Auto-beep profanity or flag copyrighted content in an uploaded video | Low |

**Recommendation:** `video-rag` is fastest to demo and most visually convincing —
"type a question, watch the video jump to the answer."

## Core mental model (from `pages_getting-started_core-concepts-in-5-min.md`)

```
See → Understand → Act
```

- **See**: ingest from files, streams, or desktop capture → `Video`, `RTStream`, or `CaptureSession`
- **Understand**: create indexes, search with natural language → timestamped moments with playable evidence
- **Act**: trigger alerts, compose edits, export streams → webhooks, playable URLs, downloadable files

## Quickstart code (Python)

Setup:

```bash
pip install videodb python-dotenv
export VIDEODB_API_KEY="your-api-key"   # from console.videodb.io, free tier: 50 uploads, no card
```

Minimal video-RAG loop:

```python
import videodb

conn = videodb.connect()
coll = conn.get_collection()

# 1. SEE — ingest any public video (YouTube, S3, direct URL)
video = coll.upload(url="https://www.youtube.com/watch?v=WDv4AWk0J3U")

# 2. UNDERSTAND — index spoken words (add index_visuals() too if scenes matter)
video.index_spoken_words()

# 3. ACT — search in plain English, get timestamped playable results
results = video.search("what are the key takeaways?")
for shot in results.shots:
    print(f"{shot.start}s - {shot.end}s: {shot.text}")

results.play()  # returns a playable HLS link to the matching moments
```

Extensions:
- `video.index_visuals(prompt="...")` — scene/visual search
- `conn.create_event(...)` + `index.create_alert(...)` — real-time alerts (live-intelligence demos)
- `from videodb.editor import Timeline, Track, Clip, VideoAsset` — programmatic editing

## Key doc references

- `videodb_docs/pages_getting-started_quickstart.md` — 5-minute quickstart, includes real-time
  desktop capture (OpenClaw) sample and file-upload/search sample
- `videodb_docs/pages_getting-started_python.md` — Python SDK install/config
- `videodb_docs/pages_getting-started_core-concepts-in-5-min.md` — full mental model + object glossary
- `videodb_docs/examples-and-tutorials.md` — index of all example categories with Colab notebook links

## Open next step

Offered to scaffold a runnable script/notebook for one specific use case (video-RAG search demo
or a live intrusion-alert demo) once the user picks a target video/stream — not yet started.
