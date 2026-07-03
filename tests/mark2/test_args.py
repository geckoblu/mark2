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

    def test_keep_tex_valid_with_pdf_format(self, monkeypatch, tmp_path):
        """`--keep-tex` is accepted when generating PDF output."""
        input_file = tmp_path / "input.md"
        input_file.write_text("# Title\n", encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["mark2", str(input_file), "--format", "pdf", "--keep-tex"],
        )

        args = parse_args()

        assert args.format == "pdf"
        assert args.keep_tex is True

        env = get_env(args)
        assert env["keep_tex"] is True

    def test_keep_tex_rejected_for_non_pdf_format(self, monkeypatch, tmp_path):
        """`--keep-tex` fails validation for non-PDF formats."""
        input_file = tmp_path / "input.md"
        input_file.write_text("# Title\n", encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["mark2", str(input_file), "--format", "html", "--keep-tex"],
        )

        with pytest.raises(SystemExit) as err:
            parse_args()

        assert err.value.code == 2

    def test_keep_tex_default_is_false(self, monkeypatch, tmp_path):
        """`--keep-tex` defaults to False for PDF generation."""
        input_file = tmp_path / "input.md"
        input_file.write_text("# Title\n", encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["mark2", str(input_file), "--format", "pdf"],
        )

        args = parse_args()

        assert args.keep_tex is False

        env = get_env(args)
        assert env["keep_tex"] is False
