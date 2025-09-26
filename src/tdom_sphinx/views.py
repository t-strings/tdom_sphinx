from dataclasses import dataclass

from tdom import Node

from tdom_sphinx.components.base_layout import BaseLayout
from tdom_sphinx.models import TdomContext


@dataclass
class DefaultView:
    """Default page view using the BaseLayout.

    Accepts a plain context dict as used in tests.
    """

    context: TdomContext

    def __call__(self) -> Node:
        # Directly instantiate and invoke the BaseLayout to avoid nested HTML assembly
        return BaseLayout(context=self.context)
