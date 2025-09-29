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

## Notes

- The theme’s CSS grid and PicoCSS aim for a clean, semantic layout; override by adding your own CSS if needed.
- Public API is intentionally small; most users only need the Sphinx config shown above.
