# tdom-sphinx

A Sphinx theme, based on PicoCSS for semantic HTML, implemented with `tdom` instead of Jinja.

- How it works
- How to install
- Look in tests/roots for examples
- htpy component and decorator example

## Live-reloading the docs

Use sphinx-autobuild for a local server that rebuilds on changes to the docs/ directory.

```bash
uv sync --group dev
uv run docs-autobuild
```

This serves your documentation with live reload (by default at http://127.0.0.1:8000) and writes the built HTML to docs/_build/html.
