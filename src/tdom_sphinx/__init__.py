"""tdom Sphinx extension + theme registration + event handlers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sphinx.application import Sphinx

THEME_ROOT = Path(__file__).parent / "theme"

type PathTo = Callable[[str, int | None], str]


def _on_builder_inited(app: Sphinx) -> None:
    """Ensure our Template Bridge is used for HTML builds.

    This avoids the need to set ``template_bridge`` in conf.py for tests.
    """
    try:
        # Lazy import to avoid hard dependency at module import time
        from tdom_sphinx.template_bridge import TdomBridge
    except Exception:  # pragma: no cover - fallback if import fails
        return

    # If the builder exists (e.g., during HTML builds), swap the templates
    builder = getattr(app, "builder", None)
    if builder is not None:
        try:
            # BuiltinTemplateLoader expects the app instance
            builder.templates = TdomBridge(app)  # type: ignore[assignment]
        except Exception:
            # Don't break Sphinx build; just leave default bridge in place
            pass


def _on_html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree,
) -> None:
    """Inject the Sphinx app into the page context for the Template Bridge.

    Our bridge expects ``context['sphinx_app']`` to be available.
    """
    context.setdefault("sphinx_app", app)


def setup(app) -> dict[str, Any]:
    """Register the theme so html_theme = "tdom-theme" works and wire events.

    We don't rely on theme templates thanks to our TemplateBridge, but Sphinx
    requires the theme to be registered if configured.
    """
    if THEME_ROOT.exists():
        app.add_html_theme("tdom-theme", str(THEME_ROOT))

    app.config.template_bridge = "tdom_sphinx.template_bridge.TdomBridge"

    # Connect event handlers used by our custom Template Bridge and views
    app.connect("builder-inited", _on_builder_inited)
    app.connect("html-page-context", _on_html_page_context)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
