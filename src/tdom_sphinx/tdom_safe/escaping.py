"""HTML entity escaping logic for tdom_safe."""

from __future__ import annotations

import html
from typing import Dict, Any

from tdom import Text
from .walker import NodeWalker


class EscapeWalker(NodeWalker):
    """Walker that escapes HTML content in text nodes and attributes."""

    def __init__(self, escape_attributes: bool = True):
        self.escape_attributes = escape_attributes

    def visit_text(self, node: Text) -> Text:
        """Escape HTML entities in text content."""
        escaped_text = html.escape(node.text)
        return Text(escaped_text)

    def transform_attributes(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Escape HTML entities in attribute values if enabled."""
        if not self.escape_attributes:
            return attrs.copy()

        escaped_attrs = {}
        for key, value in attrs.items():
            if isinstance(value, str):
                escaped_attrs[key] = html.escape(value)
            else:
                escaped_attrs[key] = value
        return escaped_attrs


class UnescapeWalker(NodeWalker):
    """Walker that unescapes HTML entities in text nodes."""

    def visit_text(self, node: Text) -> Text:
        """Unescape HTML entities in text content."""
        unescaped_text = html.unescape(node.text)
        return Text(unescaped_text)