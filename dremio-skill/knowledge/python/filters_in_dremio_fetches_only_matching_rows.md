# Filters in Dremio, fetches only matching rows
df = client.table("sales").filter("amount > 100").collect()
```

## 3. Parallelism

### Pipeline Parallelism
Use the `orchestration` module to run independent tasks in parallel.

```python
pipeline = Pipeline("etl", max_workers=4)
```

### Async Client
For high-concurrency applications (e.g., a web app backend), use `AsyncDremioClient` to avoid blocking the main thread while waiting for Dremio.

```python
async with AsyncDremioClient() as client:
    result = await client.query("SELECT * FROM large_table")
```

## 4. Caching

If you query the same dataset multiple times in a script, cache it locally.

```python
