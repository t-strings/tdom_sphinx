"""Helper functions and utilities for tdom_safe."""

from __future__ import annotations

from tdom import Element, Fragment, Node, Text


def node_to_text(node: Node) -> str:
    """Extract all text content from a node tree."""
    if isinstance(node, Text):
        return node.text
    elif isinstance(node, Element):
        return "".join(node_to_text(child) for child in node.children)
    elif isinstance(node, Fragment):
        return "".join(node_to_text(child) for child in node.children)
    else:
        return str(node)


def count_nodes(node: Node) -> int:
    """Count the total number of nodes in a tree."""
    if isinstance(node, Text):
        return 1
    elif isinstance(node, Element):
        return 1 + sum(count_nodes(child) for child in node.children)
    elif isinstance(node, Fragment):
        return sum(count_nodes(child) for child in node.children)
    else:
        return 1


def find_text_nodes(node: Node) -> list[Text]:
    """Find all Text nodes in a tree."""
    results = []

    if isinstance(node, Text):
        results.append(node)
    elif isinstance(node, Element):
        for child in node.children:
            results.extend(find_text_nodes(child))
    elif isinstance(node, Fragment):
        for child in node.children:
            results.extend(find_text_nodes(child))

    return results


def is_empty_node(node: Node) -> bool:
    """Check if a node tree contains any meaningful content."""
    if isinstance(node, Text):
        return not node.text.strip()
    elif isinstance(node, Element):
        return all(is_empty_node(child) for child in node.children)
    elif isinstance(node, Fragment):
        return all(is_empty_node(child) for child in node.children)
    else:
        return True
