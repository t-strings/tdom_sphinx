from pathlib import Path
from typing import Optional

from tdom import html


def NavbarEndButton(
        href: Path,
        color: str,
        text: str,
        image: Optional[str] = None):
    if image:
        icon = html(t'''\n
<span class="icon">
    <i class={image}></i>
</span>
            ''')
    else:
        icon = False
    return html(t'''\n
<p class="control">
    <a
        class={f"button {color}"}
        href={href}
        target="_blank"
    >
        {icon if icon else ''}
        <strong>{text}</strong>
    </a>
</p>
''')
