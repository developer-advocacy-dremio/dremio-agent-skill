# Ingestion And Loading

## Ingestion Overview

DremioFrame provides multiple ways to ingest data into Dremio, ranging from simple API calls to complex file system and database integrations.

## 1. API Ingestion

Ingest data directly from REST APIs. This method is built into the main client.

**Method:** `client.ingest_api(...)`

```python
client.ingest_api(
    url="https://api.example.com/users",
    table_name="raw_users",
    mode="replace" # 'replace', 'append', or 'merge'
)
```

[Read more about API Ingestion strategies (Modes, Auth, Batching)](ingestion_patterns.md)

## 2. File Upload

Upload local files (CSV, JSON, Parquet, Excel, etc.) directly to Dremio as tables.

**Method:** `client.upload_file(...)`

```python
client.upload_file("data/sales.csv", "space.folder.sales_table")
```

[Read the full File Upload guide](file_upload.md)

## 3. Ingestion Modules

Advanced ingestion capabilities are grouped under the `client.ingest` namespace.

### DLT (Data Load Tool)

Integration with the `dlt` library for robust pipelines.

**Method:** `client.ingest.dlt(...)`

```python
data = [{"id": 1, "name": "Alice"}]
client.ingest.dlt(data, "my_dlt_table")
```

[Read the DLT Integration guide](dlt_integration.md)

### Database Ingestion

Ingest query results from other databases (Postgres, MySQL, etc.) using JDBC/ODBC connectors via `connectorx` or `sqlalchemy`.

**Method:** `client.ingest.database(...)`

```python
client.ingest.database(
    connection_string="postgresql://user:pass@localhost/db",
    query="SELECT * FROM users",
    table_name="postgres_users"
)
```

[Read the Database Ingestion guide](database_ingestion.md)

### File System Ingestion

Ingest multiple files from a local directory or glob pattern.

**Method:** `client.ingest.files(...)`

```python
client.ingest.files("data/*.parquet", "my_dataset")
```

[Read the File System Ingestion guide](file_system_ingestion.md)


---

<!-- Source: docs/data_engineering/ingestion_patterns.md -->

---

## Create from data
test_data = [
    {'product_id': 1, 'name': 'Widget', 'price': 9.99},
    {'product_id': 2, 'name': 'Gadget', 'price': 19.99}
]

df = manager.create_fixture('products', test_data)
```

### Loading from Files

```python

---

## Create large dataset
data = pd.DataFrame({
    "id": range(100000),
    "name": [f"user_{i}" for i in range(100000)],
    "value": range(100000)
})

---

## Database Ingestion

DremioFrame provides a standardized way to ingest data from any SQL database (PostgreSQL, MySQL, SQLite, Oracle, etc.) into Dremio.

## Installation

To use the database ingestion feature, you must install the optional dependencies:

```bash
pip install dremioframe[database]
```

This installs `connectorx` (for high-performance loading) and `sqlalchemy` (for broad compatibility).

## Usage

The integration is exposed via `client.ingest.database()`.

### Example: Loading from PostgreSQL

```python
from dremioframe.client import DremioClient

client = DremioClient()

# Connection string (URI)
db_uri = "postgresql://user:password@localhost:5432/mydb"

# Ingest query results into Dremio
client.ingest.database(
    connection_string=db_uri,
    query="SELECT * FROM users WHERE active = true",
    table_name='"my_space"."my_folder"."users"',
    write_disposition="replace",
    backend="connectorx" # Default, faster
)
```

### Parameters

- **connection_string**: Database connection URI (e.g., `postgresql://...`, `mysql://...`).
- **query**: SQL query to execute on the source database.
- **table_name**: The target table name in Dremio.
- **write_disposition**: `'replace'` or `'append'`.
- **backend**:
    - `'connectorx'` (default): Extremely fast, written in Rust. Supports Postgres, MySQL, SQLite, Redshift, Clickhouse, SQL Server.
    - `'sqlalchemy'`: Uses standard SQLAlchemy engines. Slower but supports any database with a Python driver.
