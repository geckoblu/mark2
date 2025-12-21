"""Command-line argument parsing for mark2.

This module defines the command-line interface for mark2, including argument
parsing, validation, and configuration of output formats and options.
"""

import argparse
import os


from markdown_it.utils import EnvType

from mark2 import argparsext


def configure_parser() -> argparse.ArgumentParser:
    """Configure and return the argument parser for the application.

    Returns:
        Configured ArgumentParser instance
    """
    output_choices = ["html", "epub", "pdf", "tex"]

    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to various output formats.",
    )

    parser.add_argument(
        "input_filename",
        metavar="INPUT_FILENAME",
        type=argparsext.FileType("r", extension="md"),
        help="input Markdown (.md) file to convert (use '-' for stdin)",
    )

    # output_group = parser.add_mutually_exclusive_group()

    parser.add_argument(
        "-f",
        "--format",
        choices=output_choices,
        help="output format (choices: %(choices)s) [default: %(default)s]",
        default="html",
    )

    parser.add_argument(
        "-o",
        "--output-filename",
        metavar="OUTPUT_FILENAME",
        type=argparsext.FileType("w", extension=output_choices),
        help="output file name (use '-' for stdout) [default: input name with format extension]",
    )

    # --- format-specific options ----------------

    # EPUB options -------------------------------
    epub_group = parser.add_argument_group("EPUB options")
    epub_group.add_argument(
        "--epub-cover",
        type=argparsext.FileType("r", extension=["jpg", "jpeg", "png"]),
        help="cover image for epub",
    )
    epub_group.add_argument(
        "--epub-stylesheet",
        type=argparsext.FileType("r", extension=["css"]),
        help="stylesheet for epub",
    )

    # html_group = parser.add_argument_group("HTML options")
    # html_group.add_argument("--html-css", help="CSS file to embed in HTML output")

    # pdf_group = parser.add_argument_group("PDF options")
    # pdf_group.add_argument("--pdf-engine", choices=["weasyprint", "wkhtmltopdf"])
    # pdf_group.add_argument("--pdf-margins", metavar="MM")

    # tex_group = parser.add_argument_group("ConTeXt options")
    # tex_group.add_argument("--tex-engine", choices=["xelatex", "lualatex"])

    # Hidden/development options
    dev_group = parser.add_mutually_exclusive_group()
    dev_group.add_argument(
        "--reference-html",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    dev_group.add_argument(
        "--reference-html-test",
        action="store_true",
        help=argparse.SUPPRESS,
    )

    parser.add_argument("-q", "--quiet", action="store_true", help="suppress non-error messages")
    parser.add_argument("-d", "--debug", action="store_true", help=argparse.SUPPRESS)

    return parser


def validate_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    """Validate command-line arguments for format-specific options.

    Args:
        args: Parsed command-line arguments
        parser: ArgumentParser instance for error reporting

    Raises:
        SystemExit: If format-specific options are used with incompatible formats
    """

    fmt = args.format

    if fmt != "epub" and args.epub_cover:
        parser.error("--epub-cover is only valid with --format epub")
    if fmt != "epub" and args.epub_stylesheet:
        parser.error("--epub-stylesheet is only valid with --format epub")

    # if fmt != "html" and args.html_css:
    #     parser.error("--html-css is only valid with --format html")

    # if fmt != "pdf" and (args.pdf_engine or args.pdf_margins):
    #     parser.error("--pdf-* options are only valid with --format pdf")

    # if fmt != "tex" and args.tex_engine:
    #     parser.error("--tex-engine is only valid with --format tex")


def parse_args() -> argparse.Namespace:
    """Parse and validate command-line arguments and determine output settings.

    Determines the output filename if not specified and validates format-specific options.

    Returns:
        Parsed and validated arguments with input_filename, output_filename, format, and quiet flags
    """

    parser = configure_parser()
    args = parser.parse_args()

    # Determine output filename
    if args.output_filename is None:
        if args.input_filename == "-":
            args.output_filename = "-"
        else:
            root, __ = os.path.splitext(args.input_filename)
            args.output_filename = f"{root}.{args.format}"
            if args.output_filename == args.input_filename:
                args.output_filename = f"{root}_new.{args.format}"
    else:
        if args.output_filename != "-":
            __, ext = os.path.splitext(args.output_filename)
            if ext.startswith("."):
                ext = ext[1:]
            args.format = ext

    validate_args(args, parser)

    return args


def get_env(args: argparse.Namespace) -> EnvType:
    """Construct the environment dictionary for the MarkdownIt parser.

    Args:
        args: Parsed command-line arguments
    Returns:
        Environment dictionary with format-specific settings
    """
    env: EnvType = {}

    env["input_filename"] = args.input_filename
    env["output_filename"] = args.output_filename
    env["output_format"] = args.format
    env["quiet"] = args.quiet
    env["debug"] = args.debug

    if args.format == "epub":
        env["epub_cover"] = args.epub_cover
        env["epub_stylesheet"] = args.epub_stylesheet

    # if args.format == "html":
    #     env["html_css"] = args.html_css

    # if args.format == "pdf":
    #     env["pdf_engine"] = args.pdf_engine
    #     env["pdf_margins"] = args.pdf_margins

    # if args.format == "tex":
    #     env["tex_engine"] = args.tex_engine

    return env
