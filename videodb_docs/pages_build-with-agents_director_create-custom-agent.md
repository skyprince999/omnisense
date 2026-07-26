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

### Open Source Frameworks

- [MCP Server](\pages\build-with-agents\mcp-server)
- [LlamaIndex Retriever](\pages\community\open-source\llamaindex-retriever)
- Director Framework
    - [Director Framework](\pages\build-with-agents\director)
    - [Setup Director](\pages\build-with-agents\director\setup-director)
    - [Create Custom Agent](\pages\build-with-agents\director\create-custom-agent)

## On this page

- [Understanding the Architecture](#understanding-the-architecture)
    - [System Overview](#system-overview)
    - [Understanding the Director Framework](#understanding-the-director-framework)
    - [Reasoning Engine](#reasoning-engine)
    - [Agents](#agents)
    - [Tools](#tools)
    - [Session Management](#session-management)
    - [The Reasoning Engine in Detail](#the-reasoning-engine-in-detail)
    - [Bringing It All Together](#bringing-it-all-together)
- [Planning Phase](#planning-phase)
- [Pre-Development Checklist](#pre-development-checklist)
    - [1. Purpose](#1-purpose)
    - [2. Background Check](#2-background-check)
    - [3. Agent architecture](#3-agent-architecture)
    - [4. Session Management](#4-session-management)
    - [5. Error Handling](#5-error-handling)
- [Best Practices](#best-practices)
- [Further Resources and Next Steps](#further-resources-and-next-steps)

[Open Source Frameworks](\pages\build-with-agents\mcp-server)

[Director Framework](\pages\build-with-agents\director\index)

# Create Custom Agent

Copy page

Learn how to design, develop, and integrate custom agents into the Director framework with best practices for architecture, communication, and error handling.

Copy page

This playbook will guide you through the process of creating your own agents within the Director framework. **You'll learn:**

- How to plan and structure an effective agent
- Best practices for development and integration
- Techniques for handling user communication and errors
- Ways to leverage Director's powerful video processing capabilities

## [ Understanding the Architecture](#understanding-the-architecture)

Before diving into agent creation, let's understand how Director works as a system. Director follows a modular architecture that enables seamless interaction between users and AI-powered video processing capabilities.

### [ System Overview](#system-overview)

Director's architecture is designed around three core principles:

1. **Modularity** : Each component has a specific responsibility and can be developed or modified independently
2. **Scalability** : The system can handle multiple requests and complex video operations efficiently
3. **Extensibility** : New agents and tools can be easily added to expand functionality

Looking at the system architecture diagram below, you can see how these principles come together:

Director system architecture showing modularity, scalability, and extensibility principles

<!-- image -->

### [ Understanding the Director Framework](#understanding-the-director-framework)

Director consists of several key components working together:

#### [ Reasoning Engine](#reasoning-engine)

The brain of the system that interprets natural language commands, coordinates multiple agents, maintains conversation context, and manages workflows and decision-making.

Reasoning engine showing how it interprets commands, coordinates agents, and manages workflows

<!-- image -->

#### [ Agents](#agents)

Specialized workers that handle specific tasks. Agents collaborate to complete complex video operations.

## SearchAgent

Finds specific content within videos using semantic search

## ThumbnailAgent

Generates preview images and thumbnails

## UploadAgent

Handles media uploads to VideoDB

## View All Agents

Explore the complete collection of built-in agents in the repository

#### [ Tools](#tools)

Reusable functions that agents can leverage to perform their tasks:

## VideoDB Tool

Core video database operations and queries

## AI Model Integrations

OpenAI, Anthropic, and other LLM providers

## External Connections

Slack, Composio, ElevenLabs, and more

#### [ Session Management](#session-management)

Handles state and context across interactions, ensuring consistent conversation flow and data persistence.

### [ The Reasoning Engine in Detail](#the-reasoning-engine-in-detail)

The Reasoning Engine is the orchestrator of all agent activities. It performs four critical functions:

## Processes User Input

Understands natural language requests, maintains conversation history and context, and determines required actions and sequence

## Orchestrates Agents

Selects appropriate agents from the pool, coordinates multiple agents for complex tasks, and manages dependencies between operations

## Handles Communication

Provides real-time progress updates, manages error scenarios, and returns formatted responses to the user

## Maintains State

Tracks ongoing operations, manages session data, and ensures context persistence across interactions

### [ Bringing It All Together](#bringing-it-all-together)

The architecture enables powerful workflows like:

- A user requests a `video summary` through the chat interface
- The Flask server processes this request and routes it to the Reasoning Engine
- The Reasoning Engine coordinates multiple agents to analyze and process the video
- Real-time updates flow back through WebSocket connections
- The final result is presented in the video player

This architectural foundation is what makes Director so powerful. When you create a new agent, it becomes part of this ecosystem, leveraging all these capabilities to perform its tasks efficiently. With the fundamentals covered, **let's start building!**

## [ Planning Phase](#planning-phase)

The success of an agent heavily depends on thorough planning and requirements gathering. Before writing any code:

1. **Question Everything**

- Compile a comprehensive list of questions across all aspects
- Include edge cases and potential future requirements
- Consider integration points with other agents/systems

1. **Categorize Requirements**

```
MUST-HAVE (v1)
- Core functionality requirements
- Essential error handling
- Basic user feedback

SHOULD-HAVE (v2)
- Enhanced features
- Performance optimizations
- Additional provider support

NICE-TO-HAVE (v3)
- Advanced customization
- Extra integration points
- Optional enhancements
```

1. **Define Constraints**

```
TECHNICAL_LIMITS = {
"max_input_length" : "Clear limits" ,
"rate_limits" : "API constraints" ,
"storage_requirements" : "Resource needs" ,
"performance_expectations" : "Response times"
}
```

Investing time in this planning phase:

- Prevents scope creep during development
- Ensures clear alignment with team expectations
- Makes code structure more maintainable
- Helps predict potential issues before they arise
- Creates clear testing boundaries
- Provides systematic upgrade paths for future versions

Remember: **It's easier to adjust plans than refactor code. Take time to ask questions and challenge assumptions before implementation begins.**

## [ Pre-Development Checklist](#pre-development-checklist)

### [ 1. Purpose](#1-purpose)

Define a clear, single-responsibility purpose. Study these examples from the codebase:

## SearchAgent

Finds and retrieves specific content within videos

## ThumbnailAgent

Generates preview images from video frames

## UploadAgent

Handles media uploads with format validation and processing

### [ 2. Background Check](#2-background-check)

Review the [director/agents/](https://github.com/video-db/Director/tree/main/backend/director/agents) directory for similar functionality

- Consider extending existing agents by:
    - Optimizing core functionality or improving performance
    - Adding new capabilities
    - Enhancing integration points (adding support for better tools, platforms or models)

### [ 3. Agent architecture](#3-agent-architecture)

**I/O Contract**

The **I/O Contract** defines how your agent interacts with the system, including the expected inputs, outputs, and how they are structured. It ensures consistency and clarity in communication between the agent, the system, and the end user. This contract is critical for integrating your agent with the infrastructure and enabling seamless interaction with other components. **Input Contract** The input contract specifies the parameters your agent expects to receive. These parameters can be simple (e.g., a string or number) or complex (e.g., a nested JSON object). The input contract is defined in two parts:

1. **Function Signature** : The `run` method of your agent defines the expected parameters.
2. **JSON Schema** : For complex inputs, a JSON schema is used to describe the structure and constraints of the input data.

**Simple Input Example** For agents with straightforward inputs, you can define the parameters directly in the `run` method. Here's an example for a Slack agent:

```
def run ( self , message : str , channel : str = None ) -> AgentResponse:
"""Send a message to a Slack channel.

Args:
message (str): The content to send.
channel (str, optional): The target Slack channel. Defaults to None.
"""
# Agent logic here
return AgentResponse( status = AgentStatus. SUCCESS , message = "Message sent successfully" )
```

**Complex Input Example** For agents requiring structured inputs (e.g., video generation), you define a JSON schema. This schema is used to validate the input and provide clear documentation for API consumers. Here's an example for a video generation agent:

```
VIDEO_GENERATION_PARAMETERS = {
"type" : "object" ,
"properties" : {
"prompt" : {
"type" : "string" ,
"description" : "Text prompt for video generation" ,
},
"config" : {
"type" : "object" ,
"properties" : {
"duration" : {
"type" : "integer" ,
"description" : "Duration of the video in seconds" ,
},
"style" : {
"type" : "string" ,
"description" : "Visual style for the video (e.g., cinematic, photorealistic)" ,
},
},
"required" : [ "duration" ], # Mandatory fields
},
},
"required" : [ "prompt" ], # Mandatory fields
}
```

In this example:

- The `prompt` field is a required string.
- The `config` field is an optional object with nested properties ( `duration` and `style` ).
- The `required` keyword ensures mandatory fields are validated.

**Output Contract** The output contract defines how your agent communicates results, errors, and progress updates. This includes:

1. **AgentResponse** : A standardized response format for success or failure.
2. **Progress Updates** : Real-time updates using the `output_message` object.
3. **Frontend Content Handling** : Structured content for rendering in the frontend (e.g., text, video, images).

**AgentResponse** The `AgentResponse` object is used to return the result of the agent's execution. It includes:

- `status` : Indicates success ( `AgentStatus.SUCCESS` ) or failure ( `AgentStatus.ERROR` ).
- `message` : A human-readable message describing the result.
- `data` : Additional data returned by the agent (e.g., generated content).

Example:

```
return AgentResponse(
status = AgentStatus. SUCCESS ,
message = "Video generated successfully" ,
data = { "video_url" : "https://example.com/video.mp4" },
)
```

**Progress Updates** Use the `output_message` object to provide real-time updates during the agent's execution. For example:

```
self .output_message.actions.append( "Generating video..." )
self .output_message.push_update()
```

**Frontend Content Handling** Agents can return different types of content (e.g., text, video, images) using the `output_message.content` list. Each content type is represented by a specific model (e.g., `TextContent` , `VideoContent` ). Example:

```
video_content = VideoContent(
agent_name = self .agent_name,
status = MsgStatus.progress,
status_message = "Generating video..." ,
video = VideoData( stream_url = "https://example.com/video.mp4" ),
)
self .output_message.content.append(video_content)
self .output_message.publish()
```

**Workflow Definition**

Plan and fix the steps to go from input → output. Keep the following factors in mind:

- Input validation &amp; preprocessing
- Resource initialization
- Core processing steps
- Progress updates
- Result formatting &amp; cleanup

**Agent &amp; Tool Composition**

Look for composition opportunities with existing agents or tools

- Example 1: ComparisonAgent leveraging VideoGenerationAgent
- Example 2: AudioGenerationAgent using ElevenLabs tool

### [ 4. Session Management](#4-session-management)

- The `session` parameter is crucial for maintaining context across multiple interactions, preventing the agent from handling requests without retaining state.
- Assigning a unique name and description aids in debugging and log analysis, making it easier to track agent behavior
- Flexible parameter handling: Your agent can either get its settings on-the-fly from user input (dynamic parameters), or use pre-defined parameters that you specify upfront. Simple agents often work best with dynamic parameters, while complex agents usually need pre-defined configurations.

```
class NewAgent ( BaseAgent ):
def __init__ ( self , session : Session, ** kwargs ):
self .agent_name = "unique_name"
self .description = "Clear, specific description"
self .parameters = self .get_parameters()
super (). __init__ ( session = session, ** kwargs)
```

Note: Parameter handling `self.parameters` changes based on the complexity of the parameters required for the agent:

```
#in case of simple docstring
self .parameters = self .get_parameters()

#in case of dictionary of complex parameters:
self .parameters = AGENT_PARAMETERS
```

**Key Points of User Communication:**

**Director's Log (Showing Steps)**

Think of this like a progress bar or status updates you see when installing software. It tells users what's happening behind the scenes.

```
# Shows up as a list of actions in the chat
self .output_message.actions.append( "Starting video processing..." )
self .output_message.actions.append( "Loading AI model..." )
self .output_message.actions.append( "Creating final video..." )
```

**Progress Updates (Showing Content Responses)**

This handles the actual content (videos, images, text) and its current state. Think of this like when you upload a file to Google Drive - you see both the file and its upload status.

```
# Create a video player with loading state
content = VideoContent(
status = MsgStatus.progress, # Can be progress/success/error
status_message = "Your video is being generated..." , # User-friendly message
)

# Add it to the chat
self .output_message.content.append(content)

# Show it to the user
self .output_message.push_update()
```

This shows up in the chat as:

- A video player
- A loading indicator
- A message saying "Your video is being generated..."

**Final Cut (Returning Results)**

When the agent finishes, it returns three things:

- `status:` Did it work? (success/error)
- `message:` What happened? (user-friendly explanation)
- `data:` The actual results (video URLs, text, etc.)

```
self .output_message.status = MsgStatus.success # Can also be error
self .output_message.status_message = "Your video is ready!"
self .output_message.data = { "video_url" : generated_video_url} # Or relevant result data

# Send the final message to the user
self .output_message.publish()
```

### [ 5. Error Handling](#5-error-handling)

Clear error responses help the reasoning engine interpret failures, guide users effectively, and determine the next appropriate actions in the workflow.

```
try :
# Main logic
self .output_message.actions.append( "Current action..." )
self .output_message.push_update()
except Exception as e:
logger.exception( f "Error in { self .agent_name } " )
content.status = MsgStatus.error
content.status_message = "User-friendly error message"
self .output_message.publish()
return AgentResponse( status = AgentStatus. ERROR , message = str (e))
```

## [ Best Practices](#best-practices)

1. **Clear Agent &amp; Parameter Descriptions**

- Agent definitions help Reasoning Engine select the appropriate agent
- Parameter definitions guide RE in providing correct instructions

```
self .description = "Generates video with AI models, supporting multiple providers and configurations"
```

1. **Use explicit status updates**

```
self .output_message.actions.append( "Specific action..." )
self .output_message.push_update()
```

1. **Resource Management**

```
try :
# Resource operations
finally :
# Cleanup
```

1. **Validate inputs early:**

```
if not required_param:
raise ValueError ( "Clear error message explaining what's missing and how to fix" )
```

1. **Use appropriate content [response] types:**

```
`VideoContent` , `TextContent` , `ImageContent` , `SearchResultsContent`
```

## [ Further Resources and Next Steps](#further-resources-and-next-steps)

Ready to build your first agent? Start with our sample agents in the `director/agents/` directory or check out these resources:

## Director Documentation

Comprehensive guides and API references for the Director framework

## Sample Agents Repository

Real-world examples and implementations of custom agents

## OpenAI Function Schema Guide

Learn about parameter schema design and function calling

## Discord Community

Connect with other agent developers and get support

Need help? Reach out to our community or open an issue on [GitHub](https://github.com/video-db) .

[Setup Director](\pages\build-with-agents\director\setup-director)

⌘ I