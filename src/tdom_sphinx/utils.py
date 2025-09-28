"""Utility functions for tdom-sphinx."""
from __future__ import annotations

from html.parser import HTMLParser
from typing import Any

from tdom.nodes import Element as TElement, Fragment as TFragment, Text as TText, Node as TNode


class TdomHTMLParser(HTMLParser):
    """Custom HTML parser that builds tdom Node trees."""

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[TElement] = []
        self.root_nodes: list[TNode] = []
        self.current_text: str = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Handle opening HTML tags."""
        # Flush any pending text content
        self._flush_text()

        # Convert attrs list to dict, handling None values
        attrs_dict = {name: value or "" for name, value in attrs}

        # Create new element
        element = TElement(tag=tag, attrs=attrs_dict, children=[])

        if self.stack:
            # Add to current parent's children
            self.stack[-1].children.append(element)
        else:
            # This is a root element
            self.root_nodes.append(element)

        # Push onto stack
        self.stack.append(element)

    def handle_endtag(self, tag: str) -> None:
        """Handle closing HTML tags."""
        # Flush any pending text content
        self._flush_text()

        # Pop from stack
        if self.stack:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        """Handle text content between tags."""
        self.current_text += data

    def _flush_text(self) -> None:
        """Add accumulated text as a Text node if non-empty."""
        if self.current_text.strip():  # Only add non-whitespace text
            text_node = TText(self.current_text)

            if self.stack:
                # Add to current parent's children
                self.stack[-1].children.append(text_node)
            else:
                # This is root-level text
                self.root_nodes.append(text_node)

        self.current_text = ""

    def close(self) -> TNode:
        """Finish parsing and return the root node(s)."""
        # Flush any remaining text
        self._flush_text()

        super().close()

        # Return appropriate node type
        if len(self.root_nodes) == 0:
            # Empty content - return empty fragment
            return TFragment(children=[])
        elif len(self.root_nodes) == 1:
            # Single root - return it directly
            return self.root_nodes[0]
        else:
            # Multiple roots - wrap in fragment
            return TFragment(children=self.root_nodes)


def html_string_to_tdom(html_string: str) -> TNode:
    """Convert an HTML string into a tdom Node tree.

    Uses Python's built-in html.parser to parse the HTML and constructs
    tdom Node objects following the same patterns used throughout the codebase.

    Args:
        html_string: A string containing HTML content

    Returns:
        A tdom Node tree representing the parsed HTML:
        - Single root element returns TElement
        - Multiple root elements returns TFragment
        - Text-only content returns TText
        - Empty content returns empty TFragment

    Examples:
        >>> html_string_to_tdom("<div>Hello</div>")
        TElement(tag='div', attrs={}, children=[TText('Hello')])

        >>> html_string_to_tdom("<p>One</p><p>Two</p>")
        TFragment(children=[TElement(...), TElement(...)])

        >>> # Can be used with tdom's html() function:
        >>> from tdom import html
        >>> parsed_node = html_string_to_tdom("<em>emphasis</em>")
        >>> result = html(t"<div>Before {parsed_node} after</div>")
        >>> # Creates: <div>Before <em>emphasis</em> after</div>
    """
    if not html_string.strip():
        # Empty or whitespace-only string
        return TFragment(children=[])

    parser = TdomHTMLParser()
    parser.feed(html_string)
    return parser.close()