#!/usr/bin/env python3
"""Demo script showcasing TdomSafe functionality."""

from tdom import Element, Text, html, Fragment

from tdom_sphinx.tdom_safe import (
    Markup,
    escape,
    escape_node,
    safe_node,
    unescape_node,
)
from tdom_sphinx.utils import html_string_to_tdom


def demo_html_string_to_tdom():
    """Demonstrate converting HTML strings to tdom Node trees."""
    print("=== HTML String to tdom Node Tree ===")

    # Simple HTML
    simple_html = "<div>Hello <em>world</em>!</div>"
    node1 = html_string_to_tdom(simple_html)
    print(f"Input: {simple_html}")
    print(f"Node type: {type(node1).__name__}")
    print(f"Output: {node1}")
    print()

    # Complex HTML
    complex_html = """
    <article class="post">
        <header>
            <h1>Blog Post Title</h1>
            <p class="meta">By Author on <time>2023-01-01</time></p>
        </header>
        <div class="content">
            <p>This is a paragraph with <strong>bold</strong> text.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </div>
    </article>
    """
    node2 = html_string_to_tdom(complex_html)
    print(f"Complex HTML converted to: {type(node2).__name__}")
    print(f"Rendered: {node2}")
    print()

    # Multiple root elements
    multi_root = "<p>First</p><p>Second</p>"
    node3 = html_string_to_tdom(multi_root)
    print(f"Multi-root: {multi_root}")
    print(f"Node type: {type(node3).__name__}")
    print(
        f"Children count: {len(node3.children) if isinstance(node3, (Element, Fragment)) else 'N/A'}"
    )
    print()


def demo_basic_escaping():
    """Demonstrate basic HTML escaping functionality."""
    print("=== Basic HTML Escaping ===")

    # Dangerous input
    dangerous = '<script>alert("XSS attack!")</script>'

    # Escape it
    safe = escape_node(dangerous)
    print(f"Dangerous input: {dangerous}")
    print(f"Escaped: {safe}")
    print(f"Type: {type(safe).__name__}")
    print()

    # Mark as safe (trusted content)
    trusted_html = "<em>This is trusted emphasis</em>"
    safe_trusted = safe_node(trusted_html)
    print(f"Trusted input: {trusted_html}")
    print(f"Safe node: {safe_trusted}")
    print()


def demo_node_tree_escaping():
    """Demonstrate escaping tdom node trees."""
    print("=== Node Tree Escaping ===")

    # Create a node tree with unsafe content
    unsafe_element = Element(
        tag="div",
        attrs={"class": "user-content", "title": 'Contains "quotes" & <entities>'},
        children=[
            Text("User said: "),
            Element(tag="span", children=[Text('<script>alert("bad")</script>')]),
            Text(" - end quote"),
        ],
    )

    print("Original element:")
    print(f"  {unsafe_element}")
    print()

    # Escape the entire tree
    safe_tree = escape_node(unsafe_element)
    print("Escaped element:")
    print(f"  {safe_tree}")
    print()


def demo_safe_combination():
    """Demonstrate combining safe and unsafe content."""
    print("=== Safe Content Combination ===")

    # Safe content
    safe_emphasis = safe_node("<em>trusted emphasis</em>")
    safe_bold = safe_node("<strong>trusted bold</strong>")

    # Unsafe content
    user_input = '<script>alert("XSS")</script>'

    # Combine them
    combined = safe_emphasis + " and " + safe_bold + " with user: " + user_input

    print("Safe emphasis:", safe_emphasis)
    print("Safe bold:", safe_bold)
    print("User input (unsafe):", user_input)
    print("Combined result:", combined)
    print()


def demo_markupsafe_compatibility():
    """Demonstrate MarkupSafe compatibility functions."""
    print("=== MarkupSafe Compatibility ===")

    # Using Markup function
    markup = Markup("<div>Safe markup</div>")
    print(f"Markup('<div>Safe markup</div>'): {markup}")

    # Using escape function
    escaped = escape('<div onclick="alert()">Dangerous</div>')
    print(f"escape('<div onclick=\"alert()\">Dangerous</div>'): {escaped}")

    # Combining
    combined = markup + " " + escaped
    print(f"Combined: {combined}")
    print()


def demo_template_integration():
    """Demonstrate integration with tdom t-strings."""
    print("=== Template Integration ===")

    # Safe content for interpolation
    safe_title = safe_node("<h1>Page Title</h1>")
    user_content = escape_node('<script>alert("XSS")</script>')

    # Use in a template
    page = html(t"""
    <html>
    <head><title>Demo Page</title></head>
    <body>
        {safe_title}
        <div class="user-content">
            User submitted: {user_content}
        </div>
    </body>
    </html>
    """)

    print("Template with safe and escaped content:")
    print(page)
    print()


def demo_unescaping():
    """Demonstrate unescaping functionality."""
    print("=== Unescaping ===")

    # Start with some content
    original = "<em>emphasis</em> & <strong>bold</strong>"
    print(f"Original: {original}")

    # Escape it
    escaped = escape_node(original)
    print(f"Escaped: {escaped}")

    # Unescape it back
    unescaped = unescape_node(escaped)
    print(f"Unescaped node: {unescaped}")
    print(f"Unescaped text: {unescaped}")
    print()


if __name__ == "__main__":
    print("TdomSafe Demo - MarkupSafe functionality using tdom node trees")
    print("=" * 60)
    print()

    demo_html_string_to_tdom()
    demo_basic_escaping()
    demo_node_tree_escaping()
    demo_safe_combination()
    demo_markupsafe_compatibility()
    demo_template_integration()
    demo_unescaping()

    print("Demo completed!")