"""HTML renderer for converting Markdown to HTML format."""

from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.base import Renderer


class HTMLRenderer(Renderer):
    """A minimal HTML renderer for markdown-it tokens."""

    def __init__(self) -> None:
        """Initialize the HTML renderer.

        Uses markdown-it's built-in RendererHTML for token rendering.
        """
        self.renderer = RendererHTML()

    def render(
        self,
        tokens: list[Token],
        output_filename: str,
        options: OptionsDict,
        env: EnvType | None = None,
    ) -> None:
        """Render markdown-it tokens to HTML format with custom styling.

        Generates a complete HTML document with header and footer, including
        CSS styling for justified text.

        Args:
            tokens: List of tokens from markdown-it parser
            output_filename: Output file path (use '-' for stdout)
            options: Optional rendering options from markdown-it
            env: Optional environment variables for rendering context
        """
        html = self.renderer.render(tokens, options, env)

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
