"""Configuration values used to build the ConTeXt document header."""

from dataclasses import dataclass, field
from typing import Sequence

from markdown_it.token import Token
from markdown_it.utils import EnvType
from mark2.plugins.yaml_parser import parse_simple_yaml


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
    define_verse_helpers: bool = False

    # Heading levels (e.g. ["h2", "h3"]) that must start on a recto (right-hand) page.
    # Front-matter only for now (`pdf-header-at-recto: h2,h3`);
    # not yet consumed by the header builder.
    header_at_recto: list[str] = field(default_factory=list)

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
            define_verse_helpers=False,
        )

    @classmethod
    def get(cls, env: EnvType, filtered: Sequence[Token]) -> "ContextConfig":
        """Get the appropriate ContextConfig based on environment and front matter.

        Args:
            env: The environment dictionary containing potential overrides.
            filtered: The list of tokens from the parsed markdown, used to extract front matter.

        Returns:
            An instance of ContextConfig with values overridden by front matter and environment
            variables if available.
        """
        page_format = env.get("pdf_page_format", "A4")
        pfl = page_format.lower()
        cfg = ContextConfig.a5() if page_format == "A5" else ContextConfig.a4()

        # Parse Front Matter
        front_matter_token = next((tok for tok in filtered if tok.type == "front_matter"), None)
        front_matter = parse_simple_yaml(front_matter_token.content) if front_matter_token else {}

        # Override with Front Matter and environment variables if available
        if front_matter.get("pdf-font-size"):
            cfg.font_size = str(front_matter["pdf-font-size"])
        if front_matter.get(f"pdf-{pfl}-font-size"):
            cfg.font_size = str(front_matter[f"pdf-{pfl}-font-size"])
        if env.get("pdf_font_size"):
            cfg.font_size = env["pdf_font_size"]

        if front_matter.get("pdf-font-name"):
            cfg.font_name = str(front_matter["pdf-font-name"])
        if front_matter.get(f"pdf-{pfl}-font-name"):
            cfg.font_name = str(front_matter[f"pdf-{pfl}-font-name"])
        if env.get("pdf_font_name"):
            cfg.font_name = env["pdf_font_name"]

        if front_matter.get("pdf-header-at-recto"):
            cfg.header_at_recto = _parse_header_at_recto(str(front_matter["pdf-header-at-recto"]))
        if front_matter.get(f"pdf-{pfl}-header-at-recto"):
            cfg.header_at_recto = _parse_header_at_recto(
                str(front_matter[f"pdf-{pfl}-header-at-recto"])
            )

        return cfg


VALID_HEADER_AT_RECTO_LEVELS = ("h1", "h2", "h3", "h4")


def _parse_header_at_recto(raw: str) -> list[str]:
    """Parse and validate a comma-separated list of heading levels.

    Args:
        raw: Comma-separated heading levels, e.g. ``"h2,h3"``.

    Returns:
        The parsed heading levels.

    Raises:
        ValueError: If any level is not one of ``h1``, ``h2``, ``h3``, ``h4``.
    """
    levels = [level.strip() for level in raw.split(",") if level.strip()]
    invalid = [level for level in levels if level not in VALID_HEADER_AT_RECTO_LEVELS]
    if invalid:
        raise ValueError(
            f"Invalid pdf-header-at-recto level(s) {invalid}; "
            f"expected one of {VALID_HEADER_AT_RECTO_LEVELS}"
        )
    return levels
