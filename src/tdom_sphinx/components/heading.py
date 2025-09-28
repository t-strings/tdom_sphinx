from tdom import Node, html

from tdom_sphinx.components.navbar_brand import NavbarBrand
from tdom_sphinx.components.navbar_links import NavbarLinks
from tdom_sphinx.models import IconLink, Link, NavbarConfig, PageContext, SiteConfig


def Heading(
    *,
    page_context: PageContext,
    site_config: SiteConfig,
) -> Node:
    """Page heading that contains the site navigation.

    Renders a PicoCSS <header> with class "is-fixed" and inlines the navbar
    by directly composing NavbarBrand and NavbarLinks. Heading derives brand
    properties from SiteConfig when available.
    """

    # Fetch navbar config from site_config when provided
    navbar = None if site_config is None else site_config.navbar

    # Extract links/buttons from the navbar config if present
    links: tuple[Link, ...] | list[Link] = ()
    buttons: tuple[IconLink, ...] | list[IconLink] = ()
    if isinstance(navbar, NavbarConfig):
        links = navbar.links or ()
        buttons = navbar.buttons or ()

    return html(
        t"""
<header class="is-fixed">
  <nav class="container">
    <{NavbarBrand} page_context={page_context} href={site_config.root_url} title={site_config.site_title} />
    <{NavbarLinks} page_context={page_context} links={links} buttons={buttons} />
  </nav>
</header>
"""
    )
