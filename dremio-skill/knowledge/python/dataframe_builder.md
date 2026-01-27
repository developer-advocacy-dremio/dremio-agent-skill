# Dataframe Builder

The `DremioBuilder` provides a fluent interface for querying data, similar to Ibis or PySpark.

## Getting a Builder

Start by selecting a table from the client:

```python
from dremioframe.client import DremioClient

client = DremioClient()
df = client.table('finance.bronze.transactions')
```

## Querying Data

You can chain methods to build a query:

```python
result = (
    df.select("transaction_id", "customer_id", "amount")
      .filter("amount > 1000")
      .limit(10)
      .collect()
)

print(result)
```

### Methods

- `select(*cols)`: Select specific columns.
- `mutate(**kwargs)`: Add calculated columns. Example: `.mutate(total="price * quantity")`
    - **Conflict Resolution**: If a mutated column name matches a selected column, the mutation takes precedence.
    - **Implicit Select**: If `select()` is not called, `mutate` preserves all existing columns (equivalent to `SELECT *, mutation AS alias`).
- `filter(condition)`: Add a WHERE clause.
- `limit(n)`: Limit the number of rows.
- `collect(library='polars')`: Execute the query and return a DataFrame. Supported libraries: `polars` (default), `pandas`.
- `show(n=20)`: Print the first `n` rows.

## Query Explanation

You can view the execution plan for a query using the `explain()` method. This is useful for debugging performance issues.

```python
plan = df.filter("amount > 1000").explain()
print(plan)
```

## DML Operations

You can also perform Data Manipulation Language (DML) operations:

```python
# Create Table As Select (CTAS)
df.filter("amount > 5000").create("finance.silver.large_transactions")

# Insert into existing table from query
df.filter("amount > 10000").insert("finance.silver.large_transactions")

# Insert from Pandas DataFrame or Arrow Table
import pandas as pd
data = pd.DataFrame({"transaction_id": [1001], "customer_id": [5], "amount": [15000.00]})
client.table("finance.silver.large_transactions").insert("finance.silver.large_transactions", data=data)

# Update rows
client.table("finance.bronze.transactions").filter("transaction_id = 1001").update({"amount": 16000.00})

# Delete rows
client.table("finance.bronze.transactions").filter("amount < 0").delete()

## Slowly Changing Dimensions (SCD2)

The `scd2` method automates the process of maintaining Type 2 Slowly Changing Dimensions. It closes old records (updates `valid_to`) and inserts new records (`valid_from`).

```python
builder.table("source_view").scd2(
    target_table="target_dim",
    on=["id"],
    track_cols=["name", "status"],
    valid_from_col="valid_from",
    valid_to_col="valid_to"
)
```

This executes two operations:
1. **Close**: Updates `valid_to` to `CURRENT_TIMESTAMP` for records in `target_dim` that have changed in `source_view`.
2. **Insert**: Inserts new versions of changed records and completely new records from `source_view` into `target_dim`.

## Merge (Upsert)

You can perform `MERGE INTO` operations to upsert data.

```python
