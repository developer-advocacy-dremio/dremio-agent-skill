# Performance Tuning

## Cache the result of a heavy query to a local Parquet file
cached_df = client.table("heavy_view").cache("local_cache_name", ttl_seconds=600)

---

## Default batch size is often safe, but for very wide tables, reduce it.
client.table("target").insert("target", data=df, batch_size=5000)
```

### Compression

Flight supports compression (LZ4/ZSTD). DremioFrame negotiates this automatically. Ensure your client machine has CPU cycles to spare for decompression.

## 2. Client-Side vs. Server-Side Processing

Always push filtering and aggregation to Dremio (Server-Side) before collecting data to Python (Client-Side).

**Bad Pattern (Client-Side Filtering):**
```python

---

## Iteratively improve query
queries = [
    "SELECT * FROM large_table",
    "SELECT id, name FROM large_table",
    "SELECT id, name FROM large_table WHERE active = true"
]

comparison = estimator.compare_queries(*queries)
print(f"Best approach: Query {comparison['best_query_id']}")
```

### 3. Automated Query Review

```python

---

## Local Caching with DataFusion

DremioFrame allows you to cache query results locally as Arrow Feather files and query them using the DataFusion python library. This is useful for iterative analysis where you don't want to repeatedly hit the Dremio engine for the same data.

## Usage

Use the `cache()` method on a `DremioBuilder` object.

```python
# Cache the result of a query for 5 minutes (300 seconds)
# If the cache file exists and is younger than 5 minutes, it will be used.
# Otherwise, the query is executed on Dremio and the result is saved.
local_df = client.table("source.table") \
    .filter("col > 10") \
    .cache("my_cache", ttl_seconds=300)

# local_df is a LocalBuilder backed by DataFusion
# You can continue chaining methods
result = local_df.filter("col < 50") \
    .group_by("category") \
    .agg(avg_val="AVG(val)") \
    .collect()

print(result)
```

## Features

- **TTL (Time-To-Live)**: Automatically invalidates cache if it's too old.
- **DataFusion Engine**: Executes SQL locally on the cached Arrow file, providing fast performance without network overhead.
- **Seamless Integration**: `LocalBuilder` mimics the `DremioBuilder` API for `select`, `filter`, `group_by`, `agg`, `order_by`, `limit`, and `sql`.

## API

### `cache(name, ttl_seconds=None, folder=".cache")`

- `name`: Name of the cache file (saved as `{folder}/{name}.feather`).
- `ttl_seconds`: Expiration time in seconds. If `None`, cache never expires (unless manually deleted).
- `folder`: Directory to store cache files. Defaults to `.cache`.


---

<!-- Source: docs/data_engineering/creating_tables.md -->

---

## Output: "Query 2 has the lowest estimated cost (45.2)"

for query in result['queries']:
    print(f"Query {query['query_id']}: Cost = {query['total_cost']}")
```

## Use Cases

### 1. Pre-execution Validation

```python

---

## Query Profile Analyzer

Analyze and visualize Dremio query execution profiles.

## Usage

### Get Job Profile

```python
profile = client.admin.get_job_profile("job_id_123")
```

### Summary

Print a summary of the job execution.

```python
profile.summary()
# Job ID: job_id_123
# State: COMPLETED
# Start: 1600000000000
# End: 1600000005000
```

### Visualize

Visualize the execution timeline using Plotly.

```python
# Display interactive chart
profile.visualize().show()

# Save to HTML
profile.visualize(save_to="profile.html")
```


---

<!-- Source: docs/api_compatibility.md -->

---

## Review all queries in a pipeline
for sql in pipeline_queries:
    estimate = estimator.estimate_query_cost(sql)
    if len(estimate.optimization_hints) > 0:
        print(f"Query needs review: {sql[:50]}...")
        for hint in estimate.optimization_hints:
            print(f"  - {hint}")
```

## Limitations

- **Cost Metrics**: Costs are relative estimates, not absolute resource usage
- **Plan Parsing**: Based on Dremio's EXPLAIN output format (may vary by version)
- **Optimization Hints**: Static analysis; may not catch all issues
- **Reflection Impact**: Doesn't account for reflection acceleration

## Best Practices

1. **Use Early**: Check costs during development, not just production
2. **Iterate**: Use `compare_queries()` to test different approaches
3. **Combine with Profiling**: Use cost estimation for planning, profiling for actual performance
4. **Set Thresholds**: Define acceptable cost limits for your use case


---

<!-- Source: docs/performance/tuning.md -->

# Performance Tuning Guide

Optimizing `dremioframe` applications involves tuning both the client-side Python code and the server-side Dremio execution.

## 1. Arrow Flight Optimization

DremioFrame uses Apache Arrow Flight for high-performance data transfer.

### Batch Sizes

When fetching large datasets using `collect()`, the data is streamed in chunks.
*   **Default**: Dremio controls the chunk size.
*   **Optimization**: Ensure your network has high throughput. Flight is bandwidth-bound.

When **writing** data (`insert`, `create`), `dremioframe` splits data into batches to avoid hitting message size limits (usually 2GB, but practically smaller).

```python

---

## Subsequent operations use the local file (via DuckDB/DataFusion)
cached_df.filter("col1 = 1").show()
```


---

<!-- Source: docs/reference/advanced.md -->

# Advanced Features

## External Queries

Dremio allows you to push queries directly to the underlying source, bypassing Dremio's SQL parser. This is useful for using source-specific SQL dialects or features not yet supported by Dremio.

```python