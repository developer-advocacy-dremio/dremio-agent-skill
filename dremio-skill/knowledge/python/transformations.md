# Transformations

## Aggregation

DremioFrame supports standard SQL aggregation using `group_by` and `agg`.

## Group By

Use `group_by` to group rows by one or more columns.

```python
df.group_by("state")
df.group_by("state", "city")
```

## Aggregation

Use `agg` to define aggregation expressions. The keys become the new column names.

```python
# Calculate average population by state
df.group_by("state").agg(
    avg_pop="AVG(pop)",
    max_pop="MAX(pop)",
    count="COUNT(*)"
).show()
```

This generates SQL like:
```sql
SELECT AVG(pop) AS avg_pop, MAX(pop) AS max_pop, COUNT(*) AS count 
FROM table 
GROUP BY state
```


---

<!-- Source: docs/data_engineering/builder.md -->

---

## Case When
df.select(
    F.when("age < 18", "Minor")
     .when("age < 65", "Adult")
     .otherwise("Senior").alias("age_group")
)
```

## Available Functions

| Function | Description |
| :--- | :--- |
| `coalesce(*cols)` | Returns the first non-null value. |
| `when(cond, val).otherwise(val)` | CASE WHEN statement builder. |


---

<!-- Source: docs/reference/functions/date.md -->

# Date & Time Functions

Functions for date and time manipulation.

## Usage

```python
from dremioframe import F

df.select(
    F.year(F.col("date")),
    F.date_add(F.col("date"), 7)
)
```

## Available Functions

| Function | Description |
| :--- | :--- |
| `current_date()` | Current date. |
| `current_timestamp()` | Current timestamp. |
| `date_add(col, days)` | Add days to date. |
| `date_sub(col, days)` | Subtract days from date. |
| `date_diff(col1, col2)` | Difference in days between dates. |
| `to_date(col, fmt)` | Convert string to date. |
| `to_timestamp(col, fmt)` | Convert string to timestamp. |
| `year(col)` | Extract year. |
| `month(col)` | Extract month. |
| `day(col)` | Extract day. |
| `hour(col)` | Extract hour. |
| `minute(col)` | Extract minute. |
| `second(col)` | Extract second. |
| `extract(field, source)` | Extract specific field (e.g., 'YEAR' from date). |


---

<!-- Source: docs/reference/functions/math.md -->

# Math Functions

Mathematical functions for numeric operations.

## Usage

```python
from dremioframe import F

df.select(
    F.abs(F.col("diff")),
    F.round(F.col("price"), 2)
)
```

## Available Functions

| Function | Description |
| :--- | :--- |
| `abs(col)` | Absolute value. |
| `ceil(col)` | Ceiling (round up). |
| `floor(col)` | Floor (round down). |
| `round(col, scale=0)` | Round to specified decimal places. |
| `sqrt(col)` | Square root. |
| `exp(col)` | Exponential (e^x). |
| `ln(col)` | Natural logarithm. |
| `log(base, col)` | Logarithm with specified base. |
| `pow(col, power)` | Power (x^y). |


---

<!-- Source: docs/reference/functions/string.md -->

# String Functions

Functions for string manipulation.

## Usage

```python
from dremioframe import F

df.select(
    F.upper(F.col("name")),
    F.concat(F.col("first"), F.lit(" "), F.col("last"))
)
```

## Available Functions

| Function | Description |
| :--- | :--- |
| `upper(col)` | Convert to uppercase. |
| `lower(col)` | Convert to lowercase. |
| `concat(*cols)` | Concatenate strings. |
| `substr(col, start, length)` | Extract substring. |
| `trim(col)` | Trim whitespace from both ends. |
| `ltrim(col)` | Trim whitespace from left. |
| `rtrim(col)` | Trim whitespace from right. |
| `length(col)` | Length of string. |
| `replace(col, pattern, replacement)` | Replace substring. |
| `regexp_replace(col, pattern, replacement)` | Replace using regex. |
| `initcap(col)` | Capitalize first letter of each word. |


---

<!-- Source: docs/reference/functions/window.md -->

# Window Functions

Window functions operate on a set of rows related to the current row.

## Usage

```python
from dremioframe import F

window = F.Window.partition_by("dept").order_by("salary")

