from tdom import html

from tdom_sphinx.aria_testing import (
    get_all_by_role,
    get_by_role,
)
from tdom_sphinx.components.navbar_links import NavbarLinks
from tdom_sphinx.models import IconLink, Link


def test_navbar_links_renders_links_and_buttons(page_context):
    links = [
        Link(href="/docs", style="", text="Docs"),
        Link(href="/about", style="btn", text="About"),
    ]
    buttons = [
        IconLink(
            href="https://github.com/org", color="#111", icon_class="fa fa-github"
        ),
        IconLink(href="https://x.com/org", color="#08f", icon_class="fa fa-twitter"),
    ]

    result = html(
        t"""
        <{NavbarLinks} page_context={page_context} links={links} buttons={buttons} />
        """
    )

    # Find the main list structure
    ul_element = get_by_role(result, "list")
    assert ul_element.tag == "ul"

    # Find all links within the navbar
    all_links = get_all_by_role(result, "link")
    # 2 text links + 2 button links
    assert len(all_links) == 4

    # Check text links by finding them by their href attribute
    docs_link = None
    about_link = None

    for link in all_links:
        href = link.attrs.get("href", "")
        if href == "docs":
            docs_link = link
        elif href == "about":
            about_link = link

    assert docs_link is not None
    assert docs_link.tag == "a"
    assert docs_link.attrs.get("href") == "docs"

    assert about_link is not None
    assert about_link.tag == "a"
    assert about_link.attrs.get("href") == "about"
