from bs4 import BeautifulSoup
from tdom import html

from tdom_sphinx.components.navbar_brand_logo import NavbarBrandLogo
from tdom_sphinx.theme_config import NavbarBrandLogoConfig


def test_navbar_brand_logo_renders_with_expected_attributes():
    # Simple pathto function like Sphinx provides; identity for tests
    def pathto(filename: str, flag: int | None = 0) -> str:
        return filename

    config = NavbarBrandLogoConfig(
        src="/static/logo.svg",
        alt="My Site",
        width=128,
        height=32,
    )

    result = html(
        t"""
        <{NavbarBrandLogo}
            pathto={pathto}
            config={config}
        />
        """
    )

    soup = BeautifulSoup(str(result), "html.parser")

    a = soup.select_one("a.navbar-item")
    assert a is not None
    assert a.get("href") == "/"

    img = a.select_one("img")
    assert img is not None
    assert img.get("src") == "/static/logo.svg"
    assert img.get("alt") == "My Site"
    assert img.get("width") == "128"
    assert img.get("height") == "32"
