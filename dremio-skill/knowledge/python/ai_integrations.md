# Ai Integrations

## AI API Call Generation

The `generate-api` command (or `agent.generate_api_call()` method) generates a cURL command for the Dremio REST API. It uses the library's documentation and native Dremio documentation (if available) to find the correct endpoint and payload.

## Usage via CLI

The `generate-api` command takes the following arguments:

- `prompt` (Required): The natural language description of the API call you want to generate.
- `--model` / `-m` (Optional): The LLM model to use. Defaults to `gpt-4o`.

**Examples:**

```bash
# Generate a cURL command to list all sources (using default gpt-4o)
dremio-cli generate-api "List all sources"

# Generate a command to create a space using Claude 3 Opus
dremio-cli generate-api "Create a space named 'Marketing'" --model claude-3-opus

# Generate a command to trigger a reflection refresh
dremio-cli generate-api "Refresh the reflection with ID 12345"
```

## Usage via Python

```python
from dremioframe.ai.agent import DremioAgent

agent = DremioAgent()
curl = agent.generate_api_call("List all sources")
print(curl)
```

## How it Works

1.  **Context Awareness**: The agent is aware of the API specification (via documentation).
2.  **Security**: The agent generates the command but does not execute it automatically. You have full control to review and run the output.


---

<!-- Source: docs/ai/cli_chat.md -->

---

## AI Governance Tools

The `DremioAgent` assists with governance tasks such as auditing access and automating documentation.

## Features

### 1. Access Auditing
The agent can list privileges granted on specific entities (tables, views, folders, spaces).

-   **Tool**: `show_grants(entity)`

### 2. Automated Documentation
The agent can inspect a dataset's schema and automatically generate a Wiki description and suggest Tags.

-   **Method**: `agent.auto_document_dataset(path)`

## Usage Examples

### Auditing Access

```python
from dremioframe.ai.agent import DremioAgent

agent = DremioAgent()

# Check who has access to a sensitive table
response = agent.generate_script("Show grants for table 'finance.payroll'")
print(response)
```

### Auto-Documenting a Dataset

```python
# Generate documentation for a dataset
path = "sales.transactions"
documentation = agent.auto_document_dataset(path)

print("Generated Documentation:")
print(documentation)

# You can then use the client to apply this documentation
# import json
# doc_data = json.loads(documentation)
# client.catalog.update_wiki(dataset_id, doc_data['wiki'])
# client.catalog.set_tags(dataset_id, doc_data['tags'])
```


---

<!-- Source: docs/ai/mcp_client.md -->

---

## AI Observability Tools

The `DremioAgent` includes powerful observability tools to help you monitor and debug your Dremio environment.

## Features

### 1. Job Analysis
The agent can inspect job details, including status, duration, and error messages.

-   **Tool**: `get_job_details(job_id)`
-   **Tool**: `list_recent_jobs(limit)`

### 2. Failure Analysis
The agent can analyze failed jobs and provide actionable explanations and fixes using its LLM capabilities.

-   **Method**: `agent.analyze_job_failure(job_id)`

## Usage Examples

### Listing Recent Jobs

```python
from dremioframe.ai.agent import DremioAgent

agent = DremioAgent()

# Ask the agent to list jobs
response = agent.generate_script("List the 5 most recent failed jobs")
print(response)
```

### Analyzing a Failed Job

```python
# Analyze a specific job failure
job_id = "12345-67890-abcdef"
analysis = agent.analyze_job_failure(job_id)

print("Failure Analysis:")
print(analysis)
```

### Interactive Debugging

You can also use the agent to interactively debug issues:

```python
agent.agent.invoke({"messages": [("user", "Why did my last query fail?")]})
```


---

<!-- Source: docs/ai/optimization.md -->

---

## AI Reflection Tools

The `DremioAgent` can help you manage and optimize Dremio Reflections, which are critical for query acceleration.

## Features

### 1. Reflection Management
The agent can list existing reflections and create new ones.

