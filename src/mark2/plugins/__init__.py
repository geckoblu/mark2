"""Plugins package for mark2 - provides custom markdown-it plugins.

This package contains custom plugins that extend markdown-it functionality,
including footnote handling, heading ID generation, and YAML frontmatter parsing.
"""

from mark2.plugins.container_plugin import container_plugin

# from mark2.plugins.footnote_plugin import footnote_tail
from mark2.plugins.headingsid_plugin import headingsid_plugin
from mark2.plugins.myst_role_plugin import myst_role_plugin
from mark2.plugins.pagebreak_plugin import pagebreak_plugin
from mark2.plugins.sup_plugin import sup_plugin

__all__ = [
    "container_plugin",
    # "footnote_tail",
    "headingsid_plugin",
    "myst_role_plugin",
    "pagebreak_plugin",
    "sup_plugin",
]
