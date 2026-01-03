#!/usr/bin/env python3
"""Test script for parsing and rendering Markdown lists.

This module demonstrates the behavior of markdown-it parser with different
list formatting styles, particularly nested lists with and without blank lines.
"""

from markdown_it import MarkdownIt
from markdown_it.token import Token

LIST1 = """
- a
- b
  - c
  - d
"""

LIST2 = """
- a
- b

  - c
  - d
"""


def print_tokens(tokens: list[Token], indent: int = 0) -> None:
    """Recursively print tokens with indentation.

    Args:
        tokens: List of markdown-it tokens to print.
        indent: Number of spaces to indent (default: 0).
    """
    for token in tokens:
        # print(" " * indent + f"type: {token.type}, content: '{token.content}'")
        print(" " * indent + f"{token}")
        if token.children:
            print_tokens(token.children, indent + 2)


def main() -> None:
    """Test markdown list parsing and rendering.

    Parses and prints tokens for two different list formatting styles:
    - LIST1: Nested list without blank lines
    - LIST2: Nested list with blank lines
    """
    md = MarkdownIt()

    # tokens = md.parse("some *text*")
    # print_tokens(tokens)

    tokens = md.parse(LIST1)
    print_tokens(tokens)
    print()
    print(md.render(LIST1))

    print("\n---\n")

    tokens = md.parse(LIST2)
    print_tokens(tokens)
    print()
    print(md.render(LIST2))


if __name__ == "__main__":
    main()
