"""Utility functions for specification tests.

This module provides helper functions for creating MarkdownIt instances
with various renderers for testing purposes.
"""

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML

from mark2.main import set_plugins
from mark2.renderer import (
    HTMLRenderer,
    EPUBRenderer,
    PDFRenderer,
    ConTeXtRenderer,
    MDRenderer,
)


def get_MarkdownIt(renderer: str) -> MarkdownIt:  # pylint: disable=invalid-name
    """Create a MarkdownIt instance with default settings."""

    if renderer == "default":
        renderer_cls = RendererHTML
    elif renderer == "html":
        renderer_cls = HTMLRenderer
    # elif renderer == "odt":
    #     renderer_cls = ODTRenderer()
    elif renderer == "epub":
        renderer_cls = EPUBRenderer
    elif renderer == "pdf":
        renderer_cls = PDFRenderer
    elif renderer == "tex":
        renderer_cls = ConTeXtRenderer
    elif renderer == "md":
        renderer_cls = MDRenderer
    else:
        raise ValueError(f"Unsupported renderer: {renderer}")

    md = MarkdownIt("commonmark", renderer_cls=renderer_cls)
    set_plugins(md)

    return md
