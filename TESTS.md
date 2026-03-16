#Tests

This project uses pytest and pytest-flask to test Flask routes.

## Installing development dependencies

```bash
pip install -e .[dev]

```

## Running the tests

```bash
pytest
```

## Test structure

- `tests/conftest.py`: Fixture configuration for the Flask app.

- `tests/test_routes.py`: Tests for the main routes.

The tests use an in-memory database for isolation.