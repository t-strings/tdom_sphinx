from typing import Sequence

from tdom import Node, html

from tdom_sphinx.components.navbar_brand import NavbarBrand
from tdom_sphinx.components.navbar_links import NavbarLinks
from tdom_sphinx.models import TdomContext, Link, IconLink


def Navbar(*, brand_href: str, brand_title: str, context: TdomContext) -> Node:
    """Render a PicoCSS-style navbar with brand and links sections.

    - brand_href/brand_title: passed to NavbarBrand to render the brand link
    - links/buttons: taken from context.page_context['navbar'] if available
    - Fallback to empty when not provided.
    """
    page_ctx = context.page_context
    navbar_val = page_ctx.get("navbar") if isinstance(page_ctx, dict) else None

    # Extract links/buttons from the navbar mapping if present
    # Expect concrete Link/IconLink objects; default to empty sequences.
    links: Sequence[Link] = ()
    buttons: Sequence[IconLink] = ()
    if isinstance(navbar_val, dict):
        links = navbar_val.get("links") or ()  # type: ignore[assignment]
        buttons = navbar_val.get("buttons") or ()  # type: ignore[assignment]

    pathto = page_ctx["pathto"]

    return html(
        t"""
<nav>
  <{NavbarBrand} pathto={pathto} href={brand_href} title={brand_title} />
  <{NavbarLinks} pathto={pathto} links={links} buttons={buttons} />
</nav>
"""
    )
