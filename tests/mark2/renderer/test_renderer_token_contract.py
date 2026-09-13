"""Tests that the main renderer pipeline handles its generated tokens."""

from pathlib import Path
import tempfile
import zipfile

import pytest
from markdown_it import MarkdownIt

from mark2.main import set_plugins
from mark2.renderer.context.renderer import ConTeXtRenderer
from mark2.renderer.epub.renderer import EPUBRenderer

PAGEBREAK_FIXTURE = Path(__file__).parents[2] / "assets" / "TEST-PAGEBREAK.md"
COMMENTS_FIXTURE = PAGEBREAK_FIXTURE.parent / "TEST-COMMENTS.md"
ASSET_DIR = PAGEBREAK_FIXTURE.parent


def _token_types(tokens):
    """Return block and nested inline token types from a token stream."""
    result = set()
    for token in tokens:
        result.add(token.type)
        if token.children:
            result.update(_token_types(token.children))
    return result


@pytest.mark.parametrize("renderer_cls, output_format", [(ConTeXtRenderer, "tex")])
def test_context_renderer_rules_cover_all_asset_tokens(renderer_cls, output_format):
    """Every token in the Markdown fixtures has a ConTeXt render rule."""
    parser = MarkdownIt("commonmark", renderer_cls=renderer_cls)
    set_plugins(parser, output_format=output_format)

    token_types = set()
    for asset in ASSET_DIR.glob("*.md"):
        token_types.update(_token_types(parser.parse(asset.read_text(encoding="utf-8"))))

    dynamic_containers = {token for token in token_types if token.startswith("container_")}
    registered_rules = set(parser.renderer.rules)
    missing = sorted(token_types - registered_rules - {"inline"} - dynamic_containers)

    assert not missing, f"Missing ConTeXt render rules: {missing}"


def test_epub_renderer_rules_cover_custom_asset_tokens():
    """Every custom token in the Markdown fixtures has an EPUB render rule."""
    parser = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
    set_plugins(parser, output_format="epub")

    token_types = set()
    for asset in ASSET_DIR.glob("*.md"):
        token_types.update(_token_types(parser.parse(asset.read_text(encoding="utf-8"))))

    custom_tokens = {
        token
        for token in token_types
        if token.startswith("myst_")
        or token in {"pagebreak", "front_matter"}
        or token.startswith("footnote_")
        or token in {"sup_open", "sup_close", "sub_open", "sub_close"}
    }
    missing = sorted(custom_tokens - set(parser.renderer.rules))

    assert not missing, f"Missing EPUB render rules: {missing}"


def test_context_renderer_handles_pagebreak_fixture_tokens():
    """The ConTeXt renderer must not reject tokens from the pagebreak fixture."""
    markdown = PAGEBREAK_FIXTURE.read_text(encoding="utf-8")
    parser = MarkdownIt("commonmark", renderer_cls=ConTeXtRenderer)
    set_plugins(parser, output_format="tex")

    with tempfile.NamedTemporaryFile(suffix=".tex") as output:
        parser.render(markdown, env={"output_filename": output.name})


def test_context_renderer_handles_myst_comment_fixture_tokens():
    """The ConTeXt renderer must handle MyST comment tokens for PDF output."""
    markdown = COMMENTS_FIXTURE.read_text(encoding="utf-8")
    parser = MarkdownIt("commonmark", renderer_cls=ConTeXtRenderer)
    set_plugins(parser, output_format="pdf")

    with tempfile.NamedTemporaryFile(suffix=".tex") as output:
        parser.render(markdown, env={"output_filename": output.name})


def test_epub_renderer_handles_pagebreak_fixture_tokens():
    """The EPUB renderer must not reject tokens from the pagebreak fixture."""
    markdown = PAGEBREAK_FIXTURE.read_text(encoding="utf-8")
    parser = MarkdownIt("commonmark", renderer_cls=EPUBRenderer)
    set_plugins(parser, output_format="epub")

    with tempfile.NamedTemporaryFile(suffix=".epub") as output:
        parser.render(markdown, env={"output_filename": output.name})
        with zipfile.ZipFile(output.name) as epub:
            assert "mimetype" in epub.namelist()
