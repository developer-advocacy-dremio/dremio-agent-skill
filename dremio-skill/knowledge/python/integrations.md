# Integrations


---

## dlt Integration

DremioFrame integrates with [dlt (Data Load Tool)](https://dlthub.com/) to allow you to easily ingest data from hundreds of sources (APIs, Databases, SaaS applications) directly into Dremio.

## Installation

To use the `dlt` integration, you must install the optional dependencies:

```bash
pip install dremioframe[ingest]
```

## Usage

The integration is exposed via `client.ingest.dlt()`. It accepts any `dlt` source or resource and loads it into a Dremio table.

### Example: Loading from an API

```python
import dlt
from dremioframe.client import DremioClient

# 1. Initialize Client
client = DremioClient()

# 2. Define a dlt resource (e.g., fetching from an API)
@dlt.resource(name="pokemon")
def get_pokemon():
    import requests
    url = "https://pokeapi.co/api/v2/pokemon?limit=10"
    response = requests.get(url).json()
    yield from response["results"]

# 3. Ingest into Dremio
# This will create (or replace) the table "space.folder.pokemon"
client.ingest.dlt(
    source=get_pokemon(),
    table_name='"my_space"."my_folder"."pokemon"',
    write_disposition="replace"
)
```

### Parameters

- **source**: A `dlt` source or resource object.
- **table_name**: The target table name in Dremio (e.g., `"Space"."Folder"."Table"`).
- **write_disposition**:
    - `"replace"`: Drop table if exists and create new.
    - `"append"`: Append data to existing table.
- **batch_size**: Number of records to process per batch (default: 10,000).

## Supported Sources

Since DremioFrame accepts standard `dlt` sources, you can use any of the [verified sources](https://dlthub.com/docs/dlt-ecosystem/verified-sources/) from the dlt Hub, including:

- Salesforce
- HubSpot
- Google Sheets
- Notion
- Stripe
- And many more...


---

<!-- Source: docs/data_engineering/export.md -->

---

## Notebook Integration

DremioFrame provides rich integration with Jupyter Notebooks and other interactive environments (VS Code, Colab), making it an excellent tool for data exploration and analysis.

## Features

- **Rich DataFrame Display**: Automatically displays query results as formatted HTML tables.
- **Progress Bars**: Shows download progress for large datasets using `tqdm`.
- **Magic Commands**: IPython magic commands for quick SQL execution.

## Installation

Ensure you have the notebook dependencies installed:

```bash
pip install dremioframe[notebook]
```

## Rich Display

When you display a `DremioBuilder` object in a notebook, it automatically executes a preview query (LIMIT 20) and displays the results as a formatted HTML table, along with the generated SQL.

```python
from dremioframe.client import DremioClient

client = DremioClient()
df = client.table("finance.bronze.trips")

# Displaying the builder object shows a preview
df
```

## Progress Bars

When collecting large datasets, you can enable a progress bar to track the download status.

```python
# Download with progress bar
pdf = df.collect(library='pandas', progress_bar=True)
```

## Magic Commands

DremioFrame includes IPython magic commands to simplify your workflow.

### Loading Magics

First, load the extension:

```python
%load_ext dremioframe.notebook
```

### Connecting

Connect to Dremio using `%dremio_connect`. You can pass arguments or rely on environment variables.

```python
%dremio_connect pat=YOUR_PAT project_id=YOUR_PROJECT_ID
```

### Executing SQL

Use `%%dremio_sql` to execute SQL queries directly in a cell.

```sql
%%dremio_sql my_result
SELECT 
    trip_date,
    passenger_count
FROM finance.bronze.trips
WHERE passenger_count > 2
LIMIT 100
```

The result is automatically displayed and saved to the variable `my_result` (if specified).


---

<!-- Source: docs/modeling/dimensional.md -->

---

## Pydantic Integration

DremioFrame integrates with Pydantic to allow for schema validation and table creation based on data models.

## Creating Tables from Models

You can generate a `CREATE TABLE` statement directly from a Pydantic model.

```python
from pydantic import BaseModel
from dremioframe.client import DremioClient

class User(BaseModel):
    id: int
    name: str
    active: bool

client = DremioClient(...)
builder = client.builder

# Create table 'users' with columns id (INTEGER), name (VARCHAR), active (BOOLEAN)
builder.create_from_model("users", User)
```

## Validating Data

You can validate existing data in Dremio against a Pydantic schema. This fetches a sample of data and checks if it conforms to the model.

```python
# Validate the first 1000 rows of 'users' table
builder.table("users").validate(User, sample_size=1000)
```

## Inserting Data with Validation

When inserting data using `create` or `insert`, you can pass a `schema` argument to validate the data before insertion.

```python
data = [{"id": 1, "name": "Alice", "active": True}]
builder.insert("users", data, schema=User)
```


---

<!-- Source: docs/data_engineering/query_templates.md -->

---

## S3 Integration

DremioFrame provides seamless integration with Amazon S3 through the optional `s3` dependency. This allows you to perform file operations directly within your orchestration pipelines, such as uploading data files before ingestion or downloading results.

## Installation

To use S3 features, you must install the `s3` optional dependency group, which includes `boto3`.

```bash
pip install "dremioframe[s3]"
```

## S3Task

The primary way to interact with S3 is through the `S3Task` in the orchestration module. This task wraps `boto3` operations into a reusable pipeline component.

### Supported Operations

- **`upload_file`**: Upload a local file to an S3 bucket.
- **`download_file`**: Download a file from an S3 bucket to a local path.

### Configuration

You can configure credentials directly in the task or rely on environment variables (recommended).

**Environment Variables:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

### Examples

#### Uploading a File

```python
from dremioframe.orchestration import Pipeline
from dremioframe.orchestration.tasks import S3Task

# Define the task
upload_task = S3Task(
    name="upload_csv",
    operation="upload_file",
    bucket="my-datalake-bucket",
    key="raw/data.csv",
    local_path="./data/local_data.csv"
)

# Create and run pipeline
pipeline = Pipeline("s3_ingest")
pipeline.add_task(upload_task)
pipeline.run()
```

#### Downloading a File

```python
download_task = S3Task(
    name="download_report",
    operation="download_file",
    bucket="my-reports-bucket",
    key="monthly/report.pdf",
    local_path="./downloads/report.pdf"
)
```

#### Using Custom Credentials

```python
custom_s3_task = S3Task(
    name="upload_secure",
    operation="upload_file",
    bucket="secure-bucket",
    key="data.csv",
    local_path="./data.csv",
    aws_access_key_id="AKIA...",
    aws_secret_access_key="SECRET...",
    region_name="us-west-2"
)
```

#### Using MinIO or S3-Compatible Storage

You can connect to S3-compatible storage like MinIO by providing an `endpoint_url`.

```python
minio_task = S3Task(
    name="upload_minio",
    operation="upload_file",
    bucket="test-bucket",
    key="test.csv",
    local_path="./test.csv",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin"
)
```


---

<!-- Source: docs/getting_started/troubleshooting.md -->