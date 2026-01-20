"""Page break plugin for markdown-it-py.

This plugin intercepts three-dash sequences (---) and transforms them into
custom pagebreak tokens. Thematic breaks with asterisks (***) are not affected.
"""

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock


def pagebreak_plugin(md: MarkdownIt) -> None:
    """Parse page breaks (``---``) in Markdown documents."""
    md.block.ruler.before("hr", "pagebreak", pagebreak_rule)


def pagebreak_rule(state: StateBlock, startline: int, endline: int, silent: bool) -> bool:
    """Parse page breaks (---) but not thematic breaks (***).

    Args:
        state: The current parsing state
        startline: The line number where parsing starts
        endline: The line number where parsing ends
        silent: If True, only check if the rule matches without creating tokens

    Returns:
        True if a pagebreak was successfully parsed, False otherwise
    """
    pos = state.bMarks[startline] + state.tShift[startline]
    maximum = state.eMarks[startline]

    # Check if line is too short for a pagebreak (minimum 3 characters)
    if pos + 3 > maximum:
        return False

    # Must start with a dash character
    marker = state.src[pos]
    if marker != "-":
        return False

    # Count consecutive dash characters
    cnt = 1
    pos += 1
    while pos < maximum and state.src[pos] == marker:
        cnt += 1
        pos += 1

    # # Must be exactly 3 dashes to distinguish from thematic breaks
    # if cnt != 3:
    #     return False

    # Ensure no non-whitespace trailing content on the line
    while pos < maximum:
        if not state.src[pos].isspace():
            return False
        pos += 1

    if silent:
        return True

    # Create custom pagebreak token
    token = state.push("pagebreak", "", 0)
    token.markup = "---"
    token.map = [startline, state.line]

    state.line = startline + 1
    return True
