# Python DOM Testing Library Plan (tdom-based)

Based on my analysis of the DOM Testing Library JavaScript codebase, here's a plan for a simple Python port using
tdom.Node types:

## Core Architecture

The library would provide accessibility-focused query functions that work with tdom's `Node`, `Element`, `Text`, and
`Fragment` types. The main API would follow DOM Testing Library's philosophy: **"The more your tests resemble the way
your software is used, the more confidence they can give you."**

## Primary Query Methods

### 1. **By Role** (`get_by_role`, `query_by_role`, `find_by_role`)

- Query elements by ARIA role (button, textbox, heading, etc.)
- Support role attributes like `name`, `description`, `level` (for headings)
- Use Python's `aria-query` equivalent or custom role mapping
- Try to match the W3C specification on ARIA roles

### 2. **By Text** (`get_by_text`, `query_by_text`, `find_by_text`)

- Find elements containing specific text content
- Support exact/fuzzy matching with normalization options
- Handle text content extraction from tdom nodes
- Automatically call `.strip()` on string values

### 3. **By Label Text** (`get_by_label_text`, `query_by_label_text`)

- Find form controls by their associated label
- Support `<label>` elements and `aria-labelledby`
- Automatically call `.strip()` on string values

### 4. **By Placeholder** (`get_by_placeholder_text`)

- Query form inputs by placeholder attribute
- Automatically call `.strip()` on string values

### 5. **By Test ID** (`get_by_test_id`)

- Find elements by `data-testid` attribute
- Configurable test ID attribute name

## API Structure

```python
from tdom import Node, Element
from typing import Optional, Union, Callable, Pattern
from enum import Enum


class QueryVariant(Enum):
    GET = "get"  # Returns single element, throws if not found/multiple
    QUERY = "query"  # Returns single element or None
    FIND = "find"  # Async version with waiting
    GET_ALL = "get_all"  # Returns list, throws if empty
    QUERY_ALL = "query_all"  # Returns list (can be empty)
    FIND_ALL = "find_all"  # Async list version


# Core query functions
def get_by_role(container: Node, role: str, *, name: Optional[str] = None,
                level: Optional[int] = None, **kwargs) -> Element: ...


def query_by_text(container: Node, text: Union[str, Pattern], *,
                  exact: bool = True, normalize: bool = True) -> Optional[Element]: ...


# Convenience function that binds all queries to a container
def within(container: Node) -> QueryMethods: ...
```

## Implementation Priorities

### Phase 1: Core Infrastructure

1. **Text extraction** - Function to get text content from tdom nodes
2. **Attribute querying** - Generic attribute-based element finding
3. **Normalization** - Text matching with whitespace/case handling
4. **Error messages** - Helpful debugging when queries fail

### Phase 2: Essential Queries

1. **By Role** - Most important for accessibility testing
2. **By Text** - Universal content-based queries
3. **By Test ID** - Escape hatch for difficult cases

### Phase 3: Form-Specific Queries

1. **By Label Text** - Critical for form testing
2. **By Placeholder** - Input testing convenience
3. **By Display Value** - Current form field values

### Phase 4: Advanced Features

1. **Multiple element variants** (`get_all_by_*`)
2. **Waiting/async queries** (`find_by_*`)
3. **Custom matchers** - Regex and function-based matching
4. **Pretty printing** - Enhanced error messages with DOM context

## Key Design Decisions

1. **Pure Python** - No browser/DOM dependencies, works with tdom trees
2. **Type safety** - Full type hints using tdom's Node types
3. **Accessibility first** - Prioritize ARIA-aware queries over CSS selectors
4. **Simple API** - Follow DOM Testing Library conventions closely
5. **Configurable** - Allow customization of text normalization, test ID attributes
6. **Error-friendly** - Clear error messages suggesting alternative queries

This approach provides a lightweight, accessibility-focused testing library that integrates naturally with tdom's
component-based architecture while maintaining the proven patterns from the JavaScript ecosystem.