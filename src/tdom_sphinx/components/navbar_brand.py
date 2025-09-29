from pathlib import PurePosixPath

from tdom import Node, html

from tdom_sphinx.url import relative_tree


def NavbarBrand(*, pagename: str, href: str, title: str) -> Node:
    """First <ul> of a PicoCSS navbar with a brand link.

    Renders a <ul> containing a single <li> with an <a> whose text is wrapped
    in <strong>. Uses relative_tree to make hrefs relative to the current page.
    """
    result = html(
        t"""
<ul>
  <li>
    <a href={href}><strong>{title}</strong></a>
  </li>
</ul>
"""
    )

    # Make hrefs in this subtree relative to the current page
    current = PurePosixPath("/" + pagename)
    relative_tree(result, current)

    return result
