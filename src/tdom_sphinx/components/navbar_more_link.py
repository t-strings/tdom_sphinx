"""
Presentation component to format an entry in the More dropdown.
"""

from pathlib import Path, PurePath, PurePosixPath
from typing import Optional

from tdom import html

from goku.url import relative_path


def NavbarMoreLink(
        href: PurePosixPath,
        color: str,
        icon_class: str,
        text: str,
        current_path: PurePosixPath,
        subtitle: Optional[str] = None
):
    more_link = relative_path(current=current_path, target=href)
    return html(t'''\n
<a class="navbar-item" href={more_link}>
  <span>
    <span class="{f"icon has-text-{color}" }">
      <i class="{icon_class}"></i>
    </span>
    <strong>{text}</strong>
    <br/>
      {subtitle}
  </span>
</a>
<hr class="navbar-divider" />
            ''')
