"""Tests for HTML rendering functionality.

This module contains tests for the HTML renderer, verifying that markdown
is correctly converted to HTML according to the CommonMark specification.
"""

import io
from contextlib import redirect_stdout

import pytest

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML

from mark2.renderer.html import HTMLRenderer


class TestHTMLRenderer:
    """Test suite for HTML renderer."""

    def test_tabs_in_indented_code_block(self):
        """Test that tabs are handled in indented code blocks.

        From CommonMark spec example (lines 355-360):
        Tabs in lines are not expanded to spaces. However, in contexts where
        spaces help to define block structure, tabs behave as if they were
        replaced by spaces with a tab stop of 4 characters.

        Note: The actual CommonMark implementation expands tabs to spaces for
        rendering purposes, but the leading tab is used to determine the code block.
        """

        # Input: tab followed by "foo", tab, "baz", two tabs, "bim"
        markdown_input = "\tfoo\tbaz\t\tbim"

        # Create markdown parser with HTML renderer
        md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)

        # Parse and render, capturing stdout
        env = {"output_filename": "-"}
        tokens = md.parse(markdown_input)

        # Capture stdout since render() writes to stdout when output is "-"
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            md.renderer.render(tokens, md.options, env)

        html_output = output_buffer.getvalue()

        # Verify it's a code block containing the text
        assert "<pre><code>" in html_output
        assert "foo" in html_output
        assert "baz" in html_output
        assert "bim" in html_output
        assert "</code></pre>" in html_output

    def test_tabs_in_indented_code_block_raw(self):
        """Test tab handling in indented code blocks using raw rendering.

        This test directly checks the token rendering without the HTML
        header/footer wrapper.
        """

        # Input: tab followed by "foo", tab, "baz", two tabs, "bim"
        markdown_input = "\tfoo\tbaz\t\tbim"

        # Create markdown parser with standard RendererHTML
        md = MarkdownIt("commonmark", renderer_cls=RendererHTML)

        # Parse and render
        tokens = md.parse(markdown_input)
        html_output = md.renderer.render(tokens, md.options, {})

        # Expected: tabs are preserved in the code block
        assert "foo\tbaz\t\tbim" in html_output
        assert "<pre><code>" in html_output
        assert "</code></pre>" in html_output

    @pytest.mark.parametrize(
        "markdown_input,expected_content",
        [
            # Tab creates indented code block
            ("\tfoo", "foo"),
            # Tab with internal tabs preserved
            ("\tfoo\tbar", "foo\tbar"),
            # Multiple tabs at start and internal tabs
            ("\t\tfoo\t\tbar", "\tfoo\t\tbar"),
        ],
    )
    def test_tab_handling_variations(self, markdown_input, expected_content):
        """Test various tab handling scenarios in code blocks.

        Args:
            markdown_input: The markdown text with tabs
            expected_content: The expected content in the code block
        """
        # Create markdown parser with standard RendererHTML
        md = MarkdownIt("commonmark", renderer_cls=RendererHTML)
        tokens = md.parse(markdown_input)
        html_output = md.renderer.render(tokens, md.options, {})

        # Verify the expected content appears in a code block
        assert expected_content in html_output
        assert "<pre><code>" in html_output
