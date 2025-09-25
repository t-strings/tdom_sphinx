from pathlib import PurePath

from tdom import html

from tdom_sphinx import PathTo
from tdom_sphinx.components.navbar_brand_logo import NavbarBrandLogo
from tdom_sphinx.theme_config import NavbarBrandConfig


def NavbarBrand(*, pathto: PathTo, brand_config: NavbarBrandConfig):
    icons = [
        html(t"""\n
<a class="navbar-item is-hidden-desktop" href={link.href} target="_blank">
  <span class="icon" style={f"color: {link.color}"}>
    <i class={link.icon_class}></i>
  </span>
</a>  
            """)
        for link in brand_config.links
    ]

    return html(t"""\n
<div class="navbar-brand">
    <{NavbarBrandLogo} pathto={pathto} config={brand_config.logo} />
    {icons}

    <div id="navbarBurger" class="navbar-burger burger" data-target="navMenu">
        <span></span>
        <span></span>
        <span></span>
    </div>
</div>
        """)
