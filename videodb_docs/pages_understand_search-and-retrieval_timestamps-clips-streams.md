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
- [Search Result Structure](#search-result-structure)
    - [Shot Attributes](#shot-attributes)
    - [Accessing Results](#accessing-results)
- [Playback Options](#playback-options)
    - [Play Results](#play-results)
    - [Play Individual Shot](#play-individual-shot)
- [Generate Stream URLs](#generate-stream-urls)
    - [From Search Results](#from-search-results)
    - [From Custom Timestamps](#from-custom-timestamps)
    - [Stream URL Format](#stream-url-format)
- [Working with Timestamps](#working-with-timestamps)
    - [Extract Timestamps from Results](#extract-timestamps-from-results)
    - [Merge Overlapping Segments](#merge-overlapping-segments)
- [Embedding Streams](#embedding-streams)
    - [HTML Embed](#html-embed)
    - [React Component](#react-component)
    - [VideoDB Player](#videodb-player)
- [Filter and Sort Results](#filter-and-sort-results)
    - [By Score](#by-score)
    - [By Duration](#by-duration)
- [Next Steps](#next-steps)

[Understand](\pages\understand\indexing-pipelines\create-an-index)

[Search and Retrieval](\pages\understand\search-and-retrieval\natural-language-query)

# Timestamps, Clips, Streams

Copy page

Understand search results and generate playable video clips

Copy page

Search returns structured results with timestamps, descriptions, and relevance scores. Generate playable clips or stream URLs from any result.

## [ Quick Example](#quick-example)

Python

Node.js

```
results = video.search( "car chase scene" )

# Access individual shots
for shot in results.get_shots():
print ( f " { shot.start } s - { shot.end } s: { shot.text } " )
print ( f "Score: { shot.search_score } " )

# Play all matching segments
results.play()

# Generate a stream URL
stream_url = results.compile()
print (stream_url)
```

```
const results = await video . search ( "car chase scene" );

// Access individual shots
for ( const shot of results . shots ) {
console . log ( ` ${ shot . start } s - ${ shot . end } s: ${ shot . text } ` );
console . log ( `Score: ${ shot . searchScore } ` );
}

// Get stream URL
const streamUrl = await results . compile ();
console . log ( streamUrl );
```

## [ Search Result Structure](#search-result-structure)

Each search returns a `SearchResult` object containing matching shots:

### [ Shot Attributes](#shot-attributes)

| Attribute      | Type   | Description                       |
|----------------|--------|-----------------------------------|
| `start`        | float  | Start timestamp in seconds        |
| `end`          | float  | End timestamp in seconds          |
| `text`         | str    | Content description or transcript |
| `search_score` | float  | Relevance score (0-1)             |
| `stream_url`   | str    | Direct playback URL               |

### [ Accessing Results](#accessing-results)

Python

Node.js

```
results = video.search( "introduction to the topic" )

# Get all shots
shots = results.get_shots()

# Access first result
first_shot = shots[ 0 ]
print ( f "Starts at: { first_shot.start } " )
print ( f "Ends at: { first_shot.end } " )
print ( f "Content: { first_shot.text } " )
print ( f "Relevance: { first_shot.search_score } " )
```

```
const results = await video . search ( "introduction to the topic" );

// Get all shots
const shots = results . shots ;

// Access first result
const firstShot = shots [ 0 ];
console . log ( `Starts at: ${ firstShot . start } ` );
console . log ( `Ends at: ${ firstShot . end } ` );
console . log ( `Content: ${ firstShot . text } ` );
console . log ( `Relevance: ${ firstShot . searchScore } ` );
```

## [ Playback Options](#playback-options)

### [ Play Results](#play-results)

Python

Node.js

```
results = video.search( "product demo" )
results.play() # Opens matching segments in your default browser
```

```
const results = await video . search ( "product demo" );
const streamUrl = await results . compile ();
console . log ( streamUrl ); // Use this URL in a video player
```

### [ Play Individual Shot](#play-individual-shot)

Python

Node.js

```
results = video.search( "funny moments" )
shots = results.get_shots()

# Play just the first match
shots[ 0 ].play()
```

```
const results = await video . search ( "funny moments" );
const shots = results . shots ;

// Play just the first match
await shots [ 0 ]. play ();
```

## [ Generate Stream URLs](#generate-stream-urls)

Create playable URLs for embedding or sharing.

### [ From Search Results](#from-search-results)

Python

Node.js

```
results = video.search( "highlight reel" )
stream_url = results.compile()
# Returns: https://stream.videodb.io/v3/...
```

```
const results = await video . search ( "highlight reel" );
const streamUrl = await results . compile ();
// Returns: https://stream.videodb.io/v3/...
```

### [ From Custom Timestamps](#from-custom-timestamps)

Python

Node.js

```
# Generate stream from specific time ranges
timestamps = [
( 10.5 , 25.0 ), # First segment
( 45.0 , 60.0 ), # Second segment
( 120.0 , 135.5 ) # Third segment
]

stream_url = video.generate_stream(timestamps)
```

```
// Generate stream from specific time ranges
const timestamps = [
[ 10.5 , 25.0 ], // First segment
[ 45.0 , 60.0 ], // Second segment
[ 120.0 , 135.5 ] // Third segment
];

const streamUrl = await video . generateStream ( timestamps );
```

### [ Stream URL Format](#stream-url-format)

Generated URLs are HLS streams that work in any video player:

```
https://stream.videodb.io/v3/published/manifests/{manifest-id}.m3u8
```

## [ Working with Timestamps](#working-with-timestamps)

### [ Extract Timestamps from Results](#extract-timestamps-from-results)

Python

Node.js

```
results = video.search( "key moments" )

# Get as list of tuples
timestamps = [(shot.start, shot.end) for shot in results.get_shots()]
# [(5.2, 15.0), (45.5, 52.3), (120.0, 145.8)]
```

```
const results = await video . search ( "key moments" );

// Get as list of arrays
const timestamps = results . shots . map ( shot => [ shot . start , shot . end ]);
// [[5.2, 15.0], [45.5, 52.3], [120.0, 145.8]]
```

### [ Merge Overlapping Segments](#merge-overlapping-segments)

Python

Node.js

```
def merge_timestamps ( timestamps ):
"""Merge overlapping time ranges"""
if not timestamps:
return []

sorted_ts = sorted (timestamps)
merged = [ list (sorted_ts[ 0 ])]

for start, end in sorted_ts[ 1 :]:
if start <= merged[ - 1 ][ 1 ]:
merged[ - 1 ][ 1 ] = max (merged[ - 1 ][ 1 ], end)
else :
merged.append([start, end])

return merged

# Merge results from multiple searches
ts1 = [( 10 , 20 ), ( 15 , 25 )]
ts2 = [( 22 , 30 ), ( 50 , 60 )]
merged = merge_timestamps(ts1 + ts2)
# [[10, 30], [50, 60]]
```

```
function mergeTimestamps ( timestamps ) {
if ( timestamps . length === 0 ) return [];

const sorted = [ ... timestamps ]. sort (( a , b ) => a [ 0 ] - b [ 0 ]);
const merged = [[ ... sorted [ 0 ]]];

for ( const [ start , end ] of sorted . slice ( 1 )) {
const last = merged [ merged . length - 1 ];
if ( start <= last [ 1 ]) {
last [ 1 ] = Math . max ( last [ 1 ], end );
} else {
merged . push ([ start , end ]);
}
}

return merged ;
}

// Merge results from multiple searches
const ts1 = [[ 10 , 20 ], [ 15 , 25 ]];
const ts2 = [[ 22 , 30 ], [ 50 , 60 ]];
const merged = mergeTimestamps ([ ... ts1 , ... ts2 ]);
// [[10, 30], [50, 60]]
```

## [ Embedding Streams](#embedding-streams)

### [ HTML Embed](#html-embed)

```
< video controls >
< source src = "https://stream.videodb.io/v3/published/manifests/{id}.m3u8" type = "application/x-mpegURL" >
</ video >
```

### [ React Component](#react-component)

```
import Hls from 'hls.js' ;

function VideoPlayer ({ streamUrl }) {
const videoRef = useRef ( null );

useEffect (() => {
if ( Hls . isSupported ()) {
const hls = new Hls ();
hls . loadSource ( streamUrl );
hls . attachMedia ( videoRef . current );
}
}, [ streamUrl ]);

return < video ref = { videoRef } controls /> ;
}
```

### [ VideoDB Player](#videodb-player)

Use the built-in player with the console URL:

```
https://console.videodb.io/player?url={stream_url}
```

## [ Filter and Sort Results](#filter-and-sort-results)

### [ By Score](#by-score)

Python

Node.js

```
results = video.search( "important moments" )

# Get high-confidence results only
shots = results.get_shots()
high_confidence = [s for s in shots if s.search_score > 0.5 ]
```

```
const results = await video . search ( "important moments" );

// Get high-confidence results only
const shots = results . shots ;
const highConfidence = shots . filter ( s => s . searchScore > 0.5 );
```

### [ By Duration](#by-duration)

Python

Node.js

```
results = video.search( "long segments" )

# Get segments longer than 10 seconds
shots = results.get_shots()
long_segments = [s for s in shots if (s.end - s.start) > 10 ]
```

```
const results = await video . search ( "long segments" );

// Get segments longer than 10 seconds
const shots = results . shots ;
const longSegments = shots . filter ( s => ( s . end - s . start ) > 10 );
```

## [ Next Steps](#next-steps)

## Collection Search

Search across your entire library

## Accuracy Tips

Improve search precision

[Natural Language Query](\pages\understand\search-and-retrieval\natural-language-query) [Collection Search](\pages\understand\search-and-retrieval\collection-search)

⌘ I