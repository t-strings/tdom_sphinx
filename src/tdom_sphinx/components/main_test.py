from tdom import html

from tdom_sphinx.aria_testing import get_by_role
from tdom_sphinx.aria_testing.utils import get_text_content
from tdom_sphinx.components.main import Main


def test_main_includes_body_from_context(page_context):
    result = html(t"<{Main} page_context={page_context} />")

    main_element = get_by_role(result, "main")
    assert main_element.tag == "main"

    # Check that the main contains the expected text
    main_text = get_text_content(main_element).strip()
    assert "Hello World" in main_text

    # The main element should contain the raw HTML from page_context.body
    main_html = str(main_element)
    assert "<p>Hello World</p>" in main_html
