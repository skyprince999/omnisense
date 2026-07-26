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
    - [Step 1: Content Discovery](#step-1-content-discovery)
    - [Step 2: Video Upload and Processing](#step-2-video-upload-and-processing)
    - [Step 3: Content Analysis](#step-3-content-analysis)
    - [Step 4: Notion Integration](#step-4-notion-integration)
- [Conclusion](#conclusion)

[Automate](\pages\automate\integrations-overview)

[n8n Workflows](\pages\automate\n8n\index)

# YouTube to Notion Workflow

Copy page

Monitor YouTube channels for new content and automatically create summaries in Notion using n8n and VideoDB.

Copy page

This workflow monitors YouTube channels for new content and automatically creates summaries in Notion. It builds a searchable knowledge base of video content without requiring manual video watching. The workflow helps teams track multiple content sources and extract insights from educational or industry content automatically.

## [ Prerequisites](#prerequisites)

1. **n8n Instance** : Running n8n automation platform (cloud or self-hosted)
2. **VideoDB API Key** : Obtain from [VideoDB Console](https://console.videodb.io/auth?utm_source=docs_videodb_io&utm_medium=docs_link&utm_campaign=console_auth&utm_content=docs_link&id=docs)
3. **Notion Workspace** : With page/database access for content storage
4. **YouTube Channels** : Specific channels to monitor via RSS feed
5. **RSS Configuration** : n8n RSS trigger setup for channel monitoring

## [ Workflow Steps](#workflow-steps)

### [ Step 1: Content Discovery](#step-1-content-discovery)

1. RSS feed trigger monitors specified YouTube channels for new uploads
2. Capture video metadata (title, description, author, publication date, URL)
3. Activate immediately when new video is published

### [ Step 2: Video Upload and Processing](#step-2-video-upload-and-processing)

1. Upload video content to VideoDB for processing
2. Monitor upload and indexing completion status
3. Index spoken words for transcript extraction

### [ Step 3: Content Analysis](#step-3-content-analysis)

1. Generate full transcript of video content with timestamps
2. Apply AI summarization to extract:
    - Key topics and themes discussed
    - Important quotes and insights
    - Technical concepts explained
    - Action items or recommendations mentioned

### [ Step 4: Notion Integration](#step-4-notion-integration)

1. Create new Notion page with structured video summary
2. Include comprehensive documentation:
    - Video title and source channel information
    - Publication date and metadata
    - Detailed summary with key insights
    - Direct link to original video
3. Add entry to Notion database with appropriate tags for searching

## [ Conclusion](#conclusion)

This workflow automates video content monitoring and creates a searchable knowledge repository in Notion, enabling teams to stay informed about relevant content without manual video consumption.

[Subtitle Generation Workflow](\pages\automate\n8n\n8n-workflow-subtitle-generation) [HubSpot CRM Sync Workflow](\pages\automate\n8n\n8n-workflow-hubspot-crm)

⌘ I