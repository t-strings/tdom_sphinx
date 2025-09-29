# tdom-sphinx

A Sphinx extension and theme that renders pages with tdom components instead of Jinja templates. It ships a minimal, semantic HTML theme styled with PicoCSS and Sphinx defaults, plus a small set of composable page components.

- PicoCSS with CSS Grid
- ThemeConfig, SiteConfig, and PageContext
- Focus on component-driven development
  - Symbols, not files/strings (e.g. navigation, refactoring, autocomplete)
- Views
- Look in tests/roots for examples
- htpy component and decorator example
- txslt
- aria_testing
- Relative URL rewriting
- Re-parsed Sphinx toctree
- Hint at component replaceability

## Features

- Sphinx theme: set `html_theme = "tdom-theme"` to use the bundled theme.
- tdom-powered rendering: replaces Sphinx’s Jinja pipeline via a custom Template Bridge so pages are rendered by Python components (no Jinja files).
- Semantic layout components:
  - BaseLayout builds a full HTML5 page with `<head>`, header, aside, main, and footer.
  - Head sets the `<title>`, favicon, and includes CSS (tdom-sphinx.css, PicoCSS, Sphinx, Pygments).
  - Heading, SiteAside, Main, Footer components compose the page shell.
- Correct static asset paths: stylesheet and favicon links are rewritten relative to the current page depth (e.g. `_static/...` vs `../../../_static/...`).
- MyST/Markdown friendly: docs are authored in Markdown via `myst_parser`.
- Works as both a theme and an extension: add `"tdom_sphinx"` to `extensions` to enable the Template Bridge automatically.
- Python 3.14+ only (matches this project’s `requires-python`).
- Utilities for interop: optional `htpy_component` decorator converts htpy components to tdom nodes for use inside t-strings.

## Quickstart

1) Install (uv is recommended):

```bash
uv sync
```

2) Enable in `docs/conf.py`:

```python
extensions = [
    "myst_parser",   # Markdown
    "tdom_sphinx",   # enable tdom-based rendering
]
html_theme = "tdom-theme"
```

3) Build your docs:

```bash
uv run sphinx-build -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` in your browser.

## Live-reloading the docs

Use sphinx-autobuild for a local server that rebuilds on changes to the docs/ directory.

```bash
uv sync --group dev
uv run docs-autobuild
```

