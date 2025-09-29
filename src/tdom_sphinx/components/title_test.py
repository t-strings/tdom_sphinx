from tdom import html

from tdom_sphinx.components.title import Title


def test_with_site_title():
    container = html(t'<{Title} page_title="The Resource" site_title="The Site"/>')
    assert str(container) == "<title>The Resource - The Site</title>"


def test_without_site_title():
    container = html(t"<{Title} page_title='The Resource' />")
    assert str(container) == "<title>The Resource</title>"