- **batch_size**: (Only for `sqlalchemy` backend) Number of records to process per batch. Useful for large datasets to avoid memory issues.

### Performance Tips

- Use `backend="connectorx"` whenever possible for significantly faster load times.
- For very large tables with `sqlalchemy`, set a `batch_size` (e.g., 50,000) to stream data instead of loading it all into memory.


---

<!-- Source: docs/data_engineering/dlt_integration.md -->

---

## Document Extraction to Tables

The DremioAgent can extract structured data from documents (PDFs, markdown files) in your context folder and generate code to create or insert data into Dremio tables.

## Installation

```bash
pip install dremioframe[document]
```

## Usage

### Basic Workflow

1. Place documents in a context folder
2. Initialize agent with context folder
3. Ask agent to extract data with a specific schema
4. Agent generates code to create/insert into Dremio

### Example: Extract Invoice Data from PDFs

```python
from dremioframe.ai.agent import DremioAgent

# Initialize agent with context folder
agent = DremioAgent(
    model="gpt-4o",
    context_folder="./invoices"
)

# Ask agent to extract structured data
script = agent.generate_script("""
Read all PDF files in the context folder that contain invoice data.
Extract the following fields: invoice_number, date, customer_name, total_amount.
Generate code to create a table 'invoices' with this schema and insert the extracted data.
""")

print(script)
```

### Example: Extract Product Catalog from Markdown

```python
agent = DremioAgent(
    model="gpt-4o",
    context_folder="./product_docs"
)

script = agent.generate_script("""
Read all markdown files in the context folder.
Extract product information: product_id, name, category, price, description.
Create a table 'products' and insert the data.
""")
```

## Supported Document Types

### PDF Files
- Uses `pdfplumber` for text extraction
- Works with text-based PDFs
- Scanned PDFs require OCR (not currently supported)

### Markdown Files
- Direct text reading
- Supports tables, lists, and structured content

### Text Files
- Any `.txt`, `.md`, `.csv` files
- Read via `read_context_file` tool

## How It Works

1. **List Files**: Agent uses `list_context_files()` to see available documents
2. **Read Content**: Agent uses `read_pdf_file()` or `read_context_file()` to extract text
3. **Extract Data**: LLM analyzes content and extracts structured data
4. **Generate Code**: Agent creates Python code to load data into Dremio

## Best Practices

### Provide Clear Schema
Be specific about the fields you want extracted:
```python
"""
Extract these exact fields:
- invoice_number (string)
- date (YYYY-MM-DD format)
- customer_name (string)
- total_amount (decimal)
"""
```

### Use Examples
Provide example data if documents have varying formats:
```python
"""
Example invoice format:
Invoice #: INV-12345
Date: 2024-01-15
Customer: Acme Corp
Total: $1,500.00
"""
```

### Handle Missing Data
Specify how to handle missing fields:
```python
"""
If a field is missing, use NULL or empty string.
"""
```

## Limitations

- **OCR Not Supported**: Scanned PDFs won't work (text-based only)
- **Token Limits**: Very large documents may exceed LLM context windows
- **Accuracy**: Extraction quality depends on document structure and LLM capabilities
- **Performance**: Large batches of documents may be slow

## Future Enhancements

- Image OCR support (via Tesseract or cloud services)
- Table extraction from PDFs
- Multi-page document handling
- Batch processing optimization


---

<!-- Source: docs/ai/generation.md -->

---

## File System Ingestion

DremioFrame provides a convenient way to ingest multiple files from your local filesystem or network drives using glob patterns.

## Installation

No additional dependencies required - this feature uses the core DremioFrame installation.

## Usage

The integration is exposed via `client.ingest.files()`.

### Example: Loading Multiple Parquet Files

```python
from dremioframe.client import DremioClient

client = DremioClient()

# Ingest all parquet files in a directory
client.ingest.files(
    pattern="data/sales_*.parquet",
    table_name='"my_space"."my_folder"."sales"',
    write_disposition="replace"
)
```

