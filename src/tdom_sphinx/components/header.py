from tdom import Node, html

from tdom_sphinx.components.navbar import Navbar
from tdom_sphinx.models import NavbarConfig, PageContext, SiteConfig


def Header(
    *,
    page_context: PageContext,
    navbar: NavbarConfig | None = None,
    site_config: SiteConfig | None = None,
) -> Node:
    """Page header that contains the site navigation.

    Renders a PicoCSS <header> with class "is-fixed" and includes the Navbar.
    Header derives brand properties from SiteConfig when available.
    """

    # Safe fallbacks when a SiteConfig isn't provided
    brand_href = "/" if site_config is None else site_config.root_url
    brand_title = None if site_config is None else site_config.site_title
    if brand_title is None and isinstance(page_context, dict):
        brand_title = page_context.get("site_title")

    return html(
        t"""
<header class="is-fixed container">
  <{Navbar} brand_href={brand_href} brand_title={brand_title} page_context={page_context} navbar={navbar} />
</header>
"""
    )
