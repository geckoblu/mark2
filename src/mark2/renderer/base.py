"""Base class for mark2 renderers."""

import inspect
import sys
from typing import Any, Sequence

from markdown_it.renderer import RendererProtocol, Token
from markdown_it.utils import EnvType, OptionsDict


class Renderer(RendererProtocol):
    """Base class for all mark2 renderers."""

    def __init__(self, parser: Any = None):
        """Initialize the renderer."""
        self.rules = {
            k: v
            for k, v in inspect.getmembers(self, predicate=inspect.ismethod)
            if not (k.startswith("render") or k.startswith("_"))
        }

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates output.

        :param tokens: list on block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input

        """
        for i, token in enumerate(tokens):
            if token.type == "inline":
                if token.children:
                    self.render_inline(token.children, options, env)
            elif token.type in self.rules:
                self.rules[token.type](tokens, i, options, env)
            else:
                self.render_token(tokens, i, options, env)

    def render_inline(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """The same as ``render``, but for single token of `inline` type.

        :param tokens: list on block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input (references, for example)
        """
        for i, token in enumerate(tokens):
            if token.type in self.rules:
                self.rules[token.type](tokens, i, options, env)
            else:
                self.render_token(tokens, i, options, env)

    def render_token(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> None:
        """Default token renderer.

        Can be overridden by custom function

        :param idx: token index to render
        :param options: params of parser instance
        """
        # raise NotImplementedError(f"[{tokens[idx]}]")
        print(f"[UNHANDLED TOKEN] {tokens[idx]}", file=sys.stderr)
        sys.exit(1)

    def _debug(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
        name: str = "[RENDER]",
    ) -> None:
        """Render opening paragraph token."""
        token = tokens[idx]
        print(
            f"{name} {token.type}: tag={token.tag}, nesting={token.nesting}, attrs={token.attrs}, content='{token.content}'",  # pylint: disable=line-too-long
            file=sys.stderr,
        )

    def _get_attr(self, token: Token, attr_name: str) -> str | None:
        """Get attribute value from token.

        Args:
            token: The markdown-it token
            attr_name: The name of the attribute

        Returns:
            The attribute value if found, None otherwise
        """
        if token.attrs:
            for attr in token.attrs:
                if attr[0] == attr_name:
                    return attr[1]
        return None

    def _get_href(self, token: Token) -> str | None:
        """Get href attribute from link token.

        Args:
            token: The markdown-it link token

        Returns:
            The href URL if found, None otherwise
        """
        return self._get_attr(token, "href")

    ###########################################################################
    # All the methods not starting with "render" nor "_" are rules renderers
    ###########################################################################

    def paragraph_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening paragraph token."""
        self._debug(tokens, idx, options, env)

    def paragraph_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing paragraph token."""
        self._debug(tokens, idx, options, env)

    def text(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render text token."""
        self._debug(tokens, idx, options, env)

    def em_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening emphasis token."""
        self._debug(tokens, idx, options, env)

    def em_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing emphasis token."""
        self._debug(tokens, idx, options, env)

    def heading_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening heading token."""
        self._debug(tokens, idx, options, env)

    def heading_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing heading token."""
        self._debug(tokens, idx, options, env)

    def bullet_list_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening bullet list token."""
        self._debug(tokens, idx, options, env)

    def bullet_list_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing bullet list token."""
        self._debug(tokens, idx, options, env)

    def ordered_list_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening ordered list token."""
        self._debug(tokens, idx, options, env)

    def ordered_list_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing ordered list token."""
        self._debug(tokens, idx, options, env)

    def list_item_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening list item token."""
        self._debug(tokens, idx, options, env)

    def list_item_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing list item token."""
        self._debug(tokens, idx, options, env)

    def link_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening link token."""
        self._debug(tokens, idx, options, env)

    def link_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing link token."""
        self._debug(tokens, idx, options, env)

    def strong_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening strong/bold token."""
        self._debug(tokens, idx, options, env)

    def strong_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing strong/bold token."""
        self._debug(tokens, idx, options, env)

    def code_inline(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render inline code token."""
        self._debug(tokens, idx, options, env)

    def code_block(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render code block token."""
        self._debug(tokens, idx, options, env)

    def fence(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render fenced code block token."""
        self._debug(tokens, idx, options, env)

    def blockquote_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening blockquote token."""
        self._debug(tokens, idx, options, env)

    def blockquote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing blockquote token."""
        self._debug(tokens, idx, options, env)

    def hr(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render horizontal rule token."""
        self._debug(tokens, idx, options, env)

    def image(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render image token."""
        self._debug(tokens, idx, options, env)

    def hardbreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render hard line break token."""
        self._debug(tokens, idx, options, env)

    def softbreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render soft line break token."""
        self._debug(tokens, idx, options, env)

    def html_block(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render HTML block token."""
        self._debug(tokens, idx, options, env)

    def html_inline(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render inline HTML token."""
        self._debug(tokens, idx, options, env)

    def s_open(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render opening strikethrough token."""
        self._debug(tokens, idx, options, env)

    def s_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing strikethrough token."""
        self._debug(tokens, idx, options, env)

    def table_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table token."""
        self._debug(tokens, idx, options, env)

    def table_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table token."""
        self._debug(tokens, idx, options, env)

    def thead_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table header token."""
        self._debug(tokens, idx, options, env)

    def thead_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table header token."""
        self._debug(tokens, idx, options, env)

    def tbody_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table body token."""
        self._debug(tokens, idx, options, env)

    def tbody_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table body token."""
        self._debug(tokens, idx, options, env)

    def tr_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table row token."""
        self._debug(tokens, idx, options, env)

    def tr_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table row token."""
        self._debug(tokens, idx, options, env)

    def th_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table header cell token."""
        self._debug(tokens, idx, options, env)

    def th_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table header cell token."""
        self._debug(tokens, idx, options, env)

    def td_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table data cell token."""
        self._debug(tokens, idx, options, env)

    def td_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table data cell token."""
        self._debug(tokens, idx, options, env)

    ###########################################################################
    # Footnote plugin renderers
    ###########################################################################

    # Helper methods (return values, used by other render rules)
    def footnote_anchor_name(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Generate footnote anchor ID.
        The anchor name is used in HTML id and href attributes for linking."""
        # return render_footnote_anchor_name(self, tokens, idx, options, env)
        self._debug(tokens, idx, options, env, name="  [FOOTNOTE]")

    def footnote_caption(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Generate footnote caption text.
        The caption is what's displayed to users (the visible number)."""
        # return render_footnote_caption(self, tokens, idx, options, env)
        self._debug(tokens, idx, options, env, name="  [FOOTNOTE]")

    # Token renderers
    def footnote_ref(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render footnote reference (inline superscript link)."""
        self._debug(tokens, idx, options, env, name="  [FOOTNOTE]")

    def footnote_block_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening of footnote block section."""
        self._debug(tokens, idx, options, env, name="  [FOOTNOTE]")

    def footnote_block_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing of footnote block section."""
        self._debug(tokens, idx, options, env, name="  [FOOTNOTE]")

    def footnote_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening of individual footnote item."""
        self._debug(tokens, idx, options, env, name="  [FOOTNOTE]")

    def footnote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing of individual footnote item."""
        self._debug(tokens, idx, options, env, name="  [FOOTNOTE]")

    def footnote_anchor(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render back-reference link at end of footnote."""
        self._debug(tokens, idx, options, env, name="  [FOOTNOTE]")

    def footnote_reference_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening of footnote reference item (in footnote block)."""
        self._debug(tokens, idx, options, env, name="  [FOOTNOTE]")

    def footnote_reference_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing of footnote reference item (in footnote block)."""
        self._debug(tokens, idx, options, env, name="  [FOOTNOTE]")
