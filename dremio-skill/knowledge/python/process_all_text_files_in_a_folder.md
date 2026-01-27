# Process all text files in a folder
client.list_files("@source/folder") \
    .filter("file_name LIKE '%.txt'") \
    .select(
        F.col("file_name"),
        F.ai_classify("Sentiment?", F.col("file_content"), ["Positive", "Negative"])
    )
```


---

<!-- Source: docs/reference/functions/complex.md -->

# Complex Type Functions

Functions for working with complex types like Arrays, Maps, and Structs.

## Usage

```python
from dremioframe import F

