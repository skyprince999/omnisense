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
- [Events vs Alerts](#events-vs-alerts)
- [Delivery Methods](#delivery-methods)
    - [WebSocket](#websocket)
    - [Webhook](#webhook)
- [Latency Profile](#latency-profile)
- [Delivery Guarantees](#delivery-guarantees)
- [Event Channels](#event-channels)
- [Best Practices](#best-practices)
- [What You Can Build](#what-you-can-build)
- [Next Steps](#next-steps)

[Core Concepts](\pages\core-concepts\overview)

# Events &amp; Real-time

Copy page

Events and alerts turn understanding into action. VideoDB processes live media with sub-second latency, delivering events via WebSocket or webhook.

Copy page

## [ Quick Example](#quick-example)

```
import videodb

conn = videodb.connect()
ws = conn.connect_websocket()
await ws.connect()

# Create detection rule (reusable)
event_id = conn.create_event(
event_prompt = "Detect intruder" ,
label = "security_alert"
)

# Wire to index with delivery method
index.create_alert(
event_id = event_id,
callback_url = "https://your-backend.com/alerts" , # Webhook
ws_connection_id = ws.connection_id # Real-time
)

# Alerts fire in <1 second
async for event in ws.stream():
if event.get( "channel" ) == "alert" :
print ( f "ALERT: { event[ 'data' ][ 'text' ] } " )
```

## [ Events vs Alerts](#events-vs-alerts)

| Concept   | Purpose                        | Example                        |
|-----------|--------------------------------|--------------------------------|
| **Event** | What to detect (reusable rule) | "Detect person without helmet" |
| **Alert** | Where to deliver (wiring)      | Webhook URL, WebSocket ID      |

```
# Events are reusable across streams
safety_event = conn.create_event(
event_prompt = "Detect safety violation" ,
label = "safety"
)

# Alerts wire events to specific indexes
for rtstream in streams:
index = rtstream.get_scene_index(index_id)
index.create_alert( event_id = safety_event)
```

## [ Delivery Methods](#delivery-methods)

| Method        | Latency        | Use Case                     |
|---------------|----------------|------------------------------|
| **WebSocket** | Real-time      | Dashboards, interactive apps |
| **Webhook**   | Near real-time | Automation, integrations     |

### [ WebSocket](#websocket)

```
ws = conn.connect_websocket()
await ws.connect()

async for event in ws.stream():
channel = event.get( "channel" )
# transcript, scene_index, audio_index, alert
```

### [ Webhook](#webhook)

```
index.create_alert(
event_id = event_id,
callback_url = "https://your-backend.com/alerts"
)
```

Payload:

```
{
"event_label" : "intrusion" ,
"rtstream_id" : "rts-xxx" ,
"timestamp" : 1710000012340 ,
"data" : { "text" : "Person in restricted area" }
}
```

## [ Latency Profile](#latency-profile)

| Operation          | Typical Latency   |
|--------------------|-------------------|
| Alert trigger      | < 1 second        |
| Transcript event   | 1-2 seconds       |
| Visual index event | 2-5 seconds       |
| Search query       | < 500ms           |

## [ Delivery Guarantees](#delivery-guarantees)

| Method    | Guarantee     | Handle             |
|-----------|---------------|--------------------|
| WebSocket | At-most-once  | Client reconnects  |
| Webhook   | At-least-once | Idempotency checks |

```
# Webhook idempotency
@app.post ( "/webhooks" )
async def handle ( request ):
event = await request.json()
if already_processed(event[ "event_id" ]):
return { "status" : "ok" }
process(event)
```

## [ Event Channels](#event-channels)

| Channel       | Source               | Content             |
|---------------|----------------------|---------------------|
| `transcript`  | `start_transcript()` | Speech-to-text      |
| `scene_index` | `index_visuals()`    | Visual analysis     |
| `audio_index` | `index_audio()`      | Audio analysis      |
| `alert`       | `create_alert()`     | Alert notifications |

## [ Best Practices](#best-practices)

1. **Make events reusable** - Define once, use across streams
2. **Be specific in prompts** - "Detect person falling" beats "detect problems"
3. **Use both methods** - WebSocket for UI, webhooks for automation
4. **Handle idempotency** - Webhooks may deliver duplicates

## [ What You Can Build](#what-you-can-build)

## Baby Crib Monitoring

Real-time infant monitoring with AI-powered alerts

## Intrusion Detection

Sub-second alerts when unauthorized access is detected

## Traffic Violations

Real-time detection of red light and stop sign violations

## [ Next Steps](#next-steps)

## RTStream Reference

Complete real-time API

## Webhooks Guide

Setting up callbacks

[Indexes &amp; Search](\pages\core-concepts\indexes-and-search) [Programmable Editing](\pages\core-concepts\programmable-editing)

⌘ I