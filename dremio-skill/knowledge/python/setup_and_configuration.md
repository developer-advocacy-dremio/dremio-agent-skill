# Setup And Configuration

## Configuration Reference

This guide details all configuration options for DremioFrame, including environment variables and client arguments.

## Quick Start Examples

### Dremio Cloud
```python
from dremioframe.client import DremioClient

# Simplest - uses environment variables DREMIO_PAT and DREMIO_PROJECT_ID
client = DremioClient()

# Or specify explicitly
client = DremioClient(
    pat="your_pat_here",
    project_id="your_project_id",
    mode="cloud"  # Optional, auto-detected
)
```

### Dremio Software v26+
```python
# With PAT (recommended for v26+)
client = DremioClient(
    hostname="v26.dremio.org",
    pat="your_pat_here",
    tls=True,
    mode="v26"  # Automatically sets correct ports
)

# With username/password
client = DremioClient(
    hostname="localhost",
    username="admin",
    password="password123",
    tls=False,
    mode="v26"
)
```

### Dremio Software v25
```python
client = DremioClient(
    hostname="localhost",
    username="admin",
    password="password123",
    mode="v25"  # Uses v25-specific endpoints
)
```

## Environment Variables

### Dremio Cloud Connection
| Variable | Description | Required |
|----------|-------------|----------|
| `DREMIO_PAT` | Personal Access Token for authentication. | Yes (for Cloud) |
| `DREMIO_PROJECT_ID` | Project ID of the Dremio Cloud project. | Yes (for Cloud) |

### Dremio Software Connection
| Variable | Description | Default |
|----------|-------------|---------|
| `DREMIO_SOFTWARE_HOST` | Hostname or URL of the Dremio coordinator. | `localhost` |
| `DREMIO_SOFTWARE_PAT` | Personal Access Token (v26+ only). | - |
| `DREMIO_SOFTWARE_USER` | Username (optional for v26+ with PAT, required for v25). | - |
| `DREMIO_SOFTWARE_PORT` | REST API port (optional, auto-detected). | `443` (TLS) or `9047` |
| `DREMIO_SOFTWARE_FLIGHT_PORT` | Arrow Flight port (optional, auto-detected). | `32010` |
| `DREMIO_SOFTWARE_PASSWORD` | Password for authentication. | - |
| `DREMIO_SOFTWARE_TLS` | Enable TLS (`true`/`false`). | `false` |
| `DREMIO_ICEBERG_URI` | Iceberg Catalog REST URI (Required for Software). | `https://catalog.dremio.cloud/api/iceberg` (Cloud default) |

### Orchestration Backend
| Variable | Description | Example |
|----------|-------------|---------|
| `DREMIOFRAME_PG_DSN` | PostgreSQL connection string. | `postgresql://user:pass@host/db` |
| `DREMIOFRAME_MYSQL_USER` | MySQL username. | `root` |
| `DREMIOFRAME_MYSQL_PASSWORD` | MySQL password. | `password` |
| `DREMIOFRAME_MYSQL_HOST` | MySQL host. | `localhost` |
| `DREMIOFRAME_MYSQL_DB` | MySQL database name. | `dremioframe` |
| `DREMIOFRAME_MYSQL_PORT` | MySQL port. | `3306` |

### Celery Executor
| Variable | Description | Default |
|----------|-------------|---------|
| `CELERY_BROKER_URL` | Broker URL for Celery (Redis/RabbitMQ). | `redis://localhost:6379/0` |
| `CELERY_RESULT_BACKEND` | Backend for Celery results. | `redis://localhost:6379/0` |

### AWS / S3 Task
| Variable | Description |
|----------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS Access Key. |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Key. |
| `AWS_DEFAULT_REGION` | AWS Region (e.g., `us-east-1`). |

## DremioClient Arguments

When initializing `DremioClient`, you can pass arguments directly or rely on environment variables.

