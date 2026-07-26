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
- [Workflow 1: Upload and Indexing Process](#workflow-1-upload-and-indexing-process)
    - [Step 1: Trigger Setup](#step-1-trigger-setup)
    - [Step 2: Video Upload and Indexing](#step-2-video-upload-and-indexing)
    - [Step 3: Publish Workflow 1](#step-3-publish-workflow-1)
- [Workflow 2: Highlight Clips and Summaries](#workflow-2-highlight-clips-and-summaries)
    - [Step 1: Trigger Setup](#step-1-trigger-setup-2)
    - [Step 2: Highlight Clip Generation](#step-2-highlight-clip-generation)
    - [Step 3: Summary Generation](#step-3-summary-generation)
    - [Step 4: Delay for Processing](#step-4-delay-for-processing)
    - [Step 5: Job Status Checks](#step-5-job-status-checks)
    - [Step 6: Notion Storage](#step-6-notion-storage)
    - [Step 7: Test and Publish Workflow 2](#step-7-test-and-publish-workflow-2)
- [Workflow Templates](#workflow-templates)

[Automate](\pages\automate\integrations-overview)

[Zapier Workflows](\pages\automate\zapier\index)

# Video Highlights to Notion

Copy page

Automate video highlight clip extraction and summary generation, stored in Notion using Zapier and VideoDB.

Copy page

This Zap automates the generation of video highlight clips and summaries from YouTube videos using VideoDB, with the results automatically stored in Notion. The goal is to simplify knowledge capture, optimize workflow efficiency, and create a system that generates insights with minimal manual effort.

## [ Goals](#goals)

1. Automate the extraction of highlight clips from YouTube videos
2. Generate concise, insightful summaries for each video
3. Store both highlights and summaries in a designated Notion page
4. Optimize efficiency by leveraging asynchronous processing and targeted workflow triggers

## [ Prerequisites](#prerequisites)

- A Zapier account to create and manage workflows
- Access to VideoDB with an active API key
- A configured YouTube playlist (e.g., "Informative Videos and Lectures")
- A Notion account with a parent page prepared for storing video highlights and summaries
- Basic understanding of how Zapier workflows (Zaps) function

## [ Workflow 1: Upload and Indexing Process](#workflow-1-upload-and-indexing-process)

### [ Step 1: Trigger Setup](#step-1-trigger-setup)

1. Create a new Zap in Zapier
2. Set the trigger to *New Video in Playlist* (YouTube)
3. Select the playlist (e.g., "Informative Videos and Lectures")

### [ Step 2: Video Upload and Indexing](#step-2-video-upload-and-indexing)

1. Add an action step using VideoDB to upload and index the video
2. Connect to VideoDB using the API key
3. Pass the video title and YouTube URL
4. Set a **target label** (e.g., `YT highlights` ) to direct the workflow
5. Confirm that a **Job ID** is returned as a token for asynchronous processing

### [ Step 3: Publish Workflow 1](#step-3-publish-workflow-1)

Once verified, publish this workflow to make it active.

## [ Workflow 2: Highlight Clips and Summaries](#workflow-2-highlight-clips-and-summaries)

### [ Step 1: Trigger Setup](#step-1-trigger-setup-2)

1. Create a new Zap in Zapier
2. Set the trigger to *Upload Job Completed* from VideoDB
3. Filter by the target label ( `YT highlights` )

### [ Step 2: Highlight Clip Generation](#step-2-highlight-clip-generation)

1. Add an action to generate highlight clips using VideoDB
2. Use prompts such as *"Extract interesting and insightful information"*
3. Select dynamic video ID from the trigger
4. Configure clip aspect ratio and subtitles (optional)
5. Note: this action returns a new **asynchronous Job ID**

### [ Step 3: Summary Generation](#step-3-summary-generation)

1. Add another action to summarize the video with VideoDB
2. Prompt: *"Create Notion markdown notes capturing key insights"*
3. Use the same video ID dynamically
4. Another asynchronous Job ID will be returned

### [ Step 4: Delay for Processing](#step-4-delay-for-processing)

Insert a Zapier delay (e.g., 5-6 minutes) to allow highlight and summary jobs to complete.

### [ Step 5: Job Status Checks](#step-5-job-status-checks)

1. Add steps to check the status of both highlight and summary jobs
2. Verify the results are available (player link for highlights, markdown text for summary)

### [ Step 6: Notion Storage](#step-6-notion-storage)

1. Add an action to create a new Notion page under the parent "Playlist Highlights" page
2. Use the video title as the page title
3. Insert the summary text first
4. Add a "Highlights" section, including the **VideoDB Player URL** for generated highlight clips

### [ Step 7: Test and Publish Workflow 2](#step-7-test-and-publish-workflow-2)

Test the full process end-to-end. Once successful, publish this workflow.

## [ Workflow Templates](#workflow-templates)

## Part 1: Upload and Indexing Process

Upload videos and index them in VideoDB

## Part 2: Highlight Clips and Summaries

Extract highlights and create summaries in Notion

[YouTube Summaries to Notion](\pages\automate\zapier\zapier-workflow-youtube-summaries) [Subtitle Generation](\pages\automate\zapier\zapier-workflow-subtitle-generation)

⌘ I