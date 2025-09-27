from bs4 import BeautifulSoup
from tdom import html

from tdom_sphinx.components.main import Main


def test_main_includes_body_from_context(page_context):
    result = html(t"<{Main} page_context={page_context} />")
    soup = BeautifulSoup(str(result), "html.parser")

    main = soup.select_one("main")
    assert main is not None

    p = main.select_one("p")
    assert p is not None
    assert p.text == "Hello World"