```python
class DremioClient:
    def __init__(
        self,
        # Authentication
        pat: str = None,                    # Personal Access Token (Cloud or Software v26+)
        username: str = None,               # Username (Software with user/pass auth)
        password: str = None,               # Password (Software with user/pass auth)
        project_id: str = None,             # Project ID (Cloud only)
        
        # Connection Mode
        mode: str = None,                   # 'cloud', 'v26', or 'v25' (auto-detected if None)
        
        # Endpoints
        hostname: str = "data.dremio.cloud", # Dremio hostname
        port: int = None,                   # REST API port (auto-detected based on mode)
        base_url: str = None,               # Custom base URL (overrides auto-detection)
        
        # Arrow Flight
        flight_port: int = None,            # Arrow Flight port (auto-detected based on mode)
        flight_endpoint: str = None,        # Arrow Flight endpoint (defaults to hostname)
        
        # Security
        tls: bool = True,                   # Enable TLS/SSL
        disable_certificate_verification: bool = False  # Disable SSL cert verification
    ):
        ...
```

## Connection Mode Details

The `mode` parameter automatically configures ports and endpoints for different Dremio versions:

### `mode="cloud"` (Default)
- **REST API**: `https://api.dremio.cloud/v0` (port 443)
- **Arrow Flight**: `grpc+tls://data.dremio.cloud:443`
- **Authentication**: PAT with Bearer token
- **Auto-detected when**: `hostname == "data.dremio.cloud"` or `project_id` is set

### `mode="v26"` (Dremio Software v26+)
- **REST API**: `https://{hostname}:{port}/api/v3` (port 443 with TLS, 9047 without)
- **Arrow Flight**: `grpc+tls://{hostname}:32010` (or `grpc+tcp` without TLS)
- **Authentication**: PAT with Bearer token or username/password
- **Auto-detected when**: `DREMIO_SOFTWARE_HOST` or `DREMIO_SOFTWARE_PAT` env vars are set

### `mode="v25"` (Dremio Software v25 and earlier)
- **REST API**: `http://{hostname}:9047/api/v3`
- **Arrow Flight**: `grpc+tcp://{hostname}:32010`
- **Authentication**: Username/password only
- **Login Endpoint**: `/apiv2/login`

## Port Configuration

Ports are automatically configured based on the `mode`, but can be overridden:

| Mode | REST Port (default) | Flight Port (default) |
|------|---------------------|----------------------|
| `cloud` | 443 | 443 |
| `v26` (TLS) | 443 | 32010 |
| `v26` (no TLS) | 9047 | 32010 |
| `v25` | 9047 | 32010 |

**Override examples:**
```python
# Custom REST API port
client = DremioClient(hostname="custom.dremio.com", port=8443, mode="v26")

# Custom Flight port
client = DremioClient(hostname="custom.dremio.com", flight_port=31010, mode="v26")
```

## Example .env File

### For Dremio Cloud
```bash
DREMIO_PAT=your_cloud_pat_here
DREMIO_PROJECT_ID=your_project_id_here
```

### For Dremio Software v26+
```bash
DREMIO_SOFTWARE_HOST=https://v26.dremio.org
DREMIO_SOFTWARE_PAT=your_software_pat_here
DREMIO_SOFTWARE_TLS=true
# Optional: Override default ports
# DREMIO_SOFTWARE_PORT=443
# DREMIO_SOFTWARE_FLIGHT_PORT=32010
```

### For Dremio Software v25
```bash
DREMIO_SOFTWARE_HOST=localhost
DREMIO_SOFTWARE_USER=admin
DREMIO_SOFTWARE_PASSWORD=password123
DREMIO_SOFTWARE_TLS=false
```

## Troubleshooting

### Connection Issues

**Problem**: "Connection timeout" or "Connection refused"
- **Solution**: Verify the hostname and ports are correct. For Software, ensure the Dremio coordinator is running.

**Problem**: "Authentication failed"
- **Solution**: 
  - For Cloud: Verify your PAT and Project ID are correct
  - For Software v26+: Ensure your PAT has the necessary permissions
  - For Software v25: Verify username/password are correct

**Problem**: "Flight queries fail but REST API works"
- **Solution**: Check that the `flight_port` is correct (default: 32010 for Software). Verify Arrow Flight is enabled on your Dremio instance.

### Mode Selection

If auto-detection isn't working correctly, explicitly set the `mode` parameter:

```python
# Force v26 mode
client = DremioClient(hostname="my-dremio.com", pat="...", mode="v26")

# Force cloud mode
client = DremioClient(pat="...", project_id="...", mode="cloud")
```


---

<!-- Source: docs/getting_started/connection.md -->

---

## Connecting to Dremio

This guide provides detailed instructions on how to connect `dremioframe` to your Dremio environment, whether it's Dremio Cloud or a self-managed Dremio Software instance.

## Overview

