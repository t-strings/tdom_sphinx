"""Tests for the tdom Sphinx views module."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from sphinx.testing.util import SphinxTestApp
from tdom_sphinx.models import TdomContext
from tdom_sphinx.views import DefaultView


@pytest.fixture
def tdom_context() -> TdomContext:
    srcdir = Path(__file__).parent / "roots/test-basic-sphinx"
    sphinx_app = SphinxTestApp(srcdir=srcdir)
    page_context = {
        "title": "My Test Page",
        "body": "<p>Hello World</p>",
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
    assert title_tag.text == "My Test Page"

    # Check for header with h1
    header = soup.find("header")
    assert header is not None
    h1 = header.find("h1")
    assert h1 is not None
    assert h1.text == "My Test Page"

    # Check for article with content
    article = soup.find("article")
    assert article is not None
    assert "Hello World" in article.get_text()


def test_default_view_with_default_title(tdom_context: TdomContext) -> None:
    """Test DefaultView with default title when none provided."""
    tdom_context.page_context = {"body": "<p>Content without title</p>"}
    view = DefaultView(context=tdom_context)

    result = view()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Should use default title
    title_tag = soup.find("title")
    assert title_tag is not None
    assert title_tag.text == "tdom Documentation"


def test_default_view_with_no_body(tdom_context: TdomContext) -> None:
    """Test DefaultView when no body content is provided."""
    tdom_context.page_context = {"title": "Empty Page"}
    view = DefaultView(context=tdom_context)

    result = view()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Should use default "No content" message
    article = soup.find("article")
    assert article is not None
    assert "No content" in article.get_text()


def test_default_view_includes_static_assets(tdom_context: TdomContext) -> None:
    """Test that DefaultView includes required static assets."""
    tdom_context.page_context = {"title": "Asset Test"}
    view = DefaultView(context=tdom_context)

    result = view()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Check for PicoCSS stylesheet
    css_link = soup.find("link", {"rel": "stylesheet"})
    assert css_link is not None
    assert css_link.get("href") == "_static/pico.min.css"

    # Check for favicon
    favicon_link = soup.find("link", {"rel": "icon"})
    assert favicon_link is not None
    assert favicon_link.get("href") == "_static/favicon.ico"
    assert favicon_link.get("type") == "image/x-icon"


def test_default_view_meta_tags(tdom_context: TdomContext) -> None:
    """Test that DefaultView includes proper meta tags."""
    tdom_context.page_context = {"title": "Meta Test"}
    view = DefaultView(context=tdom_context)

    result = view()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Check for charset meta tag
    charset_meta = soup.find("meta", {"charset": "utf-8"})
    assert charset_meta is not None

    # Check for viewport meta tag
    viewport_meta = soup.find("meta", {"name": "viewport"})
    assert viewport_meta is not None
    assert viewport_meta.get("content") == "width=device-width, initial-scale=1"


def test_default_view_container_structure(tdom_context: TdomContext) -> None:
    """Test that DefaultView has proper container structure."""
    tdom_context.page_context = {
        "title": "Container Test",
        "sphinx_context": {"body": "<p>Container content</p>"},
    }
    view = DefaultView(context=tdom_context)

    result = view()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Check for main container
    main = soup.find("main")
    assert main is not None
    assert "container" in main.get("class")

    # Check that header and article are inside main
    header = main.find("header")
    article = main.find("article")
    assert header is not None
    assert article is not None


def test_default_view_context_handling(tdom_context: TdomContext) -> None:
    """Test that DefaultView properly handles different context structures."""
    # Test with nested sphinx_context
    tdom_context.page_context = {
        "title": "Context Test",
        "body": "<div><h2>Nested Content</h2><p>Some text</p></div>",
        "other_data": "ignored",
        "extra_data": "also ignored",
    }
    view = DefaultView(context=tdom_context)

    result = view()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Check that nested HTML is preserved
    article = soup.find("article")
    assert article is not None
    h2 = article.find("h2")
    assert h2 is not None
    assert h2.text == "Nested Content"

    # Check that paragraph content is there
    p = article.find("p")
    assert p is not None
    assert p.text == "Some text"
