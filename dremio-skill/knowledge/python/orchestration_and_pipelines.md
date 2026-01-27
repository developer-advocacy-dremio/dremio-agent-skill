# Orchestration And Pipelines

## 2. Start UI Server (in a separate thread or process)

---

## 3. Run Pipeline
pipeline = Pipeline("my_pipeline", backend=backend)

---

## ... add tasks ...
pipeline.run()
```

Access the UI at `http://localhost:8080`.


---

<!-- Source: docs/performance/bulk_loading.md -->

# Bulk Loading Optimization

For large datasets (10,000+ rows), using the default `VALUES` clause method can be slow and may hit SQL statement size limits. DremioFrame provides a **staging method** that dramatically improves performance by using Parquet files as an intermediate format.

## Usage

Both `create()` and `insert()` methods support a `method` parameter:

```python
from dremioframe.client import DremioClient
import pandas as pd

client = DremioClient()

---

## Airflow Integration

DremioFrame provides native integration with Apache Airflow, allowing you to orchestrate Dremio workflows within your Airflow DAGs.

## Installation

Install DremioFrame with Airflow support:

```bash
pip install "dremioframe[airflow]"
```

This will install `apache-airflow` as a dependency.

## Components

### DremioHook

The `DremioHook` wraps the `DremioClient` and integrates with Airflow's connection management system.

#### Configuration

Create a Dremio connection in Airflow:

**Via Airflow UI:**
1. Navigate to Admin → Connections
2. Add a new connection with the following details:
   - **Connection ID**: `dremio_default` (or custom name)
   - **Connection Type**: `Dremio` (or `Generic` if custom type not available)
   - **Host**: `data.dremio.cloud` (or your Dremio hostname)
   - **Port**: `443` (or your port)
   - **Login**: Username (for Dremio Software with username/password auth)
   - **Password**: Password or PAT
   - **Extra**: JSON with additional config

**Extra JSON Fields:**
```json
{
  "pat": "your_personal_access_token",
  "project_id": "your_project_id",
  "tls": true,
  "disable_certificate_verification": false
}
```

**Via Environment Variable:**
```bash
export AIRFLOW_CONN_DREMIO_DEFAULT='{"conn_type": "dremio", "host": "data.dremio.cloud", "port": 443, "extra": {"pat": "YOUR_PAT", "project_id": "YOUR_PROJECT_ID"}}'
```

#### Usage

```python
from dremioframe.airflow import DremioHook

hook = DremioHook(dremio_conn_id="dremio_default")
client = hook.get_conn()

# Execute SQL
df = hook.get_pandas_df("SELECT * FROM my_table LIMIT 10")

# Get records as list of dicts
records = hook.get_records("SELECT * FROM my_table LIMIT 10")
```

### DremioSQLOperator

Execute SQL queries in Dremio as part of your Airflow DAG.

#### Parameters

- `sql` (str): The SQL query to execute. Supports Jinja templating.
- `dremio_conn_id` (str): Connection ID. Default: `"dremio_default"`.
- `return_result` (bool): Whether to return results as XCom. Default: `False`.

#### Example

```python
from airflow import DAG
from airflow.utils.dates import days_ago
from dremioframe.airflow import DremioSQLOperator

default_args = {
    'owner': 'data_team',
    'start_date': days_ago(1),
}

with DAG('dremio_etl', default_args=default_args, schedule_interval='@daily') as dag:
    
    # Create a table
    create_table = DremioSQLOperator(
        task_id='create_staging_table',
        sql='''
            CREATE TABLE IF NOT EXISTS staging.daily_metrics AS
            SELECT 
                DATE_TRUNC('day', event_time) as date,
                COUNT(*) as event_count,
                COUNT(DISTINCT user_id) as unique_users
            FROM raw.events
            WHERE DATE(event_time) = CURRENT_DATE - INTERVAL '1' DAY
            GROUP BY 1
        '''
    )
    
    # Run aggregation
    aggregate_data = DremioSQLOperator(
        task_id='aggregate_metrics',
        sql='''
            INSERT INTO analytics.daily_summary
            SELECT * FROM staging.daily_metrics
        '''
    )
    
    # Optimize table
    optimize_table = DremioSQLOperator(
        task_id='optimize_table',
        sql='OPTIMIZE TABLE analytics.daily_summary'
    )
    
    create_table >> aggregate_data >> optimize_table
