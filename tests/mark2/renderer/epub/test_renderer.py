"""Tests for EPUBRenderer class.

This module contains tests for the EPUBRenderer class which renders
markdown to EPUB format with support for covers, metadata, TOC, and more.
"""

import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

import pytest
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

from mark2.main import set_plugins
from mark2.renderer.epub.renderer import EPUBRenderer
from mark2.plugins.headingsid_plugin import headingsid_plugin
from mark2.plugins.pagebreak_plugin import pagebreak_plugin


class TestEPUBRenderer:
    """Test suite for EPUBRenderer."""

    def test_basic_epub_creation(self):
        """Test basic EPUB creation with minimal content."""
        markdown_input = "# Hello World\n\nThis is a test."

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        headingsid_plugin(md)
        env = {"output_filename": "test.epub"}
        tokens = md.parse(markdown_input)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env["output_filename"] = temp_path
            md.renderer.render(tokens, md.options, env)

            # Verify EPUB was created
            assert Path(temp_path).exists()

            # Verify it's a valid ZIP
            with zipfile.ZipFile(temp_path, "r") as epub:
                # Check required EPUB files exist
                assert "mimetype" in epub.namelist()
                assert "META-INF/container.xml" in epub.namelist()
                assert "OEBPS/content.opf" in epub.namelist()
                assert "OEBPS/toc.ncx" in epub.namelist()
                assert "OEBPS/Styles/stylesheet.css" in epub.namelist()

                # Check mimetype content
                mimetype = epub.read("mimetype").decode("utf-8")
                assert mimetype == "application/epub+zip"

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_with_frontmatter(self):
        """Test EPUB creation with frontmatter metadata."""
        markdown_input = """---
title: My Book
author: John Doe
date: 2024-01-22
publisher: Test Publisher
language: en
subject: Fiction, Adventure
description: A test book
---

# Chapter 1

This is the first chapter.
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        front_matter_plugin(md)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input, env)
            md.renderer.render(tokens, md.options, env)

            # Verify metadata in OPF file
            with zipfile.ZipFile(temp_path, "r") as epub:
                opf_content = epub.read("OEBPS/content.opf").decode("utf-8")

                assert "<dc:title>My Book</dc:title>" in opf_content
                assert "John Doe" in opf_content
                assert "Test Publisher" in opf_content
                assert "<dc:language>en</dc:language>" in opf_content
                assert "<dc:subject>Fiction</dc:subject>" in opf_content
                assert "<dc:subject>Adventure</dc:subject>" in opf_content
                assert "A test book" in opf_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_toc_generation(self):
        """Test table of contents generation from headings."""
        markdown_input = """# Chapter 1

Some content.

## Section 1.1

More content.

## Section 1.2

Even more content.

# Chapter 2

Final content.
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path, "epub_split_at_header": "h1"}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify TOC in NCX file
            with zipfile.ZipFile(temp_path, "r") as epub:
                ncx_content = epub.read("OEBPS/toc.ncx").decode("utf-8")

                assert "Chapter 1" in ncx_content
                assert "Section 1.1" in ncx_content
                assert "Section 1.2" in ncx_content
                assert "Chapter 2" in ncx_content

                # Verify hierarchical structure
                assert "navPoint" in ncx_content
                assert "playOrder" in ncx_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_page_splitting(self):
        """Test that content is split into multiple pages at specified header level."""
        markdown_input = """# Chapter 1

Content 1.

## Section 1.1

Content 1.1.

# Chapter 2

Content 2.
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path, "epub_split_at_header": "h1"}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify multiple HTML pages were created
            with zipfile.ZipFile(temp_path, "r") as epub:
                html_files = [
                    name
                    for name in epub.namelist()
                    if name.startswith("OEBPS/") and name.endswith(".html")
                ]

                # Should have at least 2 pages (one per h1)
                assert len(html_files) >= 2

                # Verify content is in separate pages
                page1_content = epub.read(html_files[0]).decode("utf-8")
                assert "Chapter 1" in page1_content or "Chapter 2" in page1_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_with_footnotes(self):
        """Test EPUB creation with footnotes."""
        markdown_input = """# Main Text

