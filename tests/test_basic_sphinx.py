"""Integration test for basic Sphinx theme functionality."""

import pytest
from tdom import Element

from tdom_sphinx.aria_testing.utils import get_text_content
from tdom_sphinx.utils import html_string_to_tdom

pytestmark = pytest.mark.sphinx("html", testroot="basic-sphinx")


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_index(page: str) -> None:
    """Ensure basics are in the page."""
    result = html_string_to_tdom(page)

    # Find HTML element - could be direct Element or in Fragment children
    html_element = None
    if isinstance(result, Element) and result.tag.lower() == "html":
        html_element = result
    else:
        assert isinstance(result, Element)
        for child in result.children:
            if isinstance(child, Element) and child.tag.lower() == "html":
                html_element = child
                break
    assert html_element is not None

    # Find head element
    head_element = None
    for child in html_element.children:
        if isinstance(child, Element) and child.tag.lower() == "head":
            head_element = child
            break
    assert head_element is not None

    # Find title element
    title_element = None
    for head_child in head_element.children:
        if isinstance(head_child, Element) and head_child.tag.lower() == "title":
            title_element = head_child
            break

    assert title_element is not None
    title_text = get_text_content(title_element).strip()
    assert title_text == "Hello PicoCSS - tdom-sphinx"
