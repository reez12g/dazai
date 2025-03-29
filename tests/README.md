# Dazai API Tests

This directory contains tests for the Dazai API application.

## Test Structure

The tests are organized as follows:

- `conftest.py`: Shared pytest fixtures used across test modules
- `unit/`: Unit tests for individual components
  - `test_services/`: Tests for service layer components
  - `test_routers/`: Tests for API endpoints
  - `test_models/`: Tests for data models
- `integration/`: Integration tests for API endpoints

## Running Tests

### Prerequisites

Make sure you have installed the development dependencies:

```bash
pip install -r requirements/requirements.txt
```

### Running All Tests

To run all tests:

```bash
pytest
```

### Running Specific Test Categories

To run only unit tests:

```bash
pytest tests/unit/
```

To run only integration tests:

```bash
pytest tests/integration/
```

To run tests for a specific component:

```bash
pytest tests/unit/test_services/test_style_transfer_service.py
```

### Test Coverage

To run tests with coverage report:

```bash
pytest --cov=app tests/
```

For a more detailed HTML coverage report:

```bash
pytest --cov=app --cov-report=html tests/
```

This will generate a coverage report in the `htmlcov` directory.

## Test Mocking Strategy

The tests use mocking to avoid dependencies on external services and NLP models:

1. **Service Tests**: Mock the underlying NLP models (T5, BERT) to test service logic without loading actual models
2. **Router Tests**: Mock the service layer to test API endpoint behavior
3. **Integration Tests**: Selectively mock components to test the integration between layers

## Adding New Tests

When adding new features to the application, follow these guidelines for testing:

1. Add unit tests for new services in `tests/unit/test_services/`
2. Add unit tests for new routers in `tests/unit/test_routers/`
3. Add unit tests for new models in `tests/unit/test_models/`
4. Add integration tests for new API endpoints in `tests/integration/`
5. Update shared fixtures in `conftest.py` if needed