-   **Tool**: `list_reflections()`
-   **Tool**: `create_reflection(dataset_id, name, type, fields)`

### 2. Smart Recommendations
The agent can analyze a SQL query and recommend the optimal reflection configuration (Raw vs. Aggregation) to accelerate it.

-   **Method**: `agent.recommend_reflections(query)`

## Usage Examples

### Listing Reflections

```python
from dremioframe.ai.agent import DremioAgent

agent = DremioAgent()

# List all reflections
response = agent.generate_script("List all reflections in the system")
print(response)
```

### Getting Recommendations

```python
query = """
SELECT 
    region, 
    SUM(sales_amount) as total_sales 
FROM sales.transactions 
GROUP BY region
"""

recommendation = agent.recommend_reflections(query)
print("Recommended Reflection:")
print(recommendation)
```

### Creating a Reflection

You can ask the agent to create a reflection based on a recommendation.

```python
agent.agent.invoke({"messages": [("user", "Create an aggregation reflection on 'sales.transactions' for the query I just showed you.")]})
```


---

<!-- Source: docs/ai/sql.md -->

---

## AI Script Generation

`dremioframe` includes an AI-powered module that can generate Python scripts for you based on natural language prompts. It uses LangChain and supports OpenAI, Anthropic, and Google Gemini models.

## Installation

To use the AI features, you must install the optional `ai` dependencies:

```bash
pip install dremioframe[ai]
```

## Configuration

You need to set the API key for your chosen model provider in your environment variables:

- **OpenAI**: `OPENAI_API_KEY`
- **Anthropic**: `ANTHROPIC_API_KEY`
- **Google Gemini**: `GOOGLE_API_KEY`

## Usage via CLI

You can generate scripts directly from the command line using the `generate` command.

```bash
# Generate a script to list all sources
dremio-cli generate "List all sources and print their names" --output list_sources.py

# Use a specific model (default is gpt-4o)
dremio-cli generate "Create a view named 'sales_summary' from 'sales_raw'" --model claude-3-opus --output create_view.py

# Use a prompt from a file
dremio-cli generate prompt.txt --output script.py
```

## Usage via Python

You can also use the `DremioAgent` class directly in your Python code.

### Arguments for `generate_script`

- `prompt` (str): The natural language request describing the script you want to generate.
- `output_file` (Optional[str]): The path to save the generated script to. If not provided, the script is returned as a string.

### Using Custom LLMs

You can use any LangChain-compatible chat model by passing it to the `DremioAgent` constructor.

```python
from dremioframe.ai.agent import DremioAgent
from langchain_openai import ChatOpenAI

# Initialize with a custom LLM instance
custom_llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.5)
agent = DremioAgent(llm=custom_llm)

# Generate a script
prompt = "Write a script to connect to Dremio and list all spaces."
script = agent.generate_script(prompt)

print(script)
```

### Example: Using a Local LLM (e.g., Ollama)

You can use a local LLM running via Ollama or any other OpenAI-compatible server.

```python
from dremioframe.ai.agent import DremioAgent
from langchain_openai import ChatOpenAI

# Connect to local Ollama instance
local_llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama", # Required but ignored
    model="llama3"
)

agent = DremioAgent(llm=local_llm)
agent.generate_script("List all sources")
```

### Example: Using Amazon Bedrock

To use Amazon Bedrock, you need to install `langchain-aws`.

```bash
pip install langchain-aws
```

```python
from dremioframe.ai.agent import DremioAgent
from langchain_aws import ChatBedrock

# Initialize Bedrock client
bedrock_llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0.1}
)

agent = DremioAgent(llm=bedrock_llm)
agent.generate_script("Create a view from sales data")
```

## How it Works

The agent has access to:
1.  **Library Documentation**: It can list and read `dremioframe` documentation files.
2.  **Dremio Documentation**: It can search and read native Dremio documentation (if available in `dremiodocs/`) to understand SQL functions and concepts.

