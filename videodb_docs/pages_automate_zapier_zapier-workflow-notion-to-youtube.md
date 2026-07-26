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
    - [Zapier Workflows](\pages\automate\zapier)
    - [YouTube Summaries to Notion](\pages\automate\zapier\zapier-workflow-youtube-summaries)
    - [Video Highlights to Notion](\pages\automate\zapier\zapier-workflow-video-highlights)
    - [Subtitle Generation](\pages\automate\zapier\zapier-workflow-subtitle-generation)
    - [Video Dubbing to Google Drive](\pages\automate\zapier\zapier-workflow-dubbing-drive)
    - [Profanity Detection to Slack](\pages\automate\zapier\zapier-workflow-profanity-detection)
    - [GenAI Video to YouTube](\pages\automate\zapier\zapier-workflow-notion-to-youtube)
    - [Video Q&amp;A Support](\pages\automate\zapier\zapier-workflow-video-qa)

### Open Source Frameworks

- [MCP Server](\pages\build-with-agents\mcp-server)
- [LlamaIndex Retriever](\pages\community\open-source\llamaindex-retriever)
- Director Framework

## On this page

- [Goals](#goals)
- [Prerequisites](#prerequisites)
- [Workflow 1: Generate AI Video](#workflow-1-generate-ai-video)
    - [Step 1: Notion Database Setup](#step-1-notion-database-setup)
    - [Step 2: Trigger Setup in Zapier](#step-2-trigger-setup-in-zapier)
    - [Step 3: Generate Video with VideoDB](#step-3-generate-video-with-videodb)
    - [Step 4: Publish Workflow 1](#step-4-publish-workflow-1)
- [Workflow 2: Upload Generated Video to YouTube](#workflow-2-upload-generated-video-to-youtube)
    - [Step 1: Trigger Setup](#step-1-trigger-setup)
    - [Step 2: YouTube Upload Configuration](#step-2-youtube-upload-configuration)
    - [Step 3: Test and Publish Workflow 2](#step-3-test-and-publish-workflow-2)
- [Workflow Templates](#workflow-templates)

[Automate](\pages\automate\integrations-overview)

[Zapier Workflows](\pages\automate\zapier\index)

# GenAI Video to YouTube

Copy page

Automate AI-generated video creation from Notion ideas and publish directly to YouTube using Zapier and VideoDB.

Copy page

This workflow explains how to automate the creation and publishing of AI-generated (GenAI) videos to YouTube using VideoDB. The goal is to enable a fully automated YouTube channel where video ideas added in Notion automatically result in generated videos uploaded to YouTube.

## [ Goals](#goals)

1. Automate the generation of AI-based videos from Notion database entries
2. Upload generated videos directly to a connected YouTube channel
3. Use target labels to route tasks efficiently and avoid duplicate triggers
4. Enable creators to scale video publishing with minimal manual effort

## [ Prerequisites](#prerequisites)

- A Zapier account to create and manage workflows
- Access to VideoDB with an active API key
- A Notion account with a database for storing video ideas and descriptions
- A YouTube account connected to Zapier for video uploads
- Basic familiarity with Zapier workflows and triggers

## [ Workflow 1: Generate AI Video](#workflow-1-generate-ai-video)

### [ Step 1: Notion Database Setup](#step-1-notion-database-setup)

Create a new database in Notion called *GenAI Video Ideas* . Add fields such as *Name* (video title) and *Description* (prompt for video content).

### [ Step 2: Trigger Setup in Zapier](#step-2-trigger-setup-in-zapier)

1. Create a new Zap
2. Set the trigger to *New Database Item* in Notion
3. Select the *GenAI Video Ideas* database

### [ Step 3: Generate Video with VideoDB](#step-3-generate-video-with-videodb)

1. Add an action using VideoDB - *Generate Video*
2. Authenticate with API key from the VideoDB dashboard
3. Pass in the Notion fields ( *Name* and *Description* ) as the prompt
4. Configure settings (e.g., 30 seconds duration, vertical aspect ratio, with subtitles)
5. Assign a **target label** (e.g., `YT upload` ) to ensure the correct next workflow is triggered
6. Test and verify that a Job ID (token) is returned

### [ Step 4: Publish Workflow 1](#step-4-publish-workflow-1)

Once tested, activate this workflow to automatically start video generation.

## [ Workflow 2: Upload Generated Video to YouTube](#workflow-2-upload-generated-video-to-youtube)

### [ Step 1: Trigger Setup](#step-1-trigger-setup)

1. Create another Zap
2. Set the trigger to *AI Generated Video Created* in VideoDB
3. Use the same target label ( `YT upload` ) so only matching jobs trigger this workflow

### [ Step 2: YouTube Upload Configuration](#step-2-youtube-upload-configuration)

1. Add an action using YouTube - *Upload Video*
2. Connect your YouTube account to Zapier
3. Map video fields:
    - Title: from Notion *Name*
    - Description: e.g., *"GenAI Video created by VideoDB"*
    - Video File: use the *Download URL* from VideoDB output
4. Optional settings: leave thumbnail empty, mark video as *Public* , and set "not made for kids"

### [ Step 3: Test and Publish Workflow 2](#step-3-test-and-publish-workflow-2)

Run a test to verify upload works. Publish the workflow to activate automatic uploads.

## [ Workflow Templates](#workflow-templates)

## Part 1: Generate AI Video

Generate AI videos from Notion ideas and prompts

## Part 2: Upload Generated Video to YouTube

Publish generated videos directly to YouTube

[Profanity Detection to Slack](\pages\automate\zapier\zapier-workflow-profanity-detection) [Video Q&amp;A Support](\pages\automate\zapier\zapier-workflow-video-qa)

⌘ I