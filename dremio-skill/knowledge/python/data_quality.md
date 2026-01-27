# Data Quality

## Data Quality Framework

DremioFrame includes a file-based Data Quality (DQ) framework to validate your data in Dremio.

## Requirements
```bash
pip install "dremioframe[dq]"
```

## Defining Tests

Tests are defined in YAML files. You can place them in any directory.

**Example: `tests/dq/sales_checks.yaml`**
```yaml
tests:
  - name: Validate Sales Table
    table: "Space.Folder.Sales"
    checks:
      - type: not_null
        column: order_id
        
      - type: unique
        column: order_id
        
      - type: values_in
        column: status
        values: ["PENDING", "SHIPPED", "DELIVERED", "CANCELLED"]
        
      - type: row_count
        condition: "amount < 0"
        threshold: 0
        operator: eq  # Expect 0 rows where amount < 0
        
      - type: custom_sql
        condition: "discount > amount"
        error_msg: "Discount cannot be greater than amount"
```

## Running Tests

Use the CLI to run tests in a directory.

```bash
dremio-cli dq run tests/dq
```

## Check Types

| Type | Description | Parameters |
|------|-------------|------------|
| `not_null` | Ensures a column has no NULL values. | `column` |
| `unique` | Ensures a column has unique values. | `column` |
| `values_in` | Ensures column values are within a list. | `column`, `values` |
| `row_count` | Checks row count matching a condition. | `condition`, `threshold`, `operator` (eq, ne, gt, lt, ge, le) |
| `custom_sql` | Fails if any row matches the condition. | `condition`, `error_msg` |


---

<!-- Source: docs/data_quality/recipes.md -->

---

## AI Data Quality Tools

The `DremioAgent` can automatically generate Data Quality (DQ) recipes for your datasets.

## Features

### 1. Automated Recipe Generation
The agent inspects a dataset's schema (columns and types) and generates a YAML configuration file for the DremioFrame Data Quality framework. It intelligently suggests checks like `not_null` for IDs and `unique` for primary keys.

-   **Tool**: `generate_dq_checks(table)`
-   **Method**: `agent.generate_dq_recipe(table)`

## Usage Examples

### Generating a Recipe

```python
from dremioframe.ai.agent import DremioAgent

agent = DremioAgent()

# Generate a DQ recipe for a table
table_name = "sales.transactions"
recipe = agent.generate_dq_recipe(table_name)

print("Generated DQ Recipe:")
print(recipe)

# You can save this to a file
with open("dq_checks.yaml", "w") as f:
    f.write(recipe)
```

### Example Output

```yaml
table: sales.transactions
checks:
  - column: transaction_id
    tests:
      - not_null
      - unique
  - column: amount
    tests:
      - positive
```


---

<!-- Source: docs/ai/document_extraction.md -->

---

## Check cost before running expensive query
estimate = estimator.estimate_query_cost(expensive_sql)

if estimate.total_cost > 1000:
    print("Warning: This query may be expensive!")
    print("Hints:", estimate.optimization_hints)
    # Decide whether to proceed
```

### 2. Query Optimization Workflow

```python

---

## Check that 'customer_id' is never NULL
df.quality.expect_not_null("customer_id")

---

## Check that 'status' is one of the allowed values
df.quality.expect_values_in("status", ["completed", "pending", "cancelled"])

---

## Check that there are at least 100 rows total
df.quality.expect_row_count("1=1", 100, "ge")
```

```


---

<!-- Source: docs/data_engineering/caching.md -->

---

## Check that there are exactly 0 rows where amount is negative
df.quality.expect_row_count("amount < 0", 0, "eq")

---

## Check that 'transaction_id' is unique
df.quality.expect_unique("transaction_id")

---

## Custom Check: Row Count

---

## Data Quality Recipes

This guide provides common patterns and recipes for validating your data using DremioFrame's Data Quality framework.

## Recipe 1: Validating Reference Data

Ensure that reference tables (like country codes or status lookups) contain expected values and no duplicates.

```yaml
- name: "Validate Country Codes"
  table: "reference.countries"
  checks:
    - type: "unique"
      column: "iso_code"
    
    - type: "not_null"
      column: "country_name"
      
    - type: "row_count"
      threshold: 190
      operator: "gt"
```

