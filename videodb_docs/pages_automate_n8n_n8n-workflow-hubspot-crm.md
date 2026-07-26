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
    - [Step 1: Sales Call Recording](#step-1-sales-call-recording)
    - [Step 2: Video Processing](#step-2-video-processing)
    - [Step 3: Deal Intelligence Extraction](#step-3-deal-intelligence-extraction)
    - [Step 4: HubSpot CRM Integration](#step-4-hubspot-crm-integration)
- [Conclusion](#conclusion)

[Automate](\pages\automate\integrations-overview)

[n8n Workflows](\pages\automate\n8n\index)

# HubSpot CRM Sync Workflow

Copy page

Capture sales conversations and sync deal information directly to HubSpot CRM using n8n and VideoDB.

Copy page

This workflow captures sales conversations and syncs deal information directly to HubSpot CRM. It eliminates manual data entry by extracting key deal details from sales calls and updating CRM records automatically. The workflow ensures consistent CRM data entry and prevents missed sales opportunities through automated deal tracking.

## [ Prerequisites](#prerequisites)

1. **n8n Instance** : Running n8n automation platform (cloud or self-hosted)
2. **VideoDB API Key** : Obtain from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs)
3. **HubSpot CRM** : With API access for deal and contact management
4. **Meeting Recording** : Capability for sales call recording
5. **HubSpot Pipeline** : Configured deal pipeline with appropriate stages

## [ Workflow Steps](#workflow-steps)

### [ Step 1: Sales Call Recording](#step-1-sales-call-recording)

1. Record sales conversations automatically
2. Ensure complete call capture before processing
3. Verify audio quality for accurate transcript generation

### [ Step 2: Video Processing](#step-2-video-processing)

1. Index spoken words from sales call audio
2. Generate detailed transcript of the conversation
3. Prepare content for deal analysis

### [ Step 3: Deal Intelligence Extraction](#step-3-deal-intelligence-extraction)

1. Extract company/prospect name for deal identification
2. Assess current deal stage based on conversation content
3. Identify deal value and monetary discussions
4. Extract next steps and follow-up requirements
5. Categorize deals into appropriate HubSpot pipeline stages

### [ Step 4: HubSpot CRM Integration](#step-4-hubspot-crm-integration)

1. Create new deal records or update existing ones
2. Populate CRM fields with:
    - Deal name and estimated value
    - Current pipeline stage
    - Meeting summary and discussion points
    - Next steps and follow-up tasks
3. Log meeting as activity in deal timeline

## [ Conclusion](#conclusion)

This workflow maintains accurate, up-to-date CRM data by automatically capturing and structuring sales conversation details in HubSpot, supporting consistent deal tracking and sales process management.

[YouTube to Notion Workflow](\pages\automate\n8n\n8n-workflow-youtube-notion) [Interview Evaluation Workflow](\pages\automate\n8n\n8n-workflow-interview-evaluation)

⌘ I