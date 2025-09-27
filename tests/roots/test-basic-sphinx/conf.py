"""Minimal Sphinx configuration for basic theme testing."""

extensions = [
    "tdom_sphinx",
]

project = "tdom-sphinx"
html_theme = "tdom-theme"

# Optional registry for tdom
tdom_registry = {}

# Example navbar config to be surfaced into html-page-context
navbar = {
    "links": [],
    "buttons": [],
}

# Suppress warnings for testing
suppress_warnings = ["misc.highlighting_failure"]
