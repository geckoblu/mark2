"""Comprehensive tests for the MyST role plugin module, specific for the custom implementation."""

from markdown_it import MarkdownIt


from mark2.plugins.myst_role_plugin import myst_role_plugin
from mark2.renderer import RendererHTML


class TestMystRolePlugin:
    """Test suite for the MyST role plugin, specific for the custom implementation."""

    def test_line_break_role(self):
        """Test line-break role (special empty role)."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(myst_role_plugin)

        markdown_input = "This is a {line-break}in the text."
        result = md.render(markdown_input)

        assert "<br/>" in result
        assert "line-break" not in result

    def test_br_alias_role(self):
        """Test br alias for line-break role."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(myst_role_plugin)

        markdown_input = "This is a {br}in the text."
        result = md.render(markdown_input)

        assert "<br/>" in result
        assert "{br}" not in result

    def test_br_role_in_heading(self):
        """Test br role inside a heading."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(myst_role_plugin)

        markdown_input = "# This is a {br}in the header."
        result = md.render(markdown_input)

        assert "<br/>" in result
        assert "<h1>" in result

    def test_multiple_line_breaks(self):
        """Test multiple line-break roles in text."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(myst_role_plugin)

        markdown_input = "Line 1{br}Line 2{line-break}Line 3"
        result = md.render(markdown_input)

        assert result.count("<br/>") == 2

    def test_line_break_with_backticks_not_parsed(self):
        """Test that line-break with backticks is not treated as special."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(myst_role_plugin)

        markdown_input = "This is a {line-break}`should not work` example."
        result = md.render(markdown_input)

        # Should render as a normal role, not as a line break
        assert '<span class="line-break">should not work</span>' in result
        assert result.count("<br/>") == 0
