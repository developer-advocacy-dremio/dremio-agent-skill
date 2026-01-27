# Iceberg Management


---

## Guide: Iceberg Lakehouse Management

DremioFrame provides powerful tools to manage your Iceberg tables directly from Python. This guide covers maintenance tasks, snapshot management, and time travel.

## Table Maintenance

Regular maintenance is crucial for Iceberg table performance.

### Optimization (Compaction)

Compacts small files into larger ones to improve read performance.

```python
from dremioframe.client import DremioClient

client = DremioClient(...)

# Optimize a specific table
client.table("warehouse.sales").optimize()

# Optimize with specific file size target (if supported by Dremio version/source)
# client.table("warehouse.sales").optimize(target_size_mb=128)
```

### Vacuum (Expire Snapshots & Remove Orphan Files)

Removes old snapshots and unused data files to reclaim space.

```python
# Expire snapshots older than 7 days
client.table("warehouse.sales").vacuum(retain_days=7)
```

## Snapshot Management

### Viewing Snapshots

Inspect the history of your table.

```python
history = client.table("warehouse.sales").history()
print(history)
# Returns a DataFrame with snapshot_id, committed_at, etc.
```

### Time Travel

Query the table as it existed at a specific point in time.

```python
# Query by Snapshot ID
df_snapshot = client.table("warehouse.sales").at(snapshot_id=123456789).collect()

# Query by Timestamp
df_time = client.table("warehouse.sales").at(timestamp="2023-01-01 12:00:00").collect()
```

### Rollback

Revert the table state to a previous snapshot.

```python
# Rollback to a specific snapshot
client.table("warehouse.sales").rollback(snapshot_id=123456789)
```

## Orchestrating Maintenance

You can automate these tasks using DremioFrame's Orchestration features.

```python
from dremioframe.orchestration import Pipeline, OptimizeTask, VacuumTask

pipeline = Pipeline("weekly_maintenance")

optimize = OptimizeTask(
    name="optimize_sales",
    client=client,
    table="warehouse.sales"
)

vacuum = VacuumTask(
    name="vacuum_sales",
    client=client,
    table="warehouse.sales",
    retain_days=7
)

pipeline.add_task(optimize)
pipeline.add_task(vacuum)

# Ensure vacuum runs after optimize
vacuum.set_upstream(optimize)

pipeline.run()
```


---

<!-- Source: docs/data_engineering/iceberg.md -->

---

## Iceberg Client

Interact directly with Dremio's Iceberg Catalog using `pyiceberg`.

---

## Iceberg Client

Interact directly with Dremio's Iceberg Catalog using `pyiceberg`.

## Configuration

The Iceberg client requires specific configuration depending on whether you are using Dremio Cloud or Dremio Software.

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DREMIO_PAT` | Personal Access Token | Yes | None |
| `DREMIO_PROJECT_ID` | Project Name (Cloud) or Warehouse Name | Yes (Cloud) | None |
| `DREMIO_ICEBERG_URI` | Iceberg Catalog REST URI | No (Cloud), Yes (Software) | `https://catalog.dremio.cloud/api/iceberg` |

### Dremio Cloud

For Dremio Cloud, you typically only need `DREMIO_PAT` and `DREMIO_PROJECT_ID`.

```bash
export DREMIO_PAT="your_pat"
export DREMIO_PROJECT_ID="your_project_id"
```

### Dremio Software

For Dremio Software, you must specify the `DREMIO_ICEBERG_URI`.

```bash
export DREMIO_PAT="your_pat"
export DREMIO_ICEBERG_URI="http://dremio-host:9047/api/iceberg"
# DREMIO_PROJECT_ID can be any string for Software, but is required by PyIceberg
export DREMIO_PROJECT_ID="my_warehouse" 
```

## Usage

### Access the Client

```python
iceberg = client.iceberg
```

### List Namespaces

```python
namespaces = iceberg.list_namespaces()
print(namespaces)
```

### List Tables

```python
tables = iceberg.list_tables("my_namespace")
print(tables)
```

### Load Table

```python
table = iceberg.load_table("my_namespace.my_table")
print(table.schema())
```

### Append Data

Append a Pandas DataFrame to an Iceberg table.

