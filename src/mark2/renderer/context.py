"""Minimal ConTeXt renderer compatible with markdown-it."""

from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.base import Renderer


class ConTeXtRenderer(Renderer):
    """A minimal ConTeXt renderer for markdown-it tokens."""

    def __init__(self) -> None:
        """Initialize the ConTeXt renderer.

        Sets up state tracking for link rendering.
        """
        self.in_link = False
        self.link_href = ""

    def render(
        self,
        tokens: list[Token],
        output_filename: str,
        options: OptionsDict,
        env: EnvType | None = None,
    ) -> None:
        """
        Render markdown-it tokens to ConTeXt.

        Args:
            tokens: List of tokens from markdown-it parser
            output_filename: Output file path (use '-' for stdout)
            options: Optional rendering options
            env: Optional environment variables
        """
        if options is None:
            options = {}
        if env is None:
            env = {}

        result = []
        self._render_tokens(tokens, result)
        tex = "".join(result)

        with self._open_output(output_filename) as writer:
            print(CONTEXT_HEADER, file=writer)
            print(tex, file=writer)
            print(CONTEXT_FOOTER, file=writer)

    def _render_tokens(self, tokens: list[Token], result: list[str]) -> None:
        """Recursively render tokens to ConTeXt format.

        Args:
            tokens: List of markdown-it tokens to render
            result: Accumulator list for rendered ConTeXt strings
        """
        for token in tokens:
            if token.type == "paragraph_open":
                pass
            elif token.type == "paragraph_close":
                result.append("\n\n")
            elif token.type == "heading_open":
                level = int(token.tag[1])  # h1 -> 1, h2 -> 2, etc.
                heading_map = {
                    1: "\\section{",
                    2: "\\subsection{",
                    3: "\\subsubsection{",
                    4: "\\subsubsubsection{",
                    5: "\\subsubsubsubsection{",
                    6: "\\subsubsubsubsubsection{",
                }
                result.append(heading_map.get(level, "\\section{"))
            elif token.type == "heading_close":
                result.append("}\n\n")
            elif token.type == "text":
                result.append(self._escape_tex(token.content))
            elif token.type == "inline":
                if token.children:
                    self._render_tokens(token.children, result)
            elif token.type == "em_open":
                result.append("{\\em ")
            elif token.type == "em_close":
                result.append("}")
            elif token.type == "strong_open":
                result.append("{\\bf ")
            elif token.type == "strong_close":
                result.append("}")
            elif token.type == "code_inline":
                result.append(f"\\type{{{self._escape_tex(token.content)}}}")
            elif token.type == "code_block":
                result.append(f"\\starttyping\n{token.content}\\stoptyping\n\n")
            elif token.type == "fence":
                info = token.info or ""
                if info:
                    result.append(f"\\starttyping[option={info}]\n{token.content}\\stoptyping\n\n")
                else:
                    result.append(f"\\starttyping\n{token.content}\\stoptyping\n\n")
            elif token.type == "bullet_list_open":
                result.append("\\startitemize\n")
            elif token.type == "bullet_list_close":
                result.append("\\stopitemize\n\n")
            elif token.type == "ordered_list_open":
                result.append("\\startitemize[n]\n")
            elif token.type == "ordered_list_close":
                result.append("\\stopitemize\n\n")
            elif token.type == "list_item_open":
                result.append("\\item ")
            elif token.type == "list_item_close":
                result.append("\n")
            elif token.type == "blockquote_open":
                result.append("\\startblockquote\n")
            elif token.type == "blockquote_close":
                result.append("\\stopblockquote\n\n")
            elif token.type == "link_open":
                self.link_href = self._get_attr(token, "href") or ""
                self.in_link = True
                result.append("\\goto{")
            elif token.type == "link_close":
                result.append(f"}}[url({self.link_href})]")
                self.in_link = False
            elif token.type == "image":
                alt = token.content or ""
                href = self._get_attr(token, "src") or ""
                if alt:
                    result.append(f"\\placefigure[here]{{{alt}}}{{\\externalfigure[{href}]}}")
                else:
                    result.append(f"\\externalfigure[{href}]")
            elif token.type == "softbreak":
                result.append(" ")
            elif token.type == "hardbreak":
                result.append("\\\\\n")
            elif token.type == "hr":
                result.append("\\thinrule\n\n")

    def _get_attr(self, token: Token, attr_name: str) -> str | None:
        """Get attribute value from token.

        Args:
            token: The markdown-it token to extract attribute from
            attr_name: The name of the attribute to retrieve

        Returns:
            The attribute value if found, None otherwise
        """
        if token.attrs:
            for attr in token.attrs:
                if attr[0] == attr_name:
                    return attr[1]
        return None

    def _get_href(self, token: Token) -> str | None:
        """Get href attribute from link token.

        Args:
            token: The markdown-it link token

        Returns:
            The href URL if found, None otherwise
        """
        return self._get_attr(token, "href")

    def _escape_tex(self, text: str) -> str:
        """Escape special ConTeXt/TeX characters.

        Args:
            text: The text string to escape

        Returns:
            The text with special characters properly escaped for ConTeXt
        """
        replacements = {
            "\\": "\\textbackslash{}",
            "{": "\\{",
            "}": "\\}",
            "$": "\\$",
            "&": "\\&",
            "%": "\\%",
            "#": "\\#",
            "_": "\\letterunderscore{}",
            "~": "\\lettertilde{}",
            "^": "\\letterhat{}",
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text


CONTEXT_HEADER = """\\starttext
"""

CONTEXT_FOOTER = """\\stoptext
"""
