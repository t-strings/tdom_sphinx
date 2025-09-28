"""Sphinx event handlers for tdom_sphinx.

Separated from package __init__ to keep responsibilities clear and ease testing.
"""

from __future__ import annotations

from typing import Any

from markupsafe import Markup
from sphinx.application import Sphinx

from tdom_sphinx.models import PageContext, Rellink, SiteConfig
from tdom_sphinx.utils import html_string_to_tdom
from tdom import Node


def _parse_toc(toc_html: str | object | None) -> Node | None:
    """Parse toctree HTML into a tdom Node.

    Args:
        toc_html: HTML string from Sphinx's toc context, or other object

    Returns:
        Parsed tdom Node if toc_html is a non-empty string, None otherwise
    """
    if isinstance(toc_html, str) and toc_html.strip():
        return html_string_to_tdom(toc_html)
    return None


def make_page_context(
    context: dict[str, Any],
    pagename: str,
    templatename: str,
    toc_num_entries: dict[str, int],
    document_metadata: dict[str, object],
) -> PageContext:
    """Given some Sphinx context information, make a PageContext."""
    rellinks = tuple(
        Rellink(
            pagename=link[0],
            link_text=link[3],
            title=link[1],
            accesskey=link[2],
        )
        for link in context.get("rellinks", ())
    )

    display_toc = (
        toc_num_entries[pagename] > 1 if "pagename" in toc_num_entries else False
    )
    ccf = context.get("css_files")
    jcf = context.get("css_files")
    # TODO Convert these to Path
    css_files = tuple(ccf) if ccf else ()
    js_files = tuple(jcf) if jcf else ()
    page_context = PageContext(
        body=Markup(context.get("body", "")),
        css_files=css_files,
        display_toc=display_toc,
        js_files=js_files,
        meta=document_metadata,
        metatags=context.get("metatags", ""),
        next=context.get("next"),
        page_source_suffix=context.get("page_source_suffix", "html"),
        pagename=pagename,
        prev=context.get("prev"),
        sourcename=context.get("sourcename"),
        templatename=templatename,
        rellinks=rellinks,
        title=context.get("title", ""),
        toc=_parse_toc(context.get("toc")),
        toctree=context.get("toctree"),
    )
    return page_context


def _on_html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree,
) -> None:
    """Inject the Sphinx app and selected config into the page context.

    - Ensure ``context['sphinx_app']`` is available for the Template Bridge.
    - Build a normalized ``PageContext`` and attach it as ``context['page_context']``.
    """
    # For our Template Bridge
    context.setdefault("sphinx_app", app)

    # ---- Build and attach PageContext
    page_ctx = make_page_context(
        context=context,
        pagename=pagename,
        templatename=templatename,
        toc_num_entries=app.env.toc_num_entries,
        document_metadata=app.env.metadata[pagename],
    )
    context["page_context"] = page_ctx


def _on_builder_inited(app: Sphinx) -> None:
    """Create a SiteConfig once at builder init and attach to the app.

    We derive defaults from Sphinx config where not provided explicitly in
    conf.py's ``site_config`` value.
    """
    existing = getattr(app.config, "site_config", None)

    project = getattr(app.config, "project", None)
    html_baseurl = getattr(app.config, "html_baseurl", None)
    sphinx_copyright = getattr(app.config, "copyright", None)

    if isinstance(existing, SiteConfig):
        navbar = existing.navbar
        site_title = existing.site_title or project
        # existing.root_url is guaranteed to be a string; prefer it, else fall back to html_baseurl or "/"
        root_url = existing.root_url or (html_baseurl or "/")
        copyright = existing.copyright or sphinx_copyright
    else:
        navbar = None
        site_title = project
        root_url = html_baseurl or "/"
        copyright = sphinx_copyright

    # Store on the app for retrieval by the template bridge and others
    setattr(
        app,
        "site_config",
        SiteConfig(
            navbar=navbar, site_title=site_title, root_url=root_url, copyright=copyright
        ),
    )
