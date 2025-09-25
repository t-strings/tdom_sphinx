from pathlib import Path

from tdom import html


def NavbarEndIcon(href: Path, image: str, color: str):
    style = {"color": color}
    return html(t'''\n
<a class="bd-navbar-icon navbar-item" href={href} target="_blank">
    <span class="icon" style={style}>
        <i class={f"fa-lg {image}"}></i>
    </span>
</a>
        ''')
