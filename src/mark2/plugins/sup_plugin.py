"""Superscript plugin for markdown-it-py.

Process ^superscript^ syntax.
"""

import re
import sys
from typing import Sequence

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol
from markdown_it.rules_inline import StateInline
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

# Same as UNESCAPE_MD_RE plus a space
UNESCAPE_RE = re.compile(r'\\([ \\!"#$%&\'()*+,./:;<=>?@\[\]^_`{|}~-])')


def sup_plugin(md: MarkdownIt) -> None:
    """Register superscript parser with MarkdownIt.

    Args:
        md: MarkdownIt instance to register the plugin with
    """
    md.inline.ruler.after("emphasis", "sup", _superscript)

    # Set renderer for sup_open tokens
    if hasattr(md.renderer, "sup_open"):
        md.add_render_rule("sup_open", md.renderer.sup_open)
        md.add_render_rule("sup_close", md.renderer.sup_close)
    else:
        md.add_render_rule("sup_open", render_sup_open)
        md.add_render_rule("sup_close", render_sup_close)


def _superscript(state: StateInline, silent: bool = False) -> bool:
    """Parse superscript syntax ^text^.

    Args:
        state: The inline parser state
        silent: If True, only check if pattern matches without creating tokens

    Returns:
        True if superscript was successfully parsed, False otherwise
    """
    start = state.pos
    max_pos = state.posMax

    # Check if current character is ^
    if state.src[start : start + 1] != "^":
        return False

    if silent:
        return False  # don't run any pairs in validation mode

    if start + 2 >= max_pos:
        return False

    state.pos = start + 1
    found = False

    while state.pos < max_pos:
        if state.src[state.pos : state.pos + 1] == "^":
            found = True
            break

        state.md.inline.skipToken(state)

    if not found or start + 1 == state.pos:
        state.pos = start
        return False

    content = state.src[start + 1 : state.pos]

    # Don't allow unescaped spaces/newlines inside
    if re.search(r"(^|[^\\])(\\\\)*\s", content):
        state.pos = start
        return False

    # Found!
    state.posMax = state.pos
    state.pos = start + 1

    # Earlier we checked !silent, but this implementation does not need it
    token_so = state.push("sup_open", "sup", 1)
    token_so.markup = "^"

    token_t = state.push("text", "", 0)
    token_t.content = UNESCAPE_RE.sub(r"\1", content)

    token_sc = state.push("sup_close", "sup", -1)
    token_sc.markup = "^"

    state.pos = state.posMax + 1
    state.posMax = max_pos
    return True


def render_sup_open(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    """Render opening <sup> tag.

    Returns:
        The HTML string for opening <sup> tag
    """
    token = tokens[idx]
    # Debug output to stderr
    print(
        f"  [SUP_OPEN] {token.type}: attrs={token.attrs}, content='{token.content}'",
        file=sys.stderr,
    )
    return ""


def render_sup_close(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    """Render closing </sup> tag.

    Returns:
        The HTML string for closing </sup> tag
    """
    token = tokens[idx]
    # Debug output to stderr
    print(
        f"  [SUP_CLOSE] {token.type}: attrs={token.attrs}, content='{token.content}'",
        file=sys.stderr,
    )
    return ""
