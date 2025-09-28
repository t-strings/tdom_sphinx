from datetime import datetime

from tdom import Node, html

from tdom_sphinx.models import PageContext, SiteConfig


def Footer(*, site_config: SiteConfig, page_context: PageContext) -> Node:
    """Page footer with centered copyright text.

    Prefers explicit site_title, then page title. Includes the current year.
    """

    # Prefer explicit site_title, then page title
    site_title = getattr(site_config, "site_title", None)

    title = getattr(page_context, "title", None)
    if title is None and isinstance(page_context, dict):
        title = page_context.get("title")

    site_title = site_title or title or ""

    year = datetime.now().year

    return html(
        t"""\
<footer class="container">
  <p style="text-align: center">© {year} {site_title}</p>
</footer>
"""
    )