DremioFrame supports three connection modes:
- **`cloud`**: Dremio Cloud (SaaS)
- **`v26`**: Dremio Software v26+ (with PAT support)
- **`v25`**: Dremio Software v25 and earlier

The `mode` parameter automatically configures ports, endpoints, and authentication methods. In most cases, the mode is auto-detected, but you can specify it explicitly for clarity.

---

## 1. Dremio Cloud

Dremio Cloud is the default connection mode. It uses Arrow Flight SQL over TLS.

### Prerequisites
- **Personal Access Token (PAT)**: Generate this in your Dremio Cloud User Settings
- **Project ID**: The ID of the project you want to query

### Environment Variables

Set these in your `.env` file or environment:

```bash
DREMIO_PAT=your_cloud_personal_access_token
DREMIO_PROJECT_ID=your_project_id_here
```

### Connection Examples

#### Using Environment Variables (Recommended)

```python
from dremioframe.client import DremioClient

# Client automatically picks up env vars and detects Cloud mode
client = DremioClient()

# Or explicitly specify mode for clarity
client = DremioClient(mode="cloud")
```

#### Using Explicit Parameters

```python
client = DremioClient(
    pat="your_pat_here",
    project_id="your_project_id_here",
    mode="cloud"  # Optional, auto-detected when project_id is provided
)
```

### Custom Flight Configuration

You can specify a custom Flight endpoint if needed:

```python
client = DremioClient(
    pat="my_token",
    project_id="my_project",
    flight_endpoint="flight.dremio.cloud",
    flight_port=443,
    mode="cloud"
)
```

### Default Ports (Cloud)
- **REST API**: Port 443 (`https://api.dremio.cloud/v0`)
- **Arrow Flight**: Port 443 (`grpc+tls://data.dremio.cloud:443`)

---

## 2. Dremio Software v26+

Dremio Software v26+ supports Personal Access Tokens (PAT) for authentication, similar to Cloud.

### Prerequisites
- **Hostname**: The address of your Dremio coordinator (e.g., `v26.dremio.org` or `localhost`)
- **Personal Access Token (PAT)** OR **Username/Password**
- **TLS**: Whether your instance uses TLS/SSL

### Environment Variables

Set these in your `.env` file:

```bash
DREMIO_SOFTWARE_HOST=https://v26.dremio.org
DREMIO_SOFTWARE_PAT=your_software_personal_access_token
DREMIO_SOFTWARE_TLS=true

# Optional: Override default ports
# DREMIO_SOFTWARE_PORT=443
# DREMIO_SOFTWARE_FLIGHT_PORT=32010
```

**Note**: `DREMIO_SOFTWARE_HOST` can include the protocol (`https://` or `http://`). If TLS is true and no port is specified in the URL, port 443 is used for REST API.

> **Important**: For Arrow Flight connections in v26+, the client uses Basic Authentication (Username + PAT). If you only provide a PAT, the client will attempt to automatically discover your username from the catalog. If discovery fails, you may need to provide `DREMIO_SOFTWARE_USER` explicitly.

### Connection Examples

#### Using PAT with Environment Variables (Recommended)

```python
from dremioframe.client import DremioClient

# Auto-detects v26 mode from DREMIO_SOFTWARE_* env vars
client = DremioClient()

# Or explicitly specify mode
client = DremioClient(mode="v26")
```

#### Using PAT with Explicit Parameters

```python
client = DremioClient(
    hostname="v26.dremio.org",
    pat="your_pat_here",
    tls=True,
    mode="v26"
)
```

#### Using Username/Password

```python
client = DremioClient(
    hostname="localhost",
    username="admin",
    password="password123",
    tls=False,
    mode="v26"
)
```

### Default Ports (v26)
- **REST API**: Port 443 (with TLS) or 9047 (without TLS)
- **Arrow Flight**: Port 32010
- **Login Endpoint**: `/api/v3/login` or `/apiv3/login`

### TLS/SSL Configuration

If your Dremio Software cluster uses TLS (Encryption), set `tls=True`:

```python
client = DremioClient(
    hostname="secure.dremio.com",
    pat="your_pat",
    tls=True,
    mode="v26"
)
```

#### Self-Signed Certificates

For self-signed certificates (common in dev/test environments):

```python
client = DremioClient(
    hostname="localhost",
    username="admin",
    password="password123",
    tls=True,
    disable_certificate_verification=True,
    mode="v26"
)
```

