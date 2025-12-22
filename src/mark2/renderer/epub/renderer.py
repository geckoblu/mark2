"""EPUB renderer for converting Markdown to EPUB format."""

from typing import Any, Sequence
import uuid
import zipfile
import tempfile
import shutil
import sys
from pathlib import Path

from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.epub.imagesize import get_image_size
from mark2.renderer.epub.constants import (
    MIMETYPE,
    CONTAINER_XML,
    COVER_XHTML,
    CONTENT_OPF,
    TOC_NCX,
    HTML_HEAD,
    HTML_TAIL,
    DEFAULT_STYLESHEET,
)


class EPUBRenderer(RendererHTML):
    """A minimal EPUB renderer for markdown-it tokens."""

    # __output__ = "epub"

    def __init__(self, parser: Any = None):
        """Initialize the renderer.

        This renderer generates EPUB files from markdown-it tokens using HTML rendering.
        """
        super().__init__(parser)

        self.manifest = []  # Store (id, href, media-type) tuples
        self.spine = []  # Store itemref ids for content.opf
        self.guide = []  # Store guide entries for content.opf
        self.toc_entries = []  # Store (title, page_num) tuples

        self.split_at_header = "h0"

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates HTML.

        :param tokens: list on block tokens to render
        :param options: params of parser instance
        :param env: additional data from parsed input

        """
        cover = env.get("epub_cover", None)
        stylesheet = env.get("epub_stylesheet", None)
        output_filename = env.get("output_filename", "-")

        self.manifest = []
        self.manifest.append(("ncx", "toc.ncx", "application/x-dtbncx+xml"))
        self.manifest.append(("stylesheet.css", "Styles/stylesheet.css", "text/css"))

        self.spine = []
        self.guide = []

        self.toc_entries = []  # Store (title, page_num) tuples
        epubuuid = uuid.uuid4()
        basename = Path(output_filename).stem
        doctitle = basename

        pages = self.generate_content(tokens, options, env)
        toctxt = self.generate_toc()

        if stylesheet is not None:
            with open(stylesheet, "r", encoding="utf-8") as f:
                stylesheet_content = f.read()
        else:
            stylesheet_content = DEFAULT_STYLESHEET

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
                self.write_cover(epub, cover)
                # Add content
                self.write_content(epub, pages)
                # Add content.opf
                self.write_content_opf(epub, doctitle, epubuuid)
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

    def write_cover(self, epub: zipfile.ZipFile, cover: str) -> None:
        """Write cover image to the EPUB archive if provided.

        Args:
            epub: ZipFile object representing the EPUB archive
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

    def generate_content(
        self, tokens: list[Token], options: OptionsDict, env: EnvType
    ) -> list[str]:
        """Generate HTML content pages from tokens.

        Splits tokens by 'split_at_header headings and extracts all heading levels
               for TOC generation.

        Args:
            tokens: List of markdown-it tokens

        Returns:
            List of HTML page strings, one per 'split_at_header section
        """

        # Split tokens by 'split_at_header' headings and extract all headers
        chunks = []
        current_chunk = []

        for token in tokens:
            if token.type == "heading_open" and token.tag == self.split_at_header:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = []

            current_chunk.append(token)

            # Extract all heading levels for TOC
            if token.type == "heading_open" and token.tag.startswith("h"):
                level = int(token.tag[1])  # Extract level from h1, h2, etc.
                # Find the inline token that contains the heading text
                for next_token in tokens[tokens.index(token) :]:
                    if next_token.type == "inline":
                        title = next_token.content
                        self.toc_entries.append((title, len(chunks) + 1, level))
                        break
                    if next_token.type == "heading_close":
                        break

        if current_chunk:
            chunks.append(current_chunk)

        # Render each chunk
        pages = []
        for chunk in chunks:
            html = super().render(chunk, options, env)
            html = HTML_HEAD + html + HTML_TAIL
            pages.append(html)

        return pages

    def write_content(self, epub: zipfile.ZipFile, pages: list[str]) -> None:
        """Write content pages to the EPUB archive.

        Args:
            epub: ZipFile object representing the EPUB archive
            pages: List of HTML page contents
        """
        # Calculate number of digits needed based on total pages
        num_pages = len(pages)
        num_digits = len(str(num_pages))

        for i, page in enumerate(pages):
            page_num = str(i + 1).zfill(num_digits)
            page_id = f"page{page_num}"
            page_name = f"{page_id}.html"
            self.manifest.append((page_id, page_name, "application/xhtml+xml"))
            self.spine.append(page_id)
            epub.writestr(f"OEBPS/{page_name}", page)

    def write_content_opf(self, epub: zipfile.ZipFile, doctitle: str, epubuuid: uuid.UUID) -> None:
        """Write the OPF (Open Packaging Format) file to the EPUB archive.

        Args:
            epub: ZipFile object representing the EPUB archive
            title: Title of the EPUB
            epubuuid: Unique identifier for the EPUB
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
                "manifest": manifest,
                "spine": spine,
                "guide": guide,
                "epubuuid": epubuuid,
            },
        )

    def generate_toc(self) -> str:
        """Generate TOC navpoints with hierarchical structure.

        Returns:
            A string containing the navpoints for the TOC
        """
        if not self.toc_entries:
            return ""

        # Calculate number of digits needed for page numbers
        max_page = max(entry[1] for entry in self.toc_entries)
        num_digits = len(str(max_page))

        navpoints = ""
        stack = []  # Stack to track open navPoints for nesting

        for idx, (title, page_num, level) in enumerate(self.toc_entries, 1):
            page_num_str = str(page_num).zfill(num_digits)

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
{indent}  <content src="page{page_num_str}.html"/>
"""
            stack.append(level)

        # Close any remaining open navPoints
        while stack:
            stack.pop()
            indent = "    " * (len(stack) + 1)
            navpoints += f"{indent}</navPoint>\n"

        return navpoints

    ###########################################################################
    # Footnote plugin renderers
    ###########################################################################

    # Token renderers
    def footnote_ref(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render footnote reference in the text."""
        ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)

        caption: str = self.rules["footnote_caption"](tokens, idx, options, env)
        refid = ident

        if tokens[idx].meta.get("subId", -1) > 0:
            refid += ":" + str(tokens[idx].meta["subId"])

        ref = (
            f'<a href="#fn{ident}" id="fnref{refid}"><sup class="footnote-ref">{caption}</sup></a>'
        )

        # print(ref)
        return ref

    def footnote_anchor(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render back-reference link at end of footnote."""
        ident: str = self.rules["footnote_anchor_name"](tokens, idx, options, env)
        caption: str = self.rules["footnote_caption"](tokens, idx, options, env)

        if tokens[idx].meta["subId"] > 0:
            ident += ":" + str(tokens[idx].meta["subId"])

        anchor = f'<a href="#fnref{ident}" id="fn{ident}" class="footnote-backref"><sup class="footnote-backref">{caption}</sup></a>'  # pylint: disable=line-too-long

        # print(anchor)
        return anchor

    def footnote_block_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render opening of footnote block section."""
        return '<div class="notes">\n'

    def footnote_block_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render closing of footnote block section."""
        return "</div>\n"

    def footnote_open(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render opening of individual footnote item."""
        return '<div class="note">\n'

    def footnote_close(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        """Render closing of individual footnote item."""
        return "</div>\n"
