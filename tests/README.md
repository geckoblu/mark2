# Test Requirements

To run the pytest tests, you need to install pytest first:

```bash
pip install pytest
```

## Test Structure

The tests follow the same package structure as the source code:

```
tests/
├── odttools/
│   ├── __init__.py
│   └── parser/
│       ├── __init__.py
│       └── test_element.py    # Tests for src/odttools/parser/element.py
└── README.md
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run tests for a specific module
pytest tests/odttools/parser/test_element.py -v

# Run a specific test class
pytest tests/odttools/parser/test_element.py::TestExtractTextContent -v

# Run a specific test method
pytest tests/odttools/parser/test_element.py::TestExtractTextContent::test_odt_paragraph_with_span -v

# Run tests with coverage (if pytest-cov is installed)
pytest tests/ --cov=src/odttools --cov-report=html

# Run a specific parameter test
pytest tests/mark2/test_main.py -k "pdf"  | grep -A 5 ^E
```