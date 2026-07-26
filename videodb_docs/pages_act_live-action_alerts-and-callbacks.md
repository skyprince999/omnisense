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
    - [Event Detection Patterns](\pages\act\live-action\event-detection-patterns)
    - [Alerts and Callbacks](\pages\act\live-action\alerts-and-callbacks)
    - [Webhooks and Reliability](\pages\act\live-action\webhooks-and-reliability)
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
- [Delivery Methods](#delivery-methods)
- [Webhook Delivery](#webhook-delivery)
    - [Create Webhook Alert](#create-webhook-alert)
    - [Webhook Payload](#webhook-payload)
    - [Payload Fields](#payload-fields)
- [WebSocket Delivery](#websocket-delivery)
    - [Connect and Listen](#connect-and-listen)
    - [WebSocket Channels](#websocket-channels)
- [Managing Alerts](#managing-alerts)
    - [List Alerts](#list-alerts)
    - [Enable/Disable Alerts](#enable%2Fdisable-alerts)
    - [Delete Alert](#delete-alert)
- [Dual Delivery Pattern](#dual-delivery-pattern)
- [Latency Profile](#latency-profile)
- [Delivery Guarantees](#delivery-guarantees)
- [Next Steps](#next-steps)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Live Action](\pages\act\live-action\event-detection-patterns)

# Alerts and Callbacks

Copy page

Wire events to delivery channels for real-time notifications

Copy page

Alerts connect events to delivery channels. Choose WebSocket for real-time dashboards or webhooks for server-to-server notifications.

## [ Quick Example](#quick-example)

Python

Node.js

```
# Create alert with webhook delivery
alert_id = scene_index.create_alert(
event_id = event_id,
callback_url = "https://your-backend.com/alerts"
)

# Or with WebSocket delivery
ws = conn.connect_websocket()
await ws.connect()

alert_id = scene_index.create_alert(
event_id = event_id,
ws_connection_id = ws.connection_id
)
```

```
// Create alert with webhook delivery
const alertId = await sceneIndex . createAlert (
eventId ,
"https://your-backend.com/alerts"
);

// Or with WebSocket delivery
const ws = conn . connectWebsocket ();
await ws . connect ();

const alertId = await sceneIndex . createAlert (
eventId ,
null , // no webhook
ws . connectionId
);
```

## [ Delivery Methods](#delivery-methods)

| Method    | Latency   | Use Case                     |
|-----------|-----------|------------------------------|
| WebSocket | Real-time | Dashboards, live UI updates  |
| Webhook   | Under 1s  | Server-to-server, automation |

You can use both simultaneously for redundancy.

## [ Webhook Delivery](#webhook-delivery)

### [ Create Webhook Alert](#create-webhook-alert)

Python

Node.js

```
alert_id = scene_index.create_alert(
event_id = event_id,
callback_url = "https://your-backend.com/webhooks/alerts"
)
```

```
const alertId = await sceneIndex . createAlert (
eventId ,
"https://your-backend.com/webhooks/alerts"
);
```

### [ Webhook Payload](#webhook-payload)

When an event triggers, you receive a POST request:

```
{
"event_id" : "event-3fd4174feceb6162" ,
"label" : "traffic_violation" ,
"confidence" : 0.95 ,
"explanation" : "A red sedan ran through the intersection while the light was red" ,
"timestamp" : "2024-01-15T10:30:45Z" ,
"start_time" : 1234.5 ,
"end_time" : 1238.0 ,
"stream_url" : "https://stream.videodb.io/v3/..." ,
"player_url" : "https://console.videodb.io/player?url=..."
}
```

### [ Payload Fields](#payload-fields)

| Field         | Type   | Description                                   |
|---------------|--------|-----------------------------------------------|
| `event_id`    | string | ID of the triggered event                     |
| `label`       | string | Human-readable event label                    |
| `confidence`  | float  | Detection confidence (0-1)                    |
| `explanation` | string | AI-generated description of what was detected |
| `timestamp`   | string | ISO 8601 timestamp                            |
| `start_time`  | float  | Video timestamp where event starts (seconds)  |
| `end_time`    | float  | Video timestamp where event ends (seconds)    |
| `stream_url`  | string | HLS stream URL for the clip                   |
| `player_url`  | string | Web player URL                                |

## [ WebSocket Delivery](#websocket-delivery)

### [ Connect and Listen](#connect-and-listen)

Python

Node.js

```
ws = conn.connect_websocket()
await ws.connect()

# Pass connection ID when creating alerts
alert_id = scene_index.create_alert(
event_id = event_id,
ws_connection_id = ws.connection_id
)

# Listen for events
async for event in ws.stream():
if event.get( "channel" ) == "alert" :
print ( f "Alert: { event[ 'data' ][ 'label' ] } " )
print ( f "Confidence: { event[ 'data' ][ 'confidence' ] } " )
```

```
const ws = conn . connectWebsocket ();
await ws . connect ();

// Pass connection ID when creating alerts
const alertId = await sceneIndex . createAlert (
eventId ,
null ,
ws . connectionId
);

// Listen for events
for await ( const event of ws . stream ()) {
if ( event . channel === "alert" ) {
console . log ( `Alert: ${ event . data . label } ` );
console . log ( `Confidence: ${ event . data . confidence } ` );
}
}
```

### [ WebSocket Channels](#websocket-channels)

| Channel       | Source               | Content             |
|---------------|----------------------|---------------------|
| `alert`       | Event triggers       | Alert notifications |
| `transcript`  | `start_transcript()` | Real-time speech    |
| `scene_index` | `index_visuals()`    | Visual analysis     |
| `audio_index` | `index_audio()`      | Audio analysis      |

## [ Managing Alerts](#managing-alerts)

### [ List Alerts](#list-alerts)

Python

Node.js

```
alerts = scene_index.list_alerts()
for alert in alerts:
print ( f " { alert.id } : { alert.event_id } - { alert.status } " )
```

```
const alerts = await sceneIndex . listAlerts ();
for ( const alert of alerts ) {
console . log ( ` ${ alert . id } : ${ alert . eventId } - ${ alert . status } ` );
}
```

### [ Enable/Disable Alerts](#enable\disable-alerts)

Python

Node.js

```
# Temporarily disable
scene_index.disable_alert(alert_id)

# Re-enable
scene_index.enable_alert(alert_id)
```

```
// Temporarily disable
await sceneIndex . disableAlert ( alertId );

// Re-enable
await sceneIndex . enableAlert ( alertId );
```

### [ Delete Alert](#delete-alert)

Python

Node.js

```
scene_index.delete_alert(alert_id)
```

```
await sceneIndex . deleteAlert ( alertId );
```

## [ Dual Delivery Pattern](#dual-delivery-pattern)

Use both channels for critical alerts:

Python

Node.js

```
# WebSocket for real-time UI
ws = conn.connect_websocket()
await ws.connect()

# Create alert with both delivery methods
alert_id = scene_index.create_alert(
event_id = event_id,
callback_url = "https://your-backend.com/alerts" , # webhook
ws_connection_id = ws.connection_id # websocket
)
```

```
// WebSocket for real-time UI
const ws = conn . connectWebsocket ();
await ws . connect ();

// Create alert with both delivery methods
const alertId = await sceneIndex . createAlert (
eventId ,
"https://your-backend.com/alerts" , // webhook
ws . connectionId // websocket
);
```

**Benefits:**

- WebSocket delivers instantly to connected clients
- Webhook provides reliable server-side processing
- If WebSocket disconnects, webhook still works

## [ Latency Profile](#latency-profile)

| Event Type         | Typical Latency   |
|--------------------|-------------------|
| Alert trigger      | Under 1s          |
| Transcript event   | 1-2s              |
| Visual index event | 2-5s              |
| Audio index event  | 2-5s              |

## [ Delivery Guarantees](#delivery-guarantees)

| Method    | Guarantee     | Notes                                   |
|-----------|---------------|-----------------------------------------|
| WebSocket | At-most-once  | May miss events if disconnected         |
| Webhook   | At-least-once | May receive duplicates; use idempotency |

## [ Next Steps](#next-steps)

## Webhooks and Reliability

Handle webhooks at scale with idempotency

## Event Detection Patterns

Create effective detection rules

[Event Detection Patterns](\pages\act\live-action\event-detection-patterns) [Webhooks and Reliability](\pages\act\live-action\webhooks-and-reliability)

⌘ I