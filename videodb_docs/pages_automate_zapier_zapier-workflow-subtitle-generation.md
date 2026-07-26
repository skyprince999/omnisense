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
- [Workflow 1: Form Submission and Upload](#workflow-1-form-submission-and-upload)
    - [Step 1: Form Creation (Zapier Interfaces)](#step-1-form-creation-zapier-interfaces)
    - [Step 2: Trigger Setup](#step-2-trigger-setup)
    - [Step 3: Upload and Index with VideoDB](#step-3-upload-and-index-with-videodb)
    - [Step 4: Publish Workflow 1](#step-4-publish-workflow-1)
- [Workflow 2: Subtitle Generation and Storage](#workflow-2-subtitle-generation-and-storage)
    - [Step 1: Trigger Setup](#step-1-trigger-setup)
    - [Step 2: Subtitle Generation](#step-2-subtitle-generation)
    - [Step 3: Google Drive Storage](#step-3-google-drive-storage)
    - [Step 4: Publish Workflow 2](#step-4-publish-workflow-2)
- [Workflow Templates](#workflow-templates)

[Automate](\pages\automate\integrations-overview)

[Zapier Workflows](\pages\automate\zapier\index)

# Subtitle Generation

Copy page

Automate subtitle generation for videos and save to Google Drive using Zapier and VideoDB.

Copy page

This workflow automates the process of generating subtitles for uploaded videos and storing the subtitled videos in a designated Google Drive folder. It improves accessibility for audiences who need captions.

## [ Goals](#goals)

1. Automate the process of generating subtitles for uploaded videos
2. Store the subtitled videos in a designated Google Drive folder
3. Improve accessibility for audiences who need captions

## [ Prerequisites](#prerequisites)

- A Zapier account to create and manage workflows
- Access to VideoDB with an active API key
- A configured Google Drive account with a folder (e.g., "Videos with Subtitles") for storing processed videos
- A Zapier Interface form to collect video name and video URL submissions
- Basic understanding of Zapier workflows (Zaps) and triggers

## [ Workflow 1: Form Submission and Upload](#workflow-1-form-submission-and-upload)

### [ Step 1: Form Creation (Zapier Interfaces)](#step-1-form-creation-zapier-interfaces)

1. Create a blank form titled *Subtitle Video*
2. Add two fields:
    - Video Name (short text, required)
    - Video URL (valid URL field, required)
3. Share the form link for submissions

### [ Step 2: Trigger Setup](#step-2-trigger-setup)

1. In Zapier, set the trigger to *Form Submission Created* from Interfaces
2. Select the subtitle video form and page

### [ Step 3: Upload and Index with VideoDB](#step-3-upload-and-index-with-videodb)

1. Add an action to upload and index the video via VideoDB
2. Authenticate using your VideoDB API key
3. Map video name and URL from the form data
4. Set a target label (e.g., `subtitle video` ) to connect with the second workflow
5. Test to confirm a Job ID is returned, indicating the task has started

### [ Step 4: Publish Workflow 1](#step-4-publish-workflow-1)

Activate the workflow so form submissions trigger video uploads automatically.

## [ Workflow 2: Subtitle Generation and Storage](#workflow-2-subtitle-generation-and-storage)

### [ Step 1: Trigger Setup](#step-1-trigger-setup)

1. Create a new Zap with trigger *New Video Uploaded Job* from VideoDB
2. Filter by target label `subtitle video` to ensure only relevant jobs trigger this workflow

### [ Step 2: Subtitle Generation](#step-2-subtitle-generation)

1. Add an action to *Generate Subtitles* using VideoDB
2. Select dynamic video ID from the trigger event
3. Configure subtitle style (e.g., *supersize* animation to enlarge the spoken word)
4. Test to confirm the output returns a stream URL, download URL, and new video ID

### [ Step 3: Google Drive Storage](#step-3-google-drive-storage)

1. Add an action to *Upload File* to Google Drive
2. Authenticate with your Google account and select the designated folder (e.g., *Videos with Subtitles* )
3. Use the downloadable URL from VideoDB as the input file
4. Set the file name dynamically from the form submission with ".mp4" extension
5. Test to confirm the subtitled video is stored in the correct folder

### [ Step 4: Publish Workflow 2](#step-4-publish-workflow-2)

Activate this workflow to automatically process and store subtitled videos.

## [ Workflow Templates](#workflow-templates)

## Part 1: Form Submission and Upload

Collect videos via form and upload to VideoDB

## Part 2: Subtitle Generation and Storage

Generate subtitles automatically and save to Google Drive

[Video Highlights to Notion](\pages\automate\zapier\zapier-workflow-video-highlights) [Video Dubbing to Google Drive](\pages\automate\zapier\zapier-workflow-dubbing-drive)

⌘ I