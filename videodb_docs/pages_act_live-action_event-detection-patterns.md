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
- [Events vs Alerts](#events-vs-alerts)
- [Creating Events](#creating-events)
    - [Basic Event](#basic-event)
    - [Event Prompt Best Practices](#event-prompt-best-practices)
- [Detection Patterns by Use Case](#detection-patterns-by-use-case)
    - [Security &amp; Safety](#security-%26-safety)
    - [Retail &amp; Operations](#retail-%26-operations)
    - [Traffic &amp; Transportation](#traffic-%26-transportation)
- [Managing Events](#managing-events)
    - [List Events](#list-events)
    - [Get Event Details](#get-event-details)
    - [Delete Event](#delete-event)
- [Prompt Engineering Tips](#prompt-engineering-tips)
    - [Be Specific About Conditions](#be-specific-about-conditions)
    - [Include Context](#include-context)
    - [Describe What "Detected" Means](#describe-what-%E2%80%9Cdetected%E2%80%9D-means)
- [Event-Index Pairing](#event-index-pairing)
- [What You Can Build](#what-you-can-build)
- [Next Steps](#next-steps)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Live Action](\pages\act\live-action\event-detection-patterns)

# Event Detection Patterns

Copy page

Events are reusable detection rules that define what to look for in video. Create once, attach to any index, and receive alerts when conditions match.

Copy page

## [ Quick Example](#quick-example)

Python

Node.js

```
import videodb

conn = videodb.connect()

# Create a reusable event
event_id = conn.create_event(
event_prompt = "Detect when a person enters a restricted area" ,
label = "intrusion_detected"
)

# Attach to a scene index
scene_index.create_alert(
event_id = event_id,
callback_url = "https://your-backend.com/alerts"
)
```

```
import { connect } from 'videodb' ;

const conn = connect ();

// Create a reusable event
const eventId = await conn . createEvent (
"Detect when a person enters a restricted area" ,
"intrusion_detected"
);

// Attach to a scene index
await sceneIndex . createAlert (
eventId ,
"https://your-backend.com/alerts"
);
```

## [ Events vs Alerts](#events-vs-alerts)

| Concept   | What It Is                      | Scope                   |
|-----------|---------------------------------|-------------------------|
| **Event** | Detection rule (prompt + label) | Account-level, reusable |
| **Alert** | Wiring between event and index  | Index-specific          |

Think of events as templates. Create them once, then wire them to multiple indexes via alerts.

## [ Creating Events](#creating-events)

### [ Basic Event](#basic-event)

Python

Node.js

```
event_id = conn.create_event(
event_prompt = "Detect when someone falls down" ,
label = "fall_detected"
)
```

```
const eventId = await conn . createEvent (
"Detect when someone falls down" ,
"fall_detected"
);
```

### [ Event Prompt Best Practices](#event-prompt-best-practices)

The `event_prompt` is what the AI uses to evaluate each indexed scene. Be specific:

```
# Too vague - will trigger on many scenes
event_prompt = "Detect anything unusual"

# Better - specific condition
event_prompt = "Detect when a vehicle runs a red light"

# Best - specific with context
event_prompt = "Detect when a vehicle enters the intersection while the traffic light is red"
```

## [ Detection Patterns by Use Case](#detection-patterns-by-use-case)

### [ Security &amp; Safety](#security-&-safety)

Python

Node.js

```
# Intrusion detection
conn.create_event(
event_prompt = "Detect when a person enters the warehouse after hours" ,
label = "after_hours_entry"
)

# Fall detection
conn.create_event(
event_prompt = "Detect when a person falls or collapses" ,
label = "fall_detected"
)

# Unauthorized access
conn.create_event(
event_prompt = "Detect when someone accesses the server room without a badge" ,
label = "unauthorized_access"
)
```

```
// Intrusion detection
await conn . createEvent (
"Detect when a person enters the warehouse after hours" ,
"after_hours_entry"
);

// Fall detection
await conn . createEvent (
"Detect when a person falls or collapses" ,
"fall_detected"
);

// Unauthorized access
await conn . createEvent (
"Detect when someone accesses the server room without a badge" ,
"unauthorized_access"
);
```

### [ Retail &amp; Operations](#retail-&-operations)

Python

Node.js

```
# Queue detection
conn.create_event(
event_prompt = "Detect when more than 5 people are waiting in line" ,
label = "queue_long"
)

# Spill detection
conn.create_event(
event_prompt = "Detect liquid spills on the floor" ,
label = "spill_detected"
)

# Shelf monitoring
conn.create_event(
event_prompt = "Detect when a shelf appears empty or low on products" ,
label = "shelf_empty"
)
```

```
// Queue detection
await conn . createEvent (
"Detect when more than 5 people are waiting in line" ,
"queue_long"
);

// Spill detection
await conn . createEvent (
"Detect liquid spills on the floor" ,
"spill_detected"
);

// Shelf monitoring
await conn . createEvent (
"Detect when a shelf appears empty or low on products" ,
"shelf_empty"
);
```

### [ Traffic &amp; Transportation](#traffic-&-transportation)

Python

Node.js

```
# Traffic violation
conn.create_event(
event_prompt = "Detect when a vehicle runs a red light or stop sign" ,
label = "traffic_violation"
)

# Wrong-way driving
conn.create_event(
event_prompt = "Detect a vehicle driving in the wrong direction" ,
label = "wrong_way"
)

# Congestion
conn.create_event(
event_prompt = "Detect when traffic has stopped or is moving very slowly" ,
label = "congestion_detected"
)
```

```
// Traffic violation
await conn . createEvent (
"Detect when a vehicle runs a red light or stop sign" ,
"traffic_violation"
);

// Wrong-way driving
await conn . createEvent (
"Detect a vehicle driving in the wrong direction" ,
"wrong_way"
);

// Congestion
await conn . createEvent (
"Detect when traffic has stopped or is moving very slowly" ,
"congestion_detected"
);
```

## [ Managing Events](#managing-events)

### [ List Events](#list-events)

Python

Node.js

```
events = conn.list_events()
for event in events:
print ( f " { event.id } : { event.label } " )
```

```
const events = await conn . listEvents ();
for ( const event of events ) {
console . log ( ` ${ event . id } : ${ event . label } ` );
}
```

### [ Get Event Details](#get-event-details)

Python

Node.js

```
event = conn.get_event(event_id)
print ( f "Label: { event.label } " )
print ( f "Prompt: { event.event_prompt } " )
```

```
const event = await conn . getEvent ( eventId );
console . log ( `Label: ${ event . label } ` );
console . log ( `Prompt: ${ event . eventPrompt } ` );
```

### [ Delete Event](#delete-event)

Python

Node.js

```
conn.delete_event(event_id)
```

```
await conn . deleteEvent ( eventId );
```

## [ Prompt Engineering Tips](#prompt-engineering-tips)

### [ Be Specific About Conditions](#be-specific-about-conditions)

```
# Weak: ambiguous threshold
"Detect crowding"

# Strong: clear threshold
"Detect when more than 10 people are visible in the frame"
```

### [ Include Context](#include-context)

```
# Weak: missing context
"Detect a person running"

# Strong: includes context
"Detect a person running in the parking lot (not jogging normally)"
```

### [ Describe What "Detected" Means](#describe-what-“detected”-means)

```
# Weak: unclear criteria
"Detect suspicious activity"

# Strong: observable criteria
"Detect when someone looks into car windows repeatedly or tries door handles"
```

## [ Event-Index Pairing](#event-index-pairing)

Match your event to the right index configuration:

| Detection Type       | Recommended Index Config   |
|----------------------|----------------------------|
| Static objects       | 1 frame per scene          |
| Motion/activity      | 3-5 frames per scene       |
| Quick events         | Short intervals (2-5s)     |
| Sustained conditions | Longer intervals (10-30s)  |

## [ What You Can Build](#what-you-can-build)

## Intrusion Detection

Real-time alerts when unauthorized access is detected

## Traffic Violations

Detect red light and stop sign violations automatically

## Beep Profanity

Audio event detection to censor inappropriate language

## Copyright Detection

Detect copyrighted content in video streams

## [ Next Steps](#next-steps)

## Alerts and Callbacks

Wire events to delivery channels

## Webhooks and Reliability

Handle alerts at scale

[Text Asset](\pages\act\programmable-editing\text-asset) [Alerts and Callbacks](\pages\act\live-action\alerts-and-callbacks)

⌘ I