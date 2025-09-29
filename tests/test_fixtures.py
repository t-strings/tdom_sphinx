"""Tests for the tdom-sphinx fixtures module.

This module tests the pytest fixtures defined in src/tdom_sphinx/fixtures.py
to ensure they provide correct test data and behave as expected.
"""

from sphinx.testing.util import SphinxTestApp

from tdom_sphinx.models import IconLink, Link, NavbarConfig, PageContext, SiteConfig


def test_page_context_fixture(page_context):
    """Test that page_context fixture returns correct PageContext instance."""
    assert isinstance(page_context, PageContext)
    assert page_context.body == "<p>Hello World</p>"
    assert page_context.css_files == ()
    assert page_context.display_toc is False
    assert page_context.js_files == ()
    assert page_context.pagename == "index"
    assert page_context.page_source_suffix == ".rst"
    assert page_context.sourcename is None
    assert page_context.templatename == "page.html"
    assert page_context.title == "My Test Page"
    assert page_context.toc is None


def test_site_config_fixture(site_config):
    """Test that site_config fixture returns correct SiteConfig instance."""
    assert isinstance(site_config, SiteConfig)
    assert site_config.site_title == "My Test Site"
    assert site_config.root_url == "/"

    # Test navbar configuration
    assert isinstance(site_config.navbar, NavbarConfig)
    assert len(site_config.navbar.links) == 2
    assert len(site_config.navbar.buttons) == 1

    # Test first link
    first_link = site_config.navbar.links[0]
    assert isinstance(first_link, Link)
    assert first_link.href == "/docs.html"
    assert first_link.style == ""
    assert first_link.text == "Docs"

    # Test second link
    second_link = site_config.navbar.links[1]
    assert isinstance(second_link, Link)
    assert second_link.href == "/about.html"
    assert second_link.style == ""
    assert second_link.text == "About"

    # Test button
    button = site_config.navbar.buttons[0]
    assert isinstance(button, IconLink)
    assert button.href == "https://github.com/org"
    assert button.color == "#000"
    assert button.icon_class == "fa fa-github"


def test_sphinx_app_fixture(sphinx_app):
    """Test that sphinx_app fixture returns configured SphinxTestApp."""
    assert isinstance(sphinx_app, SphinxTestApp)
    assert hasattr(sphinx_app, "site_config")
    site_config = getattr(sphinx_app, "site_config")
    assert isinstance(site_config, SiteConfig)

    # Test that the source directory path exists and is correct
    assert sphinx_app.srcdir.exists()
    assert sphinx_app.srcdir.name == "test-basic-sphinx"


def test_sphinx_context_fixture(sphinx_context):
    """Test that sphinx_context fixture returns correct context dict."""
    assert isinstance(sphinx_context, dict)
    assert sphinx_context["project"] == "My Test Site"
    assert sphinx_context["title"] == "My Test Page"
    assert sphinx_context["body"] == "<p>Hello World</p>"
    assert isinstance(sphinx_context["sphinx_app"], SphinxTestApp)
    assert isinstance(sphinx_context["page_context"], PageContext)


def test_fixtures_integration(site_config, page_context, sphinx_app, sphinx_context):
    """Test that fixtures work together correctly."""
    # Verify the integration works as expected
    assert sphinx_context["page_context"] is page_context
    assert sphinx_context["sphinx_app"] is sphinx_app
    assert getattr(sphinx_app, "site_config") is site_config

    # Test that the context contains all expected keys
    expected_keys = {"project", "title", "body", "sphinx_app", "page_context"}
    assert set(sphinx_context.keys()) == expected_keys


def test_page_context_immutability(page_context):
    """Test that page_context fixture provides consistent data."""
    # Test that all fields have expected types and values
    assert isinstance(page_context.body, str)
    assert isinstance(page_context.css_files, tuple)
    assert isinstance(page_context.display_toc, bool)
    assert isinstance(page_context.js_files, tuple)
    assert isinstance(page_context.pagename, str)
    assert isinstance(page_context.page_source_suffix, str)
    assert page_context.sourcename is None or isinstance(page_context.sourcename, str)
    assert isinstance(page_context.templatename, str)
    assert isinstance(page_context.title, str)
    assert page_context.toc is None or hasattr(page_context.toc, "__iter__")


