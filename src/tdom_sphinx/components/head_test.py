from tdom import html

from tdom_sphinx.aria_testing import get_by_role
from tdom_sphinx.aria_testing.utils import get_text_content
from tdom_sphinx.components.head import Head, make_full_title


def test_head(page_context, site_config):
    result = html(t"<{Head} page_context={page_context} site_config={site_config} />")
    # Head component doesn't have semantic roles, so we need to find by tag
    # Since this is document metadata, we'll check the string representation
    result_str = str(result)
    assert "<title>My Test Page - My Test Site</title>" in result_str


def test_make_full_title_with_site_config(page_context, site_config):
    assert (
        make_full_title(page_context=page_context, site_config=site_config)
        == "My Test Page - My Test Site"
    )


def test_make_full_title_without_site_config(page_context):
    assert make_full_title(page_context=page_context, site_config=None) == "My Test Page"
