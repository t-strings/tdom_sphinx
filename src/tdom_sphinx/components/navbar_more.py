"""
Presentation component to format an entry in the More dropdown.
"""

from pathlib import PurePath

from tdom import html

from goku.components.navbar.more.config import NavbarMoreConfig
from goku.components.navbar.more.navbar_more_link import NavbarMoreLink


def NavbarMore(config: NavbarMoreConfig, current_path: PurePath):
    links = [
        html(t'''\n
<{NavbarMoreLink}  href={link.href} current_path={current_path} color={link.color} icon_class={link.icon_class} text={link.text} subtitle={link.subtitle} />
            ''')
        for link in config.links
    ]
    return html(t'''\n
        <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link" href={config.href}>
                More
            </a>

            <div id="moreDropdown" class="navbar-dropdown">
                {links}
            </div>
        </div>
            ''')