"""Pytest configuration for spec tests."""

import pytest


def pytest_addoption(parser):
    """Add custom command-line options."""
    parser.addoption(
        "--spec",
        action="store_true",
        default=False,
        help="Run spec tests",
    )


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "spec: mark test as a spec test")


def pytest_collection_modifyitems(config, items):
    """Skip spec tests unless --spec is provided or -m spec is used."""
    if config.getoption("--spec"):
        return

    # Check if user explicitly selected spec tests with -m spec
    markexpr = config.getoption("-m", default="")
    if "spec" in markexpr:
        return

    skip_spec = pytest.mark.skip(reason="need --spec option to run")
    for item in items:
        if "spec" in item.keywords:
            item.add_marker(skip_spec)
