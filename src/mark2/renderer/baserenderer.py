"""Base class for mark2 renderers."""

import inspect
import sys
from collections import Counter
from typing import Any, Sequence

from markdown_it.renderer import RendererProtocol, Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.plugins.yaml_parser import parse_simple_yaml


class BaseRenderer(RendererProtocol):
    """Base class for all mark2 renderers."""

    __output__: str = "html"
    rules: dict[str, Any]

    def __init__(self, parser: Any = None) -> None:
        """Initialize the renderer.

        Args:
            parser: Optional parser instance
        """
        self.debug_tokens = False
        self.tokens_counter = Counter()  # used for debug_tokens only

        self.rules = {
            k: v
            for k, v in inspect.getmembers(self, predicate=inspect.ismethod)
            if not (k.startswith("render") or k.startswith("_"))
        }

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates output.

        :param tokens: list of block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input

        """
        self.debug_tokens = env.get("debug_tokens", False)

        for i, token in enumerate(tokens):
            if token.type == "inline":
                if token.children:
                    self.render_inline(token.children, options, env)
            elif token.type in self.rules:
                self.rules[token.type](tokens, i, options, env)
            else:
                self.render_token(tokens, i, options, env)

        if self.debug_tokens and self.tokens_counter:
            print("", file=sys.stderr)
            print("--- Token type counts ----------------------------------------", file=sys.stderr)
            # for token_type, count in self.tokens_counter.most_common():
            for token_type, count in sorted(self.tokens_counter.items(), key=lambda x: x[1]):
                print(f"{token_type}: {count}", file=sys.stderr)

    def render_inline(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """The same as ``render``, but for single token of `inline` type.

        :param tokens: list of inline tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input (references, for example)
        """
        for i, token in enumerate(tokens):
            if token.type in self.rules:
                self.rules[token.type](tokens, i, options, env)
            else:
                self.render_token(tokens, i, options, env)

    def render_token(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> None:
        """Default token renderer.

        Can be overridden by custom function

        :param idx: token index to render
        :param options: params of parser instance
        """
        # raise NotImplementedError(f"[{tokens[idx]}]")
        print(f"[UNHANDLED TOKEN] {tokens[idx]}", file=sys.stderr)
        if self.debug_tokens:
            self.tokens_counter[tokens[idx].type] += 1
        else:
            sys.exit(1)

    ###########################################################################
    # front_matter_plugin renderers
    ###########################################################################

    def front_matter(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Parse front matter block (not included in output)."""
        token = tokens[idx]
        env["front_matter"] = parse_simple_yaml(token.content)
