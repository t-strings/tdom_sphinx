from pathlib import PurePosixPath

from tdom import Node, html

from tdom_sphinx.models import PageContext, SiteConfig
from tdom_sphinx.url import relative_tree


def SiteAside(
    *, page_context: PageContext, site_config: SiteConfig | None = None
) -> Node:
    """Render a site aside with static content.

    This component renders an <aside> element with static HTML content.
    Uses relative_tree to make hrefs relative to the current page.
    """
    result = html(
        t"""
<aside>
  <h3>Quick Links</h3>
  <ul>
    <li><a href="/docs/">Documentation</a></li>
    <li><a href="/api/">API Reference</a></li>
    <li><a href="/examples/">Examples</a></li>
    <li><a href="/support/">Support</a></li>
  </ul>

  <h3>Resources</h3>
  <ul>
    <li><a href="/downloads/">Downloads</a></li>
    <li><a href="/tutorials/">Tutorials</a></li>
    <li><a href="/community/">Community</a></li>
  </ul>
</aside>
"""
    )

    # Make hrefs in this subtree relative to the current page
    current = PurePosixPath("/" + page_context.pagename)
    relative_tree(result, current)

    return result