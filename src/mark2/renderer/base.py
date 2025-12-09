"""Base class for mark2 renderers."""

import sys
from abc import ABC, abstractmethod
from contextlib import nullcontext

from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict


class Renderer(ABC):
    """Abstract base class defining the interface for all mark2 renderers."""

    @abstractmethod
    def render(
        self,
        tokens: list[Token],
        output_filename: str,
        options: OptionsDict,
        env: EnvType | None = None,
    ) -> None:
        """Render markdown-it tokens to the target format.

        Args:
            tokens: List of tokens from markdown-it parser
            output_filename: Output file path (use '-' for stdout)
            options: Rendering options from markdown-it
            env: Optional environment variables for rendering context
        """

    def _open_output(self, output_filename: str):
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
