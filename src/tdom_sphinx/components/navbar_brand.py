from typing import Callable

from tdom import Node, html


def NavbarBrand(*, pathto: Callable[[str, int | None], str], href: str, title: str) -> Node:
    """First <ul> of a PicoCSS navbar with brand link.

    Renders a <ul> containing a single <li> with an <a> whose text is wrapped
    in <strong>.
    """
    return html(
        t"""
<ul>
  <li>
    <a href={pathto(href, 1)}><strong>{title}</strong></a>
  </li>
</ul>
"""
    )
