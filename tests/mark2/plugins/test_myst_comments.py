"""Tests for MyST line comments parsing."""

import pytest
from markdown_it import MarkdownIt

from mdit_py_plugins.myst_blocks import myst_block_plugin


class TestMystLineComments:
    """Test suite for MyST line comments."""

    def setup_method(self):
        """Set up markdown parser for each test."""
        self.md = MarkdownIt()
        self.md.use(myst_block_plugin)

    def test_simple_comment(self):
        """Test that a simple line comment is converted to HTML comment."""
        markdown_input = "% This is a comment\nRegular content"
        result = self.md.render(markdown_input)

        assert "<!-- This is a comment -->" in result
        assert "<p>Regular content</p>" in result

    def test_multiline_comments(self):
        """Test that multiple consecutive comment lines are combined."""
        markdown_input = """% This is a comment
% Multi-line comments
% can span multiple lines

Regular content here."""

        result = self.md.render(markdown_input)
        expected_comment = (
            "<!-- This is a comment\n" "Multi-line comments\n" "can span multiple lines -->"
        )
        assert expected_comment in result
        assert "Regular content here" in result

    def test_comment_with_special_chars(self):
        """Test comments with special characters."""
        markdown_input = "% TODO: Implement feature X\n% FIXME: Fix bug Y\nContent"
        result = self.md.render(markdown_input)
        assert "Content" in result

    def test_comment_preserves_following_content(self):
        """Test that comments don't interfere with following markdown."""
        markdown_input = """% This is a comment
# Heading
- List item
"""
        result = self.md.render(markdown_input)
        assert "<h1>" in result
        assert "<li>" in result

    def test_empty_comment_line(self):
        """Test that a lone % character is treated as a comment."""
        markdown_input = "%\nContent after empty comment"
        result = self.md.render(markdown_input)
        assert "Content after empty comment" in result

    def test_comment_in_middle_of_content(self):
        """Test comments between content blocks."""
        markdown_input = """First paragraph.

% Separator comment

Second paragraph."""
        result = self.md.render(markdown_input)
        assert "First paragraph" in result
        assert "Second paragraph" in result

    def test_leading_whitespace_in_comment(self):
        """Test that leading whitespace is handled in comments."""
        markdown_input = "%   Comment with leading spaces\nContent"
        result = self.md.render(markdown_input)
        assert "Content" in result

    def test_comment_blocks_are_separate(self):
        """Test that non-consecutive comment lines create separate blocks."""
        markdown_input = """% First comment block

Regular content.

% Second comment block

More content."""
        result = self.md.render(markdown_input)
        # Should create two separate comment blocks
        assert "Regular content" in result
        assert "More content" in result

    def test_comment_with_markdown_syntax(self):
        """Test that markdown syntax inside comments is ignored."""
        markdown_input = "% This has **bold** and *italic* syntax\nRegular content"
        result = self.md.render(markdown_input)
        # The markdown syntax inside comment should not be rendered
        assert "Regular content" in result
