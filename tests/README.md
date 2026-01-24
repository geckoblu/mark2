# Test Requirements

To run the pytest tests, you need to install pytest first:

```bash
pip3 install pytest
```

to run tests with coverage, you need to install pytest-cov

```bash
pip3 install pytest-cov
```

## Running Tests

```bash
# Run all tests (excluding spec tests)
pytest tests/ -v

# Run all tests including spec tests
pytest tests/ -v --spec

# Run only spec tests
pytest -m spec -v

# Run tests for a specific module
pytest tests/mark2/test_main.py -v

# Run a specific test class
pytest tests/mark2/test_main.py::TestMainFunction -v

# Run a specific test method
pytest tests/mark2/test_main.py::TestMainFunction::test_specific -v

# Run a specific parameter test
pytest tests/mark2/test_main.py -k "pdf"  | grep -A 5 ^E

# Run tests with coverage (requires pytest-cov)
pytest tests/mark2 --cov=src/mark2 --cov-report=html
```

## Test Structure

The tests follow the same package structure as the source code:

```
tests/
├── mark2/
│   ├── __init__.py
│   ├── test_main.py           # Tests for src/mark2/main.py
│   ├── plugins/               # Tests for plugins
│   └── renderer/              # Tests for renderers
├── spec/                      # Spec tests
└── README.md
```