> **Warning**: Disabling certificate verification is insecure and should not be used in production.

---

## 3. Dremio Software v25 and Earlier

Dremio Software v25 and earlier versions use username/password authentication only (no PAT support).

### Prerequisites
- **Hostname**: The address of your Dremio coordinator
- **Username and Password**: Valid Dremio credentials

### Environment Variables

Set these in your `.env` file:

```bash
DREMIO_SOFTWARE_HOST=localhost
DREMIO_SOFTWARE_USER=admin
DREMIO_SOFTWARE_PASSWORD=password123
DREMIO_SOFTWARE_TLS=false

# Optional: Override default ports
# DREMIO_SOFTWARE_PORT=9047
# DREMIO_SOFTWARE_FLIGHT_PORT=32010
```

### Connection Examples

#### Using Environment Variables

```python
from dremioframe.client import DremioClient

client = DremioClient(mode="v25")
```

#### Using Explicit Parameters

```python
client = DremioClient(
    hostname="localhost",
    username="admin",
    password="password123",
    tls=False,
    mode="v25"
)
```

### Default Ports (v25)
- **REST API**: Port 9047 (`http://localhost:9047/api/v3`)
- **Arrow Flight**: Port 32010
- **Login Endpoint**: `/apiv2/login`

---

## 4. Port Configuration Reference

Ports are automatically configured based on the `mode`, but can be overridden:

| Mode | REST Port (default) | Flight Port (default) | Protocol |
|------|---------------------|----------------------|----------|
| `cloud` | 443 | 443 | HTTPS/gRPC+TLS |
| `v26` (TLS) | 443 | 32010 | HTTPS/gRPC+TLS |
| `v26` (no TLS) | 9047 | 32010 | HTTP/gRPC+TCP |
| `v25` | 9047 | 32010 | HTTP/gRPC+TCP |

### Overriding Ports

```python
# Custom REST API port
client = DremioClient(
    hostname="custom.dremio.com",
    port=8443,
    flight_port=31010,
    mode="v26"
)
```

---

## 5. Mode Auto-Detection

The client automatically detects the mode based on:

1. **Cloud mode** is detected when:
   - `hostname == "data.dremio.cloud"`, OR
   - `project_id` is provided, OR
   - `DREMIO_PROJECT_ID` environment variable is set

2. **v26 mode** is detected when:
   - `DREMIO_SOFTWARE_HOST` or `DREMIO_SOFTWARE_PAT` environment variables are set

3. **Default**: Falls back to `cloud` mode if no indicators are found

### Explicit Mode Selection

For clarity and to avoid ambiguity, you can always specify the mode explicitly:

```python
# Force v26 mode
client = DremioClient(
    hostname="my-dremio.com",
    pat="...",
    mode="v26"
)

# Force cloud mode
client = DremioClient(
    pat="...",
    project_id="...",
    mode="cloud"
)

# Force v25 mode
client = DremioClient(
    hostname="localhost",
    username="admin",
    password="password",
    mode="v25"
)
```

---

## 6. Complete .env File Examples

### For Dremio Cloud

```bash
# Required
DREMIO_PAT=dremio_pat_abc123xyz456...
DREMIO_PROJECT_ID=12345678-1234-1234-1234-123456789abc

# Optional
# DREMIO_FLIGHT_ENDPOINT=data.dremio.cloud
# DREMIO_FLIGHT_PORT=443
```

### For Dremio Software v26+ (with PAT)

```bash
# Required
DREMIO_SOFTWARE_HOST=https://v26.dremio.org
DREMIO_SOFTWARE_PAT=dremio_pat_xyz789...
DREMIO_SOFTWARE_TLS=true

# Optional
# DREMIO_SOFTWARE_PORT=443
# DREMIO_SOFTWARE_FLIGHT_PORT=32010
```

### For Dremio Software v26+ (with Username/Password)

```bash
# Required
DREMIO_SOFTWARE_HOST=localhost
DREMIO_SOFTWARE_USER=admin
DREMIO_SOFTWARE_PASSWORD=password123
DREMIO_SOFTWARE_TLS=false

# Optional
# DREMIO_SOFTWARE_PORT=9047
# DREMIO_SOFTWARE_FLIGHT_PORT=32010
```

### For Dremio Software v25

