"""HTML renderer for converting Markdown to HTML format."""

from typing import Sequence

from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.util import open_output


class HTMLRenderer(RendererHTML):
    """A minimal HTML renderer for markdown-it tokens."""

    # def __init__(self, parser: Any = None):
    #     """Initialize the renderer."""
    #     super().__init__(parser)

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates HTML.

        :param tokens: list on block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input

        """
        html = super().render(tokens, options, env)

        output_filename = env.get("output_filename", "-")
        with open_output(output_filename) as writer:
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
