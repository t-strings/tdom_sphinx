from tdom import Node, html

from tdom_sphinx.components.footer import Footer
from tdom_sphinx.components.head import Head
from tdom_sphinx.components.header import Header
from tdom_sphinx.components.main import Main
from tdom_sphinx.models import SiteConfig, PageContext


def BaseLayout(*, page_context: PageContext, site_config: SiteConfig | None = None) -> Node:
    """Render a basic HTML document shell for Sphinx pages.

    Renders a full HTML5 document using components:
    - <{Head} /> for the <head>
    - <{Header} />, <{Main} />, <{Footer} /> inside <body>
    """
    # Ensure child components always receive a SiteConfig instance
    if site_config is None:
        # If not provided, derive site title from page_context when available
        site_title = None
        if isinstance(page_context, dict):
            site_title = page_context.get("site_title")
        effective_site_config = SiteConfig(site_title=site_title)
    else:
        effective_site_config = site_config

    navbar = effective_site_config.navbar
    return html(
        t"""\
<!DOCTYPE html>
<html lang=\"EN\">
<{Head} page_context={page_context} site_config={effective_site_config} />
<body>
  <{Header} page_context={page_context} navbar={navbar} site_config={effective_site_config} />
  <{Main} page_context={page_context} />
  <{Footer} page_context={page_context} />
</body>
</html>
"""
    )
