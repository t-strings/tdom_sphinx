from pathlib import PurePosixPath

from tdom import Node, html
from tdom.nodes import Element as TElement, Fragment as TFragment, Text as TText

from tdom_sphinx.models import PageContext, SiteConfig
from tdom_sphinx.url import relative_tree


def toc_to_tree(toc_node: Node | None, *, hide_root: bool | None = True, site_title: str | None = None) -> Node:
    """Convert a tdom Node representing a toctree into semantic navigation HTML.

    Args:
        toc_node: A tdom Node containing the toctree HTML structure
        hide_root: If True, hide the root summary when its text matches site_title
        site_title: The site title to compare against for hiding the root summary

    Returns:
        A tdom Node containing semantic navigation HTML using nav, details, and summary elements

    Example:
        Given HTML like:
        <ul>
          <li>
            <a href="#">Main Page</a>
            <ul>
              <li><a href="#section1">Section 1</a></li>
              <li><a href="#section2">Section 2</a></li>
            </ul>
          </li>
        </ul>

        Returns semantic HTML:
        <nav role="navigation" aria-label="Table of contents">
            <details open="open">
                <summary>
                    <a href="#">Main Page</a>
                </summary>
                <ul>
                    <li><a href="#section1">Section 1</a></li>
                    <li><a href="#section2">Section 2</a></li>
                </ul>
            </details>
        </nav>
    """
    if not toc_node:
        return TFragment(children=[])

    def parse_ul(ul_element: TElement) -> list[Node]:
        """Parse a UL element and return a list of semantic navigation nodes."""
        nav_items = []

        for child in ul_element.children:
            if isinstance(child, TElement) and child.tag == "li":
                nav_item = parse_li(child)
                if nav_item:
                    nav_items.append(nav_item)

        return nav_items

    def parse_li(li_element: TElement) -> Node | None:
        """Parse an LI element and return a semantic navigation node."""
        link_element = None
        nested_ul = None

        # Find the anchor tag and any nested UL
        for child in li_element.children:
            if isinstance(child, TElement):
                if child.tag == "a":
                    link_element = child
                elif child.tag == "ul":
                    nested_ul = child

        if not link_element:
            return None

        # Extract text and href from the anchor
        text = ""
        for child in link_element.children:
            if isinstance(child, TText):
                text += child.text

        href = link_element.attrs.get("href", "")

        # If no children, return simple link
        if not nested_ul:
            return html(t"<a href={href}>{text.strip()}</a>")

        # If has children, create details/summary structure with ul/li
        child_items = parse_ul(nested_ul)

        # For nested children, each child_item is the content for an <li>
        child_lis = [html(t"<li>{item}</li>") for item in child_items]

        return html(t"""
<details open="open">
    <summary>
        <a href={href}>{text.strip()}</a>
    </summary>
    <ul>
        {child_lis}
    </ul>
</details>
""")

    # Start parsing from the root node
    nav_items = []

    if isinstance(toc_node, TElement):
        if toc_node.tag == "ul":
            nav_items = parse_ul(toc_node)
        elif toc_node.tag == "aside":
            # Find the UL inside the aside
            for child in toc_node.children:
                if isinstance(child, TElement) and child.tag == "ul":
                    nav_items = parse_ul(child)
                    break
    elif isinstance(toc_node, TFragment):
        # Look for UL elements in the fragment
        for child in toc_node.children:
            if isinstance(child, TElement) and child.tag == "ul":
                nav_items = parse_ul(child)
                break

    if not nav_items:
        return TFragment(children=[])

    # Apply hide_root logic if enabled
    if hide_root and site_title and len(nav_items) == 1:
        nav_item = nav_items[0]

        # The nav_item is created by html() so we need to handle it properly
        # It could be a TElement directly or we might need to find the details element within it
        details_element = None

        if isinstance(nav_item, TElement) and nav_item.tag == "details":
            details_element = nav_item
        elif isinstance(nav_item, (TElement, TFragment)):
            # Search for details element in the structure
            for child in nav_item.children:
                if isinstance(child, TElement) and child.tag == "details":
                    details_element = child
                    break

        if details_element:
            # Find the summary > a element to check the text
            for child in details_element.children:
                if isinstance(child, TElement) and child.tag == "summary":
                    for summary_child in child.children:
                        if isinstance(summary_child, TElement) and summary_child.tag == "a":
                            # Extract text from the anchor
                            anchor_text = ""
                            for text_node in summary_child.children:
                                if isinstance(text_node, TText):
                                    anchor_text += text_node.text

                            # If the anchor text matches site_title, unwrap the details
                            if anchor_text.strip() == site_title.strip():
                                # Find the ul element inside details and return its children
                                for details_child in details_element.children:
                                    if isinstance(details_child, TElement) and details_child.tag == "ul":
                                        return html(t"""
<nav role="navigation" aria-label="Table of contents">
    {details_child.children}
</nav>
""")
                            break
                    break

    return html(t"""
<nav role="navigation" aria-label="Table of contents">
    {nav_items}
</nav>
""")


def toc_tree_to_nav(toc_content: Node | None) -> Node:
    """Convert toctree content to a semantic navigation structure.

    This is now a simple wrapper around toc_to_tree since that function
    directly generates the semantic HTML structure.

    Args:
        toc_content: tdom Node containing toctree HTML, or None

    Returns:
        A tdom Node containing the semantic navigation structure

    Example:
        Input toctree with nested structure becomes:
        <nav role="navigation" aria-label="Table of contents">
            <details open="open">
                <summary>
                    <a href="#">Main Section</a>
                </summary>
                <ul>
                    <li><a href="#subsection1">Subsection 1</a></li>
                    <li><a href="#subsection2">Subsection 2</a></li>
                </ul>
            </details>
        </nav>
    """
    return toc_to_tree(toc_content)


def SiteAside(*, page_context: PageContext, site_config: SiteConfig | None = None) -> Node:
    """Render a site aside with semantic toctree navigation.

    This component renders an <aside> element containing semantic navigation
    generated from the toctree content using toc_to_tree().
    Uses relative_tree to make hrefs relative to the current page.
    """
    # Convert toctree content to semantic navigation HTML
    site_title = site_config.site_title if site_config else None
    semantic_nav = toc_to_tree(page_context.toc, hide_root=True, site_title=site_title)

    result = html(
        t"""
<aside id="site-aside">
  {semantic_nav}
</aside>
"""
    )

    # Make hrefs in this subtree relative to the current page
    # This must happen after the HTML is constructed so relative_tree can process the DOM
    current = PurePosixPath("/" + page_context.pagename)
    relative_tree(result, current)

    return result
