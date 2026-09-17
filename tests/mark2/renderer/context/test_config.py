"""Tests for ContextConfig.get()."""

import pytest
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin

from mark2.renderer.context.config import ContextConfig


def _parse_tokens(markdown_input: str):
    """Parse markdown_input and return the resulting token list."""
    md = MarkdownIt("commonmark")
    front_matter_plugin(md)
    return md.parse(markdown_input)


class TestContextConfigGet:
    """Test suite for ContextConfig.get()."""

    def test_defaults_to_a4_when_no_overrides(self):
        """No env/front matter overrides yields the A4 preset defaults."""
        tokens = _parse_tokens("# Title\n\ntext\n")

        cfg = ContextConfig.get({}, tokens)

        assert cfg.page_format == "A4"
        assert cfg.font_name == "libertinus"
        assert cfg.font_size == "12pt"

    def test_selects_a5_preset_from_env(self):
        """`pdf_page_format` in env selects the A5 preset."""
        tokens = _parse_tokens("# Title\n\ntext\n")

        cfg = ContextConfig.get({"pdf_page_format": "A5"}, tokens)

        assert cfg.page_format == "A5"
        assert cfg.font_name == "liberation"

    def test_front_matter_font_size_overrides_default(self):
        """`pdf-font-size` in front matter overrides the preset default."""
        tokens = _parse_tokens("---\npdf-font-size: 16pt\n---\n\n# Title\n\ntext\n")

        cfg = ContextConfig.get({}, tokens)

        assert cfg.font_size == "16pt"

    def test_front_matter_page_format_specific_font_size_overrides(self):
        """`pdf-<format>-font-size` in front matter overrides the generic key."""
        tokens = _parse_tokens(
            "---\npdf-font-size: 16pt\npdf-a4-font-size: 18pt\n---\n\n# Title\n\ntext\n"
        )

        cfg = ContextConfig.get({}, tokens)

        assert cfg.font_size == "18pt"

    def test_env_font_size_overrides_front_matter(self):
        """`pdf_font_size` in env has priority over front matter."""
        tokens = _parse_tokens("---\npdf-font-size: 16pt\n---\n\n# Title\n\ntext\n")

        cfg = ContextConfig.get({"pdf_font_size": "20pt"}, tokens)

        assert cfg.font_size == "20pt"

    def test_env_font_size_applies_without_front_matter(self):
        """`pdf_font_size` in env is applied even without front matter present."""
        tokens = _parse_tokens("# Title\n\ntext\n")

        cfg = ContextConfig.get({"pdf_font_size": "20pt"}, tokens)

        assert cfg.font_size == "20pt"

    def test_front_matter_font_name_overrides_default(self):
        """`pdf-font-name` in front matter overrides the preset default."""
        tokens = _parse_tokens("---\npdf-font-name: dejavu\n---\n\n# Title\n\ntext\n")

        cfg = ContextConfig.get({}, tokens)

        assert cfg.font_name == "dejavu"

    def test_front_matter_page_format_specific_font_name_overrides(self):
        """`pdf-<format>-font-name` in front matter overrides the generic key."""
        tokens = _parse_tokens(
            "---\npdf-font-name: dejavu\npdf-a4-font-name: pagella\n---\n\n# Title\n\ntext\n"
        )

        cfg = ContextConfig.get({}, tokens)

        assert cfg.font_name == "pagella"

    def test_env_font_name_overrides_front_matter(self):
        """`pdf_font_name` in env has priority over front matter."""
        tokens = _parse_tokens("---\npdf-font-name: dejavu\n---\n\n# Title\n\ntext\n")

        cfg = ContextConfig.get({"pdf_font_name": "pagella"}, tokens)

        assert cfg.font_name == "pagella"

    def test_env_font_name_applies_without_front_matter(self):
        """`pdf_font_name` in env is applied even without front matter present."""
        tokens = _parse_tokens("# Title\n\ntext\n")

        cfg = ContextConfig.get({"pdf_font_name": "pagella"}, tokens)

        assert cfg.font_name == "pagella"

    def test_header_at_recto_defaults_to_empty_list(self):
        """`header_at_recto` defaults to an empty list without front matter."""
        tokens = _parse_tokens("# Title\n\ntext\n")

        cfg = ContextConfig.get({}, tokens)

        assert cfg.header_at_recto == []

    def test_front_matter_header_at_recto_parses_comma_separated_list(self):
        """`pdf-header-at-recto` in front matter is parsed into a list of levels."""
        tokens = _parse_tokens("---\npdf-header-at-recto: h2,h3\n---\n\n# Title\n\ntext\n")

        cfg = ContextConfig.get({}, tokens)

        assert cfg.header_at_recto == ["h2", "h3"]

    def test_front_matter_page_format_specific_header_at_recto_overrides(self):
        """`pdf-<format>-header-at-recto` in front matter overrides the generic key."""
        tokens = _parse_tokens(
            "---\npdf-header-at-recto: h2,h3\npdf-a4-header-at-recto: h4\n---\n\n# Title\n\ntext\n"
        )

        cfg = ContextConfig.get({}, tokens)

        assert cfg.header_at_recto == ["h4"]

    def test_header_at_recto_rejects_invalid_level(self):
        """An unsupported heading level in `pdf-header-at-recto` raises ValueError."""
        tokens = _parse_tokens("---\npdf-header-at-recto: h2,h5\n---\n\n# Title\n\ntext\n")

        with pytest.raises(ValueError):
            ContextConfig.get({}, tokens)