It generates a complete Python script that includes:
1.  Importing `DremioClient`.
2.  Initializing the client (expecting `DREMIO_PAT` and `DREMIO_PROJECT_ID` env vars).
3.  Performing the requested actions using the appropriate methods.


---

<!-- Source: docs/ai/governance.md -->

---

## AI SQL Generation

The `generate-sql` command (or `agent.generate_sql()` method) generates a SQL query based on a natural language prompt. It uses the `list_catalog_items` and `get_table_schema` tools to inspect your Dremio catalog and validate table names and columns.

## Usage via CLI

The `generate-sql` command takes the following arguments:

- `prompt` (Required): The natural language description of the SQL query you want to generate.
- `--model` / `-m` (Optional): The LLM model to use. Defaults to `gpt-4o`.

**Examples:**

```bash
# Generate a query to select data from a specific table (using default gpt-4o)
dremio-cli generate-sql "Select the first 10 rows from the zips table in Samples"

# Generate a complex aggregation using Claude 3 Opus
dremio-cli generate-sql "Calculate the average population by state from the zips table" --model claude-3-opus
```

## Usage via Python

```python
from dremioframe.ai.agent import DremioAgent

agent = DremioAgent()
sql = agent.generate_sql("Select the first 10 rows from the zips table in Samples")
print(sql)
```

## How it Works

1.  **Context Awareness**: The agent is aware of your Dremio environment's structure (via catalog tools).
2.  **Validation**: It attempts to verify table names and columns against the actual catalog to prevent errors.
3.  **Security**: The agent generates the SQL but does not execute it automatically. You have full control to review and run the output.


---

<!-- Source: docs/analysis/charting.md -->

---

## AI SQL Optimization Tools

The `DremioAgent` can act as your personal database administrator, analyzing query plans and suggesting optimizations.

## Features

### 1. Query Plan Analysis
The agent runs `EXPLAIN PLAN` on your SQL query and analyzes the execution plan to identify bottlenecks, such as full table scans or expensive joins.

-   **Tool**: `optimize_query(query)`
-   **Method**: `agent.optimize_sql(query)`

## Usage Examples

### Optimizing a Query

```python
from dremioframe.ai.agent import DremioAgent

agent = DremioAgent()

# A potentially slow query
query = """
SELECT * 
FROM sales.transactions t
JOIN crm.customers c ON t.customer_id = c.id
WHERE t.amount > 1000
"""

# Ask the agent to optimize it
optimization = agent.optimize_sql(query)

print("Optimization Suggestions:")
print(optimization)
```

### Example Output

The agent might suggest:
-   Creating a Raw Reflection on `sales.transactions` covering `customer_id` and `amount`.
-   Filtering `sales.transactions` before joining.
-   Using a specific join type if applicable.


---

<!-- Source: docs/ai/overview.md -->

---

## Dremio Agent MCP Server

The Dremio Agent MCP Server exposes Dremio capabilities via the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), allowing you to use Dremio tools directly within MCP-compliant AI clients like Claude Desktop or IDE extensions.

> [!NOTE]
> This guide explains how to use DremioFrame as an MCP **Server**. If you want to use external MCP tools *within* the Dremio Agent, see [Using MCP Tools](mcp_client.md).

## Installation

The MCP server requires the `mcp` optional dependency:

```bash
pip install "dremioframe[server]"
```

## Configuration

To use the server, you need to configure your MCP client to run the `dremio-cli mcp start` command.

You can generate the configuration JSON using the CLI:

```bash
dremio-cli mcp config
```

This will output a JSON structure similar to:

```json
{
  "mcpServers": {
    "dremio-agent": {
      "command": "/path/to/python",
      "args": [
        "-m",
        "dremioframe.cli",
        "mcp",
        "start"
      ],
      "env": {
        "DREMIO_PAT": "your_pat_here",
        "DREMIO_PROJECT_ID": "your_project_id_here"
      }
    }
  }
}
```

### Environment Variables

