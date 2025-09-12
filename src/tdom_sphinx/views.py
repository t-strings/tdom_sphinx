from dataclasses import dataclass

from markupsafe import Markup
from tdom import Element, html

from tdom_sphinx.layouts import BaseLayout
from tdom_sphinx.models import TdomContext


@dataclass
class DefaultView:
    """Default page view using the BaseLayout.

    Accepts a plain context dict as used in tests.
    """

    context: TdomContext

    def __call__(self) -> Element:
        page_context = self.context.page_context
        children = Markup(page_context.get("body", "<p>No content</p>"))
        result = html(t"""\
<{BaseLayout} context={self.context}>
{children}
</{BaseLayout}>
""")
        return result
