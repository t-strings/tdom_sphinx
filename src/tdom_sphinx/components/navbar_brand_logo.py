from tdom import html

from tdom_sphinx import PathTo
from tdom_sphinx.theme_config import NavbarBrandLogoConfig


def NavbarBrandLogo(
    *,
    pathto: PathTo,
    config: NavbarBrandLogoConfig,
):
    return html(t"""\n
<a class="navbar-item" href={pathto("/", 0)}>
    <img src={pathto(config.src, 1)} alt={config.alt} width={config.width} height={config.height} />
</a>        
""")
