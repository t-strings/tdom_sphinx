from typing import Sequence

from tdom import Node, html

from tdom_sphinx.components.navbar_brand import NavbarBrand
from tdom_sphinx.components.navbar_links import NavbarLinks
from tdom_sphinx.models import TdomContext
from tdom_sphinx.theme_config import Link, IconLink


def Navbar(*, brand_href: str, brand_title: str, context: TdomContext) -> Node:
    """Render a PicoCSS-style navbar with brand and links sections.

    - brand_href/brand_title: passed to NavbarBrand to render the brand link
    - links/buttons: taken from context.config (attributes: nav_links, nav_buttons)
      Backward compatibility: will fall back to legacy tdom_nav_links/tdom_nav_buttons if present.
    - nav_class: class to apply to the <nav> element (defaults to Pico "container-fluid")
    """
    cfg = context.config
    # Prefer new names; fall back to legacy for compatibility
    links: Sequence[Link] = getattr(
        cfg, "nav_links", getattr(cfg, "tdom_nav_links", ())
    )  # type: ignore[assignment]
    buttons: Sequence[IconLink] = getattr(
        cfg, "nav_buttons", getattr(cfg, "tdom_nav_buttons", ())
    )  # type: ignore[assignment]

    pathto = context.page_context["pathto"]

    return html(
        t"""
<nav>
  <{NavbarBrand} pathto={pathto} href={brand_href} title={brand_title} />
  <{NavbarLinks} pathto={pathto} links={links} buttons={buttons} />
</nav>
"""
    )
