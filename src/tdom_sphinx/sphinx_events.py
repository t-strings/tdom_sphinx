"""Sphinx event handlers for tdom_sphinx.

Separated from package __init__ to keep responsibilities clear and ease testing.
"""
from __future__ import annotations

from typing import Any

from sphinx.application import Sphinx


def _on_builder_inited(app: Sphinx) -> None:
    """Ensure our Template Bridge is used for HTML builds.

    This avoids the need to set ``template_bridge`` in conf.py for tests.
    """
    try:
        # Lazy import to avoid hard dependency at module import time
        from tdom_sphinx.template_bridge import TdomBridge
    except ImportError:  # pragma: no cover - fallback if import fails
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
    """Inject the Sphinx app and selected config into the page context.

    - Ensure ``context['sphinx_app']`` is available for the Template Bridge.
    - If ``navbar`` is defined in ``conf.py`` raw config, expose it in context.
    """
    # For our Template Bridge
    context.setdefault("sphinx_app", app)

    # Surface optional navbar configuration from conf.py (raw config)
    try:
        raw_config: dict[str, Any] = getattr(app.config, "_raw_config", {})
        navbar = raw_config.get("navbar")
    except Exception:
        navbar = None

    if navbar is not None:
        context["navbar"] = navbar
