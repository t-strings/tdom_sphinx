from bs4 import BeautifulSoup
from tdom import html

from tdom_sphinx.components.navbar import Navbar
from tdom_sphinx.models import TdomContext, Link, IconLink


def test_navbar_structure_with_brand_and_links(tdom_context: TdomContext):
    # Configure links and buttons on the Sphinx config inside the context
    tdom_context.config.nav_links = [
        Link(href="/docs", style="", text="Docs"),
        Link(href="/about", style="", text="About"),
    ]
    tdom_context.config.nav_buttons = [
        IconLink(
            href="https://github.com/org", color="#000", icon_class="fa fa-github"
        ),
    ]

    result = html(
        t"""
        <{Navbar} brand_href="/" brand_title="My Site" context={tdom_context} />
        """
    )

    soup = BeautifulSoup(str(result), "html.parser")

    nav = soup.select_one("nav")
    assert nav is not None

    uls = nav.select("ul")
    assert len(uls) == 2

    # First ul contains the brand link and strong title
    brand_anchor = uls[0].select_one("li a")
    assert brand_anchor is not None
    assert brand_anchor.get("href") == "/"
    assert uls[0].select_one("li strong").text == "My Site"

    # Second ul contains the links and one button icon
    items = uls[1].select("li a")
    # Two text links + one icon button anchor
    assert len(items) == 3
    assert items[0].get("href") == "/docs"
    assert items[0].text == "Docs"
    assert items[1].get("href") == "/about"
    assert items[1].text == "About"
    # Button icon
    assert items[2].get("href") == "https://github.com/org"
    icon = items[2].select_one("i")
    assert icon is not None
