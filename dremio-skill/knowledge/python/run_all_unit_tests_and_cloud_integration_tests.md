# Run all unit tests and cloud integration tests
pytest -m "not software and not external_backend"
```
*Note: If credentials are missing, cloud integration tests will skip.*

## 2. Dremio Software
Tests specifically for Dremio Software connectivity.

**Requirements:**
- `DREMIO_SOFTWARE_HOST`: Hostname (e.g., localhost).
- `DREMIO_SOFTWARE_PORT`: Flight port (default 32010).
- `DREMIO_SOFTWARE_USER`: Username.
- `DREMIO_SOFTWARE_PASSWORD`: Password.
- `DREMIO_SOFTWARE_TLS`: "true" or "false" (default false).

**Command:**
```bash
pytest -m software
```

## 3. External Backends
Tests for persistent orchestration backends (Postgres, MySQL).

**Requirements:**
- **Postgres**: `DREMIOFRAME_PG_DSN` (e.g., `postgresql://user:pass@localhost/db`)
- **MySQL**:
    - `DREMIOFRAME_MYSQL_USER`
    - `DREMIOFRAME_MYSQL_PASSWORD`
    - `DREMIOFRAME_MYSQL_HOST`
    - `DREMIOFRAME_MYSQL_DB`
    - `DREMIOFRAME_MYSQL_PORT`

**Command:**
```bash
pytest -m external_backend
```

## Running All Tests
To run everything (skipping what isn't configured):
```bash
pytest
```


---

<!-- Source: docs/testing/mocking.md -->

# Mock/Testing Framework

DremioFrame provides a comprehensive testing framework to write tests without requiring a live Dremio connection.

## MockDremioClient

The `MockDremioClient` mimics the `DremioClient` interface, allowing you to configure query responses for testing.

### Basic Usage

```python
from dremioframe.testing import MockDremioClient
import pandas as pd

