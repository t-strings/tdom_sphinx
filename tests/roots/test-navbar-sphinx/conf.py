"""Sphinx test root that wires up the theme and sets a navbar with links/buttons."""

extensions = [
    "tdom_sphinx",
]

project = "tdom-sphinx"
html_theme = "tdom-theme"

# Optional registry for tdom
tdom_registry = {}

# Provide a site_config structure as required by our components
from tdom_sphinx.models import Link, IconLink, NavbarConfig, SiteConfig  # noqa: E402

site_config = SiteConfig(
    navbar=NavbarConfig(
        links=[
            Link(href="/docs.html", style="", text="Docs"),
            Link(href="/about.html", style="btn", text="About"),
        ],
        buttons=[
            IconLink(
                href="https://github.com/org", color="#000", icon_class="fa fa-github"
            ),
            IconLink(
                href="https://x.com/org", color="#08f", icon_class="fa fa-twitter"
            ),
        ],
    )
)

# Suppress warnings for testing
suppress_warnings = ["misc.highlighting_failure"]
