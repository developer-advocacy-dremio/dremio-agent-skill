# Advanced Usage


---

## CI/CD & Deployment

Deploying `dremioframe` pipelines and managing Dremio resources (Views, Reflections, RBAC) should be automated using CI/CD.

## 1. Managing Resources as Code

Store your Dremio logic in a version-controlled repository.

*   **Views**: Define views as SQL files or Python scripts using `create_view`.
*   **Reflections**: Define reflection configurations in JSON/YAML or Python scripts.

### Example: Deploy Script (`deploy.py`)

```python
import os
from dremioframe.client import DremioClient

client = DremioClient()

def deploy_view(view_name, sql_file):
    with open(sql_file, "r") as f:
        sql = f.read()
    client.catalog.create_view(["Space", view_name], sql, overwrite=True)
    print(f"Deployed {view_name}")

if __name__ == "__main__":
    deploy_view("sales_summary", "views/sales_summary.sql")
```

## 2. GitHub Actions Workflow

Here is an example workflow to deploy changes when merging to `main`.

```yaml
name: Deploy to Dremio

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      DREMIO_PAT: ${{ secrets.DREMIO_PAT }}
      DREMIO_PROJECT_ID: ${{ secrets.DREMIO_PROJECT_ID }}
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: pip install dremioframe
        
      - name: Run Deploy Script
        run: python deploy.py
```

## 3. Environment Management

Use different Spaces or prefixes for environments (Dev, Staging, Prod).

```python
# deploy.py
env = os.environ.get("ENV", "dev")
space = f"Marketing_{env}"

client.catalog.create_view([space, "view_name"], ...)
```

## 4. Testing

Run Data Quality checks as part of your CI pipeline before deploying.

```bash
# In CI step
dremio-cli dq run tests/dq
```


---

<!-- Source: docs/getting_started/configuration.md -->

---

## Deployment Guide

DremioFrame Orchestration is designed to be easily deployed using Docker.

## Docker Deployment

We provide a `Dockerfile` and `docker-compose.yml` to get you started quickly with a full stack including:
- **Orchestrator**: Runs the Web UI and Scheduler.
- **Worker**: Runs Celery workers for distributed tasks.
- **Postgres**: Persistent backend for pipeline history.
- **Redis**: Message broker for Celery.

### Prerequisites
- Docker and Docker Compose installed.

### Quick Start

1. **Configure Environment**:
   Create a `.env` file with your Dremio credentials:
   ```bash
   DREMIO_PAT=your_pat
   DREMIO_PROJECT_ID=your_project_id
   ```

2. **Start Services**:
   ```bash
   docker-compose up -d
   ```

3. **Access UI**:
   Open `http://localhost:8080` in your browser.

### Customizing the Image

If you need additional Python packages (e.g. for custom tasks), you can extend the Dockerfile:

```dockerfile
FROM dremioframe:latest
RUN pip install pandas numpy
```

### Production Considerations

- **Security**: Enable Basic Auth by setting `USERNAME` and `PASSWORD` env vars (requires updating entrypoint script) or putting the UI behind a reverse proxy (Nginx/Traefik).
- **Database**: Use a managed Postgres instance (RDS/CloudSQL) instead of the containerized one for production data safety.
- **Scaling**: Scale workers using Docker Compose:
  ```bash
  docker-compose up -d --scale worker=3
  ```


---

<!-- Source: docs/orchestration/distributed.md -->

---

## Dremio API Compatibility Guide

`dremioframe` is designed to work seamlessly with Dremio Cloud, Dremio Software v26+, and Dremio Software v25. This document outlines how the library handles the differences between these versions.

## Supported Modes

The `DremioClient` accepts a `mode` parameter to configure behavior:

| Mode | Description | Default Auth | Base URL Pattern |
|------|-------------|--------------|------------------|
| `cloud` | Dremio Cloud | PAT + Project ID | `https://api.dremio.cloud/v0` |
| `v26` | Software v26+ | PAT (or User/Pass) | `https://{host}:9047/api/v3` |
| `v25` | Software v25 | User/Pass (or PAT) | `https://{host}:9047/api/v3` |

## Key Differences & Handling

### 1. Authentication

