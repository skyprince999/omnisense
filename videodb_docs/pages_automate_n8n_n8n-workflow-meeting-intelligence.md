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
    - [n8n Workflows](\pages\automate\n8n)
    - [Meeting Intelligence Workflow](\pages\automate\n8n\n8n-workflow-meeting-intelligence)
    - [Meeting Summaries Workflow](\pages\automate\n8n\n8n-workflow-meeting-summaries)
    - [Video Dubbing Workflow](\pages\automate\n8n\n8n-workflow-dubbing)
    - [Subtitle Generation Workflow](\pages\automate\n8n\n8n-workflow-subtitle-generation)
    - [YouTube to Notion Workflow](\pages\automate\n8n\n8n-workflow-youtube-notion)
    - [HubSpot CRM Sync Workflow](\pages\automate\n8n\n8n-workflow-hubspot-crm)
    - [Interview Evaluation Workflow](\pages\automate\n8n\n8n-workflow-interview-evaluation)
- Zapier Workflows

### Open Source Frameworks

- [MCP Server](\pages\build-with-agents\mcp-server)
- [LlamaIndex Retriever](\pages\community\open-source\llamaindex-retriever)
- Director Framework

## On this page

- [Prerequisites](#prerequisites)
- [Workflow Steps](#workflow-steps)
    - [Step 1: Meeting Recording](#step-1-meeting-recording)
    - [Step 2: Video Processing](#step-2-video-processing)
    - [Step 3: AI Analysis with Branching](#step-3-ai-analysis-with-branching)
    - [Step 4: Multi-Platform Distribution](#step-4-multi-platform-distribution)
- [Conclusion](#conclusion)

[Automate](\pages\automate\integrations-overview)

[n8n Workflows](\pages\automate\n8n\index)

# Meeting Intelligence Workflow

Copy page

Automate the complete meeting lifecycle from recording to analysis and distribution with n8n and VideoDB.

Copy page

This workflow automates the complete meeting lifecycle from recording to analysis and distribution. It processes different meeting types (Sync, Planning, Interview, Sales) and distributes insights to Slack, Coda, and HubSpot based on the meeting context. The workflow handles different meeting types with intelligent branching instead of requiring separate workflows for each type.

## [ Prerequisites](#prerequisites)

1. **n8n Instance** : Running n8n automation platform (cloud or self-hosted)
2. **VideoDB API Key** : Obtain from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs)
3. **Meeting Platform** : Platform with bot recording support (Zoom, Teams, Google Meet)
4. **Slack Workspace** : With bot permissions for notifications
5. **Coda Workspace** : With API token for meeting documentation
6. **HubSpot Account** : With API key for sales meeting integration

## [ Workflow Steps](#workflow-steps)

### [ Step 1: Meeting Recording](#step-1-meeting-recording)

1. Form trigger collects meeting URL and meeting type (Sync/Planning/Interview/Sales)
2. VideoDB joins the meeting and records the session
3. Wait for meeting completion before processing

### [ Step 2: Video Processing](#step-2-video-processing)

1. Index spoken words from the recorded meeting
2. Generate transcript with speaker identification and mapping
3. Process video content for analysis readiness

### [ Step 3: AI Analysis with Branching](#step-3-ai-analysis-with-branching)

1. Switch workflow based on meeting type selection
2. Apply custom AI prompts for each meeting type:
    - **Planning** : Extract strategic outcomes, decisions, and action items
    - **Interview** : Generate candidate evaluation with recommendation
    - **Sales** : Identify deal details, stage, amount, and next steps
    - **Sync** : Create summaries with follow-ups and task assignments

### [ Step 4: Multi-Platform Distribution](#step-4-multi-platform-distribution)

1. Send formatted updates to Slack channels
2. Update Coda databases with meeting insights
3. For sales meetings: Create or update HubSpot deal records
4. Route data to appropriate platforms based on meeting type

## [ Conclusion](#conclusion)

This workflow consolidates multiple meeting types into one automated system, ensuring consistent documentation and appropriate distribution across your business tools.

[n8n Workflows](\pages\automate\n8n) [Meeting Summaries Workflow](\pages\automate\n8n\n8n-workflow-meeting-summaries)

⌘ I