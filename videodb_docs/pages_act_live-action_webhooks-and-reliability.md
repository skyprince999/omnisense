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
- [Idempotency](#idempotency)
    - [Generate Idempotency Keys](#generate-idempotency-keys)
    - [Store Processed Keys](#store-processed-keys)
- [Respond Quickly](#respond-quickly)
- [Queue Patterns](#queue-patterns)
    - [Basic Queue Architecture](#basic-queue-architecture)
    - [Priority Queues](#priority-queues)
- [Error Handling](#error-handling)
    - [Retry Failed Processing](#retry-failed-processing)
    - [Dead Letter Queue](#dead-letter-queue)
- [Monitoring](#monitoring)
    - [Track Webhook Health](#track-webhook-health)
    - [Alert on Issues](#alert-on-issues)
- [Checklist](#checklist)
- [Next Steps](#next-steps)

[Act](\pages\act\programmable-editing\timeline-architecture)

[Live Action](\pages\act\live-action\event-detection-patterns)

# Webhooks and Reliability

Copy page

Handle webhooks at scale with idempotency, retries, and queues

Copy page

Production systems need reliable webhook handling. This guide covers idempotency, retry logic, and queue patterns.

## [ Quick Example](#quick-example)

Python

Node.js

```
from flask import Flask, request, jsonify
import hashlib

app = Flask( __name__ )
processed_events = set () # Use Redis in production

@app.route ( "/webhooks/alerts" , methods = [ "POST" ])
def handle_alert ():
payload = request.json

# Generate idempotency key
idempotency_key = hashlib.sha256(
f " { payload[ 'event_id' ] } : { payload[ 'timestamp' ] } " .encode()
).hexdigest()

# Skip if already processed
if idempotency_key in processed_events:
return jsonify({ "status" : "duplicate" }), 200

# Process the alert
process_alert(payload)

# Mark as processed
processed_events.add(idempotency_key)

return jsonify({ "status" : "ok" }), 200
```

```
import express from 'express' ;
import crypto from 'crypto' ;

const app = express ();
app . use ( express . json ());

const processedEvents = new Set (); // Use Redis in production

app . post ( "/webhooks/alerts" , ( req , res ) => {
const payload = req . body ;

// Generate idempotency key
const idempotencyKey = crypto
. createHash ( 'sha256' )
. update ( ` ${ payload . event_id } : ${ payload . timestamp } ` )
. digest ( 'hex' );

// Skip if already processed
if ( processedEvents . has ( idempotencyKey )) {
return res . json ({ status: "duplicate" });
}

// Process the alert
processAlert ( payload );

// Mark as processed
processedEvents . add ( idempotencyKey );

res . json ({ status: "ok" });
});
```

## [ Idempotency](#idempotency)

Webhooks may be delivered multiple times. Always implement idempotency.

### [ Generate Idempotency Keys](#generate-idempotency-keys)

Use a combination of unique fields:

```
# Option 1: Event ID + timestamp
key = f " { payload[ 'event_id' ] } : { payload[ 'timestamp' ] } "

# Option 2: Hash of entire payload
key = hashlib.sha256(json.dumps(payload, sort_keys = True ).encode()).hexdigest()
```

### [ Store Processed Keys](#store-processed-keys)

Python

Node.js

```
import redis

r = redis.Redis()

def is_duplicate ( key : str ) -> bool :
"""Check if we've already processed this event"""
# Set with 24h expiry
return not r.set( f "webhook: { key } " , "1" , nx = True , ex = 86400 )

@app.route ( "/webhooks/alerts" , methods = [ "POST" ])
def handle_alert ():
payload = request.json
key = generate_key(payload)

if is_duplicate(key):
return jsonify({ "status" : "duplicate" }), 200

process_alert(payload)
return jsonify({ "status" : "ok" }), 200
```

```
import Redis from 'ioredis' ;

const redis = new Redis ();

async function isDuplicate ( key ) {
// SET with NX (only if not exists) and 24h expiry
const result = await redis . set ( `webhook: ${ key } ` , '1' , 'NX' , 'EX' , 86400 );
return result === null ;
}

app . post ( "/webhooks/alerts" , async ( req , res ) => {
const payload = req . body ;
const key = generateKey ( payload );

if ( await isDuplicate ( key )) {
return res . json ({ status: "duplicate" });
}

await processAlert ( payload );
res . json ({ status: "ok" });
});
```

## [ Respond Quickly](#respond-quickly)

Return 200 immediately, then process asynchronously:

Python

Node.js

```
from celery import Celery
from flask import Flask, request, jsonify

app = Flask( __name__ )
celery = Celery( 'tasks' , broker = 'redis://localhost:6379/0' )

@celery.task
def process_alert_async ( payload ):
"""Heavy processing happens here"""
# Notify team
send_slack_notification(payload)
# Store in database
save_to_db(payload)
# Trigger downstream actions
trigger_automation(payload)

@app.route ( "/webhooks/alerts" , methods = [ "POST" ])
def handle_alert ():
payload = request.json

# Acknowledge immediately
process_alert_async.delay(payload)

return jsonify({ "status" : "queued" }), 200
```

```
import Bull from 'bull' ;

const alertQueue = new Bull ( 'alerts' , 'redis://localhost:6379' );

// Worker processes jobs asynchronously
alertQueue . process ( async ( job ) => {
const payload = job . data ;
// Heavy processing
await sendSlackNotification ( payload );
await saveToDb ( payload );
await triggerAutomation ( payload );
});

app . post ( "/webhooks/alerts" , async ( req , res ) => {
const payload = req . body ;

// Acknowledge immediately, process async
await alertQueue . add ( payload );

res . json ({ status: "queued" });
});
```

## [ Queue Patterns](#queue-patterns)

### [ Basic Queue Architecture](#basic-queue-architecture)

```
VideoDB → Webhook Endpoint → Queue → Worker → Actions
↓
Return 200 fast
```

### [ Priority Queues](#priority-queues)

Handle critical alerts first:

Python

Node.js

```
from celery import Celery

celery = Celery( 'tasks' , broker = 'redis://localhost:6379/0' )

@app.route ( "/webhooks/alerts" , methods = [ "POST" ])
def handle_alert ():
payload = request.json
label = payload.get( "label" , "" )

# High priority for safety alerts
if label in [ "fall_detected" , "intrusion_detected" , "fire_detected" ]:
process_alert_async.apply_async( args = [payload], priority = 0 )
else :
process_alert_async.apply_async( args = [payload], priority = 5 )

return jsonify({ "status" : "queued" }), 200
```

```
import Bull from 'bull' ;

const highPriorityQueue = new Bull ( 'high-priority-alerts' );
const normalQueue = new Bull ( 'normal-alerts' );

app . post ( "/webhooks/alerts" , async ( req , res ) => {
const payload = req . body ;
const label = payload . label || "" ;

// High priority for safety alerts
const safetyLabels = [ "fall_detected" , "intrusion_detected" , "fire_detected" ];

if ( safetyLabels . includes ( label )) {
await highPriorityQueue . add ( payload );
} else {
await normalQueue . add ( payload );
}

res . json ({ status: "queued" });
});
```

## [ Error Handling](#error-handling)

### [ Retry Failed Processing](#retry-failed-processing)

Python

Node.js

```
from celery import Celery
from celery.exceptions import MaxRetriesExceededError

celery = Celery( 'tasks' , broker = 'redis://localhost:6379/0' )

@celery.task ( bind = True , max_retries = 3 , default_retry_delay = 60 )
def process_alert_async ( self , payload ):
try :
# Process the alert
send_notification(payload)
save_to_db(payload)
except Exception as e:
# Retry with exponential backoff
raise self .retry( exc = e, countdown = 60 * ( 2 ** self .request.retries))
```

```
const alertQueue = new Bull ( 'alerts' , {
defaultJobOptions: {
attempts: 3 ,
backoff: {
type: 'exponential' ,
delay: 60000 // 1 minute base
}
}
});

alertQueue . process ( async ( job ) => {
// Automatic retries on failure
await sendNotification ( job . data );
await saveToDb ( job . data );
});

// Handle failed jobs
alertQueue . on ( 'failed' , ( job , err ) => {
console . error ( `Job ${ job . id } failed after ${ job . attemptsMade } attempts` );
// Send to dead letter queue or alert ops team
});
```

### [ Dead Letter Queue](#dead-letter-queue)

Handle permanently failed jobs:

Python

Node.js

```
@celery.task ( bind = True , max_retries = 3 )
def process_alert_async ( self , payload ):
try :
process(payload)
except MaxRetriesExceededError:
# Move to dead letter queue
save_to_dead_letter(payload)
alert_ops_team(payload)
except Exception as e:
raise self .retry( exc = e)
```

```
const deadLetterQueue = new Bull ( 'dead-letter' );

alertQueue . on ( 'failed' , async ( job , err ) => {
if ( job . attemptsMade >= job . opts . attempts ) {
// Move to dead letter queue
await deadLetterQueue . add ({
originalPayload: job . data ,
error: err . message ,
failedAt: new Date ()
});
}
});
```

## [ Monitoring](#monitoring)

### [ Track Webhook Health](#track-webhook-health)

```
from prometheus_client import Counter, Histogram

webhook_received = Counter(
'webhook_received_total' ,
'Total webhooks received' ,
[ 'event_label' ]
)

webhook_latency = Histogram(
'webhook_processing_seconds' ,
'Time to process webhook'
)

@app.route ( "/webhooks/alerts" , methods = [ "POST" ])
def handle_alert ():
payload = request.json

webhook_received.labels( event_label = payload.get( "label" )).inc()

with webhook_latency.time():
process_alert(payload)

return jsonify({ "status" : "ok" }), 200
```

### [ Alert on Issues](#alert-on-issues)

```
# Alert if processing takes too long
if processing_time > 5.0 :
send_ops_alert( "Webhook processing slow" )

# Alert if queue is backing up
queue_size = celery.control.inspect().active()
if queue_size > 1000 :
send_ops_alert( "Alert queue backing up" )
```

## [ Checklist](#checklist)

Before going to production:

- Idempotency keys stored in Redis/database
- Webhook returns 200 within 500ms
- Async processing with queue (Celery, Bull, etc.)
- Retry logic with exponential backoff
- Dead letter queue for failed jobs
- Monitoring and alerting
- Key expiry to prevent memory growth

## [ Next Steps](#next-steps)

## Event Detection Patterns

Create effective detection rules

## Alerts and Callbacks

Wire events to delivery channels

[Alerts and Callbacks](\pages\act\live-action\alerts-and-callbacks) [Generative Media Overview](\pages\act\generative-media)

⌘ I