```python
import pandas as pd
df = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})

iceberg.append("my_namespace.my_table", df)
```

### Create Table

```python
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, IntegerType, StringType

schema = Schema(
    NestedField(1, "id", IntegerType(), required=True),
    NestedField(2, "name", StringType(), required=False),
)

table = iceberg.create_table("my_namespace.new_table", schema)
```


---

<!-- Source: docs/data_engineering/incremental_processing.md -->

---

## Iceberg Maintenance Tasks

`dremioframe` simplifies Iceberg table maintenance with pre-built tasks.

## OptimizeTask

Runs `OPTIMIZE TABLE` to compact small files.

### Arguments
-   `name` (str): The unique name of the task.
-   `client` (DremioClient): The authenticated Dremio client.
-   `table` (str): The full path to the Iceberg table (e.g., `source.folder.table`).
-   `rewrite_data_files` (bool, default=True): Whether to include `REWRITE DATA USING BIN_PACK`.

### Example
```python
from dremioframe.orchestration import OptimizeTask

t_opt = OptimizeTask(
    name="optimize_sales",
    client=client,
    table="my_catalog.sales",
    rewrite_data_files=True
)
```

## VacuumTask

Runs `VACUUM TABLE` to remove unused files and expire snapshots.

### Arguments
-   `name` (str): The unique name of the task.
-   `client` (DremioClient): The authenticated Dremio client.
-   `table` (str): The full path to the Iceberg table.
-   `expire_snapshots` (bool, default=True): Whether to include `EXPIRE SNAPSHOTS`.
-   `retain_last` (int, optional): Number of recent snapshots to retain.
-   `older_than` (str, optional): Timestamp string (e.g., '2023-01-01 00:00:00') to expire snapshots older than.

### Example
```python
from dremioframe.orchestration import VacuumTask

t_vac = VacuumTask(
    name="vacuum_sales",
    client=client,
    table="my_catalog.sales",
    expire_snapshots=True,
    retain_last=5,
    older_than="2023-10-01 00:00:00"
)
```

## ExpireSnapshotsTask

A specialized wrapper for expiring snapshots.

### Arguments
-   `name` (str): The unique name of the task.
-   `client` (DremioClient): The authenticated Dremio client.
-   `table` (str): The full path to the Iceberg table.
-   `retain_last` (int, default=5): Number of recent snapshots to retain.

### Example
```python
from dremioframe.orchestration import ExpireSnapshotsTask

t_exp = ExpireSnapshotsTask(
    name="expire_sales",
    client=client,
    table="my_catalog.sales",
    retain_last=3
)
```


---

<!-- Source: docs/orchestration/overview.md -->

---

## Schema Evolution

DremioFrame provides tools to manage schema evolution for your Dremio tables, allowing you to detect changes and generate migration scripts.

## SchemaManager

The `SchemaManager` class helps you compare the current schema of a table in Dremio against a desired schema (e.g., from your code or a config file) and synchronize them.

### Initialization

```python
from dremioframe.client import DremioClient
from dremioframe.schema_evolution import SchemaManager

client = DremioClient()
manager = SchemaManager(client)
```

### Comparing Schemas

You can compare the current table schema with a new schema definition.

```python
# Define desired schema
new_schema = {
    "id": "INT",
    "name": "VARCHAR",
    "email": "VARCHAR",
    "created_at": "TIMESTAMP"
}

# Get current schema
current_schema = manager.get_table_schema("space.folder.users")

# Compare
diff = manager.compare_schemas(current_schema, new_schema)

print("Added:", diff['added_columns'])
print("Removed:", diff['removed_columns'])
print("Changed:", diff['changed_columns'])
```

### Generating Migration Scripts

Generate SQL statements to migrate the table.

```python
sqls = manager.generate_migration_sql("space.folder.users", diff)

for sql in sqls:
    print(sql)
# Output:
# ALTER TABLE space.folder.users ADD COLUMN email VARCHAR
```

### Syncing Table

Automatically apply changes (or dry run).

```python
# Dry run (default) - returns SQL statements
sqls = manager.sync_table("space.folder.users", new_schema, dry_run=True)

# Execute changes
manager.sync_table("space.folder.users", new_schema, dry_run=False)
```

## Limitations

