"""HTML renderer for converting Markdown to HTML format."""

from typing import Sequence
from pathlib import Path

from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.rendererhtml import RendererHTML
from mark2.renderer.util import open_output


class HTMLRenderer(RendererHTML):
    """A minimal HTML renderer for markdown-it tokens.

    This renderer extends markdown-it's RendererHTML to add a complete HTML
    document structure with header and footer.
    """

    __output__: str = "html"

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates HTML with document structure.

        Args:
            tokens: List of block tokens to render
            options: Parser instance parameters
            env: Additional data from parsed input
        """
        html = super().render(tokens, options, env)
        html = html.replace("\xa0", "&#160;")

        output_filename = env.get("output_filename", "-")

        stylesheet = env.get("html_stylesheet", DEFAULT_STYLESHEET)
        frontmatter = env.get("front_matter", {})
        doctitle = frontmatter.get("title", Path(env.get("output_filename", "-")).stem)

        with open_output(output_filename) as writer:
            print(HTML_HEADER % {"title": doctitle, "stylesheet": stylesheet}, file=writer)
            print(html, file=writer)
            print(HTML_FOOTER, file=writer)


HTML_HEADER = """<!DOCTYPE html>
<html>
<head>
  <title>%(title)s</title>
<style>%(stylesheet)s</style>
</head>
<body>
"""

HTML_FOOTER = """
</body>
</html>
"""

DEFAULT_STYLESHEET = """h2 {
	page-break-before: always;
}

p {
    margin: 0;
    text-align: justify;
    text-indent: 1em;
}

sup {
    font-size: 0.75em;
    line-height: 0;
    vertical-align: super;
}

a {
    text-decoration: None;
}

div.footnotes {
    margin-top: 2em;
}

div.footnote p {
    font-size: 0.8em;
    margin: 1em 1em 1em 2em;
    text-indent: -1em;
}
"""
