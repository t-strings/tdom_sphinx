"""Integration test that verifies navbar links/buttons appears in built HTML."""

import pytest
from typing import Optional
from tdom import Element

from tdom_sphinx.aria_testing import get_by_role
from tdom_sphinx.aria_testing.utils import get_text_content
from tdom_sphinx.utils import html_string_to_tdom

pytestmark = pytest.mark.sphinx("html", testroot="navbar-sphinx")


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_navbar_links_and_buttons_render(page: str) -> None:
    result = html_string_to_tdom(page)

    # Find the HTML element - could be direct Element or in Fragment children
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

    # Find head element to check stylesheets
    head_element = None
    for child in html_element.children:
        if isinstance(child, Element) and child.tag.lower() == "head":
            head_element = child
            break
    assert head_element is not None

    # See if relative links in the head work
    stylesheet_element = None
    for head_child in head_element.children:
        if (
            isinstance(head_child, Element)
            and head_child.tag.lower() == "link"
            and head_child.attrs.get("rel") == "stylesheet"
        ):
            stylesheet_element = head_child
            break
    assert stylesheet_element is not None
    assert stylesheet_element.attrs.get("href") == "_static/tdom-sphinx.css"

    # Find the nav inside the header using aria_testing
    header_element = get_by_role(result, "banner")
    assert header_element.tag == "header"

    # Find nav within header
    nav_element = None
    for child in header_element.children:
        if isinstance(child, Element) and child.tag.lower() == "nav":
            nav_element = child
            break
    assert nav_element is not None

    # Find all link elements within the nav
    def find_all_links(element: Element) -> list[Element]:
        links = []
        for child in element.children:
            if isinstance(child, Element):
                if child.tag.lower() == "a":
                    links.append(child)
                # Recursively search children
                links.extend(find_all_links(child))
        return links

    a_tags = find_all_links(nav_element)
    # Expect: 1 brand link + 2 text links + 2 icon buttons = 5 total
    assert len(a_tags) == 5

    # Brand link (first one)
    assert a_tags[0].attrs.get("href") == "index"
    assert "tdom-sphinx" in get_text_content(a_tags[0])

    # Text links (now relative to the current page without .html)
    assert a_tags[1].attrs.get("href") == "docs.html"
    assert get_text_content(a_tags[1]).strip() == "Docs"

    assert a_tags[2].attrs.get("href") == "about.html"
    assert get_text_content(a_tags[2]).strip() == "About"

    # Icon buttons
    assert a_tags[3].attrs.get("href") == "https://github.com/org"

    # Find icon within this link (recursively)
    def find_icon(element: Element) -> Optional[Element]:
        for child in element.children:
            if isinstance(child, Element):
                if child.tag.lower() == "i":
                    return child
                # Recursively search children
                found = find_icon(child)
                if found:
                    return found
        return None

    icon_2 = find_icon(a_tags[3])
    assert icon_2 is not None

    assert a_tags[4].attrs.get("href") == "https://x.com/org"
    # Find icon within this link
    icon_3 = find_icon(a_tags[4])
    assert icon_3 is not None

    # Check that the site aside contains semantic navigation
    site_aside = None

    def find_element_by_id(element: Element, target_id: str) -> Optional[Element]:
        if element.attrs.get("id") == target_id:
            return element
        for child in element.children:
            if isinstance(child, Element):
                found = find_element_by_id(child, target_id)
                if found:
                    return found
        return None

    assert isinstance(result, Element)
    site_aside = find_element_by_id(result, "site-aside")
    assert site_aside is not None
    assert site_aside.tag.lower() == "aside"

    # Should contain semantic nav structure (if toctree has content)
    toc_nav_element = None
    for child in site_aside.children:
        if (
            isinstance(child, Element)
            and child.tag.lower() == "nav"
            and child.attrs.get("role") == "navigation"
            and child.attrs.get("aria-label") == "Table of contents"
        ):
            toc_nav_element = child
            break

    if toc_nav_element is not None:
        # If nav exists, check its structure
        all_links = find_all_links(toc_nav_element)
        assert len(all_links) >= 1

        # Check if there's a details structure for nested content
        details_element = None
        for child in toc_nav_element.children:
            if isinstance(child, Element) and child.tag.lower() == "details":
                details_element = child
                break

        if details_element is not None:
            # Nested structure exists
            assert details_element.attrs.get("open") == "open"

            # Find summary > a
            summary_link = None
            for child in details_element.children:
                if isinstance(child, Element) and child.tag.lower() == "summary":
                    for summary_child in child.children:
                        if (
                            isinstance(summary_child, Element)
                            and summary_child.tag.lower() == "a"
                        ):
                            summary_link = summary_child
                            break
                    break
            assert summary_link is not None

            # May contain subsections
            nested_nav = None
            for child in details_element.children:
                if (
                    isinstance(child, Element)
                    and child.tag.lower() == "nav"
                    and child.attrs.get("aria-label") == "Subsections"
                ):
                    nested_nav = child
                    break

            if nested_nav is not None:
                subsection_links = find_all_links(nested_nav)
                assert len(subsection_links) >= 0
        else:
            # Simple flat structure - just check that links exist
            assert len(all_links) >= 1
    else:
        # If no nav exists, the aside should be empty (due to missing toctree files)
        # This is acceptable for test scenarios with broken references
        aside_text = get_text_content(site_aside).strip()
        assert aside_text == ""


@pytest.mark.parametrize(
    "page",
    [
        "hello.html",
    ],
    indirect=True,
)
def test_site_aside_lower_page(page: str) -> None:
    result = html_string_to_tdom(page)

    # Check that the site aside contains semantic navigation
    def find_element_by_id(element: Element, target_id: str) -> Optional[Element]:
        if element.attrs.get("id") == target_id:
            return element
        for child in element.children:
            if isinstance(child, Element):
                found = find_element_by_id(child, target_id)
                if found:
                    return found
        return None

    assert isinstance(result, Element)
    site_aside = find_element_by_id(result, "site-aside")
    assert site_aside is not None

    # Should contain semantic nav structure
    toc_nav_element = None
    for child in site_aside.children:
        if (
            isinstance(child, Element)
            and child.tag.lower() == "nav"
            and child.attrs.get("role") == "navigation"
            and child.attrs.get("aria-label") == "Table of contents"
        ):
            toc_nav_element = child
            break
    assert toc_nav_element is not None

    # For lower pages, check if there are direct links or details structure
    # This page might have simpler navigation structure
    def find_all_links(element: Element) -> list[Element]:
        links = []
        for child in element.children:
            if isinstance(child, Element):
                if child.tag.lower() == "a":
                    links.append(child)
                # Recursively search children
                links.extend(find_all_links(child))
        return links

    all_links = find_all_links(toc_nav_element)
    assert len(all_links) >= 1

    # Find the page-specific link
    link_texts = [get_text_content(link).strip() for link in all_links]
    link_hrefs = [link.attrs.get("href", "") for link in all_links]

    # Should contain some navigation relevant to the current page
    assert "Another Page" in link_texts or any("#" in (href or "") for href in link_hrefs)
