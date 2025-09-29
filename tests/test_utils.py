"""Tests for utility functions."""

import pytest
from tdom.nodes import Element as TElement
from tdom.nodes import Fragment as TFragment
from tdom.nodes import Text as TText

from tdom_sphinx.aria_testing.utils import get_text_content
from tdom_sphinx.utils import html_string_to_tdom


def test_empty_string():
    """Test parsing an empty string returns an empty fragment."""
    result = html_string_to_tdom("")
    assert isinstance(result, TFragment)
    assert result.children == []


def test_whitespace_only():
    """Test parsing whitespace-only string returns an empty fragment."""
    result = html_string_to_tdom("   \n\t  ")
    assert isinstance(result, TFragment)
    assert result.children == []


def test_text_only():
    """Test parsing plain text returns a text node."""
    result = html_string_to_tdom("Hello World")
    assert isinstance(result, TText)
    assert result.text == "Hello World"


def test_html_parsing_with_aria_testing():
    """Test parsing HTML and finding elements using aria_testing utilities."""
    html = "<div><h1>Page Title</h1></div>"
    result = html_string_to_tdom(html)

    # Find the h1 element
    assert isinstance(result, TElement)
    assert result.tag == "div"

    h1_element = None
    for child in result.children:
        if isinstance(child, TElement) and child.tag == "h1":
            h1_element = child
            break

    assert h1_element is not None
    title_text = get_text_content(h1_element)
    assert title_text == "Page Title"


def test_single_element():
    """Test parsing a single element."""
    result = html_string_to_tdom("<div>Hello</div>")
    assert isinstance(result, TElement)
    assert result.tag == "div"
    assert result.attrs == {}
    assert len(result.children) == 1
    assert isinstance(result.children[0], TText)
    assert getattr(result.children[0], "text") == "Hello"


def test_element_with_attributes():
    """Test parsing element with attributes."""
    result = html_string_to_tdom(
        '<a href="https://example.com" class="link">Click me</a>'
    )
    assert isinstance(result, TElement)
    assert result.tag == "a"
    assert result.attrs == {"href": "https://example.com", "class": "link"}
    assert len(result.children) == 1
    assert isinstance(result.children[0], TText)
    assert getattr(result.children[0], "text") == "Click me"


def test_nested_elements():
    """Test parsing nested elements."""
    result = html_string_to_tdom("<div><p>Paragraph text</p></div>")
    assert isinstance(result, TElement)
    assert result.tag == "div"
    assert len(result.children) == 1

    p_element = result.children[0]
    assert isinstance(p_element, TElement)
    assert p_element.tag == "p"
    assert len(p_element.children) == 1
    assert isinstance(p_element.children[0], TText)
    assert getattr(p_element.children[0], "text") == "Paragraph text"


def test_multiple_root_elements():
    """Test parsing multiple root elements returns fragment."""
    result = html_string_to_tdom("<p>First</p><p>Second</p>")
    assert isinstance(result, TFragment)
    assert len(result.children) == 2

    first_p = result.children[0]
    assert isinstance(first_p, TElement)
    assert first_p.tag == "p"
    assert getattr(first_p.children[0], "text") == "First"

    second_p = result.children[1]
    assert isinstance(second_p, TElement)
    assert second_p.tag == "p"
    assert getattr(second_p.children[0], "text") == "Second"


def test_self_closing_tags():
    """Test parsing self-closing tags."""
    result = html_string_to_tdom('<img src="image.jpg" alt="An image" />')
    assert isinstance(result, TElement)
    assert result.tag == "img"
    assert result.attrs == {"src": "image.jpg", "alt": "An image"}
    assert result.children == []


def test_mixed_content():
    """Test parsing mixed text and element content."""
    result = html_string_to_tdom("Before <em>emphasis</em> after")
    assert isinstance(result, TFragment)
    assert len(result.children) == 3

    # First text node
    assert isinstance(result.children[0], TText)
    assert getattr(result.children[0], "text") == "Before "

    # Emphasis element
    assert isinstance(result.children[1], TElement)
    assert result.children[1].tag == "em"
    assert getattr(result.children[1].children[0], "text") == "emphasis"

    # Last text node
    assert isinstance(result.children[2], TText)
    assert getattr(result.children[2], "text") == " after"


def test_complex_nested_structure():
    """Test parsing complex nested HTML structure."""
    html = """
    <article>
        <header>
            <h1>Title</h1>
            <p class="subtitle">Subtitle text</p>
        </header>
        <main>
            <p>First paragraph with <a href="/link">a link</a>.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </main>
    </article>
    """
    result = html_string_to_tdom(html)
    assert isinstance(result, TElement)
    assert result.tag == "article"

    # Should have header and main children
    assert len(result.children) == 2
    header = result.children[0]
    main = result.children[1]

    assert isinstance(header, TElement)
    assert header.tag == "header"

    assert isinstance(main, TElement)
    assert main.tag == "main"


def test_attributes_with_quotes():
    """Test handling of different quote styles in attributes."""
    result = html_string_to_tdom(
        '<div class="outer" id=\'inner\' data-value="test">Content</div>'
    )
    assert isinstance(result, TElement)
    assert result.tag == "div"
    assert result.attrs == {"class": "outer", "id": "inner", "data-value": "test"}


def test_empty_attributes():
    """Test handling of empty attribute values."""
    result = html_string_to_tdom('<input type="checkbox" checked disabled>')
    assert isinstance(result, TElement)
    assert result.tag == "input"
    # HTML parser normalizes empty attributes to empty strings
    assert result.attrs == {"type": "checkbox", "checked": "", "disabled": ""}


def test_html_entities():
    """Test handling of HTML entities in content."""
    result = html_string_to_tdom("<p>&lt;Hello &amp; welcome&gt;</p>")
    assert isinstance(result, TElement)
    assert result.tag == "p"
    # HTMLParser automatically decodes entities
    assert getattr(result.children[0], "text") == "<Hello & welcome>"


def test_whitespace_handling():
    """Test how whitespace in content is preserved."""
    result = html_string_to_tdom("<div>  \n  Text with   spaces  \n  </div>")
    assert isinstance(result, TElement)
    assert result.tag == "div"
    # Whitespace should be preserved as-is
    assert getattr(result.children[0], "text") == "  \n  Text with   spaces  \n  "


def test_case_normalization():
    """Test that tag names are normalized to lowercase."""
    result = html_string_to_tdom("<DIV><P>Mixed case</P></DIV>")
    assert isinstance(result, TElement)
    assert result.tag == "div"  # HTML parser normalizes to lowercase
    assert getattr(result.children[0], "tag") == "p"


@pytest.mark.parametrize(
    "html_input,expected_type",
    [
        ("", TFragment),
        ("   ", TFragment),
        ("text", TText),
        ("<div></div>", TElement),
        ("<p>One</p><p>Two</p>", TFragment),
        ("text<br/>more", TFragment),
    ],
)
def test_return_type_patterns(html_input, expected_type):
    """Test that different input patterns return expected types."""
    result = html_string_to_tdom(html_input)
    assert isinstance(result, expected_type)
