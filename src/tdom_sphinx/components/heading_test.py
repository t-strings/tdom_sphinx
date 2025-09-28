from typing import Optional

from bs4 import BeautifulSoup, Tag
from tdom import html

from tdom_sphinx.components.heading import Heading
from tdom_sphinx.models import PageContext, SiteConfig


def test_heading_wraps_navbar_and_is_fixed(
    site_config: SiteConfig, page_context: PageContext
):
    result = html(t"""
        <{Heading} page_context={page_context} site_config={site_config} />
    """)

    soup = BeautifulSoup(str(result), "html.parser")

    header_element: Optional[Tag] = soup.select_one("header.is-fixed")
    assert header_element is not None

    nav_element: Optional[Tag] = header_element.select_one("nav")
    assert nav_element is not None

    # Brand should come from site_title, and href should be relative to the current page
    # Since page_context.pagename is "index" and brand href is "/", it becomes "index"
    brand_anchor: Optional[Tag] = nav_element.select_one("ul:nth-of-type(1) li a")
    assert brand_anchor is not None
    assert brand_anchor.get("href") == "index"

    strong_element: Optional[Tag] = nav_element.select_one("ul:nth-of-type(1) li strong")
    assert strong_element is not None
    assert strong_element.get_text(strip=True) == "My Test Site"