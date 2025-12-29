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

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates output.

        :param tokens: list on block tokens to render
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
        """Render closing paragraph token."""
        # Check if next token is list_item_close - if so, only add one newline
        if idx + 1 < len(tokens) and tokens[idx + 1].type == "list_item_close":
            self.result.append("\n")
        elif idx + 1 < len(tokens) and tokens[idx + 1].type != "blockquote_close" and self.in_quote:
            self.result.append("\n>\n")
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
        pass

    def bullet_list_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing bullet list token."""
        self.result.append("\n")

    def ordered_list_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening ordered list token."""
        self.ordered_list_counter = 1

    def ordered_list_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing ordered list token."""
        self.ordered_list_counter = -1
        self.result.append("\n")

    def list_item_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening list item token."""
        if self.ordered_list_counter > 0:
            self.result.append(f"{self.ordered_list_counter}. ")
            self.ordered_list_counter += 1
        else:
            self.result.append("- ")

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
        self.result.append(" ")

    def hr(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render soft line break token."""
        self.result.append("---\n\n")

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

    # def front_matter(
    #     self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    # ) -> None:
    #     token = tokens[idx]
    #     self.result.append("---\n")
    #     self.result.append(token.content)
    #     self.result.append("\n---\n\n")

    # def __init__(self, parser: Any = None):
    #     """Initialize the renderer."""

    # def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
    #     """
    #     Render tokens to Markdown.

    #     Args:
    #         tokens: List of tokens from markdown-it parser
    #         options: Optional rendering options
    #         env: Optional environment variables

    #     Returns:
    #         str: Rendered Markdown string
    #     """
    #     if options is None:
    #         options = {}
    #     if env is None:
    #         env = {}

    #     result = []
    #     self._render_tokens(tokens, result)
    #     md = "".join(result)

    #     output_filename = env.get("output_filename", "-")
    #     with open_output(output_filename) as writer:
    #         print(md, file=writer)

    # def _render_tokens(self, tokens: list, result: list[str]) -> None:
    #     """Recursively render tokens."""
    #     for token in tokens:
    #         if token.type == "paragraph_open":
    #             pass
    #         elif token.type == "paragraph_close":
    #             result.append("\n\n")
    #         elif token.type == "heading_open":
    #             level = int(token.tag[1])  # h1 -> 1, h2 -> 2, etc.
    #             result.append("#" * level + " ")
    #         elif token.type == "heading_close":
    #             result.append("\n\n")
    #         elif token.type == "text":
    #             result.append(token.content)
    #         elif token.type == "inline":
    #             if token.children:
    #                 self._render_tokens(token.children, result)
    #         elif token.type == "em_open":
    #             result.append("*")
    #         elif token.type == "em_close":
    #             result.append("*")
    #         elif token.type == "strong_open":
    #             result.append("**")
    #         elif token.type == "strong_close":
    #             result.append("**")
    #         elif token.type == "code_inline":
    #             result.append(f"`{token.content}`")
    #         elif token.type == "code_block":
    #             result.append(f"    {token.content}\n")
    #         elif token.type == "fence":
    #             info = token.info or ""
    #             result.append(f"```{info}\n{token.content}```\n\n")
    #         elif token.type == "bullet_list_open":
    #             pass
    #         elif token.type == "bullet_list_close":
    #             result.append("\n")
    #         elif token.type == "ordered_list_open":
    #             pass
    #         elif token.type == "ordered_list_close":
    #             result.append("\n")
    #         elif token.type == "list_item_open":
    #             result.append("- ")
    #         elif token.type == "list_item_close":
    #             result.append("\n")
    #         elif token.type == "blockquote_open":
    #             result.append("> ")
    #         elif token.type == "blockquote_close":
    #             result.append("\n")
    #         elif token.type == "link_open":
    #             result.append("[")
    #         elif token.type == "link_close":
    #             href = self._get_href(token)
    #             result.append(f"]({href})")
    #         elif token.type == "image":
    #             alt = token.content or ""
    #             href = self._get_attr(token, "src") or ""
    #             result.append(f"![{alt}]({href})")
    #         elif token.type == "softbreak":
    #             result.append("\n")
    #         elif token.type == "hardbreak":
    #             result.append("  \n")
    #         elif token.type == "hr":
    #             result.append("---\n\n")

    # def _get_attr(self, token, attr_name: str) -> str | None:
    #     """Get attribute value from token."""
    #     if token.attrs:
    #         for attr in token.attrs:
    #             if attr[0] == attr_name:
    #                 return attr[1]
    #     return None

    # def _get_href(self, token) -> str | None:
    #     """Get href from link token."""
    #     return self._get_attr(token, "href")

    ###########################################################################
    # Frontmatter plugin renderers
    ###########################################################################

    def front_matter(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Parse front matter block (not included in output)."""
        # super().front_matter(tokens, idx, options, env)
        # token = tokens[idx]
        # print("Front Matter:", token.content)
        # self.result.append("---\n")
        # self.result.append(token.content)
        # self.result.append("\n---\n\n")
        token = tokens[idx]
        env["front_matter"] = parse_simple_yaml(token.content, keep_multiline=True)
