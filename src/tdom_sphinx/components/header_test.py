from bs4 import BeautifulSoup
from tdom import html

from tdom_sphinx.components.header import Header
from tdom_sphinx.models import NavbarConfig


def test_header_wraps_navbar_and_is_fixed(page_context):
    # Provide an empty navbar to keep predictable rendering
    navbar_cfg = NavbarConfig(links=[], buttons=[])

    result = html(t"""
        <{Header} page_context={page_context} navbar={navbar_cfg} />
    """)

    soup = BeautifulSoup(str(result), "html.parser")

    header = soup.select_one("header.is-fixed")
    assert header is not None

    nav = header.select_one("nav")
    assert nav is not None

    # Brand should come from site_title and href should be "/"
    brand_anchor = nav.select_one("ul:nth-of-type(1) li a")
    assert brand_anchor is not None
    assert brand_anchor.get("href") == "/"
    assert nav.select_one("ul:nth-of-type(1) li strong").text == "My Test Site"
