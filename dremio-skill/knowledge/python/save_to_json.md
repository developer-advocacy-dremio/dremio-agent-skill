# Save to JSON
manager.save_json('products', 'tests/fixtures/products.json')
```

## Test Assertions

Helper functions for common test assertions.

### DataFrame Equality

```python
from dremioframe.testing import assert_dataframes_equal

expected = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
actual = client.sql("SELECT * FROM test").collect()

assert_dataframes_equal(expected, actual)
```

### Schema Validation

```python
from dremioframe.testing import assert_schema_matches

result = client.sql("SELECT * FROM users").collect()

expected_schema = {
    'id': 'int64',
    'name': 'object',
    'age': 'int64'
}

assert_schema_matches(result, expected_schema)
```

### Query Validation

```python
from dremioframe.testing import assert_query_valid

sql = "SELECT * FROM users WHERE age > 25"
assert_query_valid(sql)  # Checks basic SQL syntax
```

### Row Count Assertions

```python
from dremioframe.testing import assert_row_count

result = client.sql("SELECT * FROM users").collect()

assert_row_count(result, 10, 'eq')   # Exactly 10 rows
assert_row_count(result, 5, 'gt')    # More than 5 rows
assert_row_count(result, 100, 'lt')  # Less than 100 rows
```

## Complete Test Example

```python
import pytest
from dremioframe.testing import (
    MockDremioClient,
    FixtureManager,
    assert_dataframes_equal,
    assert_schema_matches
)

@pytest.fixture
def mock_client():
    """Fixture providing a configured mock client"""
    client = MockDremioClient()
    
    # Set up test data
    users = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35]
    })
    
    client.add_response("FROM users", users)
    return client

def test_user_query(mock_client):
    """Test querying users"""
    result = mock_client.sql("SELECT * FROM users WHERE age > 20").collect()
    
    # Assertions
    assert len(result) == 3
    assert_schema_matches(result, {
        'id': 'int64',
        'name': 'object',
        'age': 'int64'
    })
    
    # Verify query was executed
    assert "users" in mock_client.get_last_query()

def test_data_transformation(mock_client):
    """Test a data transformation pipeline"""
    # Your application code that uses the client
    raw_data = mock_client.sql("SELECT * FROM users").collect()
    
    # Transform
    transformed = raw_data[raw_data['age'] > 25]
    
    # Assert
    assert len(transformed) == 2
    assert all(transformed['age'] > 25)
```

## Integration with pytest

### Shared Fixtures

Create reusable fixtures in `conftest.py`:

```python
