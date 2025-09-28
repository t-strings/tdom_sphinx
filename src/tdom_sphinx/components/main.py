from markupsafe import Markup
from tdom import Node, html

from tdom_sphinx.models import PageContext


def Main(*, page_context: PageContext) -> Node:
    """Main content area for a page.

    Renders a <main> element whose contents are the raw HTML body provided by
    Sphinx in page_context['body'].
    The body is wrapped in Markup to avoid escaping.
    """
    safe_body = Markup(page_context.body)

    return html(
        t"""
<main>
  {safe_body}
</main>
"""
    )