Ensure you set the correct environment variables in the `env` section of the configuration:

- **Dremio Cloud**: `DREMIO_PAT`, `DREMIO_PROJECT_ID`
- **Dremio Software**: `DREMIO_SOFTWARE_HOST`, `DREMIO_SOFTWARE_PAT` (or `DREMIO_SOFTWARE_USER`/`PASSWORD`)

## Available Tools

The server exposes the following tools to the AI model:

- **`list_catalog(path)`**: List contents of the catalog.
- **`get_entity(path)`**: Get details of a dataset or container.
- **`query_dremio(sql)`**: Execute a SQL query and get results as JSON.
- **`list_reflections()`**: List all reflections.
- **`get_job_profile(job_id)`**: Get details of a job.
- **`create_view(path, sql)`**: Create a virtual dataset.
- **`list_available_docs()`**: List available documentation files.

## Resources

The server exposes documentation as MCP Resources. The AI client can read these resources to understand how to use `dremioframe` and Dremio SQL.

- **`dremio://docs/{category}/{file}`**: Read library documentation.
- **`dremio://dremiodocs/{category}/{file}`**: Read Dremio native documentation.

## Usage Example (Claude Desktop)

1. **Configure**: Add the server config to your Claude Desktop configuration.
2. **Ask**: "How do I query a table using dremioframe?" or "Write a script to list all reflections."
3. **Context**: Claude will use the `list_available_docs` tool to find relevant documentation, read it via the Resources, and then generate the code for you.


---

<!-- Source: docs/ai/observability.md -->

---

## Dremio AI Agent

DremioFrame includes a powerful AI Agent powered by Large Language Models (LLMs) that acts as your intelligent co-pilot for Dremio development and administration.

## Capabilities

The AI Agent is designed to assist with:

-   **[Generation](generation.md)**: Generate Python Scripts, [SQL](sql.md) and [cURL](api.md) commands to interact with your Dremio instance
-   **[Observability](observability.md)**: Analyze job failures and monitor system health.
-   **[Reflections](reflections.md)**: Recommend and manage reflections for query acceleration.
-   **[Governance](governance.md)**: Audit access and automate dataset documentation.
-   **[Data Quality](data_quality.md)**: Generate data quality recipes automatically.
-   **[SQL Optimization](optimization.md)**: Analyze query plans and suggest performance improvements.
-   **[Interactive Chat](cli_chat.md)**: Converse with the agent directly from the CLI.

**note:** this libraries embdedded agent is primarily meant as a code generation assist tool, not meant as an alternative to the integrated Dremio agent for deeper administration and natural language analytics. Login to your Dremio instance's UI to leverage integrated agent.

## Getting Started

To use the AI features, you need to install the optional dependencies:

```bash
pip install dremioframe[ai]
```

You also need to set your LLM API key in your environment variables.

### Required Environment Variables

The AI agent supports multiple LLM providers. Set the appropriate environment variable for your chosen provider:

| Provider | Environment Variable | How to Get |
|----------|---------------------|------------|
| **OpenAI** | `OPENAI_API_KEY` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| **Anthropic** | `ANTHROPIC_API_KEY` | [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys) |
| **Google** | `GOOGLE_API_KEY` | [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) |

**Example `.env` file:**
```bash
# Choose one based on your provider
OPENAI_API_KEY=sk-proj-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=AIza...

# Dremio credentials (required for agent to access catalog)
DREMIO_PAT=your_personal_access_token
DREMIO_PROJECT_ID=your_project_id
DREMIO_URL=data.dremio.cloud
```

## Usage

You can use the agent programmatically in your Python scripts or interactively via the CLI.

```python
from dremioframe.ai.agent import DremioAgent

agent = DremioAgent(model="gpt-4o")
response = agent.generate_script("List all spaces")
print(response)
```


---

<!-- Source: docs/ai/reflections.md -->

---

## Using MCP Tools in Dremio Agent

