# ----- APP: Mimic how an app like Sphinx or Flask would do
# both a global registry and a per-request container.

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp

from tdom_sphinx.models import (
    IconLink,
    Link,
    NavbarConfig,
    PageContext,
    SiteConfig,
)

pytest_plugins = ("sphinx.testing.fixtures",)


@dataclass
class Greeting:
    salutation: str = "Hello"


@dataclass
class URL:
    path: str


@pytest.fixture
def registry():
    _registry = {}
    # _registry.register_factory(Greeting, Greeting)
    return _registry


# ----- SPHINX TESTING FIXTURES -----

_TESTS_ROOT = Path(__file__).resolve().parent / "tests"
_ROOTS_DIR = _TESTS_ROOT / "roots"


@pytest.fixture(scope="session")
def rootdir() -> Path:
    return _ROOTS_DIR


@pytest.fixture()
def content(app: SphinxTestApp) -> Generator[SphinxTestApp, Any, None]:
    """The content generated from a Sphinx site."""
    app.build()
    yield app


@pytest.fixture()
def page(content: SphinxTestApp, request) -> Generator[str, Any, None]:
    """Get the text for a page."""
    pagename = request.param
    yield (content.outdir / pagename).read_text()


@pytest.fixture()
def soup(page: str) -> Generator[BeautifulSoup, Any, None]:
    """Get the text for a page and convert to BeautifulSoup document."""
    yield BeautifulSoup(page, "html.parser")


def pathto(filename: str, flag: int = 0) -> str:
    return filename


@pytest.fixture
def sphinx_app() -> SphinxTestApp:
    """A Sphinx test application rooted at basic test project.

    Also attaches a default SiteConfig which some tests rely on.
    """
    src_dir = Path(__file__).parent / "tests/roots/test-basic-sphinx"
    app = SphinxTestApp(srcdir=src_dir)
    # Attach a default SiteConfig used by the template bridge
    setattr(app, "site_config", SiteConfig(site_title="My Test Site"))
    return app


@pytest.fixture
def page_context() -> PageContext:
    """Typed PageContext for tests that require dataclass instance."""
    return PageContext(
        body="<p>Hello World</p>",
        css_files=(),
        display_toc=False,
        js_files=(),
        pagename="index",
        page_source_suffix=".rst",
        pathto=pathto,
        sourcename=None,
        templatename="page.html",
        title="My Test Page",
        toc="",
    )


@pytest.fixture
def site_config() -> SiteConfig:
    return SiteConfig(
        site_title="My Test Site",
        root_url="/",
        navbar=NavbarConfig(
            links=[
                Link(href="/docs", style="", text="Docs"),
                Link(href="/about", style="", text="About"),
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
def sphinx_context(sphinx_app: SphinxTestApp, page_context: PageContext) -> dict:
    return {
        "project": "My Test Site",
        "title": page_context.title,
        "body": page_context.body,
        "sphinx_app": sphinx_app,
        "pathto": pathto,
        "page_context": page_context,
    }