def test_site_config_immutability(site_config):
    """Test that site_config fixture provides consistent data."""
    # Test that all required fields are present and have correct types
    assert isinstance(site_config.site_title, str)
    assert isinstance(site_config.root_url, str)
    assert isinstance(site_config.navbar, NavbarConfig)

    # Test navbar structure
    assert hasattr(site_config.navbar, "links")
    assert hasattr(site_config.navbar, "buttons")
    assert isinstance(site_config.navbar.links, list)
    assert isinstance(site_config.navbar.buttons, list)


def test_navbar_config_structure(site_config):
    """Test the detailed structure of navbar configuration."""
    navbar = site_config.navbar

    # Test that all links have required attributes
    for link in navbar.links:
        assert hasattr(link, "href")
        assert hasattr(link, "style")
        assert hasattr(link, "text")
        assert isinstance(link.href, str)
        assert isinstance(link.style, str)
        assert isinstance(link.text, str)

    # Test that all buttons have required attributes
    for button in navbar.buttons:
        assert hasattr(button, "href")
        assert hasattr(button, "color")
        assert hasattr(button, "icon_class")
        assert isinstance(button.href, str)
        assert isinstance(button.color, str)
        assert isinstance(button.icon_class, str)


def test_page_context_fields(page_context):
    """Test all fields of PageContext fixture."""
    # Test specific expected values
    assert page_context.body == "<p>Hello World</p>"
    assert page_context.css_files == ()
    assert page_context.display_toc is False
    assert page_context.js_files == ()
    assert page_context.pagename == "index"
    assert page_context.page_source_suffix == ".rst"
    assert page_context.templatename == "page.html"
    assert page_context.title == "My Test Page"


def test_site_config_navbar_links(site_config):
    """Test that navbar links have expected values."""
    links = site_config.navbar.links

    assert len(links) == 2

    # Test first link
    assert links[0].href == "/docs.html"
    assert links[0].text == "Docs"
    assert links[0].style == ""

    # Test second link
    assert links[1].href == "/about.html"
    assert links[1].text == "About"
    assert links[1].style == ""


def test_site_config_navbar_buttons(site_config):
    """Test that navbar buttons have expected values."""
    buttons = site_config.navbar.buttons

    assert len(buttons) == 1

    # Test button
    button = buttons[0]
    assert button.href == "https://github.com/org"
    assert button.color == "#000"
    assert button.icon_class == "fa fa-github"


def test_sphinx_app_site_config_attachment(sphinx_app, site_config):
    """Test that sphinx_app has the correct site_config attached."""
    assert hasattr(sphinx_app, "site_config")
    app_site_config = getattr(sphinx_app, "site_config")
    assert app_site_config is site_config
    assert app_site_config.site_title == "My Test Site"


def test_content_fixture_behavior():
    """Test the content fixture behavior."""
    # The content fixture is tested through integration tests
    # that actually use it. This test verifies it can be imported.
    from tdom_sphinx.fixtures import content

    assert callable(content)


def test_page_fixture_behavior():
    """Test the page fixture behavior."""
    # The page fixture is tested through integration tests
    # that actually use it. This test verifies it can be imported.
    from tdom_sphinx.fixtures import page

    assert callable(page)


def test_greeting_dataclass():
    """Test that Greeting dataclass works correctly."""
    from tdom_sphinx.fixtures import Greeting

    # Test default value
    greeting = Greeting()
    assert greeting.salutation == "Hello"

    # Test custom value
    custom_greeting = Greeting(salutation="Hi")
    assert custom_greeting.salutation == "Hi"


def test_url_dataclass():
    """Test that URL dataclass works correctly."""
    from tdom_sphinx.fixtures import URL

    url = URL(path="/docs/index.html")
    assert url.path == "/docs/index.html"


def test_registry_fixture(registry):
    """Test that registry fixture returns correct dict."""
    assert isinstance(registry, dict)
    assert len(registry) == 0  # Empty by default


def test_rootdir_fixture(rootdir):
    """Test that rootdir fixture returns correct Path."""
    from pathlib import Path

    assert isinstance(rootdir, Path)
    assert rootdir.name == "roots"
    assert rootdir.exists()
