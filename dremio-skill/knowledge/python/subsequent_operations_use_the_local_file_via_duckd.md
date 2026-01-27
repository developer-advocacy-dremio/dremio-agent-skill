# Subsequent operations use the local file (via DuckDB/DataFusion)
cached_df.filter("col1 = 1").show()
```


---

<!-- Source: docs/reference/advanced.md -->

# Advanced Features

## External Queries

Dremio allows you to push queries directly to the underlying source, bypassing Dremio's SQL parser. This is useful for using source-specific SQL dialects or features not yet supported by Dremio.

```python