This serves your documentation with live reload (by default at http://127.0.0.1:8000) and writes the built HTML to `docs/_build/html`.

## Examples and references

- Minimal example in `docs/` (Markdown via MyST) with a toctree entry.
- More component usage in tests under `tests/` and `src/tdom_sphinx/components/`.

## aria_testing - DOM Testing Library for Python

This project includes `aria_testing`, a Python implementation of DOM Testing Library patterns for testing tdom components and HTML structures. It provides accessibility-focused queries that work with tdom's Element, Fragment, and Node types.

### Key Features

- **Role-based queries**: Find elements by their ARIA roles (button, link, heading, etc.)
- **Name filtering**: Filter elements by their accessible names using keyword arguments
- **Clean keyword API**: Use `*` separator for keyword-only arguments following Python best practices
- **Accessible name computation**: Automatically computes accessible names from aria-label, text content, alt text, href, etc.
- **Enhanced link matching**: For links, combines both text content and href attribute for comprehensive name matching

### Usage Examples

#### Basic Role Queries

```python
from tdom import html
from tdom_sphinx.aria_testing import get_by_role, get_all_by_role

# Find elements by role
document = html(t"<div><button>Save</button><button>Cancel</button></div>")
button = get_by_role(document, "button")  # Gets first button
all_buttons = get_all_by_role(document, "button")  # Gets both buttons
```

#### Name Filtering with Keyword Arguments

```python
import re

# Filter by accessible name using keyword-only arguments
container = html(t"""<div>
    <button>Save Document</button>
    <button>Cancel Operation</button>
    <button aria-label="Delete file">🗑️</button>
</div>""")

# Find button containing "Save" in its name (string matching)
save_btn = get_by_role(container, "button", name="Save")

# Find button with aria-label containing "Delete"
delete_btn = get_by_role(container, "button", name="Delete")

# Find heading with specific level
heading = get_by_role(container, "heading", level=2)

# Use regex for case-insensitive matching
cancel_btn = get_by_role(container, "button", name=re.compile(r"cancel", re.IGNORECASE))
```

#### Enhanced Link Name Matching

```python
# Links combine text content AND href for name matching
container = html(t"""<div>
    <a href="/docs">Documentation</a>
    <a href="/api">API Reference</a>
    <a href="/docs/guide">Guide</a>
</div>""")

# Match by text content
docs_link = get_by_role(container, "link", name="Documentation")

# Match by href attribute
api_link = get_by_role(container, "link", name="/api")

# Match by part of href path
guide_link = get_by_role(container, "link", name="guide")
```

#### Accessible Name Sources

The library computes accessible names from multiple sources in priority order:

1. **aria-label** attribute (highest priority)
2. **aria-labelledby** referenced elements
3. **Role-specific sources**:
   - **Links**: Text content combined with href attribute
   - **Buttons**: Text content
   - **Images**: alt attribute, then title
   - **Form controls**: value, placeholder, then text content
4. **Text content** (fallback)
5. **title** attribute (lowest priority)

```python
# Examples of name computation
container = html(t"""<div>
    <button aria-label="Custom Label">Visible Text</button>
    <a href="/docs">Documentation</a>
    <a href="/api">API</a>
    <img src="logo.png" alt="Company Logo" />
    <input type="text" placeholder="Enter name" />
</div>""")

# Matches aria-label, not visible text
btn = get_by_role(container, "button", name="Custom")

# For links, matches BOTH text content AND href
link = get_by_role(container, "link", name="Documentation")  # matches text
api_link = get_by_role(container, "link", name="/api")       # matches href

# Matches alt text for images
img = get_by_role(container, "img", name="Logo")

# Matches placeholder for inputs
input_elem = get_by_role(container, "textbox", name="Enter")
```

#### Regex Pattern Matching

```python
import re

# Advanced regex patterns for name matching
container = html(t"""<div>
    <button>save file</button>
    <button>SAVE DOCUMENT</button>
    <button>Delete Item</button>
    <a href="/api/v1">API Version 1</a>
    <a href="/api/v2">API Version 2</a>
</div>""")

# Case-insensitive matching for "save" buttons
save_buttons = get_all_by_role(container, "button", name=re.compile(r"save", re.IGNORECASE))
assert len(save_buttons) == 2  # Matches both "save file" and "SAVE DOCUMENT"

# Match all-uppercase text only
caps_button = get_by_role(container, "button", name=re.compile(r"^[A-Z\s]+$"))
# Finds "SAVE DOCUMENT"

# Match API version links using href patterns
api_links = get_all_by_role(container, "link", name=re.compile(r"/api/v\d+"))
assert len(api_links) == 2  # Matches both v1 and v2

# Exact word boundary matching
exact_save = get_by_role(container, "button", name=re.compile(r"^save file$"))
```

### Available Query Functions

- `get_by_role()` - Find single element, throw if not found or multiple found
- `query_by_role()` - Find single element, return None if not found
- `get_all_by_role()` - Find all elements, throw if none found
- `query_all_by_role()` - Find all elements, return empty list if none found

All functions use keyword-only arguments with the `*` separator, supporting `name` and `level` parameters. The `name` parameter accepts both strings (substring matching) and compiled regex patterns for advanced matching.

## Notes

- The theme's CSS grid and PicoCSS aim for a clean, semantic layout; override by adding your own CSS if needed.
- Public API is intentionally small; most users only need the Sphinx config shown above.
- Use aria_testing for component testing - it encourages accessible HTML and follows DOM Testing Library best practices.
