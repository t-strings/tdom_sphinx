from pathlib import Path
from typing import Optional

from tdom import html


def NavbarStartLink(
        a_class: str,
        color: str,
        href: Path,
        icon_class: str,
        text: str,
        alternate_text: Optional[str] = None
):
    if alternate_text:
        label = html(t'''\n
<span class="is-hidden-touch is-hidden-widescreen">
  {alternate_text}
</span>
<span class="is-hidden-desktop-only">
  {text}
</span>
''')
    else:
        label = html(t'<span>{text}</span>')
    return html(t'''\n
<a class={f"navbar-item bd-navbar-item-{a_class}"}
   href={href}>
    <span class={f"icon has-text-{color}"}>
      <i class={icon_class}></i>
    </span>
    {label}
</a>
''')
