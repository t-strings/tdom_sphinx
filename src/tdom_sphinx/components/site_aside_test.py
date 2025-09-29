from tdom import html

from tdom_sphinx.aria_testing import (
    get_all_by_role,
    get_by_label_text,
    get_by_role,
    get_by_text,
    query_all_by_role,
)
from tdom_sphinx.aria_testing.utils import get_text_content
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

    aside_element = get_by_role(result, "complementary")
    assert aside_element.tag == "aside"

    # With empty toc, aside should be essentially empty (just whitespace)
    assert get_text_content(aside_element).strip() == ""


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
    site_aside = get_by_label_text(result, "Table of contents")
    assert site_aside.tag == "nav"

    # Should have two direct anchor links (no nesting for simple flat structure)
    links = get_all_by_role(site_aside, "link")
    assert len(links) == 2

    # The URLs should be made relative to the current page
    assert links[0].attrs["href"] == "docs.html"  # Relative to the current page
    assert get_text_content(links[0]) == "Documentation"
    assert links[1].attrs["href"] == "api.html"  # Relative to the current page
    assert get_text_content(links[1]) == "API"


def test_toc_to_tree_with_empty_node():
    """Test toc_to_tree with None input returns empty fragment."""
    result = toc_to_tree(None)
    result_text = get_text_content(result).strip()
    assert result_text == ""


def test_toc_to_tree_with_simple_ul():
    """Test toc_to_tree with a simple UL containing one link."""
    html_content = '<ul><li><a href="/page.html">Page Title</a></li></ul>'
    toc_node = html_string_to_tdom(html_content)

    result = toc_to_tree(toc_node)

    # Should generate semantic nav structure
    nav = get_by_role(result, "navigation")
    assert nav is not None

    # Verify aria-label
    assert nav.attrs.get("aria-label") == "Table of contents"

    # Should have one direct anchor link (no nesting for single item)
    links = get_all_by_role(nav, "link")
    assert len(links) == 1
    assert links[0].attrs.get("href") == "/page.html"
    assert get_text_content(links[0]) == "Page Title"


def test_toc_to_tree_with_nested_structure():
    """Test toc_to_tree with a nested UL structure matching ASIDE_1."""

    sphinx_toctree = """\
    <aside id="site-aside">
      <ul><li><a class="reference internal" href="#">tdom-sphinx</a><ul><li><a class="reference internal" href="#getting-started">Getting started</a></li><li><a class="reference internal" href="#building-the-docs-locally">Building the docs locally</a></li></ul></li></ul>
    </aside>"""

    toc_node = html_string_to_tdom(sphinx_toctree)

    result = toc_to_tree(toc_node)

    # Should have main nav container
    nav = get_by_role(result, "navigation")
    assert nav is not None

    # Verify aria-label
    assert nav.attrs.get("aria-label") == "Table of contents"

    # Check that we have all three links (main + 2 children)
    all_links = get_all_by_role(nav, "link")
    assert len(all_links) == 3

    # Find and check the specific links by href
    main_link = None
    getting_started_link = None
    docs_locally_link = None

    for link in all_links:
        href = link.attrs.get("href")
        if href == "#":
            main_link = link
        elif href == "#getting-started":
            getting_started_link = link
        elif href == "#building-the-docs-locally":
            docs_locally_link = link

    assert main_link is not None
    assert get_text_content(main_link) == "tdom-sphinx"

    assert getting_started_link is not None
    assert get_text_content(getting_started_link) == "Getting started"

    assert docs_locally_link is not None
    assert get_text_content(docs_locally_link) == "Building the docs locally"


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

    # Should have main nav container
    nav = get_by_role(result, "navigation")
    assert nav is not None

    # Verify aria-label
    assert nav.attrs.get("aria-label") == "Table of contents"

    # Check all links - should be 5 total (2 direct + 1 user guide + 2 nested)
    all_links = get_all_by_role(nav, "link")
    assert len(all_links) == 5

    # Find and check the specific links by href
    intro_link = None
    reference_link = None
    user_guide_link = None
    basics_link = None
    advanced_link = None

    for link in all_links:
        href = link.attrs.get("href")
        if href == "/intro.html":
            intro_link = link
        elif href == "/reference.html":
            reference_link = link
        elif href == "/guide.html":
            user_guide_link = link
        elif href == "/guide/basics.html":
            basics_link = link
        elif href == "/guide/advanced.html":
            advanced_link = link

    assert intro_link is not None
    assert get_text_content(intro_link) == "Introduction"

    assert reference_link is not None
    assert get_text_content(reference_link) == "Reference"

    assert user_guide_link is not None
    assert get_text_content(user_guide_link) == "User Guide"

    assert basics_link is not None
    assert get_text_content(basics_link) == "Basics"

    assert advanced_link is not None
    assert get_text_content(advanced_link) == "Advanced"


