from tdom import html

from tdom_sphinx.aria_testing import get_by_role, get_all_by_role
from tdom_sphinx.aria_testing.utils import get_text_content
from tdom_sphinx.components.heading import Heading
from tdom_sphinx.models import PageContext, SiteConfig


def test_heading_wraps_navbar_and_is_fixed(
    site_config: SiteConfig, page_context: PageContext
):
    result = html(t"""
        <{Heading} page_context={page_context} site_config={site_config} />
    """)

    header_element = get_by_role(result, "banner")
    assert header_element.tag == "header"

    # Check for the fixed class in the HTML
    header_html = str(header_element)
    assert "is-fixed" in header_html

    nav_element = get_by_role(result, "navigation")
    assert nav_element.tag == "nav"

    # Brand should come from site_title, and href should be relative to the current page
    # Since page_context.pagename is "index" and brand href is "/", it becomes "index"
    # Check that the nav contains the expected text
    nav_text = get_text_content(nav_element)
    assert "My Test Site" in nav_text

    # Find all links and check for the brand link with href="index"
    all_links = get_all_by_role(result, "link")
    brand_anchor = None
    for link in all_links:
        if link.attrs.get("href") == "index":
            brand_anchor = link
            break

    assert brand_anchor is not None
    assert brand_anchor.attrs.get("href") == "index"