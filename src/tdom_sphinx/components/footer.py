from datetime import datetime

from tdom import Node, html

from tdom_sphinx.models import PageContext, SiteConfig


def Footer(*, site_config: SiteConfig, page_context: PageContext) -> Node:
    """Page footer with centered copyright text.

    Gets site_title directly from site_config attribute.
    Includes the current year.
    """

    # Get site_title directly from site_config attribute
    site_title = site_config.site_title

    year = datetime.now().year

    return html(
        t"""\
<footer class="container">
  <p style="text-align: center">© {year} {site_title}</p>
</footer>
"""
    )
