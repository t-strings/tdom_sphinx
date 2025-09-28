from dataclasses import dataclass
from typing import Callable, Iterable, List, Protocol


class _FunctionView(Protocol):
    def __call__(self, context: dict) -> str: ...


class _ClassView(Protocol):
    def __init__(self, context: dict): ...

    def render(self) -> str: ...


View = _FunctionView | _ClassView


@dataclass(frozen=True)
class Rellink:
    """A Sphinx rellink."""

    pagename: str
    link_text: str
    title: str | None = None
    accesskey: str | None = None


@dataclass(frozen=True)
class PageContext:
    """Per-page info from the underlying system needed by layout."""

    body: object
    css_files: Iterable
    display_toc: bool
    js_files: Iterable
    pagename: str
    page_source_suffix: str
    pathto: Callable[
        [
            str,
        ],
        str,
    ]
    sourcename: str | None
    templatename: str
    title: str
    toc: object
    builder: str = "html"
    meta: object = None
    metatags: str = ""
    next: object | None = None
    parents: object = None
    prev: object | None = None
    rellinks: object = None
    toctree: object | None = None


@dataclass(frozen=True)
class Link:
    href: str
    style: str
    text: str


@dataclass(frozen=True)
class IconLink:
    href: str
    color: str
    icon_class: str


@dataclass(frozen=True)
class NavbarConfig:
    links: List[Link]
    buttons: List[IconLink]


# --- Site-level configuration models


@dataclass(frozen=True)
class SiteConfig:
    navbar: NavbarConfig | None = None
    site_title: str | None = None
    root_url: str = "/"
    copyright: str | None = None
    make_relative: bool = True