This is a sentence with a footnote[^1].

Another sentence with a footnote[^2].

[^1]: This is the first footnote.
[^2]: This is the second footnote.
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        footnote_plugin(md)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify footnotes page exists
            with zipfile.ZipFile(temp_path, "r") as epub:
                html_files = [name for name in epub.namelist() if name.endswith(".html")]

                # Should have notes.html for footnotes
                assert any("notes.html" in name for name in html_files)

                # Check footnote content
                notes_content = epub.read("OEBPS/notes.html").decode("utf-8")
                assert "This is the first footnote" in notes_content
                assert "This is the second footnote" in notes_content
                assert 'class="footnote-backref"' in notes_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_pagebreak_splitting(self):
        """Test that pagebreaks create separate pages."""
        markdown_input = """# Section 1

Content before break.

---

# Section 2

Content after break.
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        pagebreak_plugin(md)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path, "epub_split_at_header": "h1"}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify multiple pages were created
            with zipfile.ZipFile(temp_path, "r") as epub:
                html_files = [
                    name
                    for name in epub.namelist()
                    if name.startswith("OEBPS/") and name.endswith(".html")
                ]

                # Should have at least 2 pages due to pagebreak
                assert len(html_files) >= 2

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_manifest_and_spine(self):
        """Test that manifest and spine are correctly generated."""
        markdown_input = """# Chapter 1

Content.

# Chapter 2

More content.
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path, "epub_split_at_header": "h1"}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify manifest and spine in OPF
            with zipfile.ZipFile(temp_path, "r") as epub:
                opf_content = epub.read("OEBPS/content.opf").decode("utf-8")

                # Check manifest entries
                assert '<item id="ncx"' in opf_content
                assert 'href="toc.ncx"' in opf_content
                assert '<item id="stylesheet.css"' in opf_content
                assert 'media-type="text/css"' in opf_content

                # Check spine
                assert "<spine" in opf_content
                assert "<itemref" in opf_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_default_language(self):
        """Test that default language is set when not in frontmatter."""
        markdown_input = "# Test"

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify default language (Italian) is set
            with zipfile.ZipFile(temp_path, "r") as epub:
                opf_content = epub.read("OEBPS/content.opf").decode("utf-8")
                assert "<dc:language>it</dc:language>" in opf_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_author_formatting(self):
        """Test author name formatting with file-as attribute."""
        markdown_input = """---
title: Test Book
author: John Smith
---

# Content
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        front_matter_plugin(md)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input, env)
            md.renderer.render(tokens, md.options, env)

            # Verify author formatting with file-as
            with zipfile.ZipFile(temp_path, "r") as epub:
                opf_content = epub.read("OEBPS/content.opf").decode("utf-8")
                assert 'opf:file-as="Smith, John"' in opf_content
                assert "John Smith" in opf_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_isbn_identifier(self):
        """Test ISBN identifier formatting in metadata."""
        markdown_input = """---
title: Test Book
id: ISBN<9788831550420>
---

