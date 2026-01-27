# Will raise ValidationError if data doesn't match
client.table("users").insert("users", data=df, schema=User)
```

## Data Quality Checks

You can run data quality checks on a builder instance. These checks execute queries to verify assumptions about the data.

```python
