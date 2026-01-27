# Use in your code
result = client.sql("SELECT * FROM users").collect()
print(result)  # Returns the mocked DataFrame
```

### Query Matching

The mock client supports both exact and partial query matching:

```python
