# Iteratively improve query
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