df.select(
    F.rank().over(window).alias("rank")
)
```

## Window Specification

Use `F.Window` to create a specification:
- `partition_by(*cols)`
- `order_by(*cols)`
- `rows_between(start, end)`
- `range_between(start, end)`

## Available Functions

| Function | Description |
| :--- | :--- |
| `rank()` | Rank with gaps. |
| `dense_rank()` | Rank without gaps. |
| `row_number()` | Unique row number. |
| `lead(col, offset, default)` | Value from following row. |
| `lag(col, offset, default)` | Value from preceding row. |
| `first_value(col)` | First value in window frame. |
| `last_value(col)` | Last value in window frame. |
| `ntile(n)` | Distribute rows into n buckets. |


---

<!-- Source: docs/reference/functions.md -->

# SQL Functions API Reference

Helper functions for constructing SQL expressions (e.g., `F.col("a")`, `F.sum("b")`).

::: dremioframe.functions
    options:
      show_root_heading: true
      show_source: true
      members:
        - col
        - lit
        - sum
        - avg
        - min
        - max
        - count
        - row_number
        - rank
        - dense_rank
        - Window


---

<!-- Source: docs/reference/functions_guide.md -->

# SQL Functions

DremioFrame provides a comprehensive set of SQL functions via `dremioframe.functions` (aliased as `F`).

## Categories

- [Aggregate Functions](functions/aggregate.md)
- [Math Functions](functions/math.md)
- [String Functions](functions/string.md)
- [Date & Time Functions](functions/date.md)
- [Window Functions](functions/window.md)
- [Conditional Functions](functions/conditional.md)
- [AI Functions](functions/ai.md)
- [Complex Type Functions](functions/complex.md)

## Usage

You can use functions in two ways:

### 1. Function Builder (Recommended)

Import `F` and chain methods. This provides autocomplete and type safety.

```python
from dremioframe import F

df.select(
    F.col("name"),
    F.upper(F.col("city")),
    F.sum("salary").over(F.Window.partition_by("dept"))
)
```

### 2. Raw SQL Strings

You can write raw SQL strings directly in `mutate` or `select`. This is useful for complex expressions or functions not yet wrapped in `dremioframe`.

```python

---

## Coalesce
df.select(F.coalesce(F.col("phone"), F.col("email"), F.lit("Unknown")))

---

## Convert from JSON
df.select(F.convert_from("json_col", "JSON"))

---

## Convert to JSON
df.select(F.convert_to("map_col", "JSON"))
```

## Available Functions

| Function | Description |
| :--- | :--- |
| `flatten(col)` | Explodes a list into multiple rows. |
| `convert_from(col, type)` | Convert from a serialized format (e.g. 'JSON') to a complex type. |
| `convert_to(col, type)` | Convert a complex type to a serialized format (e.g. 'JSON'). |


---

<!-- Source: docs/reference/functions/conditional.md -->

# Conditional Functions

Functions for conditional logic.

## Usage

```python
from dremioframe import F

---

## Fetches ALL data, then filters in Python
df = client.table("sales").collect()
filtered_df = df.filter(pl.col("amount") > 100)
```

**Good Pattern (Server-Side Filtering):**
```python

---

## Filters in Dremio, fetches only matching rows
df = client.table("sales").filter("amount > 100").collect()
```

## 3. Parallelism

### Pipeline Parallelism
Use the `orchestration` module to run independent tasks in parallel.

```python
pipeline = Pipeline("etl", max_workers=4)
```

### Async Client
For high-concurrency applications (e.g., a web app backend), use `AsyncDremioClient` to avoid blocking the main thread while waiting for Dremio.

```python
async with AsyncDremioClient() as client:
    result = await client.query("SELECT * FROM large_table")
```

## 4. Caching

If you query the same dataset multiple times in a script, cache it locally.

```python

---

## Flatten an array
df.select(F.flatten("items"))

---

## In mutate
df.mutate(
    upper_city="UPPER(city)",
    total_salary="SUM(salary) OVER (PARTITION BY dept)"
)

---

## In select
df.select(
    "name",
    "UPPER(city) AS upper_city"
)
```

## Expressions (`Expr`)

The `Expr` class allows you to build complex SQL expressions using Python operators.

- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Comparison**: `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Logical**: `&` (AND), `|` (OR), `~` (NOT)
- **Methods**:
    - `alias(name)`: Rename the expression.
    - `cast(type)`: Cast to a SQL type.
    - `isin(values)`: Check if value is in a list.
    - `is_null()`, `is_not_null()`: Check for NULLs.


