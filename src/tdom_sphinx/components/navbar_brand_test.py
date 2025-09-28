from bs4 import BeautifulSoup
from tdom import html

from tdom_sphinx.components.navbar_brand import NavbarBrand


def test_navbar_brand_renders_brand_link_and_title(page_context):
    result = html(
        t"""
        <{NavbarBrand} page_context={page_context} href="/" title="My Site" />
        """
    )

    soup = BeautifulSoup(str(result), "html.parser")

    ul = soup.select_one("ul")
    assert ul is not None

    a_tag = ul.select_one("li a")
    assert a_tag is not None
    # Since page_context.pagename is "index", "/" should be converted to "index" by relative_tree
    assert a_tag.get("href") == "index"

    strong = a_tag.select_one("strong")
    assert strong is not None
    assert strong.text == "My Site"