```

#### Templating

The `sql` parameter supports Jinja templating:

```python
DremioSQLOperator(
    task_id='process_partition',
    sql='''
        SELECT * FROM events
        WHERE date = '{{ ds }}'  -- Airflow execution date
    '''
)
```

### DremioDataQualityOperator

Run data quality checks on Dremio tables.

#### Parameters

- `table_name` (str): The table to check. Supports Jinja templating.
- `checks` (list): List of check definitions.
- `dremio_conn_id` (str): Connection ID. Default: `"dremio_default"`.

#### Check Types

- `not_null`: Check that a column has no NULL values.
- `unique`: Check that a column has only unique values.
- `row_count`: Check row count with a condition.
- `values_in`: Check that column values are in a specified list.

#### Example

```python
from dremioframe.airflow import DremioDataQualityOperator

dq_check = DremioDataQualityOperator(
    task_id='validate_daily_metrics',
    table_name='staging.daily_metrics',
    checks=[
        {
            "type": "not_null",
            "column": "date"
        },
        {
            "type": "row_count",
            "expr": "event_count > 0",
            "value": 1,
            "op": "ge"  # greater than or equal
        },
        {
            "type": "unique",
            "column": "date"
        }
    ]
)
```

If any check fails, the operator will raise a `ValueError` and fail the task.

## Complete DAG Example

```python
from airflow import DAG
from airflow.utils.dates import days_ago
from dremioframe.airflow import DremioSQLOperator, DremioDataQualityOperator

default_args = {
    'owner': 'data_team',
    'start_date': days_ago(1),
    'retries': 2,
}

with DAG(
    'dremio_daily_pipeline',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # 2 AM daily
    catchup=False
) as dag:
    
    # Extract
    extract = DremioSQLOperator(
        task_id='extract_raw_data',
        sql='''
            CREATE TABLE staging.raw_events_{{ ds_nodash }} AS
            SELECT * FROM raw.events
            WHERE DATE(event_time) = '{{ ds }}'
        '''
    )
    
    # Transform
    transform = DremioSQLOperator(
        task_id='transform_data',
        sql='''
            CREATE TABLE staging.metrics_{{ ds_nodash }} AS
            SELECT 
                user_id,
                COUNT(*) as event_count,
                MAX(event_time) as last_event
            FROM staging.raw_events_{{ ds_nodash }}
            GROUP BY user_id
        '''
    )
    
    # Data Quality
    dq_check = DremioDataQualityOperator(
        task_id='validate_metrics',
        table_name='staging.metrics_{{ ds_nodash }}',
        checks=[
            {"type": "not_null", "column": "user_id"},
            {"type": "row_count", "expr": "event_count > 0", "value": 1, "op": "ge"}
        ]
    )
    
    # Load
    load = DremioSQLOperator(
        task_id='load_to_analytics',
        sql='''
            INSERT INTO analytics.user_metrics
            SELECT '{{ ds }}' as date, *
            FROM staging.metrics_{{ ds_nodash }}
        '''
    )
    
    # Cleanup
    cleanup = DremioSQLOperator(
        task_id='cleanup_staging',
        sql='''
            DROP TABLE staging.raw_events_{{ ds_nodash }};
            DROP TABLE staging.metrics_{{ ds_nodash }};
        '''
    )
    
    extract >> transform >> dq_check >> load >> cleanup
```

## Best Practices

### 1. Use XComs Sparingly

Avoid returning large datasets via XCom:

```python
# Bad - returns large dataset
DremioSQLOperator(
    task_id='get_data',
    sql='SELECT * FROM large_table',
    return_result=True  # Avoid this for large results
)

