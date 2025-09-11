"""Ensure the Sphinx Template Bridge is replaced and uses the container."""

from pathlib import Path

import pytest

from sphinx.testing.util import SphinxTestApp
from tdom_sphinx.models import View
from tdom_sphinx.template_bridge import TdomBridge

pytestmark = pytest.mark.sphinx("html", testroot="test-basic-sphinx")


@pytest.fixture
def sphinx_context() -> dict:
    srcdir = Path(__file__).parent / "roots/test-basic-sphinx"
    sphinx_app = SphinxTestApp(srcdir=srcdir)
    context = {
        "title": "My Test Page",
        "body": "<p>Hello World</p>",
        "sphinx_app": sphinx_app,
    }
    return context


def test_render_default_view(sphinx_context: dict) -> None:
    """Test that render gets a DefaultView."""

    tb = TdomBridge()
    result = tb.render("some_template", sphinx_context)
    assert "<title>My Test Page</title>" in result
