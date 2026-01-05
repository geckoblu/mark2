"""Tests for the container plugin module."""

import pytest
from markdown_it import MarkdownIt

from mark2.plugins.container_plugin import container_plugin


class TestContainerPlugin:
    """Test suite for the container plugin."""

    def test_basic_warning_container(self):
        """Test basic container with 'warning' class name."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: warning
This is a warning message with *markdown* support.
:::
"""

        result = md.render(markdown_input)

        assert '<div class="warning">' in result
        assert "<p>This is a warning message with <em>markdown</em> support.</p>" in result
        assert "</div>" in result

    def test_multiple_container_types(self):
        """Test multiple different container types in the same document."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: warning
Warning content
:::

::: note
Note content
:::

::: info
Info content
:::

::: danger
Danger content
:::
"""

        result = md.render(markdown_input)

        assert '<div class="warning">' in result
        assert '<div class="note">' in result
        assert '<div class="info">' in result
        assert '<div class="danger">' in result

    def test_nested_containers(self):
        """Test nested containers work correctly."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """:::: outer
This is the outer container.

::: inner
This is the inner container.
:::

Back to outer.
::::
"""

        result = md.render(markdown_input)

        assert '<div class="outer">' in result
        assert '<div class="inner">' in result
        # Check proper nesting - inner should come after outer opening
        outer_pos = result.find('<div class="outer">')
        inner_pos = result.find('<div class="inner">')
        assert outer_pos < inner_pos

    def test_container_with_custom_class_name(self):
        """Test container with custom class names."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: my-custom-class
Custom content
:::
"""

        result = md.render(markdown_input)

        assert '<div class="my-custom-class">' in result
        assert "<p>Custom content</p>" in result

    def test_container_with_dashes_in_class_name(self):
        """Test container with dashes in class name."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: box-with-dashes
Content with dashed class
:::
"""

        result = md.render(markdown_input)

        assert '<div class="box-with-dashes">' in result

    def test_container_with_markdown_content(self):
        """Test that markdown inside containers is properly rendered."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: alert
This has **bold** and *italic* and `code`.
:::
"""

        result = md.render(markdown_input)

        assert "<strong>bold</strong>" in result
        assert "<em>italic</em>" in result
        assert "<code>code</code>" in result

    def test_container_with_list_content(self):
        """Test container with list content."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: box
- Item 1
- Item 2
- Item 3
:::
"""

        result = md.render(markdown_input)

        assert '<div class="box">' in result
        assert "<ul>" in result
        assert "<li>Item 1</li>" in result

    def test_container_with_code_block(self):
        """Test container with code block inside."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: example
```python
print("Hello")
```
:::
"""

        result = md.render(markdown_input)

        assert '<div class="example">' in result
        assert "<code" in result
        assert "print(&quot;Hello&quot;)" in result or 'print("Hello")' in result

    def test_container_minimum_markers(self):
        """Test that minimum 3 markers are required."""
        md = MarkdownIt()
        md.use(container_plugin)

        # Only 2 markers - should not be recognized as container
        markdown_input = """:: warning
This should not be a container.
::
"""

        result = md.render(markdown_input)

        # Should be rendered as regular paragraph, not as container
        assert '<div class="warning">' not in result

    def test_container_with_extra_markers(self):
        """Test containers with more than 3 markers."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::::: warning
Content with 5 markers.
:::::
"""

        result = md.render(markdown_input)

        assert '<div class="warning">' in result
        assert "<p>Content with 5 markers.</p>" in result

    def test_container_closing_markers_length(self):
        """Test that closing markers must be at least as long as opening."""
        md = MarkdownIt()
        md.use(container_plugin)

        # Opening with 4 markers, closing with 3 - should not close
        markdown_input = """:::: warning
Content
:::
Still inside?
::::
"""

        result = md.render(markdown_input)

        # The container should close at the 4-marker close, not the 3-marker one
        assert '<div class="warning">' in result

    def test_empty_container(self):
        """Test container with no content."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: empty
:::
"""

        result = md.render(markdown_input)

        assert '<div class="empty">' in result
        assert "</div>" in result

    def test_container_with_class_and_extra_params(self):
        """Test container where params have additional text after class name."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: warning This is extra text
Content
:::
"""

        result = md.render(markdown_input)

        # Should extract only 'warning' as the class name
        assert '<div class="warning">' in result

    def test_multiple_paragraphs_in_container(self):
        """Test container with multiple paragraphs."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: note
First paragraph.

Second paragraph.

Third paragraph.
:::
"""

        result = md.render(markdown_input)

        assert '<div class="note">' in result
        assert result.count("<p>") >= 3  # At least 3 paragraphs

    def test_container_not_matched_by_regular_code_fence(self):
        """Test that regular code fences don't interfere with containers."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: info
Regular content

```
code block
```

More content
:::
"""

        result = md.render(markdown_input)

        assert '<div class="info">' in result
        assert "<code>code block" in result

    def test_container_class_name_case_preservation(self):
        """Test that class names preserve case."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: MyCustomClass
Content
:::
"""

        result = md.render(markdown_input)

        assert '<div class="MyCustomClass">' in result

    def test_container_with_numeric_class_name(self):
        """Test container with numeric characters in class name."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: section2
Content
:::
"""

        result = md.render(markdown_input)

        assert '<div class="section2">' in result

    def test_container_with_underscores(self):
        """Test container with underscores in class name."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: my_custom_class
Content
:::
"""

        result = md.render(markdown_input)

        assert '<div class="my_custom_class">' in result

    def test_no_container_without_class_name(self):
        """Test that container without class name is not recognized."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """:::
Content
:::
"""

        result = md.render(markdown_input)

        # Should not create a container div without a class name
        assert result.count("<div") == 0 or '<div class="">' not in result

    @pytest.mark.parametrize(
        "class_name",
        [
            "warning",
            "note",
            "info",
            "danger",
            "tip",
            "alert",
            "callout",
            "aside",
            "sidebar",
            "box",
        ],
    )
    def test_various_common_class_names(self, class_name):
        """Test that various common class names work correctly."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = f"""::: {class_name}
Content
:::
"""

        result = md.render(markdown_input)

        assert f'<div class="{class_name}">' in result

    def test_deeply_nested_containers(self):
        """Test deeply nested containers."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """:::::: level1
::::: level2
:::: level3
::: level4
Content at level 4
:::
::::
:::::
::::::
"""

        result = md.render(markdown_input)

        assert '<div class="level1">' in result
        assert '<div class="level2">' in result
        assert '<div class="level3">' in result
        assert '<div class="level4">' in result

    def test_container_with_heading(self):
        """Test container with heading inside."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: section
## Heading Inside Container

Content below heading.
:::
"""

        result = md.render(markdown_input)

        assert '<div class="section">' in result
        assert "<h2>Heading Inside Container</h2>" in result

    def test_container_unclosed_auto_closes(self):
        """Test that unclosed containers auto-close at end of document."""
        md = MarkdownIt()
        md.use(container_plugin)

        markdown_input = """::: unclosed
This container is never explicitly closed.
"""

        result = md.render(markdown_input)

        # Should still create opening and closing divs
        assert '<div class="unclosed">' in result
        assert "</div>" in result