# Good - process in Dremio, only return metadata
DremioSQLOperator(
    task_id='process_data',
    sql='CREATE TABLE result AS SELECT * FROM large_table WHERE ...'
)
```

### 2. Leverage Templating

Use Airflow's templating for dynamic queries:

```python
DremioSQLOperator(
    task_id='partition_process',
    sql='''
        OPTIMIZE TABLE my_table
        WHERE partition_date = '{{ ds }}'
    '''
)
```

### 3. Idempotent Operations

Make your SQL idempotent for safe retries:

```python
# Use CREATE TABLE IF NOT EXISTS
DremioSQLOperator(
    task_id='create_table',
    sql='CREATE TABLE IF NOT EXISTS ...'
)

# Or use MERGE for upserts
DremioSQLOperator(
    task_id='upsert_data',
    sql='''
        MERGE INTO target USING source
        ON target.id = source.id
        WHEN MATCHED THEN UPDATE SET ...
        WHEN NOT MATCHED THEN INSERT ...
    '''
)
```

### 4. Connection Pooling

Reuse connections within a DAG by using the same `dremio_conn_id`.

### 5. Error Handling

Use Airflow's built-in retry mechanism:

```python
DremioSQLOperator(
    task_id='flaky_operation',
    sql='...',
    retries=3,
    retry_delay=timedelta(minutes=5)
)
```

## Comparison with Native Orchestration

DremioFrame includes its own lightweight orchestration engine. Here's when to use each:

| Use Airflow When... | Use DremioFrame Orchestration When... |
|---------------------|---------------------------------------|
| You already have Airflow infrastructure | You want a lightweight, standalone solution |
| You need complex scheduling (cron, sensors) | You need simple task dependencies |
| You integrate with many other systems | You only work with Dremio |
| You need enterprise features (RBAC, audit logs) | You want minimal dependencies |
| You have a dedicated data engineering team | You're a data analyst or scientist |

You can also use both: develop pipelines with DremioFrame orchestration, then migrate to Airflow for production.

## Troubleshooting

### Connection Issues

If you see `ModuleNotFoundError: No module named 'dremioframe'`:
- Ensure DremioFrame is installed in the Airflow environment
- Check `pip list | grep dremioframe`

### Authentication Errors

If you see authentication failures:
- Verify PAT is valid: `curl -H "Authorization: Bearer YOUR_PAT" https://api.dremio.cloud/v0/projects`
- Check connection configuration in Airflow UI
- Ensure `project_id` is set for Dremio Cloud

### Query Timeouts

For long-running queries:
- Increase Airflow task timeout: `execution_timeout=timedelta(hours=2)`
- Consider breaking into smaller tasks
- Use Dremio reflections to accelerate queries

## See Also

- [Orchestration Overview](../orchestration/overview.md)
- [Data Quality](../data_quality.md)
- [Administration](../admin_governance/admin.md)


---

<!-- Source: docs/integrations/notebook.md -->

---

## Batch Operations

DremioFrame provides a `BatchManager` to perform bulk operations on the Dremio catalog efficiently using parallel API requests.

## BatchManager

The `BatchManager` utilizes a thread pool to execute multiple API calls concurrently, significantly speeding up operations like creating many folders or deleting multiple datasets.

### Initialization

```python
from dremioframe.client import DremioClient
from dremioframe.batch import BatchManager

client = DremioClient()
# Initialize with 10 concurrent workers
manager = BatchManager(client, max_workers=10)
```

### Creating Folders

Create multiple folders at once.

```python
paths = [
    "space.folder1",
    "space.folder2",
    "space.folder3"
]

results = manager.create_folders(paths)

for path, result in results.items():
    if "error" in result:
        print(f"Failed to create {path}: {result['error']}")
    else:
        print(f"Created {path}")
```

### Deleting Items

Delete multiple items (datasets, folders, spaces) by their ID.

