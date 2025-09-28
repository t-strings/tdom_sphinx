from typing import Optional

from bs4 import BeautifulSoup, Tag
from tdom import html

from tdom_sphinx.components.site_aside import SiteAside, toc_to_tree, toc_tree_to_nav
from tdom_sphinx.models import PageContext
from tdom_sphinx.utils import html_string_to_tdom


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
    """Test SiteAside with actual toctree content generates semantic navigation."""
    # Create a PageContext with sample toctree as parsed Node
    toctree_html = '<ul><li><a href="/docs.html">Documentation</a></li><li><a href="/api.html">API</a></li></ul>'
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
        toc=html_string_to_tdom(toctree_html),
    )

    result = html(
        t"""
        <{SiteAside} page_context={page_context_with_toc} />
        """
    )

    soup = BeautifulSoup(str(result), "html.parser")

    aside_element: Optional[Tag] = soup.select_one("aside")
    assert aside_element is not None

    # Should contain semantic navigation structure
    nav_element: Optional[Tag] = aside_element.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert nav_element is not None

    # Should have two direct anchor links (no nesting for simple flat structure)
    links = nav_element.find_all("a", recursive=False)
    assert len(links) == 2

    # With the Node-based approach, relative_tree can now process the toctree content
    # The URLs should be made relative to the current page
    assert links[0].get("href") == "docs.html"  # Relative to current page
    assert links[0].text == "Documentation"
    assert links[1].get("href") == "api.html"  # Relative to current page
    assert links[1].text == "API"


ASIDE_1 = """\
<aside id="site-aside">
  <ul><li><a class="reference internal" href="#">tdom-sphinx</a><ul><li><a class="reference internal" href="#getting-started">Getting started</a></li><li><a class="reference internal" href="#building-the-docs-locally">Building the docs locally</a></li></ul></li></ul>
</aside>"""


def test_toc_to_tree_with_empty_node():
    """Test toc_to_tree with None input returns empty fragment."""
    result = toc_to_tree(None)
    soup = BeautifulSoup(str(result), "html.parser")
    assert soup.get_text(strip=True) == ""


def test_toc_to_tree_with_simple_ul():
    """Test toc_to_tree with a simple UL containing one link."""
    html_content = '<ul><li><a href="/page.html">Page Title</a></li></ul>'
    toc_node = html_string_to_tdom(html_content)

    result = toc_to_tree(toc_node)
    soup = BeautifulSoup(str(result), "html.parser")

    # Should generate semantic nav structure
    nav: Optional[Tag] = soup.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert nav is not None

    # Should have one direct anchor link (no nesting for single item)
    links = nav.find_all("a", recursive=False)
    assert len(links) == 1
    assert links[0].get("href") == "/page.html"
    assert links[0].text == "Page Title"


def test_toc_to_tree_with_nested_structure():
    """Test toc_to_tree with nested UL structure matching ASIDE_1."""
    toc_node = html_string_to_tdom(ASIDE_1)

    result = toc_to_tree(toc_node)
    soup = BeautifulSoup(str(result), "html.parser")

    # Should have main nav container
    nav: Optional[Tag] = soup.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert nav is not None

    # Should have one details element (for tdom-sphinx)
    details: Optional[Tag] = nav.select_one("details")
    assert details is not None
    assert details.get("open") == "open"

    # Check summary link
    summary_link: Optional[Tag] = details.select_one("summary > a")
    assert summary_link is not None
    assert summary_link.get("href") == "#"
    assert summary_link.get_text(strip=True) == "tdom-sphinx"

    # Check nested ul structure
    nested_ul: Optional[Tag] = details.select_one("ul")
    assert nested_ul is not None

    # Check child links within li elements
    child_lis = nested_ul.select("li")
    assert len(child_lis) == 2

    child_links = [li.select_one("a") for li in child_lis]
    assert child_links[0] is not None
    assert child_links[0].get("href") == "#getting-started"
    assert child_links[0].get_text(strip=True) == "Getting started"
    assert child_links[1] is not None
    assert child_links[1].get("href") == "#building-the-docs-locally"
    assert child_links[1].get_text(strip=True) == "Building the docs locally"


