"""Pytest fixtures for tdom-sphinx testing.

This module contains reusable pytest fixtures that provide standardized
test data and configurations for the tdom-sphinx project.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator

import pytest
from sphinx.testing.util import SphinxTestApp

from tdom_sphinx.models import (
    IconLink,
    Link,
    NavbarConfig,
    PageContext,
    SiteConfig,
)

# ----- APP: Mimic how an app like Sphinx or Flask would do
# both a global registry and a per-request container.


@dataclass
class Greeting:
    salutation: str = "Hello"


@dataclass
class URL:
    path: str


# ----- SPHINX TESTING FIXTURES -----

_TESTS_ROOT = Path(__file__).resolve().parent.parent.parent / "tests"
_ROOTS_DIR = _TESTS_ROOT / "roots"


@pytest.fixture
def registry():
    _registry = {}
    # _registry.register_factory(Greeting, Greeting)
    return _registry


@pytest.fixture(scope="session")
def rootdir() -> Path:
    return _ROOTS_DIR


@pytest.fixture
def page_context() -> PageContext:
    """Typed PageContext for tests that require dataclass instance.

    Returns:
        A PageContext instance with test data including:
        - Simple HTML body content
        - Default page metadata
        - Standard Sphinx configuration
    """
    return PageContext(
        body="<p>Hello World</p>",
        css_files=(),
        display_toc=False,
        js_files=(),
        pagename="index",
        page_source_suffix=".rst",
        sourcename=None,
        templatename="page.html",
        title="My Test Page",
        toc=None,
    )


@pytest.fixture
def site_config() -> SiteConfig:
    """Site configuration fixture for testing.

    Returns:
        A SiteConfig instance with:
        - Test site title and root URL
        - Sample navigation links and buttons
        - GitHub icon link example
    """
    return SiteConfig(
        site_title="My Test Site",
        root_url="/",
        navbar=NavbarConfig(
            links=[
                Link(href="/docs.html", style="", text="Docs"),
                Link(href="/about.html", style="", text="About"),
            ],
            buttons=[
                IconLink(
                    href="https://github.com/org",
                    color="#000",
                    icon_class="fa fa-github",
                ),
            ],
        ),
    )


@pytest.fixture
def sphinx_app(site_config: SiteConfig) -> SphinxTestApp:
    """A Sphinx test application rooted at basic test project.

    Also attaches a default SiteConfig which some tests rely on.

    Args:
        site_config: The site configuration to attach to the app

    Returns:
        A configured SphinxTestApp instance with attached site_config
    """
    src_dir = Path(__file__).parent.parent.parent / "tests/roots/test-basic-sphinx"
    app = SphinxTestApp(srcdir=src_dir)
    # Attach a default SiteConfig used by the template bridge
    setattr(app, "site_config", site_config)
    return app


@pytest.fixture
def sphinx_context(sphinx_app: SphinxTestApp, page_context: PageContext) -> dict:
    """Combined Sphinx context dictionary for template testing.

    Args:
        sphinx_app: Configured Sphinx test application
        page_context: Page context with test data

    Returns:
        Dictionary containing combined Sphinx and page context data
    """
    return {
        "project": "My Test Site",
        "title": page_context.title,
        "body": page_context.body,
        "sphinx_app": sphinx_app,
        "page_context": page_context,
    }


@pytest.fixture()
def content(app: SphinxTestApp) -> Generator[SphinxTestApp, Any, None]:
    """The content generated from a Sphinx site.

    Args:
        app: Sphinx test application

    Yields:
        The built Sphinx application with generated content
    """
    app.build()
    yield app


@pytest.fixture()
def page(content: SphinxTestApp, request) -> Generator[str, Any, None]:
    """Get the text for a page.

    Args:
        content: Built Sphinx application
        request: Pytest request object containing page parameter

    Yields:
        The HTML content of the requested page
    """
    pagename = request.param
    yield (content.outdir / pagename).read_text()