```bash
# Required
DREMIO_SOFTWARE_HOST=localhost
DREMIO_SOFTWARE_USER=admin
DREMIO_SOFTWARE_PASSWORD=password123
DREMIO_SOFTWARE_TLS=false

# Optional
# DREMIO_SOFTWARE_PORT=9047
# DREMIO_SOFTWARE_FLIGHT_PORT=32010
```

---

## 7. Troubleshooting & Common Errors

### `FlightUnavailableError` / Connection Refused

**Symptoms**: The client hangs or raises an error saying the service is unavailable.

**Causes**:
- **Wrong Port**: Ensure you are using the **Arrow Flight Port** (default `32010` for Software, `443` for Cloud), NOT the UI port (`9047`) or ODBC/JDBC port (`31010`)
- **Firewall**: Ensure the port is open and accessible
- **Dremio Down**: Check if the Dremio service is running
- **Wrong Mode**: Ensure you're using the correct mode (`cloud`, `v26`, or `v25`)

**Solution**:
```python
# Verify your mode and ports
client = DremioClient(
    hostname="your-host",
    mode="v26",  # Explicitly set mode
    flight_port=32010  # Explicitly set Flight port if needed
)
```

### `FlightUnauthenticatedError` / Auth Failed

**Symptoms**: "Invalid credentials" or "Unauthenticated".

**Causes**:
- **Expired PAT**: Tokens expire. Generate a new one
- **Wrong Project ID**: For Cloud, ensure the Project ID matches
- **Wrong Mode**: Using Cloud credentials with Software mode or vice versa
- **Typo**: Double-check credentials

**Solution**:
```python
# For Cloud, ensure both PAT and project_id are correct
client = DremioClient(pat="...", project_id="...", mode="cloud")

# For Software v26+, ensure PAT is valid
client = DremioClient(hostname="...", pat="...", mode="v26")

# For Software v25, use username/password
client = DremioClient(hostname="...", username="...", password="...", mode="v25")
```

### `FlightInternalError` (Certificate Issues)

**Symptoms**: "Handshake failed", "Certificate verify failed".

**Causes**:
- **TLS Mismatch**: You set `tls=True` but the server uses `tls=False` (or vice versa)
- **Self-Signed Cert**: Connecting to TLS-enabled server with self-signed certificate

**Solution**:
```python
# For self-signed certificates
client = DremioClient(
    hostname="localhost",
    tls=True,
    disable_certificate_verification=True,
    mode="v26"
)
```

### Environment Variable Conflicts

**Symptoms**: Client connects to wrong environment or uses wrong credentials.

**Causes**:
- Both `DREMIO_PAT` and `DREMIO_SOFTWARE_PAT` are set
- Both Cloud and Software environment variables are set

**Solution**:
```python
# Explicitly specify mode to avoid ambiguity
client = DremioClient(mode="v26")  # Forces Software mode

# Or unset conflicting environment variables
import os
if "DREMIO_PROJECT_ID" in os.environ:
    del os.environ["DREMIO_PROJECT_ID"]
```

---

## 8. Testing Connectivity

Verify your connection with a simple test:

```python
from dremioframe.client import DremioClient

try:
    # Create client (adjust mode as needed)
    client = DremioClient(mode="v26")
    
    # Test catalog access
    catalog = client.catalog.list_catalog()
    print(f"✅ Connected successfully! Found {len(catalog)} catalog items.")
    
    # Test query execution (requires Arrow Flight)
    result = client.query("SELECT 1 as test")
    print(f"✅ Query execution successful!")
    print(result)
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    import traceback
    traceback.print_exc()
```

### Quick Diagnostic Script

```python
from dremioframe.client import DremioClient
import os

print("Environment Variables:")
print(f"  DREMIO_PAT: {'SET' if os.getenv('DREMIO_PAT') else 'NOT SET'}")
print(f"  DREMIO_PROJECT_ID: {'SET' if os.getenv('DREMIO_PROJECT_ID') else 'NOT SET'}")
print(f"  DREMIO_SOFTWARE_HOST: {os.getenv('DREMIO_SOFTWARE_HOST', 'NOT SET')}")
print(f"  DREMIO_SOFTWARE_PAT: {'SET' if os.getenv('DREMIO_SOFTWARE_PAT') else 'NOT SET'}")
print(f"  DREMIO_SOFTWARE_USER: {os.getenv('DREMIO_SOFTWARE_USER', 'NOT SET')}")

client = DremioClient(mode="v26")  # Adjust mode as needed
print(f"\nClient Configuration:")
print(f"  Mode: {client.mode}")
print(f"  Hostname: {client.hostname}")
print(f"  REST Port: {client.port}")
print(f"  Flight Port: {client.flight_port}")
print(f"  Base URL: {client.base_url}")
print(f"  Project ID: {client.project_id}")
```