def test_toc_to_tree_with_multiple_top_level_items():
    """Test toc_to_tree with multiple top-level items."""
    html_content = """
    <ul>
        <li><a href="/intro.html">Introduction</a></li>
        <li>
            <a href="/guide.html">User Guide</a>
            <ul>
                <li><a href="/guide/basics.html">Basics</a></li>
                <li><a href="/guide/advanced.html">Advanced</a></li>
            </ul>
        </li>
        <li><a href="/reference.html">Reference</a></li>
    </ul>
    """
    toc_node = html_string_to_tdom(html_content)

    result = toc_to_tree(toc_node)
    soup = BeautifulSoup(str(result), "html.parser")

    # Should have main nav container
    nav: Optional[Tag] = soup.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert nav is not None

    # Should have: 2 direct links + 1 details element
    direct_links = nav.find_all("a", recursive=False)
    details_elements = nav.find_all("details", recursive=False)

    assert len(direct_links) == 2  # Introduction and Reference
    assert len(details_elements) == 1  # User Guide

    # Check direct links
    assert direct_links[0].get("href") == "/intro.html"
    assert direct_links[0].get_text(strip=True) == "Introduction"
    assert direct_links[1].get("href") == "/reference.html"
    assert direct_links[1].get_text(strip=True) == "Reference"

    # Check the details element (User Guide)
    details = details_elements[0]
    summary_link: Optional[Tag] = details.select_one("summary > a")
    assert summary_link is not None
    assert summary_link.get("href") == "/guide.html"
    assert summary_link.get_text(strip=True) == "User Guide"

    # Check nested items in ul structure
    nested_ul: Optional[Tag] = details.select_one("ul")
    assert nested_ul is not None
    nested_lis = nested_ul.select("li")
    assert len(nested_lis) == 2

    nested_links = [li.select_one("a") for li in nested_lis]
    assert nested_links[0] is not None
    assert nested_links[0].get("href") == "/guide/basics.html"
    assert nested_links[0].get_text(strip=True) == "Basics"
    assert nested_links[1] is not None
    assert nested_links[1].get("href") == "/guide/advanced.html"
    assert nested_links[1].get_text(strip=True) == "Advanced"


def test_toc_to_tree_with_fragment_input():
    """Test toc_to_tree with a Fragment containing UL."""
    from tdom.nodes import Fragment as TFragment

    # Create a fragment containing a UL
    html_content = '<ul><li><a href="/test.html">Test Link</a></li></ul>'
    ul_node = html_string_to_tdom(html_content)
    fragment = TFragment(children=[ul_node])

    result = toc_to_tree(fragment)
    soup = BeautifulSoup(str(result), "html.parser")

    # Should generate semantic nav structure
    nav: Optional[Tag] = soup.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert nav is not None

    # Should have one direct anchor link
    links = nav.find_all("a", recursive=False)
    assert len(links) == 1
    assert links[0].get("href") == "/test.html"
    assert links[0].get_text(strip=True) == "Test Link"


def test_toc_to_tree_with_li_without_anchor():
    """Test toc_to_tree handles LI elements without anchor tags gracefully."""
    html_content = """
    <ul>
        <li><a href="/valid.html">Valid Link</a></li>
        <li>Just text without anchor</li>
        <li><a href="/another.html">Another Valid Link</a></li>
    </ul>
    """
    toc_node = html_string_to_tdom(html_content)

    result = toc_to_tree(toc_node)
    soup = BeautifulSoup(str(result), "html.parser")

    # Should only render the valid links, skipping the LI without anchor
    nav: Optional[Tag] = soup.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert nav is not None

    # Should have two direct anchor links
    links = nav.find_all("a", recursive=False)
    assert len(links) == 2
    assert links[0].get("href") == "/valid.html"
    assert links[0].get_text(strip=True) == "Valid Link"
    assert links[1].get("href") == "/another.html"
    assert links[1].get_text(strip=True) == "Another Valid Link"


def test_toc_tree_to_nav_with_empty_content():
    """Test toc_tree_to_nav with None content returns empty fragment."""
    result = toc_tree_to_nav(None)
    soup = BeautifulSoup(str(result), "html.parser")

    # Should render as empty (no content)
    assert soup.get_text(strip=True) == ""


def test_toc_tree_to_nav_with_simple_structure():
    """Test toc_tree_to_nav with a simple flat structure."""
    html_content = """
    <ul>
        <li><a href="/page1.html">Page 1</a></li>
        <li><a href="/page2.html">Page 2</a></li>
    </ul>
    """
    toc_node = html_string_to_tdom(html_content)

    result = toc_tree_to_nav(toc_node)
    soup = BeautifulSoup(str(result), "html.parser")

    # Should have main nav container
    main_nav: Optional[Tag] = soup.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert main_nav is not None

    # Should have two direct anchor links (no nesting)
    direct_links = main_nav.find_all("a", recursive=False)
    assert len(direct_links) == 2
    assert direct_links[0].get("href") == "/page1.html"
    assert direct_links[0].get_text(strip=True) == "Page 1"
    assert direct_links[1].get("href") == "/page2.html"
    assert direct_links[1].get_text(strip=True) == "Page 2"


