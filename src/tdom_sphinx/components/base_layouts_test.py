from typing import Optional

from bs4 import BeautifulSoup, Tag
from tdom import html

from tdom_sphinx.components.base_layout import BaseLayout
from tdom_sphinx.models import PageContext, SiteConfig


def test_base_layout_html5_structure(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    result = html(
        t"<{BaseLayout} page_context={page_context} site_config={site_config} />"
    )
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    assert "<!DOCTYPE html>" in html_string
    html_element: Optional[Tag] = soup.find("html")
    assert html_element is not None
    assert html_element.get("lang") == "EN"
    assert soup.find("head") is not None
    assert soup.find("body") is not None


def test_base_layout_head_section(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    result = html(
        t"<{BaseLayout} page_context={page_context} site_config={site_config} />"
    )
    soup = BeautifulSoup(str(result), "html.parser")

    head_element: Optional[Tag] = soup.find("head")
    assert head_element is not None

    # meta tags
    assert head_element.find("meta", {"charset": "utf-8"}) is not None
    viewport_meta = head_element.find("meta", {"name": "viewport"})
    assert viewport_meta is not None
    assert viewport_meta.get("content") == "width=device-width, initial-scale=1"

    # title uses site title if present in context
    title_element: Optional[Tag] = head_element.find("title")
    assert title_element is not None
    assert title_element.get_text(strip=True) == "My Test Page - My Test Site"

    # stylesheets and favicon
    css_link: Optional[Tag] = head_element.find("link", {"rel": "stylesheet"})
    assert css_link is not None
    assert css_link.get("href") == "_static/tdom-sphinx.css"

    favicon_link: Optional[Tag] = head_element.find("link", {"rel": "icon"})
    assert favicon_link is not None
    assert favicon_link.get("href") == "_static/favicon.ico"
    assert favicon_link.get("type") == "image/x-icon"


def test_base_layout_body_structure(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    result = html(
        t"<{BaseLayout} page_context={page_context} site_config={site_config} />"
    )
    soup = BeautifulSoup(str(result), "html.parser")

    body_element: Optional[Tag] = soup.find("body")
    assert body_element is not None

    # Heading component
    header_element: Optional[Tag] = body_element.find("header", {"class": "is-fixed"})
    assert header_element is not None

    # Main component contains the body HTML
    main_element: Optional[Tag] = body_element.find("main")
    assert main_element is not None
    p_element: Optional[Tag] = main_element.find("p")
    assert p_element is not None and p_element.get_text(strip=True) == "Hello World"

    # Footer component present
    footer_element: Optional[Tag] = body_element.find("footer")
    assert footer_element is not None


def test_base_layout_body_content_extraction(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    local = PageContext(
        title="My Test Page",
        body="<div><h2>Section Title</h2><p>Paragraph content</p><ul><li>List item</li></ul></div>",
        css_files=(),
        display_toc=False,
        js_files=(),
        pagename="index",
        page_source_suffix=".rst",
        sourcename=None,
        templatename="page.html",
        toc="",
    )
    result = html(t"<{BaseLayout} page_context={local} site_config={site_config} />")
    soup = BeautifulSoup(str(result), "html.parser")

    main_element: Optional[Tag] = soup.find("main")
    assert main_element is not None

    h2_element: Optional[Tag] = main_element.find("h2")
    assert h2_element is not None and h2_element.get_text(strip=True) == "Section Title"
    p_element: Optional[Tag] = main_element.find("p")
    assert p_element is not None and p_element.get_text(strip=True) == "Paragraph content"
    ul_element: Optional[Tag] = main_element.find("ul")
    assert ul_element is not None
    li_element: Optional[Tag] = ul_element.find("li")
    assert li_element is not None and li_element.get_text(strip=True) == "List item"


def test_base_layout_no_body_content(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    local = PageContext(
        title="No Body Test",
        body="<p>Hello World</p>",
        css_files=(),
        display_toc=False,
        js_files=(),
        pagename="index",
        page_source_suffix=".rst",
        sourcename=None,
        templatename="page.html",
        toc="",
    )
    result = html(t"<{BaseLayout} page_context={local} site_config={site_config} />")
    soup = BeautifulSoup(str(result), "html.parser")

    main_element: Optional[Tag] = soup.find("main")
    assert main_element is not None
    p_element: Optional[Tag] = main_element.find("p")
    assert p_element is not None
    assert p_element.get_text(strip=True) == "Hello World"


def test_base_layout_no_sphinx_context(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    local = PageContext(
        title="No Sphinx Context",
        body="",
        css_files=(),
        display_toc=False,
        js_files=(),
        pagename="index",
        page_source_suffix=".rst",
        sourcename=None,
        templatename="page.html",
        toc="",
    )

    result = html(t"<{BaseLayout} page_context={local} site_config={site_config} />")
    soup = BeautifulSoup(str(result), "html.parser")

    title_element: Optional[Tag] = soup.find("title")
    assert title_element is not None
    assert title_element.get_text(strip=True) == "No Sphinx Context - My Test Site"

    # Body is missing; Main renders empty when no body provided
    main_element: Optional[Tag] = soup.find("main")
    assert main_element is not None
    assert main_element.get_text(strip=True) == ""


def test_base_layout_complex_context(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    page_context = PageContext(
        title="Complex Test",
        body="<p>Main content</p>",
        pagename="index",
        css_files=(),
        display_toc=False,
        js_files=(),
        page_source_suffix=".rst",
        sourcename=None,
        templatename="page.html",
        toc="",
    )

    result = html(
        t"<{BaseLayout} page_context={page_context} site_config={site_config} />"
    )
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    title_element: Optional[Tag] = soup.find("title")
    assert title_element is not None
    assert title_element.get_text(strip=True) == "Complex Test - My Test Site"

    main_element: Optional[Tag] = soup.find("main")
    assert main_element is not None
    assert "Main content" in main_element.get_text()

    assert "ignored" not in html_string
    assert "should be ignored" not in html_string


def test_base_layout_html_escaping(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    local = PageContext(
        title="My Test Page",
        body="<p>Content with <strong>bold</strong> and <em>italic</em> text</p>",
        css_files=(),
        display_toc=False,
        js_files=(),
        pagename="index",
        page_source_suffix=".rst",
        sourcename=None,
        templatename="page.html",
        toc="",
    )

    result = html(t"<{BaseLayout} page_context={local} site_config={site_config} />")
    soup = BeautifulSoup(str(result), "html.parser")

    main_element: Optional[Tag] = soup.find("main")
    assert main_element is not None

    strong_element: Optional[Tag] = main_element.find("strong")
    assert strong_element is not None and strong_element.get_text(strip=True) == "bold"
    em_element: Optional[Tag] = main_element.find("em")
    assert em_element is not None and em_element.get_text(strip=True) == "italic"


def test_base_layout_static_asset_paths(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    local = PageContext(
        title="Asset Path Test",
        body="",
        css_files=(),
        display_toc=False,
        js_files=(),
        pagename="index",
        page_source_suffix=".rst",
        sourcename=None,
        templatename="page.html",
        toc="",
    )

    result = html(t"<{BaseLayout} page_context={local} site_config={site_config} />")
    soup = BeautifulSoup(str(result), "html.parser")

    css_link: Optional[Tag] = soup.find("link", {"rel": "stylesheet"})
    assert css_link is not None
    assert css_link.get("href") == "_static/tdom-sphinx.css"

    favicon_link: Optional[Tag] = soup.find("link", {"rel": "icon"})
    assert favicon_link is not None
    assert favicon_link.get("href") == "_static/favicon.ico"
