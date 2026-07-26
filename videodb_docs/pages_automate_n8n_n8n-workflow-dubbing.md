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
    - [Step 1: Video Input and Upload](#step-1-video-input-and-upload)
    - [Step 2: Video Processing](#step-2-video-processing)
    - [Step 3: Video Dubbing](#step-3-video-dubbing)
    - [Step 4: Google Drive Storage](#step-4-google-drive-storage)
- [Conclusion](#conclusion)

[Automate](\pages\automate\integrations-overview)

[n8n Workflows](\pages\automate\n8n\index)

# Video Dubbing Workflow

Copy page

Automatically dub videos into different languages and save to Google Drive using n8n and VideoDB.

Copy page

This workflow takes video URLs, uploads them to VideoDB, dubs them into different languages, and saves the dubbed videos to Google Drive. It enables automatic video localization for global content distribution. The workflow is useful for content creators who need to create multilingual versions of their videos for international audiences without manual dubbing processes.

## [ Prerequisites](#prerequisites)

1. **n8n Instance** : Running n8n automation platform (cloud or self-hosted)
2. **VideoDB API Key** : Obtain from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs)
3. **Google Drive Account** : With API access for file uploads
4. **Video URLs** : Access to video content that needs dubbing

## [ Workflow Steps](#workflow-steps)

### [ Step 1: Video Input and Upload](#step-1-video-input-and-upload)

1. Form trigger collects YouTube video URL for dubbing
2. Upload video content to VideoDB for processing
3. Wait for upload completion before proceeding

### [ Step 2: Video Processing](#step-2-video-processing)

1. Monitor upload status via HTTP request polling
2. Verify video upload is complete
3. Prepare video for dubbing operations

### [ Step 3: Video Dubbing](#step-3-video-dubbing)

1. Use VideoDB dubbing operation to create dubbed version
2. Process video with target language dubbing
3. Monitor dubbing completion status

### [ Step 4: Google Drive Storage](#step-4-google-drive-storage)

1. Download dubbed video from VideoDB
2. Upload dubbed video to Google Drive folder
3. Store video with appropriate naming for language identification

## [ Conclusion](#conclusion)

This workflow automates video dubbing and storage, enabling easy creation of multilingual video content that can be distributed through Google Drive or integrated into other workflows.

[Meeting Summaries Workflow](\pages\automate\n8n\n8n-workflow-meeting-summaries) [Subtitle Generation Workflow](\pages\automate\n8n\n8n-workflow-subtitle-generation)

⌘ I