---

<!-- Source: docs/getting_started/cookbook.md -->

---

## Create a pool with 5 connections
pool = ConnectionPool(
    max_size=5,
    timeout=30,
    # DremioClient arguments
    pat="YOUR_PAT",
    project_id="YOUR_PROJECT_ID"
)
```

### Using the Context Manager

The recommended way to use the pool is via the context manager, which ensures connections are returned to the pool even if errors occur.

```python
with pool.client() as client:
    # Use client as normal
    df = client.sql("SELECT * FROM sys.version").collect()
    print(df)
```

### Manual Management

You can also manually get and release clients.

```python
try:
    client = pool.get_client()
    # Use client...
finally:
    pool.release_client(client)
```

### Configuration

- **max_size**: Maximum number of connections to create.
- **timeout**: Seconds to wait for a connection if the pool is empty and at max size. Raises `TimeoutError` if exceeded.
- **client_kwargs**: Arguments passed to `DremioClient` constructor (e.g., `pat`, `username`, `password`, `flight_endpoint`).


---

<!-- Source: docs/performance/cost_estimation.md -->

# Query Cost Estimation

DremioFrame provides a `CostEstimator` to analyze query execution plans, estimate costs, and suggest optimizations before running expensive queries.

## CostEstimator

The `CostEstimator` uses Dremio's `EXPLAIN PLAN` to analyze queries and provide actionable insights.

### Initialization

```python
from dremioframe.client import DremioClient
from dremioframe.cost_estimator import CostEstimator

client = DremioClient()
estimator = CostEstimator(client)
```

### Estimating Query Cost

Get a detailed cost estimate for any query:

```python
sql = """
SELECT customer_id, SUM(amount) as total
FROM sales.transactions
WHERE date >= '2024-01-01'
GROUP BY customer_id
"""

estimate = estimator.estimate_query_cost(sql)

print(f"Estimated rows: {estimate.estimated_rows}")
print(f"Total cost: {estimate.total_cost}")
print(f"Plan summary: {estimate.plan_summary}")
print(f"Optimization hints: {estimate.optimization_hints}")
```

**Output**:
```
Estimated rows: 50000
Total cost: 125.5
Plan summary: Query plan includes: 1 table scan(s), aggregation, 1 filter(s)
Optimization hints: ['Consider adding LIMIT for large tables']
```

### Cost Estimate Details

The `CostEstimate` object includes:
- **estimated_rows**: Number of rows expected to be processed
- **estimated_bytes**: Approximate data size
- **scan_cost**: Cost of table scans
- **join_cost**: Cost of join operations
- **total_cost**: Overall query cost metric
- **plan_summary**: Human-readable plan description
- **optimization_hints**: List of suggestions

### Optimization Hints

The estimator automatically detects common anti-patterns:

```python
hints = estimator.get_optimization_hints(sql)

for hint in hints:
    print(f"{hint.severity}: {hint.message}")
    print(f"  Suggestion: {hint.suggestion}")
```

**Common hints**:
- **SELECT \***: Suggests specifying only needed columns
- **Missing WHERE**: Warns about full table scans
- **Multiple JOINs**: Suggests using CTEs for readability
- **ORDER BY without LIMIT**: Recommends adding LIMIT
- **DISTINCT usage**: Suggests alternatives like GROUP BY

### Comparing Query Variations

Compare multiple approaches to find the most efficient:

```python
result = estimator.compare_queries(
    # Approach 1: Subquery
    """
    SELECT * FROM (
        SELECT customer_id, amount FROM sales.transactions
    ) WHERE amount > 1000
    """,
    
    # Approach 2: Direct filter
    """
    SELECT customer_id, amount 
    FROM sales.transactions 
    WHERE amount > 1000
    """
)

print(result['recommendation'])

---

## Optional Dependencies

DremioFrame uses optional dependencies to keep the core package lightweight.

## Server
- **`server`**: `mcp` (Required for running the MCP Server)

