from bs4 import BeautifulSoup
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

    header = soup.select_one("header.is-fixed")
    assert header is not None

    nav = header.select_one("nav")
    assert nav is not None

    # Brand should come from site_title, and href should be relative to the current page
    # Since page_context.pagename is "index" and brand href is "/", it becomes "index"
    brand_anchor = nav.select_one("ul:nth-of-type(1) li a")
    assert brand_anchor is not None
    assert brand_anchor.get("href") == "index"
    assert nav.select_one("ul:nth-of-type(1) li strong").text == "My Test Site"