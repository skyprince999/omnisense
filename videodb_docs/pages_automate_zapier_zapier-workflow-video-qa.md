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
- [Detailed Steps](#detailed-steps)
    - [Step 1: Setup in Zapier](#step-1-setup-in-zapier)
    - [Step 2: Configure Zendesk](#step-2-configure-zendesk)
    - [Step 3: VideoDB Integration](#step-3-videodb-integration)
    - [Step 4: Control Flow with Delay](#step-4-control-flow-with-delay)
    - [Step 5: Check Job Status](#step-5-check-job-status)
    - [Step 6: Send Notifications to Slack](#step-6-send-notifications-to-slack)
    - [Step 7: Test and Finalize](#step-7-test-and-finalize)
- [Workflow Template](#workflow-template)

[Automate](\pages\automate\integrations-overview)

[Zapier Workflows](\pages\automate\zapier\index)

# Video Q&amp;A Support

Copy page

Automatically answer Zendesk support tickets using relevant video content via Zapier and VideoDB.

Copy page

This workflow is designed to automatically send Zendesk ticket notifications to Slack while also finding relevant information from a specific video to provide quick answers to the queries raised in the tickets.

## [ Goals](#goals)

1. Automate the notification of new Zendesk tickets
2. Retrieve relevant video clips that provide answers to the ticket queries
3. Send both the ticket information and the relevant video clips to a Slack channel for quick resolution

## [ Prerequisites](#prerequisites)

- A Zendesk account with API access
- A VideoDB account to find and manage video content
- A Slack account to receive notifications
- A Zapier account to create and manage the integration

## [ Detailed Steps](#detailed-steps)

### [ Step 1: Setup in Zapier](#step-1-setup-in-zapier)

1. Navigate to Zapier and create a new Zap
2. Select Zendesk as the trigger app with the "New Ticket" event
3. Configure Zendesk account settings using the domain, admin email, and API token from Zendesk

### [ Step 2: Configure Zendesk](#step-2-configure-zendesk)

Access the Zendesk dashboard and retrieve the API token required to connect with Zapier.

### [ Step 3: VideoDB Integration](#step-3-videodb-integration)

1. Use the "Find Video Moment" action in Zapier to connect VideoDB
2. Sign in to VideoDB using Google or GitHub and obtain the API key
3. Choose the relevant video from which answers will be retrieved based on the ticket subject and description

### [ Step 4: Control Flow with Delay](#step-4-control-flow-with-delay)

Add a "Delay by Zapier" action to wait for a set time (e.g., 3 minutes) for the VideoDB processing to complete before proceeding.

### [ Step 5: Check Job Status](#step-5-check-job-status)

Add an action to check the status of the VideoDB job using the job ID obtained from the previous step.

### [ Step 6: Send Notifications to Slack](#step-6-send-notifications-to-slack)

1. Select Slack as the action app and configure it to send a direct message or channel message
2. Customize the message with ticket subject, description, VideoDB results, and a link to the video

### [ Step 7: Test and Finalize](#step-7-test-and-finalize)

Test the workflow to ensure that the message is correctly sent to Slack with all necessary details.

## [ Workflow Template](#workflow-template)

## Video Q&amp;A Support Workflow

Answer support tickets using video content

[GenAI Video to YouTube](\pages\automate\zapier\zapier-workflow-notion-to-youtube) [MCP Server](\pages\build-with-agents\mcp-server)

⌘ I