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
- [Workflow 1: Upload and Index Video](#workflow-1-upload-and-index-video)
    - [Step 1: Form Creation (Zapier Interfaces)](#step-1-form-creation-zapier-interfaces)
    - [Step 2: Trigger Setup](#step-2-trigger-setup)
    - [Step 3: Upload and Index with VideoDB](#step-3-upload-and-index-with-videodb)
    - [Step 4: Publish Workflow 1](#step-4-publish-workflow-1)
- [Workflow 2: Profanity Detection and Slack Notification](#workflow-2-profanity-detection-and-slack-notification)
    - [Step 1: Trigger Setup](#step-1-trigger-setup)
    - [Step 2: Find Video Moment (Profanity Check)](#step-2-find-video-moment-profanity-check)
    - [Step 3: Delay for Processing](#step-3-delay-for-processing)
    - [Step 4: Check Job Status](#step-4-check-job-status)
    - [Step 5: Slack Notification](#step-5-slack-notification)
    - [Step 6: Publish Workflow 2](#step-6-publish-workflow-2)
- [Workflow Templates](#workflow-templates)

[Automate](\pages\automate\integrations-overview)

[Zapier Workflows](\pages\automate\zapier\index)

# Profanity Detection to Slack

Copy page

Detect profanity in uploaded videos and send alerts to Slack using Zapier and VideoDB.

Copy page

This automation is split into two workflows: the first handles video upload and indexing, and the second checks for profanity and sends the results via Slack DM. This design ensures longer-running indexing tasks complete properly while still delivering actionable insights.

## [ Goals](#goals)

1. Automate detection of profanity or vulgar language in uploaded videos
2. Split the workflow into two parts to handle longer processing times without Zapier timeouts
3. Send detected profanity results and timestamps directly to Slack for review
4. Use target labels to ensure only the intended second workflow is triggered

## [ Prerequisites](#prerequisites)

- A Zapier account to manage and run workflows
- Access to VideoDB with an active API key
- A Slack workspace with permissions to send direct messages or channel messages
- A Zapier Interface form to collect video name and URL submissions
- Basic understanding of asynchronous job handling in Zapier

## [ Workflow 1: Upload and Index Video](#workflow-1-upload-and-index-video)

### [ Step 1: Form Creation (Zapier Interfaces)](#step-1-form-creation-zapier-interfaces)

Build a form with fields for *Video Name* and *Video URL* . Example: Enter a video title and a YouTube link.

### [ Step 2: Trigger Setup](#step-2-trigger-setup)

1. Set trigger to *Form Submission Created* (Zapier Interfaces)
2. Select the created form and page as the source

### [ Step 3: Upload and Index with VideoDB](#step-3-upload-and-index-with-videodb)

1. Add an action - VideoDB - *Upload and Index Video*
2. Authenticate using your VideoDB API key
3. Map fields: Video Name and URL from form submission
4. Set **prompt** : *Check for any profanity or vulgar content*
5. Assign a **target label** (e.g., `Profanity Check` ) to connect with the second workflow
6. Test - confirm Job ID is returned (asynchronous task)

### [ Step 4: Publish Workflow 1](#step-4-publish-workflow-1)

Activate the workflow so all new form submissions trigger video uploads automatically.

## [ Workflow 2: Profanity Detection and Slack Notification](#workflow-2-profanity-detection-and-slack-notification)

### [ Step 1: Trigger Setup](#step-1-trigger-setup)

1. Trigger: *New Video Uploaded Job Completed* (VideoDB)
2. Filter by target label `Profanity Check`

### [ Step 2: Find Video Moment (Profanity Check)](#step-2-find-video-moment-profanity-check)

1. Action: VideoDB - *Find Video Moment*
2. Use dynamic video ID from the trigger
3. Prompt: *Detect profanity or vulgar content*
4. Content type: *Multimodal* (spoken + visual)
5. This action returns a new Job ID for processing

### [ Step 3: Delay for Processing](#step-3-delay-for-processing)

Insert a delay (e.g., 3 minutes) to allow VideoDB to finish analyzing.

### [ Step 4: Check Job Status](#step-4-check-job-status)

1. Action: VideoDB - *Check Job Status*
2. Input the Job ID from the "Find Video Moment" step
3. Retrieve results: detected profanity, timestamps, and URLs

### [ Step 5: Slack Notification](#step-5-slack-notification)

1. Action: Slack - *Send Channel or DM Message*
2. Configure message format:
    - Video Name
    - Player/Download URL
    - Profanity results (text + timestamps)
3. Customize bot name (e.g., *Profanity Checker* )
4. Test - confirm profanity results are delivered in Slack

### [ Step 6: Publish Workflow 2](#step-6-publish-workflow-2)

Activate the workflow to automatically run profanity checks and push results to Slack.

## [ Workflow Templates](#workflow-templates)

## Part 1: Upload and Index Video

Upload videos and index them in VideoDB

## Part 2: Profanity Detection and Slack Notification

Detect profanity and send real-time alerts to Slack

[Video Dubbing to Google Drive](\pages\automate\zapier\zapier-workflow-dubbing-drive) [GenAI Video to YouTube](\pages\automate\zapier\zapier-workflow-notion-to-youtube)

⌘ I