"""Integration test for basic Sphinx theme functionality."""

import pytest
from bs4 import BeautifulSoup

pytestmark = pytest.mark.sphinx("html", testroot="basic-sphinx")


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_index(page: str, soup: BeautifulSoup) -> None:
    """Ensure basics are in the page."""
    title = soup.title
    assert title is not None
    assert title.get_text(strip=True) == "Hello PicoCSS - tdom-sphinx"
