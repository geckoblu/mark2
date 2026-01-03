"""Tests for the Markdown renderer module."""

from mark2.renderer.md import MDRenderer

from .util_for_test import render_str_output


class TestMDRenderer:
    """Test suite for Markdown renderer."""

    def test_bullet_list(self):
        """Test rendering of bullet lists."""

        markdown_input = """- Item 1
- Item 2
  - Subitem 2.1
  - Subitem 2.2
- Item 3

"""

        md_output = render_str_output(MDRenderer, markdown_input)

        assert md_output == markdown_input
