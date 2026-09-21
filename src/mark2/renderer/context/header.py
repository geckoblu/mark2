"""Programmatic composition of the ConTeXt document header from small sections.

Each ``_*_section`` function renders one logical block of the preamble from a
:class:`~mark2.renderer.context.config.ContextConfig`. :func:`build_header`
assembles them in order, so replacing the previous per-format header
constants (``header_a4.py`` / ``header_a5.py``) with a single, parametrized
implementation.
"""

from mark2.renderer.context.config import ContextConfig

HEADER_LEVEL_TO_CONTEXT_HEAD = {
    "h1": "section",
    "h2": "subsection",
    "h3": "subsubsection",
    "h4": "subsubsubsection",
}


def build_header(cfg: ContextConfig) -> str:
    """Build the full ConTeXt preamble text for the given configuration.

    Args:
        cfg: Header configuration, e.g. ``ContextConfig.a4()`` or ``ContextConfig.a5()``

    Returns:
        The ConTeXt preamble, ending with ``\\starttext``
    """
    sections = [
        _preamble_section(),
        _language_and_geometry_section(cfg),
        _typography_section(cfg),
        _colors_and_heads_section(),
        _header_at_recto_section(cfg),
        _navigation_section(),
        _paragraph_flow_section(cfg),
        _footnotes_section(cfg),
        _blockquote_section(),
        _list_section(),
        _other_sections(),
        "\\starttext\n\n",
    ]
    return "\n".join(section for section in sections if section)


def _preamble_section() -> str:
    return "% !TeX program = context\n% ConTeXt Mk XL (LuaMetaTeX)\n"


def _language_and_geometry_section(cfg: ContextConfig) -> str:
    return f"""% -----------------------------------------------------------------------------
% Document language and page geometry
% -----------------------------------------------------------------------------
\\mainlanguage[{cfg.language}]
\\setuppapersize[{cfg.page_format}]
\\setuppagenumbering
    [alternative={cfg.pagenumbering_alternative},
     location={{footer,inmargin}},
     style=tfxx]
\\setuplayout[
    topspace={cfg.topspace},
    bottomspace={cfg.bottomspace},
    header={cfg.header},
    headerdistance={cfg.headerdistance},
    footer={cfg.footer},
    footerdistance={cfg.footerdistance},
    height=fit,
    backspace={cfg.backspace},
    leftmargindistance={cfg.leftmargindistance},
    leftmargin={cfg.leftmargin},
    leftedgedistance={cfg.leftedgedistance},
    leftedge={cfg.leftedge},
    cutspace={cfg.cutspace},
    rightmargindistance={cfg.rightmargindistance},
    rightmargin={cfg.rightmargin},
    rightedgedistance={cfg.rightedgedistance},
    rightedge={cfg.rightedge},
    width=fit,
]
"""


def _typography_section(cfg: ContextConfig) -> str:
    return f"""% -----------------------------------------------------------------------------
% Typography (main font, OpenType features, utility sizes)
% -----------------------------------------------------------------------------
\\setupbodyfont[{cfg.font_name},{cfg.font_size}]
\\definefontfeature[novel-feat][default][lnum=yes,pnum=yes,liga=yes,expansion=quality]
\\setupbodyfontenvironment[default][features=novel-feat]

\\definebodyfontswitch[smallx][9pt]
\\definebodyfontswitch[smallxx][8pt]
\\definebodyfontswitch[smallxxx][6pt]
"""


def _colors_and_heads_section() -> str:
    return """% -----------------------------------------------------------------------------
% Colors and structural heads
% -----------------------------------------------------------------------------
\\definecolor[DarkRed2][x=c9211e]
\\setuphead[part,chapter,section,subsection,subsubsection][number=no]
\\definehead[booktitle][subsection][number=no,style=\\bfc,align=middle]
"""


def _navigation_section() -> str:
    return """% -----------------------------------------------------------------------------
% Navigation (PDF interaction and bookmarks)
% -----------------------------------------------------------------------------
\\setupinteraction[state=start,color=blue]
\\placebookmarks[part,chapter,section,subsection,booktitle,subsubsection][part]
"""


def _paragraph_flow_section(cfg: ContextConfig) -> str:
    return f"""% -----------------------------------------------------------------------------
% Paragraph flow and line-breaking behavior
% -----------------------------------------------------------------------------
\\setupindenting[yes, {cfg.indenting}]
\\pretolerance=2000
\\setuptolerance[horizontal,verytolerant,stretch]
"""


def _footnotes_section(cfg: ContextConfig) -> str:
    footnote_opts = ["location=page"]
    if cfg.footnote_columns is not None:
        footnote_opts.append(f"n={cfg.footnote_columns}")
    footnote_opts.append(f"bodyfont={cfg.footnote_bodyfont}")
    footnote_opts_text = ",\n     ".join(footnote_opts)

    note_opts = []
    if cfg.footnote_distance is not None:
        note_opts.append(f"distance={cfg.footnote_distance}")
    note_opts += ["interaction=yes", "textcolor=black", "color=black", "interactioncolor=black"]
    note_opts_text = ",\n     ".join(note_opts)

    section = f"""% -----------------------------------------------------------------------------
% Footnotes and outer-margin references
% -----------------------------------------------------------------------------
\\setupfootnotes
    [{footnote_opts_text}]
\\setupnotation[footnote]
    [textcolor=black,
     color=black,
     interactioncolor=black]
\\setupnote[footnote]
    [{note_opts_text}]
"""
    if cfg.define_verse_helpers:
        section += (
            "\\define[1]\\versenote{\\dontleavehmode\\footnote{#1}}\n"
            "\\define[1]\\verseref{\\inoutermargin[stack=yes,style=smallxx]{#1}}\n"
        )
    return section


def _blockquote_section() -> str:
    return """% -----------------------------------------------------------------------------
% Block quote environment
% -----------------------------------------------------------------------------
\\definestartstop[Blockquote]
[
    before={\\blank[halfline]\\bgroup\\noindentation\\startnarrower[2*left]},
    after={\\stopnarrower\\egroup\\blank[halfline]},
]
"""


def _list_section() -> str:
    return """% -------------------------------------------------
% List formatting
% -------------------------------------------------
\\setupitemize[each][inbetween={\\blank[none]},margin=1cm]
"""


def _header_at_recto_section(cfg: ContextConfig) -> str:
    """Force the configured heading levels to start on a recto (right-hand) page."""
    if not cfg.header_at_recto:
        return ""
    heads = ",".join(HEADER_LEVEL_TO_CONTEXT_HEAD[level] for level in cfg.header_at_recto)
    return f"\\setuphead[{heads}][page=right]\n"


def _other_sections() -> str:
    """Other miscellaneous sections."""
    return """
% Superscript formatting
\\define[1]\\Sup{%
    \\dontleavehmode
    \\hbox{\\raise0.9ex\\hbox{{\\smallxx\\strut #1}}}%
}

% Subscript formatting
\\define[1]\\Sub{%
    \\dontleavehmode
    \\hbox{\\lower0.3ex\\hbox{{\\smallxx\\strut #1}}}%

% -----------------------------------------------------------------------------
% Project-specific section
% -----------------------------------------------------------------------------

% For Bibleprj project: Verse number formatting
\\define[1]\\versenumber{%
    \\dontleavehmode
    \\hbox{\\raise0.9ex\\hbox{{\\smallxx \\strut #1}}}%
    \\kern .2em
    \\nobreak
    \\ignorespaces
}
"""
