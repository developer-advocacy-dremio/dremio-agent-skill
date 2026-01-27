# Case When
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