---

<!-- Source: docs/reference/orchestration.md -->

# Orchestration API Reference

## Pipeline

::: dremioframe.orchestration.pipeline.Pipeline
    options:
      show_root_heading: true

## Tasks

::: dremioframe.orchestration.task.Task
    options:
      show_root_heading: true

### Dremio Tasks

::: dremioframe.orchestration.tasks.dremio_tasks.DremioQueryTask
    options:
      show_root_heading: true

::: dremioframe.orchestration.tasks.builder_task.DremioBuilderTask
    options:
      show_root_heading: true

### General Tasks

::: dremioframe.orchestration.tasks.general.HttpTask
    options:
      show_root_heading: true

::: dremioframe.orchestration.tasks.general.EmailTask
    options:
      show_root_heading: true

::: dremioframe.orchestration.tasks.general.ShellTask
    options:
      show_root_heading: true

::: dremioframe.orchestration.tasks.general.S3Task
    options:
      show_root_heading: true

### Extension Tasks

::: dremioframe.orchestration.tasks.dbt_task.DbtTask
    options:
      show_root_heading: true

::: dremioframe.orchestration.tasks.dq_task.DataQualityTask
    options:
      show_root_heading: true

### Iceberg Tasks

::: dremioframe.orchestration.iceberg_tasks.OptimizeTask
    options:
      show_root_heading: true

::: dremioframe.orchestration.iceberg_tasks.VacuumTask
    options:
      show_root_heading: true

::: dremioframe.orchestration.iceberg_tasks.ExpireSnapshotsTask
    options:
      show_root_heading: true

### Reflection Tasks

::: dremioframe.orchestration.reflection_tasks.RefreshReflectionTask
    options:
      show_root_heading: true

## Sensors

::: dremioframe.orchestration.sensors.SqlSensor
    options:
      show_root_heading: true

::: dremioframe.orchestration.sensors.FileSensor
    options:
      show_root_heading: true

## Executors

::: dremioframe.orchestration.executors.LocalExecutor
    options:
      show_root_heading: true

::: dremioframe.orchestration.executors.CeleryExecutor
    options:
      show_root_heading: true

## Scheduling

::: dremioframe.orchestration.scheduling.schedule_pipeline
    options:
      show_root_heading: true

## Backends

::: dremioframe.orchestration.backend.BaseBackend
    options:
      show_root_heading: true

::: dremioframe.orchestration.backend.PostgresBackend
    options:
      show_root_heading: true

::: dremioframe.orchestration.backend.MySQLBackend
    options:
      show_root_heading: true

::: dremioframe.orchestration.backend.SQLiteBackend
    options:
      show_root_heading: true

::: dremioframe.orchestration.backend.InMemoryBackend
    options:
      show_root_heading: true


---

<!-- Source: docs/reference/testing.md -->

# Testing Guide

DremioFrame tests are categorized into three groups.

## 1. Unit & Integration (Dremio Cloud)
These tests cover the core logic and integration with Dremio Cloud. They should always pass.

**Requirements:**
- `DREMIO_PAT`: Personal Access Token for Dremio Cloud.
- `DREMIO_PROJECT_ID`: Project ID for Dremio Cloud.
- `DREMIO_TEST_SPACE`: Writable space/folder for integration tests (e.g., "Scratch").

**Command:**
```bash

---

## Joins

DremioFrame allows you to join tables or builder instances.

## Join Syntax

```python
left_df.join(other, on, how='inner')
```

- **other**: Can be a table name (string) or another `DremioBuilder` object.
- **on**: The join condition (SQL string).
- **how**: Join type (`inner`, `left`, `right`, `full`, `cross`).

## Examples

### Join with a Table Name

```python
df = client.table("orders")
joined = df.join("customers", on="left_tbl.customer_id = right_tbl.id", how="left")
joined.show()
```

### Join with Another Builder

This allows you to filter or transform the right-side table before joining.

```python
orders = client.table("orders")
customers = client.table("customers").filter("active = true")

joined = orders.join(customers, on="left_tbl.customer_id = right_tbl.id")
joined.show()
```

### Note on Aliases

When joining, DremioFrame automatically wraps the left and right sides in subqueries aliased as `left_tbl` and `right_tbl` respectively. You should use these aliases in your `on` condition.


---

<!-- Source: docs/data_engineering/pydantic_integration.md -->