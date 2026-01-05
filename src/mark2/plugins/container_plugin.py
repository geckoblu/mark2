"""Process block-level custom containers.

The content of this file is adapted from mdit-py-plugins container plugin,
with modifications to ."""

# pylint: disable=invalid-name  # Because of the naming conventions in markdown-it-py

import sys
from collections.abc import Callable, Sequence
from math import floor
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol
from markdown_it.rules_block import StateBlock
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mdit_py_plugins.utils import is_code_block


def container_plugin(
    md: MarkdownIt,
    marker: str = ":",
    validate: None | Callable[[str, str], tuple[bool, str]] = None,
    render: None | Callable[..., str] = None,
) -> None:
    """Plugin ported from
    `markdown-it-container <https://github.com/markdown-it/markdown-it-container>`__.

    It is a plugin for creating block-level custom containers:

    .. code-block:: md

        :::: name
        ::: name
        *markdown*
        :::
        ::::

    This plugin accepts any valid class name dynamically without pre-configuration.

    :param marker: the marker character to use
    :param validate: func(params, marker) -> tuple[bool, str],
                     should return (True, class_name) or (False, "")
    :param render: render func

    """

    def validateDefault(params: str, *args: Any) -> tuple[bool, str]:
        # Extract the first word as the class name
        class_name = params.strip().split(" ", 1)[0]
        # Accept any non-empty class name
        if class_name:
            return True, class_name
        return False, ""

    def renderDefault(
        self: RendererProtocol,
        tokens: Sequence[Token],
        idx: int,
        _options: OptionsDict,
        env: EnvType,
    ) -> str:
        token = tokens[idx]
        # Extract class name from token info and add it to the opening tag
        if token.nesting == 1:
            class_name = token.info.strip().split(" ", 1)[0]
            if class_name:
                token.attrJoin("class", class_name)

        if hasattr(self, "renderToken"):
            # markdown-it-py compatibility
            return self.renderToken(tokens, idx, _options, env)
        else:
            renderer_func = token.type
            if hasattr(self, renderer_func):
                return renderer_func(tokens, idx, _options, env)
            elif hasattr(self, "container_open") and token.type == "container_open":
                return self.container_open(tokens, idx, _options, env)
            elif hasattr(self, "container_close") and token.type == "container_close":
                return self.container_close(tokens, idx, _options, env)
            else:
                # Debug output to stderr
                print(
                    f"  [CONTAINER] {token.type}: attrs={token.attrs}, content='{token.content}'",
                    file=sys.stderr,
                )
                return ""

    min_markers = 3
    marker_str = marker
    marker_char = marker_str[0]
    marker_len = len(marker_str)
    validate = validate or validateDefault
    render = render or renderDefault

    def container_func(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
        if is_code_block(state, startLine):
            return False

        auto_closed = False
        start = state.bMarks[startLine] + state.tShift[startLine]
        maximum = state.eMarks[startLine]

        # Check out the first character quickly,
        # this should filter out most of non-containers
        if marker_char != state.src[start]:
            return False

        # Check out the rest of the marker string
        pos = start + 1
        while pos <= maximum:
            try:
                character = state.src[pos]
            except IndexError:
                break
            if marker_str[(pos - start) % marker_len] != character:
                break
            pos += 1

        marker_count = floor((pos - start) / marker_len)
        if marker_count < min_markers:
            return False
        pos -= (pos - start) % marker_len

        markup = state.src[start:pos]
        params = state.src[pos:maximum]
        assert validate is not None
        is_valid, container_name = validate(params, markup)
        if not is_valid:
            return False

        # Since start is found, we can report success here in validation mode
        if silent:
            return True

        # Search for the end of the block
        nextLine = startLine

        while True:
            nextLine += 1
            if nextLine >= endLine:
                # unclosed block should be autoclosed by end of document.
                # also block seems to be autoclosed by end of parent
                break

            start = state.bMarks[nextLine] + state.tShift[nextLine]
            maximum = state.eMarks[nextLine]

            if start < maximum and state.sCount[nextLine] < state.blkIndent:
                # non-empty line with negative indent should stop the list:
                # - ```
                #  test
                break

            if marker_char != state.src[start]:
                continue

            if is_code_block(state, nextLine):
                continue

            pos = start + 1
            while pos <= maximum:
                try:
                    character = state.src[pos]
                except IndexError:
                    break
                if marker_str[(pos - start) % marker_len] != character:
                    break
                pos += 1

            # closing code fence must be at least as long as the opening one
            if floor((pos - start) / marker_len) < marker_count:
                continue

            # make sure tail has spaces only
            pos -= (pos - start) % marker_len
            pos = state.skipSpaces(pos)

            if pos < maximum:
                continue

            # found!
            auto_closed = True
            break

        old_parent = state.parentType
        old_line_max = state.lineMax
        state.parentType = "container"

        # this will prevent lazy continuations from ever going past our end marker
        state.lineMax = nextLine

        token = state.push(f"container_{container_name}_open", "div", 1)
        token.markup = markup
        token.block = True
        token.info = params
        token.map = [startLine, nextLine]

        state.md.block.tokenize(state, startLine + 1, nextLine)

        token = state.push(f"container_{container_name}_close", "div", -1)
        token.markup = state.src[start:pos]
        token.block = True

        state.parentType = old_parent
        state.lineMax = old_line_max
        state.line = nextLine + (1 if auto_closed else 0)

        return True

    md.block.ruler.before(
        "fence",
        "container_generic",
        container_func,
        {"alt": ["paragraph", "reference", "blockquote", "list"]},
    )

    # Store the render function to be used dynamically
    if not hasattr(md, "_container_render"):
        md._container_render = render  # pylint: disable=protected-access

    # Add a catch-all renderer for any container type
    original_render = md.renderer.render

    def patched_render(tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> str:
        # Add render rules dynamically for any container_*_open/close tokens
        for token in tokens:
            if token.type.startswith("container_") and (
                token.type.endswith("_open") or token.type.endswith("_close")
            ):
                if token.type not in md.renderer.rules:
                    md.add_render_rule(token.type, render)
        return original_render(tokens, options, env)

    md.renderer.render = patched_render
