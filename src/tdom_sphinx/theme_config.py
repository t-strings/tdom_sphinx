from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass(frozen=True)
class LinkConfig:
    """Used in Footer"""

    href: str
    style: str
    text: str


@dataclass(frozen=True)
class IconLinkConfig:
    """Used in NavbarEnd"""

    href: str
    color: str
    icon_class: str


@dataclass(frozen=True)
class IconTextLinkConfig(IconLinkConfig):
    """Used in NavbarBrand"""

    a_class: str
    text: str
    alternate_text: Optional[str] = None  # For wide/small/display


@dataclass(frozen=True)
class IconSubtitleConfig(IconLinkConfig):
    """Used in NavbarStart More menu items, Footer Rich link"""

    text: str
    subtitle: Optional[str] = None


@dataclass(frozen=True)
class NavbarBrandLogoConfig:
    src: str
    height: int
    width: int
    alt: str = "Logo"


@dataclass(frozen=True)
class NavbarBrandConfig:
    logo: Optional[NavbarBrandLogoConfig] = None
    links: Sequence[IconLinkConfig] = tuple()


@dataclass(frozen=True)
class NavbarMoreConfig:
    href: Path  # noqa: F821
    links: Sequence[IconSubtitleConfig] = tuple()


@dataclass(frozen=True)
class NavbarStartConfig:
    links: Sequence[IconTextLinkConfig] = tuple()
