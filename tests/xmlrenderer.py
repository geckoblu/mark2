"""Minimal Markdown renderer compatible with markdown-it."""

# pylint: skip-file


class XMLRenderer:
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
            print(token.type)
            if token.type == "paragraph_open":
                result.append("<p>")
            elif token.type == "paragraph_close":
                result.append("</p>\n")
            elif token.type == "heading_open":
                level = int(token.tag[1])  # h1 -> 1, h2 -> 2, etc.
                result.append(f"<h{level}>")
            elif token.type == "heading_close":
                level = int(token.tag[1])
                result.append(f"</h{level}>\n")
            elif token.type == "text":
                result.append(token.content)
            elif token.type == "inline":
                if token.children:
                    self._render_tokens(token.children, result)
            elif token.type == "em_open":
                result.append("<em>")
            elif token.type == "em_close":
                result.append("</em>")
            elif token.type == "strong_open":
                result.append("<strong>")
            elif token.type == "strong_close":
                result.append("</strong>")
            elif token.type == "code_inline":
                result.append(f"<code>{token.content}</code>")
            elif token.type == "code_block":
                result.append(f"<pre><code>{token.content}</code></pre>\n")
            elif token.type == "fence":
                result.append(f"<pre><code>{token.content}</code></pre>\n")
            # Add more token types as needed
