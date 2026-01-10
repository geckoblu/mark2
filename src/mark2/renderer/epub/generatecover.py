"""
SVG cover image generator for EPUB books.

This module provides functionality to generate SVG cover images with
automatically scaled title and author text that fits within the page bounds.
"""


def generate_cover(title: str, author: str, width: int = 800, height: int = 1200) -> str:
    """
    Generate an SVG cover image with centered title and author.

    Args:
        title: Book title (can contain \\n for line breaks)
        author: Author name (can contain \\n for line breaks)
        width: Cover width in pixels (default: 800)
        height: Cover height in pixels (default: 1200)

    Returns:
        SVG string representation of the cover
    """
    # Split title and author by line breaks
    title_lines = title.split("\n")
    author_lines = author.split("\n")

    # Calculate font sizes with automatic scaling to fit width
    # Use 98% of width to leave margins
    max_text_width = width * 0.95

    # Initial font sizes
    title_font_size = 72

    # Adjust title font size to fit
    title_font_size = _calculate_font_size(title_lines, title_font_size, max_text_width, bold=True)

    # Author font size relative to title
    author_font_size = min(30, title_font_size // 1.5)
    # Adjust author font size to fit
    author_font_size = _calculate_font_size(
        author_lines, author_font_size, max_text_width, bold=False
    )

    # Calculate vertical positions
    # Start title at 1/3 of height
    title_start_y = height // 3
    line_height_title = title_font_size * 1.2
    line_height_author = author_font_size * 1.2

    # Author positioned below title with some spacing
    author_start_y = title_start_y + (len(title_lines) * line_height_title) + 100

    # Build SVG
    svg_parts = [
        #'<!--?xml version="1.0" encoding="UTF-8"?-->',
        # f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',  # pylint: disable=line-too-long
        f'<svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 {width} {height}" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">',  # pylint: disable=line-too-long
        # Background
        f'  <rect width="{width}" height="{height}" fill="#f5f5f5"/>',
    ]

    # Add title lines
    for i, line in enumerate(title_lines):
        y_pos = title_start_y + (i * line_height_title)
        svg_parts.append(
            f'  <text x="{width // 2}" y="{y_pos}" '
            f'font-family="serif" font-size="{title_font_size}" font-weight="bold" '
            f'text-anchor="middle" fill="#333333">{escape_xml(line)}</text>'
        )

    # Add author lines
    for i, line in enumerate(author_lines):
        y_pos = author_start_y + (i * line_height_author)
        svg_parts.append(
            f'  <text x="{width // 2}" y="{y_pos}" '
            f'font-family="serif" font-size="{author_font_size}" '
            f'text-anchor="middle" fill="#666666">{escape_xml(line)}</text>'
        )

    svg_parts.append("</svg>")

    return "\n".join(svg_parts)


def _calculate_font_size(
    lines: list[str], initial_size: int, max_width: float, bold: bool = False
) -> int:
    """
    Calculate appropriate font size to fit text within max_width.

    Args:
        lines: List of text lines
        initial_size: Starting font size
        max_width: Maximum width in pixels
        bold: Whether text is bold (affects width estimation)

    Returns:
        Adjusted font size
    """
    if not lines:
        return initial_size

    # Find the longest line
    longest_line = max(lines, key=len)

    # Estimate character width (bold text is ~10% wider)
    char_width_factor = 0.55 if bold else 0.5

    font_size = initial_size
    estimated_width = len(longest_line) * font_size * char_width_factor

    # Reduce font size if text is too wide
    min_font_size = 20  # Don't go below this
    while estimated_width > max_width and font_size > min_font_size:
        font_size -= 2
        estimated_width = len(longest_line) * font_size * char_width_factor

    return font_size


def escape_xml(text: str) -> str:
    """Escape special XML characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


# Just for testing the function
if __name__ == "__main__":
    SVGCOVER = generate_cover("My Great\nBook Title", "John Doe")
    # SVGCOVER = generate_cover(
    #     "Fede, ragione e università. Ricordi e riflessioni.",
    #     "Joseph Ratzinger\n(papa Benedetto XVI)",
    # )
    print(SVGCOVER)
    with open("cover.svg", "w", encoding="utf-8") as f:
        f.write(SVGCOVER)
