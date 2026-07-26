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
- [TypeScript Support](#typescript-support)
- [Module Formats](#module-formats)
- [Basic Usage](#basic-usage)
- [Server Side](#server-side)
- [Client Side](#client-side)
- [Next Steps](#next-steps)

[Start Here](\index)

[SDK Installation](\pages\getting-started\python)

# Node.js SDK

Copy page

Install and configure the VideoDB Node.js SDK

Copy page

## [ Installation](#installation)

```
npm install videodb
# or
yarn add videodb
```

## npm

View package on npm

## GitHub

Source code and issues

## [ Quick Start](#quick-start)

```
import { connect } from 'videodb' ;

// Connect using environment variable
const conn = connect ();

// Or pass API key directly
const conn = connect ({ apiKey: "your-api-key" });
```

## [ Environment Variables](#environment-variables)

| Variable          | Description                                                                                                                                                                     |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `VIDEODB_API_KEY` | Your API key from [console.videodb.io](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs) |

```
export VIDEODB_API_KEY = "your-api-key"
```

## [ TypeScript Support](#typescript-support)

Full TypeScript definitions are included. No additional packages needed.

```
import { connect , Video , SearchResult } from 'videodb' ;

const conn = connect ();
const video : Video = await conn . uploadURL ( "default" , { url: "..." });
const results : SearchResult = await video . search ( "query" );
```

## [ Module Formats](#module-formats)

Both ESM and CommonJS are supported:

```
// ESM
import { connect } from 'videodb' ;

// CommonJS
const { connect } = require ( 'videodb' );
```

## [ Basic Usage](#basic-usage)

```
import { connect } from 'videodb' ;

const conn = connect ();

// Upload a video
const video = await conn . uploadURL ( "default" , {
url: "https://www.youtube.com/watch?v=example"
});

// Index for search
await video . indexSpokenWords ();

// Search with natural language
const results = await video . search ( "key moments" );
for ( const shot of results . shots ) {
console . log ( ` ${ shot . start } s: ${ shot . text } ` );
}
```

## [ Server Side](#server-side)

Use the full SDK on your backend to manage sessions, run AI pipelines, and handle webhooks. Your API key should never be exposed to the browser.

```
// Create a capture session and generate a client token
const cap = await conn . createCaptureSession ({ endUserId: "user_123" });
const token = await conn . generateClientToken ( 600 );
```

## [ Client Side](#client-side)

For real-time desktop capture, install the Capture SDK on your client application. It uses short-lived tokens instead of your API key.

Desktop capture currently supports **macOS** and **Windows** .

```
npm install videodb
```

## Capture SDK Overview

Learn how to integrate real-time screen, audio, and camera capture into your application

## [ Next Steps](#next-steps)

## Quickstart

Build your first perception-enabled agent

## API Reference

Complete REST API documentation

[Python SDK](\pages\getting-started\python) [Node.js SDK v0.2.0 Migration](\pages\getting-started\node-migration)

⌘ I