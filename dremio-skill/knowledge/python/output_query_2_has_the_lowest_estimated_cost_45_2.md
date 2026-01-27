# Output: "Query 2 has the lowest estimated cost (45.2)"

for query in result['queries']:
    print(f"Query {query['query_id']}: Cost = {query['total_cost']}")
```

## Use Cases

### 1. Pre-execution Validation

```python
