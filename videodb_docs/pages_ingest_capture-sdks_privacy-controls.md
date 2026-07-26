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
    - [Capture SDK Overview](\pages\ingest\capture-sdks\overview)
    - [Real-time Context](\pages\ingest\capture-sdks\realtime-context)
    - [Storage &amp; Search](\pages\ingest\capture-sdks\storage-and-search)
    - [Privacy Controls](\pages\ingest\capture-sdks\privacy-controls)
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
- [Trust Model](#trust-model)
    - [Two-Component Architecture](#two-component-architecture)
    - [Token Pattern](#token-pattern)
- [Permission Handling](#permission-handling)
    - [Request Before Capture](#request-before-capture)
    - [Required UX Elements](#required-ux-elements)
- [Storage Control](#storage-control)
    - [Ephemeral Mode](#ephemeral-mode)
    - [Selective Storage](#selective-storage)
- [Data Retention](#data-retention)
    - [Default Behavior](#default-behavior)
    - [Manual Deletion](#manual-deletion)
    - [Implement Data Subject Access](#implement-data-subject-access)
- [Compliance Patterns](#compliance-patterns)
    - [GDPR](#gdpr)
    - [HIPAA](#hipaa)
    - [General Best Practices](#general-best-practices)
- [Summary](#summary)
- [Next Steps](#next-steps)

[Ingest](\pages\ingest\files-and-collections\upload-video)

[Capture SDKs](\pages\ingest\capture-sdks\overview)

# Privacy Controls

Copy page

Consent patterns, permission handling, and privacy-first capture

Copy page

Desktop capture handles sensitive data. Nothing records without explicit user consent. This page covers permission patterns, storage controls, and privacy-first design.

Desktop capture currently supports **macOS** and **Windows** .

## [ Quick Example](#quick-example)

Python

Node.js

```
from videodb.capture import CaptureClient

client = CaptureClient( client_token = token)

# Request explicit permissions (OS dialogs appear)
await client.request_permission( "microphone" )
await client.request_permission( "screen_capture" )

# User must grant permission before capture can start
channels = await client.list_channels()
```

```
import { CaptureClient } from 'videodb/capture' ;

const client = new CaptureClient ({ sessionToken: token });

// Request explicit permissions (OS dialogs appear)
await client . requestPermission ( 'microphone' );
await client . requestPermission ( 'screen-capture' );

// User must grant permission before capture can start
const channels = await client . listChannels ();
```

## [ Trust Model](#trust-model)

### [ Two-Component Architecture](#two-component-architecture)

Security is built into the architecture:

| Component      | Has API Key     | Can See Media             |
|----------------|-----------------|---------------------------|
| Backend        | Yes             | No (receives events only) |
| Desktop Client | No (uses token) | Yes (captures locally)    |

- **API key never leaves your backend**
- **Desktop client uses short-lived tokens** (10-15 min expiry recommended)
- **Compromised tokens have limited blast radius**

### [ Token Pattern](#token-pattern)

Python

Node.js

```
# Backend (holds API key)
conn = videodb.connect() # Uses VIDEODB_API_KEY

# Generate short-lived token for client
token = conn.generate_client_token( expires_in = 600 ) # 10 minutes

# Send token to desktop app (never send API key)
```

```
// Backend (holds API key)
const conn = connect (); // Uses VIDEO_DB_API_KEY

// Generate short-lived token for client
const token = await conn . generateClientToken ( 600 ); // 10 minutes

// Send token to desktop app (never send API key)
```

## [ Permission Handling](#permission-handling)

### [ Request Before Capture](#request-before-capture)

Python

Node.js

```
# Each permission triggers an OS dialog
await client.request_permission( "microphone" )
await client.request_permission( "screen_capture" )
# For system audio on macOS
await client.request_permission( "system_audio" )
```

```
// Each permission triggers an OS dialog
await client . requestPermission ( 'microphone' );
await client . requestPermission ( 'screen-capture' );
// For system audio on macOS
await client . requestPermission ( 'system-audio' );
```

### [ Required UX Elements](#required-ux-elements)

Your desktop client must include:

- **Recording indicator** - Visual cue that capture is active
- **Pause button** - Let users temporarily stop
- **Stop button** - Let users end the session

## [ Storage Control](#storage-control)

### [ Ephemeral Mode](#ephemeral-mode)

Process in real-time without persisting media:

Python

Node.js

```
await client.start_session(
capture_session_id = cap_id,
channels = [
{ "name" : "mic:default" , "store" : False }, # Process only
{ "name" : "display:1" , "store" : False }, # Process only
{ "name" : "system_audio:default" , "store" : False }
]
)
```

```
await client . startCaptureSession ({
sessionId: capId ,
channels: [
{ channelId: "mic:default" , store: false }, // Process only
{ channelId: "display:1" , store: false }, // Process only
{ channelId: "system_audio:default" , store: false }
]
});
```

**Use ephemeral mode when:**

- Processing sensitive content
- Storage isn't needed
- Privacy regulations require it
- Building real-time assistants only

### [ Selective Storage](#selective-storage)

Store only what you need:

Python

Node.js

```
await client.start_session(
capture_session_id = cap_id,
channels = [
{ "name" : "mic:default" , "store" : True }, # Keep for search
{ "name" : "display:1" , "store" : False }, # Don't store screen
{ "name" : "system_audio:default" , "store" : True }
]
)
```

```
await client . startCaptureSession ({
sessionId: capId ,
channels: [
{ channelId: "mic:default" , store: true }, // Keep for search
{ channelId: "display:1" , store: false }, // Don't store screen
{ channelId: "system_audio:default" , store: true }
]
});
```

## [ Data Retention](#data-retention)

### [ Default Behavior](#default-behavior)

- Media stored until explicitly deleted
- No automatic expiration
- Indexes and transcripts stored with media

### [ Manual Deletion](#manual-deletion)

Python

Node.js

```
# Delete capture session and all associated data
cap = conn.get_capture_session( "cap-xxx" )
cap.delete()

# Delete specific video
video = coll.get_video( "m-xxx" )
video.delete()
```

```
// Delete capture session and all associated data
const cap = await conn . getCaptureSession ( "cap-xxx" );
await cap . delete ();

// Delete specific video
const video = await coll . getVideo ( "m-xxx" );
await video . delete ();
```

### [ Implement Data Subject Access](#implement-data-subject-access)

Python

Node.js

```
def get_user_data ( end_user_id ):
"""Get all data for a user (GDPR access request)"""
sessions = conn.list_capture_sessions( end_user_id = end_user_id)
return { "sessions" : [s.to_dict() for s in sessions]}

def delete_user_data ( end_user_id ):
"""Delete all user data (GDPR deletion request)"""
sessions = conn.list_capture_sessions( end_user_id = end_user_id)
for session in sessions:
session.delete()
```

```
async function getUserData ( endUserId ) {
// Get all data for a user (GDPR access request)
const sessions = await conn . listCaptureSessions ({ endUserId });
return { sessions };
}

async function deleteUserData ( endUserId ) {
// Delete all user data (GDPR deletion request)
const sessions = await conn . listCaptureSessions ({ endUserId });
for ( const session of sessions ) {
await session . delete ();
}
}
```

## [ Compliance Patterns](#compliance-patterns)

### [ GDPR](#gdpr)

- Implement data access endpoints
- Implement deletion endpoints
- Document processing purposes
- Use ephemeral mode when storage isn't needed

### [ HIPAA](#hipaa)

- Use ephemeral mode for PHI
- Implement strict access controls
- Audit all data access
- Consider data minimization

### [ General Best Practices](#general-best-practices)

| Practice              | Implementation                    |
|-----------------------|-----------------------------------|
| Never expose API keys | Use client tokens                 |
| Default to ephemeral  | Only persist when needed          |
| Short token lifetimes | 10-15 minutes                     |
| Implement deletion    | Honor user requests               |
| Get consent           | Permission dialogs before capture |
| Show indicators       | Recording visible to user         |

## [ Summary](#summary)

**Key principles:**

- Nothing records without explicit user permission
- Storage is optional per-channel ( `store: false` )
- Visible recording indicators are required
- API key never leaves backend
- Tokens are short-lived and limited scope

## [ Next Steps](#next-steps)

## Capture Overview

Architecture and quickstart

## Real-time Context

Events you receive

[Storage &amp; Search](\pages\ingest\capture-sdks\storage-and-search) [When to Transcode](\pages\ingest\transcoding\when-to-transcode)

⌘ I