# Review all queries in a pipeline
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
