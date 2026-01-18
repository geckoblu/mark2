"""mark2 - A Markdown file converter supporting multiple output formats.

This package provides tools to convert Markdown files to various output formats
including HTML, EPUB, PDF, and ConTeXt.
"""

import sys
from typing import Sequence

from markdown_it.renderer import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2 import renderer


def render_undefined(
    self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType, name: str
) -> str:
    """Placeholder for undefined render rules.

    This function is used when a render rule is expected but not implemented
    in the current renderer. It returns an empty string to prevent errors.

    Args:
        self: Renderer instance
        tokens: Token sequence
        idx: Current token index
        options: Parser options
        env: Environment
        name: Name of the undefined render rule for debugging

    Returns:
        Empty string
    """
    token = tokens[idx]
    print(
        f"{name} {token.type}: tag={token.tag}, nesting={token.nesting}, attrs={token.attrs}, content='{token.content}'",  # pylint: disable=line-too-long
        file=sys.stderr,
    )
    return ""
