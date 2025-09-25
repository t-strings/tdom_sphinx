from dataclasses import dataclass
from typing import Optional, Sequence


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
