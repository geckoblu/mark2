#!/usr/bin/env python3
"""Main entry point for mark2 - a Markdown file converter."""

import sys

from mdit_py_plugins.footnote import footnote_plugin

from markdown_it import MarkdownIt

from mark2.args import get_env, parse_args
from mark2.renderer import (
    ConTeXtRenderer,
    EPUBRenderer,
    HTMLRenderer,
    PDFRenderer,
    ReferenceHTMLRenderer,
)


def read_data(input_filename: str) -> str:
    """Read data from the input file or stdin.

    Args:
        input_filename: Input file name or '-' for stdin

    Returns:
        The content of the input file as a string
    """
    if input_filename == "-":
        data = sys.stdin.read()
    else:
        with open(input_filename, "r", encoding="utf-8") as f:
            data = f.read()
    return data


def set_plugins(md: MarkdownIt) -> None:
    """Set up plugins for the MarkdownIt parser based on command-line arguments.

    Args:
        md: MarkdownIt parser instance
    Returns:
        None
    """
    set_footnote_plugin(md)


def set_footnote_plugin(md: MarkdownIt) -> None:
    """Set up the Footnote plugin with custom render rules."""
    md.use(footnote_plugin, move_to_end=True)

    # Override Footnote plugin render rules with custom renderer methods if they exist
    footnote_rules = [
        "footnote_ref",
        "footnote_block_open",
        "footnote_block_close",
        "footnote_open",
        "footnote_close",
        "footnote_anchor",
        "footnote_caption",
        "footnote_anchor_name",
        "footnote_reference_open",
        "footnote_reference_close",
    ]
    for rule in footnote_rules:
        if hasattr(md.renderer, rule):
            md.add_render_rule(rule, getattr(md.renderer, rule))


def main() -> None:
    """Main entry point for the mark2 application."""

    args = parse_args()
    # sys.stderr.write(str(args) + "\n")

    if not args.quiet and args.input_filename != "-":
        print(f"Reading from '{args.input_filename}'")
    if not args.quiet and args.output_filename != "-":
        print(f"Writing to   '{args.output_filename}'")

    if args.reference_html:
        renderer_cls = ReferenceHTMLRenderer
    elif args.format == "html":
        renderer_cls = HTMLRenderer
    # elif args.format == "odt":
    #     renrenderer_clsderer = ODTRenderer()
    elif args.format == "epub":
        renderer_cls = EPUBRenderer
    elif args.format == "pdf":
        renderer_cls = PDFRenderer
    elif args.format == "tex":
        renderer_cls = ConTeXtRenderer
    else:
        raise ValueError(f"Unsupported format: {args.format}")

    env = get_env(args)

    data = read_data(args.input_filename)

    md = MarkdownIt(renderer_cls=renderer_cls)
    set_plugins(md)

    md.render(data, env=env)

    # if args.reference_html_test:
    #     renderer_cls = ReferenceHTMLTestRenderer

    # tokens = md.parse(data)
    # renderer.render(tokens, args.output_filename)


if __name__ == "__main__":
    main()
