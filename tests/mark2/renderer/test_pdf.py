"""Tests for PDFRenderer class.

This module contains tests for the PDFRenderer class which renders
markdown to PDF documents by generating ConTeXt and compiling to PDF.
"""

import shutil
import tempfile
from pathlib import Path
from unittest import mock

import pytest
from markdown_it import MarkdownIt

from mark2.renderer.pdf import PDFRenderer


class TestPDFRenderer:
    """Test suite for PDFRenderer."""

    def test_output_attribute(self):
        """Test that PDFRenderer has correct output format."""
        renderer = PDFRenderer()
        assert renderer.__output__ == "pdf"

    def test_keep_tex_writes_tex_file(self, tmp_path, monkeypatch):
        """Test that keep_tex preserves the intermediate .tex output."""
        renderer = PDFRenderer()
        tokens = []
        options = {}
        output_pdf = tmp_path / "output.pdf"

        def fake_context_render(self, _tokens, _options, env):
            Path(env["output_filename"]).write_text("\\starttext\\stoptext", encoding="utf-8")

        def fake_subprocess_run(_cmd, cwd, capture_output, text, check):
            del capture_output, text, check
            temp_tex = Path(cwd) / "temp.tex"
            if temp_tex.exists():
                temp_tex.unlink()
            (Path(cwd) / "temp.pdf").write_bytes(b"%PDF-")
            return mock.Mock(returncode=0, stderr="")

        monkeypatch.setattr(
            "mark2.renderer.context.renderer.ConTeXtRenderer.render", fake_context_render
        )
        monkeypatch.setattr("subprocess.run", fake_subprocess_run)

        env = {"output_filename": str(output_pdf), "keep_tex": True}
        renderer.render(tokens, options, env)

        assert output_pdf.exists()
        assert output_pdf.with_suffix(".tex").exists()

    @pytest.mark.skipif(not shutil.which("context"), reason="context command not installed")
    def test_basic_pdf_creation(self):
        """Test basic PDF creation with minimal content."""
        markdown_input = "# Hello World\n\nThis is a test."

        md = MarkdownIt("commonmark", renderer_cls=PDFRenderer)
        env = {"output_filename": "test.pdf"}
        tokens = md.parse(markdown_input)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            env["output_filename"] = temp_path
            md.renderer.render(tokens, md.options, env)

            # Verify PDF was created
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

            # Verify it starts with PDF header
            with open(temp_path, "rb") as f:
                header = f.read(5)
                assert header == b"%PDF-"

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(not shutil.which("context"), reason="context command not installed")
    def test_pdf_with_headings(self):
        """Test PDF creation with various heading levels."""
        markdown_input = """# Main Title

## Subtitle

### Subsubsection

Content here.
"""

        md = MarkdownIt("commonmark", renderer_cls=PDFRenderer)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify PDF was created
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(not shutil.which("context"), reason="context command not installed")
    def test_pdf_with_lists(self):
        """Test PDF creation with bullet and ordered lists."""
        markdown_input = """# Lists Test

## Bullet List

- Item 1
- Item 2
- Item 3

## Ordered List

1. First item
2. Second item
3. Third item
"""

        md = MarkdownIt("commonmark", renderer_cls=PDFRenderer)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify PDF was created
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(not shutil.which("context"), reason="context command not installed")
    def test_pdf_with_emphasis(self):
        """Test PDF creation with bold and italic text."""
        markdown_input = """# Text Formatting

This is **bold text** and this is *italic text*.

You can also have ***bold and italic*** together.
"""

        md = MarkdownIt("commonmark", renderer_cls=PDFRenderer)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify PDF was created
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(not shutil.which("context"), reason="context command not installed")
    def test_pdf_with_links(self):
        """Test PDF creation with links."""
        markdown_input = """# Links

This is a [link to Google](https://www.google.com).

Another link: [GitHub](https://github.com)
"""

        md = MarkdownIt("commonmark", renderer_cls=PDFRenderer)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify PDF was created
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(not shutil.which("context"), reason="context command not installed")
    def test_pdf_with_code_blocks(self):
        """Test PDF creation with code blocks."""
        markdown_input = """# Code Example

Here is some Python code:

```python
def hello():
    print("Hello, World!")
```

And some inline `code` as well.
"""

        md = MarkdownIt("commonmark", renderer_cls=PDFRenderer)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify PDF was created
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(not shutil.which("context"), reason="context command not installed")
    def test_pdf_with_blockquotes(self):
        """Test PDF creation with blockquotes."""
        markdown_input = """# Quotes

> This is a blockquote.
> It can span multiple lines.

> Another quote here.
"""

        md = MarkdownIt("commonmark", renderer_cls=PDFRenderer)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify PDF was created
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(not shutil.which("context"), reason="context command not installed")
    def test_pdf_with_special_characters(self):
        """Test PDF creation with special ConTeXt characters."""
        markdown_input = """# Special Characters

Text with special characters: & % $ # _ { } ~ ^ \\

These should be properly escaped in the PDF.
"""

        md = MarkdownIt("commonmark", renderer_cls=PDFRenderer)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify PDF was created
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(not shutil.which("context"), reason="context command not installed")
    def test_pdf_complex_document(self):
        """Test PDF creation with a complex document."""
        markdown_input = """# Document Title

## Introduction

This is an introduction with **bold** and *italic* text.

## Main Content

Here is a list:

- First item
- Second item with [a link](https://example.com)
- Third item

### Subsection

Some code:

```python
def example():
    return "test"
```

### Another Subsection

1. Ordered item one
2. Ordered item two
3. Ordered item three

> A quote to finish.

## Conclusion

The end.
"""

        md = MarkdownIt("commonmark", renderer_cls=PDFRenderer)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify PDF was created
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(not shutil.which("context"), reason="context command not installed")
    def test_pdf_empty_content(self):
        """Test PDF creation with minimal content."""
        markdown_input = "Simple text."

        md = MarkdownIt("commonmark", renderer_cls=PDFRenderer)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify PDF was created
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(not shutil.which("context"), reason="context command not installed")
    def test_pdf_with_nested_lists(self):
        """Test PDF creation with nested lists."""
        markdown_input = """# Nested Lists

- Item 1
  - Subitem 1.1
  - Subitem 1.2
- Item 2
  - Subitem 2.1
    - Subsubitem 2.1.1
- Item 3
"""

        md = MarkdownIt("commonmark", renderer_cls=PDFRenderer)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify PDF was created
            assert Path(temp_path).exists()
            assert Path(temp_path).stat().st_size > 0

        finally:
            Path(temp_path).unlink(missing_ok=True)
