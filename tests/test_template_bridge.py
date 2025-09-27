"""Ensure the Sphinx Template Bridge is replaced and uses the container."""

import pytest

from tdom_sphinx.template_bridge import TdomBridge

pytestmark = pytest.mark.sphinx("html", testroot="test-basic-sphinx")


def test_render_default_view(sphinx_context: dict) -> None:
    """Test that render gets a DefaultView using shared fixtures."""

    tb = TdomBridge()
    result = tb.render("some_template", sphinx_context)
    assert "<title>My Test Page - My Test Site</title>" in result