### Example: Recursive Directory Scan

```python
# Ingest all CSV files in directory tree
client.ingest.files(
    pattern="data/**/*.csv",
    table_name='"my_space"."logs"."all_logs"',
    file_format="csv",
    recursive=True,
    write_disposition="append"
)
```

## Parameters

- **pattern**: Glob pattern (e.g., `"data/*.parquet"`, `"sales_2024_*.csv"`).
- **table_name**: The target table name in Dremio.
- **file_format**: File format (`'parquet'`, `'csv'`, `'json'`). Auto-detected from extension if not specified.
- **write_disposition**: 
    - `'replace'`: Drop table if exists and create new.
    - `'append'`: Append data to existing table.
- **recursive**: If `True`, enables recursive glob (`**` pattern).

## Supported File Formats

- **Parquet** (`.parquet`)
- **CSV** (`.csv`)
- **JSON** (`.json`, `.jsonl`, `.ndjson`)

## How It Works

1. Finds all files matching the glob pattern
2. Reads each file into an Arrow Table
3. Concatenates all tables into a single table
4. Uses the **staging method** (Parquet upload) for efficient bulk loading
5. Creates or appends to the target table in Dremio

## Performance

File system ingestion automatically uses the **staging method** for bulk loading, providing excellent performance even with large datasets:

- Handles 100+ files efficiently
- Supports files with millions of rows
- Minimal memory footprint (streaming read)

## Use Cases

- **Data Lake Ingestion**: Load partitioned datasets from S3/HDFS mounted locally
- **Batch Processing**: Ingest daily/hourly file drops
- **Migration**: Bulk load historical data from file archives
- **Development**: Quick data loading from local test files


---

<!-- Source: docs/data_engineering/file_upload.md -->

---

## File Upload

DremioFrame allows you to upload local files directly to Dremio as Iceberg tables.

## Supported Formats

*   **CSV** (`.csv`)
*   **JSON** (`.json`)
*   **Parquet** (`.parquet`)
*   **Excel** (`.xlsx`, `.xls`, `.ods`) - Requires `pandas`, `openpyxl`
*   **HTML** (`.html`) - Requires `pandas`, `lxml`
*   **Avro** (`.avro`) - Requires `fastavro`
*   **ORC** (`.orc`) - Requires `pyarrow`
*   **Lance** (`.lance`) - Requires `pylance`
*   **Feather/Arrow** (`.feather`, `.arrow`) - Requires `pyarrow`

## Usage

Use the `client.upload_file()` method.

```python
from dremioframe.client import DremioClient

client = DremioClient()

# Upload a CSV file
client.upload_file("data/sales.csv", "space.folder.sales_table")

# Upload an Excel file
client.upload_file("data/financials.xlsx", "space.folder.financials")

# Upload an Avro file
client.upload_file("data/users.avro", "space.folder.users")
```

## Arguments

*   `file_path` (str): Path to the local file.
*   `table_name` (str): Destination table name in Dremio (e.g., "space.folder.table").
*   `file_format` (str, optional): The format of the file ('csv', 'json', 'parquet', 'excel', 'html', 'avro', 'orc', 'lance', 'feather'). If not provided, it is inferred from the file extension.
*   `**kwargs`: Additional arguments passed to the underlying file reader.
    *   **CSV**: `pyarrow.csv.read_csv`
    *   **JSON**: `pyarrow.json.read_json`
    *   **Parquet**: `pyarrow.parquet.read_table`
    *   **Excel**: `pandas.read_excel`
    *   **HTML**: `pandas.read_html`
    *   **Avro**: `fastavro.reader`
    *   **ORC**: `pyarrow.orc.read_table`
    *   **Lance**: `lance.dataset`
    *   **Feather**: `pyarrow.feather.read_table`

## Example with Options

```python
# Upload Excel sheet "Sheet2"
client.upload_file("data.xlsx", "space.folder.data", sheet_name="Sheet2")
```


