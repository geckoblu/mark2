"""Reference HTML renderer for markdown-it."""

from typing import Any, Sequence

from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.base import Renderer


class ReferenceHTMLRenderer(Renderer):
    """A reference HTML renderer that produces clean, semantic HTML."""

    __output__ = "html"

    def __init__(self, parser: Any = None):
        """Initialize the renderer."""
        super().__init__(parser)

        self.result = []
        self.html = ""

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates HTML output.

        :param tokens: list on block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input
        """
        self.result = []

        super().render(tokens, options, env)

        self.html = "".join(self.result)

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters.

        Args:
            text: The text to escape

        Returns:
            Text with HTML characters escaped
        """
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    ###########################################################################
    # All the methods not starting with "render" nor "_" are rules renderers
    ###########################################################################

    def paragraph_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening paragraph token."""
        self.result.append("<p>")

    def paragraph_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing paragraph token."""
        self.result.append("</p>\n")

    def text(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render text token."""
        token = tokens[idx]
        self.result.append(self._escape_html(token.content))

    def em_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening emphasis token."""
        self.result.append("<em>")

    def em_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing emphasis token."""
        self.result.append("</em>")

    def heading_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening heading token."""
        token = tokens[idx]
        level = token.tag  # h1, h2, etc.
        self.result.append(f"<{level}>")

    def heading_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing heading token."""
        token = tokens[idx]
        level = token.tag
        self.result.append(f"</{level}>\n")

    def bullet_list_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening bullet list token."""
        self.result.append("<ul>\n")

    def bullet_list_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing bullet list token."""
        self.result.append("</ul>\n")

    def ordered_list_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening ordered list token."""
        token = tokens[idx]
        start = self._get_attr(token, "start")
        if start and start != "1":
            self.result.append(f'<ol start="{start}">\n')
        else:
            self.result.append("<ol>\n")

    def ordered_list_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing ordered list token."""
        self.result.append("</ol>\n")

    def list_item_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening list item token."""
        self.result.append("<li>")

    def list_item_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing list item token."""
        self.result.append("</li>\n")

    def link_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening link token."""
        token = tokens[idx]
        href = self._get_attr(token, "href") or ""
        title = self._get_attr(token, "title")
        if title:
            self.result.append(
                f'<a href="{self._escape_html(href)}" title="{self._escape_html(title)}">'
            )
        else:
            self.result.append(f'<a href="{self._escape_html(href)}">')

    def link_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing link token."""
        self.result.append("</a>")

    def strong_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening strong/bold token."""
        self.result.append("<strong>")

    def strong_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing strong/bold token."""
        self.result.append("</strong>")

    def code_inline(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render inline code token."""
        token = tokens[idx]
        self.result.append(f"<code>{self._escape_html(token.content)}</code>")

    def code_block(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render code block token."""
        token = tokens[idx]
        self.result.append(f"<pre><code>{self._escape_html(token.content)}</code></pre>\n")

    def fence(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render fenced code block token."""
        token = tokens[idx]
        info = token.info.strip() if token.info else ""
        lang = info.split()[0] if info else ""

        if lang:
            self.result.append(f'<pre><code class="language-{self._escape_html(lang)}">')
        else:
            self.result.append("<pre><code>")
        self.result.append(self._escape_html(token.content))
        self.result.append("</code></pre>\n")

    def blockquote_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening blockquote token."""
        self.result.append("<blockquote>\n")

    def blockquote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing blockquote token."""
        self.result.append("</blockquote>\n")

    def hr(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render horizontal rule token."""
        self.result.append("<hr>\n")

    def image(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render image token."""
        token = tokens[idx]
        src = self._get_attr(token, "src") or ""
        alt = self._get_attr(token, "alt") or ""
        title = self._get_attr(token, "title")

        self.result.append(f'<img src="{self._escape_html(src)}" alt="{self._escape_html(alt)}"')
        if title:
            self.result.append(f' title="{self._escape_html(title)}"')
        self.result.append(">")

    def hardbreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render hard line break token."""
        self.result.append("<br>\n")

    def softbreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render soft line break token."""
        self.result.append("\n")

    def html_block(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render HTML block token."""
        token = tokens[idx]
        self.result.append(token.content)

    def html_inline(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render inline HTML token."""
        token = tokens[idx]
        self.result.append(token.content)

    def s_open(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render opening strikethrough token."""
        self.result.append("<s>")

    def s_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing strikethrough token."""
        self.result.append("</s>")

    def table_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table token."""
        self.result.append("<table>\n")

    def table_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table token."""
        self.result.append("</table>\n")

    def thead_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table header token."""
        self.result.append("<thead>\n")

    def thead_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table header token."""
        self.result.append("</thead>\n")

    def tbody_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table body token."""
        self.result.append("<tbody>\n")

    def tbody_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table body token."""
        self.result.append("</tbody>\n")

    def tr_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table row token."""
        self.result.append("<tr>\n")

    def tr_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table row token."""
        self.result.append("</tr>\n")

    def th_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table header cell token."""
        token = tokens[idx]
        align = self._get_attr(token, "style")
        if align:
            self.result.append(f'<th style="{align}">')
        else:
            self.result.append("<th>")

    def th_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table header cell token."""
        self.result.append("</th>\n")

    def td_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table data cell token."""
        token = tokens[idx]
        align = self._get_attr(token, "style")
        if align:
            self.result.append(f'<td style="{align}">')
        else:
            self.result.append("<td>")

    def td_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table data cell token."""
        self.result.append("</td>\n")


# HTML_HEADER = """<!DOCTYPE html>
# <html>
# <head>
# <meta charset="UTF-8">
# <style>
#   body {
#     font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; # pylint: disable=line-too-long
#     line-height: 1.6;
#     max-width: 800px;
#     margin: 0 auto;
#     padding: 20px;
#   }
#   p {
#     text-align: justify;
#   }
#   code {
#     background-color: #f4f4f4;
#     padding: 2px 4px;
#     border-radius: 3px;
#   }
#   pre {
#     background-color: #f4f4f4;
#     padding: 10px;
#     border-radius: 5px;
#     overflow-x: auto;
#   }
#   pre code {
#     background-color: transparent;
#     padding: 0;
#   }
#   blockquote {
#     border-left: 4px solid #ccc;
#     margin-left: 0;
#     padding-left: 20px;
#     color: #666;
#   }
#   table {
#     border-collapse: collapse;
#     width: 100%;
#   }
#   th, td {
#     border: 1px solid #ddd;
#     padding: 8px;
#     text-align: left;
#   }
#   th {
#     background-color: #f4f4f4;
#     font-weight: bold;
#   }
# </style>
# </head>
# <body>
# """

# HTML_FOOTER = """
# </body>
# </html>
# """
