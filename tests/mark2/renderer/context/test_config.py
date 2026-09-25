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

    def test_selects_a5_preset_from_front_matter(self):
        """`pdf-page-format` in front matter selects the A5 preset."""
        tokens = _parse_tokens("---\npdf-page-format: A5\n---\n\n# Title\n\ntext\n")

        cfg = ContextConfig.get({}, tokens)

        assert cfg.page_format == "A5"
        assert cfg.font_name == "liberation"

    def test_normalizes_page_format_case(self):
        """Page format values are normalized before selecting the preset."""
        tokens = _parse_tokens("---\npdf-page-format: a5\n---\n\n# Title\n\ntext\n")

        cfg = ContextConfig.get({}, tokens)

        assert cfg.page_format == "A5"
        assert cfg.font_name == "liberation"

    @pytest.mark.parametrize("page_format", ["Letter", "A3", ""])
    def test_rejects_unsupported_page_format(self, page_format):
        """Unsupported page formats raise ValueError instead of falling back to A4."""
        tokens = _parse_tokens(f"---\npdf-page-format: {page_format}\n---\n\n# Title\n\ntext\n")

        with pytest.raises(ValueError, match="Unsupported page format"):
            ContextConfig.get({}, tokens)

    def test_front_matter_page_format_specific_override_uses_selected_preset(self):
        """Page-format-specific front matter uses the format selected by front matter."""
        tokens = _parse_tokens(
            "---\n" "pdf-page-format: A5\n" "pdf-a5-font-size: 9pt\n" "---\n\n# Title\n\ntext\n"
        )

        cfg = ContextConfig.get({}, tokens)

        assert cfg.page_format == "A5"
        assert cfg.font_size == "9pt"

    def test_env_page_format_overrides_front_matter_page_format(self):
        """The environment page format has priority over front matter."""
        tokens = _parse_tokens("---\npdf-page-format: A5\n---\n\n# Title\n\ntext\n")

        cfg = ContextConfig.get({"pdf_page_format": "A4"}, tokens)

        assert cfg.page_format == "A4"
        assert cfg.font_name == "libertinus"

    def test_front_matter_overrides_all_configurable_values(self):
        """All ContextConfig values can be supplied through front matter."""
        tokens = _parse_tokens(
            "---\n"
            "pdf-page-format: A5\n"
            "pdf-language: en\n"
            "pdf-pagenumbering-alternative: doublesided\n"
            "pdf-topspace: 1mm\n"
            "pdf-header: 2mm\n"
            "pdf-headerdistance: 3mm\n"
            "pdf-bottomspace: 4mm\n"
            "pdf-footer: 5mm\n"
            "pdf-footerdistance: 6mm\n"
            "pdf-gutter: 2mm\n"
            "pdf-backspace: 30mm\n"
            "pdf-leftmargindistance: 7mm\n"
            "pdf-leftmargin: 8mm\n"
            "pdf-leftedgedistance: 9mm\n"
            "pdf-leftedge: 10mm\n"
            "pdf-rightmargindistance: 11mm\n"
            "pdf-rightmargin: 12mm\n"
            "pdf-rightedgedistance: 13mm\n"
            "pdf-rightedge: 14mm\n"
            "pdf-cutspace: 40mm\n"
            "pdf-font-name: dejavu\n"
            "pdf-font-size: 10pt\n"
            "pdf-indenting: small\n"
            "pdf-footnote-columns: 3\n"
            "pdf-footnote-bodyfont: 8pt\n"
            "pdf-footnote-distance: none\n"
            "pdf-define-verse-helpers: true\n"
            "---\n\n# Title\n\ntext\n"
        )

        cfg = ContextConfig.get({}, tokens)

        assert cfg.page_format == "A5"
        assert cfg.language == "en"
        assert cfg.pagenumbering_alternative == "doublesided"
        assert cfg.topspace == "1mm"
        assert cfg.header == "2mm"
        assert cfg.headerdistance == "3mm"
        assert cfg.bottomspace == "4mm"
        assert cfg.footer == "5mm"
        assert cfg.footerdistance == "6mm"
        assert cfg.gutter == "2mm"
        assert cfg.backspace == "32mm"
        assert cfg.leftmargindistance == "7mm"
        assert cfg.leftmargin == "8mm"
        assert cfg.leftedgedistance == "9mm"
        assert cfg.leftedge == "10mm"
        assert cfg.rightmargindistance == "11mm"
        assert cfg.rightmargin == "12mm"
        assert cfg.rightedgedistance == "13mm"
        assert cfg.rightedge == "14mm"
        assert cfg.cutspace == "40mm"
        assert cfg.font_name == "dejavu"
        assert cfg.font_size == "10pt"
        assert cfg.indenting == "small"
        assert cfg.footnote_columns == 3
        assert cfg.footnote_bodyfont == "8pt"
        assert cfg.footnote_distance is None
        assert cfg.define_verse_helpers is True

    def test_cutspace_is_sum_of_right_page_margins(self):
        """The default cutspace is calculated from the right page margins."""
        tokens = _parse_tokens("# Title\n\ntext\n")

        cfg = ContextConfig.get({}, tokens)

        assert cfg.cutspace == "20mm"

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

    def test_resolves_relative_preamble_from_source_directory(self, tmp_path):
        """A relative preamble path is resolved relative to the Markdown source."""
        source_file = tmp_path / "docs" / "source.md"
        tokens = _parse_tokens("---\npdf-preamble: preamble.tex\n---\n\n# Title\n")
        source_file.parent.mkdir()
        source_file.parent.joinpath("preamble.tex").touch()

        cfg = ContextConfig.get({"input_filename": str(source_file)}, tokens)

        assert cfg.preamble == str(source_file.parent / "preamble.tex")

    def test_resolves_relative_tex_files_from_source_directory(self, tmp_path):
        """The before/after TeX paths use the Markdown source directory as base."""
        source_file = tmp_path / "docs" / "source.md"
        tokens = _parse_tokens(
            "---\npdf-tex-before: before.tex\npdf-tex-after: after.tex\n---\n\n# Title\n"
        )
        source_file.parent.mkdir()
        source_file.parent.joinpath("before.tex").touch()
        source_file.parent.joinpath("after.tex").touch()

        cfg = ContextConfig.get({"input_filename": str(source_file)}, tokens)

        assert cfg.tex_before == str(source_file.parent / "before.tex")
        assert cfg.tex_after == str(source_file.parent / "after.tex")

    # def test_reports_missing_preamble_file(self, tmp_path):
    #     """A missing preamble file raises an error with its resolved path."""
    #     source_file = tmp_path / "docs" / "source.md"
    #     tokens = _parse_tokens("---\npdf-preamble: missing.tex\n---\n\n# Title\n")

    #     with pytest.raises(FileNotFoundError, match="Preamble file not found"):
    #         ContextConfig.get({"input_filename": str(source_file)}, tokens)

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
