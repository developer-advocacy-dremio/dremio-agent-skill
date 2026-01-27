# Insert in batches of 1000 rows
client.table("target").insert("target", data=large_df, batch_size=1000)
```

## Schema Validation

You can validate data against a Pydantic schema before insertion.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

