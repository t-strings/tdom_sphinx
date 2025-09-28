from typing import Optional

from bs4 import BeautifulSoup, Tag
from tdom import html

from tdom_sphinx.components.navbar_brand import NavbarBrand


def test_navbar_brand_renders_brand_link_and_title(page_context):
    result = html(
        t"""
        <{NavbarBrand} page_context={page_context} href="/" title="My Site" />
        """
    )

    soup = BeautifulSoup(str(result), "html.parser")

    ul_element: Optional[Tag] = soup.select_one("ul")
    assert ul_element is not None

    a_element: Optional[Tag] = ul_element.select_one("li a")
    assert a_element is not None
    # Since page_context.pagename is "index", "/" should be converted to "index" by relative_tree
    assert a_element.get("href") == "index"

    strong_element: Optional[Tag] = a_element.select_one("strong")
    assert strong_element is not None
    assert strong_element.text == "My Site"
