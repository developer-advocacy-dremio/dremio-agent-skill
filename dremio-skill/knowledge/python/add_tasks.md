# ... add tasks ...
pipeline.run()
```

Access the UI at `http://localhost:8080`.


---

<!-- Source: docs/performance/bulk_loading.md -->

# Bulk Loading Optimization

For large datasets (10,000+ rows), using the default `VALUES` clause method can be slow and may hit SQL statement size limits. DremioFrame provides a **staging method** that dramatically improves performance by using Parquet files as an intermediate format.

## Usage

Both `create()` and `insert()` methods support a `method` parameter:

```python
from dremioframe.client import DremioClient
import pandas as pd

client = DremioClient()

