"""
Utility functions for text extraction and normalization from tdom nodes.
"""

import re
from typing import Union, Optional, Pattern

from tdom import Node, Element, Text, Fragment


def get_text_content(node: Node) -> str:
    """
    Extract all text content from a tdom node, similar to textContent in DOM.

    Args:
        node: The tdom node to extract text from

    Returns:
        The concatenated text content of the node and all its descendants
    """
    if isinstance(node, Text):
        return node.text
    elif isinstance(node, Element):
        return "".join(get_text_content(child) for child in node.children)
    elif isinstance(node, Fragment):
        return "".join(get_text_content(child) for child in node.children)
    else:
        # For other node types (Comment, DocumentType), return empty string
        return ""


def normalize_text(text: str, *, collapse_whitespace: bool = True, trim: bool = True) -> str:
    """
    Normalize text for matching purposes.

    Args:
        text: The text to normalize
        collapse_whitespace: Whether to collapse multiple whitespace characters into single spaces
        trim: Whether to strip leading and trailing whitespace

    Returns:
        The normalized text
    """
    if collapse_whitespace:
        # Replace any sequence of whitespace characters with a single space
        text = re.sub(r'\s+', ' ', text)

    if trim:
        text = text.strip()

    return text


def matches_text(
    element_text: str,
    matcher: Union[str, Pattern[str]],
    *,
    exact: bool = True,
    normalize: bool = True
) -> bool:
    """
    Check if element text matches the given matcher.

    Args:
        element_text: The text content of the element
        matcher: String or regex pattern to match against
        exact: Whether to use exact matching (vs substring matching)
        normalize: Whether to normalize text before matching

    Returns:
        True if the text matches, False otherwise
    """
    if normalize:
        element_text = normalize_text(element_text)

    if hasattr(matcher, 'search') and callable(getattr(matcher, 'search')):  # It's a regex pattern
        return bool(getattr(matcher, 'search')(element_text))
    elif isinstance(matcher, str):
        if normalize:
            matcher = normalize_text(matcher)

        if exact:
            return element_text == matcher
        else:
            return matcher.lower() in element_text.lower()
    else:
        return False


def find_elements_by_attribute(
    container: Node,
    attribute: str,
    value: Optional[str] = None
) -> list[Element]:
    """
    Find all elements within container that have the specified attribute.

    Args:
        container: The container node to search within
        attribute: The attribute name to look for
        value: Optional specific value the attribute must have

    Returns:
        List of matching elements
    """
    results: list[Element] = []

    def traverse(node: Node) -> None:
        if isinstance(node, Element):
            if attribute in node.attrs:
                if value is None or node.attrs[attribute] == value:
                    results.append(node)
            # Continue traversing children
            for child in node.children:
                traverse(child)
        elif isinstance(node, Fragment):
            for child in node.children:
                traverse(child)

    traverse(container)
    return results


def find_elements_by_tag(container: Node, tag: str) -> list[Element]:
    """
    Find all elements within container that have the specified tag name.

    Args:
        container: The container node to search within
        tag: The tag name to look for

    Returns:
        List of matching elements
    """
    results: list[Element] = []

    def traverse(node: Node) -> None:
        if isinstance(node, Element):
            if node.tag.lower() == tag.lower():
                results.append(node)
            # Continue traversing children
            for child in node.children:
                traverse(child)
        elif isinstance(node, Fragment):
            for child in node.children:
                traverse(child)

    traverse(container)
    return results


def get_all_elements(container: Node) -> list[Element]:
    """
    Get all Element nodes within the container.

    Args:
        container: The container node to search within

    Returns:
        List of all elements in the container
    """
    results: list[Element] = []

    def traverse(node: Node) -> None:
        if isinstance(node, Element):
            results.append(node)
            # Continue traversing children
            for child in node.children:
                traverse(child)
        elif isinstance(node, Fragment):
            for child in node.children:
                traverse(child)

    traverse(container)
    return results