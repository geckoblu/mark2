"""Tests for HTMLRenderer class.

This module contains tests for the HTMLRenderer class which renders
markdown to complete HTML documents with headers and footers.
"""

import io
from contextlib import redirect_stdout
from pathlib import Path
import tempfile

from markdown_it import MarkdownIt
from mark2.renderer.html import HTMLRenderer


class TestHTMLRenderer:
    """Test suite for HTMLRenderer."""

    def test_basic_render_to_stdout(self):
        """Test basic rendering with output to stdout."""
        markdown_input = "# Hello World\n\nThis is a test."

        md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
        env = {"output_filename": "-"}
        tokens = md.parse(markdown_input)

        # Capture stdout
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            md.renderer.render(tokens, md.options, env)

        html_output = output_buffer.getvalue()

        # Verify structure
        assert "<!DOCTYPE html>" in html_output
        assert "<html>" in html_output
        assert "<head>" in html_output
        assert "</head>" in html_output
        assert "<body>" in html_output
        assert "</body>" in html_output
        assert "</html>" in html_output

        # Verify content
        assert "<h1>Hello World</h1>" in html_output
        assert "<p>This is a test.</p>" in html_output

    def test_title_from_frontmatter(self):
        """Test that title is extracted from frontmatter."""
        markdown_input = "# Hello World"

        md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
        env = {"output_filename": "-", "front_matter": {"title": "My Custom Title"}}
        tokens = md.parse(markdown_input)

        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            md.renderer.render(tokens, md.options, env)

        html_output = output_buffer.getvalue()

        # Verify custom title is used
        assert "<title>My Custom Title</title>" in html_output

    def test_title_from_filename(self):
        """Test that title is derived from filename when no frontmatter."""
        markdown_input = "# Hello World"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", prefix="mydocument_", delete=False
        ) as f:
            temp_path = f.name

        try:
            md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Read the file and verify content
            with open(temp_path, "r", encoding="utf-8") as f:
                html_output = f.read()

            # Verify title is derived from filename stem
            expected_title = Path(temp_path).stem
            assert f"<title>{expected_title}</title>" in html_output
        finally:
            # Clean up
            Path(temp_path).unlink(missing_ok=True)

    def test_title_default_dash(self):
        """Test default title when output is stdout."""
        markdown_input = "# Hello World"

        md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
        env = {"output_filename": "-"}
        tokens = md.parse(markdown_input)

        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            md.renderer.render(tokens, md.options, env)

        html_output = output_buffer.getvalue()

        # Verify default title is dash
        assert "<title>-</title>" in html_output

    def test_custom_stylesheet(self):
        """Test that custom stylesheet is included."""
        markdown_input = "# Hello World"
        custom_css = "body { background-color: red; }"

        md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
        env = {"output_filename": "-", "html_stylesheet": custom_css}
        tokens = md.parse(markdown_input)

        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            md.renderer.render(tokens, md.options, env)

        html_output = output_buffer.getvalue()

        # Verify custom stylesheet is included
        assert custom_css in html_output
        assert "<style>" in html_output
        assert "</style>" in html_output

    def test_default_stylesheet_included(self):
        """Test that default stylesheet is included when no custom stylesheet."""
        markdown_input = "# Hello World"

        md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
        env = {"output_filename": "-"}
        tokens = md.parse(markdown_input)

        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            md.renderer.render(tokens, md.options, env)

        html_output = output_buffer.getvalue()

        # Verify default stylesheet is included
        assert "page-break-before: always" in html_output
        assert "text-align: justify" in html_output

    def test_nbsp_replacement(self):
        """Test that non-breaking spaces are replaced with HTML entities."""
        # Create markdown that will result in nbsp in HTML
        markdown_input = "Test\xa0content"

        md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
        env = {"output_filename": "-"}
        tokens = md.parse(markdown_input)

        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            md.renderer.render(tokens, md.options, env)

        html_output = output_buffer.getvalue()

        # Verify nbsp is replaced with HTML entity
        assert "&#160;" in html_output
        assert "\xa0" not in html_output

    def test_render_to_file(self):
        """Test rendering to an actual file."""
        markdown_input = "# Test Document\n\nThis is a test."

        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            temp_path = f.name

        try:
            md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
            env = {"output_filename": temp_path, "front_matter": {"title": "Test Document"}}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Read the file and verify content
            with open(temp_path, "r", encoding="utf-8") as f:
                html_output = f.read()

            assert "<!DOCTYPE html>" in html_output
            assert "<title>Test Document</title>" in html_output
            assert "<h1>Test Document</h1>" in html_output
            assert "<p>This is a test.</p>" in html_output
        finally:
            # Clean up
            Path(temp_path).unlink(missing_ok=True)

    def test_complete_document_structure(self):
        """Test that the complete HTML document structure is correct."""
        markdown_input = "# Title\n\nParagraph."

        md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
        env = {"output_filename": "-", "front_matter": {"title": "Doc Title"}}
        tokens = md.parse(markdown_input)

        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            md.renderer.render(tokens, md.options, env)

        html_output = output_buffer.getvalue()

        # Check document structure order
        doctype_pos = html_output.find("<!DOCTYPE html>")
        html_open_pos = html_output.find("<html>")
        head_open_pos = html_output.find("<head>")
        title_pos = html_output.find("<title>")
        style_pos = html_output.find("<style>")
        head_close_pos = html_output.find("</head>")
        body_open_pos = html_output.find("<body>")
        h1_pos = html_output.find("<h1>")
        body_close_pos = html_output.find("</body>")
        html_close_pos = html_output.find("</html>")

        # Verify proper nesting
        assert doctype_pos < html_open_pos
        assert html_open_pos < head_open_pos
        assert head_open_pos < title_pos
        assert title_pos < style_pos
        assert style_pos < head_close_pos
        assert head_close_pos < body_open_pos
        assert body_open_pos < h1_pos
        assert h1_pos < body_close_pos
        assert body_close_pos < html_close_pos

    def test_empty_frontmatter(self):
        """Test rendering with empty frontmatter."""
        markdown_input = "# Hello"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            temp_path = f.name

        try:
            md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
            env = {"output_filename": temp_path, "front_matter": {}}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Read the file and verify content
            with open(temp_path, "r", encoding="utf-8") as f:
                html_output = f.read()

            # Should use filename stem as title
            expected_title = Path(temp_path).stem
            assert f"<title>{expected_title}</title>" in html_output
        finally:
            # Clean up
            Path(temp_path).unlink(missing_ok=True)

    def test_multiple_paragraphs(self):
        """Test rendering multiple paragraphs."""
        markdown_input = "Paragraph 1\n\nParagraph 2\n\nParagraph 3"

        md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
        env = {"output_filename": "-"}
        tokens = md.parse(markdown_input)

        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            md.renderer.render(tokens, md.options, env)

        html_output = output_buffer.getvalue()

        # Verify all paragraphs are present
        assert html_output.count("<p>") == 3
        assert "<p>Paragraph 1</p>" in html_output
        assert "<p>Paragraph 2</p>" in html_output
        assert "<p>Paragraph 3</p>" in html_output

    def test_complex_markdown(self):
        """Test rendering complex markdown with various elements."""
        markdown_input = """# Main Title

## Subtitle

This is a paragraph with **bold** and *italic* text.

- Item 1
- Item 2
- Item 3

> A blockquote

```python
def hello():
    print("Hello, World!")
```
"""

        md = MarkdownIt("commonmark", renderer_cls=HTMLRenderer)
        env = {"output_filename": "-", "front_matter": {"title": "Complex Document"}}
        tokens = md.parse(markdown_input)

        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            md.renderer.render(tokens, md.options, env)

        html_output = output_buffer.getvalue()

        # Verify various elements are rendered
        assert "<h1>Main Title</h1>" in html_output
        assert "<h2>Subtitle</h2>" in html_output
        assert "<strong>bold</strong>" in html_output
        assert "<em>italic</em>" in html_output
        assert "<ul>" in html_output
        assert "<li>Item 1</li>" in html_output
        assert "<blockquote>" in html_output
        assert "<pre><code" in html_output
        assert "def hello():" in html_output
