#!/usr/bin/env python3
"""Test script for markdown-it with custom renderers."""

# pylint: skip-file

from pprint import pprint
from markdown_it import MarkdownIt

from mdrenderer import MDRenderer
from xmlrenderer import XMLRenderer


def main() -> None:
    """Test script for markdown-it rendering with custom renderers."""
    # md = MarkdownIt()
    # print(md.render("some *text*"))

    # for token in md.parse("some *text*"):
    #     pprint(token.as_dict())
    #     print()

    # print()
    # print("-" * 40)

    md = MarkdownIt("commonmark")
    tokens = md.parse(
        """
allora\
cosa
dici di * Atene * ?

> allora cosa *dici* di * Atene * ?
> *Dopo questi fatti* – i fatti di Atene – *Paolo lasciò Atene e si recò a Corinto*
"""
    )
    pprint([(t.type, t.nesting) for t in tokens])

    # renderer = MDRenderer()
    # options = {}
    # env = {}

    # output_markdown = renderer.render(tokens, options, env)
    # print(output_markdown)

    renderer = XMLRenderer()
    options = {}
    env = {}

    output_xml = renderer.render(tokens, options, env)
    print(output_xml)


if __name__ == "__main__":
    main()
