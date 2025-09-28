"""Test helpers for TXSLT that use tdom instead of BeautifulSoup."""

from __future__ import annotations

from typing import List, Optional

from tdom import Element, Fragment, Node, Text
from tdom.parser import parse_html


def parse_html_string(html_string: str) -> Node:
    """Parse an HTML string into a tdom Node tree."""
    return parse_html(html_string)


def select_one(root: Node, selector: str) -> Optional[Element]:
    """Select the first element matching a CSS-like selector.

    Supports basic selectors:
    - tag name: "div", "span", etc.
    - class: ".classname"
    - combination: "div.classname"
    """
    elements = select_all(root, selector)
    return elements[0] if elements else None


def select_all(root: Node, selector: str) -> List[Element]:
    """Select all elements matching a CSS-like selector."""
    # Handle descendant selectors (space separated)
    if " " in selector:
        parts = selector.split()
        current_elements = [root] if isinstance(root, Element) else []

        for part in parts:
            next_elements = []
            for element in current_elements:
                next_elements.extend(select_all(element, part))
            current_elements = next_elements

        return current_elements

    if selector.startswith("."):
        # Class selector
        class_name = selector[1:]
        return _find_elements_by_class(root, class_name)
    elif "." in selector:
        # Tag + class selector
        tag, class_name = selector.split(".", 1)
        elements = _find_elements_by_tag(root, tag)
        return [el for el in elements if _has_class(el, class_name)]
    else:
        # Tag selector
        return _find_elements_by_tag(root, selector)


def get_text(element: Element, strip: bool = False) -> str:
    """Get the text content of an element."""
    text = _extract_text_content(element)
    return text.strip() if strip else text


def get_attribute(element: Element, name: str) -> Optional[str]:
    """Get an attribute value from an element."""
    return element.attrs.get(name)


def _find_elements_by_tag(root: Node, tag: str) -> List[Element]:
    """Find all elements with the given tag name."""
    result: List[Element] = []

    def visit(node: Node) -> None:
        if isinstance(node, Element):
            if node.tag == tag:
                result.append(node)
            for child in node.children:
                visit(child)
        elif isinstance(node, Fragment):
            for child in node.children:
                visit(child)

    visit(root)
    return result


def _find_elements_by_class(root: Node, class_name: str) -> List[Element]:
    """Find all elements with the given class name."""
    result: List[Element] = []

    def visit(node: Node) -> None:
        if isinstance(node, Element):
            if _has_class(node, class_name):
                result.append(node)
            for child in node.children:
                visit(child)
        elif isinstance(node, Fragment):
            for child in node.children:
                visit(child)

    visit(root)
    return result


def _has_class(element: Element, class_name: str) -> bool:
    """Check if an element has a specific class."""
    class_attr = element.attrs.get("class")
    if not class_attr:
        return False

    # Handle both string and list forms of class attribute
    if isinstance(class_attr, str):
        classes = class_attr.split()
    else:
        classes = [str(class_attr)]

    return class_name in classes


def _extract_text_content(node: Node) -> str:
    """Extract all text content from a node and its children."""
    if isinstance(node, Text):
        return node.text
    elif isinstance(node, Element):
        return "".join(_extract_text_content(child) for child in node.children)
    elif isinstance(node, Fragment):
        return "".join(_extract_text_content(child) for child in node.children)
    else:
        return ""
