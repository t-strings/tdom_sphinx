from tdom import Node, html

from tdom_sphinx.components.navbar import Navbar
from tdom_sphinx.models import TdomContext


def Header(*, context: TdomContext) -> Node:
    """Page header that contains the site navigation.

    Renders a PicoCSS <header> with class "is-fixed" and includes the Navbar.
    Header receives only the context and derives all props for Navbar from it.
    """
    page_ctx = context.page_context
    site_title = page_ctx.get("site_title")
    title = page_ctx.get("title")

    # Derive the brand title: prefer the site title if available, otherwise fall back to page title
    brand_title = site_title or title or ""

    # Brand href: home/root. Navbar/Brand will apply pathto to this.
    brand_href = "/"

    return html(
        t"""
<header class="is-fixed container">
  <{Navbar} brand_href={brand_href} brand_title={brand_title} context={context} />
</header>
"""
    )
