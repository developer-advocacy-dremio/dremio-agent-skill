# This will match:
client.sql("SELECT id FROM users WHERE age > 25").collect()
```

### Query History

Track which queries were executed:

```python
client.sql("SELECT * FROM table1")
client.sql("SELECT * FROM table2")

