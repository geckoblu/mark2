"""The content of this file is adapted from mdit_py_plugins.myst_role.myst_role_plugin,
with modifications to allow empty content roles."""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

# Matches role names like {role-name}, {abbr}, {line-break}, etc.
VALID_NAME_PATTERN = re.compile(r"^\{([a-zA-Z0-9\_\-\+\:]+)\}")

# Set of roles that are allowed to have empty content
ALLOWED_EMPTY_ROLES = {"line-break", "br"}
EMPTY_ROLES_ALIAS = {"br": "line-break"}


def myst_role_plugin(md: MarkdownIt) -> None:
    """Register MyST role parser and renderer with MarkdownIt.

    Supports standard MyST roles like {role-name}`content` and special
    contentless roles like {line-break}.

    Args:
        md: MarkdownIt instance to register the plugin with
    """
    md.inline.ruler.before("backticks", "myst_role", myst_role)


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
            # Normalize role name if it's an alias
            name = EMPTY_ROLES_ALIAS.get(name, name)
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
