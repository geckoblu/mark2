"""HTML renderer for converting Markdown to HTML format."""

import argparse

from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.base import Renderer


class HTMLRenderer(Renderer):
    """A minimal HTML renderer for markdown-it tokens."""

    def __init__(self, args: argparse.Namespace, options: OptionsDict, env: EnvType) -> None:
        """Initialize the HTML renderer.

        Uses markdown-it's built-in RendererHTML for token rendering.
        """
        super().__init__(args, options, env)

        self.renderer = RendererHTML()

    def render(
        self,
        tokens: list[Token],
        output_filename: str,
    ) -> None:
        """Render markdown-it tokens to HTML format with custom styling.

        Generates a complete HTML document with header and footer, including
        CSS styling for justified text.

        Args:
            tokens: List of tokens from markdown-it parser
            output_filename: Output file path (use '-' for stdout)
        """
        html = self.renderer.render(tokens, self.options, self.env)

        with self._open_output(output_filename) as writer:
            print(HTML_HEADER, file=writer)
            print(html, file=writer)
            print(HTML_FOOTER, file=writer)


HTML_HEADER = """<!DOCTYPE html>
<html>
<head>
<style>
  p {
    text-align: justify;
  }
</style>
</head>
<body>
"""

HTML_FOOTER = """
</body>
</html>
"""
