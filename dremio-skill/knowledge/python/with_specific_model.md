# With specific model
F.ai_generate(
    "Extract info", 
    model_name="gpt-4", 
    schema="ROW(summary VARCHAR)"
)
```

## Using with LIST_FILES

You can combine AI functions with `client.list_files()` to process unstructured data.

```python
