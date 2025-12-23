"""YAML parser for frontmatter.

This module provides a lightweight parser for a simplified subset of YAML,
specifically designed for parsing frontmatter in Markdown documents. It supports
basic key-value pairs with automatic type coercion and multi-line strings using
YAML block scalars.

The parser intentionally implements only a subset of YAML features needed for
frontmatter use cases, avoiding the complexity and security concerns of full
YAML parsing.
"""


def parse_simple_yaml(text: str) -> dict[str, any]:
    """Parse a simplified subset of YAML frontmatter.

    This parser supports:
    - Simple key-value pairs (key: value)
    - Type coercion for booleans, integers, floats, and strings
    - Multi-line strings using block scalars (| and >)
    - Comments (lines starting with #)

    Args:
        text: The YAML text to parse.

    Returns:
        A dictionary containing the parsed key-value pairs. Values are
        automatically coerced to appropriate Python types (bool, int, float, str).

    Raises:
        ValueError: If a line doesn't contain a colon separator or is malformed.

    Examples:
        >>> parse_simple_yaml("title: My Document\\nauthor: John Doe")
        {'title': 'My Document', 'author': 'John Doe'}

        >>> parse_simple_yaml("count: 42\\nenabled: true")
        {'count': 42, 'enabled': True}

        >>> parse_simple_yaml("description: |\\n  Line 1\\n  Line 2")
        {'description': 'Line 1\\nLine 2'}

        >>> parse_simple_yaml("summary: >\\n  This text\\n  will be folded")
        {'summary': 'This text will be folded'}

    Note:
        - Block scalar (|) preserves newlines literally
        - Folded scalar (>) joins lines with spaces, preserving paragraph breaks
        - Indentation is automatically detected from the first non-empty line
        - Quoted strings have quotes stripped
    """
    data: dict[str, any] = {}
    lines: list[str] = text.splitlines()
    i: int = 0

    while i < len(lines):
        line: str = lines[i]
        stripped_line: str = line.strip()

        if not stripped_line or stripped_line.startswith("#"):
            i += 1
            continue

        if ":" not in stripped_line:
            raise ValueError(f"Invalid frontmatter line {i + 1}: {stripped_line}")

        key: str
        value: str | int | float | bool
        key, value = stripped_line.split(":", 1)
        key = key.strip()
        value = value.strip()

        # Handle multi-line strings (block scalars)
        if value in ("|", ">"):
            i, value = parse_multi_line(lines, i, value)
        else:
            # Single-line value: type coercion
            if value.lower() in ("true", "false"):
                value = value.lower() == "true"
            else:
                try:
                    if "." in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    value = value.strip("\"'")  # string
            i += 1

        data[key] = value

    return data


def parse_multi_line(
    lines: list[str],
    start_index: int,
    block_type: str,
) -> tuple[int, str]:
    """Parse multi-line string values using YAML block scalars.

    This function handles both literal (|) and folded (>) block scalar styles.
    It automatically detects indentation and collects all lines belonging to
    the block until a less-indented line or end of input is encountered.

    Args:
        lines: List of all lines in the YAML text.
        start_index: The index of the line containing the block scalar indicator.
        block_type: The block scalar style ('|' for literal, '>' for folded).

    Returns:
        A tuple containing:
        - The index of the next line to process after the block
        - The parsed multi-line string value

    Note:
        - Literal style (|) preserves all newlines
        - Folded style (>) joins lines with spaces, preserving empty line paragraph breaks
        - Indentation is automatically detected from the first non-empty content line
    """
    i = start_index + 1

    # Collect indented lines
    block_lines: list[str] = []
    base_indent: int | None = None

    while i < len(lines):
        current_line: str = lines[i]

        # Skip empty lines at the start to find base indentation
        if not current_line.strip() and base_indent is None:
            i += 1
            continue

        # Detect base indentation from first non-empty line
        if base_indent is None and current_line.strip():
            base_indent = len(current_line) - len(current_line.lstrip())
            if base_indent == 0:
                break  # No indentation, end of block

        # Check if line belongs to the block (must be indented)
        if current_line.strip():  # Non-empty line
            current_indent: int = len(current_line) - len(current_line.lstrip())
            if current_indent < base_indent:
                break  # Less indented, end of block
            # Remove base indentation
            block_lines.append(current_line[base_indent:])
        else:
            # Empty line within block
            block_lines.append("")

        i += 1

    # Process block based on type
    if block_type == "|":
        # Literal: preserve newlines
        value = "\n".join(block_lines).rstrip()
    else:  # ">"
        # Folded: join lines with spaces, preserve paragraph breaks
        paragraphs: list[str] = []
        current_para: list[str] = []
        for block_line in block_lines:
            if not block_line.strip():
                if current_para:
                    paragraphs.append(" ".join(current_para))
                    current_para = []
                paragraphs.append("")
            else:
                current_para.append(block_line.strip())
        if current_para:
            paragraphs.append(" ".join(current_para))
        value = "\n".join(paragraphs).rstrip()

    return i, value
