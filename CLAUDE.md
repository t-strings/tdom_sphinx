# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup

```bash
uv sync --group dev  # Install all dependencies including dev group
```

### Testing

```bash
uv run pytest                    # Run all tests
uv run pytest src/              # Run component tests only
uv run pytest tests/            # Run integration tests only
uv run pytest -k test_name      # Run specific test
```

### Type Checking

```bash
uv run pyright                   # Type check the entire codebase
```

### Documentation

```bash
uv run docs-autobuild            # Live-reload docs server at http://127.0.0.1:8000
uv run sphinx-build -b html docs docs/_build/html  # Build docs once
```

## Architecture Overview

This project implements a Sphinx theme using `tdom` (template DOM) instead of traditional Jinja templates. The core
architecture replaces Sphinx's template rendering with a component-based approach.

### Key Components

**Template Bridge (`template_bridge.py`)**

- `TdomBridge` replaces Sphinx's `BuiltinTemplateLoader`
- Renders pages using tdom views instead of Jinja templates
- Falls back to default behavior if tdom rendering fails

**Sphinx Events (`sphinx_events.py`)**

- `_on_builder_inited`: Creates `SiteConfig` from Sphinx config at build time
- `_on_html_page_context`: Injects Sphinx app and builds normalized `PageContext`
- `make_page_context`: Converts raw Sphinx context to typed `PageContext` dataclass

**Models (`models.py`)**

- `PageContext`: Typed representation of per-page Sphinx data
- `SiteConfig`: Site-wide configuration (navbar, title, etc.)
- `Link`, `IconLink`, `NavbarConfig`: Navigation components

**Views (`views.py`)**

- `DefaultView`: Main page orchestrator that uses `BaseLayout`
- Takes `PageContext` and `SiteConfig`, returns rendered tdom `Node`

**Components (`components/`)**

- `BaseLayout`: Main HTML5 document shell using `Head`, `Header`, `Main`, `Footer`
- Individual components: `Head`, `Header`, `Main`, `Footer`, `NavbarBrand`, etc.
- Each component is a function returning a tdom `Node`
- Components use tdom's `t"""` template string syntax

**URL Management (`url.py`)**

- `relative_tree()`: Rewrites absolute URLs to relative paths in rendered HTML
- `relative()`: Calculates relative paths between pages
- Handles complex path resolution for multi-level site structures

### Component Architecture

Components follow a functional pattern:

```python
def ComponentName(*, page_context: PageContext, site_config: SiteConfig | None = None) -> Node:
    return html(t"""<div>...</div>""")
```

Components are composed hierarchically:

- `BaseLayout` → `Head` + `Header` + `Main` + `Footer`
- `Header` → `NavbarBrand` + `NavbarLinks`

### Testing Strategy

**Component Tests**: Each component has a `*_test.py` file testing isolated functionality.

**Functionality tests**. Anything that is not a component goes under `tests` using the normal pytest naming strategy
prefix of `test_`. Always use pytest function tests, not class-based tests.

**Integration Tests**: Use Sphinx's testing framework with test projects in `tests/roots/`:

- `test-basic-sphinx/`: Minimal Sphinx project for basic functionality
- `test-navbar-sphinx/`: Tests navigation features

**Fixtures (`conftest.py`)**:

- `sphinx_app`: Preconfigured SphinxTestApp with SiteConfig
- `page_context`: Typed PageContext for component testing
- `site_config`: Default SiteConfig with sample navigation
- `content`: Built Sphinx app for integration testing
- `soup`: BeautifulSoup parsing of rendered HTML

### Development Notes

- This project uses Python 3.14+ and `uv` for dependency management
- Components use tdom's template string syntax (`t"""..."""`) for HTML
- The `tdom` dependency is installed as an editable local package (`../tdom`)
- URL rewriting happens after initial rendering via `relative_tree()`
- The theme integrates with Sphinx via extension registration in `__init__.py`
- Run `pytest` and `pyright` after making changes to ensure nothing breaks.
- Run `ruff` to format code after changes.

### t-strings and tdom Guidelines

**t-strings**:

- t-string means template string (PEP 750 feature in Python 3.14)
- A "template function" receives `string.templatelib.Template` and returns a string
- Templates are iterables of "parts" (strings or `string.templatelib.Interpolation`)
- Use structural pattern matching when analyzing template parts
- Always use type hints on function arguments and return values

**tdom Components**:

- Components go in `components/` directory with snake_case filenames
- Component function signatures always start with `*` to force named arguments
- Component tests go in same directory with `_test.py` suffix
- Component tests should use t-strings to generate results, then create `soup` variable with BeautifulSoup
- Look in `../tdom/docs/examples/components` for component style examples

**Code Quality**:

- Use ruff for linting and run after completing tasks
- Optimize imports and remove unused imports after changes
- Keep public API minimal and documented
- Prefer small, pure functions; avoid side effects except where needed
- Performance matters: avoid per-render allocations in hot paths
- Use type hints and run `pyright` when finishing tasks

### BeautifulSoup

- Try to get type safety on assertions
- Whenever you do a selection with `.select_one` or `.select`, first assign the result to `element: Tag | None` where
  `Tag` is imported from BeautifulSoup.
- Then, do an `assert element is not None`
- When trying to get at the text of an element, do `element.get_text(strip=True)`