## AI
with a core set of dependencies. However, many advanced features require additional packages. You can install these optional dependencies individually or in groups.

## Installation Syntax

To install optional dependencies, use the square bracket syntax with pip:

```bash
pip install "dremioframe[group_name]"
```

To install multiple groups:

```bash
pip install "dremioframe[group1,group2]"
```

## Dependency Groups

### Core Features

| Group | Dependencies | Features Enabled |
| :--- | :--- | :--- |
| `cli` | `rich`, `prompt_toolkit` | Enhanced CLI experience with rich text and interactive prompts for working with Orchestration and AI features. |
| `s3` | `boto3` | S3 integration for direct file operations and source management. |
| `scheduler` | `apscheduler` | Built-in task scheduling capabilities. |
| `dq` | `pyyaml` | Data Quality framework configuration parsing. |
| `ai` | `langchain`, `langchain-openai`, `langchain-anthropic`, `langchain-google-genai` | AI-powered Agent for Generating Python Scripts, SQL and cURL commands and light admin work. |
| `mcp` | `langchain-mcp-adapters` | Model Context Protocol server integration for extending AI agent with custom tools. |
| `document` | `pdfplumber` | PDF document extraction for AI agent to read and extract data from PDF files. |
**note:** this libraries embdedded agent is primarily meant as a code generation assist tool, not meant as an alternative to the integrated Dremio agent for deeper administration and natural language analytics.

### File Formats & Export

| Group | Dependencies | Features Enabled |
| :--- | :--- | :--- |
| `excel` | `openpyxl` | Reading and writing Excel files. |
| `html` | `lxml`, `html5lib` | Parsing HTML tables. |
| `avro` | `fastavro` | Support for Avro file format. |
| `lance` | `pylance` | Support for Lance file format. |
| `image_export` | `kaleido` | Exporting Plotly charts as static images (PNG, JPG, PDF). |

### Data Ingestion

| Group | Dependencies | Features Enabled |
| :--- | :--- | :--- |
| `ingest` | `dlt` | Load data from 100+ sources (APIs, SaaS, databases) using dlt integration. |
| `database` | `connectorx`, `sqlalchemy` | High-performance SQL database ingestion (Postgres, MySQL, SQLite, etc.). |
| `notebook` | `tqdm`, `ipywidgets` | For Jupyter notebook integration. |
| `delta` | `deltalake` | For Delta Lake export. |
| `lineage` | `networkx`, `graphviz` | For data lineage visualization. |

### External Backends

| Group | Dependencies | Features Enabled |
| :--- | :--- | :--- |
| `postgres` | `psycopg2-binary` | Support for using PostgreSQL as an orchestration backend. |
| `mysql` | `mysql-connector-python` | Support for using MySQL as an orchestration backend. |
| `celery` | `celery`, `redis` | Distributed task execution using Celery and Redis. |
| `airflow` | `apache-airflow` | Integration with Apache Airflow for orchestrating Dremio workflows. |

### Development & Documentation

| Group | Dependencies | Features Enabled |
| :--- | :--- | :--- |
| `dev` | `pytest`, `pytest-asyncio`, `requests-mock` | Running the test suite and contributing to DremioFrame. |
| `docs` | `mkdocs`, `mkdocs-material`, `mkdocstrings[python]` | Building and serving the documentation locally. |

## Feature-Specific Requirements

### Orchestration
- **Local Execution**: No extra dependencies required.
- **Distributed Execution**: Requires `celery`.
- **Persistent State**: Requires a backend like `postgres` or `mysql` (or uses local SQLite by default).

### AI Functions
To use the AI agent for script/SQL generation, you must install the `ai` group:
```bash
pip install "dremioframe[ai]"
```

This includes support for:
- Script, SQL, and API call generation
- Conversation memory persistence (via SQLite)
- Context folder integration for project-specific files

### Chart Exporting
To save charts as images using `chart.save("plot.png")`, you need the `image_export` group:
```bash
pip install "dremioframe[image_export]"
```


---

<!-- Source: docs/getting_started/s3_integration.md -->

---

## Python SDK Setup & Quickstart

## 📦 Installation

To use DremioFrame, install it via pip:

```bash
pip install dremioframe
```

*Note: Requires Python 3.8 or higher.*

## 🚀 Quick Start

