from datetime import datetime

from tdom import Node, html

from tdom_sphinx.models import TdomContext


def Footer(*, context: TdomContext) -> Node:
    """Page footer with centered copyright text.

    Uses site title from the page context if available, otherwise falls back
    to the page title. Includes the current year.
    """
    page_ctx = context.page_context
    site_title = page_ctx.get("site_title") or page_ctx.get("title") or ""
    year = datetime.now().year

    return html(
        t"""\
<footer class="container">
  <p style="text-align: center">© {year} {site_title}</p>
</footer>
"""
    )
