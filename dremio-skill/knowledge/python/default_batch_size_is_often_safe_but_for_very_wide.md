# Default batch size is often safe, but for very wide tables, reduce it.
client.table("target").insert("target", data=df, batch_size=5000)
```

### Compression

Flight supports compression (LZ4/ZSTD). DremioFrame negotiates this automatically. Ensure your client machine has CPU cycles to spare for decompression.

## 2. Client-Side vs. Server-Side Processing

Always push filtering and aggregation to Dremio (Server-Side) before collecting data to Python (Client-Side).

**Bad Pattern (Client-Side Filtering):**
```python
