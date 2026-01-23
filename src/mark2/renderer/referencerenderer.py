"""Reference HTML renderer for markdown-it."""

import sys
from typing import Any, Sequence

# Import Footnote render functions
from mdit_py_plugins.footnote.index import (
    render_footnote_anchor,
    render_footnote_anchor_name,
    render_footnote_block_close,
    render_footnote_block_open,
    render_footnote_caption,
    render_footnote_close,
    render_footnote_open,
    render_footnote_ref,
)

from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.baserenderer import BaseRenderer


class ReferenceRenderer(BaseRenderer):
    """A reference HTML renderer that produces clean, semantic HTML."""

    __output__: str = "html"
    result: list[str]
    html: str
    debug: bool

    def __init__(self, parser: Any = None) -> None:
        """Initialize the renderer.

        Args:
            parser: Optional parser instance
        """
        super().__init__(parser)

        self.result = []
        self.html = ""
        self.debug = False

    def render_token(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> None:
        """Default token renderer."""
        self._debug_output(tokens, idx, options, env)

    def _debug_output(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> None:
        """Print debug output in a single line with fixed width formatting.

        Args:
            tokens: Token sequence
            idx: Current token index
            options: Parser options
            env: Environment
            output: The HTML output to display (max 20 chars)
        """
        token = tokens[idx]
        # Create the first part (25 chars max)
        first_part = f"[TOKEN {token.type}"
        first_part = first_part.ljust(23) + "]:"
        # Truncate if too long and pad to 25 chars
        if len(first_part) > 25:
            first_part = first_part[:22] + "..."

        # Create the second part (50 chars max)
        second_part = f"tag={token.tag}, nesting={token.nesting}, attrs={token.attrs}"
        second_part = second_part.replace(", ", ",\t")  # Replace comma+space with comma+tab
        second_part = second_part.ljust(50)
        # Truncate if too long and pad to 50 chars
        if len(second_part) > 50:
            second_part = second_part[:47] + "..."

        # Second part (40 chars max)
        tirth_part = token.content.replace("\n", "↩").replace("\r", "↩")  # Escape newlines
        if len(tirth_part) > 50:
            tirth_part = tirth_part[:47] + "..."

        print(f"{first_part}  {second_part}  {tirth_part}", file=sys.stderr)
