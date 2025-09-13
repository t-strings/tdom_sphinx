# Import a couple of tag helpers from htpy. The API provides functions per tag.
from htpy import div, span
from tdom import html

from tdom_sphinx.convert import htpy_component


@htpy_component
def Greeting(name: str):
    # Return a htpy element; the decorator will convert to tdom Element
    # htpy treats the first positional string as id/class shorthand, so pass None first
    # to indicate no id/class, then provide children/text.
    return div[("Hello ", span[name])]


def test_htpy_component_decorator_basic():
    # Use the component inside a t-strings template via component syntax
    result = html(t'<{Greeting} name="World"/>')
    assert str(result) == "<div>Hello <span>World</span></div>"
