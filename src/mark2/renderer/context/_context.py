# pylint: skip-file

"""Minimal ConTeXt renderer compatible with markdown-it."""

from typing import Any, Sequence

from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.baserenderer import BaseRenderer
from mark2.renderer.util import open_output
from mark2.plugins.yaml_parser import parse_simple_yaml


class ConTeXtRenderer(BaseRenderer):
    """A minimal ConTeXt renderer for markdown-it tokens."""

    __output__: str = "text"
    result: list[str]
    in_link: bool
    link_href: str

    def __init__(self, parser: Any = None) -> None:
        """Initialize the renderer.

        Args:
            parser: Optional parser instance
        """
        super().__init__(parser)

        self.result = []

        self.in_link = False
        self.link_href = ""

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates ConTeXt output.

        :param tokens: list of block tokens to render
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

    def render_token(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> None:
        """Handle dynamic container tokens and other unhandled tokens.

        :param tokens: list of tokens
        :param idx: token index to render
        :param options: params of parser instance
        :param env: additional data from parsed input
        """
        token = tokens[idx]

        # Handle dynamic container tokens (container_{name}_open/close)
        if token.type.startswith("container_") and token.type.endswith("_open"):
            self.container_open(tokens, idx, options, env)
        elif token.type.startswith("container_") and token.type.endswith("_close"):
            self.container_close(tokens, idx, options, env)
        else:
            # Call parent's render_token for truly unhandled tokens
            super().render_token(tokens, idx, options, env)

    ###########################################################################
    # All the methods not starting with "render" nor "_" are rules renderers
    ###########################################################################

    def fence(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render fenced code block token."""
        token = tokens[idx]
        # ConTeXt doesn't have built-in syntax highlighting in the same way,
        # but we can use typing environment
        self.result.append("\\starttyping\n")
        self.result.append(token.content)
        self.result.append("\\stoptyping\n\n")

    def hr(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render horizontal rule token."""
        self.result.append("\\thinrule\n\n")

    def image(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render image token."""
        token = tokens[idx]
        src = token.attrGet("src") or ""
        alt = token.attrGet("alt") or ""
        # ConTeXt image inclusion
        self.result.append(f"\\externalfigure[{src}]")
        if alt:
            self.result.append(f"[{alt}]")
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

    def front_matter(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Parse front matter block and store in environment."""
        token = tokens[idx]
        env["front_matter"] = parse_simple_yaml(token.content)
        # Front matter is not rendered in ConTeXt output
        # Could be used to set document metadata if needed

    def myst_role(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render MyST role inline span."""
        token = tokens[idx]
        name = token.meta.get("name", "unknown")

        # Handle special roles
        if name == "line-break" and token.content == "":
            self.result.append("\\crlf\n")
        else:
            # For other roles, render content with comment about role
            if token.children:
                # Render child tokens inline
                self.render_inline(token.children, options, env)
            elif token.content:
                self.result.append(self._escape_tex(token.content))

    def container_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening of custom container."""
        token = tokens[idx]
        # Extract container class/name from token info
        info = token.info.strip().split(" ", 1)[0] if token.info else ""
        # Use ConTeXt framed environment for containers
        self.result.append(f"% Container: {info}\n")
        self.result.append("\\startframedtext\n")

    def container_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing of custom container."""
        self.result.append("\\stopframedtext\n\n")


CONTEXT_HEADER = """% !TeX program = context
% ConTeXt Mk XL (LuaMetaTeX)
\\starttext
"""

CONTEXT_FOOTER = """\\stoptext
"""
