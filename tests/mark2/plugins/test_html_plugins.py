import pytest
from markdown_it import MarkdownIt

from mdit_py_plugins.attrs import attrs_block_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.subscript import sub_plugin

from mark2.renderer import RendererHTML
from mark2.plugins import (
    container_plugin,
    headingsid_plugin,
    myst_role_plugin,
    pagebreak_plugin,
    sup_plugin,
)


def test_sub_plugin():

    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(sub_plugin)

    input_text = "This is a sub~2~ like H~2~O"
    expected = "<p>This is a sub<sub>2</sub> like H<sub>2</sub>O</p>\n"

    result = md.render(input_text)
    assert result == expected


def test_sup_plugin():
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(sup_plugin)

    input_text = "This is a sup^1^ like l^2^"
    expected = "<p>This is a sup<sup>1</sup> like l<sup>2</sup></p>\n"

    result = md.render(input_text)
    assert result == expected


def test_pagebreak_plugin():
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(pagebreak_plugin)

    input_text = "First Page\n\n---\n\nSecond Page"
    expected = '<p>First Page</p>\n<hr class="pagebreak" />\n<p>Second Page</p>\n'


def test_headingsid_plugin():
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(headingsid_plugin, min_level=1, max_level=6)

    input_text = "# Heading 1\n\n## Heading 2"
    expected = '<h1 id="toc_id_1">Heading 1</h1>\n<h2 id="toc_id_2">Heading 2</h2>\n'

    result = md.render(input_text)
    assert result == expected


def test_container_plugin():
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(container_plugin)

    input_text = "::: warning\nThis is a warning box.\n:::"
    expected = '<div class="warning">\n<p>This is a warning box.</p>\n</div>\n'

    result = md.render(input_text)
    assert result == expected


def test_myst_role_plugin():
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(myst_role_plugin)

    input_text = "This is a {role}`custom text` example."
    expected = '<p>This is a <span class="role">custom text</span> example.</p>\n'

    result = md.render(input_text)
    assert result == expected

    ###########################################################################
    # br role
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
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.use(attrs_block_plugin)

    input_text = "Paragraph with class {.my-class}.\n\nAnother paragraph."
    expected = '<p class="my-class">Paragraph with class.</p>\n<p>Another paragraph.</p>\n'

    result = md.render(input_text)
    assert result == expected


def test_front_matter_plugin():
    md = MarkdownIt(renderer_cls=RendererHTML)

    md.use(front_matter_plugin)

    input_text = "---\ntitle: Sample Document\nauthor: Test Author\n---\n\n# Heading\n\nContent."
    expected = "<h1>Heading</h1>\n<p>Content.</p>\n"

    env = {}
    result = md.render(input_text, env=env)
    assert result.strip() == expected.strip()

    expected_front_matter = {"title": "Sample Document", "author": "Test Author"}
    assert env.get("front_matter") == expected_front_matter
