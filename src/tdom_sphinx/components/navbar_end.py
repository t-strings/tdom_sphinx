"""
Navbar items in the NavbarEnd component.
"""

from tdom import html

from goku.components.navbar.end.button import NavbarEndButton
from goku.components.navbar.end.config import NavbarEndConfig
from goku.components.navbar.end.icon import NavbarEndIcon


def NavbarEnd(config: NavbarEndConfig):
    rendered_icons = [
        html(t'<{NavbarEndIcon} href={icn.href} image={icn.image} color={icn.color}/>')
        for icn in config.icons
    ]

    rendered_buttons = [
        html(t'<{NavbarEndButton} href={btn.href} image={btn.image} color={btn.color} text={btn.text}/>')
        for btn in config.buttons
    ]

    return html(t'''\n
<div class="navbar-start">
    {rendered_icons}
    <div class="navbar-item">
        <div class="field is-grouped is-grouped-multiline">
            {rendered_buttons}
        </div>
    </div>
</div>    
''')
