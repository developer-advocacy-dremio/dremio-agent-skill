# Fetches ALL data, then filters in Python
df = client.table("sales").collect()
filtered_df = df.filter(pl.col("amount") > 100)
```

**Good Pattern (Server-Side Filtering):**
```python
