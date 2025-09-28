from typing import Optional

from bs4 import BeautifulSoup, Tag
from tdom import html

from tdom_sphinx.components.navbar_links import NavbarLinks
from tdom_sphinx.models import Link, IconLink


def test_navbar_links_renders_links_and_buttons(page_context):
    links = [
        Link(href="/docs", style="", text="Docs"),
        Link(href="/about", style="btn", text="About"),
    ]
    buttons = [
        IconLink(href="https://github.com/org", color="#111", icon_class="fa fa-github"),
        IconLink(href="https://x.com/org", color="#08f", icon_class="fa fa-twitter"),
    ]

    result = html(
        t"""
        <{NavbarLinks} page_context={page_context} links={links} buttons={buttons} />
        """
    )

    soup = BeautifulSoup(str(result), "html.parser")

    ul_element: Optional[Tag] = soup.select_one("ul")
    assert ul_element is not None

    a_tags = ul_element.select("li a")
    # 2 text links + 2 button links
    assert len(a_tags) == 4

    # Check text links
    assert a_tags[0].get("href") == "docs"
    assert a_tags[0].get_text(strip=True) == "Docs"

    assert a_tags[1].get("href") == "about"
    assert a_tags[1].get_text(strip=True) == "About"

    # Check buttons have icons
    assert a_tags[2].get("href") == "https://github.com/org"
    icon_2: Optional[Tag] = a_tags[2].select_one("i")
    assert icon_2 is not None

    assert a_tags[3].get("href") == "https://x.com/org"
    icon_3: Optional[Tag] = a_tags[3].select_one("i")
    assert icon_3 is not None