## Recipe 2: Financial Integrity Checks

Validate financial transactions for non-negative amounts and referential integrity (via custom SQL).

```yaml
- name: "Transaction Integrity"
  table: "finance.transactions"
  checks:
    - type: "custom_sql"
      condition: "MIN(amount) >= 0"
      error_msg: "Found negative transaction amounts"
      
    - type: "not_null"
      column: "transaction_date"
      
    # Check that all transactions belong to valid accounts (simplified referential integrity)
    - type: "custom_sql"
      condition: "(SELECT COUNT(*) FROM finance.transactions t LEFT JOIN finance.accounts a ON t.account_id = a.id WHERE a.id IS NULL) = 0"
      error_msg: "Found transactions for non-existent accounts"
```

## Recipe 3: Daily Ingestion Validation

Verify that a daily ingestion job loaded data correctly by checking row counts and freshness.

```yaml
- name: "Daily Web Logs"
  table: "raw.web_logs"
  checks:
    # Ensure we loaded at least some rows
    - type: "row_count"
      threshold: 0
      operator: "gt"
      
    # Ensure data is from today (assuming 'event_timestamp' column)
    - type: "custom_sql"
      condition: "MAX(event_timestamp) >= CURRENT_DATE"
      error_msg: "No data loaded for today"
```

## Recipe 4: Categorical Data Validation

Ensure columns with categorical data only contain allowed values.

```yaml
- name: "User Status Validation"
  table: "users.profiles"
  checks:
    - type: "values_in"
      column: "subscription_tier"
      values: ["free", "basic", "premium", "enterprise"]
      
    - type: "values_in"
      column: "email_verified"
      values: [true, false]
```

## Recipe 5: Running Tests Programmatically

You can run these YAML recipes from your Python code using the `DQRunner`.

```python
from dremioframe.client import DremioClient
from dremioframe.dq.runner import DQRunner

client = DremioClient()
runner = DQRunner(client)

# Load tests from a directory containing your YAML files
tests = runner.load_tests("./dq_checks")

# Run all loaded tests
success = runner.run_tests(tests)

if not success:
    print("Data Quality checks failed!")
    exit(1)
```


---

<!-- Source: docs/data_quality/yaml_syntax.md -->

---

## Data Quality Task

The `DataQualityTask` integrates the Data Quality Framework into your orchestration pipelines. It allows you to run a suite of DQ checks as a step in your DAG. If any check fails, the task fails, halting the pipeline (unless handled).

## Usage

