"""Tests for Sphinx event handlers in sphinx_events.py."""

from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from tdom_sphinx.sphinx_events import _on_html_page_context


@pytest.mark.sphinx("html", testroot="test-basic-sphinx")
def test_navbar_from_conf_added_to_context() -> None:
    srcdir = Path(__file__).parent / "roots/test-basic-sphinx"
    app = SphinxTestApp(srcdir=srcdir)

    # Precondition: navbar is present in raw config via conf.py
    assert hasattr(app.config, "_raw_config")
    expected = app.config._raw_config.get("navbar")

    # Simulate Sphinx calling the event handler
    context: dict = {}
    _on_html_page_context(app, "index", "page.html", context, doctree=None)

    # The handler should add the navbar to the context
    assert context.get("navbar") == expected
