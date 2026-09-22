"""Tests for the ConTeXt header builder."""

from mark2.renderer.context.config import ContextConfig
from mark2.renderer.context.header import build_header


class TestHeaderAtRecto:
    """Test suite for the header_at_recto -> \\setuphead mapping."""

    def test_no_setuphead_when_header_at_recto_is_empty(self):
        """No `header_at_recto` levels means no extra `\\setuphead` is emitted."""
        cfg = ContextConfig.a4()

        header = build_header(cfg)

        assert "page=right" not in header

    def test_maps_each_level_to_the_matching_context_head(self):
        """Each configured level maps to its ConTeXt head, in a single \\setuphead line."""
        cfg = ContextConfig.a4()
        cfg.header_at_recto = ["h1", "h2", "h3", "h4"]

        header = build_header(cfg)

        assert (
            "\\setuphead[section,subsection,subsubsection,subsubsubsection][page=right]\n" in header
        )

    def test_ignores_missing_additional_preamble_file(self, tmp_path):
        """A missing additional preamble file does not prevent header generation."""
        cfg = ContextConfig.a4()
        cfg.preamble = str(tmp_path / "missing.tex")

        header = build_header(cfg)

        assert "% Additional preamble" not in header
