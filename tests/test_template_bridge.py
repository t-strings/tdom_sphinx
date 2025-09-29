"""Ensure the Sphinx Template Bridge is replaced and uses the container."""

from tdom import Element

from tdom_sphinx.aria_testing.utils import get_text_content
from tdom_sphinx.models import PageContext
from tdom_sphinx.template_bridge import TdomBridge
from tdom_sphinx.utils import html_string_to_tdom


def test_render_default_view(sphinx_context: dict) -> None:
    """Test that render gets a DefaultView using shared fixtures."""

    tb = TdomBridge()
    result_str = tb.render("some_template", sphinx_context)

    # Convert HTML string to tdom structure for aria_testing
    result = html_string_to_tdom(result_str)

    # Find the head element - html_string_to_tdom returns the HTML element directly
    document_head = None
    assert isinstance(result, Element)
    if hasattr(result, "tag") and result.tag.lower() == "html":
        for html_child in result.children:
            assert isinstance(html_child, Element)
            if hasattr(html_child, "tag") and html_child.tag.lower() == "head":
                document_head = html_child
                break

    assert document_head is not None, "Could not find document head"

    # Find title element within head
    title_element = None
    for head_child in document_head.children:
        assert isinstance(head_child, Element)
        if hasattr(head_child, "tag") and head_child.tag.lower() == "title":
            title_element = head_child
            break

    assert title_element is not None, "Could not find title element"
    title_text = get_text_content(title_element).strip()
    assert title_text == "My Test Page - My Test Site"

    # Find stylesheet link
    stylesheet_element = None
    for head_child in document_head.children:
        assert isinstance(head_child, Element)
        if (
            hasattr(head_child, "tag")
            and head_child.tag.lower() == "link"
            and head_child.attrs.get("rel") == "stylesheet"
        ):
            stylesheet_element = head_child
            break

    assert stylesheet_element is not None, "Could not find stylesheet link"
    assert stylesheet_element.attrs.get("href") == "_static/tdom-sphinx.css"


def test_deep_static_nesting(sphinx_context: dict) -> None:
    """Test that render gets a DefaultView using shared fixtures."""

    # Change this path to be several folders down and see if the
    # relative static path is correct
    page_context = PageContext(
        body="<p>Hello World</p>",
        css_files=(),
        display_toc=False,
        js_files=(),
        pagename="foo/bar/baz/home.html",
        page_source_suffix=".rst",
        sourcename=None,
        templatename="page.html",
        title="My Test Page",
        toc=None,
    )
    sphinx_context["page_context"] = page_context

    tb = TdomBridge()
    result_str = tb.render("some_template", sphinx_context)

    # Convert HTML string to tdom structure for aria_testing
    result = html_string_to_tdom(result_str)

    # Find the head element - html_string_to_tdom returns the HTML element directly
    document_head = None
    assert isinstance(result, Element)
    if hasattr(result, "tag") and result.tag.lower() == "html":
        for html_child in result.children:
            assert isinstance(html_child, Element)
            if hasattr(html_child, "tag") and html_child.tag.lower() == "head":
                document_head = html_child
                break

    assert document_head is not None, "Could not find document head"

    # Find title element within head
    title_element = None
    for head_child in document_head.children:
        assert isinstance(head_child, Element)
        if hasattr(head_child, "tag") and head_child.tag.lower() == "title":
            title_element = head_child
            break

    assert title_element is not None, "Could not find title element"
    title_text = get_text_content(title_element).strip()
    assert title_text == "My Test Page - My Test Site"

    # Find all stylesheet links
    stylesheet_elements = []
    for head_child in document_head.children:
        assert isinstance(head_child, Element)
        if (
            hasattr(head_child, "tag")
            and head_child.tag.lower() == "link"
            and head_child.attrs.get("rel") == "stylesheet"
        ):
            stylesheet_elements.append(head_child)

    assert len(stylesheet_elements) > 0, "Could not find any stylesheet links"
    assert (
        stylesheet_elements[0].attrs.get("href") == "../../../_static/tdom-sphinx.css"
    )
