"""Integration test that verifies navbar links/buttons appear in built HTML."""

import pytest
from bs4 import BeautifulSoup

pytestmark = pytest.mark.sphinx("html", testroot="navbar-sphinx")


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_navbar_links_and_buttons_render(page: str) -> None:
    soup = BeautifulSoup(page, "html.parser")

    # Find the nav inside the header
    nav = soup.select_one("header nav")
    assert nav is not None

    # First two links should be the text links
    a_tags = nav.select("ul:nth-of-type(2) li a")
    # Expect: 2 text links + 2 icon buttons
    assert len(a_tags) == 4

    # Text links
    assert a_tags[0].get("href") == "/docs.html"
    assert a_tags[0].text.strip() == "Docs"

    assert a_tags[1].get("href") == "/about.html"
    assert a_tags[1].text.strip() == "About"

    # Icon buttons
    assert a_tags[2].get("href") == "https://github.com/org"
    assert a_tags[2].select_one("i") is not None

    assert a_tags[3].get("href") == "https://x.com/org"
    assert a_tags[3].select_one("i") is not None
