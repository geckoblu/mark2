"""Comprehensive tests for the MyST role plugin,
covering both the original and custom implementations."""

from markdown_it import MarkdownIt

from mdit_py_plugins.myst_role import myst_role_plugin as original_myst_role_plugin

from mark2.plugins.myst_role_plugin import myst_role
from mark2.renderer import RendererHTML

from .test_myst_role_plugin import plugin  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name,comparison-with-callable  # pytest fixtures pattern


class TestMystRolePlugin:
    """Test suite for MyST role plugin, comparing original and custom implementations."""

    def test_role_with_emphasis(self, plugin):
        """Test role content with emphasis markup."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {customrole}`*emphasized* content` example."
        result = md.render(markdown_input)

        # Custom plugin parses markdown inside roles, original doesn't
        if plugin == original_myst_role_plugin:
            assert '<span class="customrole">*emphasized* content</span>' in result
        else:
            assert '<span class="customrole"><em>emphasized</em> content</span>' in result

    def test_role_with_multiple_backticks(self, plugin):
        """Test role with multiple backticks for content containing backticks."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {customrole}``content with `backtick` inside`` example."
        result = md.render(markdown_input)

        # Custom plugin parses markdown (backticks become code), original doesn't
        if plugin == original_myst_role_plugin:
            assert '<span class="customrole">content with `backtick` inside</span>' in result
        else:
            assert (
                '<span class="customrole">content with <code>backtick</code> inside</span>'
                in result
            )

    def test_role_with_triple_backticks(self, plugin):
        """Test role with triple backticks."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {customrole}```content with ``double`` inside``` example."
        result = md.render(markdown_input)

        # Custom plugin parses markdown (double backticks become code), original doesn't
        if plugin == original_myst_role_plugin:
            assert '<span class="customrole">content with ``double`` inside</span>' in result
        else:
            assert (
                '<span class="customrole">content with <code>double</code> inside</span>' in result
            )

    def test_role_with_markdown(self, plugin):
        """Test role with markdown content."""
        md = MarkdownIt(renderer_cls=RendererHTML)
        md.use(plugin)
        md.add_render_rule("myst_role", myst_role)

        markdown_input = "This is a {customrole}`with *italic* content` example."
        result = md.render(markdown_input)

        # Custom plugin parses markdown inside roles, original doesn't
        if plugin == original_myst_role_plugin:
            assert '<span class="customrole">with *italic* content</span>' in result
        else:
            assert '<span class="customrole">with <em>italic</em> content</span>' in result
