from tdom import Node, html

from tdom_sphinx.components.footer import Footer
from tdom_sphinx.components.head import Head
from tdom_sphinx.components.header import Header
from tdom_sphinx.components.main import Main
from tdom_sphinx.models import TdomContext


def BaseLayout(*, context: TdomContext) -> Node:
    """Render a basic HTML document shell for Sphinx pages.

    Renders a full HTML5 document using components:
    - <{Head} /> for the <head>
    - <{Header} />, <{Main} />, <{Footer} /> inside <body>
    """
    return html(
        t"""\
<!DOCTYPE html>
<html lang=\"EN\">
<{Head} context={context} />
<body>
  <{Header} context={context} />
  <{Main} context={context} />
  <{Footer} context={context} />
</body>
</html>
"""
    )
