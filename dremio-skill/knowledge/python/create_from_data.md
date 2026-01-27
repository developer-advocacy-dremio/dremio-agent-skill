# Create from data
test_data = [
    {'product_id': 1, 'name': 'Widget', 'price': 9.99},
    {'product_id': 2, 'name': 'Gadget', 'price': 19.99}
]

df = manager.create_fixture('products', test_data)
```

### Loading from Files

```python
