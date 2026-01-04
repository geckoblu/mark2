"""EPUB generation constants.

This module contains all constants used for EPUB file generation,
including XML templates, XHTML templates, and default stylesheets.
"""

MIMETYPE = "application/epub+zip"

DEFAULT_STYLESHEET = """h1 {
  text-indent: 0;
	text-align: center;
}

h2 {
	page-break-before: always;
  text-indent: 0;
	text-align: center;
}

p {
  margin: 0;
  text-align: justify;
  text-indent: 1em;
}

sup {
  font-size: 0.75em;
  line-height: 0;
  vertical-align: super;
}

a {
  text-decoration: None;
}

div.notes {
  margin-top: 2em;
}

div.note p {
  font-size: 0.8em;
  margin: 1em 1em 1em 2em;
  text-indent: -1em;
}
"""

CONTAINER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>"""

CONTENT_OPF = """<?xml version="1.0" encoding="utf-8"?>
<package version="2.0" unique-identifier="BookId" xmlns="http://www.idpf.org/2007/opf">
  <metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier opf:scheme="UUID" id="BookId">urn:uuid:%(epubuuid)s</dc:identifier>
    <dc:title>%(title)s</dc:title>
%(metadata)s
  </metadata>
  <manifest>
%(manifest)s
  </manifest>
  <spine toc="ncx">
%(spine)s
  </spine>
%(guide)s
</package>"""

TOC_NCX = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
   "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:%(epubuuid)s" />
    <meta name="dtb:depth" content="0" />
    <meta name="dtb:totalPageCount" content="0" />
    <meta name="dtb:maxPageNumber" content="0" />
  </head>
<docTitle>
  <text>%(title)s</text>
</docTitle>
<navMap>
%(navpoints)s</navMap>
</ncx>"""

COVER_XHTML = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Cover</title>
</head>
<body>
  <div style="text-align: center; padding: 0pt; margin: 0pt;">
    <svg xmlns="http://www.w3.org/2000/svg" height="100%%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 %(width)s %(height)s" width="100%%" xmlns:xlink="http://www.w3.org/1999/xlink">
      <image width="%(width)s" height="%(height)s" xlink:href="%(cover_name)s"/>
    </svg>
  </div>
</body>
</html>
"""

HTML_HEAD = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE htmltxt PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title></title>
<link href="Styles/stylesheet.css" rel="stylesheet" type="text/css" />
</head>
<body>

"""

HTML_TAIL = """
</body>
</html>
"""

EMPTY_TOC = """  <navPoint id="navPoint-1" playOrder="1">
    <navLabel>
      <text>Start</text>
    </navLabel>
    <content src="page001.html"/>
  </navPoint>"""
