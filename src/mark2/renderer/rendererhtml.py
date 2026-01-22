"""HTML renderer for mark2 with plugin support.

This module extends markdown-it-py's RendererHTML with custom render methods
for various mark2 plugins including superscript, MyST roles, and front matter.
"""

from typing import Sequence

import markdown_it
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.plugins.yaml_parser import parse_simple_yaml


class RendererHTML(markdown_it.renderer.RendererHTML):
    """Custom HTML renderer with support for mark2 plugins.

    Extends markdown-it-py's RendererHTML to add rendering support for:
    - Superscript tags (sup_plugin)
    - MyST roles including line breaks (myst_role_plugin)
    - Front matter parsing (front_matter_plugin)

    """

    __output__: str = "html"

    ###########################################################################
    # sup_plugin renderers
    ###########################################################################

    def sup_open(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        """Render opening <sup> tag for superscript text."""
        return "<sup>"

    def sup_close(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        """Render closing </sup> tag for superscript text."""
        return "</sup>"

    ###########################################################################
    # pagebreak_plugin renderers
    ###########################################################################
    def pagebreak(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        """Render page break as an HTML horizontal rule with class 'pagebreak'."""
        return '<hr class="pagebreak" />\n'

    ###########################################################################
    # myst_role_plugin renderers (with special handling).
    ###########################################################################

    def myst_role(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render MyST role (inline span with special handling)."""
        token = tokens[idx]

        name = token.meta.get("name", "unknown")
        if name == "line-break":
            return "<br/>"
        else:
            return f'<span class="role">{token.content}</span>'

    ###########################################################################
    # front_matter_plugin renderers
    ###########################################################################

    def front_matter(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Parse front matter block and store in environment."""
        token = tokens[idx]

        env["front_matter"] = parse_simple_yaml(token.content)

        return ""  # Front matter is not rendered in output

    ###########################################################################
    # footnote_plugin renderers
    ###########################################################################

    # Token renderers
    def footnote_ref(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render footnote reference in the text."""
        caption: str = self.rules["footnote_caption"](tokens, idx, options, env)

        ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)

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
        caption: str = self.rules["footnote_caption"](tokens, idx, options, env)

        ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)

        if tokens[idx].meta["subId"] > 0:
            ident += ":" + str(tokens[idx].meta["subId"])

        anchor = f'<a href="#fnref{ident}" id="fn{ident}" class="footnote-backref"><sup class="footnote-backref">{caption}</sup></a>&#160;'  # pylint: disable=line-too-long

        # print(anchor)
        return anchor

    def footnote_block_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render opening of footnote block section."""
        return '<div class="footnotes">\n'

    def footnote_block_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render closing of footnote block section."""
        return "</div>\n"

    def footnote_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render opening of individual footnote item."""
        return '<div class="footnote">\n'

    def footnote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render closing of individual footnote item."""
        return "</div>\n"
