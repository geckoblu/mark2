"""The content of this file is adapted from mdit_py_plugins.myst_role.myst_role_plugin,
with modifications to allow empty content roles."""

import re
import sys
from typing import Sequence

from markdown_it import MarkdownIt

from markdown_it.renderer import RendererProtocol
from markdown_it.rules_inline import StateInline
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

# Matches role names like {role-name}, {abbr}, {line-break}, etc.
VALID_NAME_PATTERN = re.compile(r"^\{([a-zA-Z0-9\_\-\+\:]+)\}")

# Set of roles that are allowed to have empty content
ALLOWED_EMPTY_ROLES = {"line-break"}


def myst_role_plugin(md: MarkdownIt) -> None:
    """Register MyST role parser and renderer with MarkdownIt.

    Supports standard MyST roles like {role-name}`content` and special
    contentless roles like {line-break}.

    Args:
        md: MarkdownIt instance to register the plugin with
    """
    md.inline.ruler.before("backticks", "myst_role", myst_role)

    if hasattr(md.renderer, "myst_role"):
        md.add_render_rule("myst_role", md.renderer.myst_role)
    else:
        md.add_render_rule("myst_role", render_myst_role)


def myst_role(state: StateInline, silent: bool) -> bool:
    """Parse MyST role syntax {role-name}`content` or special ALLOWED_EMPTY_ROLES without content.

    Args:
        state: The inline parser state
        silent: If True, only check if pattern matches without creating tokens

    Returns:
        True if a role was successfully parsed, False otherwise
    """
    # Check if the current position matches a valid role name pattern
    match = VALID_NAME_PATTERN.match(state.src[state.pos :])
    if not match:
        return False
    name = match.group(1)

    # Check if role is escaped with backslash (e.g., \{role})
    try:
        if state.src[state.pos - 1] == "\\":
            # Role is escaped, don't parse it
            return False
    except IndexError:
        pass

    # Count the number of opening backticks after the role name
    start = pos = state.pos + match.end()
    try:
        while state.src[pos] == "`":
            pos += 1
    except IndexError:
        return False

    tick_length = pos - start
    if tick_length == 0:
        # Special case: allow roles without any content or backticks if in allowed list
        if name in ALLOWED_EMPTY_ROLES:
            if not silent:
                token = state.push("myst_role", "", 0)
                token.meta = {"name": name}
                token.content = ""
            state.pos = pos
            return True
        else:
            return False

    # Search for matching closing backticks
    match = re.search("`" * tick_length, state.src[pos + 1 :])
    if not match:
        return False
    # Extract content and normalize newlines to spaces
    content = state.src[pos : pos + match.start() + 1].replace("\n", " ")

    if not silent:
        token = state.push("myst_role", "", 0)
        token.meta = {"name": name}
        token.content = content

    state.pos = pos + match.end() + 1

    return True


def render_myst_role(
    self: "RendererProtocol",
    tokens: Sequence[Token],
    idx: int,
    options: "OptionsDict",
    env: "EnvType",
) -> str:
    """Render a MyST role token (currently outputs debug info to stderr).

    Args:
        self: The renderer instance
        tokens: List of all tokens
        idx: Index of the current token to render
        options: Markdown-it options
        env: Environment for rendering

    Returns:
        Empty string (debug-only implementation)
    """
    token = tokens[idx]
    name = token.meta.get("name", "unknown")

    print(
        f"  [MYST_ROLE] {token.type}: name={name}, attrs={token.attrs}, content='{token.content}'",
        file=sys.stderr,
    )
    return ""
