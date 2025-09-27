from typing import Sequence

from tdom import Node, html

from tdom_sphinx.components.navbar_brand import NavbarBrand
from tdom_sphinx.components.navbar_links import NavbarLinks
from tdom_sphinx.models import Link, IconLink, NavbarConfig, PageContext


def Navbar(
    *, brand_href: str, brand_title: str, page_context: PageContext, navbar: NavbarConfig | None = None
) -> Node:
    """Render a PicoCSS-style navbar with brand and links sections.

    - brand_href/brand_title: passed to NavbarBrand to render the brand link
    - links/buttons: taken from provided `navbar` if available
    - Fallback to empty when not provided.
    """

    # Extract links/buttons from the navbar config if present
    links: Sequence[Link] = ()
    buttons: Sequence[IconLink] = ()
    if isinstance(navbar, NavbarConfig):
        links = navbar.links or ()
        buttons = navbar.buttons or ()

    pathto = getattr(page_context, "pathto", None) or (page_context.get("pathto") if isinstance(page_context, dict) else None)

    return html(
        t"""
<nav>
  <{NavbarBrand} pathto={pathto} href={brand_href} title={brand_title} />
  <{NavbarLinks} pathto={pathto} links={links} buttons={buttons} />
</nav>
"""
    )
