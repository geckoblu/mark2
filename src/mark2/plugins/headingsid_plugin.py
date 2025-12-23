"""Plugin for adding unique IDs to heading elements.

This module provides functionality to automatically generate and add unique IDs
to heading elements in markdown documents. The content is adapted from
mdit-py-plugins anchors_plugin.
"""

import re
from typing import Callable

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore


def headingsid_plugin(
    md: MarkdownIt,
    min_level: int = 1,
    max_level: int = 2,
    use_title_based_ids: bool = False,
    slug_func: Callable[[str], str] | None = None,
) -> None:
    """Plugin for adding header anchors with unique IDs.

    Automatically generates unique IDs for heading elements within the specified level range.

    Example:
        .. code-block:: md

            # Title String

        renders as:

        .. code-block:: html

            <h1 id="title-string">Title String</h1>

    Args:
        md: The MarkdownIt instance to register the plugin with.
        min_level: Minimum heading level to apply anchors to (1-6). Defaults to 1.
        max_level: Maximum heading level to apply anchors to (1-6). Defaults to 2.
        use_title_based_ids: If True, generates IDs based on heading titles (slugs).
                             If False, generates simple alphanumeric IDs like 'h1', 'h2', etc.
                             Defaults to True.
        slug_func: Optional custom function to convert title text to ID slug.
                   If None, uses the default slugify function.

    Note:
        The default slug function aims to mimic the GitHub Markdown format:

        - https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb
        - https://gist.github.com/asabaylus/3071099

    """
    selected_levels = list(range(min_level, max_level + 1))
    md.core.ruler.push(
        "anchor",
        _make_anchors_func(
            selected_levels,
            use_title_based_ids,
            slug_func or slugify,
        ),
    )


def _make_anchors_func(
    selected_levels: list[int],
    use_title_based_ids: bool,
    slug_func: Callable[[str], str],
) -> Callable[[StateCore], None]:
    """Create an anchor function for processing markdown tokens.

    This factory function creates a closure that processes markdown tokens
    and adds unique ID attributes to heading elements within the specified levels.

    Args:
        selected_levels: List of heading levels (1-6) to process.
        use_title_based_ids: If True, use title-based slugs. If False, use alphanumeric IDs.
        slug_func: Function to convert heading text to URL-safe slug.

    Returns:
        A function that processes StateCore and adds IDs to heading tokens.
    """

    def _anchor_func(state: StateCore) -> None:
        """Process markdown tokens and add unique IDs to headings.

        Args:
            state: The StateCore containing tokens to process.
        """
        slugs: set[str] = set()
        heading_counter = 0
        for idx, token in enumerate(state.tokens):
            if token.type != "heading_open":
                continue
            level = int(token.tag[1])
            if level not in selected_levels:
                continue

            if use_title_based_ids:
                inline_token = state.tokens[idx + 1]
                assert inline_token.children is not None
                title = "".join(
                    child.content
                    for child in inline_token.children
                    if child.type in ["text", "code_inline"]
                )
                slug = unique_slug(slug_func(title), slugs)
            else:
                heading_counter += 1
                slug = f"toc_id_{heading_counter}"

            token.attrSet("id", slug)
            # import sys
            # print(token, file=sys.stderr)

    return _anchor_func


def slugify(title: str) -> str:
    """Convert a title string to a URL-safe slug.

    Mimics GitHub's markdown slugification format by:
    - Converting to lowercase
    - Replacing spaces with hyphens
    - Removing special characters (keeping alphanumeric, CJK characters, hyphens, and spaces)

    Args:
        title: The heading title text to convert.

    Returns:
        A URL-safe slug string with spaces replaced by hyphens and special characters removed.

    Example:
        >>> slugify("Hello World!")
        'hello-world'
        >>> slugify("Test 123 & More")
        'test-123--more'
    """
    return re.sub(r"[^\w\u4e00-\u9fff\- ]", "", title.strip().lower().replace(" ", "-"))


def unique_slug(slug: str, slugs: set[str]) -> str:
    """Ensure slug uniqueness by appending a counter if needed.

    If the slug already exists in the set, appends "-1", "-2", etc. until
    a unique slug is found. The unique slug is then added to the set.

    Args:
        slug: The base slug string to make unique.
        slugs: Set of existing slugs to check against. Modified in-place
               by adding the unique slug.

    Returns:
        A unique slug string that doesn't exist in the slugs set.

    Example:
        >>> slugs = {'intro', 'intro-1'}
        >>> unique_slug('intro', slugs)
        'intro-2'
        >>> slugs
        {'intro', 'intro-1', 'intro-2'}
    """
    uniq = slug
    i = 1
    while uniq in slugs:
        uniq = f"{slug}-{i}"
        i += 1
    slugs.add(uniq)
    return uniq
