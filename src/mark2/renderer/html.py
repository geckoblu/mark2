"""HTML renderer for converting Markdown to HTML format."""

import sys
from typing import Sequence
from pathlib import Path

from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.plugins.yaml_parser import parse_simple_yaml
from mark2.renderer.util import open_output


class HTMLRenderer(RendererHTML):
    """A minimal HTML renderer for markdown-it tokens.

    This renderer extends markdown-it's RendererHTML to add a complete HTML
    document structure with header and footer.
    """

    __output__: str = "html"

    # def __init__(self, parser: Any = None):
    #     """Initialize the renderer."""
    #     super().__init__(parser)

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

    ###########################################################################
    # Footnote plugin renderers
    ###########################################################################
    # pylint: disable=duplicate-code

    # Token renderers
    def footnote_ref(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render footnote reference in the text."""
        ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)

        caption: str = self.rules["footnote_caption"](tokens, idx, options, env)
        refid = ident

        if tokens[idx].meta.get("subId", -1) > 0:
            refid += ":" + str(tokens[idx].meta["subId"])

        ref = (
            f'<a href="#fn{ident}" id="fnref{refid}"><sup class="footnote-ref">{caption}</sup></a>'
        )

        # print(ref)
        return ref

    def footnote_anchor(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render back-reference link at end of footnote."""
        ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)
        caption: str = self.rules["footnote_caption"](tokens, idx, options, env)

        if tokens[idx].meta["subId"] > 0:
            ident += ":" + str(tokens[idx].meta["subId"])

        anchor = f'<a href="#fnref{ident}" id="fn{ident}" class="footnote-backref"><sup class="footnote-backref">{caption}</sup></a>&#160;'  # pylint: disable=line-too-long

        # print(anchor)
        return anchor

    def footnote_block_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render opening of footnote block section."""
        return '<div class="notes">\n'

    def footnote_block_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render closing of footnote block section."""
        return "</div>\n"

    def footnote_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render opening of individual footnote item."""
        return '<div class="note">\n'

    def footnote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render closing of individual footnote item."""
        return "</div>\n"

    # pylint: enable=duplicate-code

    ###########################################################################
    # Frontmatter plugin renderers
    ###########################################################################

    def front_matter(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Parse front matter block (not included in output)."""
        token = tokens[idx]
        # print(f"FRONT MATTER RENDERER CALLED: {token}", file=sys.stderr)

        env["front_matter"] = parse_simple_yaml(token.content)
        # print(env["front_matter"], file=sys.stderr)

        return ""  # Front matter is not rendered in output

    ###########################################################################
    # Pagebreak plugin renderer
    ###########################################################################

    # def pagebreak(
    #     self,
    #     tokens: Sequence[Token],
    #     idx: int,
    #     options: OptionsDict,
    #     env: EnvType,
    # ) -> str:
    #     """Render a pagebreak token.

    #     Args:
    #         self: The renderer instance
    #         tokens: List of all tokens being rendered
    #         idx: Index of the current pagebreak token to render
    #         options: Markdown-it parser options
    #         env: Environment variables for rendering context

    #     Returns:
    #         Empty string (debug-only implementation that prints to stderr)
    #     """
    #     return "<hr/>"  # Simple horizontal rule for HTML output

    ###########################################################################
    # MyST role plugin renderer
    ###########################################################################

    def myst_role(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render MyST role (inline span)."""
        token = tokens[idx]
        name = token.meta.get("name", "unknown")
        if name == "line-break":
            return "<br/>"
        else:
            print(
                "  [HTMLRenderer] no rendering for "
                + f"{token.type}: name={name}, attrs={token.attrs}, content='{token.content}'",
                file=sys.stderr,
            )
            return ""  # No output for other roles in HTML


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

div.notes {
    margin-top: 2em;
}

div.note p {
    font-size: 0.8em;
    margin: 1em 1em 1em 2em;
    text-indent: -1em;
}
"""
