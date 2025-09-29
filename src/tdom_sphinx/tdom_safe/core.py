"""SafeNode class and core functions for tdom_safe."""

from __future__ import annotations

import html
from dataclasses import dataclass
from typing import Union, Any

from tdom import Node, Text, Fragment
from tdom_sphinx.utils import html_string_to_tdom
from .escaping import EscapeWalker, UnescapeWalker


@dataclass(frozen=True)
class SafeNode:
    """A tdom Node wrapper that marks content as safe for HTML insertion."""

    node: Node
    _is_safe: bool = True

    def __html__(self) -> str:
        """Return HTML string representation for framework compatibility."""
        return str(self.node)

    def __str__(self) -> str:
        """Convert to string representation."""
        return str(self.node)

    def __add__(self, other: Any) -> SafeNode:
        """Concatenate with other content, escaping if necessary."""
        if isinstance(other, SafeNode):
            # Both are safe, combine their nodes
            combined = Fragment(children=[self.node, other.node])
            return SafeNode(combined, True)
        else:
            # Other content is unsafe, escape it first
            escaped_other = escape_node(other)
            combined = Fragment(children=[self.node, escaped_other.node])
            return SafeNode(combined, True)

    def __radd__(self, other: Any) -> SafeNode:
        """Right-hand addition (when other + safe_node)."""
        if isinstance(other, SafeNode):
            combined = Fragment(children=[other.node, self.node])
            return SafeNode(combined, True)
        else:
            escaped_other = escape_node(other)
            combined = Fragment(children=[escaped_other.node, self.node])
            return SafeNode(combined, True)


def escape_node(input_value: Union[Node, str, Any]) -> SafeNode:
    """Escape content and return a SafeNode."""
    if isinstance(input_value, SafeNode):
        # Already safe, return as-is
        return input_value
    elif isinstance(input_value, Node):
        # tdom Node - escape text content
        walker = EscapeWalker()
        escaped_node = walker.walk(input_value)
        return SafeNode(escaped_node, True)
    elif isinstance(input_value, str):
        # String - always treat as plain text and escape
        escaped_text = html.escape(input_value)
        text_node = Text(escaped_text)
        return SafeNode(text_node, True)
    else:
        # Other types - convert to string, then escape
        escaped_text = html.escape(str(input_value))
        text_node = Text(escaped_text)
        return SafeNode(text_node, True)


def safe_node(input_value: Union[Node, str]) -> SafeNode:
    """Mark content as safe without escaping."""
    if isinstance(input_value, SafeNode):
        return input_value
    elif isinstance(input_value, Node):
        return SafeNode(input_value, True)
    elif isinstance(input_value, str):
        # Check if it looks like HTML and parse if so
        if _looks_like_html(input_value):
            parsed_node = html_string_to_tdom(input_value)
            return SafeNode(parsed_node, True)
        else:
            # Plain text - convert to Text node without escaping
            text_node = Text(input_value)
            return SafeNode(text_node, True)
    else:
        text_node = Text(str(input_value))
        return SafeNode(text_node, True)


def unescape_node(safe_node: SafeNode) -> Node:
    """Convert HTML entities back to characters in text nodes."""
    walker = UnescapeWalker()
    return walker.walk(safe_node.node)


def _looks_like_html(text: str) -> bool:
    """Simple heuristic to detect if a string contains HTML markup."""
    text = text.strip()
    return ('<' in text and '>' in text) or ('&' in text and ';' in text)


# MarkupSafe compatibility functions
def Markup(content: Union[str, Node]) -> SafeNode:
    """MarkupSafe.Markup compatibility function."""
    return safe_node(content)


def escape(content: Union[str, Node]) -> SafeNode:
    """MarkupSafe.escape compatibility function."""
    return escape_node(content)


def escape_silent(content: Union[str, Node, None]) -> SafeNode:
    """MarkupSafe.escape_silent compatibility function."""
    if content is None:
        return safe_node("")
    return escape_node(content)