from typing import Sequence

from pathlib import PurePosixPath
from tdom import Node, html

from tdom_sphinx.models import IconLink, Link
from tdom_sphinx.url import relative_tree


def NavbarLinks(
    *,
    pagename: str,
    links: Sequence[Link],
    buttons: Sequence[IconLink],
) -> Node:
    """Second <ul> of a PicoCSS navbar.

    Renders a list of text links followed by a list of icon buttons.

    This version does not use Sphinx pathto; it renders the provided hrefs
    as-is, then rewrites internal absolute URLs to be relative to the current
    page by calling relative_tree on the resulting Node.
    """

    link_nodes = [
        html(t"""<li><a href={l.href} class={l.style}>{l.text}</a></li>""")
        for l in links
    ]

    button_nodes = [
        html(
            t"""
<li>
  <a href={b.href}>
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

    result = html(
        t"""
<ul>
  {items}
</ul>
"""
    )

    # Make hrefs in this subtree relative to the current page
    current = PurePosixPath("/" + pagename)
    relative_tree(result, current)

    return result
