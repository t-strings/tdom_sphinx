from datetime import datetime

from bs4 import BeautifulSoup
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

    footer = soup.select_one("footer")
    assert footer is not None

    p = footer.select_one("p")
    assert p is not None
    # Check if the style is centered
    assert p.get("style") == "text-align: center"

    text = p.text.strip()
    assert text.startswith("© ")
    assert str(datetime.now().year) in text
    assert "My Test Site" in text
