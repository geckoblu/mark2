CONTEXT_HEADER_A4 = r"""% !TeX program = context
% ConTeXt Mk XL (LuaMetaTeX)

%\showframe % debug layout boundaries

% -----------------------------------------------------------------------------
% Document language and page geometry
% -----------------------------------------------------------------------------
\mainlanguage[it]
\setuppapersize[A4]
\setuppagenumbering
    [alternative=doublesided,
     location={footer,inmargin},
     style=tfxx]
\setuplayout[
    topspace=15mm,
    bottomspace=15mm,
    header=5mm,
    footer=5mm,
    headerdistance=5mm,
    height=fit,
    backspace=25mm,
    rightedge=1mm,
    rightmargin=29mm,
    width=fit,
]

% -----------------------------------------------------------------------------
% Typography (main font, OpenType features, utility sizes)
% -----------------------------------------------------------------------------
\setupbodyfont[libertinus,14.4pt]
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
\setupindenting[yes, medium]
%\hyphenpenalty=5000 % stronger anti-hyphenation (kept disabled)
\pretolerance=2000
\setuptolerance[horizontal,verytolerant,stretch]

% -----------------------------------------------------------------------------
% Footnotes and outer-margin references
% -----------------------------------------------------------------------------
\setupfootnotes
    [location=page,
     n=2,
     bodyfont=11pt]
\setupnotation[footnote]
    [textcolor=black,
     color=black,
     interactioncolor=black]
\setupnote[footnote]
    [distance=-1mm,
    interaction=yes,
     textcolor=black,
     color=black,
     interactioncolor=black]
\define[1]\versenote{\dontleavehmode\footnote{#1}}
\define[1]\verseref{\inoutermargin[stack=yes,style=smallxx]{#1}}

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
