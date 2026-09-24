"""Configuration values used to build the ConTeXt document header."""

import re
import sys
from dataclasses import dataclass, field, fields
from decimal import Decimal
from pathlib import Path
from typing import Sequence, get_args, get_origin, get_type_hints
from types import UnionType

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
    topspace: str = "10mm"
    header: str = "5mm"
    headerdistance: str = "5mm"
    bottomspace: str = "10mm"
    footer: str = "5mm"
    footerdistance: str = "5mm"

    # Internal value: it is added to backspace by get() for doublesided layouts.
    # Will be calculated as 5mm for doublesided layout
    gutter: str = "0mm"

    backspace: str = "20mm"
    leftmargindistance: str = "5mm"
    leftmargin: str = "15mm"
    leftedgedistance: str = "0mm"
    leftedge: str = "0mm"

    rightmargindistance: str = "5mm"
    rightmargin: str = "15mm"
    rightedgedistance: str = "0mm"
    rightedge: str = "0mm"
    cutspace: str = "20mm"  # rightmargindistance + rightmargin + rightedgedistance + rightedge

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
    header_at_recto: list[str] = field(default_factory=list)

    # Preamble
    preamble: str | None = None

    @classmethod
    def a4(cls) -> "ContextConfig":
        """Return the configuration matching the current A4 header."""
        return cls()

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
        # Parse Front Matter
        front_matter_token = next((tok for tok in filtered if tok.type == "front_matter"), None)
        front_matter = parse_simple_yaml(front_matter_token.content) if front_matter_token else {}
        env["front_matter"] = front_matter

        page_format = _normalize_page_format(
            env.get("pdf_page_format", front_matter.get("pdf-page-format", "A4"))
        )
        pfl = page_format.lower()
        cfg = ContextConfig.a5() if page_format == "A5" else ContextConfig.a4()
        cfg.page_format = page_format

        # Override with Front Matter and environment variables if available
        for config_field in fields(cfg):
            attribute = config_field.name
            if attribute == "page_format":
                continue
            key = attribute.replace("_", "-")
            value = _front_matter_value(front_matter, key, pfl)
            if value is not None:
                setattr(cfg, attribute, _convert_value(attribute, value, cfg))
            env_key = f"pdf_{attribute}"
            value = env.get(env_key)
            if value is not None:
                setattr(cfg, attribute, _convert_value(attribute, value, cfg))

        # pdf-cutspace
        cfg.cutspace = _sum_measurements(
            cfg.rightmargindistance,
            cfg.rightmargin,
            cfg.rightedgedistance,
            cfg.rightedge,
        )
        value = _front_matter_value(front_matter, "cutspace", pfl)
        if value is not None:
            cfg.cutspace = str(value)
        if env.get("pdf_cutspace"):
            cfg.cutspace = env["pdf_cutspace"]

        # pdf-gutter
        if cfg.pagenumbering_alternative == "doublesided":
            cfg.gutter = "5mm"
        value = _front_matter_value(front_matter, "gutter", pfl)
        if value is not None:
            cfg.gutter = str(value)
        if env.get("pdf_gutter"):
            cfg.gutter = env["pdf_gutter"]

        # pdf-backspace
        cfg.backspace = _sum_measurements(
            cfg.leftmargindistance,
            cfg.leftmargin,
            cfg.leftedgedistance,
            cfg.leftedge,
        )
        value = _front_matter_value(front_matter, "backspace", pfl)
        if value is not None:
            cfg.backspace = str(value)
        if env.get("pdf_backspace"):
            cfg.backspace = env["pdf_backspace"]
        cfg.backspace = _sum_measurements(cfg.backspace, cfg.gutter)

        # pdf-preamble
        if env.get("pdf_preamble"):
            preamble_path = Path(env["pdf_preamble"]).resolve()
            cfg.preamble = str(preamble_path)
        else:
            value = _front_matter_value(front_matter, "preamble", pfl)
            if value is not None:
                preamble_path = Path(value)
                if not preamble_path.is_absolute():
                    # Relative paths are resolved relative to the source directory.
                    input_filename = env.get("input_filename", "-")
                    source_directory = (
                        Path(input_filename).resolve().parent
                        if input_filename != "-"
                        else Path.cwd()
                    )
                    preamble_path = source_directory / preamble_path
                preamble_path = preamble_path.resolve()
                if not preamble_path.is_file():
                    print(
                        f"Preamble file defined in front matter not found:\n\t{preamble_path}",
                        file=sys.stderr,
                    )
                    # raise FileNotFoundError(f"Preamble file not found: {preamble_path}")
                cfg.preamble = str(preamble_path)

        return cfg


def _front_matter_value(front_matter: dict, attribute: str, page_format: str):
    """Return a generic front-matter value, overridden by its page-specific value."""
    value = front_matter.get(f"pdf-{attribute}")
    page_specific_value = front_matter.get(f"pdf-{page_format}-{attribute}")
    return page_specific_value if page_specific_value is not None else value


VALID_PAGE_FORMATS = ("A4", "A5")


def _normalize_page_format(value: object) -> str:
    """Normalize and validate a configured page format."""
    page_format = str(value).strip().upper()
    if page_format not in VALID_PAGE_FORMATS:
        raise ValueError(f"Unsupported page format {value!r}; expected one of {VALID_PAGE_FORMATS}")
    return page_format


def _convert_value(attribute: str, value: object, cfg: ContextConfig):
    """Convert a front-matter value to the appropriate type based on the annotation in ContextConfig."""  # pylint: disable=line-too-long
    annotation = get_type_hints(type(cfg))[attribute]
    origin = get_origin(annotation)
    args = get_args(annotation)

    if annotation is bool:
        return _parse_bool(value)

    if annotation is str:
        return str(value)

    if origin is list and args == (str,):
        return _parse_header_at_recto(str(value))

    if origin in (UnionType,):
        non_none_types = [arg for arg in args if arg is not type(None)]

        if non_none_types == [int]:
            return _parse_optional_int(value)

        if non_none_types == [str]:
            return _parse_optional_str(value)

    return value


def _parse_bool(value: object) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"Expected a boolean front-matter value, got {value!r}")
    return value


def _parse_optional_int(value: object) -> int | None:
    if value is None or (isinstance(value, str) and value.lower() == "none"):
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"Expected an integer or none, got {value!r}")
    return value


def _parse_optional_str(value: object) -> str | None:
    if value is None or (isinstance(value, str) and value.lower() == "none"):
        return None
    return str(value)


VALID_HEADER_AT_RECTO_LEVELS = ("h1", "h2", "h3", "h4")
MEASUREMENT_RE = re.compile(r"^([+-]?(?:\d+(?:\.\d*)?|\.\d+))([a-zA-Z]+)$")


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


def _sum_measurements(*measurements: str) -> str:
    """Return the sum of measurements, preserving their common unit."""
    parsed = [MEASUREMENT_RE.fullmatch(measurement.strip()) for measurement in measurements]
    if any(match is None for match in parsed):
        raise ValueError(f"Invalid measurement: {measurements}")

    units = {match.group(2) for match in parsed if match is not None}
    if len(units) != 1:
        raise ValueError(f"Measurements must use the same unit: {measurements}")

    total = sum((Decimal(match.group(1)) for match in parsed if match is not None), Decimal(0))
    return f"{total:g}{units.pop()}"
