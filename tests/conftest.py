# ----- APP: Mimic how an app like Sphinx or Flask would do
# both a global registry and a per-request container.

from dataclasses import dataclass

from pathlib import Path
from typing import Any, Generator

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp

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

_TESTS_ROOT = Path(__file__).resolve().parent
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
