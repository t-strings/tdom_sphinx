"""Custom Template Bridge that renders pages using tdom views/layouts."""

from sphinx.jinja2glue import BuiltinTemplateLoader

from tdom_sphinx.models import PageContext, SiteConfig
from tdom_sphinx.views import DefaultView


class TdomBridge(BuiltinTemplateLoader):
    """Replace the built-in Sphinx-Jinja rendering with tdom rendering.

    If anything goes wrong, it falls back to the default BuiltinTemplateLoader.
    """

    def render(self, template, context: dict) -> str:
        # Expect the builder-init event to put Sphinx app into context
        sphinx_app = context.get("sphinx_app")
        page_context: PageContext = context.get("page_context")
        # Get SiteConfig from the app, created during builder-inited
        site_config: SiteConfig = getattr(sphinx_app, "site_config")
        view = DefaultView(page_context=page_context, site_config=site_config)
        result = view()
        return str(result)