```python
from dremioframe.orchestration import Pipeline
from dremioframe.orchestration.tasks.dq_task import DataQualityTask
from dremioframe.client import DremioClient

client = DremioClient()
pipeline = Pipeline("dq_pipeline")

# Run checks from a directory
dq_task = DataQualityTask(
    name="run_sales_checks",
    client=client,
    directory="tests/dq"
)

pipeline.add_task(dq_task)
pipeline.run()
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `name` | `str` | Name of the task. |
| `client` | `DremioClient` | Authenticated Dremio client. |
| `directory` | `str` | Path to a directory containing YAML test files. |
| `tests` | `list` | List of test dictionaries (alternative to directory). |

## Behavior

- **Success**: If all checks pass, the task completes successfully.
- **Failure**: If any check fails, the task raises a `RuntimeError`, marking the task as failed.


---

<!-- Source: docs/orchestration/dremio_jobs.md -->

---

## Data Quality YAML Syntax

DremioFrame's Data Quality framework allows you to define tests in YAML files. This enables a declarative approach to data quality, where checks are version-controlled and separated from your application code.

## File Structure

A Data Quality YAML file can contain a list of test definitions. Each test targets a specific table and contains a list of checks to perform.

### Root Element

The root of the YAML file can be:
1. A **list** of test objects.
2. A **dictionary** with a `tests` key containing a list of test objects.

### Test Object

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | string | No | A descriptive name for the test suite. Defaults to "Unnamed Test". |
| `table` | string | **Yes** | The full path to the Dremio table or view being tested (e.g., `source.folder.table`). |
| `checks` | list | **Yes** | A list of check objects to execute against the table. |

### Check Object

Every check object requires a `type` field. Other fields depend on the check type.

#### `not_null`
Ensures a column contains no NULL values.

| Field | Type | Description |
| :--- | :--- | :--- |
| `type` | string | Must be `not_null`. |
| `column` | string | The name of the column to check. |

#### `unique`
Ensures all values in a column are unique.

| Field | Type | Description |
| :--- | :--- | :--- |
| `type` | string | Must be `unique`. |
| `column` | string | The name of the column to check. |

#### `values_in`
Ensures column values are within a specified allowed list.

| Field | Type | Description |
| :--- | :--- | :--- |
| `type` | string | Must be `values_in`. |
| `column` | string | The name of the column to check. |
| `values` | list | A list of allowed values (strings, numbers, etc.). |

#### `row_count`
Validates the total number of rows in the table based on a condition.

| Field | Type | Description |
| :--- | :--- | :--- |
| `type` | string | Must be `row_count`. |
| `condition` | string | Optional SQL WHERE clause to filter rows before counting. Default: `1=1` (all rows). |
| `threshold` | number | The value to compare the count against. |
| `operator` | string | Comparison operator: `eq` (=), `gt` (>), `lt` (<), `gte` (>=), `lte` (<=). Default: `gt`. |

#### `custom_sql`
Runs a custom SQL condition that must return TRUE for the check to pass.

| Field | Type | Description |
| :--- | :--- | :--- |
| `type` | string | Must be `custom_sql`. |
| `condition` | string | A SQL boolean expression (e.g., `SUM(amount) > 0`). |
| `error_msg` | string | Optional error message to display if the check fails. |

## Example

```yaml
tests:
  - name: "Customer Table Checks"
    table: "marketing.customers"
    checks:
      - type: "not_null"
        column: "customer_id"
      
      - type: "unique"
        column: "email"
        
      - type: "values_in"
        column: "status"
        values: ["active", "inactive", "pending"]

  - name: "Sales Data Validation"
    table: "sales.transactions"
    checks:
      - type: "row_count"
        threshold: 1000
        operator: "gt"
        
      - type: "custom_sql"
        condition: "SUM(total_amount) > 0"
        error_msg: "Total sales amount must be positive"
```


---

<!-- Source: docs/deployment/cicd.md -->

---

## SQL Linting

DremioFrame provides a `SqlLinter` to validate SQL queries against Dremio and perform static code analysis to catch common issues.

## SqlLinter

The `SqlLinter` can validate queries by requesting an execution plan from Dremio (ensuring syntax and table references are correct) and by checking for patterns that might lead to poor performance or unexpected results.

### Initialization

```python
from dremioframe.client import DremioClient
from dremioframe.linter import SqlLinter

client = DremioClient()
linter = SqlLinter(client)
```

### Validating SQL

Validation runs `EXPLAIN PLAN FOR <query>` against Dremio. This confirms that the SQL syntax is valid and that all referenced tables and columns exist and are accessible.

```python
sql = "SELECT count(*) FROM space.folder.table"
result = linter.validate_sql(sql)

if result["valid"]:
    print("SQL is valid!")
else:
    print(f"Validation failed: {result['error']}")
```

### Static Linting

Static linting checks the SQL string for common anti-patterns without connecting to Dremio.

```python
sql = "SELECT * FROM huge_table"
warnings = linter.lint_sql(sql)

for warning in warnings:
    print(f"Warning: {warning}")
# Output: Warning: Avoid 'SELECT *' in production queries. Specify columns explicitly.
```

### Rules Checked

- **SELECT \***: Discourages selecting all columns in production.
- **Unbounded DELETE/UPDATE**: Warns if `DELETE` or `UPDATE` statements are missing a `WHERE` clause.


---

<!-- Source: docs/data_quality/framework.md -->

---

## Will raise ValidationError if data doesn't match
client.table("users").insert("users", data=df, schema=User)
```

## Data Quality Checks

You can run data quality checks on a builder instance. These checks execute queries to verify assumptions about the data.

```python