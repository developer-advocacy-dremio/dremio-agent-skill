# tests/conftest.py
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