def test_toc_tree_to_nav_with_nested_structure():
    """Test toc_tree_to_nav with ASIDE_1 nested structure."""
    toc_node = html_string_to_tdom(ASIDE_1)

    result = toc_tree_to_nav(toc_node)
    soup = BeautifulSoup(str(result), "html.parser")

    # Should have main nav container
    main_nav: Optional[Tag] = soup.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert main_nav is not None

    # Should have one details element (for tdom-sphinx)
    details: Optional[Tag] = main_nav.select_one("details")
    assert details is not None
    assert details.get("open") == "open"

    # Check summary link
    summary_link: Optional[Tag] = details.select_one("summary > a")
    assert summary_link is not None
    assert summary_link.get("href") == "#"
    assert summary_link.get_text(strip=True) == "tdom-sphinx"

    # Check nested ul structure
    nested_ul: Optional[Tag] = details.select_one("ul")
    assert nested_ul is not None

    # Check child links within li elements
    child_lis = nested_ul.select("li")
    assert len(child_lis) == 2

    child_links = [li.select_one("a") for li in child_lis]
    assert child_links[0] is not None
    assert child_links[0].get("href") == "#getting-started"
    assert child_links[0].get_text(strip=True) == "Getting started"
    assert child_links[1] is not None
    assert child_links[1].get("href") == "#building-the-docs-locally"
    assert child_links[1].get_text(strip=True) == "Building the docs locally"


def test_toc_tree_to_nav_with_deep_nesting():
    """Test toc_tree_to_nav with deeply nested structure."""
    html_content = """
    <ul>
        <li>
            <a href="/guide.html">User Guide</a>
            <ul>
                <li>
                    <a href="/guide/basics.html">Basics</a>
                    <ul>
                        <li><a href="/guide/basics/intro.html">Introduction</a></li>
                        <li><a href="/guide/basics/setup.html">Setup</a></li>
                    </ul>
                </li>
                <li><a href="/guide/advanced.html">Advanced Topics</a></li>
            </ul>
        </li>
    </ul>
    """
    toc_node = html_string_to_tdom(html_content)

    result = toc_tree_to_nav(toc_node)
    soup = BeautifulSoup(str(result), "html.parser")

    # Should have main nav
    main_nav = soup.select_one("nav[aria-label='Table of contents']")
    assert main_nav is not None

    # Level 1: User Guide (should have details/summary)
    level1_details = main_nav.select_one("details")
    assert level1_details is not None
    level1_summary: Tag | None = level1_details.select_one("summary > a")
    assert level1_summary is not None
    assert level1_summary.get_text(strip=True) == "User Guide"
    assert level1_summary.get("href") == "/guide.html"

    # Level 2: Should have nested ul with two items
    level2_ul = level1_details.select_one("ul")
    assert level2_ul is not None

    # Should have two li elements (direct children only)
    level2_lis = level2_ul.find_all("li", recursive=False)
    assert len(level2_lis) == 2

    # Level 2a: Basics (should have details/summary for sub-items)
    basics_details = level2_lis[0].select_one("details")
    assert basics_details is not None
    basics_summary = basics_details.select_one("summary > a")
    assert basics_summary.text == "Basics"
    assert basics_summary.get("href") == "/guide/basics.html"

    # Level 2b: Advanced Topics (should be simple link in second li)
    advanced_link = level2_lis[1].select_one("a")
    assert advanced_link is not None
    assert advanced_link.text.strip() == "Advanced Topics"
    assert advanced_link.get("href") == "/guide/advanced.html"

    # Level 3: Basics sub-items (should be in ul/li structure)
    level3_ul = basics_details.select_one("ul")
    assert level3_ul is not None
    level3_lis = level3_ul.select("li")
    assert len(level3_lis) == 2

    level3_links = [li.select_one("a") for li in level3_lis]
    assert level3_links[0].text == "Introduction"
    assert level3_links[0].get("href") == "/guide/basics/intro.html"
    assert level3_links[1].text == "Setup"
    assert level3_links[1].get("href") == "/guide/basics/setup.html"


def test_toc_tree_to_nav_accessibility_attributes():
    """Test that the generated navigation has proper accessibility attributes."""
    html_content = """
    <ul>
        <li>
            <a href="/section.html">Main Section</a>
            <ul>
                <li><a href="/section/sub.html">Subsection</a></li>
            </ul>
        </li>
    </ul>
    """
    toc_node = html_string_to_tdom(html_content)

    result = toc_tree_to_nav(toc_node)
    soup = BeautifulSoup(str(result), "html.parser")

    # Main nav should have role and aria-label
    main_nav: Optional[Tag] = soup.select_one("nav")
    assert main_nav is not None
    assert main_nav.get("role") == "navigation"
    assert main_nav.get("aria-label") == "Table of contents"

    # Nested structure should use ul/li, not nav
    nested_ul: Optional[Tag] = soup.select_one("details ul")
    assert nested_ul is not None

    # Details should be open by default for better accessibility
    details: Optional[Tag] = soup.select_one("details")
    assert details is not None
    assert details.get("open") == "open"


