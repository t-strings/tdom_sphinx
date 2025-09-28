from typing import Optional

from bs4 import BeautifulSoup, Tag
from tdom import html

from tdom_sphinx.components.main import Main


def test_main_includes_body_from_context(page_context):
    result = html(t"<{Main} page_context={page_context} />")
    soup = BeautifulSoup(str(result), "html.parser")

    main_element: Optional[Tag] = soup.select_one("main")
    assert main_element is not None

    p_element: Optional[Tag] = main_element.select_one("p")
    assert p_element is not None
    assert p_element.get_text(strip=True) == "Hello World"
