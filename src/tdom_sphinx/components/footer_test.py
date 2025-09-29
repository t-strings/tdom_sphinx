from datetime import datetime

from tdom import html

from tdom_sphinx.aria_testing import get_by_role
from tdom_sphinx.aria_testing.utils import get_text_content
from tdom_sphinx.components.footer import Footer
from tdom_sphinx.models import PageContext, SiteConfig


def test_footer_contains_centered_copyright(
    site_config: SiteConfig, page_context: PageContext
):
    result = html(t"""
        <{Footer} site_config={site_config} page_context={page_context} />
    """)

    footer_element = get_by_role(result, "contentinfo")
    assert footer_element.tag == "footer"

    # Find the paragraph within the footer
    # Footer typically contains copyright info as text
    text = get_text_content(footer_element).strip()
    assert text.startswith("© ")
    assert str(datetime.now().year) in text
    assert "My Test Site" in text

    # Check the style attribute on the paragraph
    # Since we can't easily query by tag with aria_testing, check the HTML structure
    footer_html = str(footer_element)
    assert 'style="text-align: center"' in footer_html