def test_toc_to_tree_hide_root_disabled():
    """Test toc_to_tree with hide_root=False preserves the root details structure."""
    html_content = """
    <ul>
        <li>
            <a href="#">My Site</a>
            <ul>
                <li><a href="/page1.html">Page 1</a></li>
                <li><a href="/page2.html">Page 2</a></li>
            </ul>
        </li>
    </ul>
    """
    toc_node = html_string_to_tdom(html_content)

    result = toc_to_tree(toc_node, hide_root=False, site_title="My Site")
    soup = BeautifulSoup(str(result), "html.parser")

    # Should have the details structure preserved
    main_nav: Optional[Tag] = soup.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert main_nav is not None

    details: Optional[Tag] = main_nav.select_one("details")
    assert details is not None

    summary_link: Optional[Tag] = details.select_one("summary > a")
    assert summary_link is not None
    assert summary_link.get("href") == "#"
    assert summary_link.get_text(strip=True) == "My Site"


def test_toc_to_tree_hide_root_enabled_matching_title():
    """Test toc_to_tree with hide_root=True and matching site_title unwraps the root."""
    html_content = """
    <ul>
        <li>
            <a href="#">My Site</a>
            <ul>
                <li><a href="/page1.html">Page 1</a></li>
                <li><a href="/page2.html">Page 2</a></li>
            </ul>
        </li>
    </ul>
    """
    toc_node = html_string_to_tdom(html_content)

    result = toc_to_tree(toc_node, hide_root=True, site_title="My Site")
    soup = BeautifulSoup(str(result), "html.parser")

    # Should unwrap and show direct links
    main_nav: Optional[Tag] = soup.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert main_nav is not None

    # Should not have a details element (unwrapped)
    details: Optional[Tag] = main_nav.select_one("details")
    assert details is None

    # Should have direct li elements for the children (unwrapped from the details)
    direct_lis = main_nav.find_all("li", recursive=False)
    assert len(direct_lis) == 2

    # Check the links within the li elements
    link1: Optional[Tag] = direct_lis[0].select_one("a")
    assert link1 is not None
    assert link1.get("href") == "/page1.html"
    assert link1.get_text(strip=True) == "Page 1"

    link2: Optional[Tag] = direct_lis[1].select_one("a")
    assert link2 is not None
    assert link2.get("href") == "/page2.html"
    assert link2.get_text(strip=True) == "Page 2"


def test_toc_to_tree_hide_root_enabled_non_matching_title():
    """Test toc_to_tree with hide_root=True but non-matching site_title preserves structure."""
    html_content = """
    <ul>
        <li>
            <a href="#">My Site</a>
            <ul>
                <li><a href="/page1.html">Page 1</a></li>
                <li><a href="/page2.html">Page 2</a></li>
            </ul>
        </li>
    </ul>
    """
    toc_node = html_string_to_tdom(html_content)

    result = toc_to_tree(toc_node, hide_root=True, site_title="Different Site")
    soup = BeautifulSoup(str(result), "html.parser")

    # Should preserve the details structure (titles don't match)
    main_nav: Optional[Tag] = soup.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert main_nav is not None

    details: Optional[Tag] = main_nav.select_one("details")
    assert details is not None

    summary_link: Optional[Tag] = details.select_one("summary > a")
    assert summary_link is not None
    assert summary_link.get("href") == "#"
    assert summary_link.get_text(strip=True) == "My Site"


def test_toc_to_tree_hide_root_multiple_root_items():
    """Test toc_to_tree with hide_root=True but multiple root items preserves structure."""
    html_content = """
    <ul>
        <li><a href="/intro.html">Introduction</a></li>
        <li>
            <a href="#">My Site</a>
            <ul>
                <li><a href="/page1.html">Page 1</a></li>
                <li><a href="/page2.html">Page 2</a></li>
            </ul>
        </li>
    </ul>
    """
    toc_node = html_string_to_tdom(html_content)

    result = toc_to_tree(toc_node, hide_root=True, site_title="My Site")
    soup = BeautifulSoup(str(result), "html.parser")

    # Should preserve structure because there are multiple root items
    main_nav: Optional[Tag] = soup.select_one(
        "nav[role='navigation'][aria-label='Table of contents']"
    )
    assert main_nav is not None

    # Should have both a direct link and a details element
    direct_links = main_nav.find_all("a", recursive=False)
    details: Optional[Tag] = main_nav.select_one("details")

    assert len(direct_links) == 1
    assert direct_links[0].get("href") == "/intro.html"
    assert direct_links[0].get_text(strip=True) == "Introduction"

    assert details is not None
    summary_link: Optional[Tag] = details.select_one("summary > a")
    assert summary_link is not None
    assert summary_link.get_text(strip=True) == "My Site"
