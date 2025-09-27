from markupsafe import Markup
from tdom import Node, html

from tdom_sphinx.models import PageContext


def Main(*, page_context: PageContext) -> Node:
    """Main content area for a page.

    Renders a <main> element whose contents are the raw HTML body provided by
    Sphinx in page_context['body'].
    The body is wrapped in Markup to avoid escaping.
    """
    body = getattr(page_context, "body", None)
    if body is None and isinstance(page_context, dict):
        body = page_context.get("body", "")
    if body is None:
        body = ""

    safe_body = Markup(body)

    return html(
        t"""
<main class="container">
  {safe_body}
</main>
"""
    )