> [!NOTE]
> This guide explains how to use external MCP tools *within* the Dremio Agent. If you want to use DremioFrame as an MCP **Server** for other clients (like Claude), see [MCP Server](mcp_server.md).

The DremioAgent supports integration with **Model Context Protocol (MCP)** servers, allowing you to extend the agent with custom tools from any MCP-compatible server.

## What is MCP?

The Model Context Protocol is an open standard introduced by Anthropic that standardizes how AI systems integrate with external tools, systems, and data sources. It provides a universal interface for:
- File system access
- Database connections
- API integrations
- Custom tool implementations

## Installation

```bash
pip install dremioframe[mcp]
```

## Usage

### Basic Example

```python
from dremioframe.ai.agent import DremioAgent

# Configure MCP servers
mcp_servers = {
    "filesystem": {
        "transport": "stdio",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/data"]
    },
    "github": {
        "transport": "stdio",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"]
    }
}

# Initialize agent with MCP servers
agent = DremioAgent(
    model="gpt-4o",
    mcp_servers=mcp_servers
)

# The agent now has access to tools from both MCP servers
script = agent.generate_script(
    "List all files in the data directory and create a table from the CSV files"
)
```

### Available MCP Servers

Popular MCP servers include:
- **@modelcontextprotocol/server-filesystem**: File system operations
- **@modelcontextprotocol/server-github**: GitHub API access
- **@modelcontextprotocol/server-postgres**: PostgreSQL database access
- **@modelcontextprotocol/server-sqlite**: SQLite database access

