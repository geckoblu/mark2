"""Tests for HTML plugins in the Mark2 Markdown processor."""

import pytest
from markdown_it import MarkdownIt

from mdit_py_plugins.attrs import attrs_block_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.subscript import sub_plugin

from mark2.main import set_footnote_plugin
from mark2.renderer import RendererHTML
from mark2.plugins import (
    container_plugin,
    headingsid_plugin,
    myst_role_plugin,
    pagebreak_plugin,
    sup_plugin,
)


def test_sub_plugin():
    """Test subscript plugin rendering."""
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(sub_plugin)

    input_text = "This is a sub~2~ like H~2~O"
    expected = "<p>This is a sub<sub>2</sub> like H<sub>2</sub>O</p>\n"

    result = md.render(input_text)
    assert result == expected


def test_sup_plugin():
    """Test superscript plugin rendering."""
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(sup_plugin)

    input_text = "This is a sup^1^ like l^2^"
    expected = "<p>This is a sup<sup>1</sup> like l<sup>2</sup></p>\n"

    result = md.render(input_text)
    assert result == expected


def test_pagebreak_plugin():
    """Test page break plugin rendering."""
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(pagebreak_plugin)

    input_text = "First Page\n\n---\n\nSecond Page"
    expected = '<p>First Page</p>\n<hr class="pagebreak" />\n<p>Second Page</p>\n'

    result = md.render(input_text)
    assert result == expected


def test_headingsid_plugin():
    """Test headings ID plugin rendering."""
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(headingsid_plugin, min_level=1, max_level=6)

    input_text = "# Heading 1\n\n## Heading 2"
    expected = '<h1 id="toc_id_1">Heading 1</h1>\n<h2 id="toc_id_2">Heading 2</h2>\n'

    result = md.render(input_text)
    assert result == expected


def test_container_plugin():
    """Test container plugin rendering."""
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(container_plugin)

    input_text = "::: warning\nThis is a warning box.\n:::"
    expected = '<div class="warning">\n<p>This is a warning box.</p>\n</div>\n'

    result = md.render(input_text)
    assert result == expected


def test_myst_role_plugin():
    """Test myst role plugin rendering."""
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(myst_role_plugin)

    input_text = "This is a {role}`custom text` example."
    expected = '<p>This is a <span class="role">custom text</span> example.</p>\n'

    result = md.render(input_text)
    assert result == expected

    ###########################################################################
    # {br} role
    ###########################################################################
    input_text = "This is a {line-break}in the text."
    expected = "<p>This is a <br/>in the text.</p>\n"

    result = md.render(input_text)
    assert result == expected

    input_text = "This is a {br}in the text."
    expected = "<p>This is a <br/>in the text.</p>\n"

    result = md.render(input_text)
    assert result == expected

    input_text = "# This is a {br}in the header."
    expected = "<h1>This is a <br/>in the header.</h1>\n"

    result = md.render(input_text)
    assert result == expected


@pytest.mark.skip(reason="TODO: Temporarily disabled - needs implementation review")
def test_attrs_block_plugin():
    """Test attrs block plugin rendering."""
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(attrs_block_plugin)

    input_text = "Paragraph with class {.my-class}.\n\nAnother paragraph."
    expected = '<p class="my-class">Paragraph with class.</p>\n<p>Another paragraph.</p>\n'

    result = md.render(input_text)
    assert result == expected


def test_front_matter_plugin():
    """Test front matter plugin rendering."""
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(front_matter_plugin)

    input_text = "---\ntitle: Sample Document\nauthor: Test Author\n---\n\n# Heading\n\nContent."
    expected = "<h1>Heading</h1>\n<p>Content.</p>\n"

    env = {}
    result = md.render(input_text, env=env)
    assert result.strip() == expected.strip()

    expected_front_matter = {"title": "Sample Document", "author": "Test Author"}
    assert env.get("front_matter") == expected_front_matter


def test_front_matter_plugin_empty():
    """Test front matter plugin with empty front matter."""
    md = MarkdownIt(renderer_cls=RendererHTML)

    md.use(front_matter_plugin)

    input_text = "---\n---\n\n# Heading\n\nContent."
    expected = "<h1>Heading</h1>\n<p>Content.</p>\n"

    env = {}
    result = md.render(input_text, env=env)
    assert result.strip() == expected.strip()

    expected_front_matter = {}
    assert env.get("front_matter") == expected_front_matter


def test_footnote_plugin():
    """Test footnote plugin rendering."""
    md = MarkdownIt(renderer_cls=RendererHTML)
    set_footnote_plugin(md)

    input_text = "Here is a footnote reference.[^1]\n\n[^1]: This is the footnote."
    expected = (
        "<p>Here is a footnote reference."
        '<a href="#fn1" id="fnref1"><sup class="footnote-ref">1</sup></a>'
        "</p>\n"
        '<div class="footnotes">\n'
        '<div class="footnote">\n'
        "<p>\n"
        '<a href="#fnref1" id="fn1" class="footnote-backref">'
        '<sup class="footnote-backref">1</sup></a>&#160;This is the footnote.</p>\n'
        "</div>\n"
        "</div>\n"
    )

    result = md.render(input_text)
    assert result == expected


def test_footnote_plugin_multiple():
    """Test footnote plugin rendering with multiple footnotes."""
    md = MarkdownIt(renderer_cls=RendererHTML)
    set_footnote_plugin(md)

    input_text = (
        "First footnote reference.[^1] Second footnote reference.[^2]\n\n"
        "[^1]: This is the first footnote.\n"
        "[^2]: This is the second footnote."
    )
    expected = (
        "<p>First footnote reference."
        '<a href="#fn1" id="fnref1"><sup class="footnote-ref">1</sup></a> '
        "Second footnote reference."
        '<a href="#fn2" id="fnref2"><sup class="footnote-ref">2</sup></a>'
        "</p>\n"
        '<div class="footnotes">\n'
        '<div class="footnote">\n'
        "<p>\n"
        '<a href="#fnref1" id="fn1" class="footnote-backref">'
        '<sup class="footnote-backref">1</sup></a>&#160;This is the first footnote.</p>\n'
        "</div>\n"
        '<div class="footnote">\n'
        "<p>\n"
        '<a href="#fnref2" id="fn2" class="footnote-backref">'
        '<sup class="footnote-backref">2</sup></a>&#160;This is the second footnote.</p>\n'
        "</div>\n"
        "</div>\n"
    )

    result = md.render(input_text)
    assert result == expected


def test_footnote_plugin_inline():
    """Test footnote plugin rendering with inline footnotes."""
    md = MarkdownIt(renderer_cls=RendererHTML)
    set_footnote_plugin(md)

    input_text = "Here is an inline footnote.^[This is the inline footnote.]"
    expected = (
        "<p>Here is an inline footnote."
        '<a href="#fn1" id="fnref1"><sup class="footnote-ref">1</sup></a>'
        "</p>\n"
        '<div class="footnotes">\n'
        '<div class="footnote">\n'
        "<p>\n"
        '<a href="#fnref1" id="fn1" class="footnote-backref">'
        '<sup class="footnote-backref">1</sup></a>&#160;This is the inline footnote.</p>\n'
        "</div>\n"
        "</div>\n"
    )

    result = md.render(input_text)
    assert result == expected
