"""EPUB renderer for converting Markdown to EPUB format."""

import html
import shutil
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import Any, Sequence

from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.rendererhtml import RendererHTML
from mark2.renderer.epub.generatecover import generate_cover as generatecover
from mark2.renderer.epub.imagesize import get_image_size
from mark2.renderer.epub.constants import (
    MIMETYPE,
    CONTAINER_XML,
    COVER_XHTML,
    COVER_XHTML_GENERATED,
    CONTENT_OPF,
    TOC_NCX,
    EMPTY_TOC,
    HTML_HEAD,
    HTML_TAIL,
    DEFAULT_STYLESHEET,
)


class EPUBRenderer(RendererHTML):
    """A minimal EPUB renderer for markdown-it tokens."""

    manifest: list[tuple[str, str, str]]  # Store (id, href, media-type) tuples
    spine: list[str]  # Store itemref ids for content.opf
    guide: list[tuple[str, str, str]]  # Store guide entries for content.opf
    toc_entries: list[tuple[str, str, int, str]]  # Store (title, page_id, level, toc_id)
    split_at_header: str  # Header tag to split content into separate pages
    footnote_ref_pages: dict[str, str]  # Map footnote_id -> page_id
    current_page_id: str  # Track the current page ID

    def __init__(self, parser: Any = None) -> None:
        """Initialize the renderer.

        This renderer generates EPUB files from markdown-it tokens using HTML rendering.

        Args:
            parser: Optional parser instance
        """
        super().__init__(parser)

        self.debug = False  # Enable debug logging if needed

        self.manifest = []  # Store (id, href, media-type) tuples
        self.spine = []  # Store itemref ids for content.opf
        self.guide = []  # Store guide entries for content.opf
        self.toc_entries = []  # Store (title, page_num, level, toc_id) tuples for hierarchical TOC
        self.footnote_ref_pages = {}  # Track which page each footnote reference is on

        self.split_at_header = "h2"

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates EPUB file.

        :param tokens: list of block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input

        """
        cover = env.get("epub_cover", None)
        generate_cover = env.get("epub_generatecover", False)
        stylesheet = env.get("epub_stylesheet", None)
        keep_stylesheet = env.get("epub_keepstylesheet", False)
        output_filename = env.get("output_filename", "-")

        self.debug = env.get("debug", False)
        self.split_at_header = env.get("epub_split_at_header", "h2")

        self.manifest = []
        self.manifest.append(("ncx", "toc.ncx", "application/x-dtbncx+xml"))
        self.manifest.append(("stylesheet.css", "Styles/stylesheet.css", "text/css"))

        self.spine = []
        self.guide = []

        self.toc_entries = []  # Store (title, page_num, level, toc_id)
        self.footnote_ref_pages = {}  # Map footnote_id -> page_id
        self.current_page_id = ""  # Track the current page ID

        epubuuid = uuid.uuid4()

        pages = self._generate_content(tokens, options, env)
        toctxt = self._generate_toc()

        if stylesheet is not None:
            with open(stylesheet, "r", encoding="utf-8") as f:
                stylesheet_content = f.read()
        elif keep_stylesheet:
            stylesheet_content = self._read_stylesheet_from_existing_epub(output_filename)
            if stylesheet_content is None:
                stylesheet_content = DEFAULT_STYLESHEET
        else:
            stylesheet_content = DEFAULT_STYLESHEET

        doctitle, author, metadata = self._generate_metadata(env)

        # Write EPUB to a temporary file first
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".epub", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            with zipfile.ZipFile(tmp_path, "w") as epub:
                # Add mimetype file
                epub.writestr("mimetype", MIMETYPE)
                # Add META-INF/container.xml
                epub.writestr("META-INF/container.xml", CONTAINER_XML)
                # Add cover image if provided
                if cover is not None:
                    self._write_cover(epub, cover)
                elif generate_cover:
                    self._generate_cover(epub, doctitle, author)
                # Add content
                self._write_content(epub, pages)
                # Add content.opf
                self._write_content_opf(epub, doctitle, epubuuid, metadata)
                # Add toc.ncx
                epub.writestr(
                    "OEBPS/toc.ncx",
                    TOC_NCX % {"title": doctitle, "navpoints": toctxt, "epubuuid": epubuuid},
                )
                # Add stylesheet
                epub.writestr("OEBPS/Styles/stylesheet.css", stylesheet_content)

            # Write to final destination
            if output_filename == "-":
                with open(tmp_path, "rb") as f:
                    sys.stdout.buffer.write(f.read())
            else:
                shutil.copy(tmp_path, output_filename)
        finally:
            # Clean up temporary file
            Path(tmp_path).unlink(missing_ok=True)

    def _read_stylesheet_from_existing_epub(self, epub_path: str) -> str | None:
        """Read existing stylesheet from an EPUB file if it exists.

        Args:
            epub_path: Path to the existing EPUB file
        Returns:
            The content of the existing stylesheet if found, otherwise None
        """
        if not Path(epub_path).is_file():
            return None

        try:
            with zipfile.ZipFile(epub_path, "r") as epub:
                for item in epub.infolist():
                    if item.filename.endswith("stylesheet.css"):
                        with epub.open(item) as f:
                            if self.debug:
                                print(f"Found existing stylesheet in {epub_path}, reusing it.")
                            return f.read().decode("utf-8")
        except zipfile.BadZipFile:
            # Not a valid ZIP file, ignore and return None
            pass

        return None

    def _write_cover(self, epub: zipfile.ZipFile, cover: str | None) -> None:
        """Write cover image to the EPUB archive if provided.

        Args:
            epub: ZipFile object representing the EPUB archive
            cover: Path to the cover image file, or None if no cover
        """
        if cover is not None:
            cover_path = Path(cover)
            if cover_path.is_file():
                cover_id = "cover"
                cover_name = "cover" + cover_path.suffix.lower()
                media_type = {
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".png": "image/png",
                    ".gif": "image/gif",
                }.get(cover_path.suffix.lower(), "application/octet-stream")

                self.manifest.append((cover_id, cover_name, media_type))
                self.guide.append(("cover", "Cover", "cover.xhtml"))

                with open(cover_path, "rb") as f:
                    epub.writestr(f"OEBPS/{cover_name}", f.read())

                width, height = get_image_size(cover_path)
                epub.writestr(
                    "OEBPS/cover.xhtml",
                    COVER_XHTML % {"width": width, "height": height, "cover_name": cover_name},
                )
                self.manifest.append(("cover.xhtml", "cover.xhtml", "application/xhtml+xml"))
                self.spine.insert(0, "cover.xhtml")

    def _generate_cover(self, epub: zipfile.ZipFile, doctitle, author: str) -> None:
        """Generate a simple SVG cover page and add it to the EPUB archive.
        Args:
            epub: ZipFile object representing the EPUB archive
            doctitle: Title of the EPUB
            author: Author of the EPUB
        """
        svgcover = generatecover(doctitle, author)
        epub.writestr(
            "OEBPS/cover.xhtml",
            COVER_XHTML_GENERATED % {"svgcover": svgcover},
        )
        self.manifest.append(("cover.xhtml", "cover.xhtml", "application/xhtml+xml"))
        self.spine.insert(0, "cover.xhtml")

    def _generate_content(
        self, tokens: list[Token], options: OptionsDict, env: EnvType
    ) -> list[tuple[str, str]]:
        """Generate HTML content pages from tokens.

        Splits tokens by 'split_at_header' headings and extracts all heading levels
        for TOC generation.

        Args:
            tokens: List of markdown-it tokens
            options: Parser instance parameters
            env: Additional data from parsed input

        Returns:
            List of tuples (page_id, HTML content), one per 'split_at_header' section
        """

        # Split tokens by 'split_at_header' headings and extract all headers
        chunks = []
        current_chunk = []

        num_digits = 3
        page_number = 1
        page_id = f"page{str(page_number).zfill(num_digits)}"

        for token in tokens:
            if token.type == "pagebreak":
                if current_chunk:
                    chunks.append((page_id, current_chunk))
                    current_chunk = []
                    page_number += 1
                    page_id = f"page{str(page_number).zfill(num_digits)}"
                continue

            if token.type == "heading_open" and token.tag == self.split_at_header:
                if current_chunk:
                    chunks.append((page_id, current_chunk))
                    current_chunk = []
                    page_number += 1
                    page_id = f"page{str(page_number).zfill(num_digits)}"

            if token.type == "footnote_block_open":
                chunks.append((page_id, current_chunk))
                current_chunk = []
                page_number += 1
                page_id = "notes"

                self._create_notes_header(page_id, current_chunk)

            current_chunk.append(token)

            # Extract all heading levels for TOC
            if token.type == "heading_open" and token.tag.startswith("h"):
                self._add_header_to_toc(token, tokens, page_id)

        if current_chunk:
            chunks.append((page_id, current_chunk))

        # Render each chunk
        pages = []
        for page_id, chunk in chunks:
            self.current_page_id = page_id
            body = super().render(chunk, options, env)
            body = body.replace("\xa0", "&#160;")
            body = HTML_HEAD + body + HTML_TAIL
            pages.append((page_id, body))

        return pages

    def _extract_text_from_token(self, token: Token) -> str:
        """Recursively extract plain text from a token and its children.

        Walks through the token tree and concatenates all text content,
        stripping out any formatting markup.

        Args:
            token: The token to extract text from

        Returns:
            Plain text content without formatting tags
        """
        text_parts = []

        if token.type == "text":
            text_parts.append(token.content)
        elif token.type == "myst_role":
            # Handle MyST roles if needed
            name = token.meta.get("name")
            if name == "line-break":
                text_parts.append(" ")

        if token.children:
            for child in token.children:
                text_parts.append(self._extract_text_from_token(child))

        return "".join(text_parts)

    def _add_header_to_toc(self, token: Token, tokens: Sequence[Token], page_id: str) -> None:
        """Add a heading token to the table of contents entries.

        Extracts the heading level, text content, and ID from the token and adds it
        to the TOC entries list for later use in generating the EPUB navigation.

        Args:
            token: The heading_open token to process
            tokens: Complete sequence of tokens to search for the heading text
            page_id: Identifier of the page containing this heading

        Returns:
            None. Modifies self.toc_entries in place.
        """
        if token.type != "heading_open":
            return

        level = int(token.tag[1])  # Extract level from h1, h2, etc.
        # Find the inline token that contains the heading text
        for next_token in tokens[tokens.index(token) :]:
            if next_token.type == "inline":
                title = self._extract_text_from_token(next_token)
                toc_id = token.attrGet("id") or ""
                self.toc_entries.append((title, page_id, level, toc_id))
                break
            if next_token.type == "heading_close":
                break

    def _create_notes_header(self, page_id: str, current_chunk: list[Token]) -> None:
        """
        Create a "Note" header section and add it to the table of contents.

        This method generates heading tokens for a notes section, appends them to the
        current chunk, and registers the header in the table of contents.

        Args:
            page_id (str): The identifier for the current page.
            current_chunk (list): A list of tokens representing the current document chunk
                                    to which the header tokens will be appended.

        Returns:
            None

        Side Effects:
            - Appends three tokens (heading_open, inline, heading_close) to current_chunk
            - Adds the header to the table of contents via add_header_to_toc
        """
        tk_open = Token(type="heading_open", tag="h2", nesting=1, attrs={"id": "toc_id_1"})
        current_chunk.append(tk_open)

        # Create inline token with text as child, following markdown-it pattern
        tk_text = Token(type="text", tag="", nesting=0, content="Note")
        tk_inline = Token(type="inline", tag="", nesting=0, content="Note", children=[tk_text])
        current_chunk.append(tk_inline)

        tk_close = Token(type="heading_close", tag="h2", nesting=-1)
        current_chunk.append(tk_close)
        self._add_header_to_toc(tk_open, current_chunk, page_id)

    def _write_content(self, epub: zipfile.ZipFile, pages: list[tuple[str, str]]) -> None:
        """Write content pages to the EPUB archive.

        Args:
            epub: ZipFile object representing the EPUB archive
            pages: List of tuples containing (page_id, HTML content)
        """
        for page_id, page in pages:
            page_name = f"{page_id}.html"
            self.manifest.append((page_id, page_name, "application/xhtml+xml"))
            self.spine.append(page_id)
            epub.writestr(f"OEBPS/{page_name}", page)

    def _write_content_opf(
        self, epub: zipfile.ZipFile, doctitle: str, epubuuid: uuid.UUID, metadata: str
    ) -> None:
        """Write the OPF (Open Packaging Format) file to the EPUB archive.

        Args:
            epub: ZipFile object representing the EPUB archive
            doctitle: Title of the EPUB
            epubuuid: Unique identifier for the EPUB
            metadata: Additional metadata for the EPUB
        """

        manifest = "\n".join(
            f'    <item id="{item_id}" href="{href}" media-type="{media_type}"/>'
            for item_id, href, media_type in self.manifest
        )

        spine = "\n".join(f'    <itemref idref="{item_id}"/>' for item_id in self.spine)

        if len(self.guide) > 0:
            guide = "  <guide>\n"
            for type_, title, href in self.guide:
                guide += f'    <reference type="{type_}" title="{title}" href="{href}"/>\n'
            guide += "  </guide>\n"
        else:
            guide = ""

        epub.writestr(
            "OEBPS/content.opf",
            CONTENT_OPF
            % {
                "title": doctitle,
                "metadata": metadata,
                "manifest": manifest,
                "spine": spine,
                "guide": guide,
                "epubuuid": epubuuid,
            },
        )

    def _generate_toc(self) -> str:
        """Generate TOC navpoints with hierarchical structure.

        Creates a nested navigation structure for the EPUB table of contents based on
        heading levels. If no TOC entries exist (document has no headings), returns
        an empty string to generate a valid but empty TOC.

        Returns:
            A string containing the hierarchical navPoint XML elements for the NCX TOC.
            Returns empty string if no headings were found in the document.
        """
        # Return a default empty TOC if no headings were extracted from the document
        if not self.toc_entries:
            return EMPTY_TOC

        navpoints = ""
        stack = []  # Stack to track open navPoints for nesting

        for idx, (title, page_id, level, toc_id) in enumerate(self.toc_entries, 1):

            # Close navPoints that are at same or deeper level
            while stack and stack[-1] >= level:
                stack.pop()
                navpoints += "    " * (len(stack) + 1) + "</navPoint>\n"

            # Add current navPoint
            indent = "    " * (len(stack) + 1)
            navpoints += f"""{indent}<navPoint id="navPoint-{idx}" playOrder="{idx}">
{indent}  <navLabel>
{indent}    <text>{title}</text>
{indent}  </navLabel>
{indent}  <content src="{page_id}.html#{toc_id}"/>
"""
            stack.append(level)

        # Close any remaining open navPoints
        while stack:
            stack.pop()
            indent = "    " * (len(stack) + 1)
            navpoints += f"{indent}</navPoint>\n"

        return navpoints

    def _generate_metadata(self, env: EnvType) -> tuple[str, str, str]:
        """Generate EPUB metadata from front matter.

        Args:
            env: Environment dictionary containing front matter and output settings

        Returns:
            A tuple containing:
            - The document title
            - The author name
            - A string with additional metadata XML entries
        """
        frontmatter = env.get("front_matter", {})

        doctitle = frontmatter.get("title", Path(env.get("output_filename", "-")).stem)
        author = ""

        metadata_entries = []

        # Author
        if "author" in frontmatter:
            author = frontmatter["author"]
            parts = author.split()
            if len(parts) == 2:
                # Format: NAME SURNAME -> add opf:file-as="SURNAME, NAME"
                file_as = f"{parts[1]}, {parts[0]}"
                metadata_entries.append(
                    f'    <dc:creator opf:role="aut" opf:file-as="{file_as}">{author}</dc:creator>'
                )
            else:
                # No file-as attribute for non-standard name formats
                metadata_entries.append(f'    <dc:creator opf:role="aut">{author}</dc:creator>')

        # Language
        language = frontmatter.get("language") or "it"
        metadata_entries.append(f"    <dc:language>{language}</dc:language>")

        # Publisher
        if "publisher" in frontmatter:
            metadata_entries.append(f'    <dc:publisher>{frontmatter["publisher"]}</dc:publisher>')

        # Date
        if "date" in frontmatter:
            metadata_entries.append(
                f'    <dc:date xmlns:opf="http://www.idpf.org/2007/opf" opf:event="publication">{frontmatter["date"]}</dc:date>'  # pylint: disable=line-too-long
            )
        today = __import__("datetime").datetime.today().strftime("%Y-%m-%d")
        metadata_entries.append(
            f'    <dc:date xmlns:opf="http://www.idpf.org/2007/opf" opf:event="modification">{today}</dc:date>'  # pylint: disable=line-too-long
        )

        # ID
        if "id" in frontmatter:
            id_value = frontmatter["id"]
            # Split format like "ISBN<9788831550420>" into scheme and value
            if "<" in id_value and ">" in id_value:
                scheme = id_value.split("<")[0]
                value = id_value.split("<")[1].rstrip(">")
            else:
                # Fallback to UUID scheme if format doesn't match
                scheme = "UUID"
                value = id_value
            metadata_entries.append(
                f'    <dc:identifier opf:scheme="{scheme}">{value}</dc:identifier>'  # pylint: disable=line-too-long
            )

        # Subject
        if "subject" in frontmatter:
            subjects: str = frontmatter["subject"]
            for subject in subjects.split(","):
                subject = subject.strip()
                metadata_entries.append(f"    <dc:subject>{subject}</dc:subject>")

        # Description
        if "description" in frontmatter:
            description: str = frontmatter["description"]
            # Parse markdown and convert to HTML
            md = MarkdownIt()
            description = md.render(description).strip()
            # Remove wrapping <p> tags if present
            if description.startswith("<p>") and description.endswith("</p>"):
                description = description[3:-4]
            description = html.escape(description, quote=True)
            metadata_entries.append(f"    <dc:description>{description}</dc:description>")

        metadata_str = "\n".join(metadata_entries)

        return doctitle, author, metadata_str

    ###########################################################################
    # footnote_plugin renderers
    ###########################################################################

    def footnote_ref(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render footnote reference in the text."""
        caption: str = self.rules["footnote_caption"](tokens, idx, options, env)

        ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)

        refid = ident
        if tokens[idx].meta.get("subId", -1) > 0:
            refid += ":" + str(tokens[idx].meta["subId"])

        self.footnote_ref_pages[refid] = self.current_page_id

        ref = (
            f'<a href="notes.html#fn{ident}" id="fnref{refid}">'
            + f'<sup class="footnote-ref">{caption}</sup></a>'
        )

        # print(ref)
        return ref

    def footnote_anchor(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render back-reference link at end of footnote."""
        caption: str = self.rules["footnote_caption"](tokens, idx, options, env)

        ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)

        refid = ident
        if tokens[idx].meta.get("subId", -1) > 0:
            refid += ":" + str(tokens[idx].meta["subId"])

        # Get the page_id where this footnote was referenced
        page_id = self.footnote_ref_pages.get(refid, "---")

        anchor = (
            f'<a href="{page_id}.html#fnref{ident}" id="fn{ident}" class="footnote-backref">'
            + f'<sup class="footnote-backref">{caption}</sup></a>&#160;'
        )

        return anchor
