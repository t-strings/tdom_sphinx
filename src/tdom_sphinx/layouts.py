"""Layouts for tdom-based Sphinx theme.

Provides a BaseLayout that renders a complete HTML5 document using t-strings.
"""

from dataclasses import dataclass
from typing import Iterable, Optional

from markupsafe import Markup
from tdom import Element, html

from tdom_sphinx.models import TdomContext

DEFAULT_TITLE = "tdom Documentation"


@dataclass
class BaseLayout:
    """Render a basic HTML document shell for Sphinx pages.

    Context keys of interest:
    - title: Optional[str] – page title, defaults to DEFAULT_TITLE
    - sphinx_context: Optional[dict] – the raw Sphinx template context
      - body: Optional[str] – HTML for the page body content
    """

    context: TdomContext

    def __call__(self) -> Element:
        page_context = self.context.page_context
        title = page_context.get("title") or DEFAULT_TITLE
        body_html = Markup(page_context.get("body", "<p>No content</p>"))
        pathto = page_context.get("pathto")

        # Full HTML5 structure with PicoCSS and favicon links expected by tests
        return html(
            t"""<!DOCTYPE html><html lang="EN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <link rel="stylesheet" href="{pathto("_static/pico.css", 1)}" />
  <link rel="stylesheet" href="{pathto("_static/sphinx.css", 1)}" />
  <link rel="icon" href="{pathto("_static/favicon.ico", 1)}" type="image/x-icon" />
</head>
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
