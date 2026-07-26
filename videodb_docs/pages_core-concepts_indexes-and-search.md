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
- [Events &amp; Real-time](\pages\core-concepts\events-and-realtime)
- [Programmable Editing](\pages\core-concepts\programmable-editing)
- [Security &amp; Privacy](\pages\core-concepts\security-privacy)

### Ingest

- Files and Collections
- Live Streams
- Capture SDKs
- Transcoding

### Understand

- Indexing Pipelines
- Search and Retrieval
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

- [Quick Example](#quick-example)
- [Index Types](#index-types)
    - [Key Properties](#key-properties)
- [Search Scopes](#search-scopes)
- [Playable Evidence](#playable-evidence)
- [Multi-Index Search](#multi-index-search)
- [Best Practices](#best-practices)
- [What You Can Build](#what-you-can-build)
- [Next Steps](#next-steps)

[Core Concepts](\pages\core-concepts\overview)

# Indexes &amp; Search

Copy page

Indexes turn raw media into searchable knowledge. Search returns playable evidence - timestamps and stream URLs you can verify.

Copy page

## [ Quick Example](#quick-example)

```
import videodb

conn = videodb.connect()
video = conn.get_collection().upload( url = "https://example.com/video.mp4" )

# Create an index with a prompt
index_id = video.index_scenes(
prompt = "Extract key decisions and action items"
)

# Search returns playable evidence
results = video.search( "budget approval" , index_id = index_id)
for shot in results.shots:
print ( f " { shot.start } s: { shot.text } " )
shot.play() # Opens in browser
```

Comparison showing video search results with and without indexing, demonstrating how indexing finds exact moments

<!-- image -->

## [ Index Types](#index-types)

Scene index visual example showing search query 'Show me the bomb explosion scene' with matching video frames and timestamps

<!-- image -->

| Type       | Method                       | Use Case                        |
|------------|------------------------------|---------------------------------|
| **Visual** | `video.index_scenes()`       | Describe scenes, detect objects |
| **Spoken** | `video.index_spoken_words()` | Transcripts, spoken content     |
| **Audio**  | `rtstream.index_audio()`     | Audio analysis, topics          |

### [ Key Properties](#key-properties)

- **Prompt-driven** - You define what to extract with natural language
- **Additive** - Multiple indexes on the same media
- **Non-destructive** - Add/remove without affecting source

```
# Multiple indexes = multiple perspectives
safety_index = video.index_scenes( prompt = "Identify safety issues" )
summary_index = video.index_scenes( prompt = "Summarize each segment" )
transcript = video.index_spoken_words()
```

## [ Search Scopes](#search-scopes)

```
# Single video
results = video.search( "product demo" )

# Single stream
results = rtstream.search( "intrusion" )

# Collection-wide
results = coll.search( "quarterly results" , index_type = "scene" )
```

## [ Playable Evidence](#playable-evidence)

Every search result includes playable proof:

```
for shot in results.shots:
shot.start # 45.2 (seconds)
shot.end # 52.8
shot.text # "CEO announces Q3 results"
shot.search_score # 0.87
shot.play() # Verify the result
```

## [ Multi-Index Search](#multi-index-search)

Search across visual and spoken content:

```
results = video.search(
query = "budget discussion" ,
index_type = [ "scene" , "spoken_word" ]
)
```

- **Union** - Broader recall (results from any index)
- **Intersection** - Higher precision (matches in all indexes)

## [ Best Practices](#best-practices)

1. **Be specific in prompts** - "Identify safety violations" beats "describe what you see"
2. **Use specific queries** - "red car entering lot" beats "car"
3. **Verify with playback** - Always validate with `shot.play()`
4. **Create focused indexes** - One index per question or domain

## [ What You Can Build](#what-you-can-build)

## Keyword Search Compilation

Create highlight reels from keyword-based search

## Multimodal Search

Combine visual and spoken indexes for powerful queries

## Character Clips

Extract clips featuring specific people from video libraries

## [ Next Steps](#next-steps)

## Indexing Guide

Detailed indexing patterns

## Semantic Search

Advanced search techniques

[Data Model](\pages\core-concepts\data-model) [Events &amp; Real-time](\pages\core-concepts\events-and-realtime)

⌘ I