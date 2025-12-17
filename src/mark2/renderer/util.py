"""Utility functions for mark2 renderers.

This module provides common utility functions used across different renderer
implementations, including file I/O helpers for managing output destinations.
"""

import sys
from contextlib import nullcontext
from typing import ContextManager, TextIO


def open_output(output_filename: str) -> ContextManager[TextIO]:
    """Get a context manager for writing output.

    Args:
        output_filename: Output file path (use '-' for stdout)

    Returns:
        A context manager that yields a file-like object for writing
    """
    if output_filename == "-":
        return nullcontext(sys.stdout)
    else:
        return open(output_filename, "w", encoding="utf-8")
