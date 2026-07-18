# ISRO Mission Checker - Test Suite

This directory contains comprehensive test cases for the ISRO Mission Checker project.

## Test Structure

### Test Files

1. **test_no_duplicate_logger.py**
   - Tests for the custom NoDuplicateLogger class
   - Covers: duplicate message filtering, single message logging, edge cases

2. **test_email_utils.py**
   - Tests for email sending functionality
   - Covers: SMTP connection, email formatting, attachment handling, error cases

3. **test_mission_checker.py**
   - Unit tests for the main mission-checker script
   - Covers: mission data fetching, caching, email notifications, Selenium interactions

4. **test_integration.py**
   - Integration tests for complete workflows
   - Covers: end-to-end mission checking, error handling, multi-element parsing

## Setup

### Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### Install Project Dependencies

```bash
pip install -r requirements.txt
```

Or for Docker:

```bash
docker build -t isro-mission-checker:test .
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=com --cov-report=html --cov-report=term-missing
```

### Run Specific Test File

```bash
pytest tests/test_no_duplicate_logger.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_no_duplicate_logger.py::TestNoDuplicateLogger -v
```

### Run Specific Test Function

```bash
pytest tests/test_no_duplicate_logger.py::TestNoDuplicateLogger::test_single_message_is_logged -v
```

### Run Tests by Marker

```bash
pytest -m "unit" -v
pytest -m "integration" -v
pytest -m "email" -v
```

### Run Tests with Detailed Output

```bash
pytest -vv --tb=long
```

### Run Tests in Parallel (requires pytest-xdist)

```bash
pytest -n auto
```

## Test Coverage

### Current Coverage

- **NoDuplicateLogger**: 100% - All methods and branches tested
- **EmailUtils**: 100% - Happy path and error cases
- **MissionChecker**: Core functionality with mocked external dependencies

### Generate Coverage Report

After running tests:

```bash
# Terminal report
pytest --cov=com --cov-report=term-missing

# HTML report (open htmlcov/index.html in browser)
pytest --cov=com --cov-report=html
```

## Test Categories

### Unit Tests
Tests for individual functions and classes in isolation:
- `test_no_duplicate_logger.py`
- `test_email_utils.py`
- `test_mission_checker.py`

### Integration Tests
Tests for workflows combining multiple components:
- `test_integration.py`

### Test Markers

Tag your tests with markers for better organization:

```bash
@pytest.mark.unit
def test_something():
    pass

@pytest.mark.integration
def test_workflow():
    pass

@pytest.mark.email
def test_email_sending():
    pass

@pytest.mark.slow
def test_long_running():
    pass
```

## Mocking Strategy

All tests use mocking to avoid external dependencies:

- **Selenium WebDriver**: Mocked using unittest.mock
- **Redis**: Mocked to simulate cache operations
- **SMTP**: Mocked to avoid actual email sending
- **File Operations**: Mocked for image file handling

## Key Test Scenarios

### NoDuplicateLogger
- ✅ Single message logging
- ✅ Duplicate message filtering
- ✅ Different message logging
- ✅ Edge cases (empty strings, whitespace)

### EmailUtils
- ✅ Successful email sending
- ✅ Subject and content verification
- ✅ Image attachment handling
- ✅ SMTP configuration
- ✅ Error handling (SMTP errors, file not found)

### MissionChecker
- ✅ Mission data fetching from website
- ✅ Email notification on mission change
- ✅ Cache management with Redis
- ✅ Screenshot capture
- ✅ Error handling and driver cleanup
- ✅ Multiple element parsing

### Integration
- ✅ Complete workflow with new mission
- ✅ Workflow with cached mission
- ✅ Error recovery
- ✅ Email parameter verification

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements-test.txt
    pytest --cov=com --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Troubleshooting

### Issue: Import errors when running tests

**Solution**: Ensure you're running from the project root and have installed dependencies:

```bash
cd /path/to/isro-missions
pip install -r requirements-test.txt
```

### Issue: Tests fail with "module not found"

**Solution**: Check that the Python path includes the project root in conftest.py

### Issue: Mock patches not working

**Solution**: Ensure you're patching at the location where the object is used, not where it's defined

## Adding New Tests

When adding new functionality:

1. Create test file or add to existing file: `tests/test_*.py`
2. Use descriptive test names: `test_<what>_<condition>_<expected_result>`
3. Follow the Arrange-Act-Assert pattern
4. Use appropriate fixtures and mocks
5. Add docstrings explaining what is tested
6. Run tests to verify coverage: `pytest --cov=com`

### Test Template

```python
def test_feature_does_something_when_condition(mock_dependency):
    # Arrange
    expected_value = "something"
    mock_dependency.return_value = expected_value
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
    mock_dependency.assert_called_once()
```

## Documentation

For more information about pytest:
- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)

## License

MIT License - See main README.md

