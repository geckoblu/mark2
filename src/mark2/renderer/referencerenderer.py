"""Reference HTML renderer for markdown-it."""

import sys
from typing import Any, Sequence


from markdown_it.renderer import RendererProtocol, Token
from markdown_it.utils import EnvType, OptionsDict


class ReferenceRenderer(RendererProtocol):
    """Reference renderer that outputs token stream structure for debugging."""

    __output__: str = "html"
    rules: dict[str, Any]

    def __init__(self, parser: Any = None) -> None:
        """Initialize the renderer.

        Args:
            parser: Optional parser instance
        """
        super().__init__(parser)

        self.rules = {}
        self.column_lengths = {}

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates output.

        :param tokens: list of block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input

        """
        self.print_renderer_rules()

        # First pass: calculate column widths
        self.column_lengths = {
            "type": 0,
            "tag": 0,
            "nesting": 0,
            "attrs": 0,
        }
        self._calculate_column_widths(tokens, 0)

        # Second pass: print with calculated widths
        self._render_tokens(tokens, 0)

    def _render_tokens(self, tokens: Sequence[Token], indent_level: int) -> None:
        """Render tokens with proper indentation and column widths."""
        for token in tokens:
            self._output_token(token, indent_level)
            if token.children:
                self._render_tokens(token.children, indent_level + 1)

    def _calculate_column_widths(self, tokens: Sequence[Token], indent_level: int) -> None:
        """Calculate maximum column widths for token display."""
        for token in tokens:
            self.get_column_widths(token, indent_level)
            if token.children:
                self._calculate_column_widths(token.children, indent_level + 1)

    def get_column_widths(self, token, indent_level: int) -> None:
        """Update column widths based on the given token."""
        self.column_lengths["type"] = max(
            self.column_lengths["type"], len(token.type) + indent_level * 2
        )
        self.column_lengths["tag"] = max(self.column_lengths["tag"], len(str(token.tag)))
        self.column_lengths["nesting"] = max(
            self.column_lengths["nesting"], len(str(token.nesting))
        )
        self.column_lengths["attrs"] = max(self.column_lengths["attrs"], len(str(token.attrs)))

    def _output_token(self, token: Token, indent_level: int) -> None:
        """Output a single token with proper indentation and column widths."""
        indent = "  " * indent_level
        type_ = f"{indent}{str(token.type)}".ljust(self.column_lengths["type"])
        tag = f"{str(token.tag)},".ljust(self.column_lengths["tag"] + 1)
        nesting = f"{str(token.nesting)},".rjust(self.column_lengths["nesting"] + 1)
        attrs = f"{str(token.attrs)},".ljust(self.column_lengths["attrs"] + 1)
        content = token.content.replace("\n", "↩").replace("\r", "↩")  # Escape newlines

        line = f"{type_} : tag={tag} nesting={nesting} attrs={attrs}" + f" content='{content}'"
        if len(line) > 175:
            line = line[:171] + "...'"

        print(
            line,
            file=sys.stderr,
        )

    def print_renderer_rules(self) -> None:
        """Print all renderer rules defined outside this class."""
        # TO_SKIP = {}

        lines = []
        # Get all class names in the renderer's MRO (method resolution order)
        renderer_class_names = {cls.__name__ for cls in self.__class__.__mro__}

        for rule_name, method in self.rules.items():
            original = method.__func__

            # Extract class name from __qualname__
            class_name = (
                original.__qualname__.rsplit(".", 1)[0] if "." in original.__qualname__ else None
            )

            # Skip methods defined in the renderer class itself or inherited from parent classes
            if class_name in renderer_class_names:
                continue

            first_part = f"{original.__module__}.{original.__qualname__}"
            # Skip specific known methods
            # if first_part in TO_SKIP:
            #     continue

            # Truncate if too long and pad to 80 chars
            if len(first_part) > 80:
                first_part = first_part[:77] + "..."
            first_part = first_part.ljust(80)

            rule_name = rule_name.ljust(30)
            lines.append(rule_name + " " + first_part)

        print("---", file=sys.stderr)
        for line in sorted(lines):
            print(line, file=sys.stderr)
        print("---", file=sys.stderr)
