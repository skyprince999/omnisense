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
    - [Step 2: Spoken Content Indexing](#step-2-spoken-content-indexing)
    - [Step 3: Subtitle Generation and Overlay](#step-3-subtitle-generation-and-overlay)
    - [Step 4: Google Drive Storage](#step-4-google-drive-storage)
- [Conclusion](#conclusion)

[Automate](\pages\automate\integrations-overview)

[n8n Workflows](\pages\automate\n8n\index)

# Subtitle Generation Workflow

Copy page

Generate and embed professional subtitles in videos, then save to Google Drive using n8n and VideoDB.

Copy page

This workflow takes video URLs, uploads them to VideoDB, indexes spoken content, adds subtitle overlays directly to the video, and saves the subtitled videos to Google Drive. It creates professional subtitle overlays that are permanently embedded in the video. The workflow is useful for creating accessible video content with professional subtitle styling that works across all platforms, unlike platform-specific auto-generated subtitles.

## [ Prerequisites](#prerequisites)

1. **n8n Instance** : Running n8n automation platform (cloud or self-hosted)
2. **VideoDB API Key** : Obtain from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs)
3. **Google Drive Account** : With API access for file uploads
4. **Video URLs** : Access to video content that needs subtitles

## [ Workflow Steps](#workflow-steps)

### [ Step 1: Video Input and Upload](#step-1-video-input-and-upload)

1. Form trigger collects YouTube video URL for subtitle processing
2. Upload video content to VideoDB for processing
3. Wait for upload completion before proceeding

### [ Step 2: Spoken Content Indexing](#step-2-spoken-content-indexing)

1. Monitor upload status via HTTP request polling
2. Index spoken words from the video content
3. Generate timestamped transcript for subtitle creation

### [ Step 3: Subtitle Generation and Overlay](#step-3-subtitle-generation-and-overlay)

1. Use VideoDB subtitle operation to add subtitle overlays
2. Create professional subtitle styling embedded in video
3. Process video with precisely timed subtitle overlays

### [ Step 4: Google Drive Storage](#step-4-google-drive-storage)

1. Download subtitled video from VideoDB
2. Upload subtitled video to Google Drive folder
3. Store video with subtitles permanently embedded

## [ Conclusion](#conclusion)

This workflow creates professional subtitled videos with embedded subtitle overlays, making content accessible across all platforms while maintaining consistent subtitle styling and timing.

[Video Dubbing Workflow](\pages\automate\n8n\n8n-workflow-dubbing) [YouTube to Notion Workflow](\pages\automate\n8n\n8n-workflow-youtube-notion)

⌘ I