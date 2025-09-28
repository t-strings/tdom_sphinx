"""Tests for Sphinx event handlers in sphinx_events.py."""

from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from tdom_sphinx.sphinx_events import _on_html_page_context, _on_builder_inited
from tdom_sphinx.models import PageContext


@pytest.mark.sphinx("html", testroot="test-basic-sphinx")
def test_site_config_on_app_from_builder_inited() -> None:
    srcdir = Path(__file__).parent / "roots/test-basic-sphinx"
    app = SphinxTestApp(srcdir=srcdir)

    # Precondition: site_config may be present via registered config
    expected = getattr(app.config, "site_config", None)

    # Simulate Sphinx calling the builder-inited handler
    _on_builder_inited(app)

    # The handler should create app.site_config and preserve navbar
    actual = getattr(app, "site_config", None)
    assert actual is not None
    assert getattr(actual, "navbar", None) == getattr(expected, "navbar", None)


@pytest.mark.sphinx("html", testroot="test-basic-sphinx")
def test_page_context_added_to_context() -> None:
    srcdir = Path(__file__).parent / "roots/test-basic-sphinx"
    app = SphinxTestApp(srcdir=srcdir)

    # Provide a minimal context expected by make_page_context
    context: dict = {
        "project": "My Test Site",
        "title": "My Test Page",
        "body": "<p>Hello</p>",
        "toc": "",
        "page_source_suffix": ".rst",
        "sourcename": "index.rst",
    }

    _on_html_page_context(app, "index", "page.html", context, doctree=None)

    pc = context.get("page_context")
    assert isinstance(pc, PageContext)
    assert pc.pagename == "index"
    assert pc.templatename == "page.html"


@pytest.mark.sphinx("html", testroot="test-navbar-sphinx")
def test_copyright_defaults_from_sphinx_config_when_absent() -> None:
    srcdir = Path(__file__).parent / "roots/test-navbar-sphinx"
    app = SphinxTestApp(srcdir=srcdir)

    # Simulate a Sphinx conf.py with a copyright value
    app.config.copyright = "Acme Corp"

    # Trigger builder-inited to create SiteConfig on the app
    _on_builder_inited(app)

    sc = getattr(app, "site_config", None)
    assert sc is not None
    assert getattr(sc, "copyright", None) == "Acme Corp"
