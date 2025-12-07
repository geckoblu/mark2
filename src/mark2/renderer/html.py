"""HTML renderer for converting Markdown to HTML format."""

import sys
from contextlib import nullcontext
from markdown_it import MarkdownIt


class HTMLRenderer:
    """A minimal HTML renderer for markdown-it tokens."""

    def __init__(self) -> None:
        """Initialize the renderer."""

    def render(self, data: str, output_filename: str) -> None:
        """Render Markdown data to HTML format.

        Args:
            data: Markdown content as string
            output_filename: Output file path (use '-' for stdout)
        """
        md = MarkdownIt()
        html = md.render(data)

        if output_filename == "-":
            context = nullcontext(sys.stdout)
        else:
            context = open(output_filename, "w", encoding="utf-8")

        with context as writer:
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
