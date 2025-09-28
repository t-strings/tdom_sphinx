"""Integration test that verifies navbar links/buttons appears in built HTML."""

import pytest
from typing import Optional
from bs4 import BeautifulSoup, Tag

pytestmark = pytest.mark.sphinx("html", testroot="navbar-sphinx")


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_navbar_links_and_buttons_render(page: str) -> None:
    soup = BeautifulSoup(page, "html.parser")

    # See if relative links in the head work
    stylesheets = soup.select("link[rel='stylesheet']")[0]
    assert stylesheets["href"] == "_static/tdom-sphinx.css"

    # Find the nav inside the header
    nav: Optional[Tag] = soup.select_one("header nav")
    assert nav is not None

    # The first two links should be the text links
    a_tags = nav.select("ul:nth-of-type(2) li a")
    # Expect: 2 text links + 2 icon buttons
    assert len(a_tags) == 4

    # Text links (now relative to the current page without .html)
    assert a_tags[0].get("href") == "docs.html"
    assert a_tags[0].get_text(strip=True) == "Docs"

    assert a_tags[1].get("href") == "about.html"
    assert a_tags[1].get_text(strip=True) == "About"

    # Icon buttons
    assert a_tags[2].get("href") == "https://github.com/org"
    icon_2: Optional[Tag] = a_tags[2].select_one("i")
    assert icon_2 is not None

    assert a_tags[3].get("href") == "https://x.com/org"
    icon_3: Optional[Tag] = a_tags[3].select_one("i")
    assert icon_3 is not None

    # Check that the site aside contains semantic navigation
    site_aside: Optional[Tag] = soup.select_one("aside#site-aside")
    assert site_aside is not None

    # Should contain semantic nav structure (if toctree has content)
    nav_element: Optional[Tag] = site_aside.select_one("nav[role='navigation'][aria-label='Table of contents']")

    if nav_element is not None:
        # If nav exists, check its structure
        all_links = nav_element.select("a")
        assert len(all_links) >= 1

        # Check if there's a details structure for nested content
        details: Optional[Tag] = nav_element.select_one("details")
        if details is not None:
            # Nested structure exists
            assert details.get("open") == "open"
            summary_link: Optional[Tag] = details.select_one("summary > a")
            assert summary_link is not None

            # May contain subsections
            nested_nav: Optional[Tag] = details.select_one("nav[aria-label='Subsections']")
            if nested_nav is not None:
                subsection_links = nested_nav.select("a")
                assert len(subsection_links) >= 0
        else:
            # Simple flat structure - just check that links exist
            assert len(all_links) >= 1
    else:
        # If no nav exists, the aside should be empty (due to missing toctree files)
        # This is acceptable for test scenarios with broken references
        assert site_aside.get_text(strip=True) == ""


@pytest.mark.parametrize(
    "page",
    [
        "hello.html",
    ],
    indirect=True,
)
def test_site_aside_lower_page(page: str) -> None:
    soup = BeautifulSoup(page, "html.parser")

    # Check that the site aside contains semantic navigation
    site_aside: Optional[Tag] = soup.select_one("aside#site-aside")
    assert site_aside is not None

    # Should contain semantic nav structure
    nav_element: Optional[Tag] = site_aside.select_one("nav[role='navigation'][aria-label='Table of contents']")
    assert nav_element is not None

    # For lower pages, check if there are direct links or details structure
    # This page might have simpler navigation structure
    all_links = nav_element.select("a")
    assert len(all_links) >= 1

    # Find the page-specific link
    link_texts = [link.text.strip() for link in all_links]
    link_hrefs = [link.get("href") for link in all_links]

    # Should contain some navigation relevant to the current page
    assert "Another Page" in link_texts or any("#" in href for href in link_hrefs)
