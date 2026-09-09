CONTEXT_HEADER_A5 = r"""% !TeX program = context
% ConTeXt Mk XL (LuaMetaTeX)

%\showframe % debug layout boundaries

% -----------------------------------------------------------------------------
% Document language and page geometry
% -----------------------------------------------------------------------------
\mainlanguage[it]
\setuppapersize[A5]
\setuppagenumbering
    [alternative=singlesided,
     location={footer,inmargin},
     style=tfxx]
\setuplayout[
    topspace=5mm,
    bottomspace=5mm,
    header=5mm,
    footer=5mm,
    headerdistance=5mm,
    height=fit,
    backspace=5mm,
    rightedge=1mm,
    rightmargin=12mm,
    width=fit,
]

% -----------------------------------------------------------------------------
% Typography (main font, OpenType features, utility sizes)
% -----------------------------------------------------------------------------
\setupbodyfont[liberation,12pt]
\definefontfeature[novel-feat][default][lnum=yes,pnum=yes,liga=yes,expansion=quality]
\setupbodyfontenvironment[default][features=novel-feat]

\definebodyfontswitch[smallx][9pt]
\definebodyfontswitch[smallxx][8pt]
\definebodyfontswitch[smallxxx][6pt]

% -----------------------------------------------------------------------------
% Colors and structural heads
% -----------------------------------------------------------------------------
\definecolor[DarkRed2][x=c9211e]
\setuphead[part,chapter,section,subsection,subsubsection][number=no]
\definehead[booktitle][subsection][number=no,style=\bfc,align=middle]

% -----------------------------------------------------------------------------
% Navigation (PDF interaction and bookmarks)
% -----------------------------------------------------------------------------
\setupinteraction[state=start]
\placebookmarks[part,chapter,section,subsection,booktitle,subsubsection][part]

% -----------------------------------------------------------------------------
% Paragraph flow and line-breaking behavior
% -----------------------------------------------------------------------------
\setupindenting[yes, small]
%\hyphenpenalty=5000 % stronger anti-hyphenation (kept disabled)
\pretolerance=2000
\setuptolerance[horizontal,verytolerant,stretch]

% -----------------------------------------------------------------------------
% Footnotes and outer-margin references
% -----------------------------------------------------------------------------
\setupfootnotes
    [location=page,
     bodyfont=9pt]
\setupnotation[footnote]
    [textcolor=black,
     color=black,
     interactioncolor=black]
\setupnote[footnote]
    [interaction=yes,
     textcolor=black,
     color=black,
     interactioncolor=black]

% -----------------------------------------------------------------------------
% Block quote environment
% -----------------------------------------------------------------------------
\definestartstop[Blockquote]
[
    before={\blank[halfline]\bgroup\noindentation\startnarrower[2*left]},
    after={\stopnarrower\egroup\blank[halfline]},
]
% -------------------------------------------------
% List formatting
% -------------------------------------------------
\setupitemize[each][inbetween={\blank[none]},margin=1cm]

\starttext

"""


# \char"200B % zero-width space (for debugging)