```python
ids_to_delete = ["id1", "id2", "id3"]

results = manager.delete_items(ids_to_delete)

for id, success in results.items():
    if success is True:
        print(f"Deleted {id}")
    else:
        print(f"Failed to delete {id}: {success['error']}")
```

## Performance Considerations

- **Rate Limits**: Be mindful of Dremio's API rate limits when using a high number of workers.
- **Error Handling**: Batch operations return a dictionary of results where individual failures are captured without stopping the entire batch. Always check the results for errors.


---

<!-- Source: docs/admin_governance/catalog.md -->

---

## Distributed Execution

DremioFrame Orchestration supports distributed task execution using **Celery**. This allows you to scale your pipelines across multiple worker nodes.

## Executors

The `Pipeline` class now accepts an `executor` argument.

### LocalExecutor (Default)

Executes tasks locally using a thread pool.

```python
from dremioframe.orchestration import Pipeline
from dremioframe.orchestration.executors import LocalExecutor

# Default behavior (uses LocalExecutor with 1 worker)
pipeline = Pipeline("my_pipeline")

# Explicitly configure LocalExecutor
executor = LocalExecutor(backend=backend, max_workers=4)
pipeline = Pipeline("my_pipeline", executor=executor)
```

### CeleryExecutor

Executes tasks on a Celery cluster. This requires a message broker (like Redis or RabbitMQ).

#### Requirements
```bash
pip install "dremioframe[celery]"
```

#### Configuration

1.  **Start a Redis Server** (or other broker).
2.  **Start a Celery Worker**:
    You need a worker process that can import `dremioframe` and your task code.
    
    Create a `worker.py`:
    ```python
    from celery import Celery
    
    # Configure the app to match the executor's settings
    app = Celery("dremioframe_orchestration", broker="redis://localhost:6379/0")
    app.conf.update(
        result_backend="redis://localhost:6379/0",
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        imports=["dremioframe.orchestration.executors"] # Important!
    )
    ```
    
    Run the worker:
    ```bash
    celery -A worker worker --loglevel=info
    ```

3.  **Configure the Pipeline**:
    ```python
    from dremioframe.orchestration import Pipeline
    from dremioframe.orchestration.executors import CeleryExecutor
    
    executor = CeleryExecutor(backend=backend, broker_url="redis://localhost:6379/0")
    pipeline = Pipeline("my_pipeline", executor=executor)
    
    pipeline.run()
    ```

## Task Serialization

The `CeleryExecutor` uses `pickle` to serialize your task objects and their actions. 
**Important**: Ensure your task actions are top-level functions or importable callables. Lambdas and nested functions may fail to pickle.


---

<!-- Source: docs/orchestration/dq_task.md -->

---

## Dremio Job Integration

`dremioframe` provides specialized tasks for interacting with Dremio Jobs.

## DremioQueryTask

The `DremioQueryTask` submits a SQL query to Dremio, waits for its completion, and supports cancellation.

### Features
-   **Job Tracking**: Tracks the Dremio Job ID.
-   **Cancellation**: If the pipeline is killed or the task is cancelled, it attempts to cancel the running Dremio Job.
-   **Polling**: Efficiently polls for job status.

### Usage

```python
from dremioframe.orchestration import DremioQueryTask, Pipeline
from dremioframe.client import DremioClient

client = DremioClient(...)

# Create a task
t1 = DremioQueryTask(
    name="run_heavy_query",
    client=client,
    sql="SELECT * FROM my_heavy_table"
)

pipeline = Pipeline("dremio_pipeline")
pipeline.add_task(t1)
pipeline.run()
```


---

<!-- Source: docs/orchestration/extensions.md -->

---

## Incremental Processing

DremioFrame simplifies incremental data loading patterns, allowing you to efficiently process only new or changed data.

## IncrementalLoader

The `IncrementalLoader` class provides helper methods for watermark-based loading and MERGE (upsert) operations.

### Initialization

