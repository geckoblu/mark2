"""Configuration values used to build the ConTeXt document header."""

from dataclasses import dataclass


@dataclass
class ContextConfig:
    """Parameters controlling the generated ConTeXt header.

    Values default to the current A4 layout; use :meth:`a4` / :meth:`a5`
    to obtain the presets matching the existing hard-coded headers.
    """

    page_format: str = "A4"
    language: str = "it"

    # Page numbering (\setuppagenumbering)
    pagenumbering_alternative: str = "doublesided"

    # Page geometry (\setuplayout)
    topspace: str = "15mm"
    bottomspace: str = "15mm"
    header: str = "5mm"
    footer: str = "5mm"
    headerdistance: str = "5mm"
    backspace: str = "25mm"
    rightedge: str = "1mm"
    rightmargin: str = "29mm"

    # Typography (\setupbodyfont)
    font_name: str = "libertinus"
    font_size: str = "12pt"
    indenting: str = "medium"

    # Footnotes (\setupfootnotes / \setupnote)
    footnote_columns: int | None = 2
    footnote_bodyfont: str = "11pt"
    footnote_distance: str | None = "-1mm"

    # Project-specific structural tweaks
    subsubsection_start_right_page: bool = False
    define_verse_helpers: bool = False

    @classmethod
    def a4(cls) -> "ContextConfig":
        """Return the configuration matching the current A4 header."""
        return cls(
            page_format="A4",
            pagenumbering_alternative="doublesided",
            topspace="15mm",
            bottomspace="15mm",
            backspace="25mm",
            rightmargin="29mm",
            font_name="libertinus",
            indenting="medium",
            footnote_columns=2,
            footnote_bodyfont="11pt",
            footnote_distance="-1mm",
            subsubsection_start_right_page=True,
            define_verse_helpers=True,
        )

    @classmethod
    def a5(cls) -> "ContextConfig":
        """Return the configuration matching the current A5 header."""
        return cls(
            page_format="A5",
            pagenumbering_alternative="singlesided",
            topspace="5mm",
            bottomspace="5mm",
            backspace="5mm",
            rightmargin="12mm",
            font_name="liberation",
            indenting="small",
            footnote_columns=None,
            footnote_bodyfont="9pt",
            footnote_distance=None,
            subsubsection_start_right_page=False,
            define_verse_helpers=False,
        )
