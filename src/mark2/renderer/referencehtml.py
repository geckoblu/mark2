"""Reference HTML renderer for markdown-it."""

import sys
from typing import Any, Sequence

# Import Footnote render functions
from mdit_py_plugins.footnote.index import (
    render_footnote_anchor,
    render_footnote_anchor_name,
    render_footnote_block_close,
    render_footnote_block_open,
    render_footnote_caption,
    render_footnote_close,
    render_footnote_open,
    render_footnote_ref,
)

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
        self.debug = False

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates HTML output.

        :param tokens: list on block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input
        """
        self.debug = env.get("debug", False)
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

    def _debug_output(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
        output: str,
        name: str = "[RENDER]",
    ) -> None:
        """Print debug output in a single line with fixed width formatting.

        Args:
            tokens: Token sequence
            idx: Current token index
            options: Parser options
            env: Environment
            output: The HTML output to display (max 20 chars)
        """
        token = tokens[idx]
        # Create the first part (80 chars max)
        first_part = f"{name} {token.type}: tag={token.tag}, nesting={token.nesting}, attrs={token.attrs}, content='{token.content}'"  # pylint: disable=line-too-long
        # Truncate if too long and pad to 80 chars
        if len(first_part) > 80:
            first_part = first_part[:77] + "..."
        first_part = first_part.ljust(80)

        # Second part (40 chars max)
        second_part = output[:40] if len(output) > 40 else output
        second_part = second_part.replace("\n", "↩").replace("\r", "↩")  # Escape newlines

        print(f"{first_part}  {second_part}", file=sys.stderr)

    ###########################################################################
    # All the methods not starting with "render" nor "_" are rules renderers
    ###########################################################################

    def paragraph_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening paragraph token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<p>")
        self.result.append("<p>")

    def paragraph_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing paragraph token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</p>")
        self.result.append("</p>\n")

    def text(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render text token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, tokens[idx].content)
        token = tokens[idx]
        self.result.append(self._escape_html(token.content))

    def em_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening emphasis token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<em>")
        self.result.append("<em>")

    def em_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing emphasis token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</em>")
        self.result.append("</em>")

    def heading_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening heading token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, f"<{tokens[idx].tag}>")
        token = tokens[idx]
        level = token.tag  # h1, h2, etc.
        self.result.append(f"<{level}>")

    def heading_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing heading token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, f"</{tokens[idx].tag}>")
        token = tokens[idx]
        level = token.tag
        self.result.append(f"</{level}>\n")

    def bullet_list_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening bullet list token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<ul>")
        self.result.append("<ul>\n")

    def bullet_list_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing bullet list token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</ul>")
        self.result.append("</ul>\n")

    def ordered_list_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening ordered list token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<ol>")
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
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</ol>")
        self.result.append("</ol>\n")

    def list_item_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening list item token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<li>")
        self.result.append("<li>")

    def list_item_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing list item token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</li>")
        self.result.append("</li>\n")

    def link_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening link token."""
        if self.debug:
            href = self._get_attr(tokens[idx], "href") or ""
            self._debug_output(tokens, idx, options, env, f"<a href='{href[:10]}'>")
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
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</a>")
        self.result.append("</a>")

    def strong_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening strong/bold token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<strong>")
        self.result.append("<strong>")

    def strong_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing strong/bold token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</strong>")
        self.result.append("</strong>")

    def code_inline(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render inline code token."""
        if self.debug:
            self._debug_output(
                tokens, idx, options, env, f"<code>{tokens[idx].content[:10]}</code>"
            )
        token = tokens[idx]
        self.result.append(f"<code>{self._escape_html(token.content)}</code>")

    def code_block(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render code block token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<pre><code>...")
        token = tokens[idx]
        self.result.append(f"<pre><code>{self._escape_html(token.content)}</code></pre>\n")

    def fence(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render fenced code block token."""
        if self.debug:
            lang = tokens[idx].info[:10] if tokens[idx].info else ""
            self._debug_output(tokens, idx, options, env, f"<pre><code lang={lang}>")
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
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<blockquote>")
        self.result.append("<blockquote>\n")

    def blockquote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing blockquote token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</blockquote>")
        self.result.append("</blockquote>\n")

    def hr(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render horizontal rule token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<hr>")
        self.result.append("<hr>\n")

    def image(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render image token."""
        if self.debug:
            src = self._get_attr(tokens[idx], "src") or ""
            self._debug_output(tokens, idx, options, env, f"<img src='{src[:10]}'>")
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
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<br>")
        self.result.append("<br>\n")

    def softbreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render soft line break token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "softbreak")
        self.result.append("\n")

    def html_block(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render HTML block token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, tokens[idx].content[:20])
        token = tokens[idx]
        self.result.append(token.content)

    def html_inline(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render inline HTML token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, tokens[idx].content[:20])
        token = tokens[idx]
        self.result.append(token.content)

    def s_open(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
        """Render opening strikethrough token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<s>")
        self.result.append("<s>")

    def s_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing strikethrough token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</s>")
        self.result.append("</s>")

    def table_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<table>")
        self.result.append("<table>\n")

    def table_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</table>")
        self.result.append("</table>\n")

    def thead_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table header token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<thead>")
        self.result.append("<thead>\n")

    def thead_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table header token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</thead>")
        self.result.append("</thead>\n")

    def tbody_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table body token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<tbody>")
        self.result.append("<tbody>\n")

    def tbody_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table body token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</tbody>")
        self.result.append("</tbody>\n")

    def tr_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table row token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<tr>")
        self.result.append("<tr>\n")

    def tr_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing table row token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</tr>")
        self.result.append("</tr>\n")

    def th_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table header cell token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<th>")
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
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</th>")
        self.result.append("</th>\n")

    def td_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening table data cell token."""
        if self.debug:
            self._debug_output(tokens, idx, options, env, "<td>")
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
        if self.debug:
            self._debug_output(tokens, idx, options, env, "</td>")
        self.result.append("</td>\n")

    ###########################################################################
    # Footnote plugin renderers
    ###########################################################################

    # Helper methods (return values, used by other render rules)
    def footnote_anchor_name(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Generate footnote anchor ID.
        The anchor name is used in HTML id and href attributes for linking."""
        return render_footnote_anchor_name(self, tokens, idx, options, env)

    def footnote_caption(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Generate footnote caption text.
        The caption is what's displayed to users (the visible number)."""
        return render_footnote_caption(self, tokens, idx, options, env)

    # Token renderers
    def footnote_ref(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render footnote reference (inline superscript link)."""
        output = render_footnote_ref(self, tokens, idx, options, env)
        self.result.append(output)

        if self.debug:
            self._debug_output(tokens, idx, options, env, output, name="  [FOOTNOTE]")

    def footnote_block_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening of footnote block section."""
        output = render_footnote_block_open(self, tokens, idx, options, env)
        self.result.append(output)

        if self.debug:
            self._debug_output(tokens, idx, options, env, output[:40], name="  [FOOTNOTE]")

    def footnote_block_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing of footnote block section."""
        output = render_footnote_block_close(self, tokens, idx, options, env)
        self.result.append(output)

        if self.debug:
            self._debug_output(tokens, idx, options, env, output, name="  [FOOTNOTE]")

    def footnote_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening of individual footnote item."""
        output = render_footnote_open(self, tokens, idx, options, env)
        self.result.append(output)

        if self.debug:
            self._debug_output(tokens, idx, options, env, output, name="  [FOOTNOTE]")

    def footnote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing of individual footnote item."""
        output = render_footnote_close(self, tokens, idx, options, env)
        self.result.append(output)

        if self.debug:
            self._debug_output(tokens, idx, options, env, output, name="  [FOOTNOTE]")

    def footnote_anchor(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render back-reference link at end of footnote."""
        output = render_footnote_anchor(self, tokens, idx, options, env)
        self.result.append(output)

        if self.debug:
            self._debug_output(tokens, idx, options, env, output, name="  [FOOTNOTE]")

    def footnote_reference_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render opening of footnote reference item (in footnote block)."""
        output = "----------"  # renderer_footnote_reference_open(self, tokens, idx, options, env)
        self.result.append(output)

        if self.debug:
            self._debug_output(tokens, idx, options, env, output, name="  [FOOTNOTE]")

    def footnote_reference_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> None:
        """Render closing of footnote reference item (in footnote block)."""
        output = "##########"  # renderer_footnote_reference_close(self, tokens, idx, options, env)
        self.result.append(output)

        if self.debug:
            self._debug_output(tokens, idx, options, env, output, name="  [FOOTNOTE]")


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
