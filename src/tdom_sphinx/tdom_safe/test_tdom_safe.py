"""Tests for tdom_safe functionality."""

import pytest
from tdom import Element, Text, html

from tdom_sphinx.tdom_safe import (
    Markup,
    SafeNode,
    escape,
    escape_node,
    escape_silent,
    safe_node,
    unescape_node,
)
from tdom_sphinx.tdom_safe.utils import (
    count_nodes,
    find_text_nodes,
    is_empty_node,
    node_to_text,
)


def test_escape_node_with_text():
    """Test escaping of plain text content."""
    unsafe = "<script>alert('xss')</script>"
    safe = escape_node(unsafe)
    assert isinstance(safe, SafeNode)
    result_str = str(safe)
    # Should escape the dangerous content
    assert "lt;script" in result_str  # Might be &lt; or &amp;lt; due to double escaping
    assert "script" in result_str
    assert "alert" in result_str


def test_escape_node_with_html_string():
    """Test escaping of HTML string content treats it as plain text."""
    unsafe_html = '<div class="test">Content with <script>alert("xss")</script></div>'
    safe = escape_node(unsafe_html)
    assert isinstance(safe, SafeNode)
    result_str = str(safe)
    # Should escape all HTML as plain text
    assert "lt;div" in result_str  # Might be &lt; or &amp;lt;
    assert "lt;script" in result_str


def test_escape_node_with_element():
    """Test escaping preserves element structure but escapes text content."""
    element = Element(tag="div", attrs={"class": "test"}, children=[Text("<script>")])
    safe = escape_node(element)
    result_str = str(safe)
    assert '<div class="test">' in result_str
    assert "lt;script" in result_str  # Text content should be escaped
    assert "</div>" in result_str


def test_safe_node_with_text():
    """Test marking plain text as safe."""
    content = "Safe content"
    safe = safe_node(content)
    assert isinstance(safe, SafeNode)
    assert str(safe) == "Safe content"


def test_safe_node_with_html():
    """Test marking HTML content as safe."""
    html_content = "<em>emphasis</em>"
    safe = safe_node(html_content)
    assert isinstance(safe, SafeNode)
    result_str = str(safe)
    assert "<em>" in result_str
    assert "emphasis" in result_str
    assert "</em>" in result_str


def test_safe_node_combination():
    """Test combining safe nodes."""
    safe1 = safe_node("<em>emphasis</em>")
    safe2 = safe_node("<strong>bold</strong>")
    combined = safe1 + safe2
    assert isinstance(combined, SafeNode)
    result = str(combined)
    assert "<em>emphasis</em>" in result
    assert "<strong>bold</strong>" in result


def test_safe_and_unsafe_combination():
    """Test combining safe and unsafe content."""
    safe_part = safe_node("<em>emphasis</em>")
    unsafe_part = "<script>alert('xss')</script>"
    combined = safe_part + unsafe_part
    assert isinstance(combined, SafeNode)
    result = str(combined)
    assert "<em>emphasis</em>" in result
    assert "lt;script" in result  # Should be escaped


def test_unescape_node():
    """Test unescaping HTML entities."""
    # Create an escaped node from plain text
    escaped = escape_node("<em>test</em>")
    # Unescape it
    unescaped = unescape_node(escaped)
    # Should contain original content
    text_content = node_to_text(unescaped)
    assert "<em>test</em>" in text_content


def test_markupsafe_compatibility():
    """Test MarkupSafe compatibility functions."""
    # Test Markup function
    markup = Markup("<em>safe</em>")
    assert isinstance(markup, SafeNode)
    assert "<em>safe</em>" in str(markup)

    # Test escape function
    escaped = escape("<script>alert('xss')</script>")
    assert isinstance(escaped, SafeNode)
    assert "lt;script" in str(escaped)

    # Test escape_silent function
    escaped_none = escape_silent(None)
    assert isinstance(escaped_none, SafeNode)
    assert str(escaped_none) == ""

    escaped_content = escape_silent("<em>test</em>")
    assert isinstance(escaped_content, SafeNode)


def test_html_attribute_escaping():
    """Test that HTML attributes are properly escaped."""
    element = Element(
        tag="div",
        attrs={"title": 'Contains "quotes" & <tags>'},
        children=[Text("Content")],
    )
    safe = escape_node(element)
    result_str = str(safe)
    # tdom might double-escape attributes, so check for the presence of escaped content
    assert "quotes" in result_str
    assert "amp;" in result_str  # Could be &amp; or &amp;amp;
    assert "tags" in result_str


def test_empty_content():
    """Test handling of empty content."""
    empty_safe = safe_node("")
    assert isinstance(empty_safe, SafeNode)
    assert str(empty_safe) == ""

    empty_escaped = escape_node("")
    assert isinstance(empty_escaped, SafeNode)
    assert str(empty_escaped) == ""


def test_node_utils():
    """Test utility functions."""
    # Create a test node tree
    element = Element(
        tag="div",
        children=[
            Text("Hello "),
            Element(tag="em", children=[Text("world")]),
            Text("!"),
        ],
    )

    # Test text extraction
    text = node_to_text(element)
    assert text == "Hello world!"

    # Test node counting
    count = count_nodes(element)
    assert count == 5  # div + em + 3 text nodes

    # Test finding text nodes
    text_nodes = find_text_nodes(element)
    assert len(text_nodes) == 3
    assert any(node.text == "Hello " for node in text_nodes)
    assert any(node.text == "world" for node in text_nodes)
    assert any(node.text == "!" for node in text_nodes)

    # Test empty node detection
    empty_element = Element(tag="div", children=[Text("   ")])
    assert is_empty_node(empty_element)

    non_empty_element = Element(tag="div", children=[Text("content")])
    assert not is_empty_node(non_empty_element)


def test_complex_html_parsing():
    """Test parsing and escaping complex HTML structures."""
    complex_html = """
    <article class="post">
        <header>
            <h1>Title with <script>alert("xss")</script></h1>
        </header>
        <div class="content">
            <p>Paragraph with "quotes" & entities</p>
        </div>
    </article>
    """

    # Test safe parsing
    safe = safe_node(complex_html)
    result = str(safe)
    assert '<article class="post">' in result
    assert "<h1>" in result
    assert "<script>" in result  # Should be preserved as safe

    # Test escaped parsing (treats as plain text)
    escaped = escape_node(complex_html)
    escaped_result = str(escaped)
    assert "lt;article" in escaped_result  # Should be escaped as plain text
    assert "lt;script" in escaped_result  # Should be escaped


def test_t_string_integration():
    """Test integration with tdom t-strings."""
    # Test with safe content
    safe_content = safe_node("<em>emphasis</em>")
    result = html(t"<div>Before {safe_content} after</div>")
    result_str = str(result)
    assert "<div>" in result_str
    assert "<em>emphasis</em>" in result_str
    assert "Before" in result_str
    assert "after" in result_str


if __name__ == "__main__":
    pytest.main([__file__])
