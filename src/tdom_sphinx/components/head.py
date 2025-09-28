from pathlib import PurePosixPath
from typing import Any

from tdom import Node, html

from tdom_sphinx.models import PageContext, SiteConfig
from tdom_sphinx.url import relative_tree


def make_full_title(
    *, page_context: PageContext | dict[str, Any], site_config: SiteConfig | None
) -> str:
    """Return the full <title> text for a page.

    - If a SiteConfig with a site_title is provided, append it with a hyphen
      separator after the page title (e.g., "Page - Site").
    - Page title is taken from PageContext.title or from a dict-like page_context
      under the "title" key.
    """
    site_title = None if site_config is None else site_config.site_title

    # Page title from PageContext or dict
    title = getattr(page_context, "title", None)
    if title is None and isinstance(page_context, dict):
        title = page_context.get("title")

    return f"{title}" if site_title is None else f"{title} - {site_title}"


def Head(*, page_context: PageContext, site_config: SiteConfig | None = None) -> Node:
    # Support both typed PageContext and dict-style contexts
    full_title = make_full_title(page_context=page_context, site_config=site_config)

    result = html(t"""
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{full_title}</title>
  <link rel="stylesheet" href="/_static/tdom-sphinx.css" />
  <link rel="stylesheet" href="/_static/pico.css" />
  <link rel="stylesheet" href="/_static/sphinx.css" />
  <link rel="stylesheet" href="/_static/pygments.css" />
  <link rel="icon" href="/_static/favicon.ico"  type="image/x-icon" />
</head>  
""")
    relative_tree(result, PurePosixPath("/" + page_context.pagename))
    return result
