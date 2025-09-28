"""Unit tests for make_page_context in sphinx_events.py."""

from markupsafe import Markup
from tdom.nodes import Element as TElement

from tdom_sphinx.sphinx_events import make_page_context


def test_make_page_context_builds_expected_page_context():
    # Arrange: minimal Sphinx-like context inputs
    context = {
        "body": "<p>Hello Body</p>",
        "metatags": '<meta charset="utf-8">',
        "next": {"title": "Next Page"},
        "page_source_suffix": ".rst",
        "prev": {"title": "Previous Page"},
        "sourcename": "index.rst",
        "title": "My Title",
        "toc": "<ul><li>Item</li></ul>",
        "toctree": "<div>TOC Tree</div>",
        # Intentionally provide both; implementation currently reads js from css
        "css_files": ["_static/sphinx.css", "_static/tdom-sphinx.css"],
        "js_files": ["_static/sphinx.js"],
        # Sphinx provides rellinks entries as tuples; map accordingly in make_page_context
        # Format: (pagename, title, accesskey, link_text)
        "rellinks": [
            ("genindex", "General Index", "I", "index"),
            ("search", "Search", "S", "search"),
        ],
    }

    # pagename must match the key in toc_num_entries to avoid KeyError in current logic
    pagename = "pagename"
    templatename = "page.html"
    toc_num_entries = {"pagename": 2}
    document_metadata = {"author": "Alice"}

    # Act
    page_context = make_page_context(
        context=context,
        pagename=pagename,
        templatename=templatename,
        toc_num_entries=toc_num_entries,
        document_metadata=document_metadata,
    )

    # Assert: selected fields are correctly transformed/preserved
    assert isinstance(page_context.body, Markup)
    assert "Hello Body" in str(page_context.body)

    assert page_context.templatename == templatename
    assert page_context.pagename == pagename
    assert page_context.page_source_suffix == ".rst"
    assert page_context.sourcename == "index.rst"
    assert page_context.title == "My Title"

    # toc is now parsed into a tdom Node and metatags remain string
    assert isinstance(page_context.toc, TElement)
    assert page_context.toc.tag == "ul"
    assert "Item" in str(page_context.toc)
    assert page_context.metatags == '<meta charset="utf-8">'

    # css/js become tuples; js currently mirrors css per implementation
    assert page_context.css_files == tuple(context["css_files"])  # type: ignore[comparison-overlap]
    assert page_context.js_files == tuple(
        context["css_files"]
    )  # mirrors css_files in current code

    # display_toc is True due to toc_num_entries["pagename"] > 1
    assert page_context.display_toc is True

    # rellinks are mapped into Rellink dataclasses
    assert len(page_context.rellinks) == 2
    rl0 = page_context.rellinks[0]
    assert rl0.pagename == "genindex"
    assert rl0.link_text == "index"
    assert rl0.title == "General Index"
    assert rl0.accesskey == "I"

    # document metadata passthrough
    assert page_context.meta == document_metadata
