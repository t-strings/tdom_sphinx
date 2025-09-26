"""Tests for the tdom Sphinx views module."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp

from conftest import pathto
from tdom_sphinx.models import TdomContext
from tdom_sphinx.views import DefaultView


@pytest.fixture
def tdom_context() -> TdomContext:
    srcdir = Path(__file__).parent / "roots/test-basic-sphinx"
    sphinx_app = SphinxTestApp(srcdir=srcdir)
    page_context = {
        "site_title": "My Test Site",
        "title": "My Test Page",
        "body": "<p>Hello World</p>",
        "pathto": pathto,
    }
    context = TdomContext(
        app=sphinx_app,
        environment=sphinx_app.env,
        config=sphinx_app.config,
        page_context=page_context,
    )
    return context


def test_default_view_initialization(tdom_context: TdomContext) -> None:
    """Test that DefaultView can be initialized with context."""
    view = DefaultView(context=tdom_context)

    assert view.context == tdom_context
    assert isinstance(view, DefaultView)


def test_default_view_call_method(tdom_context: TdomContext):
    """Test that DefaultView.__call__ returns a tdom Element."""
    view = DefaultView(context=tdom_context)
    result = view()

    # The result should be a tdom Element that can be converted to string
    assert result is not None
    html_string = str(result)
    assert isinstance(html_string, str)
    assert len(html_string) > 0


def test_default_view_html_structure(tdom_context: TdomContext) -> None:
    """Test that DefaultView renders proper HTML structure."""
    view = DefaultView(context=tdom_context)

    result = view()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Check for proper HTML5 structure
    assert soup.find("html") is not None
    assert soup.find("html").get("lang") == "EN"
    assert soup.find("head") is not None
    assert soup.find("body") is not None

    # Check for DOCTYPE
    assert "<!DOCTYPE html>" in html_string

    # Check for title
    title_tag = soup.find("title")
    assert title_tag is not None
    assert title_tag.text == "My Test Page - My Test Site"
