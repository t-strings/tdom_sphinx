from bs4 import BeautifulSoup
from tdom import html

from tdom_sphinx.components.navbar_links import NavbarLinks
from tdom_sphinx.models import Link, IconLink


def test_navbar_links_renders_links_and_buttons():
    links = [
        Link(href="/docs", style="", text="Docs"),
        Link(href="/about", style="btn", text="About"),
    ]
    buttons = [
        IconLink(href="https://github.com/org", color="#111", icon_class="fa fa-github"),
        IconLink(href="https://x.com/org", color="#08f", icon_class="fa fa-twitter"),
    ]

    def pathto(filename: str, flag: int = 0) -> str:
        return filename

    result = html(
        t"""
        <{NavbarLinks} pathto={pathto} links={links} buttons={buttons} />
        """
    )

    soup = BeautifulSoup(str(result), "html.parser")

    ul = soup.select_one("ul")
    assert ul is not None

    a_tags = ul.select("li a")
    # 2 text links + 2 button links
    assert len(a_tags) == 4

    # Check text links
    assert a_tags[0].get("href") == "/docs"
    assert a_tags[0].text == "Docs"

    assert a_tags[1].get("href") == "/about"
    assert a_tags[1].text == "About"

    # Check buttons have icons
    assert a_tags[2].get("href") == "https://github.com/org"
    assert a_tags[2].select_one("i") is not None

    assert a_tags[3].get("href") == "https://x.com/org"
    assert a_tags[3].select_one("i") is not None
