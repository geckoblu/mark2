"""ConTeXt renderer for converting Markdown to ConTeXt format."""

from typing import Any, Sequence

from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.util import open_output
from mark2.renderer.baserenderer import BaseRenderer
from mark2.renderer.context.header_a5 import CONTEXT_HEADER_A5
from mark2.renderer.context.header_a4 import CONTEXT_HEADER_A4


class ConTeXtRenderer(BaseRenderer):
    """A minimal ConTeXt renderer for markdown-it tokens."""

    result: list[str]

    def __init__(self, parser: Any = None) -> None:
        """Initialize the renderer.

        Args:
            parser: Optional parser instance
        """
        super().__init__(parser)

        self.result = []
        self.in_list_item = False

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates ConTeXt output.

        :param tokens: list of block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input

        """

        self.result = []
        filtered = self._populate_reference_footnotes(tokens, env)

        self.result.append(CONTEXT_HEADER_A5)

        super().render(filtered, options, env)

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
        if not self.in_list_item:
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

    def sup_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening superscript token."""
        self.result.append("\\high{")

    def sup_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing superscript token."""
        self.result.append("}")

    def sub_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening subscript token."""
        self.result.append("\\low{")

    def sub_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing subscript token."""
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
        self.in_list_item = True
        self.result.append("\\item ")

    def list_item_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing list item token."""
        self.in_list_item = False
        self.result.append("\n")

    def link_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening link token."""
        token = tokens[idx]
        self.link_href = token.attrGet("href") or ""
        self.in_link = True
        self.result.append("\\goto{")

    def link_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing link token."""
        self.result.append(f"}}[url({self.link_href})]")
        self.in_link = False

    def blockquote_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening blockquote token."""
        self.result.append("\\startBlockquote\n")

    def blockquote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing blockquote token."""
        self.result.append("\\stopBlockquote\n\n")

    def pagebreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render page break token."""
        self.result.append("\\page\n\n")

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

    ###########################################################################
    # Footnote methods
    ###########################################################################

    def _render_inline_tokens(self, children: list[Token]) -> str:
        """Render inline token children to a ConTeXt markup string."""
        parts: list[str] = []
        for child in children:
            if child.type == "text":
                parts.append(self._escape_tex(child.content))
            elif child.type == "code_inline":
                parts.append(f"\\type{{{child.content}}}")
            elif child.type == "em_open":
                parts.append("{\\em ")
            elif child.type == "em_close":
                parts.append("}")
            elif child.type == "strong_open":
                parts.append("{\\bf ")
            elif child.type == "strong_close":
                parts.append("}")
            elif child.type in ("softbreak", "hardbreak"):
                parts.append(" ")
        return "".join(parts)

    def footnote_ref(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render footnote reference in the text."""
        footnote_id = tokens[idx].meta.get("id")
        foot_note = env.get("footnotes", {}).get("list", {}).get(footnote_id, {})
        if "tokens" in foot_note:
            content = self._render_inline_tokens(foot_note["tokens"])
        else:
            content = foot_note.get("content", "")
        self.result.append(
            "{\\setupinteraction[color=black,contrastcolor=black]"
            + f"\\footnote{{{content}}}"
            + "}"
        )

    def _populate_reference_footnotes(self, tokens: Sequence[Token], env: EnvType) -> list[Token]:
        """Populate env footnotes for reference-style notes and return filtered token list.

        Supports both plugin modes:
        - with footnote_tail: content is in footnote_block_open ... footnote_block_close
        - without footnote_tail: content is in footnote_reference_open ... footnote_reference_close

        In both cases, reference note text is extracted into
        env['footnotes']['list'][id]['content'] and note-definition tokens are
        filtered out from the stream so they are never rendered as body text
        (ConTeXt/PDF use inline \footnote{}).
        """
        footnotes = env.get("footnotes", {})
        fn_list = env.get("footnotes", {}).get("list", {})
        refs = footnotes.get("refs", {})

        in_reference = False
        current_ref_id: int | None = None
        ref_parts: list[str] = []

        in_footnote_block = False
        in_footnote = False
        current_id: int | None = None
        filtered: list[Token] = []

        for tok in tokens:
            if tok.type == "footnote_reference_open":
                in_reference = True
                label = tok.meta.get("label", "")
                current_ref_id = refs.get(":" + label)
                ref_parts = []
                continue

            if tok.type == "footnote_reference_close":
                in_reference = False
                if current_ref_id is not None and "content" not in fn_list.get(current_ref_id, {}):
                    fn_list.setdefault(current_ref_id, {})["content"] = "".join(ref_parts).strip()
                current_ref_id = None
                continue

            if in_reference:
                if tok.type == "inline" and tok.children:
                    ref_parts.append(self._render_inline_tokens(tok.children))
                continue

            if tok.type == "footnote_block_open":
                in_footnote_block = True
                continue

            if tok.type == "footnote_block_close":
                in_footnote_block = False
                continue

            if not in_footnote_block:
                filtered.append(tok)
                continue

            # Inside footnote block — skip all tokens (they are never rendered
            # directly), but extract content for reference notes.
            if tok.type == "footnote_open":
                in_footnote = True
                current_id = tok.meta.get("id")
                continue

            if tok.type == "footnote_close":
                in_footnote = False
                current_id = None
                continue

            if in_footnote and tok.type == "inline" and tok.children and current_id is not None:
                foot_note = fn_list.get(current_id, {})
                # Only extract for reference notes ("label" but no "tokens")
                if "label" in foot_note and "tokens" not in foot_note:
                    if "content" not in foot_note:
                        fn_list.setdefault(current_id, {})["content"] = self._render_inline_tokens(
                            tok.children
                        )

        return filtered

    ###########################################################################
    # Table methods
    ###########################################################################

    def table_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table token."""
        self.result.append("\\bTABLE\n")

    def table_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table token."""
        self.result.append("\\eTABLE\n\n")

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


CONTEXT_FOOTER = """\\stoptext
"""