# Content
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        front_matter_plugin(md)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input, env)
            md.renderer.render(tokens, md.options, env)

            # Verify ISBN identifier
            with zipfile.ZipFile(temp_path, "r") as epub:
                opf_content = epub.read("OEBPS/content.opf").decode("utf-8")
                assert 'opf:scheme="ISBN"' in opf_content
                assert "9788831550420" in opf_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_empty_toc(self):
        """Test EPUB with no headings generates valid empty TOC."""
        markdown_input = "Just some text without headings."

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify empty TOC
            with zipfile.ZipFile(temp_path, "r") as epub:
                ncx_content = epub.read("OEBPS/toc.ncx").decode("utf-8")

                # Should have valid NCX structure even without entries
                assert "navMap" in ncx_content
                assert "<?xml" in ncx_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_custom_stylesheet(self):
        """Test EPUB with custom stylesheet."""
        markdown_input = "# Test"
        custom_css = "body { background-color: beige; }"

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        headingsid_plugin(md)

        # Create temporary stylesheet file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False) as css_file:
            css_file.write(custom_css)
            css_path = css_file.name

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as epub_file:
            epub_path = epub_file.name

        try:
            env = {"output_filename": epub_path, "epub_stylesheet": css_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify custom stylesheet is included
            with zipfile.ZipFile(epub_path, "r") as epub:
                stylesheet_content = epub.read("OEBPS/Styles/stylesheet.css").decode("utf-8")
                assert "background-color: beige" in stylesheet_content

        finally:
            Path(epub_path).unlink(missing_ok=True)
            Path(css_path).unlink(missing_ok=True)

    def test_epub_nested_headings_toc(self):
        """Test hierarchical TOC with nested heading levels."""
        markdown_input = """# Chapter 1

## Section 1.1

### Subsection 1.1.1

## Section 1.2

# Chapter 2

## Section 2.1
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path, "epub_split_at_header": "h1"}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify hierarchical TOC structure
            with zipfile.ZipFile(temp_path, "r") as epub:
                ncx_content = epub.read("OEBPS/toc.ncx").decode("utf-8")

                # Should have nested navPoints
                assert ncx_content.count("<navPoint") >= 6  # All headings
                assert ncx_content.count("</navPoint>") >= 6
                assert "Chapter 1" in ncx_content
                assert "Section 1.1" in ncx_content
                assert "Subsection 1.1.1" in ncx_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_description_html_conversion(self):
        """Test that description in frontmatter is converted from markdown to HTML."""
        markdown_input = """---
title: Test
description: |
  This has **bold** and *italic* text.
---

# Content
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        front_matter_plugin(md)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input, env)
            md.renderer.render(tokens, md.options, env)

            # Verify description is converted to HTML
            with zipfile.ZipFile(temp_path, "r") as epub:
                opf_content = epub.read("OEBPS/content.opf").decode("utf-8")
                assert "<dc:description>" in opf_content
                # HTML should be escaped in XML
                assert "&lt;strong&gt;" in opf_content or "<strong>" in opf_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_multiple_subjects(self):
        """Test that multiple subjects are split and added correctly."""
        markdown_input = """---
title: Test
subject: Fiction, Adventure, Mystery
---

# Content
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        front_matter_plugin(md)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input, env)
            md.renderer.render(tokens, md.options, env)

            # Verify all subjects are included
            with zipfile.ZipFile(temp_path, "r") as epub:
                opf_content = epub.read("OEBPS/content.opf").decode("utf-8")
                assert "<dc:subject>Fiction</dc:subject>" in opf_content
                assert "<dc:subject>Adventure</dc:subject>" in opf_content
                assert "<dc:subject>Mystery</dc:subject>" in opf_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_container_xml(self):
        """Test that container.xml is correctly formatted."""
        markdown_input = "# Test"

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify container.xml structure
            with zipfile.ZipFile(temp_path, "r") as epub:
                container_content = epub.read("META-INF/container.xml").decode("utf-8")
                assert '<?xml version="1.0"' in container_content
                assert "urn:oasis:names:tc:opendocument:xmlns:container" in container_content
                assert 'full-path="OEBPS/content.opf"' in container_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_uuid_generation(self):
        """Test that each EPUB gets a unique UUID."""
        markdown_input = "# Test"

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path1 = f.name

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path2 = f.name

        try:
            # Create first EPUB
            env = {"output_filename": temp_path1}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Create second EPUB
            env = {"output_filename": temp_path2}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Extract UUIDs and verify they're different
            with zipfile.ZipFile(temp_path1, "r") as epub1:
                opf1 = epub1.read("OEBPS/content.opf").decode("utf-8")

            with zipfile.ZipFile(temp_path2, "r") as epub2:
                opf2 = epub2.read("OEBPS/content.opf").decode("utf-8")

            # UUIDs should be different
            assert opf1 != opf2

        finally:
            Path(temp_path1).unlink(missing_ok=True)
            Path(temp_path2).unlink(missing_ok=True)

    def test_epub_footnote_cross_references(self):
        """Test that footnote references link to correct pages."""
        markdown_input = """# Chapter 1

