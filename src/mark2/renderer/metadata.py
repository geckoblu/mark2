"""Document metadata shared by output renderers."""

from pathlib import Path

from markdown_it.utils import EnvType


def get_document_metadata(env: EnvType) -> tuple[str, str]:
    """Return the document title and author from the rendering environment."""
    frontmatter = env.get("front_matter", {})
    title = frontmatter.get("title", Path(env.get("output_filename", "-")).stem)
    author = frontmatter.get("author", "")
    return str(title), str(author)
