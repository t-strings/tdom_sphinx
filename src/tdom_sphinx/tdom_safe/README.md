# TdomSafe: MarkupSafe for tdom Node Trees

TdomSafe provides MarkupSafe-like functionality but operates on tdom node trees instead of strings, maintaining the structural benefits of working with parsed DOM trees while providing HTML escaping and safety features.

## Quick Start

```python
from tdom_sphinx.tdom_safe import escape_node, safe_node, SafeNode

# Escape dangerous content
dangerous = '<script>alert("XSS")</script>'
safe = escape_node(dangerous)
print(safe)  # Escaped output

# Mark trusted content as safe
trusted = safe_node('<em>This is safe</em>')
print(trusted)  # Unescaped HTML

# Combine safely
combined = trusted + " and " + dangerous  # Automatically escapes dangerous part
```

## Core Functions

### `escape_node(input: Node | str | Any) -> SafeNode`

Escapes HTML content and returns a SafeNode. Works with:
- Strings (treated as plain text and escaped)
- tdom Node trees (text content escaped, structure preserved)
- Other types (converted to string then escaped)

```python
# String escaping
safe_text = escape_node('<script>alert("xss")</script>')

# Node tree escaping
from tdom import Element, Text
element = Element(tag="div", children=[Text("<script>")])
safe_element = escape_node(element)
```

### `safe_node(input: Node | str) -> SafeNode`

Marks content as safe without escaping. Handles HTML strings by parsing them into node trees:

```python
# Safe HTML (will be parsed into node tree)
safe_html = safe_node('<em>trusted emphasis</em>')

# Safe text
safe_text = safe_node('Plain text content')
```

### `unescape_node(safe_node: SafeNode) -> Node`

Converts HTML entities back to characters in text nodes:

```python
escaped = escape_node('<em>test</em>')
unescaped = unescape_node(escaped)  # Returns original content
```

## SafeNode Class

The `SafeNode` wrapper provides:

- **Safety tracking**: Marks content as safe for HTML insertion
- **Arithmetic operations**: Automatic escaping when combining with unsafe content
- **Framework compatibility**: Implements `__html__()` for MarkupSafe compatibility

```python
safe1 = safe_node('<em>emphasis</em>')
safe2 = safe_node('<strong>bold</strong>')
unsafe = '<script>alert("xss")</script>'

# Safe + Safe = Safe (no escaping)
combined_safe = safe1 + safe2

# Safe + Unsafe = Safe (unsafe part escaped)
combined_mixed = safe1 + unsafe
```

## MarkupSafe Compatibility

Drop-in replacements for common MarkupSafe functions:

```python
from tdom_sphinx.tdom_safe import Markup, escape, escape_silent

# MarkupSafe-style usage
markup = Markup('<div>Safe content</div>')
escaped = escape('<div onclick="alert()">Dangerous</div>')
silent = escape_silent(None)  # Handles None gracefully
```

## HTML String to Node Conversion

TdomSafe leverages the existing `html_string_to_tdom()` function for converting HTML strings to tdom node trees:

```python
from tdom_sphinx.utils import html_string_to_tdom

# Simple HTML
node = html_string_to_tdom('<div>Hello <em>world</em>!</div>')
# Returns: Element(tag='div', ...)

# Multiple elements
nodes = html_string_to_tdom('<p>First</p><p>Second</p>')
# Returns: Fragment(children=[...])

# Empty content
empty = html_string_to_tdom('')
# Returns: Fragment(children=[])
```

## Template Integration

Works seamlessly with tdom t-strings:

```python
from tdom import html

safe_title = safe_node('<h1>Page Title</h1>')
user_input = escape_node('<script>alert("xss")</script>')

page = html(t'''
<html>
<body>
    {safe_title}
    <div>User content: {user_input}</div>
</body>
</html>
''')
```

## Benefits Over String-Based MarkupSafe

1. **Structural Preservation**: Maintains DOM tree structure during escaping
2. **Type Safety**: Full type hints and static analysis support
3. **Performance**: Avoids string parsing/rebuilding cycles
4. **Composability**: Easy combination with existing tdom components
5. **Context Awareness**: Can escape based on element context
6. **Debugging**: Better error reporting with node location information

## Walker Pattern

For advanced usage, TdomSafe provides a walker pattern for custom transformations:

```python
from tdom_sphinx.tdom_safe import NodeWalker, EscapeWalker

class CustomWalker(NodeWalker):
    def visit_text(self, node):
        # Custom text transformation
        return Text(node.text.upper())

# Use custom walker
walker = CustomWalker()
transformed = walker.walk(my_node_tree)
```

## Testing

Run the test suite:

```bash
PYTHONPATH=src uv run pytest src/tdom_sphinx/tdom_safe/test_tdom_safe.py -v
```

See `tdom_safe_demo.py` in the project root for comprehensive usage examples.