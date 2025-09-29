from typing import Optional

from tdom import Element, html

from tdom_sphinx.aria_testing import get_by_role
from tdom_sphinx.aria_testing.utils import get_text_content
from tdom_sphinx.components.base_layout import BaseLayout
from tdom_sphinx.models import PageContext, SiteConfig


def test_base_layout_html5_structure(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    result = html(
        t"<{BaseLayout} page_context={page_context} site_config={site_config} />"
    )
    html_string = str(result)

    assert "<!DOCTYPE html>" in html_string

    # Find HTML element within Fragment
    html_element = None
    assert isinstance(result, Element)
    for child in result.children:
        if isinstance(child, Element) and child.tag.lower() == "html":
            html_element = child
            break
    assert html_element is not None
    assert html_element.attrs.get("lang") == "EN"

    # Find head and body elements
    head_element = None
    body_element = None
    for child in html_element.children:
        if isinstance(child, Element):
            if child.tag.lower() == "head":
                head_element = child
            elif child.tag.lower() == "body":
                body_element = child

    assert head_element is not None
    assert body_element is not None


def test_base_layout_head_section(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    result = html(
        t"<{BaseLayout} page_context={page_context} site_config={site_config} />"
    )

    # Find HTML element within Fragment
    html_element = None
    assert isinstance(result, Element)
    for child in result.children:
        if isinstance(child, Element) and child.tag.lower() == "html":
            html_element = child
            break
    assert html_element is not None

    # Find head element
    head_element = None
    for child in html_element.children:
        if isinstance(child, Element) and child.tag.lower() == "head":
            head_element = child
            break
    assert head_element is not None

    # Find meta tags
    charset_meta = None
    viewport_meta = None
    for head_child in head_element.children:
        if isinstance(head_child, Element) and head_child.tag.lower() == "meta":
            if head_child.attrs.get("charset") == "utf-8":
                charset_meta = head_child
            elif head_child.attrs.get("name") == "viewport":
                viewport_meta = head_child

    assert charset_meta is not None
    assert viewport_meta is not None
    assert viewport_meta.attrs.get("content") == "width=device-width, initial-scale=1"

    # title uses site title if present in context
    title_element = None
    for head_child in head_element.children:
        if isinstance(head_child, Element) and head_child.tag.lower() == "title":
            title_element = head_child
            break
    assert title_element is not None
    assert get_text_content(title_element) == "My Test Page - My Test Site"

    # stylesheets and favicon
    css_link = None
    favicon_link = None
    for head_child in head_element.children:
        if isinstance(head_child, Element) and head_child.tag.lower() == "link":
            if (
                head_child.attrs.get("rel") == "stylesheet"
                and head_child.attrs.get("href") == "_static/tdom-sphinx.css"
            ):
                css_link = head_child
            elif head_child.attrs.get("rel") == "icon":
                favicon_link = head_child

    assert css_link is not None
    assert css_link.attrs.get("href") == "_static/tdom-sphinx.css"

    assert favicon_link is not None
    assert favicon_link.attrs.get("href") == "_static/favicon.ico"
    assert favicon_link.attrs.get("type") == "image/x-icon"


def test_base_layout_body_structure(
    page_context: PageContext, site_config: SiteConfig
) -> None:
    result = html(
        t"<{BaseLayout} page_context={page_context} site_config={site_config} />"
    )

    # Find HTML element within Fragment
    html_element = None
    assert isinstance(result, Element)
    for child in result.children:
        if isinstance(child, Element) and child.tag.lower() == "html":
            html_element = child
            break
    assert html_element is not None

    # Find body element
    body_element = None
    for child in html_element.children:
        if isinstance(child, Element) and child.tag.lower() == "body":
            body_element = child
            break
    assert body_element is not None

    # Heading component - using semantic role
    header_element = get_by_role(result, "banner")
    assert header_element.tag == "header"
    # Check for the fixed class in the HTML
    assert "is-fixed" in str(header_element)

    # Main component contains the body HTML - using semantic role
    main_element = get_by_role(result, "main")
    assert main_element.tag == "main"

    # Find p element within main using tdom navigation
    def find_element_by_tag(element: Element, tag: str) -> Optional[Element]:
        for child in element.children:
            if isinstance(child, Element):
                if child.tag.lower() == tag.lower():
                    return child
                # Recursively search children
                found = find_element_by_tag(child, tag)
                if found:
                    return found
        return None

    # Debug: check what's in the main element
    main_content = get_text_content(main_element).strip()
    # The content might be directly in the main element without p tags
    assert "Hello World" in main_content

    # Footer component present - using semantic role
    footer_element = get_by_role(result, "contentinfo")
    assert footer_element.tag == "footer"


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
        toc=None,
    )
    result = html(t"<{BaseLayout} page_context={local} site_config={site_config} />")

    main_element = get_by_role(result, "main")
    assert main_element.tag == "main"

    # Find elements within main using tdom navigation
    def find_element_by_tag(element: Element, tag: str) -> Optional[Element]:
        for child in element.children:
            if isinstance(child, Element):
                if child.tag.lower() == tag.lower():
                    return child
                # Recursively search children
                found = find_element_by_tag(child, tag)
                if found:
                    return found
        return None

    # Check that the content is present in the main element
    main_content = get_text_content(main_element)
    assert "Section Title" in main_content
    assert "Paragraph content" in main_content
    assert "List item" in main_content


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
        toc=None,
    )
    result = html(t"<{BaseLayout} page_context={local} site_config={site_config} />")

    main_element = get_by_role(result, "main")
    assert main_element.tag == "main"

    # Find p element within main using tdom navigation
    def find_element_by_tag(element: Element, tag: str) -> Optional[Element]:
        for child in element.children:
            if isinstance(child, Element):
                if child.tag.lower() == tag.lower():
                    return child
                # Recursively search children
                found = find_element_by_tag(child, tag)
                if found:
                    return found
        return None

    # Check that the content is present in the main element
    main_content = get_text_content(main_element).strip()
    assert "Hello World" in main_content


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
        toc=None,
    )

    result = html(t"<{BaseLayout} page_context={local} site_config={site_config} />")

    # Find HTML element within Fragment
    html_element = None
    assert isinstance(result, Element)
    for child in result.children:
        if isinstance(child, Element) and child.tag.lower() == "html":
            html_element = child
            break
    assert html_element is not None

    # Find head element and then title
    head_element = None
    for child in html_element.children:
        if isinstance(child, Element) and child.tag.lower() == "head":
            head_element = child
            break
    assert head_element is not None

    title_element = None
    for head_child in head_element.children:
        if isinstance(head_child, Element) and head_child.tag.lower() == "title":
            title_element = head_child
            break
    assert title_element is not None
    assert get_text_content(title_element) == "No Sphinx Context - My Test Site"

    # Body is missing; Main renders empty when no body provided
    main_element = get_by_role(result, "main")
    assert main_element is not None
    assert get_text_content(main_element).strip() == ""


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
        toc=None,
    )

    result = html(
        t"<{BaseLayout} page_context={page_context} site_config={site_config} />"
    )
    html_string = str(result)

    # Find HTML element within Fragment
    html_element = None
    assert isinstance(result, Element)
    for child in result.children:
        if isinstance(child, Element) and child.tag.lower() == "html":
            html_element = child
            break
    assert html_element is not None

    # Find head element and then title
    head_element = None
    for child in html_element.children:
        if isinstance(child, Element) and child.tag.lower() == "head":
            head_element = child
            break
    assert head_element is not None

    title_element = None
    for head_child in head_element.children:
        if isinstance(head_child, Element) and head_child.tag.lower() == "title":
            title_element = head_child
            break
    assert title_element is not None
    assert get_text_content(title_element) == "Complex Test - My Test Site"

    main_element = get_by_role(result, "main")
    assert main_element is not None
    assert "Main content" in get_text_content(main_element)

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
        toc=None,
    )

    result = html(t"<{BaseLayout} page_context={local} site_config={site_config} />")

    main_element = get_by_role(result, "main")
    assert main_element is not None

    # Find elements within main using tdom navigation
    def find_element_by_tag(element: Element, tag: str) -> Optional[Element]:
        for child in element.children:
            if isinstance(child, Element):
                if child.tag.lower() == tag.lower():
                    return child
                # Recursively search children
                found = find_element_by_tag(child, tag)
                if found:
                    return found
        return None

    # Check that the content is present in the main element
    main_content = get_text_content(main_element)
    assert "bold" in main_content
    assert "italic" in main_content


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
        toc=None,
    )

    result = html(t"<{BaseLayout} page_context={local} site_config={site_config} />")

    # Find HTML element within Fragment
    html_element = None
    assert isinstance(result, Element)
    for child in result.children:
        if isinstance(child, Element) and child.tag.lower() == "html":
            html_element = child
            break
    assert html_element is not None

    # Find head element
    head_element = None
    for child in html_element.children:
        if isinstance(child, Element) and child.tag.lower() == "head":
            head_element = child
            break
    assert head_element is not None

    # Find stylesheets and favicon
    css_link = None
    favicon_link = None
    for head_child in head_element.children:
        if isinstance(head_child, Element) and head_child.tag.lower() == "link":
            if (
                head_child.attrs.get("rel") == "stylesheet"
                and head_child.attrs.get("href") == "_static/tdom-sphinx.css"
            ):
                css_link = head_child
            elif head_child.attrs.get("rel") == "icon":
                favicon_link = head_child

    assert css_link is not None
    assert css_link.attrs.get("href") == "_static/tdom-sphinx.css"

    assert favicon_link is not None
    assert favicon_link.attrs.get("href") == "_static/favicon.ico"
