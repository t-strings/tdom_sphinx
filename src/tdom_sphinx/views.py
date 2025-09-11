from dataclasses import dataclass
from typing import Any

from tdom import Element
from tdom_sphinx.layouts import BaseLayout
from tdom_sphinx.models import TdomContext


@dataclass
class DefaultView:
    """Default page view using the BaseLayout.

    Accepts a plain context dict as used in tests.
    """

    context: TdomContext

    def __call__(self) -> Element:
        layout = BaseLayout(context=self.context)
        return layout()
