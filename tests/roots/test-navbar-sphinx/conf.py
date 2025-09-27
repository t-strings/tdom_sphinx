"""Sphinx test root that wires up the theme and sets a navbar with links/buttons."""

extensions = [
    "tdom_sphinx",
]

project = "tdom-sphinx"
html_theme = "tdom-theme"

# Optional registry for tdom
tdom_registry = {}

# Provide a navbar structure as required by our components
from tdom_sphinx.models import Link, IconLink  # noqa: E402

navbar = {
    "links": [
        Link(href="/docs", style="", text="Docs"),
        Link(href="/about", style="btn", text="About"),
    ],
    "buttons": [
        IconLink(href="https://github.com/org", color="#000", icon_class="fa fa-github"),
        IconLink(href="https://x.com/org", color="#08f", icon_class="fa fa-twitter"),
    ],
}

# Suppress warnings for testing
suppress_warnings = ["misc.highlighting_failure"]
