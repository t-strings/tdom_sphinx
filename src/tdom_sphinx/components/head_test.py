from bs4 import BeautifulSoup
from tdom import html

from tdom_sphinx.components.head import Head
from tdom_sphinx.models import TdomContext


def test_head(tdom_context: TdomContext):
    result = html(t"<{Head}  context={tdom_context} />")
    soup = BeautifulSoup(str(result), "html.parser")
    assert soup.select_one("title").text == "My Test Page - My Test Site"
