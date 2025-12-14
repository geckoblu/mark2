"""Base class for mark2 renderers."""

import argparse
import sys
from abc import ABC, abstractmethod
from contextlib import nullcontext
from typing import ContextManager, TextIO

from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict


class Renderer(ABC):
    """Abstract base class defining the interface for all mark2 renderers."""

    def __init__(self, args: argparse.Namespace, options: OptionsDict, env: EnvType) -> None:
        """Initialize the renderer."""
        if options is None:
            self.options = {}
        else:
            self.options = options
        if env is None:
            self.env = {}
        else:
            self.env = env

        self.quiet = args.quiet

    @abstractmethod
    def render(
        self,
        tokens: list[Token],
        output_filename: str,
    ) -> None:
        """Render markdown-it tokens to the target format.

        Args:
            tokens: List of tokens from markdown-it parser
            output_filename: Output file path (use '-' for stdout)
        """

    def _open_output(self, output_filename: str) -> ContextManager[TextIO]:
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
