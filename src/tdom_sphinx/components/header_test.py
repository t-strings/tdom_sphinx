from bs4 import BeautifulSoup
from tdom import html

from tdom_sphinx.components.header import Header
from tdom_sphinx.models import TdomContext


def test_header_wraps_navbar_and_is_fixed(tdom_context: TdomContext):
    # Configure some links/buttons to ensure NavbarLinks renders predictably
    tdom_context.config.nav_links = []
    tdom_context.config.nav_buttons = []

    result = html(t"""
        <{Header} context={tdom_context} />
    """)

    soup = BeautifulSoup(str(result), "html.parser")

    header = soup.select_one("header.is-fixed")
    assert header is not None

    nav = header.select_one("nav.container-fluid")
    assert nav is not None

    # Brand should come from site_title and href should be "/"
    brand_anchor = nav.select_one("ul:nth-of-type(1) li a")
    assert brand_anchor is not None
    assert brand_anchor.get("href") == "/"
    assert nav.select_one("ul:nth-of-type(1) li strong").text == "My Test Site"