def test_toc_to_tree_with_fragment_input():
    """Test toc_to_tree with a Fragment containing UL."""
    from tdom.nodes import Fragment as TFragment

    # Create a fragment containing a UL
    html_content = '<ul><li><a href="/test.html">Test Link</a></li></ul>'
    ul_node = html_string_to_tdom(html_content)
    fragment = TFragment(children=[ul_node])

    result = toc_to_tree(fragment)

    # Should generate semantic nav structure
    nav = get_by_role(result, "navigation")
    assert nav is not None

    # Verify aria-label
    assert nav.attrs.get("aria-label") == "Table of contents"

    # Should have one direct anchor link
    links = get_all_by_role(nav, "link")
    assert len(links) == 1

    test_link = get_by_text(nav, "Test Link")
    assert test_link.attrs.get("href") == "/test.html"


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

    # Should only render the valid links, skipping the LI without anchor
    nav = get_by_role(result, "navigation")
    assert nav is not None

    # Verify aria-label
    assert nav.attrs.get("aria-label") == "Table of contents"

    # Should have two direct anchor links
    links = get_all_by_role(nav, "link")
    assert len(links) == 2

    # Find links by href to avoid text ambiguity
    valid_link = None
    another_link = None

    for link in links:
        href = link.attrs.get("href")
        if href == "/valid.html":
            valid_link = link
        elif href == "/another.html":
            another_link = link

    assert valid_link is not None
    assert get_text_content(valid_link) == "Valid Link"

    assert another_link is not None
    assert get_text_content(another_link) == "Another Valid Link"


def test_toc_tree_to_nav_with_empty_content():
    """Test toc_tree_to_nav with None content returns empty fragment."""
    result = toc_tree_to_nav(None)

    # Should render as empty (no content)
    result_text = get_text_content(result).strip()
    assert result_text == ""


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

    # Should have main nav container
    main_nav = get_by_role(result, "navigation")
    assert main_nav is not None

    # Verify aria-label
    assert main_nav.attrs.get("aria-label") == "Table of contents"

    # Should have two direct anchor links (no nesting)
    direct_links = get_all_by_role(main_nav, "link")
    assert len(direct_links) == 2

    # Check specific links
    page1_link = get_by_text(main_nav, "Page 1")
    assert page1_link.attrs.get("href") == "/page1.html"

    page2_link = get_by_text(main_nav, "Page 2")
    assert page2_link.attrs.get("href") == "/page2.html"


