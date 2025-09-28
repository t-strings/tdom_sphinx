"""Ensure the Sphinx Template Bridge is replaced and uses the container."""

from typing import Optional

from bs4 import BeautifulSoup, Tag, ResultSet

from tdom_sphinx.models import PageContext
from tdom_sphinx.template_bridge import TdomBridge


def test_render_default_view(sphinx_context: dict) -> None:
    """Test that render gets a DefaultView using shared fixtures."""

    tb = TdomBridge()
    result = tb.render("some_template", sphinx_context)
    soup = BeautifulSoup(result, "html.parser")

    element: Optional[Tag] = soup.select_one("title")
    assert element is not None
    assert element.get_text(strip=True) == "My Test Page - My Test Site"
    stylesheets: Optional[Tag] = soup.select_one("link[rel='stylesheet']")
    assert stylesheets is not None
    assert stylesheets["href"] == "_static/tdom-sphinx.css"


def test_deep_static_nesting(sphinx_context: dict) -> None:
    """Test that render gets a DefaultView using shared fixtures."""

    # Change this path to be several folders down and see if the
    # relative static path is correct
    page_context = PageContext(
        body="<p>Hello World</p>",
        css_files=(),
        display_toc=False,
        js_files=(),
        pagename="foo/bar/baz/home.html",
        page_source_suffix=".rst",
        sourcename=None,
        templatename="page.html",
        title="My Test Page",
        toc=None,
    )
    sphinx_context["page_context"] = page_context

    tb = TdomBridge()
    result = tb.render("some_template", sphinx_context)
    soup = BeautifulSoup(result, "html.parser")

    element: Optional[Tag] = soup.select_one("title")
    assert element is not None
    assert element.get_text(strip=True) == "My Test Page - My Test Site"

    stylesheets: ResultSet[Tag] = soup.select("link[rel='stylesheet']")  # noqa: F821
    assert stylesheets
    assert stylesheets[0]["href"] == "../../../_static/tdom-sphinx.css"