---

<!-- Source: docs/data_engineering/files.md -->

---

## Ingestion Patterns & Best Practices

This guide outlines common patterns for moving data into Iceberg tables using DremioFrame, covering both Dremio-connected sources and external data.

## Why Move Data to Iceberg?

While Dremio can query data directly from sources like Postgres, SQL Server, or S3, moving data into **Apache Iceberg** tables (in Dremio's Arctic or S3/Data Lake sources) offers significant benefits:
- **Performance**: Iceberg tables are optimized for analytics (columnar, partitioned).
- **Features**: Enables Time Travel, Rollback, and DML operations (Update/Delete/Merge).
- **Isolation**: Decouples analytical workloads from operational databases.

---

## Pattern 1: Source to Iceberg (ELT)

If your data is already in a source connected to Dremio (e.g., a Postgres database or a raw S3 folder), you can use Dremio to move it into an Iceberg table.

### Initial Load (CTAS)

Use the `create` method to perform a `CREATE TABLE AS SELECT` (CTAS) operation. This pushes the work to the Dremio engine.

```python
# Create an Iceberg table 'marketing.users' from a Postgres source table
client.table("postgres.public.users") \
    .filter("active = true") \
    .create("marketing.users")
```

### Incremental Append

Use `insert` to append new rows from a source to an existing Iceberg table.

```python
# Append new logs from S3 to Iceberg
client.table("s3.raw_logs") \
    .filter("event_date = CURRENT_DATE") \
    .insert("marketing.logs")
```

### Upsert (Merge)

Use `merge` to update existing records and insert new ones.

```python
# Upsert users from Postgres to Iceberg
client.table("postgres.public.users").merge(
    target_table="marketing.users",
    on="id",
    matched_update={"email": "source.email", "status": "source.status"},
    not_matched_insert={"id": "source.id", "email": "source.email", "status": "source.status"}
)
```

---

## Pattern 2: External Data to Iceberg (ETL)

If your data originates outside Dremio (e.g., REST APIs, local files, Python scripts), you can ingest it using DremioFrame.

### API Ingestion

Use the `ingest_api` utility for REST APIs.

```python
# Fetch users from an API and merge them into an Iceberg table
client.ingest_api(
    url="https://api.example.com/users",
    table_name="marketing.users",
    mode="merge",
    pk="id"
)
```

### Local Dataframes (Pandas/Arrow)

If you have data in a Pandas DataFrame or PyArrow Table, the recommended approach for creating new tables is `client.create_table`.

```python
import pandas as pd

# Load local CSV
df = pd.read_csv("local_data.csv")

# Option 1: Using create_table (Recommended for new tables)
# This is the cleanest API for creating tables from local data
client.create_table("marketing.local_data", schema=df, insert_data=True)

# Option 2: Using builder.create (CTAS approach)
# Note: The source table in client.table() is ignored when 'data' is provided.
# This pattern is useful if you are already working with a builder object.
client.table("marketing.local_data").create("marketing.local_data", data=df)

# Option 3: Appending to existing table
# Use this to add data to an existing table
client.table("marketing.local_data").insert("marketing.local_data", data=df)
```

**Note**: For large local datasets, use the `batch_size` parameter to avoid memory issues and timeouts.

```python
client.table("target").insert("target", data=large_df, batch_size=5000)
```

See [Creating Tables](creating_tables.md) for more details on table creation methods.

---

## Best Practices

### 1. Optimize Your Tables
After significant data ingestion (especially many small inserts), run `optimize()` to compact small files.

```python
client.table("marketing.users").optimize()
```

### 2. Manage Snapshots
Iceberg keeps history for Time Travel. To save storage, periodically expire old snapshots using `vacuum()`.

```python
# Retain only the last 5 snapshots
client.table("marketing.users").vacuum(retain_last=5)
```

### 3. Use Staging Tables for Complex Merges
If you need to perform complex transformations before merging, load data into a temporary staging table first.

```python
# 1. Load raw data to staging
client.ingest_api(..., table_name="staging_users", mode="replace")

# 2. Transform and Merge from staging to target
client.table("staging_users") \
    .mutate(full_name="concat(first, ' ', last)") \
    .merge(target_table="marketing.users", on="id", ...)

# 3. Drop staging
client.table("staging_users").delete() # Or drop via SQL
```

### 4. Batching
When inserting data from Python (Pandas/Arrow), always use `batch_size` for datasets larger than a few thousand rows.

### 5. Type Consistency
Ensure your local DataFrame types match Dremio's expected types. DremioFrame handles basic conversion, but explicit casting in Pandas (e.g., `pd.to_datetime`) is recommended before ingestion.


---

<!-- Source: docs/data_engineering/joins.md -->

---

## Insert in batches of 1000 rows
client.table("target").insert("target", data=large_df, batch_size=1000)
```

## Batching

For `insert` and `merge` operations with in-memory data (Arrow Table or Pandas DataFrame), you can specify a `batch_size` to split the data into multiple chunks. This is useful for large datasets to avoid hitting query size limits.

```python

---

## Insert in batches of 1000 rows
client.table("target").insert("target", data=large_df, batch_size=1000)
```

## Schema Validation

You can validate data against a Pydantic schema before insertion.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

---

## Load CSV
df = manager.load_csv('customers', 'tests/fixtures/customers.csv')

---

## Load JSON
df = manager.load_json('orders', 'tests/fixtures/orders.json')

---

## Upsert from a DataFrame
client.table("target").merge(
    target_table="target",
    on="id",
    matched_update={"val": "source.val"},
    not_matched_insert={"id": "source.id", "val": "source.val"},
    data=df_upsert
)
```

## Batching

For `insert` and `merge` operations with in-memory data (Arrow Table or Pandas DataFrame), you can specify a `batch_size` to split the data into multiple chunks. This is useful for large datasets to avoid hitting query size limits.

```python

---

## Use staging method for fast bulk load
client.table('"my_space"."my_folder"."large_table"').create(
    '"my_space"."my_folder"."large_table"',
    data=data,
    method="staging"  # Much faster than default "values"
)
```

## How It Works

### Values Method (Default)

```python
method="values"  # Default
```

- Generates SQL `INSERT INTO ... VALUES (...)` statements
- Good for small datasets (< 10,000 rows)
- Simple and straightforward
- Can hit SQL statement size limits with large data

### Staging Method (Recommended for Large Data)

```python
method="staging"
```

**For `create()`:**
1. Writes data to a temporary local Parquet file
2. Uploads the Parquet file to Dremio (creates the table)
3. Cleans up the temporary file

**For `insert()`:**
1. Writes data to a temporary local Parquet file
2. Uploads to a temporary staging table in Dremio
3. Executes `INSERT INTO target SELECT * FROM staging_table`
4. Drops the staging table
5. Cleans up the temporary file

## Performance Comparison

| Rows    | Values Method | Staging Method | Speedup |
|---------|---------------|----------------|---------|
| 1,000   | ~2s           | ~3s            | 0.67x   |
| 10,000  | ~20s          | ~5s            | 4x      |
| 100,000 | Fails*        | ~15s           | ∞       |

*SQL statement size limit exceeded

## When to Use Staging

Use `method="staging"` when:
- Loading more than 10,000 rows
- Experiencing slow `INSERT` performance
- Hitting SQL statement size limits
- Working with wide tables (many columns)

Use `method="values"` (default) when:
- Loading small datasets (< 1,000 rows)
- Simplicity is preferred over performance
- You don't have write access to create temporary tables


---

<!-- Source: docs/performance/connection_pooling.md -->

# Connection Pooling

DremioFrame includes a `ConnectionPool` to manage and reuse `DremioClient` instances, which is essential for high-concurrency applications or long-running services.

## ConnectionPool

The `ConnectionPool` manages a thread-safe queue of clients.

### Initialization

```python
from dremioframe.connection_pool import ConnectionPool