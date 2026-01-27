# Check cost before running expensive query
estimate = estimator.estimate_query_cost(expensive_sql)

if estimate.total_cost > 1000:
    print("Warning: This query may be expensive!")
    print("Hints:", estimate.optimization_hints)
    # Decide whether to proceed
```

### 2. Query Optimization Workflow

```python
