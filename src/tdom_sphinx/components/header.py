from tdom import Node, html

from tdom_sphinx.components.navbar_brand import NavbarBrand
from tdom_sphinx.components.navbar_links import NavbarLinks
from tdom_sphinx.models import IconLink, Link, NavbarConfig, PageContext, SiteConfig


def Header(
    *,
    page_context: PageContext,
    site_config: SiteConfig | None = None,
) -> Node:
    """Page header that contains the site navigation.

    Renders a PicoCSS <header> with class "is-fixed" and inlines the navbar
    by directly composing NavbarBrand and NavbarLinks. Header derives brand
    properties from SiteConfig when available.
    """

    # Safe fallbacks when a SiteConfig isn't provided
    brand_href = "/" if site_config is None else site_config.root_url
    brand_title = None if site_config is None else site_config.site_title
    if brand_title is None and isinstance(page_context, dict):
        brand_title = page_context.get("site_title")

    # Fetch navbar config from site_config when provided
    navbar = None if site_config is None else site_config.navbar

    # Extract links/buttons from the navbar config if present
    links: tuple[Link, ...] | list[Link] = ()
    buttons: tuple[IconLink, ...] | list[IconLink] = ()
    if isinstance(navbar, NavbarConfig):
        links = navbar.links or ()
        buttons = navbar.buttons or ()

    # Support both typed PageContext and dict-style contexts for pathto
    pathto = getattr(page_context, "pathto", None) or (
        page_context.get("pathto") if isinstance(page_context, dict) else None
    )

    return html(
        t"""
<header class="is-fixed container">
  <nav>
    <{NavbarBrand} pathto={pathto} href={brand_href} title={brand_title} />
    <{NavbarLinks} page_context={page_context} links={links} buttons={buttons} />
  </nav>
</header>
"""
    )
