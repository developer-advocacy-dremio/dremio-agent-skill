# You can then chain DremioFrame operations on top
df.filter("age > 21").select("name").show()
```

This generates SQL like:
```sql
SELECT name FROM (
    SELECT * FROM TABLE(Postgres.EXTERNAL_QUERY('SELECT * FROM users WHERE active = true'))
) AS sub
WHERE age > 21
```


---

<!-- Source: docs/reference/async_client.md -->

# Async Client

`dremioframe` provides an asynchronous client for high-concurrency applications.

## Usage

The `AsyncDremioClient` is designed to be used as an async context manager.

```python
import asyncio
from dremioframe.async_client import AsyncDremioClient

async def main():
    async with AsyncDremioClient(pat="my-pat") as client:
        # Get catalog item
        item = await client.get_catalog_item("dataset-id")
        print(item)
        
        # Execute SQL (REST API)
        job = await client.execute_sql("SELECT 1")
        print(job)

if __name__ == "__main__":
    asyncio.run(main())
```

## Methods

- `get_catalog_item(id)`: Get catalog item by ID.
- `get_catalog_by_path(path)`: Get catalog item by path list.
- `execute_sql(sql)`: Submit a SQL job via REST API.
- `get_job_status(job_id)`: Check job status.


---

<!-- Source: docs/reference/builder.md -->

# Builder API Reference

::: dremioframe.builder.DremioBuilder
    options:
      show_root_heading: true
      show_source: true


---

<!-- Source: docs/reference/cli.md -->

# DremioFrame CLI

DremioFrame includes a command-line interface (CLI) for quick interaction with Dremio.

## Installation

The CLI is installed automatically with `dremioframe`.

```bash
pip install dremioframe
```

## Interactive Shell (REPL)

DremioFrame provides an interactive shell with syntax highlighting and auto-completion.

```bash
dremio-cli repl
```

Commands:
- `SELECT ...`: Execute SQL query and display results.
- `tables`: List tables in the root catalog.
- `exit` or `quit`: Exit the shell.

Requires `rich` and `prompt_toolkit` (install with `pip install dremioframe[cli]`).

## Configuration

Set the following environment variables:

- `DREMIO_PAT`: Personal Access Token
- `DREMIO_URL`: Dremio URL (e.g., `data.dremio.cloud`)
- `DREMIO_PROJECT_ID`: Project ID (optional, for Cloud)

## Usage

### Run a Query

```bash
dremio-cli query "SELECT * FROM my_table LIMIT 5"
```

### List Catalog

```bash
