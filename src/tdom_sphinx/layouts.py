"""Layouts for tdom-based Sphinx theme.

Provides a BaseLayout that renders a complete HTML5 document using t-strings.
"""

from dataclasses import dataclass

from markupsafe import Markup
from tdom import Node, html

from tdom_sphinx.components.head import Head
from tdom_sphinx.models import TdomContext


@dataclass
class BaseLayout:
    """Render a basic HTML document shell for Sphinx pages.

    Context keys of interest:
    - title: Optional[str] – page title, defaults to DEFAULT_TITLE
    - sphinx_context: Optional[dict] – the raw Sphinx template context
      - body: Optional[str] – HTML for the page body content
    """

    context: TdomContext

    def __call__(self) -> Node:
        page_context = self.context.page_context
        title = page_context.get("title", "Default Title")
        site_title = page_context.get("site_title")
        body_html = Markup(page_context.get("body", "<p>No content</p>"))
        pathto = page_context.get("pathto")

        # Full HTML5 structure with PicoCSS and favicon links expected by tests
        return html(
            t"""<!DOCTYPE html><html lang="EN">
<{Head} pathto={pathto} title={title} site_title={site_title} />
<body>
  <main class="container">
    <header>
      <h1>{title}</h1>
    </header>
    <article>
      {body_html}
    </article>
  </main>
</body>
</html>"""
        )
