from typing import Optional

from bs4 import BeautifulSoup, Tag
from tdom import html

from tdom_sphinx.components.site_aside import SiteAside
from tdom_sphinx.models import PageContext


def test_site_aside_renders_empty_toctree(page_context):
    """Test SiteAside with empty toctree (default page_context fixture)."""
    result = html(
        t"""
        <{SiteAside} page_context={page_context} />
        """
    )

    soup = BeautifulSoup(str(result), "html.parser")

    aside_element: Optional[Tag] = soup.select_one("aside")
    assert aside_element is not None

    # With empty toc, aside should be essentially empty (just whitespace)
    assert aside_element.get_text(strip=True) == ""


def test_site_aside_renders_toctree_content():
    """Test SiteAside with actual toctree content."""
    # Create a PageContext with sample toctree HTML
    page_context_with_toc = PageContext(
        body="<p>Hello World</p>",
        css_files=(),
        display_toc=False,
        js_files=(),
        pagename="index",
        page_source_suffix=".rst",
        sourcename=None,
        templatename="page.html",
        title="My Test Page",
        toc='<ul><li><a href="/docs.html">Documentation</a></li><li><a href="/api.html">API</a></li></ul>',
    )

    result = html(
        t"""
        <{SiteAside} page_context={page_context_with_toc} />
        """
    )

    soup = BeautifulSoup(str(result), "html.parser")

    aside_element: Optional[Tag] = soup.select_one("aside")
    assert aside_element is not None

    # Check that toctree content is present
    links = aside_element.select("a")
    assert len(links) == 2

    # Note: relative_tree doesn't currently work with injected HTML via Markup
    # In practice, Sphinx-generated toctree HTML should already have correct relative URLs
    assert links[0].get("href") == "/docs.html"
    assert links[0].text == "Documentation"
    assert links[1].get("href") == "/api.html"
    assert links[1].text == "API"