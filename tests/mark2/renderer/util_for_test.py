"""Utility functions for testing markdown renderers."""

import io
from contextlib import redirect_stdout

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol


def render_str_output(
    renderer_cls: RendererProtocol,
    markdown_input: str,
) -> str:
    """Render markdown input using renderer_cls and return the output string."""

    # Create markdown parser
    md = MarkdownIt("commonmark", renderer_cls=renderer_cls)

    # Capture stdout since render() writes to stdout when output is "-"
    env = {"output_filename": "-"}
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        # Parse and render
        md.render(markdown_input, env=env)

    rendered_output = output_buffer.getvalue()

    return rendered_output