```python
from dremioframe.client import DremioClient
from dremioframe.incremental import IncrementalLoader

client = DremioClient()
loader = IncrementalLoader(client)
```

### Watermark-based Loading

This pattern loads data from a source table to a target table where a specific column (e.g., timestamp or ID) is greater than the maximum value in the target table.

```python
# Load new data from 'staging.events' to 'analytics.events'
# based on the 'event_time' column.
rows_inserted = loader.load_incremental(
    source_table="staging.events",
    target_table="analytics.events",
    watermark_col="event_time"
)

print(f"Loaded {rows_inserted} new rows.")
```

**How it works:**
1. Queries `MAX(event_time)` from `analytics.events`.
2. Executes `INSERT INTO analytics.events SELECT * FROM staging.events WHERE event_time > 'MAX_VALUE'`.
3. If the target table is empty, it performs a full load.

### Merge (Upsert)

The `merge` method performs a standard SQL MERGE operation to update existing records and insert new ones.

```python
# Upsert users from staging to production
loader.merge(
    source_table="staging.users",
    target_table="production.users",
    on=["user_id"],                 # Join condition
    update_cols=["email", "status"], # Columns to update when matched
    insert_cols=["user_id", "email", "status", "created_at"] # Columns to insert when not matched
)
```

**Generated SQL:**
```sql
MERGE INTO production.users AS target 
USING staging.users AS source 
ON (target.user_id = source.user_id)
WHEN MATCHED THEN 
    UPDATE SET email = source.email, status = source.status
WHEN NOT MATCHED THEN 
    INSERT (user_id, email, status, created_at) 
    VALUES (source.user_id, source.email, source.status, source.created_at)
```

## Best Practices

- **Indexing**: Ensure your watermark columns and join keys are optimized (e.g., sorted or partitioned) in Dremio for performance.
- **Reflections**: Use Dremio Reflections to accelerate the `MAX(watermark)` query on large target tables.
- **Data Types**: Ensure data types match between source and target to avoid casting issues during INSERT/MERGE.


---

<!-- Source: docs/data_engineering/ingestion.md -->

---

## Note: In production, you might run this as a separate script.
ui_thread = threading.Thread(target=start_ui, args=(backend, 8080))
ui_thread.daemon = True
ui_thread.start()

---

## Orchestration Backend

By default, `dremioframe` pipelines store their state in memory. This means if the process exits, the history of pipeline runs is lost.
To persist pipeline history and enable features like the Web UI, you can use a persistent backend.

## SQLite Backend

The `SQLiteBackend` stores pipeline runs and task statuses in a local SQLite database file.

### Usage

```python
from dremioframe.orchestration import Pipeline
from dremioframe.orchestration.backend import SQLiteBackend

# Initialize backend
backend = SQLiteBackend(db_path="pipeline_history.db")

# Pass backend to Pipeline
pipeline = Pipeline("my_pipeline", backend=backend)

pipeline.run()
```

### Custom Backends

You can implement your own backend (e.g., Postgres, Redis, S3) by extending `BaseBackend`.

#### The `PipelineRun` Object
Your backend will need to store and retrieve `PipelineRun` objects.
```python
@dataclass
class PipelineRun:
    pipeline_name: str
    run_id: str
    start_time: float
    status: str          # "RUNNING", "SUCCESS", "FAILED"
    end_time: float      # Optional
    tasks: Dict[str, str] # Map of task_name -> status
```

#### Required Methods

You must implement the following 4 methods:

1.  **`save_run(self, run: PipelineRun)`**:
    *   Called when a pipeline starts and finishes.
    *   Should upsert the run record in your storage.

2.  **`get_run(self, run_id: str) -> Optional[PipelineRun]`**:
    *   Called to retrieve a specific run.
    *   Return `None` if not found.

3.  **`update_task_status(self, run_id: str, task_name: str, status: str)`**:
    *   Called every time a task changes state (RUNNING, SUCCESS, FAILED, SKIPPED).
    *   Must be efficient and thread-safe if possible.

