from typing import Optional

from bs4 import BeautifulSoup, Tag
from tdom import html

from tdom_sphinx.components.site_aside import SiteAside


def test_site_aside_renders_static_content(page_context):
    result = html(
        t"""
        <{SiteAside} page_context={page_context} />
        """
    )

    soup = BeautifulSoup(str(result), "html.parser")

    aside_element: Optional[Tag] = soup.select_one("aside")
    assert aside_element is not None

    # Check for Quick Links section
    headings = aside_element.select("h3")
    assert len(headings) >= 2
    assert headings[0].text == "Quick Links"
    assert headings[1].text == "Resources"

    # Check for links in Quick Links - URLs should be relative to current page
    # Since page_context.pagename is "index", "/docs/" becomes "docs", etc.
    quick_links = aside_element.select("ul")[0]
    links = quick_links.select("li a")
    assert len(links) >= 4
    assert links[0].text == "Documentation"
    assert links[0].get("href") == "docs"
    assert links[1].text == "API Reference"
    assert links[1].get("href") == "api"

    # Check for links in Resources
    resources = aside_element.select("ul")[1]
    resource_links = resources.select("li a")
    assert len(resource_links) >= 3
    assert resource_links[0].text == "Downloads"
    assert resource_links[0].get("href") == "downloads"