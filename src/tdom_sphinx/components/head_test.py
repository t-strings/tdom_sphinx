from bs4 import BeautifulSoup
from tdom import html

from tdom_sphinx.components.head import Head, make_full_title


def test_head(page_context, site_config):
    result = html(t"<{Head} page_context={page_context} site_config={site_config} />")
    soup = BeautifulSoup(str(result), "html.parser")
    assert soup.select_one("title").text == "My Test Page - My Test Site"


def test_make_full_title_with_site_config(page_context, site_config):
    assert (
        make_full_title(page_context=page_context, site_config=site_config)
        == "My Test Page - My Test Site"
    )


def test_make_full_title_without_site_config(page_context):
    assert make_full_title(page_context=page_context, site_config=None) == "My Test Page"
