#!/usr/bin/env python3
# pylint: skip-file
"""Generate pytest tests from spec.txt examples."""

import re
from pathlib import Path


def parse_spec_examples(spec_file):
    """Parse all examples from spec.txt file.

    Returns:
        List of tuples: (example_number, start_line, end_line, input_text, expected_output)
    """
    with open(spec_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    examples = []
    example_num = 0
    i = 0

    while i < len(lines):
        line = lines[i]

        # Look for example start
        if line.strip() == "`" * 32 + " example":
            example_num += 1
            start_line = i + 1
            i += 1

            # Collect input lines until we hit the separator '.'
            input_lines = []
            while i < len(lines) and lines[i].strip() != ".":
                input_lines.append(lines[i].rstrip("\n"))
                i += 1

            # Skip the '.' separator
            if i < len(lines) and lines[i].strip() == ".":
                i += 1

            # Collect expected output lines until we hit the closing backticks
            output_lines = []
            while i < len(lines) and lines[i].strip() != "`" * 32:
                # Keep the line as-is, removing only the final \n since we'll reconstruct properly
                output_lines.append(lines[i].rstrip("\n"))
                i += 1

            end_line = i + 1

            # Join lines with newlines, replacing → with actual tabs
            input_text = "\n".join(input_lines).replace("→", "\t")
            # For output, join with \n but don't add trailing \n
            # We'll strip it from the result in the test
            if output_lines:
                expected_output = "\n".join(output_lines).replace("→", "\t")
            else:
                expected_output = ""

            examples.append((example_num, start_line, end_line, input_text, expected_output))

        i += 1

    return examples


def escape_string(s):
    """Escape a string for Python source code."""
    return repr(s)


def generate_test_function(example_num, start_line, end_line, input_text, expected_output):
    """Generate a pytest test function for an example."""
    func_name = f"test_example{example_num}"

    # Create a descriptive name from the input (first 50 chars, safe characters only)
    desc = input_text[:50].replace("\n", " ").replace("\t", " ")
    desc = re.sub(r"[^a-zA-Z0-9 ]", "", desc).strip()
    if desc:
        desc = f": {desc}"
    else:
        desc = ""

    # Don't add any newline - use the expected output exactly as parsed
    # markdown-it.render() behavior varies: raw HTML passthrough has no \n,
    # but generated HTML (like <p> tags) adds \n
    expected_with_newline = expected_output

    return f'''@pytest.mark.spec
def {func_name}():
    """Test example {example_num}{desc}.

    Source: spec.txt lines {start_line}-{end_line}
    """
    md = MarkdownIt()

    input_text = {escape_string(input_text)}
    expected = {escape_string(expected_with_newline)}

    result = md.render(input_text).rstrip('\\n')
    assert result == expected


'''


def generate_test_file(examples, output_file):
    """Generate the complete test file."""
    header = '''# pylint: skip-file
# fmt: off
"""Test spec examples for default HTML rendering.

This file is auto-generated from spec.txt.
Run generate_test_default.py to regenerate.
"""

import pytest
from markdown_it import MarkdownIt


'''

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header)

        for example_num, start_line, end_line, input_text, expected_output in examples:
            test_func = generate_test_function(
                example_num, start_line, end_line, input_text, expected_output
            )
            f.write(test_func)


if __name__ == "__main__":
    spec_file = Path(__file__).parent.parent / "spec.txt"
    output_file = Path(__file__).parent / "test_default.py"

    print(f"Parsing examples from {spec_file}...")
    examples = parse_spec_examples(spec_file)
    print(f"Found {len(examples)} examples")

    print(f"Generating tests to {output_file}...")
    generate_test_file(examples, output_file)
    print("Done!")
