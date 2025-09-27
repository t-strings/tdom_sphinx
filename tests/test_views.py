"""Tests for the tdom Sphinx views module."""

from bs4 import BeautifulSoup

from tdom_sphinx.models import PageContext, SiteConfig
from tdom_sphinx.views import DefaultView


def test_default_view_initialization(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    """Test that DefaultView can be initialized."""
    view = DefaultView(page_context=page_context, site_config=site_config)

    assert isinstance(view, DefaultView)


def test_default_view_call_method(
    page_context: PageContext, site_config: SiteConfig
):
    """Test that DefaultView.__call__ returns a tdom Element."""
    view = DefaultView(page_context=page_context, site_config=site_config)
    result = view()

    # The result should be a tdom Element that can be converted to string
    assert result is not None
    html_string = str(result)
    assert isinstance(html_string, str)
    assert len(html_string) > 0


def test_default_view_html_structure(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    """Test that DefaultView renders proper HTML structure."""
    view = DefaultView(page_context=page_context, site_config=site_config)

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
