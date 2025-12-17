from mark2.renderer.base import Renderer


class ReferenceHTMLRenderer(Renderer):
    __output__ = "html"

    # def text(self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType) -> None:
    #     return escapeHtml(tokens[idx].content)
