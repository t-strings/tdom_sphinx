from pathlib import PurePath

from tdom import html

from goku.components.navbar.brand import NavbarBrand, NavbarBrandConfig
from goku.components.navbar.end import NavbarEnd, NavbarEndConfig
from goku.components.navbar.more import NavbarMoreConfig
from goku.components.navbar.start import NavbarStart, NavbarStartConfig


def Navbar(brand_config: NavbarBrandConfig, root_path: PurePath,
           start_config: NavbarStartConfig, current_path: PurePath,
           more_config: NavbarMoreConfig, end_config: NavbarEndConfig | None,
           ):
    return html(t'''\n
        <nav id="navbar" class="bd-navbar navbar has-shadow is-spaced">
            <div class="container">
                <{NavbarBrand} config={brand_config} root_path={root_path}/>

                <div id="navMenu" class="navbar-menu">
                    <{NavbarStart} config={start_config} current_path={current_path} more_config={more_config} />
                    {html(t'<{NavbarEnd} config={end_config}/>') if end_config else "" }
                </div>
            </div>
        </nav>
        ''')
