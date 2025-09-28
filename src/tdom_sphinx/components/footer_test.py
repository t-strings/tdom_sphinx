from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup, Tag
from tdom import html

from tdom_sphinx.components.footer import Footer
from tdom_sphinx.models import PageContext, SiteConfig


def test_footer_contains_centered_copyright(
    site_config: SiteConfig, page_context: PageContext
):
    result = html(t"""
        <{Footer} site_config={site_config} page_context={page_context} />
    """)

    soup = BeautifulSoup(str(result), "html.parser")

    footer_element: Optional[Tag] = soup.select_one("footer")
    assert footer_element is not None

    p_element: Optional[Tag] = footer_element.select_one("p")
    assert p_element is not None
    # Check if the style is centered
    assert p_element.get("style") == "text-align: center"

    text = p_element.text
    assert text.startswith("© ")
    assert str(datetime.now().year) in text
    assert "My Test Site" in text
