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

[Open Source Frameworks](\pages\build-with-agents\mcp-server)

[Director Framework](\pages\build-with-agents\director\index)

# Setup Director

Copy page

Install and configure the Director framework locally to build custom video agents and workflows for your applications.

Copy page

- **Clone the repository:**

Begin by cloning the **Director** repository and navigating to the project directory:

```
git clone https://github.com/video-db/Director.git
cd Director
```

- **Run the setup script:**

Execute the setup script to install all necessary dependencies:

```
./setup.sh
```

- **Run the Application**

You can start both the backend and frontend servers with:

```
make run
```

If you want to run them separately:

- **Backend only:** make run-be (Runs at [http://127.0.0.1:8000](http://127.0.0.1:8000/) )
- **Frontend only:** make run-fe (Runs at [http://127.0.0.1:8080](http://127.0.0.1:8080/) )

You are now ready to begin creating an agent in VideoDB Director!

[Director Framework](\pages\build-with-agents\director) [Create Custom Agent](\pages\build-with-agents\director\create-custom-agent)

⌘ I