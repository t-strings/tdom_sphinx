from markupsafe import Markup
from tdom import Node, html

from tdom_sphinx.models import TdomContext


def Main(*, context: TdomContext) -> Node:
    """Main content area for a page.

    Renders a <main> element whose contents are the raw HTML body provided by
    Sphinx in context.page_context['body'].
    The body is wrapped in Markup to avoid escaping.
    """
    body = context.page_context.get("body", "")
    safe_body = Markup(body)

    return html(
        t"""
<main class="container">
  {safe_body}
</main>
"""
    )
