"""Pattern matching engine for TXSLT node selection."""

from __future__ import annotations

from typing import List, Optional

from tdom import Node, Element, Fragment, Text


class PatternMatcher:
    """Engine for matching nodes against XPath-like patterns."""

    @staticmethod
    def matches(node: Node, pattern: str) -> bool:
        """Check if a node matches the given pattern."""
        if pattern == "*":
            return True
        if pattern == "node()":
            return True
        if pattern == "text()" and isinstance(node, Text):
            return True
        if pattern == "element()" and isinstance(node, Element):
            return True

        # Element tag name matching
        if isinstance(node, Element):
            return node.tag == pattern

        return False

    @staticmethod
    def select_nodes(root: Node, selector: str) -> List[Node]:
        """Select nodes from root using a simple selector syntax."""
        # Simple implementation for basic selectors
        if selector == ".":
            return [root]
        if selector == "*":
            return PatternMatcher._get_all_children(root)

        # Child element selection by tag name
        if isinstance(root, Element):
            return [
                child
                for child in root.children
                if isinstance(child, Element) and child.tag == selector
            ]
        elif isinstance(root, Fragment):
            return [
                child
                for child in root.children
                if isinstance(child, Element) and child.tag == selector
            ]

        return []

    @staticmethod
    def select_first(root: Node, selector: str) -> Optional[Node]:
        """Select the first node matching the selector."""
        nodes = PatternMatcher.select_nodes(root, selector)
        return nodes[0] if nodes else None

    @staticmethod
    def get_text_content(node: Node) -> str:
        """Get the text content of a node."""
        if isinstance(node, Text):
            return node.text
        elif isinstance(node, Element):
            return "".join(
                PatternMatcher.get_text_content(child) for child in node.children
            )
        elif isinstance(node, Fragment):
            return "".join(
                PatternMatcher.get_text_content(child) for child in node.children
            )
        return ""

    @staticmethod
    def _get_all_children(node: Node) -> List[Node]:
        """Get all children of a node."""
        if isinstance(node, (Element, Fragment)):
            return list(node.children)
        return []

    @staticmethod
    def get_attribute(node: Node, name: str) -> Optional[str]:
        """Get an attribute value from an element."""
        if isinstance(node, Element):
            return node.attrs.get(name)
        return None
