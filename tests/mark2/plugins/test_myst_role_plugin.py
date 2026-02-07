"""Comprehensive tests for the MyST role plugin module,
covering both the custom implementation and the original from mdit_py_plugins."""

# pylint: disable=redefined-outer-name  # pytest fixtures pattern

import pytest
from markdown_it import MarkdownIt

from mdit_py_plugins.myst_role import myst_role_plugin as original_myst_role_plugin

from mark2.plugins.myst_role_plugin import myst_role_plugin, myst_role
from mark2.renderer import RendererHTML


@pytest.fixture(params=[myst_role_plugin, original_myst_role_plugin], ids=["custom", "original"])
def plugin(request):
    """Parametrized fixture to test both plugin implementations."""
    return request.param


class TestMystRolePlugin:
    """Test suite for the MyST role plugin, covering both the custom implementation and
    the original from mdit_py_plugins."""

    def test_basic_role(self, plugin):
        """Test basic role with simple content."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {customrole}`custom text` example."
        result = md.render(markdown_input)

        assert '<span class="customrole">custom text</span>' in result

    def test_role_with_dashes(self, plugin):
        """Test role names with dashes."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {my-role}`content` example."
        result = md.render(markdown_input)

        assert '<span class="my-role">content</span>' in result

    def test_role_with_underscores(self, plugin):
        """Test role names with underscores."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {my_role}`content` example."
        result = md.render(markdown_input)

        assert '<span class="my_role">content</span>' in result

    def test_role_with_numbers(self, plugin):
        """Test role names with numbers."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {role123}`content` example."
        result = md.render(markdown_input)

        assert '<span class="role123">content</span>' in result

    def test_role_with_colon(self, plugin):
        """Test role names with colons (namespace-style)."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {namespace:role}`content` example."
        result = md.render(markdown_input)

        assert '<span class="namespace:role">content</span>' in result

    def test_role_with_plus(self, plugin):
        """Test role names with plus signs."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {role+name}`content` example."
        result = md.render(markdown_input)

        assert '<span class="role+name">content</span>' in result

    def test_multiple_roles_in_text(self, plugin):
        """Test multiple roles in the same text."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "First {role1}`content1` and second {role2}`content2` here."
        result = md.render(markdown_input)

        assert '<span class="role1">content1</span>' in result
        assert '<span class="role2">content2</span>' in result

    def test_role_with_newline(self, plugin):
        """Test role content with newlines (should be converted to spaces)."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {customrole}`multi\nline` example."
        result = md.render(markdown_input)

        assert '<span class="customrole">multi line</span>' in result

    def test_escaped_role(self, plugin):
        """Test escaped role (should not be parsed)."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = r"This is an \{customrole}`content` example."
        result = md.render(markdown_input)

        # Escaped role should appear as literal text
        assert '<span class="customrole">' not in result
        assert "{customrole}" in result

    def test_invalid_role_no_backticks(self, plugin):
        """Test that roles without backticks (non-empty) are not parsed."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is {not-a-role}text here."
        result = md.render(markdown_input)

        # Should not be parsed as a role
        assert '<span class="customrole">' not in result
        assert "{not-a-role}" in result

    def test_role_with_empty_content(self, plugin):
        """Test role with empty content is not allowed."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {customrole}`` example."
        result = md.render(markdown_input)

        # Empty content should not be parsed as a role
        assert '<span class="customrole">' not in result
        assert "{customrole}``" in result

    def test_role_without_closing_backticks(self, plugin):
        """Test that role without closing backticks is not parsed."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {customrole}`content without closing"
        result = md.render(markdown_input)

        # Should not be parsed as a role
        assert '<span class="customrole">' not in result
        assert "{customrole}`content without closing" in result

    def test_role_in_paragraph(self, plugin):
        """Test role in a paragraph."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "Paragraph with {customrole}`inline content` here.\n\nAnother paragraph."
        result = md.render(markdown_input)

        assert '<span class="customrole">inline content</span>' in result
        assert result.count("<p>") == 2

    def test_role_at_start_of_line(self, plugin):
        """Test role at the start of a line."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "{customrole}`content` at the start."
        result = md.render(markdown_input)

        assert '<span class="customrole">content</span>' in result

    def test_role_at_end_of_line(self, plugin):
        """Test role at the end of a line."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "Content ends with {customrole}`text`"
        result = md.render(markdown_input)

        assert '<span class="customrole">text</span>' in result

    def test_role_with_special_characters(self, plugin):
        """Test role content with special characters."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {customrole}`content with & < > chars` example."
        result = md.render(markdown_input)

        # Special chars should be escaped by the renderer
        assert '<span class="customrole">content with &amp; &lt; &gt; chars</span>' in result

    def test_role_adjacent_to_punctuation(self, plugin):
        """Test role adjacent to punctuation."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "Here is a {customrole}`word`, and here's another."
        result = md.render(markdown_input)

        assert '<span class="customrole">word</span>,' in result

    def test_nested_backticks_mismatch(self, plugin):
        """Test that mismatched backtick counts don't parse."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        # Start with double backticks, end with single
        markdown_input = "This is {customrole}``content` text."
        result = md.render(markdown_input)

        # Should not be parsed as a complete role
        assert '<span class="customrole">' not in result

    def test_role_with_unicode(self, plugin):
        """Test role with unicode content."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {customrole}`héllo wörld 你好` example."
        result = md.render(markdown_input)

        assert '<span class="customrole">héllo wörld 你好</span>' in result

    def test_empty_role_name(self, plugin):
        """Test that empty role names are not parsed."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is {}`content` not valid."
        result = md.render(markdown_input)

        assert '<span class="customrole">' not in result

    def test_role_name_with_spaces_not_valid(self, plugin):
        """Test that role names with spaces are not parsed."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is {role name}`content` not valid."
        result = md.render(markdown_input)

        assert '<span class="customrole">' not in result

    def test_consecutive_roles(self, plugin):
        """Test consecutive roles without spaces."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "Text {role1}`one`{role2}`two` here."
        result = md.render(markdown_input)

        assert '<span class="role1">one</span>' in result
        assert '<span class="role2">two</span>' in result

    def test_role_with_long_content(self, plugin):
        """Test role with long content."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        long_content = "This is a very long piece of content " * 10
        markdown_input = f"Text {{customrole}}`{long_content}` here."
        result = md.render(markdown_input)

        assert f'<span class="customrole">{long_content}</span>' in result
