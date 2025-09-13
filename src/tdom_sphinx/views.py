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
        # Directly instantiate and invoke the BaseLayout to avoid nested HTML assembly
        layout = BaseLayout(context=self.context)
        return layout()