4.  **`list_runs(self, pipeline_name: str = None, limit: int = 10) -> List[PipelineRun]`**:
    *   Called by the UI to show history.
    *   Should return the most recent runs, optionally filtered by pipeline name.

#### Example Implementation Skeleton

```python
from dremioframe.orchestration.backend import BaseBackend, PipelineRun
from typing import List, Optional

class MyRedisBackend(BaseBackend):
    def __init__(self, redis_client):
        self.redis = redis_client

    def save_run(self, run: PipelineRun):
        # Serialize run to JSON and save to Redis key `run:{run.run_id}`
        pass
        
    def get_run(self, run_id: str) -> Optional[PipelineRun]:
        # Get JSON from Redis and deserialize to PipelineRun
        pass
        
    def update_task_status(self, run_id: str, task_name: str, status: str):
        # Update the specific field in the stored JSON or Hash
        pass

    def list_runs(self, pipeline_name: str = None, limit: int = 10) -> List[PipelineRun]:
        # Scan keys or use a sorted set for time-based retrieval
        pass
```

## Postgres Backend

The `PostgresBackend` stores pipeline state in a PostgreSQL database.

### Requirements
```bash
pip install "dremioframe[postgres]"
```

### Usage
```python
from dremioframe.orchestration.backend import PostgresBackend

# Uses DREMIOFRAME_PG_DSN env var if dsn not provided
backend = PostgresBackend(dsn="postgresql://user:password@localhost:5432/mydb")
pipeline = Pipeline("my_pipeline", backend=backend)
```

## MySQL Backend

The `MySQLBackend` stores pipeline state in a MySQL database.

### Requirements
```bash
pip install "dremioframe[mysql]"
```

### Usage
```python
from dremioframe.orchestration.backend import MySQLBackend

# Uses DREMIOFRAME_MYSQL_* env vars if config not provided
backend = MySQLBackend(config={
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "database": "mydb"
})
pipeline = Pipeline("my_pipeline", backend=backend)
```


---

<!-- Source: docs/orchestration/best_practices.md -->

---

## Orchestration Best Practices

This guide provides recommendations and patterns for building robust data pipelines using `dremioframe.orchestration`.

## 1. Organizing Your Tasks

### Use the `@task` Decorator
The decorator syntax is cleaner and keeps your code readable.

```python
from dremioframe.orchestration import task

@task(name="extract_data")
def extract():
    ...
```

### Keep Tasks Atomic
Each task should do one thing well. This makes debugging easier and allows for better retry granularity.

**Bad:**
```python
@task(name="do_everything")
def run():
    # Extract
    # Transform
    # Load
    # Email
```

**Good:**
```python
@task(name="extract")
def extract(): ...

@task(name="transform")
def transform(): ...

@task(name="load")
def load(): ...
```

## 2. Managing Dependencies

### Linear Chains
For simple sequences, chain the calls:

```python
t1.set_downstream(t2).set_downstream(t3)
```

### Fan-Out / Fan-In
Run multiple tasks in parallel and then aggregate results.

```python
extract_users = extract("users")
extract_orders = extract("orders")
extract_products = extract("products")

consolidate = consolidate_data()

# Fan-in
extract_users.set_downstream(consolidate)
extract_orders.set_downstream(consolidate)
extract_products.set_downstream(consolidate)
```

## 3. Handling Failures

### Use Retries for Transient Errors
Network blips happen. Always add retries to tasks that interact with external systems (Dremio, S3, APIs).

```python
@task(name="query_dremio", retries=3, retry_delay=2.0)
def query():
    ...
```

### Use Branching for Alerts
Don't let a failure go unnoticed. Use the `one_failed` trigger rule to send notifications.

```python
@task(name="alert_slack", trigger_rule="one_failed")
def alert(context=None):
    # Send message to Slack
    pass

critical_task.set_downstream(alert)
```

