from pathlib import PurePosixPath

from tdom import html

from goku.components.navbar.more import NavbarMore, NavbarMoreConfig
from goku.components.navbar.start.config import NavbarStartConfig
from goku.components.navbar.start.navbar_start_link import NavbarStartLink
from goku.url import relative_path


def NavbarStart(config: NavbarStartConfig, current_path: PurePosixPath, more_config: NavbarMoreConfig):
    links = [
        html(t'<{NavbarStartLink} a_class={link.a_class} color={link.color} href={relative_path(current_path, link.href)} icon_class={link.icon_class} text={link.text} alternate_text={link.alternate_text} />')
        for link in config.links
    ]

    return html(t'''\n
        <div class="navbar-end">
            {links}
            {t'{NavbarMore} config={more_config} current_path={current_path} />' if more_config else ''}
        </div>
        ''')
