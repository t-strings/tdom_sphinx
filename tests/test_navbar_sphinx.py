"""Integration test that verifies navbar links/buttons appears in built HTML."""

import pytest
from bs4 import BeautifulSoup

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
    nav = soup.select_one("header nav")
    assert nav is not None

    # The first two links should be the text links
    a_tags = nav.select("ul:nth-of-type(2) li a")
    # Expect: 2 text links + 2 icon buttons
    assert len(a_tags) == 4

    # Text links (now relative to the current page without .html)
    assert a_tags[0].get("href") == "docs.html"
    assert a_tags[0].text.strip() == "Docs"

    assert a_tags[1].get("href") == "about.html"
    assert a_tags[1].text.strip() == "About"

    # Icon buttons
    assert a_tags[2].get("href") == "https://github.com/org"
    assert a_tags[2].select_one("i") is not None

    assert a_tags[3].get("href") == "https://x.com/org"
    assert a_tags[3].select_one("i") is not None

    # Check that the site aside contains the Sphinx toctree
    site_aside = soup.select_one("aside#site-aside")
    assert site_aside is not None

    # Check that the aside contains toctree links
    toctree_links = site_aside.select("a")
    assert len(toctree_links) == 1

    # Verify that the toctree contains expected content
    # The toctree shows the local navigation for the current page
    link_texts = [link.text.strip() for link in toctree_links]
    link_hrefs = [link.get("href") for link in toctree_links]

    # Should contain the main page link (root page title)
    assert link_texts[0] == "Navbar Sphinx Root"

    # Should contain fragment links (# for current page)
    assert "#" in link_hrefs


@pytest.mark.parametrize(
    "page",
    [
        "hello.html",
    ],
    indirect=True,
)
def test_site_aside_lower_page(page: str) -> None:
    soup = BeautifulSoup(page, "html.parser")

    # Check that the site aside contains the Sphinx toctree
    site_aside = soup.select_one("aside#site-aside")
    assert site_aside is not None

    # Check that the aside contains toctree links
    toctree_links = site_aside.select("a")
    assert len(toctree_links) == 1

    # Verify that the toctree contains expected content
    # The toctree shows the local navigation for the current page
    link_texts = [link.text.strip() for link in toctree_links]
    link_hrefs = [link.get("href") for link in toctree_links]

    # Should contain the main page link (root page title)
    assert link_texts[0] == "Another Page"

    # Should contain fragment links (# for current page)
    assert "#" in link_hrefs
