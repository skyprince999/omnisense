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
    - Understanding
    - Indexing
        - [Create an Index](\pages\understand\indexing-pipelines\create-an-index)
        - [Index Fields](\pages\understand\indexing-pipelines\multiple-indexes)
        - [View Indexes](\pages\understand\indexing-pipelines\view-indexes)
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

- [List indexes](#list-indexes)
- [Get one index](#get-one-index)
- [Inspect field schema](#inspect-field-schema)
- [Preview indexed records](#preview-indexed-records)
- [Search APIs remain separate from index inspection](#search-apis-remain-separate-from-index-inspection)
- [Delete an index](#delete-an-index)
- [Next steps](#next-steps)

[Understand](\pages\understand\indexing-pipelines\understanding-artifacts)

[Understanding &amp; Indexing Pipelines](\pages\understand\indexing-pipelines\understanding-artifacts)

[Indexing](\pages\understand\indexing-pipelines\create-an-index)

# View Indexes

Copy page

List indexes, inspect their fields and capabilities, and preview indexed records.

Copy page

After you create indexes, use index inspection APIs to see what exists, whether each index is ready, which fields are available, and what records were indexed.

In V2, use `get_index()` plus `index.records()` instead of legacy `get_scene_index()` . Keep using `get_scene_index()` only with legacy scene indexes.

## [ List indexes](#list-indexes)

Use `list_indexes()` to see the indexes available on a video.

```
indexes = video.list_indexes()

for index in indexes:
print (index.name, index.status, index.use_for)
```

Example response:

```
[
{
"index_id" : "idx_scene_123" ,
"name" : "scene" ,
"status" : "ready" ,
"use_for" : [ "semantic" , "query" , "aggregate" ],
"source" : {
"understanding_id" : "und_123" ,
"artifact" : "scene" ,
"analyzer" : { "name" : "scene" , "type" : "vlm" }
},
"record_count" : 128
},
{
"index_id" : "idx_objects_456" ,
"name" : "objects" ,
"status" : "ready" ,
"use_for" : [ "query" , "aggregate" ],
"source" : {
"understanding_id" : "und_123" ,
"artifact" : "objects" ,
"analyzer" : { "name" : "objects" , "type" : "object_detection" }
},
"record_count" : 128
}
]
```

You can filter by capability when you only want indexes that support a retrieval mode:

```
semantic_indexes = video.list_indexes( use_for = "semantic" )
query_indexes = video.list_indexes( use_for = "query" )
aggregate_indexes = video.list_indexes( use_for = "aggregate" )
```

## [ Get one index](#get-one-index)

Use `get_index()` to inspect one index manifest.

```
index = video.get_index( name = "scene" )

print (index.status)
print (index.use_for)
print (index.fields)
```

You can also fetch by index ID:

```
index = video.get_index( index_id = "idx_scene_123" )
```

`get_index()` returns metadata and schema. It does not return every indexed record by default.

```
{
"index_id" : "idx_scene_123" ,
"name" : "scene" ,
"status" : "ready" ,
"use_for" : [ "semantic" , "query" , "aggregate" ],
"record_count" : 128 ,
"source" : {
"understanding_id" : "und_123" ,
"artifact" : "scene" ,
"analyzer" : { "name" : "scene" , "type" : "vlm" }
},
"fields" : {
"semantic" : [ "scene_description" , "activity" , "setting" ],
"filter" : [ "activity" , "setting" ],
"aggregate" : [ "activity" , "setting" ]
}
}
```

## [ Inspect field schema](#inspect-field-schema)

Because V2 indexes can support `query()` and `aggregate()` , users need to know which fields are available for each capability.

```
index = video.get_index( name = "scene" )

for field, schema in index.field_schema.items():
print (field, schema.type, schema.groups)
```

Example schema:

```
{
"scene_description" : {
"type" : "text" ,
"groups" : [ "semantic" ]
},
"activity" : {
"type" : "string" ,
"groups" : [ "semantic" , "filter" , "aggregate" ],
"operators" : [ "==" , "!=" , "contains" , "in" , "exists" ]
},
"setting" : {
"type" : "string" ,
"groups" : [ "semantic" , "filter" , "aggregate" ],
"operators" : [ "==" , "!=" , "contains" , "in" , "exists" ]
}
}
```

Use this schema to decide which retrieval API to call:

| Field group   | Retrieval API                                                                                   |
|---------------|-------------------------------------------------------------------------------------------------|
| `semantic`    | `video.semantic_search()` / `collection.semantic_search()` ; also used by high-level `search()` |
| `filter`      | `video.query()` / `collection.query()` ; optional filters in `search()` and `semantic_search()` |
| `aggregate`   | `video.aggregate()` / `collection.aggregate()`                                                  |
| `sort`        | result ordering in `query()` / `search()`                                                       |

## [ Preview indexed records](#preview-indexed-records)

Use record preview when you want to inspect what was indexed.

```
page = index.records( limit = 20 )

for record in page.records:
print (record.start, record.end, record.data)
```

Example record:

```
{
"video_id" : "m-123" ,
"understanding_id" : "und-123" ,
"scene_id" : "scene-000002" ,
"start" : 3.42 ,
"end" : 7.1 ,
"data" : {
"scene_description" : "A person walks through a retail aisle while holding a phone." ,
"activity" : "walking through store" ,
"setting" : "retail aisle" ,
"frames" : [
{ "timestamp" : 4.8 , "asset" : { "type" : "s3_object" , "key" : "..." }}
]
}
}
```

Records are paginated:

```
page = index.records( limit = 50 )
next_page = index.records( limit = 50 , cursor = page.next_cursor)
```

`index.records()` is for inspection and debugging. For retrieval, filtering, ranking, and analytics, use `search()` , `semantic_search()` , `query()` , and `aggregate()` .

## [ Search APIs remain separate from index inspection](#search-apis-remain-separate-from-index-inspection)

`get_index()` tells you what is possible. It does not duplicate retrieval APIs. For direct semantic search:

```
results = video.semantic_search(
query = "person holding a phone" ,
index_names = [ "scene" ],
)
```

For structured filtering on the scene index:

```
results = video.query(
index_name = "scene" ,
filter = { "activity" : "walking through store" },
)
```

For object filters, query the objects index:

```
results = video.query(
index_name = "objects" ,
filter = { "object_labels" : { "contains" : "phone" }},
)
```

For counts and facets, use the index that owns the field:

```
response = collection.aggregate(
index_name = "brands" ,
group_by = "brand_names" ,
)
counts = response[ "results" ]
```

## [ Delete an index](#delete-an-index)

Delete by id from the video, or call `delete()` on an `Index` object you already hold:

```
video.delete_index( index_id = "idx_scene_123" )

# or, given an Index object
index = video.get_index( name = "scene" )
index.delete()
```

Deleting an index removes the retrieval structures for that index. It does not delete the original video or stored understanding artifacts.

## [ Next steps](#next-steps)

## Search APIs

Retrieve from the indexes you inspected.

## Index Fields

Configure which fields become semantic text, filters, facets, and sort keys.

[Index Fields](\pages\understand\indexing-pipelines\multiple-indexes) [Search and Retrieval](\pages\understand\search-and-retrieval\natural-language-query)

⌘ I