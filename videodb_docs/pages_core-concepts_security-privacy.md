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

- [When to Reference This](#when-to-reference-this)
- [Quick Example](#quick-example)
- [Next Steps](#next-steps)
- [Storage Modes](#storage-modes)
    - [Persistent Storage (Default)](#persistent-storage-default)
    - [Ephemeral Processing](#ephemeral-processing)
- [Retention Patterns](#retention-patterns)
    - [Default Retention](#default-retention)
    - [Manual Deletion](#manual-deletion)
    - [Recommended Patterns](#recommended-patterns)
- [API Key Security](#api-key-security)
    - [Key Management](#key-management)
    - [Key Operations](#key-operations)
- [Client Token Pattern](#client-token-pattern)
- [Consent Patterns](#consent-patterns)
    - [User Consent for Capture](#user-consent-for-capture)
    - [Data Subject Access](#data-subject-access)
- [Network Security](#network-security)
    - [HTTPS](#https)
    - [Webhook Security](#webhook-security)
- [Compliance Considerations](#compliance-considerations)
    - [GDPR](#gdpr)
    - [HIPAA](#hipaa)
    - [SOC 2](#soc-2)
- [Best Practices Summary](#best-practices-summary)

[Core Concepts](\pages\core-concepts\overview)

# Security &amp; Privacy

Copy page

VideoDB handles sensitive media data. Understand storage modes, data retention, and privacy patterns to build compliant systems.

Copy page

## [ When to Reference This](#when-to-reference-this)

Use this page when you're:

- Designing systems with privacy requirements
- Choosing storage and retention policies
- Implementing consent workflows
- Securing API access patterns

## [ Quick Example](#quick-example)

```
import videodb

# Secure connection
conn = videodb.connect() # Uses VIDEODB_API_KEY env var

# Desktop capture with client tokens (never expose API key)
cap = conn.create_capture_session(
end_user_id = "user_abc" ,
callback_url = "https://your-backend.com/webhooks"
)
token = conn.generate_client_token( expires_in = 600 ) # Short-lived
```

## [ Next Steps](#next-steps)

## Capture Session

Secure desktop capture patterns

## API Reference

API key management

## [ Storage Modes](#storage-modes)

### [ Persistent Storage (Default)](#persistent-storage-default)

Media and derived data are stored for retrieval and search:

```
video = coll.upload( url = "https://..." ) # Stored
index = video.index_scenes( ... ) # Stored
results = video.search( "query" ) # Searchable
```

**Use for:**

- Video archives and libraries
- Searchable knowledge bases
- Long-term agent memory

### [ Ephemeral Processing](#ephemeral-processing)

Process in real-time without persistent storage:

```
# Real-time processing only
rtstream.index_visuals(
prompt = "Monitor for activity" ,
ephemeral = True # Process but don't store
)
```

**Use for:**

- Live monitoring dashboards
- Real-time alerts without storage
- Privacy-sensitive contexts

## [ Retention Patterns](#retention-patterns)

### [ Default Retention](#default-retention)

- Media stored until explicitly deleted
- Indexes and metadata stored with media
- No automatic expiration

### [ Manual Deletion](#manual-deletion)

```
# Delete video and all associated data
video.delete()

# Delete specific index
index.delete()

# Delete collection
coll.delete()
```

### [ Recommended Patterns](#recommended-patterns)

| Use Case           | Pattern                               |
|--------------------|---------------------------------------|
| Temporary analysis | Ephemeral mode                        |
| GDPR compliance    | Implement deletion on user request    |
| Meeting recordings | Define retention policy, batch delete |
| Security footage   | Time-based archival and deletion      |

## [ API Key Security](#api-key-security)

### [ Key Management](#key-management)

```
# Environment variable (recommended)
conn = videodb.connect() # Uses VIDEODB_API_KEY

# Explicit key (server-side only)
conn = videodb.connect( api_key = "your-key" )
```

**Best practices:**

- Never embed keys in client applications
- Use environment variables
- Rotate keys periodically
- Use separate keys for dev/prod

### [ Key Operations](#key-operations)

```
# Create new key
new_key = conn.create_api_key( name = "production" )

# List keys
keys = conn.list_api_keys()

# Delete key
conn.delete_api_key(key_id)
```

## [ Client Token Pattern](#client-token-pattern)

For desktop and mobile clients, use short-lived tokens instead of API keys:

```
# Backend (holds API key)
token = conn.generate_client_token( expires_in = 600 ) # 10 minutes

# Client (uses token, never sees API key)
client = CaptureClient( client_token = token)
```

**Why this matters:**

- Tokens expire automatically
- Tokens have limited scope
- Compromised tokens have limited blast radius
- API key never leaves your backend

## [ Consent Patterns](#consent-patterns)

### [ User Consent for Capture](#user-consent-for-capture)

Before capturing screen, mic, or camera:

```
# Request explicit permission
await client.request_permission( "microphone" )
await client.request_permission( "screen_capture" )

# User must grant permission in OS dialog
channels = await client.list_channels()
```

### [ Data Subject Access](#data-subject-access)

Implement endpoints for user data requests:

```
# Get all data for a user
def get_user_data ( end_user_id ):
sessions = conn.list_capture_sessions( end_user_id = end_user_id)
videos = coll.list_videos( metadata = { "user_id" : end_user_id})
return { "sessions" : sessions, "videos" : videos}

# Delete all user data
def delete_user_data ( end_user_id ):
sessions = conn.list_capture_sessions( end_user_id = end_user_id)
for session in sessions:
session.delete()
# Delete associated RTStreams and indexes
```

## [ Network Security](#network-security)

### [ HTTPS](#https)

All API communication uses HTTPS. No configuration needed.

### [ Webhook Security](#webhook-security)

Verify webhook payloads to prevent spoofing:

```
@app.post ( "/webhooks/videodb" )
async def handle_webhook ( request ):
# Verify signature (implementation depends on your setup)
signature = request.headers.get( "X-VideoDB-Signature" )
if not verify_signature(request.body, signature):
return { "error" : "Invalid signature" }, 401

event = await request.json()
process_event(event)
return { "status" : "ok" }
```

## [ Compliance Considerations](#compliance-considerations)

### [ GDPR](#gdpr)

- Implement data access endpoints
- Implement deletion endpoints
- Document data processing purposes
- Use ephemeral mode when storage isn't needed

### [ HIPAA](#hipaa)

- Use ephemeral mode for sensitive content
- Implement strict access controls
- Audit all data access
- Consider on-premise deployment for PHI

### [ SOC 2](#soc-2)

- VideoDB maintains SOC 2 compliance
- Implement access logging
- Use separate keys per environment
- Regular key rotation

## [ Best Practices Summary](#best-practices-summary)

1. **Never expose API keys** - Use client tokens for untrusted clients
2. **Default to ephemeral** - Only persist data when needed
3. **Implement deletion** - Honor data deletion requests
4. **Short token lifetimes** - 10-15 minutes for desktop capture
5. **Audit access** - Log who accesses what data
6. **Encrypt at rest** - VideoDB encrypts stored data
7. **Get consent** - Always get user permission before capture

[Programmable Editing](\pages\core-concepts\programmable-editing) [Upload Video](\pages\ingest\files-and-collections\upload-video)

⌘ I