"""Minimal Sphinx configuration for basic theme testing."""

extensions = [
    "tdom_sphinx",
]

project = "tdom-sphinx"
html_theme = "tdom-theme"

# Optional registry for tdom
tdom_registry = {}

# Suppress warnings for testing
suppress_warnings = ["misc.highlighting_failure"]
