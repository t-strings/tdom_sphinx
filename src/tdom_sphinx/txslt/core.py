"""Core TXSLT functionality - templates, transformations, and helper functions."""

from __future__ import annotations

from functools import wraps
from string.templatelib import Template
from typing import Callable, List, Optional, Union

from tdom import Element, Fragment, Node, Text
from tdom import html as tdom_html

from .patterns import PatternMatcher
from .registry import TemplateContext, get_global_registry


def template(pattern: str, priority: int = 0, mode: Optional[str] = None) -> Callable:
    """Decorator to register a template function with a pattern.

    Args:
        pattern: The pattern to match (e.g., "person", "*", "text()")
        priority: Template priority (higher priority templates match first)
        mode: Optional mode for template processing

    Example:
        @template(pattern="person")
        def person_template(node, context):
            return html(t'''<div class="person">{node.text}</div>''')
    """

    def decorator(func: Callable) -> Callable:
        # Register the template in the global registry
        registry = get_global_registry()
        registry.register(pattern, func, priority, mode)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def apply_templates(
    nodes: Union[Node, List[Node]],
    mode: Optional[str] = None,
    context: Optional[TemplateContext] = None,
) -> Node:
    """Apply templates to nodes recursively.

    Args:
        nodes: Node or list of nodes to process
        mode: Optional mode for template selection
        context: Template context (created if not provided)

    Returns:
        Transformed node tree
    """
    if context is None:
        context = TemplateContext(mode=mode)

    registry = get_global_registry()

    # Handle single node
    if isinstance(nodes, Node):
        nodes = [nodes]

    results: List[Node] = []

    for i, node in enumerate(nodes):
        # Update context for current node
        node_context = context.copy(current_node=node, position=i + 1, size=len(nodes))

        # Find matching template
        template_info = registry.find_template(node, mode)

        if template_info:
            # Apply the template
            result = template_info.function(node, node_context)
            if isinstance(result, Node):
                results.append(result)
            elif result is not None:
                # Convert other types to text nodes
                results.append(Text(str(result)))
        else:
            # Default behavior: copy the node and apply templates to children
            result = _default_template(node, node_context)
            if result:
                results.append(result)

    # Return single node or fragment
    if len(results) == 1:
        return results[0]
    elif len(results) == 0:
        return Fragment(children=[])
    else:
        return Fragment(children=results)


def _default_template(node: Node, context: TemplateContext) -> Optional[Node]:
    """Default template behavior for unmatched nodes."""
    if isinstance(node, Text):
        return node
    elif isinstance(node, Element):
        # Apply templates to children
        transformed_children = []
        if node.children:
            child_result = apply_templates(node.children, context.mode, context)
            if isinstance(child_result, Fragment):
                transformed_children = child_result.children
            else:
                transformed_children = [child_result]

        return Element(
            tag=node.tag, attrs=node.attrs.copy(), children=transformed_children
        )
    elif isinstance(node, Fragment):
        # Apply templates to children
        transformed_children = []
        if node.children:
            child_result = apply_templates(node.children, context.mode, context)
            if isinstance(child_result, Fragment):
                transformed_children = child_result.children
            else:
                transformed_children = [child_result]

        return Fragment(children=transformed_children)

    return node


def select(node: Node, selector: str) -> List[Node]:
    """Select nodes using a simple selector syntax.

    Args:
        node: Root node to search from
        selector: Selector string (e.g., "name", "*", ".")

    Returns:
        List of matching nodes
    """
    return PatternMatcher.select_nodes(node, selector)


def select_first(node: Node, selector: str) -> Optional[Node]:
    """Select the first node matching the selector.

    Args:
        node: Root node to search from
        selector: Selector string

    Returns:
        First matching node or None
    """
    return PatternMatcher.select_first(node, selector)


def value_of(node: Node, selector: Optional[str] = None) -> str:
    """Get the text content of a node or selected child.

    Args:
        node: Node to extract text from
        selector: Optional selector for child node

    Returns:
        Text content as string
    """
    if selector:
        selected = select_first(node, selector)
        if selected:
            return PatternMatcher.get_text_content(selected)
        return ""
    else:
        return PatternMatcher.get_text_content(node)


def copy_of(node: Node) -> Node:
    """Create a deep copy of a node.

    Args:
        node: Node to copy

    Returns:
        Deep copy of the node
    """
    if isinstance(node, Text):
        return Text(node.text)
    elif isinstance(node, Element):
        return Element(
            tag=node.tag,
            attrs=node.attrs.copy(),
            children=[copy_of(child) for child in node.children],
        )
    elif isinstance(node, Fragment):
        return Fragment(children=[copy_of(child) for child in node.children])
    else:
        return node


def html(template: Template) -> Node:
    """Create HTML nodes from t-string template.

    This is a re-export of tdom's html function for convenience.
    """
    return tdom_html(template)
