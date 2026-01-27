# Insert in batches of 1000 rows
client.table("target").insert("target", data=large_df, batch_size=1000)
```

## Batching

For `insert` and `merge` operations with in-memory data (Arrow Table or Pandas DataFrame), you can specify a `batch_size` to split the data into multiple chunks. This is useful for large datasets to avoid hitting query size limits.

```python
