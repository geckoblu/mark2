# pylint: skip-file

"""Minimal Markdown renderer compatible with markdown-it."""


class MDRenderer:
    """A minimal Markdown renderer for markdown-it tokens."""

    def __init__(self) -> None:
        """Initialize the renderer."""
        pass

    def render(self, tokens: list, options: dict | None = None, env: dict | None = None) -> str:
        """
        Render tokens to Markdown.

        Args:
            tokens: List of tokens from markdown-it parser
            options: Optional rendering options
            env: Optional environment variables

        Returns:
            str: Rendered Markdown string
        """
        if options is None:
            options = {}
        if env is None:
            env = {}

        result = []
        self._render_tokens(tokens, result)
        return "".join(result)

    def _render_tokens(self, tokens: list, result: list[str]) -> None:
        """Recursively render tokens."""
        for token in tokens:
            if token.type == "paragraph_open":
                pass
            elif token.type == "paragraph_close":
                result.append("\n\n")
            elif token.type == "heading_open":
                level = int(token.tag[1])  # h1 -> 1, h2 -> 2, etc.
                result.append("#" * level + " ")
            elif token.type == "heading_close":
                result.append("\n\n")
            elif token.type == "text":
                result.append(token.content)
            elif token.type == "inline":
                if token.children:
                    self._render_tokens(token.children, result)
            elif token.type == "em_open":
                result.append("*")
            elif token.type == "em_close":
                result.append("*")
            elif token.type == "strong_open":
                result.append("**")
            elif token.type == "strong_close":
                result.append("**")
            elif token.type == "code_inline":
                result.append(f"`{token.content}`")
            elif token.type == "code_block":
                result.append(f"    {token.content}\n")
            elif token.type == "fence":
                info = token.info or ""
                result.append(f"```{info}\n{token.content}```\n\n")
            elif token.type == "bullet_list_open":
                pass
            elif token.type == "bullet_list_close":
                result.append("\n")
            elif token.type == "ordered_list_open":
                pass
            elif token.type == "ordered_list_close":
                result.append("\n")
            elif token.type == "list_item_open":
                result.append("- ")
            elif token.type == "list_item_close":
                result.append("\n")
            elif token.type == "blockquote_open":
                result.append("> ")
            elif token.type == "blockquote_close":
                result.append("\n")
            elif token.type == "link_open":
                result.append("[")
            elif token.type == "link_close":
                href = self._get_href(token)
                result.append(f"]({href})")
            elif token.type == "image":
                alt = token.content or ""
                href = self._get_attr(token, "src") or ""
                result.append(f"![{alt}]({href})")
            elif token.type == "softbreak":
                result.append("\n")
            elif token.type == "hardbreak":
                result.append("  \n")
            elif token.type == "hr":
                result.append("---\n\n")

    def _get_attr(self, token, attr_name: str) -> str | None:
        """Get attribute value from token."""
        if token.attrs:
            for attr in token.attrs:
                if attr[0] == attr_name:
                    return attr[1]
        return None

    def _get_href(self, token) -> str | None:
        """Get href from link token."""
        return self._get_attr(token, "href")
