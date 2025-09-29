# TdomSafe: MarkupSafe Functionality Using tdom Node Trees

## Overview

Create a tdom-based equivalent of MarkupSafe that operates on node trees instead of strings, providing HTML escaping and
safety features while maintaining the structural benefits of working with parsed DOM trees.

## Key Components

### 1. SafeNode Wrapper Class

```python
@dataclass(frozen=True)
class SafeNode:
    """A tdom Node wrapper that marks content as safe for HTML insertion."""
    node: Node
    _is_safe: bool = True

    def __html__(self) -> str:
        """Return HTML string representation."""
        return str(self.node)
```

### 2. Core Functions

**escape_node(input: Node | str | Any) -> SafeNode**

- Escape text content in tdom nodes using walker pattern
- Convert strings to escaped Text nodes
- Preserve Element structure while escaping text content

**safe_node(input: Node | str) -> SafeNode**

- Mark content as safe without escaping
- Wrap existing nodes in SafeNode

**unescape_node(safe_node: SafeNode) -> Node**

- Convert HTML entities back to characters in text nodes
- Return unwrapped, unescaped node tree

### 3. Node Tree Walker

```python
class EscapeWalker:
    """Walker that traverses and transforms tdom node trees for escaping."""

    def walk(self, node: Node) -> Node:
        """Recursively process node tree, escaping text content."""
        # Handle Element, Text, Fragment types
        # Escape text nodes, preserve element structure
```

### 4. Integration Features

**Template Function Integration**

- Support `{safe_content}` and `{escaped_content}` in t-strings
- Automatic escaping of unsafe content in templates

**Component Safety**

- Component functions return SafeNode by default
- Unsafe content automatically escaped when combined

## Implementation Strategy

### Phase 1: Core Walker and Escaping

1. Implement `EscapeWalker` class with recursive traversal
2. Create `escape_node()` function using walker
3. Add HTML entity escaping for text nodes
4. Support for Element attribute escaping

### Phase 2: SafeNode Wrapper System

1. Implement `SafeNode` dataclass with safety tracking
2. Add `safe_node()` and `unescape_node()` functions
3. Implement `__html__()` interface compatibility
4. Support arithmetic operations (concatenation) between SafeNodes

### Phase 3: tdom Integration

1. Modify tdom's html() function to handle SafeNode inputs
2. Add safety checking in template interpolation
3. Automatic escaping for unsafe content in t-strings
4. Component return value safety validation

### Phase 4: Advanced Features

1. Context-aware escaping (HTML vs attribute vs URL contexts)
2. Policy-based escaping rules
3. Custom escaping functions for specific content types
4. Performance optimizations for large node trees

## File Structure

```
src/tdom_sphinx/tdom_safe/
├── __init__.py           # Public API exports
├── core.py              # SafeNode class and core functions
├── walker.py            # Node tree walking and transformation
├── escaping.py          # HTML entity escaping logic
├── integration.py       # tdom/template integration
└── utils.py            # Helper functions and utilities
```

## Benefits Over String-Based MarkupSafe

1. **Structural Preservation**: Maintains DOM tree structure during escaping
2. **Type Safety**: Full type hints and static analysis support
3. **Performance**: Avoids string parsing/rebuilding cycles
4. **Composability**: Easy combination with existing tdom components
5. **Context Awareness**: Can escape based on element context (attributes vs content)
6. **Debugging**: Better error reporting with node location information

## Backward Compatibility

- Implement `__str__()` method for string conversion
- Support existing MarkupSafe patterns via adapter functions
- Gradual migration path from string-based to node-based safety

## Detailed Implementation

### Core Walker Pattern

Based on the existing walker patterns in the codebase (from `url.py` and `aria_testing/utils.py`), implement a generic
node tree walker:

```python
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

    def transform_attributes(self, attrs: dict) -> dict:
        """Override to transform element attributes."""
        return attrs.copy()
```

### HTML Escaping Implementation

```python
import html
from typing import Dict, Any


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
```

### SafeNode Implementation

```python
from dataclasses import dataclass
from typing import Union, Any
import html


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

    def __add__(self, other: Any) -> "SafeNode":
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

    def __radd__(self, other: Any) -> "SafeNode":
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
        # String - escape and convert to Text node
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
        # Convert string to Text node without escaping
        text_node = Text(input_value)
        return SafeNode(text_node, True)
    else:
        text_node = Text(str(input_value))
        return SafeNode(text_node, True)


def unescape_node(safe_node: SafeNode) -> Node:
    """Convert HTML entities back to characters in text nodes."""

    class UnescapeWalker(NodeWalker):
        def visit_text(self, node: Text) -> Text:
            unescaped_text = html.unescape(node.text)
            return Text(unescaped_text)

    walker = UnescapeWalker()
    return walker.walk(safe_node.node)
```

### Usage Examples

```python
from tdom import html, Text, Element
from tdom_sphinx.tdom_safe import escape_node, safe_node, SafeNode

# Basic escaping
unsafe_text = "<script>alert('xss')</script>"
safe_content = escape_node(unsafe_text)
print(safe_content)  # SafeNode containing escaped text

# Working with tdom nodes
element = html(t'<div>{"<em>emphasis</em>"}</div>')
escaped_element = escape_node(element)

# Combining safe and unsafe content
safe_part = safe_node("<strong>Bold</strong>")
unsafe_part = "<script>alert('xss')</script>"
combined = safe_part + unsafe_part  # Automatically escapes unsafe_part


# Template integration
def my_component(user_input: str) -> SafeNode:
    escaped_input = escape_node(user_input)
    return safe_node(html(t"""
    <div class="user-content">
        {escaped_input}
    </div>
    """))
```

### Testing Strategy

```python
def test_escape_node_with_text():
    """Test escaping of text content."""
    unsafe = "<script>alert('xss')</script>"
    safe = escape_node(unsafe)
    assert isinstance(safe, SafeNode)
    assert "&lt;script&gt;" in str(safe)


def test_escape_node_with_element():
    """Test escaping preserves element structure."""
    element = Element(tag="div", children=[Text("<script>")])
    safe = escape_node(element)
    result_str = str(safe)
    assert "<div>" in result_str
    assert "&lt;script&gt;" in result_str


def test_safe_node_combination():
    """Test combining safe nodes."""
    safe1 = safe_node("<em>emphasis</em>")
    safe2 = safe_node("<strong>bold</strong>")
    combined = safe1 + safe2
    assert isinstance(combined, SafeNode)
    # Should contain both without escaping
    result = str(combined)
    assert "<em>emphasis</em>" in result
    assert "<strong>bold</strong>" in result
```

## Migration from MarkupSafe

To ease migration from existing MarkupSafe usage:

```python
# Adapter functions for MarkupSafe compatibility
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
```

This plan provides a comprehensive approach to implementing MarkupSafe functionality using tdom node trees, maintaining
the structural benefits while providing the safety features expected from HTML escaping libraries.