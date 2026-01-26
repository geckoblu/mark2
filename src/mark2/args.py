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
    output_choices = ["html", "epub", "pdf", "tex"]  # disabled "md" for now

    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to various output formats.",
    )

    parser.add_argument(
        "input_filename",
        metavar="INPUT_FILENAME",
        type=argparsext.FileType("r", extension="md"),
        help="input Markdown (.md) file to convert (use '-' for stdin)",
    )

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
        type=argparsext.FileOrDirType("w", extension=output_choices),
        help="output file name (use '-' for stdout) [default: input name with format extension]",
    )

    # --- format-specific options ----------------

    # EPUB options -------------------------------
    epub_group = parser.add_argument_group("EPUB options")
    epub_cover_group = epub_group.add_mutually_exclusive_group()
    epub_cover_group.add_argument(
        "--epub-cover",
        type=argparsext.FileType("r", extension=["jpg", "jpeg", "png"]),
        help="cover image for epub",
    )
    epub_cover_group.add_argument(
        "--epub-generatecover",
        action="store_true",
        help="generate cover for epub",
    )
    epub_group.add_argument(
        "--epub-stylesheet",
        type=argparsext.FileType("r", extension=["css"]),
        help="stylesheet for epub",
    )
    epub_group.add_argument(
        "--epub-split-at-header",
        choices=["h1", "h2", "h3", "h4", "h5", "h6"],
        default="h2",
        help="header level at which to split content into separate pages [default: %(default)s]",
    )

    # MARKDOWN options ---------------------------
    # markdown_group = parser.add_argument_group("MARKDOWN options")
    # markdown_group.add_argument(
    #     "--md-word-wrap",
    #     choices=["no", "keep", "semantic"],
    #     help="word wrap level for markdown output [default: no]",
    # )

    # Hidden/development options
    parser.add_argument(
        "--reference",
        action="store_true",
        help=argparse.SUPPRESS,
    )

    parser.add_argument("-q", "--quiet", action="store_true", help="suppress non-error messages")
    parser.add_argument("-d", "--debug", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument(
        "--link-check",
        action="store_true",
        help="extract and check all links in the document",
    )

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
    if fmt != "epub" and args.epub_generatecover:
        parser.error("--epub-generatecover is only valid with --format epub")
    if fmt != "epub" and args.epub_stylesheet:
        parser.error("--epub-stylesheet is only valid with --format epub")
    if fmt != "epub" and args.epub_split_at_header != "h2":
        parser.error("--epub-split-at-header is only valid with --format epub")

    # if fmt != "md" and args.md_word_wrap:
    #     parser.error("--md-word-wrap is only valid with --format md")


def parse_args() -> argparse.Namespace:
    """Parse and validate command-line arguments and determine output settings.

    Determines the output filename if not specified and validates format-specific options.

    Returns:
        Parsed and validated arguments with input_filename, output_filename, format, and quiet flags
    """

    parser = configure_parser()
    args = parser.parse_args()

    if args.reference or args.link_check:
        args.output_filename = "-"

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
            if ext == "":
                if args.format is None:
                    parser.error(
                        "output filename must have an extension"
                        + " (or provide the format with --format)"
                    )
                else:
                    basename, __ = os.path.splitext(os.path.basename(args.input_filename))
                    args.output_filename = os.path.join(
                        args.output_filename, f"{basename}.{args.format}"
                    )
                    if args.output_filename == args.input_filename:
                        root, ext = os.path.splitext(args.output_filename)
                        args.output_filename = f"{root}_new.{ext}"
            else:
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
        env["epub_generatecover"] = args.epub_generatecover
        env["epub_stylesheet"] = args.epub_stylesheet
        env["epub_split_at_header"] = args.epub_split_at_header

    if args.format == "md":
        if args.md_word_wrap is None:
            args.md_word_wrap = "no"
        env["md_word_wrap"] = args.md_word_wrap

    return env
