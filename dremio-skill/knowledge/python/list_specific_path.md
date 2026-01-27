# List specific path
dremio-cli catalog --path "source.folder"
```

### List Reflections

```bash
dremio-cli reflections
```


---

<!-- Source: docs/reference/client.md -->

# Client API Reference

::: dremioframe.client.DremioClient
    options:
      show_root_heading: true
      show_source: true

::: dremioframe.client.AsyncDremioClient
    options:
      show_root_heading: true
      show_source: true

# Client Helpers

These classes are accessed via properties on the `DremioClient` instance (e.g., `client.admin`, `client.catalog`).

## Admin

::: dremioframe.admin.Admin
    options:
      show_root_heading: true
      show_source: true

## Catalog

::: dremioframe.catalog.Catalog
    options:
      show_root_heading: true
      show_source: true

## Iceberg

::: dremioframe.iceberg.Iceberg
    options:
      show_root_heading: true
      show_source: true

## UDF

::: dremioframe.udf.UDF
    options:
      show_root_heading: true
      show_source: true

## Profile

::: dremioframe.profile.Profile
    options:
      show_root_heading: true
      show_source: true


---

<!-- Source: docs/reference/dq.md -->

# Data Quality API Reference

::: dremioframe.dq.runner.DQRunner
    options:
      show_root_heading: true

::: dremioframe.dq.checks.DataQuality
    options:
      show_root_heading: true


---

<!-- Source: docs/reference/function_reference.md -->

# Function Reference

This document lists the SQL functions supported by `dremioframe.functions`.

## General Functions

- `col(name)`: Creates a column expression.
- `lit(val)`: Creates a literal expression.

## Aggregates

- `sum(col)`: Calculates the sum of a column.
- `avg(col)`: Calculates the average of a column.
- `min(col)`: Finds the minimum value in a column.
- `max(col)`: Finds the maximum value in a column.
- `count(col)`: Counts the number of non-null values in a column.
- `stddev(col)`: Calculates the standard deviation.
- `variance(col)`: Calculates the variance.
- `approx_distinct(col)`: Approximates the count of distinct values.

## Math

- `abs(col)`: Absolute value.
- `ceil(col)`: Ceiling.
- `floor(col)`: Floor.
- `round(col, scale=0)`: Rounds to the specified scale.
- `sqrt(col)`: Square root.
- `exp(col)`: Exponential.
- `ln(col)`: Natural logarithm.
- `log(base, col)`: Logarithm with specified base.
- `pow(col, power)`: Power.

## String

- `upper(col)`: Converts to uppercase.
- `lower(col)`: Converts to lowercase.
- `concat(*cols)`: Concatenates strings.
- `substr(col, start, length=None)`: Substring.
- `trim(col)`: Trims whitespace from both ends.
- `ltrim(col)`: Trims whitespace from left.
- `rtrim(col)`: Trims whitespace from right.
- `length(col)`: String length.
- `replace(col, pattern, replacement)`: Replaces occurrences of pattern.
- `regexp_replace(col, pattern, replacement)`: Replaces using regex.
- `initcap(col)`: Capitalizes first letter of each word.

## Date/Time

- `current_date()`: Current date.
- `current_timestamp()`: Current timestamp.
- `date_add(col, days)`: Adds days to date.
- `date_sub(col, days)`: Subtracts days from date.
- `date_diff(col1, col2)`: Difference in days between dates.
- `to_date(col, fmt=None)`: Converts string to date.
- `to_timestamp(col, fmt=None)`: Converts string to timestamp.
- `year(col)`: Extracts year.
- `month(col)`: Extracts month.
- `day(col)`: Extracts day.
- `hour(col)`: Extracts hour.
- `minute(col)`: Extracts minute.
- `second(col)`: Extracts second.
- `extract(field, source)`: Extracts field from source.

## Conditional

- `coalesce(*cols)`: Returns first non-null value.
- `when(condition, value)`: Starts a CASE statement builder.

## Window Functions

- `rank()`: Rank.
- `dense_rank()`: Dense rank.
- `row_number()`: Row number.
- `lead(col, offset=1, default=None)`: Lead.
- `lag(col, offset=1, default=None)`: Lag.
- `first_value(col)`: First value in window.
- `last_value(col)`: Last value in window.
- `ntile(n)`: N-tile.

## AI Functions

- `ai_classify(prompt, categories, model_name=None)`: Classifies text into categories.
- `ai_complete(prompt, model_name=None)`: Generates text completion.
- `ai_generate(prompt, model_name=None, schema=None)`: Generates structured data.

## Complex Types

- `flatten(col)`: Explodes a list into multiple rows.
- `convert_from(col, type_)`: Converts from serialized format.
- `convert_to(col, type_)`: Converts to serialized format.


---

<!-- Source: docs/reference/functions/aggregate.md -->

# Aggregate Functions

Aggregate functions operate on a set of values to compute a single result.

## Usage

```python
from dremioframe import F

df.group_by("dept").agg(
    total=F.sum("salary"),
    count=F.count("*")
)
```

## Available Functions

| Function | Description |
| :--- | :--- |
| `sum(col)` | Returns the sum of values in the column. |
| `avg(col)` | Returns the average of values in the column. |
| `min(col)` | Returns the minimum value. |
| `max(col)` | Returns the maximum value. |
| `count(col)` | Returns the count of non-null values. Use `*` for total rows. |
| `stddev(col)` | Returns the sample standard deviation. |
| `variance(col)` | Returns the sample variance. |
| `approx_distinct(col)` | Returns the approximate number of distinct values (HyperLogLog). |


---

<!-- Source: docs/reference/functions/ai.md -->

# AI Functions

Dremio provides AI-powered functions for classification, text completion, and structured data generation.

## Usage

```python
from dremioframe import F

