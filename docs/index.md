---
title: tdom-sphinx
---

# tdom-sphinx

Welcome to the documentation for tdom-sphinx, a Sphinx extension and theme that
integrates the tdom rendering approach with Sphinx.

This documentation is written in Markdown using the MyST parser.

## Getting started

- Theme: `html_theme = "tdom-theme"`
- Extension: add `"tdom_sphinx"` to `extensions`
- Markdown support: add `"myst_parser"` to `extensions`

```python
# docs/conf.py (snippet)
extensions = [
    "myst_parser",
    "tdom_sphinx",
]
html_theme = "tdom-theme"
```

## Building the docs locally

- Ensure you have uv installed
- Create a dev environment and install dev deps
- Run Sphinx

```bash
uv sync --group dev
uv run sphinx-build -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` in your browser.
