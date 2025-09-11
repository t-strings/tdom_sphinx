"""Minimal Sphinx configuration for basic theme testing."""

extensions = [
    "tdom_sphinx",
]

html_theme = "tdom-theme"
html_title = "Test tdom Theme"

# Optional registry for tdom
tdom_registry = {}

# Suppress warnings for testing
suppress_warnings = ["misc.highlighting_failure"]
