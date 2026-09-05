"""Tests for command-line argument parsing."""

import pytest

from mark2.args import get_env, parse_args


class TestArgs:
    """Test suite for argument parser behavior."""

    def test_debug_tokens_default_is_false(self, monkeypatch, tmp_path):
        """`--debug-tokens` defaults to False."""
        input_file = tmp_path / "input.md"
        input_file.write_text("# Title\n", encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["mark2", str(input_file)],
        )

        args = parse_args()

        assert args.debug_tokens is False

        env = get_env(args)
        assert env["debug_tokens"] is False

    def test_debug_tokens_enabled(self, monkeypatch, tmp_path):
        """`--debug-tokens` is enabled when explicitly set."""
        input_file = tmp_path / "input.md"
        input_file.write_text("# Title\n", encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["mark2", str(input_file), "--debug-tokens"],
        )

        args = parse_args()

        assert args.debug_tokens is True

        env = get_env(args)
        assert env["debug_tokens"] is True

    def test_pdf_keep_tex_valid_with_pdf_format(self, monkeypatch, tmp_path):
        """`--pdf-keep-tex` is accepted when generating PDF output."""
        input_file = tmp_path / "input.md"
        input_file.write_text("# Title\n", encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["mark2", str(input_file), "--format", "pdf", "--pdf-keep-tex"],
        )

        args = parse_args()

        assert args.format == "pdf"
        assert args.pdf_keep_tex is True

        env = get_env(args)
        assert env["pdf_keep_tex"] is True

    def test_pdf_keep_tex_rejected_for_non_pdf_format(self, monkeypatch, tmp_path):
        """`--pdf-keep-tex` fails validation for non-PDF formats."""
        input_file = tmp_path / "input.md"
        input_file.write_text("# Title\n", encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["mark2", str(input_file), "--format", "html", "--pdf-keep-tex"],
        )

        with pytest.raises(SystemExit) as err:
            parse_args()

        assert err.value.code == 2

    def test_pdf_keep_tex_default_is_false(self, monkeypatch, tmp_path):
        """`--pdf-keep-tex` defaults to False for PDF generation."""
        input_file = tmp_path / "input.md"
        input_file.write_text("# Title\n", encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["mark2", str(input_file), "--format", "pdf"],
        )

        args = parse_args()

        assert args.pdf_keep_tex is False

        env = get_env(args)
        assert env["pdf_keep_tex"] is False

    def test_pdf_page_format_accepts_a5(self, monkeypatch, tmp_path):
        """`--pdf-page-format A5` is passed to PDF rendering."""
        input_file = tmp_path / "input.md"
        input_file.write_text("# Title\n", encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["mark2", str(input_file), "--format", "pdf", "--pdf-page-format", "A5"],
        )

        args = parse_args()

        assert args.pdf_page_format == "A5"
        assert get_env(args)["pdf_page_format"] == "A5"

    def test_pdf_page_format_defaults_to_a4(self, monkeypatch, tmp_path):
        """PDF page format defaults to A4."""
        input_file = tmp_path / "input.md"
        input_file.write_text("# Title\n", encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["mark2", str(input_file), "--format", "pdf"],
        )

        args = parse_args()

        assert args.pdf_page_format == "A4"
        assert get_env(args)["pdf_page_format"] == "A4"

    def test_pdf_page_format_rejected_for_non_pdf_format(self, monkeypatch, tmp_path):
        """`--pdf-page-format` fails validation for non-PDF formats."""
        input_file = tmp_path / "input.md"
        input_file.write_text("# Title\n", encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["mark2", str(input_file), "--format", "html", "--pdf-page-format", "A5"],
        )

        with pytest.raises(SystemExit) as err:
            parse_args()

        assert err.value.code == 2
