from pathlib import PurePosixPath

from tdom import Markup, Node, html

from tdom_sphinx.models import PageContext
from tdom_sphinx.url import relative_tree


def SiteAside(*, page_context: PageContext) -> Node:
    """Render a site aside with toctree content.

    This component renders an <aside> element with the toctree from page_context.
    Uses relative_tree to make hrefs relative to the current page.
    """
    # Get the toctree HTML from page_context and wrap it in Markup for safe injection
    toctree_html = Markup(str(page_context.toc)) if page_context.toc else ""

    result = html(
        t"""
<aside id="site-aside">
  {toctree_html}
</aside>
"""
    )

    # Make hrefs in this subtree relative to the current page
    # This must happen after the HTML is constructed so relative_tree can process the DOM
    current = PurePosixPath("/" + page_context.pagename)
    relative_tree(result, current)

    return result
