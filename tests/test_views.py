"""Tests for the tdom Sphinx views module."""

from tdom import Element, Fragment

from tdom_sphinx.aria_testing import get_by_role
from tdom_sphinx.aria_testing.utils import get_text_content
from tdom_sphinx.models import PageContext, SiteConfig
from tdom_sphinx.views import DefaultView


def test_default_view_initialization(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    """Test that DefaultView can be initialized."""
    view = DefaultView(page_context=page_context, site_config=site_config)

    assert isinstance(view, DefaultView)


def test_default_view_call_method(page_context: PageContext, site_config: SiteConfig):
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
    """Test that DefaultView renders a proper HTML structure."""
    view = DefaultView(page_context=page_context, site_config=site_config)

    result = view()
    html_string = str(result)

    # Check for proper HTML5 structure using tdom navigation
    # DefaultView returns a Fragment containing DOCTYPE and HTML element
    html_element = None
    assert isinstance(result, Fragment)
    for child in result.children:
        if isinstance(child, Element) and child.tag.lower() == "html":
            html_element = child
            break

    assert html_element is not None, "Could not find HTML element"
    assert html_element.attrs.get("lang") == "EN"

    # Find head and body elements
    head_element = None
    body_element = None
    for child in html_element.children:
        if isinstance(child, Element):
            if child.tag.lower() == "head":
                head_element = child
            elif child.tag.lower() == "body":
                body_element = child

    assert head_element is not None, "Could not find head element"
    assert body_element is not None, "Could not find body element"

    # Check for DOCTYPE
    assert "<!DOCTYPE html>" in html_string

    # Check for title
    title_element = None
    for head_child in head_element.children:
        if isinstance(head_child, Element) and head_child.tag.lower() == "title":
            title_element = head_child
            break

    assert title_element is not None, "Could not find title element"
    title_text = get_text_content(title_element)
    assert title_text == "My Test Page - My Test Site"

    # Check for semantic structure using aria_testing
    header_element = get_by_role(result, "banner")
    assert header_element.tag == "header"

    main_element = get_by_role(result, "main")
    assert main_element.tag == "main"

    footer_element = get_by_role(result, "contentinfo")
    assert footer_element.tag == "footer"
