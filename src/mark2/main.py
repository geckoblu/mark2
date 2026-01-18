#!/usr/bin/env python3
"""Main entry point for mark2 - a Markdown file converter."""

import sys

from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.attrs import attrs_block_plugin


# from mdit_py_plugins.myst_role import myst_role_plugin
from mdit_py_plugins.subscript import sub_plugin

from markdown_it import MarkdownIt

from mark2.__init__ import render_undefined
from mark2.args import get_env, parse_args
from mark2.renderer import (
    ConTeXtRenderer,
    EPUBRenderer,
    HTMLRenderer,
    PDFRenderer,
    MDRenderer,
    ReferenceHTMLRenderer,
)
from mark2.plugins import footnote_plugin as mark2_footnote_plugin
from mark2.plugins import (
    container_plugin,
    headingsid_plugin,
    myst_role_plugin,
    pagebreak_plugin,
    sup_plugin,
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
    """Set up plugins for the MarkdownIt parser.

    Args:
        md: MarkdownIt parser instance
    """
    md.use(front_matter_plugin)
    md.use(attrs_block_plugin)
    md.use(container_plugin)
    md.use(sub_plugin)
    md.use(sup_plugin)

    md.use(headingsid_plugin, min_level=1, max_level=6)
    md.use(myst_role_plugin)
    md.use(pagebreak_plugin)

    set_footnote_plugin(md)


def set_footnote_plugin(md: MarkdownIt) -> None:
    """Set up the Footnote plugin with custom render rules.

    Args:
        md: MarkdownIt parser instance
    """
    md.use(footnote_plugin, move_to_end=True)

    md.core.ruler.at("footnote_tail", mark2_footnote_plugin.footnote_tail)
    # helpers (only used in other rules, no tokens are attached to those)
    md.add_render_rule("footnote_caption", mark2_footnote_plugin.render_footnote_caption)
    md.add_render_rule("footnote_anchor_name", mark2_footnote_plugin.render_footnote_anchor_name)

    # Override Footnote plugin render rules with custom renderer methods if they exist
    footnote_rules = [
        "footnote_ref",
        "footnote_block_open",
        "footnote_block_close",
        "footnote_open",
        "footnote_close",
        "footnote_anchor",
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
                    self, tokens, idx, options, env, name="  [FOOTNOTE NOT IMPLEMENTED]"
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

    env = get_env(args)

    data = read_data(args.input_filename)

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
    elif args.format == "md":
        renderer_cls = MDRenderer
    else:
        raise ValueError(f"Unsupported format: {args.format}")

    md = MarkdownIt("commonmark", renderer_cls=renderer_cls)
    set_plugins(md)

    md.render(data, env=env)

    # if args.reference_html_test:
    #     renderer_cls = ReferenceHTMLTestRenderer

    # tokens = md.parse(data)
    # renderer.render(tokens, args.output_filename)


if __name__ == "__main__":
    main()
