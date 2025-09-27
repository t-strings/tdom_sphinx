from bs4 import BeautifulSoup
from tdom import html

from conftest import pathto
from tdom_sphinx.components.base_layout import BaseLayout
from tdom_sphinx.models import TdomContext


def test_base_layout_html5_structure(tdom_context: TdomContext) -> None:
    result = html(t"<{BaseLayout} context={tdom_context} />")
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    assert "<!DOCTYPE html>" in html_string
    assert soup.find("html") is not None
    assert soup.find("html").get("lang") == "EN"
    assert soup.find("head") is not None
    assert soup.find("body") is not None


def test_base_layout_head_section(tdom_context: TdomContext) -> None:
    result = html(t"<{BaseLayout} context={tdom_context} />")
    soup = BeautifulSoup(str(result), "html.parser")

    head = soup.find("head")
    assert head is not None

    # meta tags
    assert head.find("meta", {"charset": "utf-8"}) is not None
    viewport_meta = head.find("meta", {"name": "viewport"})
    assert viewport_meta is not None
    assert viewport_meta.get("content") == "width=device-width, initial-scale=1"

    # title uses site title if present in context
    title_tag = head.find("title")
    assert title_tag is not None
    assert title_tag.text == "My Test Page - My Test Site"

    # stylesheets and favicon
    css_link = head.find("link", {"rel": "stylesheet"})
    assert css_link is not None
    assert css_link.get("href") == "_static/tdom-sphinx.css"

    favicon_link = head.find("link", {"rel": "icon"})
    assert favicon_link is not None
    assert favicon_link.get("href") == "_static/favicon.ico"
    assert favicon_link.get("type") == "image/x-icon"


def test_base_layout_body_structure(tdom_context: TdomContext) -> None:
    result = html(t"<{BaseLayout} context={tdom_context} />")
    soup = BeautifulSoup(str(result), "html.parser")

    body = soup.find("body")
    assert body is not None

    # Header component
    header = body.find("header", {"class": "is-fixed"})
    assert header is not None

    # Main component contains the body HTML
    main = body.find("main")
    assert main is not None
    p = main.find("p")
    assert p is not None and p.text == "Hello World"

    # Footer component present
    footer = body.find("footer")
    assert footer is not None


def test_base_layout_body_content_extraction(tdom_context: TdomContext) -> None:
    tdom_context.page_context["body"] = (
        "<div><h2>Section Title</h2><p>Paragraph content</p><ul><li>List item</li></ul></div>"
    )
    result = html(t"<{BaseLayout} context={tdom_context} />")
    soup = BeautifulSoup(str(result), "html.parser")

    main = soup.find("main")
    assert main is not None

    h2 = main.find("h2")
    assert h2 is not None and h2.text == "Section Title"
    p = main.find("p")
    assert p is not None and p.text == "Paragraph content"
    ul = main.find("ul")
    assert ul is not None
    li = ul.find("li")
    assert li is not None and li.text == "List item"


def test_base_layout_no_body_content(tdom_context: TdomContext) -> None:
    tdom_context.page_context["title"] = "No Body Test"
    # body remains default from fixture: <p>Hello World</p>
    result = html(t"<{BaseLayout} context={tdom_context} />")
    soup = BeautifulSoup(str(result), "html.parser")

    main = soup.find("main")
    assert main is not None
    p = main.find("p")
    assert p is not None
    assert p.text.strip() == "Hello World"


def test_base_layout_no_sphinx_context(tdom_context: TdomContext) -> None:
    tdom_context.page_context["title"] = "No Sphinx Context"
    del tdom_context.page_context["body"]

    result = html(t"<{BaseLayout} context={tdom_context} />")
    soup = BeautifulSoup(str(result), "html.parser")

    title_tag = soup.find("title")
    assert title_tag.text == "No Sphinx Context - My Test Site"

    # Body is missing; Main renders empty when no body provided
    main = soup.find("main")
    assert main is not None
    assert main.get_text().strip() == ""


def test_base_layout_complex_context(tdom_context: TdomContext) -> None:
    tdom_context.page_context = {
        "title": "Complex Test",
        "body": "<p>Main content</p>",
        "pagename": "index",
        "docname": "index",
        "other_sphinx_data": "ignored",
        "extra_data": "should be ignored",
        "nested": {"data": "also ignored"},
        "pathto": pathto,
        "site_title": "My Test Site",
    }

    result = html(t"<{BaseLayout} context={tdom_context} />")
    html_string = str(result)
    soup = BeautifulSoup(html_string, "html.parser")

    title_tag = soup.find("title")
    assert title_tag.text == "Complex Test - My Test Site"

    main = soup.find("main")
    assert main is not None
    assert "Main content" in main.get_text()

    assert "ignored" not in html_string
    assert "should be ignored" not in html_string


def test_base_layout_html_escaping(tdom_context: TdomContext) -> None:
    tdom_context.page_context["body"] = (
        "<p>Content with <strong>bold</strong> and <em>italic</em> text</p>"
    )

    result = html(t"<{BaseLayout} context={tdom_context} />")
    soup = BeautifulSoup(str(result), "html.parser")

    main = soup.find("main")
    assert main is not None

    strong = main.find("strong")
    assert strong is not None and strong.text == "bold"
    em = main.find("em")
    assert em is not None and em.text == "italic"


def test_base_layout_static_asset_paths(tdom_context: TdomContext) -> None:
    tdom_context.page_context["title"] = "Asset Path Test"

    result = html(t"<{BaseLayout} context={tdom_context} />")
    soup = BeautifulSoup(str(result), "html.parser")

    css_link = soup.find("link", {"rel": "stylesheet"})
    assert css_link.get("href") == "_static/tdom-sphinx.css"

    favicon_link = soup.find("link", {"rel": "icon"})
    assert favicon_link.get("href") == "_static/favicon.ico"