def test_toc_tree_to_nav_with_deep_nesting():
    """Test toc_tree_to_nav with a deeply nested structure."""
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

    # Should have main nav
    main_nav = get_by_role(result, "navigation")
    assert main_nav is not None

    # Verify aria-label
    assert main_nav.attrs.get("aria-label") == "Table of contents"

    # Should have all 5 links (User Guide + Basics + Advanced Topics + Introduction + Setup)
    all_links = get_all_by_role(main_nav, "link")
    assert len(all_links) == 5

    # Find links by href to avoid text ambiguity
    user_guide_link = None
    basics_link = None
    advanced_link = None
    intro_link = None
    setup_link = None

    for link in all_links:
        href = link.attrs.get("href")
        if href == "/guide.html":
            user_guide_link = link
        elif href == "/guide/basics.html":
            basics_link = link
        elif href == "/guide/advanced.html":
            advanced_link = link
        elif href == "/guide/basics/intro.html":
            intro_link = link
        elif href == "/guide/basics/setup.html":
            setup_link = link

    assert user_guide_link is not None
    assert get_text_content(user_guide_link) == "User Guide"

    assert basics_link is not None
    assert get_text_content(basics_link) == "Basics"

    assert advanced_link is not None
    assert get_text_content(advanced_link) == "Advanced Topics"

    assert intro_link is not None
    assert get_text_content(intro_link) == "Introduction"

    assert setup_link is not None
    assert get_text_content(setup_link) == "Setup"


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

    # Main nav should have role and aria-label
    main_nav = get_by_role(result, "navigation")
    assert main_nav is not None
    assert main_nav.attrs.get("role") == "navigation"
    assert main_nav.attrs.get("aria-label") == "Table of contents"

    # Check that we have the expected structure with links
    all_links = get_all_by_role(main_nav, "link")
    assert len(all_links) == 2  # Main Section + Subsection

    # Find links by href to avoid text ambiguity
    main_section_link = None
    subsection_link = None

    for link in all_links:
        href = link.attrs.get("href")
        if href == "/section.html":
            main_section_link = link
        elif href == "/section/sub.html":
            subsection_link = link

    assert main_section_link is not None
    assert get_text_content(main_section_link) == "Main Section"

    assert subsection_link is not None
    assert get_text_content(subsection_link) == "Subsection"


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

    # Should have the details structure preserved
    main_nav = get_by_role(result, "navigation")
    assert main_nav is not None

    # Find all links and get the one with the right href
    links = query_all_by_role(main_nav, "link")
    summary_link = None
    for link in links:
        if link.attrs.get("href") == "#":
            summary_link = link
            break

    assert summary_link is not None
    summary_text = get_text_content(summary_link)
    assert summary_text.strip() == "My Site"


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

    # Should unwrap and show direct links
    main_nav = get_by_role(result, "navigation")
    assert main_nav is not None

    # Verify aria-label
    assert main_nav.attrs.get("aria-label") == "Table of contents"

    # Should have 2 direct links (unwrapped from the details)
    direct_links = get_all_by_role(main_nav, "link")
    assert len(direct_links) == 2

    # Find links by href to avoid text ambiguity
    page1_link = None
    page2_link = None

    for link in direct_links:
        href = link.attrs.get("href")
        if href == "/page1.html":
            page1_link = link
        elif href == "/page2.html":
            page2_link = link

    assert page1_link is not None
    assert get_text_content(page1_link) == "Page 1"

    assert page2_link is not None
    assert get_text_content(page2_link) == "Page 2"


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

    # Should preserve the details structure (titles don't match)
    main_nav = get_by_role(result, "navigation")
    assert main_nav is not None

    # Verify aria-label
    assert main_nav.attrs.get("aria-label") == "Table of contents"

    # Should have all 3 links (My Site + Page 1 + Page 2)
    all_links = get_all_by_role(main_nav, "link")
    assert len(all_links) == 3

    # Find links by href to avoid text ambiguity
    my_site_link = None
    page1_link = None
    page2_link = None

    for link in all_links:
        href = link.attrs.get("href")
        if href == "#":
            my_site_link = link
        elif href == "/page1.html":
            page1_link = link
        elif href == "/page2.html":
            page2_link = link

    assert my_site_link is not None
    assert get_text_content(my_site_link) == "My Site"

    assert page1_link is not None
    assert get_text_content(page1_link) == "Page 1"

    assert page2_link is not None
    assert get_text_content(page2_link) == "Page 2"


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

    # Should preserve structure because there are multiple root items
    main_nav = get_by_role(result, "navigation")
    assert main_nav is not None

    # Verify aria-label
    assert main_nav.attrs.get("aria-label") == "Table of contents"

    # Should have all 4 links (Introduction + My Site + Page 1 + Page 2)
    all_links = get_all_by_role(main_nav, "link")
    assert len(all_links) == 4

    # Find links by href to avoid text ambiguity
    intro_link = None
    my_site_link = None
    page1_link = None
    page2_link = None

    for link in all_links:
        href = link.attrs.get("href")
        if href == "/intro.html":
            intro_link = link
        elif href == "#":
            my_site_link = link
        elif href == "/page1.html":
            page1_link = link
        elif href == "/page2.html":
            page2_link = link

    assert intro_link is not None
    assert get_text_content(intro_link) == "Introduction"

    assert my_site_link is not None
    assert get_text_content(my_site_link) == "My Site"

    assert page1_link is not None
    assert get_text_content(page1_link) == "Page 1"

    assert page2_link is not None
    assert get_text_content(page2_link) == "Page 2"
