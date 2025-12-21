"""HTML renderer for converting Markdown to HTML format."""

from typing import Sequence
from pathlib import Path

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
        basename = Path(output_filename).stem
        with open_output(output_filename) as writer:
            print(HTML_HEADER % {"title": basename}, file=writer)
            print(html, file=writer)
            print(HTML_FOOTER, file=writer)


HTML_HEADER = """<!DOCTYPE html>
<html>
<head>
  <title>%(title)s</title>
<style>
  p {
    margin: 0;
    text-indent: 1em;
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
