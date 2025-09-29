"""Node tree walking and transformation utilities for tdom_safe."""

from __future__ import annotations

from typing import Dict, Any
from tdom import Node, Element, Text, Fragment


class NodeWalker:
    """Base class for walking tdom node trees."""

    def walk(self, node: Node) -> Node:
        """Walk a node tree and return a transformed tree."""
        if isinstance(node, Text):
            return self.visit_text(node)
        elif isinstance(node, Element):
            return self.visit_element(node)
        elif isinstance(node, Fragment):
            return self.visit_fragment(node)
        else:
            return node

    def visit_text(self, node: Text) -> Node:
        """Override to transform text nodes."""
        return node

    def visit_element(self, node: Element) -> Node:
        """Override to transform element nodes."""
        # Transform children recursively
        new_children = [self.walk(child) for child in node.children]
        # Transform attributes if needed
        new_attrs = self.transform_attributes(node.attrs)
        return Element(tag=node.tag, attrs=new_attrs, children=new_children)

    def visit_fragment(self, node: Fragment) -> Node:
        """Override to transform fragment nodes."""
        new_children = [self.walk(child) for child in node.children]
        return Fragment(children=new_children)

    def transform_attributes(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Override to transform element attributes."""
        return attrs.copy()