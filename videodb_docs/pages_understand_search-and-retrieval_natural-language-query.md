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
    - [Natural Language Query](\pages\understand\search-and-retrieval\natural-language-query)
    - [Timestamps, Clips, Streams](\pages\understand\search-and-retrieval\timestamps-clips-streams)
    - [Collection Search](\pages\understand\search-and-retrieval\collection-search)
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
- [How It Works](#how-it-works)
- [Search Types](#search-types)
    - [Semantic Search (Default)](#semantic-search-default)
    - [Keyword Search](#keyword-search)
    - [Comparison](#comparison)
- [Index Types](#index-types)
- [Tuning Results](#tuning-results)
    - [Result Threshold](#result-threshold)
    - [Score Threshold](#score-threshold)
    - [Dynamic Score Percentage](#dynamic-score-percentage)
- [Search Parameters Reference](#search-parameters-reference)
- [Query Examples](#query-examples)
    - [Sort by Timestamp](#sort-by-timestamp)
    - [Spoken Content Queries](#spoken-content-queries)
    - [Visual Content Queries](#visual-content-queries)
    - [Multimodal Queries](#multimodal-queries)
- [What You Can Build](#what-you-can-build)
- [Next Steps](#next-steps)

[Understand](\pages\understand\indexing-pipelines\create-an-index)

[Search and Retrieval](\pages\understand\search-and-retrieval\natural-language-query)

# Natural Language Query

Copy page

Search videos using plain English questions and get relevant results

Copy page

Ask questions in plain English. VideoDB uses semantic search to understand intent and return relevant video segments.

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video( "m-xxx" )

# Natural language query
results = video.search( "when does the speaker discuss climate change?" )

# Play matching segments
results.play()
```

```
import { connect } from 'videodb' ;

const conn = connect ();
const coll = await conn . getCollection ();
const video = await coll . getVideo ( "m-xxx" );

// Natural language query
const results = await video . search ( "when does the speaker discuss climate change?" );

// Get stream URL
const streamUrl = await results . compile ();
console . log ( streamUrl );
```

## [ How It Works](#how-it-works)

1. **Query Understanding** - Your query is transformed into a vector embedding
2. **Similarity Matching** - Embeddings are compared against indexed content
3. **Relevance Scoring** - Results are ranked by semantic similarity
4. **Timestamp Retrieval** - Matching segments are returned with timestamps

## [ Search Types](#search-types)

### [ Semantic Search (Default)](#semantic-search-default)

Understands meaning and intent, not just keywords.

Python

Node.js

```
from videodb import SearchType

# Semantic search (default)
results = video.search( "How do I fix a leaky faucet?" )

# Explicit semantic search
results = video.search(
query = "How do I fix a leaky faucet?" ,
search_type = SearchType.semantic
)
```

```
import { SearchTypeValues } from 'videodb' ;

// Semantic search (default)
const results = await video . search ( "How do I fix a leaky faucet?" );

// Explicit semantic search
const results = await video . search (
"How do I fix a leaky faucet?" ,
SearchTypeValues . semantic
);
```

**Best for:**

- Questions ("What causes...?", "How do you...?")
- Conceptual queries ("explain the theory")
- Fuzzy matching ("something about cars")

### [ Keyword Search](#keyword-search)

Exact substring matching. Finds literal occurrences.

Python

Node.js

```
from videodb import SearchType

results = video.search(
query = "API" ,
search_type = SearchType.keyword
)
```

```
import { SearchTypeValues } from 'videodb' ;

const results = await video . search (
"API" ,
SearchTypeValues . keyword
);
```

**Best for:**

- Technical terms
- Proper nouns
- Exact phrases

### [ Comparison](#comparison)

| Feature   | Semantic Search            | Keyword Search    |
|-----------|----------------------------|-------------------|
| Query     | Natural language           | Exact terms       |
| Matching  | By meaning                 | By substring      |
| Example   | "How to repair pipes?"     | "plumbing repair" |
| Scope     | Single video or collection | Single video only |

## [ Index Types](#index-types)

Specify which index to search.

Python

Node.js

```
from videodb import IndexType

# Search spoken content (default)
results = video.search(
query = "discusses machine learning" ,
index_type = IndexType.spoken_word
)

# Search visual content
results = video.search(
query = "person running through a park" ,
index_type = IndexType.scene
)

# Search specific scene index
results = video.search(
query = "red car" ,
index_type = IndexType.scene,
index_id = "scene-index-xxx"
)
```

```
import { IndexTypeValues , SearchTypeValues } from 'videodb' ;

// Search spoken content (default)
const results = await video . search (
"discusses machine learning" ,
SearchTypeValues . semantic ,
IndexTypeValues . spoken
);

// Search visual content
const results = await video . search (
"person running through a park" ,
SearchTypeValues . semantic ,
IndexTypeValues . scene
);

// Search specific scene index
const results = await video . search (
"red car" ,
SearchTypeValues . semantic ,
IndexTypeValues . scene ,
null , // resultThreshold
null , // scoreThreshold
null , // dynamicScorePercentage
null , // filter
null , // namespace
"scene-index-xxx" // sceneIndexId
);
```

## [ Tuning Results](#tuning-results)

### [ Result Threshold](#result-threshold)

Limit the number of results returned:

Python

Node.js

```
results = video.search(
query = "funny moments" ,
result_threshold = 10 # Return top 10 matches
)
```

```
const results = await video . search (
"funny moments" ,
SearchTypeValues . semantic ,
IndexTypeValues . spoken ,
10 // resultThreshold - Return top 10 matches
);
```

### [ Score Threshold](#score-threshold)

Filter out low-relevance results:

Python

Node.js

```
results = video.search(
query = "product demo" ,
score_threshold = 0.3 # Only results with score >= 0.3
)
```

```
const results = await video . search (
"product demo" ,
SearchTypeValues . semantic ,
IndexTypeValues . spoken ,
null , // resultThreshold
0.3 // scoreThreshold - Only results with score >= 0.3
);
```

### [ Dynamic Score Percentage](#dynamic-score-percentage)

Adaptive filtering based on score distribution:

Python

Node.js

```
results = video.search(
query = "key insights" ,
dynamic_score_percentage = 50 # Keep top 50% of score range
)
```

```
const results = await video . search (
"key insights" ,
SearchTypeValues . semantic ,
IndexTypeValues . spoken ,
null , // resultThreshold
null , // scoreThreshold
50 // dynamicScorePercentage - Keep top 50% of score range
);
```

The dynamic threshold is calculated as:

```
dynamic_threshold = max_score - (range × percentage)
```

## [ Search Parameters Reference](#search-parameters-reference)

| Parameter                  | Type       | Default     | Description                                                             |
|----------------------------|------------|-------------|-------------------------------------------------------------------------|
| `query`                    | str        | required    | Natural language query                                                  |
| `search_type`              | SearchType | semantic    | `semantic` or `keyword`                                                 |
| `index_type`               | IndexType  | spoken_word | `spoken_word` or `scene`                                                |
| `result_threshold`         | int        | 5           | Max results to return                                                   |
| `score_threshold`          | float      | 0.2         | Minimum relevance score                                                 |
| `dynamic_score_percentage` | float      | 20          | Adaptive score filter                                                   |
| `index_id`                 | str        | None        | Specific scene index ID                                                 |
| `sort_docs_on`             | str        | `"score"`   | Sort results by `"score"` (relevance, default) or `"start"` (timestamp) |

Layers and parameters of semantic search showing how queries are transformed into vectors and matched against indexed content

<!-- image -->

## [ Query Examples](#query-examples)

### [ Sort by Timestamp](#sort-by-timestamp)

Python

Node.js

```
# Sort results by timestamp instead of relevance
results = coll.search( query = "morning sunlight" , sort_docs_on = "start" )
```

```
// Sort results by timestamp instead of relevance
const results = await coll . search ({ query: "morning sunlight" , sortDocsOn: "start" });
```

### [ Spoken Content Queries](#spoken-content-queries)

```
# Question format
video.search( "What are the main benefits of solar energy?" )

# Topic lookup
video.search( "discussion about renewable energy" )

# Speaker search
video.search( "when the CEO mentions revenue" )
```

### [ Visual Content Queries](#visual-content-queries)

```
# Object detection
video.search( "red car on the highway" , index_type = IndexType.scene)

# Action detection
video.search( "person running" , index_type = IndexType.scene)

# Scene description
video.search( "sunset over the ocean" , index_type = IndexType.scene)
```

### [ Multimodal Queries](#multimodal-queries)

Combine spoken and visual search for precise results:

Python

Node.js

```
from videodb import IndexType

# Search spoken content
spoken_results = video.search(
query = "talks about the solar system" ,
index_type = IndexType.spoken_word
)

# Search visual content
visual_results = video.search(
query = "shows planets or galaxies" ,
index_type = IndexType.scene
)

# Find intersection (both conditions met)
spoken_times = [(s.start, s.end) for s in spoken_results.get_shots()]
visual_times = [(s.start, s.end) for s in visual_results.get_shots()]
```

```
import { IndexTypeValues , SearchTypeValues } from 'videodb' ;

// Search spoken content
const spokenResults = await video . search (
"talks about the solar system" ,
SearchTypeValues . semantic ,
IndexTypeValues . spoken
);

// Search visual content
const visualResults = await video . search (
"shows planets or galaxies" ,
SearchTypeValues . semantic ,
IndexTypeValues . scene
);

// Find intersection (both conditions met)
const spokenTimes = spokenResults . shots . map ( s => [ s . start , s . end ]);
const visualTimes = visualResults . shots . map ( s => [ s . start , s . end ]);
```

## [ What You Can Build](#what-you-can-build)

## Keyword Search Compilation

Create highlight reels from specific keywords or phrases

## Multimodal Search

Combine spoken and visual search for precise results

## Character Clips

Extract clips featuring specific people using search

## [ Next Steps](#next-steps)

## Timestamps, Clips, Streams

What you get back from search

## Collection Search

Search across your entire library

[Multiple Indexes](\pages\understand\indexing-pipelines\multiple-indexes) [Timestamps, Clips, Streams](\pages\understand\search-and-retrieval\timestamps-clips-streams)

⌘ I