```python
from dremioframe.client import DremioClient

# Authenticate using an environment variable (Recommended)
# export DREMIO_PAT="your-token"
client = DremioClient(endpoint="https://api.dremio.cloud")

print(client.catalog.list_catalog())
```

DremioFrame provides tools for managing your Dremio environment, including sources, folders, users, grants, and security policies.

## Catalog Management

Access via `client.catalog`.

### Sources

```python
# Create a new S3 source
config = {
    "accessKey": "...",
    "accessSecret": "...",
    "bucketName": "my-bucket"
}
client.catalog.create_source("my_s3", "S3", config)

# Delete a source
source_id = client.catalog.get_entity_by_path("my_s3")['id']
client.catalog.delete_catalog_item(source_id)
```

### Folders

```python
# Create a folder
client.catalog.create_folder(["space_name", "folder_name"])
```

## User & Security Management

Access via `client.admin`.

### Users

```python
# Create a user
client.admin.create_user("new_user", "password123")

# Change password
client.admin.alter_user_password("new_user", "new_password456")

# Delete user
client.admin.drop_user("new_user")
```

### Grants (RBAC)

Manage permissions for users and roles.

```python
# Grant SELECT on a table to a role
client.admin.grant("SELECT", "TABLE marketing.sales", to_role="DATA_ANALYST")

# Grant all privileges on a space to a user
client.admin.grant("ALL PRIVILEGES", "SPACE marketing", to_user="john.doe")

# Revoke privileges
client.admin.revoke("SELECT", "TABLE marketing.sales", from_role="DATA_ANALYST")
```

### Masking Policies

Column masking allows you to obscure sensitive data based on user roles.

1. **Create a Policy Function** (UDF)

```python
# Create a function that masks SSN for non-admins
client.admin.create_policy_function(
    name="mask_ssn",
    args="ssn VARCHAR",
    return_type="VARCHAR",
    body="CASE WHEN is_member('admin') THEN ssn ELSE '***-**-****' END"
)
```

2. **Apply Policy**

```python
# Apply to the 'ssn' column of 'employees' table
client.admin.apply_masking_policy("employees", "ssn", "mask_ssn(ssn)")
```

3. **Drop Policy**

```python
client.admin.drop_masking_policy("employees", "ssn")
```

### Source Management

Manage data sources (S3, Nessie, Postgres, etc.).

### List Sources

```python
sources = client.admin.list_sources()
```

### Get Source

```python
source = client.admin.get_source("my_source")
```

### Create Source

```python
# Generic
client.admin.create_source(
    name="my_postgres",
    type="POSTGRES",
    config={"hostname": "...", "username": "..."}
)

# S3 Helper
client.admin.create_source_s3(
    name="my_datalake",
    bucket_name="my-bucket",
    access_key="...",
    secret_key="..."
)
```

### Delete Source

```python
client.admin.delete_source("source_id")
```

## Reflection Management

You can manage Dremio reflections (Raw and Aggregation) using the `admin` interface.

```python
# List all reflections
reflections = client.admin.list_reflections()

# Create a Raw Reflection
client.admin.create_reflection(
    dataset_id="dataset-uuid",
    name="my_raw_reflection",
    type="RAW",
    display_fields=["col1", "col2"],
    distribution_fields=["col1"],
    partition_fields=["col2"],
    sort_fields=["col1"]
)

# Create an Aggregation Reflection
client.admin.create_reflection(
    dataset_id="dataset-uuid",
    name="my_agg_reflection",
    type="AGGREGATION",
    dimension_fields=["dim1", "dim2"],
    measure_fields=["measure1"],
    distribution_fields=["dim1"]
)

# Enable/Disable Reflection
client.admin.enable_reflection("reflection-id")
client.admin.disable_reflection("reflection-id")

# Delete Reflection
client.admin.delete_reflection("reflection-id")
```

## Row Access Policies

Row access policies filter rows based on user roles.

1. **Create a Policy Function**

```python
# Create a function that returns TRUE if user can see the row
client.admin.create_policy_function(
    name="region_filter",
    args="region VARCHAR",
    return_type="BOOLEAN",
    body="is_member('admin') OR is_member(region)"
)
```

2. **Apply Policy**

```python
# Apply to 'sales' table
client.admin.apply_row_access_policy("sales", "region_filter(region)")
```

3. **Drop Policy**

```python
client.admin.drop_row_access_policy("sales")
```


---

<!-- Source: docs/admin_governance/batch_operations.md -->