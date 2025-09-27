from typing import Callable, Sequence

from tdom import Node, html

from tdom_sphinx.models import IconLink, Link


def NavbarLinks(
    *,
    pathto: Callable[[str, int | None], str],
    links: Sequence[Link],
    buttons: Sequence[IconLink],
) -> Node:
    """Second <ul> of a PicoCSS navbar.

    Renders a list of text links followed by a list of icon buttons.
    """
    link_nodes = [
        html(t"""<li><a href={pathto(l.href, 0)} class={l.style}>{l.text}</a></li>""")
        for l in links
    ]

    button_nodes = [
        html(
            t"""
<li>
  <a href={pathto(b.href, 0)}>
    <span class="icon" style={f"color: {b.color}"}>
      <i class={b.icon_class}></i>
    </span>
  </a>
</li>
"""
        )
        for b in buttons
    ]

    items = [*link_nodes, *button_nodes]

    return html(
        t"""
<ul>
  {items}
</ul>
"""
    )
