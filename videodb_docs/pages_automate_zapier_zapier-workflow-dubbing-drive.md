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
    - [Step 1: Form Creation](#step-1-form-creation)
    - [Step 2: Trigger Setup](#step-2-trigger-setup)
    - [Step 3: Video Upload and Indexing](#step-3-video-upload-and-indexing)
    - [Step 4: Publish Workflow 1](#step-4-publish-workflow-1)
- [Workflow 2: Dubbing and Storage Process](#workflow-2-dubbing-and-storage-process)
    - [Step 1: Trigger Setup](#step-1-trigger-setup)
    - [Step 2: Dubbing Process](#step-2-dubbing-process)
    - [Step 3: Delay for Processing](#step-3-delay-for-processing)
    - [Step 4: Check Dubbing Status](#step-4-check-dubbing-status)
    - [Step 5: Google Drive Storage](#step-5-google-drive-storage)
    - [Step 6: Test and Publish Workflow 2](#step-6-test-and-publish-workflow-2)
- [Workflow Templates](#workflow-templates)

[Automate](\pages\automate\integrations-overview)

[Zapier Workflows](\pages\automate\zapier\index)

# Video Dubbing to Google Drive

Copy page

Automate video dubbing into Spanish and store in Google Drive using Zapier and VideoDB.

Copy page

This workflow automates the process of dubbing videos into Spanish and storing them in a dedicated Google Drive folder using Zapier and VideoDB. The goal is to enhance content accessibility, optimize workflow efficiency, and conserve resources, allowing for seamless management of multilingual video content.

## [ Goals](#goals)

1. Automate the process of dubbing videos into Spanish
2. Store the dubbed videos in a specified Google Drive folder
3. Optimize workflow efficiency by minimizing unnecessary triggers and conserving credits

## [ Prerequisites](#prerequisites)

- A Zapier account to create and manage workflows
- Access to VideoDB with an active API key
- A configured Google Drive account with a folder called "Dubbed Videos" for storage
- The ability to create forms via interfaces.zapier.com for video submissions
- A basic understanding of how Zapier workflows (zaps) function

## [ Workflow 1: Upload and Indexing Process](#workflow-1-upload-and-indexing-process)

### [ Step 1: Form Creation](#step-1-form-creation)

Use interfaces.zapier.com to create a video submission form. The form should capture the video name and URL, which can be a downloadable link or a YouTube link.

### [ Step 2: Trigger Setup](#step-2-trigger-setup)

1. Create a new Zap in Zapier
2. Set the trigger to be a form submission from Zapier Interfaces
3. Choose the interface and specific form created for video submissions

### [ Step 3: Video Upload and Indexing](#step-3-video-upload-and-indexing)

1. Add an action step using VideoDB to upload and index the video
2. Connect to VideoDB using your API key
3. Pass the video name and URL from the form submission
4. Use "dubvideo" as the target label to ensure specific workflow triggering
5. Test the step to verify that a job ID is returned, indicating the process is in progress

### [ Step 4: Publish Workflow 1](#step-4-publish-workflow-1)

Once verified, publish this initial workflow to make it active.

## [ Workflow 2: Dubbing and Storage Process](#workflow-2-dubbing-and-storage-process)

### [ Step 1: Trigger Setup](#step-1-trigger-setup)

1. Create a new Zap in Zapier
2. Set the trigger to "New Video Uploaded and Indexed" from VideoDB
3. Use the target label "dubvideo" to ensure this workflow is only triggered for designated tasks

### [ Step 2: Dubbing Process](#step-2-dubbing-process)

1. Add an action step for autodubbing the video using VideoDB
2. Set the language code to "ES" for Spanish
3. Test the step to receive a new job ID, indicating the dubbing process has started

### [ Step 3: Delay for Processing](#step-3-delay-for-processing)

Insert a delay action using Zapier's flow control to wait for a specified time (e.g., 5 minutes) to allow the dubbing process to complete.

### [ Step 4: Check Dubbing Status](#step-4-check-dubbing-status)

After the delay, check the job status using VideoDB's action to confirm the dubbing has finished.

### [ Step 5: Google Drive Storage](#step-5-google-drive-storage)

1. Add an action step to upload the dubbed video to Google Drive
2. Select the appropriate account and folder ("Dubbed Videos")
3. Use the downloadable URL from the completed video job for the file upload
4. Use the video name with ".mp4" as the extension for the file name

### [ Step 6: Test and Publish Workflow 2](#step-6-test-and-publish-workflow-2)

Test the entire workflow to ensure a dubbed video is correctly uploaded to Google Drive. Once complete, publish this workflow to activate it.

## [ Workflow Templates](#workflow-templates)

## Part 1: Upload and Indexing Process

Upload videos and index them in VideoDB

## Part 2: Dubbing and Storage Process

Dub videos into different languages and save to Google Drive

[Subtitle Generation](\pages\automate\zapier\zapier-workflow-subtitle-generation) [Profanity Detection to Slack](\pages\automate\zapier\zapier-workflow-profanity-detection)

⌘ I