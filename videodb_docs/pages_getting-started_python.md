### Start Here

- [Welcome to VideoDB](\)
- [Quickstart](\pages\getting-started\quickstart)
- SDK Installation
    - [Python SDK](\pages\getting-started\python)
    - [Node.js SDK](\pages\getting-started\node)
    - [Node.js SDK v0.2.0 Migration](\pages\getting-started\node-migration)
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

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Requirements](#requirements)
- [Basic Usage](#basic-usage)
- [Server Side](#server-side)
- [Client Side](#client-side)
- [Next Steps](#next-steps)

[Start Here](\index)

[SDK Installation](\pages\getting-started\python)

# Python SDK

Copy page

Install and configure the VideoDB Python SDK

Copy page

## [ Installation](#installation)

```
pip install videodb
```

## PyPI

View package on PyPI

## GitHub

Source code and issues

## [ Quick Start](#quick-start)

```
import videodb

# Connect using environment variable
conn = videodb.connect()

# Or pass API key directly
conn = videodb.connect( api_key = "your-api-key" )
```

## [ Environment Variables](#environment-variables)

| Variable          | Description                                                                                                                                                                     |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `VIDEODB_API_KEY` | Your API key from [console.videodb.io](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) |

```
export VIDEODB_API_KEY = "your-api-key"
```

## [ Requirements](#requirements)

- Python 3.8 or higher
- Works on Linux, macOS, and Windows

## [ Basic Usage](#basic-usage)

```
import videodb

conn = videodb.connect()

# Upload a video
coll = conn.get_collection()
video = coll.upload( url = "https://www.youtube.com/watch?v=example" )

# Index for search
video.index_spoken_words()

# Search with natural language
results = video.search( "key moments" )
for shot in results.shots:
print ( f " { shot.start } s: { shot.text } " )
```

## [ Server Side](#server-side)

Use the full SDK on your backend to manage sessions, run AI pipelines, and handle webhooks. Your API key should never be exposed to the browser.

```
# Create a capture session and generate a client token
cap = conn.create_capture_session( end_user_id = "user_123" )
token = conn.generate_client_token( expires_in = 600 )
```

## [ Client Side](#client-side)

For real-time desktop capture, install the Capture SDK on your client application. It uses short-lived tokens instead of your API key.

Desktop capture currently supports **macOS** and **Windows** .

```
pip install "videodb[capture]"
```

## Capture SDK Overview

Learn how to integrate real-time screen, audio, and camera capture into your application

## [ Next Steps](#next-steps)

## Quickstart

Build your first perception-enabled agent

## API Reference

Complete REST API documentation

[Quickstart](\pages\getting-started\quickstart) [Node.js SDK](\pages\getting-started\node)

⌘ I