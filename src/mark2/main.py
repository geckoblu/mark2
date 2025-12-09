#!/usr/bin/env python3
"""Main entry point for mark2 - a Markdown file converter."""

import argparse
import os
import sys

from markdown_it import MarkdownIt

from mark2 import argparsext
from mark2.renderer import ConTeXtRenderer, HTMLRenderer, PDFRenderer, Renderer


def configure_parser() -> argparse.ArgumentParser:
    """Configure and return the argument parser for the application.

    Returns:
        Configured ArgumentParser instance
    """
    output_choices = ["html", "odt", "epub", "pdf", "tex"]

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

    parser.add_argument("-q", "--quiet", action="store_true", help="suppress non-error messages")

    # parser.add_argument("-aj", action="store_true", help="Output JSON AST")

    return parser


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments and determine output settings.

    Returns:
        Parsed arguments with input_filename, output_filename, format, and quiet flags
    """

    parser = configure_parser()
    args = parser.parse_args()
    # sys.stderr.write(str(args) + "\n")

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

    if not args.quiet and args.output_filename != "-":
        print(f"Writing to   '{args.output_filename}'")

    return args


def read_data(input_filename: str, quiet: bool) -> str:
    """Read data from the input file or stdin.

    Args:
        input_filename: Input file name or '-' for stdin
        quiet: If True, suppress informational messages

    Returns:
        The content of the input file as a string
    """
    if input_filename == "-":
        data = sys.stdin.read()
    else:
        if not quiet:
            print(f"Reading from '{input_filename}'")
        with open(input_filename, "r", encoding="utf-8") as f:
            data = f.read()
    return data


def main() -> None:
    """Main entry point for the mark2 application."""

    args = parse_args()

    data = read_data(args.input_filename, args.quiet)

    md = MarkdownIt()
    tokens = md.parse(data)

    renderer: Renderer
    if args.format == "html":
        renderer = HTMLRenderer()
    # elif args.format == "odt":
    #     renderer = ODTRenderer()
    # elif args.format == "epub":
    #     renderer = EPUBRenderer()
    elif args.format == "pdf":
        renderer = PDFRenderer()
    elif args.format == "tex":
        renderer = ConTeXtRenderer()
    else:
        raise ValueError(f"Unsupported format: {args.format}")

    renderer.render(tokens, args.output_filename, md.options, env={})


if __name__ == "__main__":
    main()