- **Cloud**: Uses Personal Access Tokens (PAT) exclusively. Requires `DREMIO_PAT` and `DREMIO_PROJECT_ID`.
- **Software v26**: Supports PATs natively. Can also use Username/Password to obtain a token via `/apiv3/login`.
- **Software v25**: Primarily uses Username/Password via `/apiv2/login` (legacy) or `/login` to obtain a token.

`dremioframe` automatically selects the correct login endpoint and token handling based on the `mode`.

### 2. API Endpoints

- **Project ID**: Dremio Cloud API paths typically require a project ID (e.g., `/v0/projects/{id}/catalog`). Dremio Software paths do not (e.g., `/api/v3/catalog`).
- **Base URL**: Cloud uses `/v0`, Software uses `/api/v3`.

The library's internal `_build_url` methods in `Catalog` and `Admin` classes automatically append the project ID for Cloud mode and omit it for Software mode.

### 3. Feature Support

| Feature | Cloud | Software | Handling |
|---------|-------|----------|----------|
| **Create Space** | No (Use Folders) | Yes | `create_space` raises `NotImplementedError` in Cloud mode. |
| **Reflections** | Yes | Yes | Unified interface via `admin.list_reflections`, etc. |
| **SQL Runner** | Yes | Yes | Unified via `client.query()`. |
| **Flight** | `data.dremio.cloud` | `{host}:32010` | Port and endpoint auto-configured. |

## Best Practices

- **Use Environment Variables**: Set `DREMIO_PAT`, `DREMIO_PROJECT_ID` (for Cloud), or `DREMIO_SOFTWARE_PAT`, `DREMIO_SOFTWARE_HOST` (for Software) to switch environments easily without changing code.
- **Check Mode**: If writing scripts that run across environments, check `client.mode` before calling software-specific methods like `create_space`.

```python
if client.mode == 'cloud':
    client.admin.create_folder("my_folder")
else:
    client.admin.create_space("my_space")
```


---

<!-- Source: docs/data_engineering/aggregation.md -->

---

## DremioAgent Class

The `DremioAgent` class is the core of the AI capabilities in `dremioframe`. It uses LangGraph and LangChain to create an agent that can understand your request, consult documentation, inspect the Dremio catalog, and generate code, SQL, or API calls.

## Purpose

The `DremioAgent` is designed to:
1.  **Generate Python Scripts**: Create complete, runnable scripts using `dremioframe` to automate tasks.
2.  **Generate SQL Queries**: Write complex SQL queries, validating table names and columns against the actual catalog.
3.  **Generate API Calls**: Construct cURL commands for the Dremio REST API by referencing the documentation.

## Constructor

```python
class DremioAgent(
    model: str = "gpt-4o", 
    api_key: Optional[str] = None, 
    llm: Optional[BaseChatModel] = None,
    memory_path: Optional[str] = None,
    context_folder: Optional[str] = None
)
```

### Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `model` | `str` | `"gpt-4o"` | The name of the LLM model to use. Supported providers are OpenAI, Anthropic, and Google. |
| `api_key` | `Optional[str]` | `None` | The API key for the chosen model provider. If not provided, the agent will look for the corresponding environment variable (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`). |
| `llm` | `Optional[BaseChatModel]` | `None` | A pre-configured LangChain Chat Model instance. If provided, `model` and `api_key` arguments are ignored. Use this to support other providers (AWS Bedrock, Ollama, Azure, etc.). |
| `memory_path` | `Optional[str]` | `None` | Path to a SQLite database file for persisting conversation history. If provided, conversations can be resumed using a `session_id`. Requires `langgraph-checkpoint-sqlite` (included in `ai` optional dependencies). |
| `context_folder` | `Optional[str]` | `None` | Path to a folder containing additional context files (schemas, documentation, etc.). The agent can list and read these files when generating code or SQL. |

## Supported Models

The `model` argument supports string identifiers for major providers. The agent automatically selects the correct LangChain class based on the string.

### OpenAI
*Requires `OPENAI_API_KEY`*
- `gpt-4o` (Default)
- `gpt-4-turbo`
- `gpt-3.5-turbo`

### Anthropic
*Requires `ANTHROPIC_API_KEY`*
- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307`

### Google Gemini
*Requires `GOOGLE_API_KEY`*
- `gemini-1.5-pro`
- `gemini-pro`

## Custom LLMs

To use a model provider not natively supported by the string shortcuts (like AWS Bedrock, Ollama, or Azure OpenAI), you can instantiate the LangChain model object yourself and pass it to the `llm` argument.

### Example: Local LLM (Ollama)

Use `ChatOpenAI` pointing to a local server (e.g., Ollama running Llama 3).

```python
from dremioframe.ai.agent import DremioAgent
from langchain_openai import ChatOpenAI

# Connect to local Ollama instance
local_llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama", # Required but ignored by Ollama
    model="llama3",
    temperature=0
)

agent = DremioAgent(llm=local_llm)
print(agent.generate_sql("List all tables in the 'Samples' space"))
```

### Example: AWS Bedrock

Use `ChatBedrock` from `langchain-aws`.

```bash
pip install langchain-aws
```

```python
from dremioframe.ai.agent import DremioAgent
from langchain_aws import ChatBedrock

bedrock_llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0}
)

agent = DremioAgent(llm=bedrock_llm)
```

### Example: Azure OpenAI

Use `AzureChatOpenAI` from `langchain-openai`.

```python
from dremioframe.ai.agent import DremioAgent
from langchain_openai import AzureChatOpenAI

azure_llm = AzureChatOpenAI(
    azure_deployment="my-gpt-4-deployment",
    openai_api_version="2023-05-15",
    temperature=0
)

agent = DremioAgent(llm=azure_llm)
```

## Memory Persistence

By default, the `DremioAgent` does not persist conversation history between sessions. Each invocation starts fresh. To enable memory persistence, provide a `memory_path` when creating the agent.

### Basic Usage

```python
from dremioframe.ai.agent import DremioAgent

# Create agent with memory
agent = DremioAgent(memory_path="./agent_memory.db")

# First conversation
code1 = agent.generate_script("Create a table from CSV", session_id="user123")

# Later, in the same or different session
code2 = agent.generate_script("Now add a column to that table", session_id="user123")
# The agent remembers the previous conversation and knows which table you're referring to
```

### How It Works

- **SQLite Database**: Conversation history is stored in a SQLite database at the specified path.
- **Session ID**: Each conversation thread is identified by a `session_id`. Use the same `session_id` to continue a conversation.
- **Thread Isolation**: Different `session_id` values create independent conversation threads.

### Example: Multi-Turn Conversation

```python
agent = DremioAgent(memory_path="./conversations.db")

session = "project_alpha"

# Turn 1
sql1 = agent.generate_sql("Get all users from the users table", session_id=session)
print(sql1)  # SELECT * FROM users

# Turn 2 - Agent remembers context
sql2 = agent.generate_sql("Filter to only active users", session_id=session)
print(sql2)  # SELECT * FROM users WHERE status = 'active'

# Turn 3 - Agent still has context
sql3 = agent.generate_sql("Add their email addresses", session_id=session)
print(sql3)  # SELECT *, email FROM users WHERE status = 'active'
```

### Managing Sessions

```python
# Different projects/users can have separate conversations
agent.generate_script("Create ETL pipeline", session_id="project_alpha")
agent.generate_script("Create dashboard", session_id="project_beta")

# Each session maintains its own context
```

### Clearing Memory

To clear all conversation history, simply delete the SQLite database file:

```python
import os
os.remove("./agent_memory.db")
```

## Context Folder

The `context_folder` feature allows the agent to access files from a specified directory. This is useful for:
- Reading project-specific schemas
- Referencing data dictionaries
- Using custom documentation
- Accessing configuration files

### Basic Usage

```python
from dremioframe.ai.agent import DremioAgent

# Create agent with context folder
agent = DremioAgent(context_folder="./project_docs")

# Agent can now reference files in ./project_docs
script = agent.generate_script(
    "Create a table based on the schema in schema.sql"
)
```

### Example: Project Documentation

```
project_docs/
├── schema.sql
├── data_dictionary.md
└── business_rules.txt
```

```python
agent = DremioAgent(context_folder="./project_docs")

# Agent can read these files when needed
sql = agent.generate_sql(
    "Create a query following the business rules in business_rules.txt"
)
```

### How It Works

When `context_folder` is set, the agent gains two additional tools:
1.  **`list_context_files()`**: Lists all files in the context folder.
2.  **`read_context_file(file_path)`**: Reads the content of a specific file.

The agent automatically uses these tools when your prompt mentions files or context.

### Example: Schema-Driven Development

```python
# schema.sql contains:
# CREATE TABLE customers (
#     id INT,
#     name VARCHAR(100),
#     email VARCHAR(100),
#     created_at TIMESTAMP
# )

agent = DremioAgent(context_folder="./schemas")

# Agent reads schema.sql and generates appropriate code
code = agent.generate_script(
    "Create a Python script to validate that the customers table matches the schema in schema.sql"
)
```

### Combining Memory and Context

```python
agent = DremioAgent(
    memory_path="./memory.db",
    context_folder="./project_docs"
)

session = "data_migration"

# Turn 1
agent.generate_script(
    "Read the source schema from source_schema.sql",
    session_id=session
)

# Turn 2 - Agent remembers the source schema from Turn 1
agent.generate_script(
    "Now generate a migration script to the target schema in target_schema.sql",
    session_id=session
)
```

## Best Practices

### Memory Persistence
- **Use descriptive session IDs**: `"user_123_project_alpha"` is better than `"session1"`.
- **Clean up old sessions**: Periodically delete the database or implement session expiration.
- **Don't share session IDs**: Each user or project should have unique session IDs.

### Context Folder
- **Keep files small**: Large files may exceed LLM context limits.
- **Use clear file names**: `customer_schema.sql` is better than `schema1.sql`.
- **Organize by topic**: Group related files in subdirectories.
- **Mention files explicitly**: "Use the schema in schema.sql" is clearer than "use the schema".

### Performance
- **Limit context folder size**: Too many files can slow down the agent.
- **Use memory sparingly**: Long conversation histories increase token usage.
- **Clear memory between projects**: Start fresh for unrelated work.


---

<!-- Source: docs/ai/api.md -->

---

## DremioFrame Cookbook

A collection of recipes for common data engineering tasks using valid Dremio SQL patterns.

## Deduplicating Data

Remove duplicate records based on specific columns, keeping the most recent one.

```python
# Keep the row with the latest 'updated_at' for each 'id'
df = client.table("source_table") \
    .select("*", 
            F.row_number().over(
                F.Window.partition_by("id").order_by("updated_at", ascending=False)
            ).alias("rn")
    ) \
    .filter("rn = 1") \
    .drop("rn")

# Save as new table
df.create("deduplicated_table")
```

## Pivoting Data

Transform rows into columns (e.g., monthly sales).

```python
# Source: region, month, sales
# Target: region, jan_sales, feb_sales, ...

df = client.table("monthly_sales") \
    .group_by("region") \
    .agg(
        jan_sales="SUM(CASE WHEN month = 'Jan' THEN sales ELSE 0 END)",
        feb_sales="SUM(CASE WHEN month = 'Feb' THEN sales ELSE 0 END)",
        mar_sales="SUM(CASE WHEN month = 'Mar' THEN sales ELSE 0 END)"
    )

df.show()
```

## Incremental Loading (Watermark)

Load only new data based on a watermark (max timestamp).

```python
# Get max timestamp from target
max_ts = client.table("target_table").agg(max_ts="MAX(updated_at)").collect().iloc[0]['max_ts']

# Fetch only new data from source
new_data = client.table("source_table").filter(f"updated_at > '{max_ts}'")

# Append to target
new_data.insert("target_table")
```

## Exporting to S3 (Parquet)

```python
# Option 1: Client-Side Export (Requires local credentials & s3fs)
# Fetches data to client and writes to S3
df = client.table("warehouse.sales").collect()
df.to_parquet("s3://my-bucket/export/data.parquet")

# Option 2: Materialize to Source (CTAS)
# Creates a new table (Iceberg or Parquet folder) in the S3 source
client.sql("""
    CREATE TABLE "s3_source"."bucket"."folder"."new_table"
    AS SELECT * FROM "warehouse"."sales"
""")
```

## Handling JSON Data

Access nested fields in JSON/Struct columns using dot notation.

```python
# Source has a 'details' column (Struct or Map): {"color": "red", "size": "M"}
df = client.table("products") \
    .select(
        "id",
        "name",
        F.col("details.color").alias("color"),
        F.col("details.size").alias("size")
    )

df.show()
```

## Unnesting Arrays (Flatten)

Explode a list column into multiple rows.

```python
# Source: id, tags (["A", "B"])
# Target: id, tag (one row per tag)

df = client.table("posts") \
    .select(
        "id",
        F.flatten("tags").alias("tag")
    )

df.show()
```

## Date Arithmetic

Perform calculations on dates.

```python
# Calculate deadline (created_at + 7 days) and days_overdue
df = client.table("tasks") \
    .select(
        "id",
        "created_at",
        F.date_add("created_at", 7).alias("deadline"),
        F.date_diff(F.current_date(), "created_at").alias("days_since_creation")
    )

df.show()
```

## String Manipulation

Clean and transform text data.

```python
# Normalize email addresses
df = client.table("users") \
    .select(
        "id",
        F.lower(F.trim("email")).alias("clean_email"),
        F.substr("phone", 1, 3).alias("area_code")
    )

df.show()
```

## Window Functions (Running Total)

Calculate cumulative sums or moving averages.

```python
# Calculate running total of sales by date
df = client.table("sales") \
    .select(
        "date",
        "amount",
        F.sum("amount").over(
            F.Window.order_by("date").rows_between("UNBOUNDED PRECEDING", "CURRENT ROW")
        ).alias("running_total")
    )

df.show()
```

## Approximate Count Distinct

Estimate the number of distinct values for large datasets (faster than COUNT DISTINCT).

```python
# Estimate unique visitors
df = client.table("web_logs") \
    .agg(
        unique_visitors=F.approx_distinct("visitor_id")
    )

df.show()
```

## AI Functions (Generative AI)

Use Dremio's AI functions to classify text or generate content.

```python
# Classify customer feedback
df = client.table("feedback") \
    .select(
        "comment",
        F.ai_classify("comment", ["Positive", "Negative", "Neutral"]).alias("sentiment")
    )

df.show()
```

## Time Travel (Snapshot Querying)

Query an Iceberg table as it existed at a specific point in time.

```python
# Query specific snapshot
df = client.table("iceberg_table").at_snapshot("1234567890")

# Query by timestamp
df = client.table("iceberg_table").at_timestamp("2023-10-27 10:00:00")

df.show()
```

## Schema Evolution

Add a new column to an existing Iceberg table.

```python
# Add 'status' column
client.sql('ALTER TABLE "iceberg_table" ADD COLUMNS (status VARCHAR)')
```

## Creating Partitioned Tables

Create a new table partitioned by specific columns for better performance.

```python
# Create table partitioned by 'region' and 'date'
client.sql("""
    CREATE TABLE "iceberg_source"."new_table"
    PARTITION BY (region, date)
    AS SELECT * FROM "source_table"
""")
```

## Map & Struct Access

Access values within Map and Struct data types.

```python
# Struct: details.color
# Map: properties['priority']

df = client.table("events") \
    .select(
        "id",
        F.col("details.color").alias("color"),
        F.col("properties['priority']").alias("priority")
    )

df.show()
```


---

<!-- Source: docs/getting_started/dependencies.md -->

---

## Troubleshooting Guide

Common issues and solutions when using DremioFrame.

## Connectivity Issues

### Arrow Flight: Connection Refused
**Error**: `pyarrow.lib.ArrowIOError: Flight returned unavailable error, with message: failed to connect to all addresses`
**Cause**: The client cannot reach the Dremio Flight endpoint.
**Solution**:
- Verify `hostname` and `port` (default 32010 for Software, 443 for Cloud).
- Ensure firewall allows traffic on the Flight port.
- If using Docker, ensure ports are mapped (`-p 32010:32010`).

### Authentication Failed
**Error**: `pyarrow.flight.FlightUnauthenticatedError`
**Cause**: Invalid credentials.
**Solution**:
- **Cloud**: Check `DREMIO_PAT` is valid and not expired.
- **Software**: Verify username/password.
- Ensure `DREMIO_PROJECT_ID` is set for Cloud.

## Orchestration Issues

### Backend Import Errors
**Error**: `ImportError: psycopg2 is required...`
**Cause**: Missing optional dependencies.
**Solution**:
- Install with extras: `pip install "dremioframe[postgres]"` or `pip install "dremioframe[mysql]"`.

### Task Execution Fails Immediately
**Cause**: Missing environment variables or configuration in the execution environment (e.g., inside a Docker container).
**Solution**:
- Pass environment variables to the container or worker process.

## Debugging

Enable debug logging to see detailed request/response info:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will output REST API calls and Flight connection details.


---

<!-- Source: docs/getting_started/tutorial_etl.md -->