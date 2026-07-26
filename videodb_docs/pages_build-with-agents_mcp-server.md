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

## On this page

- [Prerequisite: Ensure Python 3.12 or Later is Installed](#prerequisite-ensure-python-3-12-or-later-is-installed)
- [Install and Configure VideoDB MCP Server](#install-and-configure-videodb-mcp-server)
- [1. Install uv](#1-install-uv)
- [2. Automatic Installation for Clients](#2-automatic-installation-for-clients)
- [3. Update VideoDB MCP package](#3-update-videodb-mcp-package)
- [Setup Video](#setup-video)
- [Alternative Methods](#alternative-methods)
- [1. Install the VideoDB MCP Server](#1-install-the-videodb-mcp-server)
    - [a. Using pipx](#a-using-pipx)
    - [b. Install Using pip](#b-install-using-pip)
- [2. Configuring the MCP Server in Clients](#2-configuring-the-mcp-server-in-clients)
    - [Claude Desktop](#claude-desktop)
    - [Cursor Editor](#cursor-editor)
    - [Claude Code](#claude-code)
- [3. Update the VideoDB Director MCP Package](#3-update-the-videodb-director-mcp-package)

[Open Source Frameworks](\pages\build-with-agents\mcp-server)

# MCP Server

Copy page

The VideoDB MCP Server can be installed and used in multiple ways. Follow the steps below to set it up.

Copy page

## [ Prerequisite: Ensure Python 3.12 or Later is Installed](#prerequisite-ensure-python-3-12-or-later-is-installed)

Before installing the VideoDB MCP Server, verify that Python 3.12 or later is installed on your system.

- **Check Python version:**

```
python --version
```

- If the version is below 3.12, update Python from the [official website](https://www.python.org/downloads/) .

# [ Install and Configure VideoDB MCP Server](#install-and-configure-videodb-mcp-server)

simplest method using `uvx`

## [ 1. Install uv](#1-install-uv)

**macOS:**

```
brew install uv
```

**For macOS/Linux:**

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**For Windows:**

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

You can visit the complete installation steps for uv [here](https://astral.sh/uv) .

## [ 2. Automatic Installation for Clients](#2-automatic-installation-for-clients)

To automatically add the MCP Server to Claude, Cursor and Claude Code: **Install for Claude only**

```
uvx videodb-director-mcp --install=claude
```

**Install for Cursor only**

```
uvx videodb-director-mcp --install=cursor
```

**Install for both Claude and Cursor**

```
uvx videodb-director-mcp --install=all
```

**Install for Claude Code**

```
claude mcp add videodb-director uvx -- videodb-director-mcp --api-key= < VIDEODB_API_KEY >
```

## [ 3. Update VideoDB MCP package](#3-update-videodb-mcp-package)

To ensure you're using the latest version of the MCP server with `uvx` , start by clearing the cache:

```
uv cache clean
```

This command removes any outdated cached packages of `videodb-director-mcp` , allowing `uvx` to fetch the most recent version. If you always want to use the latest version of the MCP server, update your command as follows:

```
uvx videodb-director-mcp@latest --api-key= < VIDEODB_API_KEY >
```

This ensures that `uvx` pulls the latest release every time you run it.

## [ Setup Video](#setup-video)

# [ Alternative Methods](#alternative-methods)

## [ 1. Install the VideoDB MCP Server](#1-install-the-videodb-mcp-server)

### [ a. Using pipx](#a-using-pipx)

We need to install `pipx` first. **For macOS:**

```
brew install pipx
pipx ensurepath
```

**For Windows:**

```
python -m pip install --user pipx
python -m pipx ensurepath
```

You can now run the MCP Server using:

```
pipx run videodb-director-mcp --api-key=VIDEODB_API_KEY
```

### [ b. Install Using pip](#b-install-using-pip)

Install the package using pip:

```
pip install videodb-director-mcp
```

The MCP server can now be started with the following command:

```
videodb-director-mcp --api-key=VIDEODB_API_KEY
```

## [ 2. Configuring the MCP Server in Clients](#2-configuring-the-mcp-server-in-clients)

### [ Claude Desktop](#claude-desktop)

**a. Open Configuration File**

- **MacOS/Linux:**

```
code ~/Library/Application \ Support/Claude/claude_desktop_config.json
```

- **Windows:**

```
code $env :AppData \C laude \c laude_desktop_config.json
```

**b. Modify Configuration Using** **`pipx`** **:**

```
{
"mcpServers" : {
"videodb-director" : {
"command" : "pipx" ,
"args" : [ "run" , "videodb-director-mcp" , "--api-key=<VIDEODB-API-KEY>" ]
}
}
}
```

**Using package installed via** **`pip`** **:**

```
{
"mcpServers" : {
"videodb-director" : {
"command" : "videodb-director-mcp" ,
"args" : [ "--api-key=<VIDEODB-API-KEY>" ]
}
}
}
```

### [ Cursor Editor](#cursor-editor)

**a. Open MCP Settings**

1. Navigate to **Settings** &gt; **Cursor Settings**
2. Click on **MCP**
3. Click on **Add new Global MCP Server**

**b. Add Configuration Using** **`pipx`** **:**

```
{
"mcpServers" : {
"videodb-director" : {
"command" : "pipx" ,
"args" : [ "run" , "videodb-director-mcp" , "--api-key=<VIDEODB-API-KEY>" ]
}
}
}
```

**Using package installed via** **`pip`** **:**

```
{
"mcpServers" : {
"videodb-director" : {
"command" : "videodb-director-mcp" ,
"args" : [ "--api-key=<VIDEODB-API-KEY>" ]
}
}
}
```

### [ Claude Code](#claude-code)

**a. Add configuration** To configure VideoDB Director MCP for Claude code you can run the following command **Using** **`pipx`** **:**

```
claude mcp add videodb-director pipx -- run videodb-director-mcp --api-key= < VIDEODB_API_KEY >
```

**Using package installed via** **`pip`** **:**

```
claude mcp add videodb-director videodb-director-mcp -- --api-key= < VIDEODB_API_KEY >
```

**b. Verify configuration** You can verify if the MCP Server has been added correctly or not by simply running the following command:

```
claude mcp list
```

## [ 3. Update the VideoDB Director MCP Package](#3-update-the-videodb-director-mcp-package)

To ensure you're using the latest version of a package installed via `pipx` or `pip` , run:

```
pip install --upgrade videodb-director-mcp
```

This will upgrade the package to its latest available version.

[Video Q&amp;A Support](\pages\automate\zapier\zapier-workflow-video-qa) [LlamaIndex Retriever](\pages\community\open-source\llamaindex-retriever)

⌘ I