- **Type Changes**: Changing column types is complex and may not be supported directly by Dremio for all table formats. The tool generates a warning comment for type changes.
- **Data Migration**: This tool handles schema changes (DDL), not data transformation.
- **Iceberg Support**: Works best with Iceberg tables which support full schema evolution.


---

<!-- Source: docs/data_engineering/sorting.md -->

---

## Slowly Changing Dimensions (SCD)

Slowly Changing Dimensions (SCD) are techniques used in data warehousing to manage how data changes over time. DremioFrame provides support for the two most common types: Type 1 and Type 2.

## Type 1 (Overwrite)

SCD Type 1 overwrites the old data with the new data. No history is kept. This is useful for correcting errors or when historical values are not significant (e.g., correcting a spelling mistake in a name).

### Implementation

Use the `merge` method to perform an upsert (Update if exists, Insert if new).

```python
# Source data contains the latest state of users
new_user_data = client.table("staging.users")

# Target dimension table
target_table = "gold.dim_users"

# Perform Merge
client.table(target_table).merge(
    target_table=target_table,
    on="user_id",
    matched_update={
        "email": "source.email", 
        "status": "source.status",
        "updated_at": "CURRENT_TIMESTAMP"
    },
    not_matched_insert={
        "user_id": "source.user_id", 
        "email": "source.email", 
        "status": "source.status",
        "created_at": "CURRENT_TIMESTAMP",
        "updated_at": "CURRENT_TIMESTAMP"
    },
    data=new_user_data
)
```

## Type 2 (History)

SCD Type 2 tracks historical data by creating multiple records for a given natural key, each representing a specific time range. This allows you to query the state of a record at any point in the past.

### Table Design

To use SCD2, your target table must be designed with two special columns to track the validity period of each record:

- **`valid_from`** (TIMESTAMP): The time when the record became active.
- **`valid_to`** (TIMESTAMP): The time when the record ceased to be active. `NULL` indicates the current active record.

### Using the Helper

DremioFrame provides a `scd2` helper method to automate the complex logic of closing old records and inserting new ones.

```python
from dremioframe.client import DremioClient

client = DremioClient(...)

# Define your source (e.g., a staging table or view)
source = client.table("staging.customers")

# Apply SCD2 logic to the target dimension table
# This generates and executes the necessary SQL statements
source.scd2(
    target_table="warehouse.dim_customers",
    on=["id"],                      # Natural key(s) to join on
    track_cols=["name", "status"],  # Columns to check for changes
    valid_from_col="valid_from",    # Name of your valid_from column
    valid_to_col="valid_to"         # Name of your valid_to column
)
```

### Before and After Example

#### Initial State (Target Table)

| id | name | status | valid_from | valid_to |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Alice | Active | 2023-01-01 10:00:00 | NULL |
| 2 | Bob | Active | 2023-01-01 10:00:00 | NULL |

#### Source Data (New Batch)

| id | name | status |
| :--- | :--- | :--- |
| 1 | Alice | Inactive |  <-- Changed Status
| 2 | Bob | Active |      <-- No Change
| 3 | Charlie | Active |  <-- New Record

#### After `scd2` Execution

| id | name | status | valid_from | valid_to | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Alice | Active | 2023-01-01 10:00:00 | **2023-01-02 12:00:00** | Closed (Old Version) |
| 1 | Alice | Inactive | **2023-01-02 12:00:00** | NULL | **New Version** |
| 2 | Bob | Active | 2023-01-01 10:00:00 | NULL | Unchanged |
| 3 | Charlie | Active | **2023-01-02 12:00:00** | NULL | **New Record** |

### Logic Breakdown

1.  **Identify Changes**: The method joins the source and target on `id`. It compares `name` and `status`.
2.  **Update**: For ID 1, `status` changed. The old record (where `valid_to` is NULL) is updated with `valid_to = NOW()`.
3.  **Insert**:
    -   ID 1 (New Version): Inserted with `valid_from = NOW()`, `valid_to = NULL`.
    -   ID 3 (New Record): Inserted with `valid_from = NOW()`, `valid_to = NULL`.
    -   ID 2: Ignored because it matched and no columns changed.


---

<!-- Source: docs/modeling/views.md -->