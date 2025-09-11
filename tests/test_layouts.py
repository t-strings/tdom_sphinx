"""Tests for the tdom Sphinx layouts module."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from sphinx.testing.util import SphinxTestApp
from tdom_sphinx.layouts import BaseLayout
from tdom_sphinx.models import TdomContext


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


def test_base_layout_initialization(tdom_context: TdomContext) -> None:
    """Test that BaseLayout can be initialized with context."""
    tdom_context.page_context = {
        "title": "Test Layout",
        "sphinx_context": {"body": "<p>Test content</p>"},
    }
    layout = BaseLayout(context=tdom_context)

    assert layout.context == tdom_context
    assert layout.children is None
    assert isinstance(layout, BaseLayout)


def test_base_layout_initialization_with_children(tdom_context: TdomContext) -> None:
    """Test that BaseLayout can be initialized with children."""
    tdom_context.page_context = {"title": "Test Layout"}
    children = ["<p>Child 1</p>", "<p>Child 2</p>"]
    layout = BaseLayout(context=tdom_context, children=children)

    assert layout.context == tdom_context
    assert layout.children == children


def test_base_layout_call_method(tdom_context: TdomContext) -> None:
    """Test that BaseLayout.__call__ returns a tdom Element."""
    tdom_context.page_context = {
        "title": "Test Layout",
        "sphinx_context": {"body": "<p>Test content</p>"},
    }
    layout = BaseLayout(context=tdom_context)

    result = layout()

    # The result should be a tdom Element that can be converted to string
    assert result is not None
    html_string = str(result)
    assert isinstance(html_string, str)
    assert len(html_string) > 0


def test_base_layout_html5_structure(tdom_context: TdomContext) -> None:
    """Test that BaseLayout renders proper HTML5 structure."""
    tdom_context.page_context = {
        "title": "HTML5 Test",
        "sphinx_context": {"body": "<p>HTML5 content</p>"},
    }
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Check for proper HTML5 structure
    assert "<!DOCTYPE html>" in html_string
    assert soup.find("html") is not None
    assert soup.find("html").get("lang") == "EN"
    assert soup.find("head") is not None
    assert soup.find("body") is not None


def test_base_layout_head_section(tdom_context: TdomContext) -> None:
    """Test that BaseLayout includes proper head section elements."""
    tdom_context.page_context = {
        "title": "Head Test",
        "sphinx_context": {"body": "<p>Head test content</p>"},
    }
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    head = soup.find("head")
    assert head is not None

    # Check for charset meta tag
    charset_meta = head.find("meta", {"charset": "utf-8"})
    assert charset_meta is not None

    # Check for viewport meta tag
    viewport_meta = head.find("meta", {"name": "viewport"})
    assert viewport_meta is not None
    assert viewport_meta.get("content") == "width=device-width, initial-scale=1"

    # Check for title
    title_tag = head.find("title")
    assert title_tag is not None
    assert title_tag.text == "Head Test"

    # Check for PicoCSS stylesheet
    css_link = head.find("link", {"rel": "stylesheet"})
    assert css_link is not None
    assert css_link.get("href") == "_static/pico.min.css"

    # Check for favicon
    favicon_link = head.find("link", {"rel": "icon"})
    assert favicon_link is not None
    assert favicon_link.get("href") == "_static/favicon.ico"
    assert favicon_link.get("type") == "image/x-icon"


def test_base_layout_body_structure(tdom_context: TdomContext) -> None:
    """Test that BaseLayout has proper body structure."""
    tdom_context.page_context = {
        "title": "Body Test",
        "body": "<p>Body test content</p>",
    }
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    body = soup.find("body")
    assert body is not None

    # Check for main container
    main = body.find("main")
    assert main is not None
    assert "container" in main.get("class")

    # Check for header inside main
    header = main.find("header")
    assert header is not None
    h1 = header.find("h1")
    assert h1 is not None
    assert h1.text == "Body Test"

    # Check for article inside main
    article = main.find("article")
    assert article is not None
    assert "Body test content" in article.get_text()


def test_base_layout_title_handling(tdom_context: TdomContext) -> None:
    """Test that BaseLayout properly handles title from context."""
    # Test with explicit title
    tdom_context.page_context = {
        "title": "Custom Title",
        "body": "<p>Content</p>",
    }
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    title_tag = soup.find("title")
    assert title_tag.text == "Custom Title"

    h1_tag = soup.find("h1")
    assert h1_tag.text == "Custom Title"


def test_base_layout_default_title(tdom_context: TdomContext) -> None:
    """Test that BaseLayout uses default title when none provided."""
    tdom_context.page_context = {"body": "<p>Content without title</p>"}
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Should use default title
    title_tag = soup.find("title")
    assert title_tag.text == "tdom Documentation"

    h1_tag = soup.find("h1")
    assert h1_tag.text == "tdom Documentation"


def test_base_layout_body_content_extraction(tdom_context: TdomContext) -> None:
    """Test that BaseLayout properly extracts body content from sphinx_context."""
    tdom_context.page_context = {
        "title": "Content Test",
        "body": "<div><h2>Section Title</h2><p>Paragraph content</p><ul><li>List item</li></ul></div>",
    }
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    article = soup.find("article")
    assert article is not None

    # Check that nested HTML structure is preserved
    h2 = article.find("h2")
    assert h2 is not None
    assert h2.text == "Section Title"

    p = article.find("p")
    assert p is not None
    assert p.text == "Paragraph content"

    ul = article.find("ul")
    assert ul is not None
    li = ul.find("li")
    assert li is not None
    assert li.text == "List item"


def test_base_layout_no_body_content(tdom_context: TdomContext) -> None:
    """Test that BaseLayout handles missing body content gracefully."""
    tdom_context.page_context = {"title": "No Body Test"}
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    article = soup.find("article")
    assert article is not None
    assert "No content" in article.get_text()


def test_base_layout_no_sphinx_context(tdom_context: TdomContext) -> None:
    """Test that BaseLayout handles missing sphinx_context gracefully."""
    tdom_context.page_context = {"title": "No Sphinx Context"}
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Should still render with default content
    title_tag = soup.find("title")
    assert title_tag.text == "No Sphinx Context"

    article = soup.find("article")
    assert article is not None
    assert "No content" in article.get_text()


def test_base_layout_empty_context(tdom_context: TdomContext) -> None:
    """Test that BaseLayout handles empty context gracefully."""
    tdom_context.page_context = {}
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Should use all defaults
    title_tag = soup.find("title")
    assert title_tag.text == "tdom Documentation"

    h1_tag = soup.find("h1")
    assert h1_tag.text == "tdom Documentation"

    article = soup.find("article")
    assert article is not None
    assert "No content" in article.get_text()


def test_base_layout_complex_context(tdom_context: TdomContext) -> None:
    """Test that BaseLayout handles complex context with extra data."""
    tdom_context.page_context = {
        "title": "Complex Test",
        "body": "<p>Main content</p>",
        "pagename": "index",
        "docname": "index",
        "other_sphinx_data": "ignored",
        "extra_data": "should be ignored",
        "nested": {"data": "also ignored"},
    }
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Should only use title and body from the context
    title_tag = soup.find("title")
    assert title_tag.text == "Complex Test"

    article = soup.find("article")
    assert article is not None
    assert "Main content" in article.get_text()

    # Extra data should not appear in the output
    assert "ignored" not in html_string
    assert "should be ignored" not in html_string


def test_base_layout_html_escaping(tdom_context: TdomContext) -> None:
    """Test that BaseLayout properly handles HTML content without double-escaping."""
    tdom_context.page_context = {
        "title": "HTML Test",
        "body": "<p>Content with <strong>bold</strong> and <em>italic</em> text</p>",
    }
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    article = soup.find("article")
    assert article is not None

    # Check that HTML tags are preserved, not escaped
    strong = article.find("strong")
    assert strong is not None
    assert strong.text == "bold"

    em = article.find("em")
    assert em is not None
    assert em.text == "italic"


def test_base_layout_static_asset_paths(tdom_context: TdomContext) -> None:
    """Test that BaseLayout uses correct static asset paths."""
    tdom_context.page_context = {"title": "Asset Path Test"}
    layout = BaseLayout(context=tdom_context)

    result = layout()
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    # Check CSS path
    css_link = soup.find("link", {"rel": "stylesheet"})
    assert css_link.get("href") == "_static/pico.min.css"

    # Check favicon path
    favicon_link = soup.find("link", {"rel": "icon"})
    assert favicon_link.get("href") == "_static/favicon.ico"
