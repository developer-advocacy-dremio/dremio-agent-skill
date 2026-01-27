# Create large dataset
data = pd.DataFrame({
    "id": range(100000),
    "name": [f"user_{i}" for i in range(100000)],
    "value": range(100000)
})

