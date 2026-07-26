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
    - [Search and Retrieval](\pages\understand\search-and-retrieval\natural-language-query)
    - [Intelligent Search](\pages\understand\search-and-retrieval\intelligent-search)
    - [Results, Evidence, and Returned Fields](\pages\understand\search-and-retrieval\timestamps-clips-streams)
    - [Search Patterns and Results](\pages\understand\search-and-retrieval\collection-search)
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

- [How intelligent search works](#how-intelligent-search-works)
- [Ways to use intelligent search](#ways-to-use-intelligent-search)
    - [Find the relevant moments](#find-the-relevant-moments)
    - [Investigate and refine](#investigate-and-refine)
    - [Explain the findings](#explain-the-findings)
- [Search responses](#search-responses)
- [DeepSearch: multi-step investigation](#deepsearch-multi-step-investigation)
- [Ask: answers grounded in video](#ask-answers-grounded-in-video)
- [Choose an intelligent method](#choose-an-intelligent-method)
- [Next steps](#next-steps)

[Understand](\pages\understand\indexing-pipelines\understanding-artifacts)

[Search and Retrieval](\pages\understand\search-and-retrieval\natural-language-query)

# Intelligent Search

Copy page

Use Search, DeepSearch, and Ask when you want VideoDB to plan retrieval from natural language.

Copy page

Use intelligent search when you know the goal, but do not want to manually choose indexes and retrieval methods. VideoDB interprets the request, plans retrieval over available indexes, and returns timestamped evidence or a grounded answer.

| Method                      | Best for                                                   | Returns                               |
|-----------------------------|------------------------------------------------------------|---------------------------------------|
| `search()`                  | Natural-language retrieval across one or more signals      | Matching moments or aggregate rows    |
| `search(mode="deepsearch")` | Complex investigation, refinement, and follow-up questions | Matching moments plus session state   |
| `ask()`                     | A synthesized answer grounded in indexed video             | An answer and optional source moments |

## [ How intelligent search works](#how-intelligent-search-works)

Intelligent search sits above the direct retrieval methods. Your application describes the goal, and VideoDB handles the retrieval plan.

```
Natural-language request
↓
Interpret the intent and available index schemas
↓
Use one or more of: semantic search · structured query · aggregation
↓
Return moments, analytics, or a grounded answer
```

The plan can draw on several indexed signals, such as spoken words, scene descriptions, objects, brands, OCR, and custom structured fields. Results retain their source video and timestamps, so the output remains connected to playable evidence.

## [ Ways to use intelligent search](#ways-to-use-intelligent-search)

The right intelligent method depends on the outcome the user wants. Consider a collection of customer interviews.

### [ Find the relevant moments](#find-the-relevant-moments)

```
response = collection.search(
query = "Find moments where customers object to pricing" ,
)
```

Use Search when the result should be ranked, timestamped moments or an aggregate selected from the request.

### [ Investigate and refine](#investigate-and-refine)

```
response = collection.search(
query = "Find the strongest pricing objections and identify which ones mention competitors" ,
mode = "deepsearch" ,
)
```

Use DeepSearch when the task benefits from multiple retrieval steps, clarification, or follow-up questions.

### [ Explain the findings](#explain-the-findings)

```
answer = collection.ask(
question = "What are the main pricing objections?" ,
include_sources = True ,
)
```

Use Ask when the application needs a synthesized answer with optional source moments.

| User intent                                              | Result                                  |
|----------------------------------------------------------|-----------------------------------------|
| "Find product demonstrations"                            | Ranked, timestamped moments             |
| "How many scenes contain each brand?"                    | Aggregate rows                          |
| "Investigate negative reactions, then refine the result" | DeepSearch results and session state    |
| "What are the main customer objections?"                 | A grounded answer with optional sources |

## [ Search responses](#search-responses)

`search()` returns a `SearchResponse` because the planned result can take more than one form.

| Attribute       | Description                                                                           |
|-----------------|---------------------------------------------------------------------------------------|
| `response_type` | Usually `"shots"` ; can be `"aggregate"` when the request asks for grouped analytics. |
| `results`       | A `SearchResult` for moments, or aggregate rows for an aggregate response.            |
| `shots`         | Convenience list of `Shot` objects for moment responses.                              |
| `trace`         | Optional planner trace for debugging.                                                 |

Compile matching moments into one stream through the nested `SearchResult` :

```
if response.response_type == "shots" :
stream_url = response.results.compile()
```

## [ DeepSearch: multi-step investigation](#deepsearch-multi-step-investigation)

Use DeepSearch when one retrieval step is unlikely to be enough, or when a user needs to refine the result through follow-up requests.

```
response = collection.search(
query = "find the strongest examples of customers objecting to pricing" ,
mode = "deepsearch" ,
top_k = 10 ,
return_fields = "all" ,
)

print (response.session_id)
```

Continue the investigation with the returned session ID:

```
followup = collection.search(
query = "only keep moments where a competitor is mentioned" ,
mode = "deepsearch" ,
session_id = response.session_id,
top_k = 10 ,
)
```

DeepSearch responses can include:

| Attribute           | Description                                                             |
|---------------------|-------------------------------------------------------------------------|
| `session_id`        | ID used to continue the investigation.                                  |
| `waiting_for`       | Current DeepSearch waiting state.                                       |
| `clarification`     | A question from DeepSearch when it needs more detail before continuing. |
| `results` / `shots` | Retrieved timestamped moments.                                          |

For example, DeepSearch might ask:

Which product line or time period should I focus on?

Answer by continuing the same DeepSearch session:

```
if response.clarification:
print (response.clarification)

followup = collection.search(
query = "Focus on the enterprise plan discussed in the Q4 interviews" ,
mode = "deepsearch" ,
session_id = response.session_id,
)
```

DeepSearch supports `top_k` , `session_id` , and `return_fields` . Filters, sorting, score thresholds, planner traces, and index selectors are not supported in DeepSearch mode.

## [ Ask: answers grounded in video](#ask-answers-grounded-in-video)

Use `ask()` when the desired output is an answer rather than a list of matching moments.

```
answer = collection.ask(
question = "What objections do customers raise about pricing?" ,
top_k = 15 ,
include_sources = True ,
)

print (answer.answer)
```

When `include_sources=True` , the response includes the timestamped moments used as evidence:

```
for source in answer.sources:
print (source.video_id, source.start, source.end)
print (source.stream_url or source.generate_stream())
```

Ask is available at both scopes:

```
video.ask(
question = "What happens after the demo?" ,
include_sources = True ,
)

collection.ask(
question = "Which videos mention Nike?" ,
include_sources = True ,
)
```

## [ Choose an intelligent method](#choose-an-intelligent-method)

| Your goal                                             | Use                                                                                                                |
|-------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Find relevant moments from a natural-language request | `search()`                                                                                                         |
| Investigate a complex request over multiple steps     | `search(mode="deepsearch")`                                                                                        |
| Continue refining a previous investigation            | DeepSearch with `session_id`                                                                                       |
| Receive a concise answer with optional evidence       | `ask()`                                                                                                            |
| Control the exact retrieval operation or index        | [Direct retrieval methods](\pages\understand\search-and-retrieval\natural-language-query#direct-retrieval-methods) |

## [ Next steps](#next-steps)

## Direct Retrieval

Use semantic search, query, and aggregation directly.

## Results and Evidence

Work with shots, timestamps, returned fields, and streams.

[Search and Retrieval](\pages\understand\search-and-retrieval\natural-language-query) [Results, Evidence, and Returned Fields](\pages\understand\search-and-retrieval\timestamps-clips-streams)

⌘ I