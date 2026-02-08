"""
HTML frontpage generator for EPUB books.

This module provides functionality to generate HTML frontpages with
title and author text for EPUB documents.
"""


def generate_frontpage(title: str, author: str) -> str:
    """
    Generate an HTML frontpage with centered title and author.

    Args:
        title: Book title (can contain \\n for line breaks)
        author: Author name (can contain \\n for line breaks)

    Returns:
        HTML string representation of the frontpage
    """
    # Split title and author by line breaks and convert to HTML
    title_lines = title.split("\n")
    author_lines = author.split("\n")

    # Build title HTML
    title_html = "<br/>".join(escape_html(line) for line in title_lines)

    # Build author HTML
    author_html = "<br/>".join(escape_html(line) for line in author_lines)

    # Build complete HTML
    html = f"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8"/>
    <title>{escape_html(title_lines[0] if title_lines else "")}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            text-align: center;
            font-family: serif;
            background-color: #f5f5f5;
        }}
        .title {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 3em 0 1.5em 0;
            line-height: 1.3;
        }}
        .author {{
            font-size: 1.5em;
            line-height: 1.4;
        }}
    </style>
</head>
<body>
    <div class="frontpage">
        <div class="title">{title_html}</div>
        <div class="author">{author_html}</div>
    </div>
</body>
</html>"""

    return html


def escape_html(text: str) -> str:
    """Escape special HTML characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


# Just for testing the function
if __name__ == "__main__":
    HTML_FRONTPAGE = generate_frontpage("My Great\nBook Title", "John Doe")
    # HTML_FRONTPAGE = generate_frontpage(
    #     "Fede, ragione e università. Ricordi e riflessioni.",
    #     "Joseph Ratzinger\n(papa Benedetto XVI)",
    # )
    print(HTML_FRONTPAGE)
    with open("frontpage.html", "w", encoding="utf-8") as f:
        f.write(HTML_FRONTPAGE)
