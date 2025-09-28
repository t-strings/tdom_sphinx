from pathlib import PurePosixPath

from tdom import Node, html

from tdom_sphinx.models import PageContext, SiteConfig
from tdom_sphinx.url import relative_tree


def make_full_title(
    *, page_context: PageContext, site_config: SiteConfig | None
) -> str:
    """Return the full <title> text for a page.

    Gets title directly from page_context and site_title directly from site_config.
    If site_config is provided, appends it with a hyphen separator after the page title.
    """
    # Get title directly from page_context attribute
    title = page_context.title

    # Get site_title directly from site_config attribute if provided
    if site_config is not None:
        site_title = site_config.site_title
        return f"{title} - {site_title}"
    else:
        return f"{title}"


def Head(*, page_context: PageContext, site_config: SiteConfig | None = None) -> Node:
    # Generate the full title using page context and site config
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
