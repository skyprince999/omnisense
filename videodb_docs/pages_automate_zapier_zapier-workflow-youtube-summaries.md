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
- [Workflow 1: YouTube Upload to VideoDB Upload and Index](#workflow-1-youtube-upload-to-videodb-upload-and-index)
    - [Step 1: Trigger Setup (YouTube)](#step-1-trigger-setup-youtube)
    - [Step 2: Upload and Index with VideoDB](#step-2-upload-and-index-with-videodb)
    - [Step 3: Publish Workflow 1](#step-3-publish-workflow-1)
- [Workflow 2: VideoDB Done to Summarize to Notion Page](#workflow-2-videodb-done-to-summarize-to-notion-page)
    - [Step 1: Trigger Setup (VideoDB)](#step-1-trigger-setup-videodb)
    - [Step 2: Request Video Summarization](#step-2-request-video-summarization)
    - [Step 3: Wait / Poll for Completion](#step-3-wait-%2F-poll-for-completion)
    - [Step 4: Create Notion Page](#step-4-create-notion-page)
    - [Step 5: Publish Workflow 2](#step-5-publish-workflow-2)
- [Workflow Templates](#workflow-templates)

[Automate](\pages\automate\integrations-overview)

[Zapier Workflows](\pages\automate\zapier\index)

# YouTube Summaries to Notion

Copy page

Automatically summarize new YouTube videos and save to Notion using Zapier and VideoDB.

Copy page

This Zapier workflow automates the process of summarizing newly uploaded YouTube videos and saving those summaries into Notion using VideoDB. The goal is to create an end-to-end pipeline that detects channel uploads, sends videos to VideoDB for indexing, requests an automated summary, and stores the Markdown-formatted summary as a new Notion page.

## [ Goals](#goals)

1. Automatically detect new YouTube uploads on a specific channel
2. Upload and index each new video in VideoDB and tag it with a target label (e.g., `YT summary` )
3. Generate a Markdown-formatted summary of the indexed video using VideoDB
4. Create a new Notion page containing the summary and relevant metadata for easy storage and reference

## [ Prerequisites](#prerequisites)

- A Zapier account to create and manage the two workflows (zaps)
- Access to VideoDB with an active API key
- A Notion account and a parent Notion page (e.g., **YouTube video summaries** ) where new pages will be created
- The YouTube channel ID (Note: YouTube typically displays channel usernames/handles like `@channelname` instead of the actual channel ID. Use a converter tool such as [StreamWeasels YouTube Channel ID Converter](https://www.streamweasels.com/tools/youtube-channel-id-and-user-id-convertor/) to convert the username to a channel ID)
- Basic familiarity with Zapier actions (triggers, async jobs, delay/flow control) and dynamic field mapping

## [ Workflow 1: YouTube Upload to VideoDB Upload and Index](#workflow-1-youtube-upload-to-videodb-upload-and-index)

### [ Step 1: Trigger Setup (YouTube)](#step-1-trigger-setup-youtube)

1. Create a new Zap with the trigger **New Video in Channel** (YouTube)
2. Provide the correct YouTube **channel ID** . Note that YouTube displays channel usernames/handles (like `@channelname` ) instead of the actual channel ID. Use a converter tool such as [StreamWeasels YouTube Channel ID Converter](https://www.streamweasels.com/tools/youtube-channel-id-and-user-id-convertor/) to get the channel ID from the username.
3. Test the trigger to ensure Zapier can fetch a recent video from the channel

### [ Step 2: Upload and Index with VideoDB](#step-2-upload-and-index-with-videodb)

1. Add a Zapier action: **VideoDB - Upload an Index job**
2. Authenticate using your VideoDB API key (retrieve from the VideoDB console / Access Control)
3. Map fields: video title, video URL (YouTube link), and a descriptive prompt (e.g., "informative video - summarize accordingly")
4. **Set a target label** (e.g., `YT summary` ) so VideoDB knows which downstream workflow(s) to trigger when indexing completes
5. Test the step and confirm VideoDB returns a **Job ID** (indexing is asynchronous)

### [ Step 3: Publish Workflow 1](#step-3-publish-workflow-1)

Activate (publish) the zap so that every new upload on the specified channel triggers this upload/index job automatically.

## [ Workflow 2: VideoDB Done to Summarize to Notion Page](#workflow-2-videodb-done-to-summarize-to-notion-page)

### [ Step 1: Trigger Setup (VideoDB)](#step-1-trigger-setup-videodb)

1. Create a second Zap with trigger **New video uploaded &amp; indexed** from VideoDB
2. Filter by the **same target label** ( `YT summary` ) to ensure only relevant indexing jobs trigger this workflow
3. Test to obtain a sample payload (includes `video_id` , stream/download URLs, length, etc.)

### [ Step 2: Request Video Summarization](#step-2-request-video-summarization)

1. Add an action: **VideoDB - Summarize Video**
2. Use the **dynamic** `video_id` from the VideoDB trigger (do not use a static video id)
3. Provide a summarization prompt tailored for Notion, for example: "Summarize the technical content of this video. Provide the final notes in Markdown format suitable for Notion."
4. Run the step - VideoDB returns a **summary job id** because summarization is asynchronous

### [ Step 3: Wait / Poll for Completion](#step-3-wait-\-poll-for-completion)

1. Insert a Zapier **Delay** (Flow Control) - e.g., **Delay for 3 minutes** - to allow time for the async summarization job
2. After the delay, add **VideoDB - Check Job Status** and pass the summary job id (dynamic)
3. Test the check step; once complete it will return the summarized text (already formatted per the prompt)

### [ Step 4: Create Notion Page](#step-4-create-notion-page)

1. Add an action: **Notion - Create Page** under the parent page **YouTube video summaries**
2. Authenticate and grant Zapier access to that Notion page
3. Configure the page:
    - **Title:** map dynamically from the original YouTube upload (video name from the first trigger)
    - **Body/content:** use the Markdown summary returned by the VideoDB Check Job Status step (Notion supports Markdown import)
    - Optionally map metadata (video URL, video length, VideoDB job id) into properties or content for traceability
4. Test creating the page to confirm formatting and placement are correct

### [ Step 5: Publish Workflow 2](#step-5-publish-workflow-2)

Activate (publish) the zap so VideoDB completion events automatically trigger summarization and Notion page creation.

## [ Workflow Templates](#workflow-templates)

## Part 1: YouTube Upload to VideoDB Upload and Index

Detect YouTube uploads and automatically index them in VideoDB

## Part 2: VideoDB Done to Summarize to Notion Page

Generate AI summaries and save as Notion pages

[Zapier Workflows](\pages\automate\zapier) [Video Highlights to Notion](\pages\automate\zapier\zapier-workflow-video-highlights)

⌘ I