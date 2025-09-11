"""Custom Template Bridge that renders pages using tdom views/layouts."""

from sphinx.jinja2glue import BuiltinTemplateLoader

from tdom_sphinx.models import TdomContext
from tdom_sphinx.views import DefaultView


class TdomBridge(BuiltinTemplateLoader):
    """Replace the built-in Sphinx-Jinja rendering with tdom rendering.

    If anything goes wrong, falls back to the default BuiltinTemplateLoader.
    """

    def render(self, template, context: dict) -> str:
        # Expect the builder-init event to put Sphinx app into context
        sphinx_app = context.get("sphinx_app")
        tdom_context = TdomContext(
            app=sphinx_app,
            environment=sphinx_app.env,
            config=sphinx_app.config,
            page_context=context,
        )
        view = DefaultView(context=tdom_context)
        result = view()
        return str(result)
