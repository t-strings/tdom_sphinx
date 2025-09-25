from bs4 import BeautifulSoup
from tdom import html

from tdom_sphinx.components.navbar_brand import NavbarBrand


def test_navbar_brand_renders_brand_link_and_title():
    def pathto(filename: str, flag: int = 0) -> str:
        return filename

    result = html(
        t"""
        <{NavbarBrand} pathto={pathto} href="/" title="My Site" />
        """
    )

    soup = BeautifulSoup(str(result), "html.parser")

    ul = soup.select_one("ul")
    assert ul is not None

    a_tag = ul.select_one("li a")
    assert a_tag is not None
    assert a_tag.get("href") == "/"

    strong = a_tag.select_one("strong")
    assert strong is not None
    assert strong.text == "My Site"
