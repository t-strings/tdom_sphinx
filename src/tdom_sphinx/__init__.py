"""tdom Sphinx extension + theme registration + event handlers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

# Import Sphinx event handlers from a dedicated module
from .sphinx_events import _on_html_page_context, _on_builder_inited

THEME_ROOT = Path(__file__).parent / "theme"

type PathTo = Callable[[str, int | None], str]


def setup(app) -> dict[str, Any]:
    """Register the theme so html_theme = "tdom-theme" works and wire events.

    We don't rely on theme templates thanks to our TemplateBridge, but Sphinx
    requires the theme to be registered if configured.
    """
    if THEME_ROOT.exists():
        app.add_html_theme("tdom-theme", str(THEME_ROOT))

    # Register our Template Bridge by default so tests don't need to set it
    app.config.template_bridge = "tdom_sphinx.template_bridge.TdomBridge"

    # Register optional config values we may surface in page context
    # `site_config` can be defined in conf.py (as a SiteConfig) and will be
    # passed through into the HTML page context by our event handler.
    app.add_config_value("site_config", None, "env")

    # Connect event handlers used by our custom Template Bridge and views
    app.connect("builder-inited", _on_builder_inited)
    app.connect("html-page-context", _on_html_page_context)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
