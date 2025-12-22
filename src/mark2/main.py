#!/usr/bin/env python3
"""Main entry point for mark2 - a Markdown file converter."""

import sys
from typing import Sequence

from mdit_py_plugins.footnote import footnote_plugin

from markdown_it import MarkdownIt
from markdown_it.renderer import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.args import get_env, parse_args
from mark2.renderer import (
    ConTeXtRenderer,
    EPUBRenderer,
    HTMLRenderer,
    PDFRenderer,
    ReferenceHTMLRenderer,
)


def render_undefined(
    self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType, name: str
):
    """Placeholder for undefined render rules.

    This function is used when a render rule is expected but not implemented
    in the current renderer. It returns an empty string to prevent errors.

    Args:
        self: Renderer instance
        tokens: Token sequence
        idx: Current token index
        options: Parser options
        env: Environment

    Returns:
        Empty string
    """
    token = tokens[idx]
    print(
        f"{name} {token.type}: tag={token.tag}, nesting={token.nesting}, attrs={token.attrs}, content='{token.content}'",  # pylint: disable=line-too-long
        file=sys.stderr,
    )
    return ""


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
        else:
            # Wrap partial in lambda to avoid AttributeError with __get__
            md.add_render_rule(
                rule,
                lambda self, tokens, idx, options, env: render_undefined(
                    self, tokens, idx, options, env, name="  [FOOTNOTE]"
                ),
            )


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
