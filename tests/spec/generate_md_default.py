#!/usr/bin/env python3
"""Generate pytest tests for markdown-to-markdown rendering from spec.txt examples."""

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


def generate_test_function(example_num, start_line, end_line, input_text):
    """Generate a pytest test function for a markdown example.

    For markdown-to-markdown rendering, input and expected are the same.
    """
    func_name = f"test_md_example{example_num}"

    # Create a descriptive name from the input (first 50 chars, safe characters only)
    desc = input_text[:50].replace("\n", " ").replace("\t", " ")
    desc = re.sub(r"[^a-zA-Z0-9 ]", "", desc).strip()
    if desc:
        desc = f": {desc}"
    else:
        desc = ""

    return f'''@pytest.mark.spec
def {func_name}():
    """Test markdown example {example_num}{desc}.

    Source: spec.txt lines {start_line}-{end_line}
    """
    md = MarkdownIt(renderer_cls=MDRenderer)

    input_text = {escape_string(input_text)}
    expected = {escape_string(input_text)}

    result = render_str_output(md, input_text).rstrip('\\n')
    assert result == expected


'''


def generate_test_file(examples, output_file):
    """Generate the complete test file."""
    header = '''# pylint: skip-file
# fmt: off
"""Test spec examples for markdown-to-markdown rendering.

This file is auto-generated from spec.txt.
Run generate_md_default.py to regenerate.
"""

import io
from contextlib import redirect_stdout

import pytest
from markdown_it import MarkdownIt
from mark2.renderer import MDRenderer


def render_str_output(
    md: MarkdownIt,
    markdown_input: str,
) -> str:
    """Render markdown input using MarkdownIt instance and return the output string."""

    # Capture stdout since render() writes to stdout when output is "-"
    env = {"output_filename": "-"}
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        # Parse and render
        md.render(markdown_input, env=env)

    rendered_output = output_buffer.getvalue()

    return rendered_output


'''

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header)

        for example_num, start_line, end_line, input_text, expected_output in examples:
            test_func = generate_test_function(example_num, start_line, end_line, input_text)
            f.write(test_func)


def main():
    """Generate pytest test file for markdown-to-markdown rendering from spec.txt examples.

    Parses spec.txt for markdown examples and generates test_md.py
    with individual pytest test functions for each example.
    For markdown rendering, input and expected are identical.
    """
    spec_file = Path(__file__).parent.parent / "spec.txt"
    output_file = Path(__file__).parent / "test_md.py"

    print(f"Parsing examples from {spec_file}...")
    examples = parse_spec_examples(spec_file)
    print(f"Found {len(examples)} examples")

    print(f"Generating markdown tests to {output_file}...")
    generate_test_file(examples, output_file)
    print("Done!")


if __name__ == "__main__":
    main()
