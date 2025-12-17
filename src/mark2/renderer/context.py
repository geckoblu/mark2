"""Minimal ConTeXt renderer compatible with markdown-it."""

from typing import Any, Sequence

from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.base import Renderer
from mark2.renderer.util import open_output


class ConTeXtRenderer(Renderer):
    """A minimal ConTeXt renderer for markdown-it tokens."""

    __output__ = "text"

    def __init__(self, parser: Any = None):
        """Initialize the renderer."""
        super().__init__(parser)

        self.result = []

        self.in_link = False
        self.link_href = ""

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates output.

        :param tokens: list on block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input

        """

        self.result = []

        self.result.append(CONTEXT_HEADER)

        super().render(tokens, options, env)

        self.result.append(CONTEXT_FOOTER)

        tex = "".join(self.result)

        output_filename = env.get("output_filename", "-")
        with open_output(output_filename) as writer:
            print(tex, file=writer)

    def _escape_tex(self, text: str) -> str:
        """Escape special ConTeXt/TeX characters.

        Args:
            text: The text string to escape

        Returns:
            The text with special characters properly escaped for ConTeXt
        """
        replacements = {
            "\\": "\\textbackslash{}",
            "{": "\\{",
            "}": "\\}",
            "$": "\\$",
            "&": "\\&",
            "%": "\\%",
            "#": "\\#",
            "_": "\\letterunderscore{}",
            "~": "\\lettertilde{}",
            "^": "\\letterhat{}",
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text

    ###########################################################################
    # All the methods not starting with "render" nor "_" are rules renderers
    ###########################################################################

    def paragraph_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening paragraph token."""
        pass

    def paragraph_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing paragraph token."""
        self.result.append("\n\n")

    def text(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render text token."""
        token = tokens[idx]
        self.result.append(self._escape_tex(token.content))

    def em_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening emphasis token."""
        self.result.append("{\\em ")

    def em_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing emphasis token."""
        self.result.append("}")

    def heading_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening heading token."""
        token = tokens[idx]
        level = int(token.tag[1])  # h1 -> 1, h2 -> 2, etc.
        heading_map = {
            1: "\\section{",
            2: "\\subsection{",
            3: "\\subsubsection{",
            4: "\\subsubsubsection{",
            5: "\\subsubsubsubsection{",
            6: "\\subsubsubsubsubsection{",
        }
        self.result.append(heading_map.get(level, "\\section{"))

    def heading_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing heading token."""
        self.result.append("}\n\n")

    def bullet_list_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening bullet list token."""
        self.result.append("\\startitemize\n")

    def bullet_list_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing bullet list token."""
        self.result.append("\\stopitemize\n\n")

    def ordered_list_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening ordered list token."""
        self.result.append("\\startitemize[n]\n")

    def ordered_list_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing ordered list token."""
        self.result.append("\\stopitemize\n\n")

    def list_item_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening list item token."""
        self.result.append("\\item ")

    def list_item_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing list item token."""
        pass

    def link_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening link token."""
        token = tokens[idx]
        self.link_href = self._get_attr(token, "href") or ""
        self.in_link = True
        self.result.append("\\goto{")

    def link_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing link token."""
        self.result.append(f"}}[url({self.link_href})]")
        self.in_link = False

    def strong_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening strong/bold token."""
        self.result.append("{\\bf ")

    def strong_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing strong/bold token."""
        self.result.append("}")

    def code_inline(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render inline code token."""
        token = tokens[idx]
        self.result.append(f"\\type{{{token.content}}}")

    def code_block(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render code block token."""
        token = tokens[idx]
        self.result.append("\\starttyping\n")
        self.result.append(token.content)
        self.result.append("\\stoptyping\n\n")

    def fence(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render fenced code block token."""
        token = tokens[idx]
        # ConTeXt doesn't have built-in syntax highlighting in the same way,
        # but we can use typing environment
        self.result.append("\\starttyping\n")
        self.result.append(token.content)
        self.result.append("\\stoptyping\n\n")

    def blockquote_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening blockquote token."""
        self.result.append("\\startblockquote\n")

    def blockquote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing blockquote token."""
        self.result.append("\\stopblockquote\n\n")

    def hr(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render horizontal rule token."""
        self.result.append("\\thinrule\n\n")

    def image(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render image token."""
        token = tokens[idx]
        src = self._get_attr(token, "src") or ""
        alt = self._get_attr(token, "alt") or ""
        # ConTeXt image inclusion
        self.result.append(f"\\externalfigure[{src}]")
        if alt:
            self.result.append(f"[{alt}]")
        self.result.append("\n")

    def hardbreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render hard line break token."""
        self.result.append("\\crlf\n")

    def softbreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render soft line break token."""
        self.result.append("\n")

    def html_block(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render HTML block token."""
        # ConTeXt can't render HTML directly, so we skip it or add a comment
        token = tokens[idx]
        self.result.append(f"% HTML block skipped: {token.content[:50]}...\n")

    def html_inline(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render inline HTML token."""
        # ConTeXt can't render HTML directly, so we skip it
        pass

    def s_open(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render opening strikethrough token."""
        self.result.append("\\overstrike{")

    def s_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing strikethrough token."""
        self.result.append("}")

    def table_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table token."""
        self.result.append("\\startTABLE\n")

    def table_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table token."""
        self.result.append("\\stopTABLE\n\n")

    def thead_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table header token."""
        pass

    def thead_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table header token."""
        pass

    def tbody_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table body token."""
        pass

    def tbody_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table body token."""
        pass

    def tr_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table row token."""
        self.result.append("\\bTR\n")

    def tr_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table row token."""
        self.result.append("\\eTR\n")

    def th_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table header cell token."""
        self.result.append("\\bTH ")

    def th_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table header cell token."""
        self.result.append(" \\eTH\n")

    def td_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table data cell token."""
        self.result.append("\\bTD ")

    def td_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table data cell token."""
        self.result.append(" \\eTD\n")


CONTEXT_HEADER = """\\starttext
"""

CONTEXT_FOOTER = """\\stoptext
"""
