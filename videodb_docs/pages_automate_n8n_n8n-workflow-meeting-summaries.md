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
    - [Step 3: AI Summarization](#step-3-ai-summarization)
    - [Step 4: Documentation and Distribution](#step-4-documentation-and-distribution)
- [Conclusion](#conclusion)

[Automate](\pages\automate\integrations-overview)

[n8n Workflows](\pages\automate\n8n\index)

# Meeting Summaries Workflow

Copy page

Convert recorded meetings into structured summaries with action items and key decisions using n8n and VideoDB.

Copy page

This workflow converts recorded meetings into structured summaries with action items and key decisions. It serves as a universal meeting processor for general business meetings and distributes summaries to both Coda and Slack. The workflow ensures consistent meeting documentation and team notification for any type of business meeting.

## [ Prerequisites](#prerequisites)

1. **n8n Instance** : Running n8n automation platform (cloud or self-hosted)
2. **VideoDB API Key** : Obtain from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs)
3. **Meeting Recording** : Access to meeting recording (any platform with recording capability)
4. **Coda Workspace** : For meeting documentation storage
5. **Slack Workspace** : For team notifications

## [ Workflow Steps](#workflow-steps)

### [ Step 1: Meeting Recording](#step-1-meeting-recording)

1. Process recorded meeting files or live meeting recordings
2. Initiate VideoDB processing for the meeting content
3. Wait for recording completion before analysis

### [ Step 2: Video Processing](#step-2-video-processing)

1. Index spoken words and generate comprehensive transcript
2. Create timestamped transcript for reference
3. Prepare content for AI summarization

### [ Step 3: AI Summarization](#step-3-ai-summarization)

1. Extract meeting title and purpose
2. Identify key discussion points and decisions made
3. Extract action items with ownership assignments and due dates
4. Structure information into consistent format

### [ Step 4: Documentation and Distribution](#step-4-documentation-and-distribution)

1. Create new entry in Coda project database with structured fields:
    - Date and meeting metadata
    - Executive summary
    - Action points with assignments
    - Decision log
2. Send formatted meeting summary to Slack with action item notifications

## [ Conclusion](#conclusion)

This workflow creates a complete meeting documentation system that stores structured summaries in Coda while keeping teams informed through Slack notifications.

[Meeting Intelligence Workflow](\pages\automate\n8n\n8n-workflow-meeting-intelligence) [Video Dubbing Workflow](\pages\automate\n8n\n8n-workflow-dubbing)

⌘ I