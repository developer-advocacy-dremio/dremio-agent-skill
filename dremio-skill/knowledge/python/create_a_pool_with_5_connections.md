# Create a pool with 5 connections
pool = ConnectionPool(
    max_size=5,
    timeout=30,
    # DremioClient arguments
    pat="YOUR_PAT",
    project_id="YOUR_PROJECT_ID"
)
```

### Using the Context Manager

The recommended way to use the pool is via the context manager, which ensures connections are returned to the pool even if errors occur.

```python
with pool.client() as client:
    # Use client as normal
    df = client.sql("SELECT * FROM sys.version").collect()
    print(df)
```

### Manual Management

You can also manually get and release clients.

```python
try:
    client = pool.get_client()
    # Use client...
finally:
    pool.release_client(client)
```

### Configuration

- **max_size**: Maximum number of connections to create.
- **timeout**: Seconds to wait for a connection if the pool is empty and at max size. Raises `TimeoutError` if exceeded.
- **client_kwargs**: Arguments passed to `DremioClient` constructor (e.g., `pat`, `username`, `password`, `flight_endpoint`).


---

<!-- Source: docs/performance/cost_estimation.md -->

# Query Cost Estimation

DremioFrame provides a `CostEstimator` to analyze query execution plans, estimate costs, and suggest optimizations before running expensive queries.

## CostEstimator

The `CostEstimator` uses Dremio's `EXPLAIN PLAN` to analyze queries and provide actionable insights.

### Initialization

```python
from dremioframe.client import DremioClient
from dremioframe.cost_estimator import CostEstimator

client = DremioClient()
estimator = CostEstimator(client)
```

### Estimating Query Cost

Get a detailed cost estimate for any query:

```python
sql = """
SELECT customer_id, SUM(amount) as total
FROM sales.transactions
WHERE date >= '2024-01-01'
GROUP BY customer_id
"""

estimate = estimator.estimate_query_cost(sql)

print(f"Estimated rows: {estimate.estimated_rows}")
print(f"Total cost: {estimate.total_cost}")
print(f"Plan summary: {estimate.plan_summary}")
print(f"Optimization hints: {estimate.optimization_hints}")
```

**Output**:
```
Estimated rows: 50000
Total cost: 125.5
Plan summary: Query plan includes: 1 table scan(s), aggregation, 1 filter(s)
Optimization hints: ['Consider adding LIMIT for large tables']
```

### Cost Estimate Details

The `CostEstimate` object includes:
- **estimated_rows**: Number of rows expected to be processed
- **estimated_bytes**: Approximate data size
- **scan_cost**: Cost of table scans
- **join_cost**: Cost of join operations
- **total_cost**: Overall query cost metric
- **plan_summary**: Human-readable plan description
- **optimization_hints**: List of suggestions

### Optimization Hints

The estimator automatically detects common anti-patterns:

```python
hints = estimator.get_optimization_hints(sql)

for hint in hints:
    print(f"{hint.severity}: {hint.message}")
    print(f"  Suggestion: {hint.suggestion}")
```

**Common hints**:
- **SELECT \***: Suggests specifying only needed columns
- **Missing WHERE**: Warns about full table scans
- **Multiple JOINs**: Suggests using CTEs for readability
- **ORDER BY without LIMIT**: Recommends adding LIMIT
- **DISTINCT usage**: Suggests alternatives like GROUP BY

### Comparing Query Variations

Compare multiple approaches to find the most efficient:

```python
result = estimator.compare_queries(
    # Approach 1: Subquery
    """
    SELECT * FROM (
        SELECT customer_id, amount FROM sales.transactions
    ) WHERE amount > 1000
    """,
    
    # Approach 2: Direct filter
    """
    SELECT customer_id, amount 
    FROM sales.transactions 
    WHERE amount > 1000
    """
)

print(result['recommendation'])