### Use `all_done` for Cleanup
Ensure temporary resources are cleaned up even if the pipeline fails.

```python
@task(name="cleanup_tmp", trigger_rule="all_done")
def cleanup():
    # Delete tmp files
    pass
```

## 4. Data Passing (Context)

### Return Small Metadata, Not Big Data
Do not pass large DataFrames between tasks via return values. The context is kept in memory.
Instead, pass **references** (e.g., table names, S3 paths, file paths).

**Bad:**
```python
@task
def get_data():
    return huge_dataframe # Don't do this
```

**Good:**
```python
@task
def get_data():
    df = ...
    df.to_parquet("s3://bucket/data.parquet")
    return "s3://bucket/data.parquet"

@task
def process(context=None):
    path = context.get("get_data")
    # Load from path
```

## 5. Project Structure

Organize your pipelines into a dedicated directory.

```
my_project/
├── pipelines/
│   ├── __init__.py
│   ├── daily_etl.py
│   └── weekly_report.py
├── tasks/
│   ├── __init__.py
│   ├── common.py
│   └── dremio_tasks.py
└── main.py
```

## 6. Testing

Write unit tests for your tasks by calling the underlying functions directly (if possible) or checking the Task object.
Use `dremioframe`'s testing utilities to mock Dremio responses.


---

<!-- Source: docs/orchestration/cli.md -->

---

## Orchestration CLI

DremioFrame provides a CLI to manage your pipelines and orchestration server.

## Installation

The CLI is installed with `dremioframe`.

```bash
dremio-cli --help
```

## Pipeline Commands

### List Pipelines (Runs)

List recent pipeline runs from the backend.

```bash
# Default (SQLite)
dremio-cli pipeline list

# Custom SQLite path
dremio-cli pipeline list --backend-url sqlite:///path/to/db.sqlite

# Postgres
dremio-cli pipeline list --backend-url postgresql://user:pass@host/db
```

### Start UI

Start the Orchestration Web UI.

```bash
dremio-cli pipeline ui --port 8080 --backend-url sqlite:///dremioframe.db
```

## Environment Variables

You can also configure the backend via environment variables if supported by the specific backend class, but the CLI currently relies on the `--backend-url` for instantiation logic.


---

<!-- Source: docs/orchestration/deployment.md -->

---

## Orchestration Extensions

DremioFrame includes advanced tasks for orchestration, including dbt integration and sensors.

## dbt Task

The `DbtTask` allows you to run dbt commands within your pipeline.

```python
from dremioframe.orchestration import Pipeline, DbtTask

pipeline = Pipeline("dbt_pipeline")

dbt_run = DbtTask(
    name="run_models",
    command="run",
    project_dir="/path/to/dbt/project",
    select="my_model+"
)

pipeline.add_task(dbt_run)
pipeline.run()
```

## Sensors

Sensors are tasks that wait for a condition to be met before proceeding.

### SqlSensor

Polls a SQL query until it returns data (or a specific condition).

```python
from dremioframe.orchestration import Pipeline, SqlSensor

pipeline = Pipeline("sensor_pipeline")

# Wait until data arrives in staging table
wait_for_data = SqlSensor(
    name="wait_for_staging",
    client=client,
    sql="SELECT 1 FROM staging_table LIMIT 1",
    poke_interval=60, # Check every 60 seconds
    timeout=3600      # Timeout after 1 hour
)

pipeline.add_task(wait_for_data)
pipeline.run()
```

### FileSensor

Checks for the existence of a file in a Dremio source.

```python
from dremioframe.orchestration import Pipeline, FileSensor

# Wait for file to appear
wait_for_file = FileSensor(
    name="wait_for_file",
    client=client,
    path="s3_source.bucket.folder",
    poke_interval=60
)

pipeline.add_task(wait_for_file)
pipeline.run()
```


---

<!-- Source: docs/orchestration/iceberg.md -->

---

## Orchestration Scheduling


You can also schedule by a simple interval in seconds.

