# TXSLT: T-String XSLT

A modern t-string DSL that extends tdom's capabilities to handle recursive descent and pattern matching transformations
similar to XSLT, but with modern Python syntax and type safety.

## Overview

TXSLT brings the power of XSLT's template-based transformation model to Python's t-strings, providing:

- **Pattern-based templates** using decorators
- **Recursive descent processing** with `apply_templates()`
- **Mode-based transformations** for different contexts
- **Priority-based template resolution**
- **XPath-like node selection**
- **Type safety** with modern Python features

## Quick Start

```python
from tdom import Element, Text, html
from tdom_sphinx.txslt import template, apply_templates, select, value_of


# Define templates with patterns
@template(pattern="person")
def person_template(node, context):
    name = value_of(node, "name")
    age = value_of(node, "age")
    return html(t"""
    <div class="person">
        <h3>{name}</h3>
        <p>Age: {age}</p>
        {apply_templates(select(node, "address"))}
    </div>
    """)


@template(pattern="address")
def address_template(node, context):
    street = value_of(node, "street")
    city = value_of(node, "city")
    return html(t"""
    <div class="address">
        <p>{street}</p>
        <p>{city}</p>
    </div>
    """)


# Create source data
person_data = Element(
    tag="person",
    children=[
        Element(tag="name", children=[Text("John Smith")]),
        Element(tag="age", children=[Text("35")]),
        Element(
            tag="address",
            children=[
                Element(tag="street", children=[Text("123 Main St")]),
                Element(tag="city", children=[Text("Anytown")]),
            ]
        )
    ]
)

# Transform the data
result = apply_templates(person_data)
print(str(result))
```

## Core Functions

### `@template(pattern, priority=0, mode=None)`

Register a template function with a pattern:

```python
@template(pattern="book", priority=5, mode="summary")
def book_summary_template(node, context):
    title = value_of(node, "title")
    return html(t"""<span>{title}</span>""")
```

**Parameters:**

- `pattern`: Element name, `"*"` (any element), `"text()"` (text nodes), or `"node()"` (any node)
- `priority`: Higher priority templates are matched first (default: 0)
- `mode`: Optional mode for context-specific processing

### `apply_templates(nodes, mode=None, context=None)`

Apply templates recursively to nodes:

```python
# Apply to single node
result = apply_templates(my_node)

# Apply to list of nodes
result = apply_templates([node1, node2, node3])

# Apply with specific mode
result = apply_templates(nodes, mode="detailed")
```

### `select(node, selector)`

Select child nodes using simple selectors:

```python
# Select all 'name' elements
names = select(person, "name")

# Select all children
children = select(parent, "*")

# Select current node
current = select(node, ".")
```

### `value_of(node, selector=None)`

Extract text content:

```python
# Get text of current node
text = value_of(text_node)

# Get text of selected child
name_text = value_of(person, "name")
```

### `copy_of(node)`

Create deep copy of a node:

```python
copied_node = copy_of(original_node)
```

## Advanced Features

### Template Priorities

Higher priority templates are selected first:

```python
@template(pattern="item", priority=1)
def generic_item_template(node, context):
    return html(t"""<span>Generic item</span>""")


@template(pattern="item", priority=10)  # This will be selected
def special_item_template(node, context):
    return html(t"""<span>Special item</span>""")
```

### Mode-based Processing

Use modes for different transformation contexts:

```python
@template(pattern="article", mode="summary")
def article_summary(node, context):
    title = value_of(node, "title")
    return html(t"""<h4>{title}</h4>""")


@template(pattern="article", mode="full")
def article_full(node, context):
    title = value_of(node, "title")
    content = value_of(node, "content")
    return html(t"""
    <article>
        <h1>{title}</h1>
        <div>{content}</div>
    </article>
    """)


# Use different modes
summary_result = apply_templates(articles, mode="summary")
full_result = apply_templates(articles, mode="full")
```

### Recursive Hierarchical Processing

Perfect for nested structures:

```python
@template(pattern="category")
def category_template(node, context):
    name = value_of(node, "name")
    subcategories = select(node, "category")  # Recursive!
    items = select(node, "item")

    return html(t"""
    <div class="category">
        <h3>{name}</h3>
        {apply_templates(subcategories)}
        <ul>
            {apply_templates(items)}
        </ul>
    </div>
    """)


@template(pattern="item")
def item_template(node, context):
    name = value_of(node, "name")
    return html(t"""<li>{name}</li>""")
```

## Pattern Matching

TXSLT supports these pattern types:

- **Element names**: `"person"`, `"book"`, `"address"`
- **Universal**: `"*"` matches any element
- **Node types**: `"text()"` for text nodes, `"node()"` for any node
- **Current node**: `"."` selects the current node in selectors

## Template Context

Template functions receive two parameters:

1. **`node`**: The current node being processed
2. **`context`**: TemplateContext with metadata:
    - `context.variables`: Dictionary for custom variables
    - `context.current_node`: Currently processing node
    - `context.mode`: Current processing mode
    - `context.position`: Position in current node list (1-based)
    - `context.size`: Size of current node list

```python
@template(pattern="item")
def numbered_item_template(node, context):
    name = value_of(node, "name")
    pos = context.position
    return html(t"""<li>{pos}. {name}</li>""")
```

## Comparison with XSLT

| XSLT                                      | TXSLT                                      |
|-------------------------------------------|--------------------------------------------|
| `<xsl:template match="person">`           | `@template(pattern="person")`              |
| `<xsl:apply-templates select="address"/>` | `apply_templates(select(node, "address"))` |
| `<xsl:value-of select="name"/>`           | `value_of(node, "name")`                   |
| `<xsl:copy-of select="."/>`               | `copy_of(node)`                            |
| `mode="summary"`                          | `mode="summary"`                           |
| Template priorities                       | `priority=N` parameter                     |

## Examples

See `examples.py` for comprehensive examples including:

- Basic person data transformation
- Hierarchical list processing
- Mode-based article rendering
- Priority-based template selection
- Complex nested transformations

## Testing

Run the test suite:

```bash
uv run pytest src/tdom_sphinx/txslt/txslt_test.py -v
```

The tests demonstrate all core functionality and provide examples of proper usage patterns.

## Integration with tdom-sphinx

TXSLT is designed to work seamlessly with the existing tdom-sphinx codebase, extending the component-based architecture
with powerful transformation capabilities for processing Sphinx documentation structures.