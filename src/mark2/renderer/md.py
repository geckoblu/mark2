"""Minimal Markdown renderer compatible with markdown-it."""

from typing import Any, Sequence

from markdown_it.renderer import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.plugins.yaml_parser import parse_simple_yaml
from mark2.renderer.baserenderer import BaseRenderer
from mark2.renderer.util import open_output


class MDRenderer(BaseRenderer):
    """A minimal Markdown renderer for markdown-it tokens."""

    result: list[str]

    link_href: str | None
    in_quote: bool
    ordered_list_counter: int
    nested_list_level: int

    def __init__(self, parser: Any = None) -> None:
        """Initialize the renderer.

        Args:
            parser: Optional parser instance
        """
        super().__init__(parser)

        self.result = []

        self.link_href = None
        self.in_quote = False
        self.ordered_list_counter = -1
        self.nested_list_level = 0

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates Markdown output.

        :param tokens: list of block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input

        """

        self.result = []

        super().render(tokens, options, env)

        tex = "".join(self.result)

        front_matter = env.get("front_matter")
        if front_matter:
            fm_lines = ["---\n"]
            for key, value in front_matter.items():
                fm_lines.append(f"{key}: {value}\n")
            fm_lines.append("---\n\n")
            tex = "".join(fm_lines) + tex

        output_filename = env.get("output_filename", "-")
        with open_output(output_filename) as writer:
            writer.write(tex)

    def text(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render text token."""
        token = tokens[idx]
        txt = token.content.replace("\xa0", "&nbsp;")
        self.result.append(txt)

    def paragraph_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening paragraph token."""
        if self.in_quote:
            self.result.append("> ")

    def paragraph_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing paragraph token.

        Adds an empty line at the closing of each paragraph, except inside list items.
        """
        # Inside blockquote, handle specially
        if self.in_quote and idx + 1 < len(tokens) and tokens[idx + 1].type != "blockquote_close":
            self.result.append("\n>\n")
        # Inside list item, only add single newline (no empty line)
        elif self.nested_list_level > 0:
            self.result.append("\n")
        # Normal case: add empty line (double newline)
        else:
            self.result.append("\n\n")

    def heading_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening heading token."""
        token = tokens[idx]
        level = int(token.tag[1])  # h1 -> 1, h2 -> 2, etc.
        self.result.append("#" * level + " ")

    def heading_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing heading token."""
        self.result.append("\n\n")

    def bullet_list_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening bullet list token."""
        self.nested_list_level += 1

    def bullet_list_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing bullet list token."""
        self.nested_list_level -= 1
        if self.nested_list_level < 0:
            raise ValueError("Nested list level went below zero")

        # If  the next token is another list item or list (nested_list_level > 0),
        # do not add extra newline
        if self.nested_list_level == 0:
            self.result.append("\n")

    def ordered_list_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening ordered list token."""
        self.nested_list_level += 1
        self.ordered_list_counter = 1

    def ordered_list_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing ordered list token."""
        self.ordered_list_counter = -1

        self.bullet_list_close(tokens, idx, options, env)

    def list_item_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening list item token.

        NOTE: this code doesn't handle multi-line list items (Loose list) correctly.
        """
        indent = "  " * (self.nested_list_level - 1)
        if self.ordered_list_counter > 0:
            self.result.append(f"{indent}{self.ordered_list_counter}. ")
            self.ordered_list_counter += 1
        else:
            self.result.append(f"{indent}- ")

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
        self.link_href = token.attrGet("href")
        self.result.append("[")

    def link_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing link token."""
        self.result.append("]")
        if self.link_href:
            self.result.append(f"({self.link_href})")

    def em_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening emphasis token."""
        self.result.append("*")

    def em_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing emphasis token."""
        self.result.append("*")

    def strong_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening strong/bold token."""
        self.result.append("**")

    def strong_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing strong/bold token."""
        self.result.append("**")

    def hardbreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render hard line break token."""
        self.result.append("\\\n")

    def softbreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render soft line break token."""
        word_wrap = env.get("md_word_wrap", "no")
        if word_wrap == "keep":
            self.result.append("\n")
        else:
            self.result.append(" ")

    def hr(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render soft line break token."""
        self.result.append("***\n\n")

    def blockquote_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening blockquote token."""
        # self.result.append("> ")
        self.in_quote = True

    def blockquote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing blockquote token."""
        self.in_quote = False

    ###########################################################################
    # Footnote plugin renderers
    ###########################################################################

    def footnote_ref(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render footnote reference in the text."""
        # ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)
        caption: str = self.rules["footnote_caption"](tokens, idx, options, env)

        # if tokens[idx].meta.get("subId", -1) > 0:
        #     refid += ":" + str(tokens[idx].meta["subId"])

        self.result.append(f"[^{caption}]")

    def footnote_anchor(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render back-reference link at end of footnote."""
        # ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)
        caption: str = self.rules["footnote_caption"](tokens, idx, options, env)

        # if tokens[idx].meta.get("subId", -1) > 0:
        #     refid += ":" + str(tokens[idx].meta["subId"])

        self.result.append(f"[^{caption}]: ")

    def footnote_block_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening of footnote block section."""
        pass

    def footnote_block_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing of footnote block section."""
        pass

    def footnote_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening of individual footnote item."""
        pass

    def footnote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing of individual footnote item."""
        pass

    ###########################################################################
    # Frontmatter plugin renderers
    ###########################################################################

    def front_matter(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Parse front matter block (not included in output)."""
        token = tokens[idx]
        env["front_matter"] = parse_simple_yaml(token.content, keep_multiline=True)

    ###########################################################################
    # Pagebreak plugin renderer
    ###########################################################################

    def pagebreak(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> None:
        """Render a pagebreak token.

        Args:
            self: The renderer instance
            tokens: List of all tokens being rendered
            idx: Index of the current pagebreak token to render
            options: Markdown-it parser options
            env: Environment variables for rendering context
        """
        self.result.append("---\n\n")

    ###########################################################################
    # MyST role plugin renderer
    ###########################################################################

    def myst_role(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render MyST role (inline span)."""
        token = tokens[idx]
        name = token.meta.get("name")
        self.result.append(f"{{{name}}}")
