from bs4 import BeautifulSoup
from tdom import html

from conftest import pathto
from tdom_sphinx.xxxcomponents import Head, Header, Body
from tdom_sphinx.models import TdomContext


def test_head_with_site_title(tdom_context: TdomContext):
    props = dict(pathto=pathto, title="This Page", site_title="This Site")
    result = html(t"<{Head} {props} />")
    soup = BeautifulSoup(str(result), "html.parser")

    assert soup.find("title").text == "This Page - This Site"
    links = soup.find_all("link", attrs={"rel": "stylesheet"})
    assert links[0].attrs["href"] == "_static/pico.css"


def test_head_with_no_site_title(tdom_context: TdomContext):
    props = dict(pathto=pathto, title="This Page")
    result = html(t"<{Head} {props} />")
    soup = BeautifulSoup(str(result), "html.parser")

    assert soup.find("title").text == "This Page"


def test_body(tdom_context: TdomContext):
    result = html(t"<{Body} context={tdom_context} />")
    soup = BeautifulSoup(str(result), "html.parser")

    assert soup.select_one("article p").text == "Hello World"


def test_header(tdom_context: TdomContext):
    result = html(t"<{Header} context={tdom_context} />")
    soup = BeautifulSoup(str(result), "html.parser")
    root_link = soup.find(attrs={"aria-label": "root"})
    assert root_link.get("href") == "/"
