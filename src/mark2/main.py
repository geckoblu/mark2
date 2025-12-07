#!/usr/bin/env python3
"""Main entry point for mark2 - a Markdown file converter."""

import argparse
import os
import sys

from mark2 import argparsext
from mark2.renderer import HTMLRenderer


def configure_parser() -> argparse.ArgumentParser:
    """Configure and return the argument parser for the application.

    Returns:
        Configured ArgumentParser instance
    """
    output_choices = ["html", "odt", "epub", "pdf"]

    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to various output formats.",
    )

    parser.add_argument(
        "input_filename",
        metavar="INPUT_FILENAME",
        type=argparsext.FileType("r", extension="md"),
        help="input Markdown (.md) file to convert (use '-' for stdin)",
    )

    output_group = parser.add_mutually_exclusive_group()

    output_group.add_argument(
        "-f",
        "--format",
        choices=output_choices,
        help="output format (choices: %(choices)s) [default: %(default)s]",
        default="html",
    )

    output_group.add_argument(
        "-o",
        "--output-filename",
        metavar="OUTPUT_FILENAME",
        type=argparsext.FileType("w", extension=output_choices),
        help="output file name (use '-' for stdout) [default: input name with format extension]",
    )

    parser.add_argument("-q", "--quiet", action="store_true", help="suppress non-error messages")

    # parser.add_argument("-aj", action="store_true", help="Output JSON AST")

    return parser


def main() -> None:
    """Main entry point for the mark2 application."""
    parser = configure_parser()
    args = parser.parse_args()
    # sys.stderr.write(str(args) + "\n")

    # Read input data
    if args.input_filename == "-":
        data = sys.stdin.read()
    else:
        if not args.quiet:
            print(f"Reading from '{args.input_filename}'")
        with open(args.input_filename, "r", encoding="utf-8") as f:
            data = f.read()

    # Determine output filename
    if args.output_filename is None:
        if args.input_filename == "-":
            args.output_filename = "-"
        else:
            root, __ = os.path.splitext(args.input_filename)
            args.output_filename = f"{root}.{args.format}"
            if args.output_filename == args.input_filename:
                args.output_filename = f"{root}_new.{args.format}"
            if not args.quiet:
                print(f"Writing to   '{args.output_filename}'")
    else:
        __, ext = os.path.splitext(args.output_filename)
        if ext.startswith("."):
            ext = ext[1:]
        args.format = ext
    if not args.quiet and args.output_filename != "-":
        print(f"Writing to   '{args.output_filename}'")

    if args.format == "html":

        # markdown_to_html(data, args.output_filename)
        renderer = HTMLRenderer()

    # elif args.format == "odt":
    #     from mark2.markdown2odt import markdown_to_odt

    #     markdown_to_odt(data, args.output_filename)
    # elif args.format == "epub":
    #     from mark2.markdown2epub import markdown_to_epub

    #     markdown_to_epub(data, args.output_filename)
    # elif args.format == "pdf":
    #     from mark2.markdown2pdf import markdown_to_pdf

    #     markdown_to_pdf(data, args.output_filename)
    else:
        raise ValueError(f"Unsupported format: {args.format}")

    renderer.render(data, args.output_filename)


if __name__ == "__main__":
    main()