See the [MCP Server Registry](https://github.com/modelcontextprotocol/servers) for more.

### Transport Protocols

MCP supports three transport protocols for client-server communication. Choose based on your deployment scenario:

#### `stdio` (Standard Input/Output)

**Best for**: Local integrations, command-line tools, development

**How it works**: The client launches the MCP server as a subprocess and communicates through standard input/output streams.

**Characteristics**:
- ✅ **Lowest latency** - No network overhead
- ✅ **Most secure** - No network exposure
- ✅ **Simplest setup** - No network configuration needed
- ❌ **Single client only** - One-to-one relationship
- ❌ **Same machine only** - Cannot communicate across network

**When to use**:
- Local AI tools running on your machine
- Development and testing
- Security-sensitive operations
- Command-line integrations

**Example**:
```python
mcp_servers = {
    "local_files": {
        "transport": "stdio",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/data"]
    }
}
```

---

#### `http` (Streamable HTTP) - **Recommended for Production**

**Best for**: Web applications, remote servers, multi-client environments

**How it works**: MCP server runs as an independent HTTP server. Clients connect over HTTP/HTTPS. Optionally uses Server-Sent Events (SSE) for server-to-client streaming.

**Characteristics**:
- ✅ **Remote access** - Works across networks
- ✅ **Multiple clients** - Supports concurrent connections
- ✅ **Authentication** - Supports JWT, API keys, etc.
- ✅ **Scalable** - Enterprise-ready
- ✅ **Modern standard** - Latest MCP specification
- ❌ **More complex setup** - Requires server deployment

**When to use**:
- Web-based AI applications
- Cloud-hosted MCP servers
- Multiple AI clients accessing same server
- Enterprise integrations requiring authentication
- Production deployments

**Example**:
```python
mcp_servers = {
    "remote_api": {
        "transport": "http",
        "url": "https://mcp-server.example.com",
        "headers": {
            "Authorization": "Bearer YOUR_TOKEN"
        }
    }
}
```

**OAuth 2.0 Support**:

Yes! The `http` transport supports OAuth authentication via the `headers` parameter. You can pass OAuth tokens (Bearer tokens, API keys, etc.) with every request:

```python
mcp_servers = {
    "oauth_server": {
        "transport": "http",
        "url": "https://secure-mcp-server.example.com/mcp",
        "headers": {
            "Authorization": "Bearer YOUR_OAUTH_TOKEN",
            "X-Custom-Header": "additional-auth-data"
        }
    }
}
```

**Note**: The current implementation passes static headers. For OAuth token refresh, you'll need to manage token renewal externally and reinitialize the agent with updated tokens.

---

#### `sse` (Server-Sent Events) - **Legacy/Deprecated**

**Best for**: Backwards compatibility only

**How it works**: Uses Server-Sent Events for server-to-client streaming, paired with HTTP POST for client-to-server requests.

**Status**: ⚠️ **Deprecated** - Replaced by Streamable HTTP

**When to use**:
- Only for compatibility with older MCP servers
- **Not recommended for new implementations**

---

### Quick Comparison

| Feature | stdio | http | sse |
|---------|-------|------|-----|
| **Latency** | Lowest | Medium | Medium |
| **Security** | Highest (local) | Good (with auth) | Good (with auth) |
| **Setup Complexity** | Simplest | Moderate | Moderate |
| **Multi-client** | ❌ No | ✅ Yes | ✅ Yes |
| **Remote Access** | ❌ No | ✅ Yes | ✅ Yes |
| **Authentication** | N/A | ✅ Yes | ✅ Yes |
| **Status** | ✅ Active | ✅ Recommended | ⚠️ Deprecated |

### Configuration Format

Each MCP server configuration requires:
- **transport**: Communication method (`"stdio"` or `"http"`)
- **command** (stdio only): Executable command (e.g., `"npx"`, `"python"`)
- **args** (stdio only): Command arguments (list of strings)
- **url** (http only): Server URL
- **headers** (http only, optional): Authentication headers

## Requirements

- **Node.js**: Required for npx-based MCP servers
- **langchain-mcp-adapters**: Installed automatically with `pip install dremioframe[mcp]`

## Example: File System Integration

```python
mcp_servers = {
    "files": {
        "transport": "stdio",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/data"]
    }
}

agent = DremioAgent(mcp_servers=mcp_servers)

# Agent can now read files, list directories, etc.
script = agent.generate_script(
    "Read all CSV files in /data and merge them into a single Dremio table"
)
```

## Troubleshooting

### MCP Server Not Found
Ensure Node.js and npx are installed:
```bash
node --version
npx --version
```

### Import Error
If you see "langchain-mcp-adapters not found":
```bash
pip install dremioframe[mcp]
```

### Server Connection Issues
Check server logs and ensure the command/args are correct for your MCP server.


---

<!-- Source: docs/ai/mcp_server.md -->

---

## Generate Structured Data
df.select(
    F.ai_generate(
        "Extract entities", 
        schema="ROW(person VARCHAR, location VARCHAR)"
    ).alias("entities")
)
```

### Raw SQL Usage

You can also use AI functions by writing the SQL string directly in `mutate` or `select`.

```python
df.mutate(
    spice_level="AI_CLASSIFY('Identify the Spice Level:' || ARRAY_TO_STRING(ingredients, ','), ARRAY [ 'mild', 'medium', 'spicy' ])"
)
```

## Available Functions

| Function | Description |
| :--- | :--- |
| `ai_classify(prompt, categories, model_name=None)` | Classifies text into one of the provided categories. |
| `ai_complete(prompt, model_name=None)` | Generates a text completion for the prompt. |
| `ai_generate(prompt, model_name=None, schema=None)` | Generates structured data based on the prompt. Use `schema` to define the output structure (e.g., `ROW(...)`). |

### Examples

#### AI_CLASSIFY

```python
F.ai_classify("Is this email spam?", ["Spam", "Not Spam"])
F.ai_classify("Categorize product", ["Electronics", "Clothing"], model_name="gpt-4")
```

#### AI_COMPLETE

```python
F.ai_complete("Write a SQL query to find top users")
F.ai_complete("Translate to French", model_name="gpt-3.5")
```

#### AI_GENERATE

```python

---

## Generate structured data
F.ai_generate(
    "Extract customer info", 
    schema="ROW(name VARCHAR, age INT)"
)