Text with footnote[^1].

# Chapter 2

More text[^2].

[^1]: First note.
[^2]: Second note.
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        footnote_plugin(md)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path, "epub_split_at_header": "h1"}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify footnote links are present
            with zipfile.ZipFile(temp_path, "r") as epub:
                notes_content = epub.read("OEBPS/notes.html").decode("utf-8")

                # Footnotes should have back-references with correct structure
                assert "href=" in notes_content
                assert 'class="footnote-backref"' in notes_content
                assert "fnref" in notes_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_epub_heading_ids_in_toc(self):
        """Test that TOC links include heading IDs."""
        markdown_input = """# Introduction

Content.

# Conclusion

More content.
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        headingsid_plugin(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path, "epub_split_at_header": "h1"}
            tokens = md.parse(markdown_input)
            md.renderer.render(tokens, md.options, env)

            # Verify TOC includes heading anchors
            with zipfile.ZipFile(temp_path, "r") as epub:
                ncx_content = epub.read("OEBPS/toc.ncx").decode("utf-8")

                # Should have content src with anchors
                assert ".html#" in ncx_content

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(not shutil.which("epubcheck"), reason="epubcheck not installed")
    def test_epub_validation_with_epubcheck(self):
        """Test that generated EPUB passes epubcheck validation.

        This test requires epubcheck to be installed and available in PATH.
        On Ubuntu/Debian: apt-get install epubcheck
        On macOS: brew install epubcheck
        Or download from: https://github.com/w3c/epubcheck/releases

        Note: This test uses a simple document without footnotes to avoid
        validation issues with the default footnote plugin rendering.
        """
        markdown_input = """---
title: Valid EPUB Test
author: Test Author
language: en
date: 2024-01-22
publisher: Test Publisher
subject: Testing, EPUB
---

# Chapter 1

This is the first chapter with some content.

## Section 1.1

More detailed content here with **bold** and *italic* text.

- Item 1
- Item 2
- Item 3

# Chapter 2

Second chapter content with a paragraph.

## Section 2.1

Final section with a [link](http://example.com) and an image reference.

## Section 2.2

Text with footnote[^1].
More text[^2].

[^1]: First note.
[^2]: Second note.
"""

        md = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
        set_plugins(md)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as f:
            temp_path = f.name

        try:
            env = {"output_filename": temp_path, "epub_split_at_header": "h2"}
            tokens = md.parse(markdown_input, env)
            md.renderer.render(tokens, md.options, env)

            # Verify EPUB was created
            assert Path(temp_path).exists()

            # Run epubcheck validation
            result = subprocess.run(
                ["epubcheck", temp_path],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            # Check that epubcheck passes (exit code 0)
            # Print output for debugging if test fails
            if result.returncode != 0:
                print("\n--- EPUBCHECK STDOUT ---")
                print(result.stdout)
                print("\n--- EPUBCHECK STDERR ---")
                print(result.stderr)

            assert result.returncode == 0, (
                f"EPUB validation failed with epubcheck.\n"
                f"STDOUT: {result.stdout}\n"
                f"STDERR: {result.stderr}"
            )

            # Verify that epubcheck reports success
            assert (
                "Check finished with no errors or warnings" in result.stdout
                or "No errors or warnings detected" in result.stdout
                or result.returncode == 0
            )

        finally:
            Path(temp_path).unlink(missing_ok=True)
