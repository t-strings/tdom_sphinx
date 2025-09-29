from tdom import html

from tdom_sphinx.aria_testing import get_by_role
from tdom_sphinx.aria_testing.utils import get_text_content
from tdom_sphinx.components.navbar_brand import NavbarBrand


def test_navbar_brand_renders_brand_link_and_title(page_context):
    result = html(
        t"""
        <{NavbarBrand} pagename={page_context.pagename} href="/" title="My Site" />
        """
    )

    ul_element = get_by_role(result, "list")
    assert ul_element.tag == "ul"

    # Find the link containing the brand text
    link_element = get_by_role(result, "link")
    assert link_element.tag == "a"
    # Since page_context.pagename is "index", "/" should be converted to "index" by relative_tree
    assert link_element.attrs.get("href") == "index"

    # Check that the link contains the expected text
    link_text = get_text_content(link_element).strip()
    assert "My Site" in link_text

    # Verify the link contains a strong element with the title
    link_html = str(link_element)
    assert "<strong>My Site</strong>" in link_html
