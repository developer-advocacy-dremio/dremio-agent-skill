# Testing

## Configure a response
users_df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie']
})

client.add_response("SELECT * FROM users", users_df)

---

## Create mock client
client = MockDremioClient()

---

## Exact match
client.add_response("SELECT * FROM users", users_df)

---

## Partial match (matches any query containing "FROM users")
client.add_response("FROM users", users_df)

---

## Retrieve loaded fixture
customers = manager.get('customers')
```

### Saving Fixtures

```python

---

## Run all unit tests and cloud integration tests
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

---

## tests/conftest.py
import pytest
from dremioframe.testing import MockDremioClient, FixtureManager

@pytest.fixture
def mock_client():
    return MockDremioClient()

@pytest.fixture
def fixture_manager():
    return FixtureManager(fixtures_dir='tests/fixtures')
```

### Parametrized Tests

```python
@pytest.mark.parametrize("age,expected_count", [
    (20, 3),
    (30, 2),
    (40, 0)
])
def test_age_filter(mock_client, age, expected_count):
    result = mock_client.sql(f"SELECT * FROM users WHERE age > {age}").collect()
    assert len(result) == expected_count
```

## Best Practices

1. **Use Fixtures**: Create pytest fixtures for common mock setups
2. **Realistic Data**: Use fixtures that mirror production data structure
3. **Test Isolation**: Clear query history between tests
4. **Partial Matching**: Use partial query matching for flexibility
5. **Schema Validation**: Always validate schema in addition to data

## Limitations

- **No Actual Execution**: Queries aren't validated against Dremio
- **Simple Matching**: Query matching is string-based, not semantic
- **No Side Effects**: Mock doesn't simulate Dremio-specific behaviors
- **In-Memory Only**: All data must fit in memory

---

## This will match:
client.sql("SELECT id FROM users WHERE age > 25").collect()
```

### Query History

Track which queries were executed:

```python
client.sql("SELECT * FROM table1")
client.sql("SELECT * FROM table2")

---

## Use in your code
result = client.sql("SELECT * FROM users").collect()
print(result)  # Returns the mocked DataFrame
```

### Query Matching

The mock client supports both exact and partial query matching:

```python