```python
# Run every 60 seconds
schedule_pipeline(pipeline, interval_seconds=60)
```


---

<!-- Source: docs/orchestration/tasks.md -->

---

## Orchestration Tasks

DremioFrame provides a set of general-purpose tasks to extend your pipelines beyond Dremio operations.

## General Tasks

Import these from `dremioframe.orchestration.tasks.general`.

### HttpTask

Performs HTTP requests. Useful for triggering webhooks or fetching external data.

```python
from dremioframe.orchestration.tasks.general import HttpTask

task = HttpTask(
    name="trigger_webhook",
    url="https://api.example.com/webhook",
    method="POST",
    json_data={"status": "pipeline_started"}
)
```

### EmailTask

Sends emails via SMTP. Useful for notifications.

```python
from dremioframe.orchestration.tasks.general import EmailTask

task = EmailTask(
    name="send_alert",
    subject="Pipeline Failed",
    body="The pipeline encountered an error.",
    to_addr="admin@example.com",
    smtp_server="smtp.example.com",
    smtp_port=587,
    use_tls=True,
    username="user",
    password="password"
)
```

### ShellTask

Executes arbitrary shell commands.

```python
from dremioframe.orchestration.tasks.general import ShellTask

task = ShellTask(
    name="run_dbt",
    command="dbt run",
    cwd="/path/to/dbt/project",
    env={"DBT_PROFILES_DIR": "."}
)
```

### S3Task

Interacts with AWS S3. Requires `boto3`.

**Requirements:**
```bash
pip install "dremioframe[s3]"
```

**Usage:**
```python
from dremioframe.orchestration.tasks.general import S3Task

# Upload
upload = S3Task(
    name="upload_report",
    operation="upload_file",
    bucket="my-bucket",
    key="reports/daily.csv",
    local_path="/tmp/daily.csv"
)

# Download
download = S3Task(
    name="download_config",
    operation="download_file",
    bucket="my-bucket",
    key="config/settings.json",
    local_path="/app/settings.json"
)
```


---

<!-- Source: docs/orchestration/ui.md -->

---

## Orchestration Web UI

`dremioframe` includes a lightweight Web UI to visualize pipeline runs and task statuses.

## Features

- **Dashboard**: View all pipelines and their recent runs.
- **Real-time Updates**: Auto-refreshing status of tasks and runs.
- **Manual Trigger**: Trigger pipeline runs directly from the UI.
- **Task Status**: Visual indicators for task success, failure, and skipping.

## Starting the UI

You can start the UI from your Python script:

```python
from dremioframe.orchestration import start_ui, Pipeline
from dremioframe.orchestration.backend import SQLiteBackend

# Setup backend and pipelines
backend = SQLiteBackend("history.db")
pipeline1 = Pipeline("etl_job", backend=backend)
pipeline2 = Pipeline("maintenance", backend=backend)

# Start UI
# Pass the pipelines dict to enable manual triggering
start_ui(backend=backend, pipelines={"etl_job": pipeline1, "maintenance": pipeline2}, port=8080)
```

Visit `http://localhost:8080` in your browser.

## Security

The UI supports Basic Authentication.

### Enabling Authentication

Pass `username` and `password` to `start_ui` or via the CLI.

```python
from dremioframe.orchestration.ui import start_ui

start_ui(backend, port=8080, username="admin", password="secret_password")
```

### CLI Usage

(CLI support for auth args is pending, currently only via python script or hardcoded in custom entrypoint)
*Note: The `dremio-cli pipeline ui` command does not yet expose auth flags, but you can wrap `start_ui` in your own script.*

## Architecture

The UI is a Single Page Application (SPA) built with **Vue.js** (loaded via CDN). It communicates with the Python backend via a simple REST API:

- `GET /api/runs`: List recent pipeline runs.
- `GET /api/pipelines`: List available pipelines.
- `POST /api/pipelines/{name}/trigger`: Trigger a new run.
nd
backend = SQLiteBackend("pipeline.db")