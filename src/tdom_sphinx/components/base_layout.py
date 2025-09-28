from tdom import Node, html

from tdom_sphinx.components.footer import Footer
from tdom_sphinx.components.head import Head
from tdom_sphinx.components.header import Header
from tdom_sphinx.components.main import Main
from tdom_sphinx.models import PageContext, SiteConfig


def BaseLayout(
    *, page_context: PageContext, site_config: SiteConfig | None = None
) -> Node:
    """Render a basic HTML document shell for Sphinx pages.

    Renders a full HTML5 document using components:
    - <{Head} /> for the <head>
    - <{Header} />, <{Main} />, <{Footer} /> inside <body>
    """

    return html(
        t"""\
<!DOCTYPE html>
<html lang=\"EN\">
<{Head} page_context={page_context} site_config={site_config} />
<body>
  <{Header} page_context={page_context} site_config={site_config} />
  <{Main} page_context={page_context} />
  <{Footer} page_context={page_context} site_config={site_config} />
</body>
</html>
"""
    )
