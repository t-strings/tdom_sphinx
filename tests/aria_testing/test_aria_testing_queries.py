"""
Tests for aria_testing.queries module.
"""

import pytest
from tdom.processor import html

from tdom_sphinx.aria_testing.errors import ElementNotFoundError, MultipleElementsError
from tdom_sphinx.aria_testing.queries import (
    get_all_by_role,
    get_all_by_test_id,
    get_all_by_text,
    get_by_role,
    get_by_test_id,
    get_by_text,
    get_role_for_element,
    query_all_by_role,
    query_all_by_test_id,
    query_all_by_text,
    query_by_role,
    query_by_test_id,
    query_by_text,
)


@pytest.fixture
def sample_document():
    """Create a sample document structure for testing."""
    return html(t"""<div>
        <h1>Welcome</h1>
        <p>Hello world</p>
        <button>Click me</button>
        <input type="text" placeholder="Enter name" />
        <div data-testid="content">
            Main content
            <span>nested</span>
        </div>
        <button data-testid="save">Save</button>
        <button data-testid="cancel">Cancel</button>
    </div>""")


def test_query_by_text_exact_match(sample_document):
    element = query_by_text(sample_document, "Hello world")
    assert element is not None
    assert element.tag == "p"


def test_query_by_text_not_found(sample_document):
    element = query_by_text(sample_document, "Not found")
    assert element is None


# Note: substring and regex matching not implemented yet
# def test_query_by_text_substring(sample_document):
#     element = query_by_text(sample_document, "Hello", exact=False)
#     assert element is not None
#     assert element.tag == "p"
#
#
# def test_query_by_text_regex(sample_document):
#     pattern = re.compile(r"Click.*")
#     element = query_by_text(sample_document, pattern)
#     assert element is not None
#     assert element.tag == "button"


def test_get_by_text_success(sample_document):
    element = get_by_text(sample_document, "Welcome")
    assert element.tag == "h1"


def test_get_by_text_not_found(sample_document):
    with pytest.raises(ElementNotFoundError) as exc_info:
        get_by_text(sample_document, "Not found")
    assert "Unable to find element with text: Not found" in str(exc_info.value)


def test_get_by_text_multiple_elements():
    document = html(t"""<div>
        <p>duplicate</p>
        <span>duplicate</span>
    </div>""")

    with pytest.raises(MultipleElementsError) as exc_info:
        get_by_text(document, "duplicate")
    assert "Found multiple elements with text: duplicate" in str(exc_info.value)
    # Add type checking for MultipleElementsError instance
    assert isinstance(exc_info.value, MultipleElementsError)
    assert exc_info.value.count == 2


def test_query_all_by_text():
    document = html(t"""<div>
        <p>test</p>
        <span>test</span>
        <div>other</div>
    </div>""")

    elements = query_all_by_text(document, "test")
    assert len(elements) == 2
    assert elements[0].tag == "p"
    assert elements[1].tag == "span"


def test_get_all_by_text_success():
    document = html(t"""<div>
        <p>item</p>
        <span>item</span>
    </div>""")

    elements = get_all_by_text(document, "item")
    assert len(elements) == 2


def test_get_all_by_text_not_found(sample_document):
    with pytest.raises(ElementNotFoundError):
        get_all_by_text(sample_document, "Not found")


def test_query_by_test_id_found(sample_document):
    element = query_by_test_id(sample_document, "content")
    assert element is not None
    assert element.attrs["data-testid"] == "content"


def test_query_by_test_id_not_found(sample_document):
    element = query_by_test_id(sample_document, "nonexistent")
    assert element is None


def test_get_by_test_id_success(sample_document):
    element = get_by_test_id(sample_document, "save")
    assert element.attrs["data-testid"] == "save"


def test_get_by_test_id_not_found(sample_document):
    with pytest.raises(ElementNotFoundError) as exc_info:
        get_by_test_id(sample_document, "nonexistent")
    assert "Unable to find element with data-testid: nonexistent" in str(exc_info.value)


def test_get_by_test_id_multiple_elements():
    document = html(t"""<div>
        <button data-testid="action">Button</button>
        <div data-testid="action">Div</div>
    </div>""")

    with pytest.raises(MultipleElementsError):
        get_by_test_id(document, "action")


def test_custom_test_id_attribute():
    document = html(t'<div><button data-qa="submit">Submit</button></div>')

    element = query_by_test_id(document, "submit", attribute="data-qa")
    assert element is not None


def test_query_all_by_test_id():
    document = html(t"""<div>
        <button data-testid="btn">Button</button>
        <input data-testid="btn" type="text" />
    </div>""")

    elements = query_all_by_test_id(document, "btn")
    assert len(elements) == 2


def test_get_all_by_test_id_success():
    document = html(t"""<div>
        <button data-testid="item">Button</button>
        <div data-testid="item">Div</div>
    </div>""")

    elements = get_all_by_test_id(document, "item")
    assert len(elements) == 2


def test_get_all_by_test_id_not_found(sample_document):
    with pytest.raises(ElementNotFoundError):
        get_all_by_test_id(sample_document, "nonexistent")


def test_explicit_role():
    document = html(t'<div><div role="button">Custom button</div></div>')

    element = query_by_role(document, "button")
    assert element is not None


def test_implicit_role_button():
    document = html(t"<div><button>Click me</button></div>")

    element = query_by_role(document, "button")
    assert element is not None
    assert element.tag == "button"


def test_implicit_role_heading():
    document = html(t"""<div>
        <h1>Title</h1>
        <h2>Subtitle</h2>
    </div>""")

    elements = query_all_by_role(document, "heading")
    assert len(elements) == 2


def test_heading_with_level():
    document = html(t"""<div>
        <h1>Title</h1>
        <h2>Subtitle</h2>
    </div>""")

    element = query_by_role(document, "heading", level=1)
    assert element is not None
    assert element.tag == "h1"

    element = query_by_role(document, "heading", level=3)
    assert element is None


def test_aria_level_attribute():
    document = html(
        t'<div><div role="heading" aria-level="3">Custom heading</div></div>'
    )

    element = query_by_role(document, "heading", level=3)
    assert element is not None


def test_input_type_roles():
    document = html(t"""<div>
        <input type="text" />
        <input type="checkbox" />
        <input type="button" />
    </div>""")

    textbox = query_by_role(document, "textbox")
    assert textbox is not None
    assert textbox.attrs["type"] == "text"

    checkbox = query_by_role(document, "checkbox")
    assert checkbox is not None
    assert checkbox.attrs["type"] == "checkbox"

    button = query_by_role(document, "button")
    assert button is not None
    assert button.attrs["type"] == "button"


# Note: Role with name parameter not fully implemented yet
# def test_role_with_name():
#     document = html(t"""<div>
#         <button aria-label="Save document">Save</button>
#         <button aria-label="Cancel operation">Cancel</button>
#     </div>""")
#
#     element = query_by_role(document, "button", name="Save")
#     assert element is not None
#     aria_label = element.attrs.get("aria-label")
#     assert aria_label is not None and "Save" in aria_label


def test_get_by_role_success():
    document = html(t"<div><nav>Navigation</nav></div>")

    element = get_by_role(document, "navigation")
    assert element.tag == "nav"


def test_get_by_role_not_found():
    document = html(t"<div><p>Just text</p></div>")

    with pytest.raises(ElementNotFoundError) as exc_info:
        get_by_role(document, "button")
    assert "Unable to find element with role 'button'" in str(exc_info.value)


def test_get_by_role_multiple_elements():
    document = html(t"""<div>
        <button>First</button>
        <button>Second</button>
    </div>""")

    with pytest.raises(MultipleElementsError):
        get_by_role(document, "button")


def test_get_all_by_role_success():
    document = html(t"""<div>
        <li>Item 1</li>
        <li>Item 2</li>
    </div>""")

    elements = get_all_by_role(document, "listitem")
    assert len(elements) == 2


def test_get_all_by_role_not_found():
    document = html(t"<div><p>Just text</p></div>")

    with pytest.raises(ElementNotFoundError):
        get_all_by_role(document, "button")


def test_get_role_for_element_explicit():
    element = html(t'<div role="button">Button</div>')
    assert get_role_for_element(element) == "button"


def test_get_role_for_element_implicit_button():
    element = html(t"<button>Click</button>")
    assert get_role_for_element(element) == "button"


def test_get_role_for_element_implicit_heading():
    element = html(t"<h1>Title</h1>")
    assert get_role_for_element(element) == "heading"


def test_get_role_for_element_input_types():
    text_input = html(t'<input type="text" />')
    assert get_role_for_element(text_input) == "textbox"

    checkbox = html(t'<input type="checkbox" />')
    assert get_role_for_element(checkbox) == "checkbox"

    button_input = html(t'<input type="button" />')
    assert get_role_for_element(button_input) == "button"


def test_get_role_for_element_no_role():
    element = html(t"<div>Content</div>")
    assert get_role_for_element(element) is None


def test_get_role_for_element_non_element():
    """Test that get_role_for_element handles non-Element nodes gracefully."""
    from tdom import Text, Fragment

    # Text nodes don't have roles
    text_node = Text("Just text")
    assert get_role_for_element(text_node) is None

    # Fragments don't have roles
    fragment = html(t"<span>One</span><span>Two</span>")
    assert get_role_for_element(fragment) is None


# Note: _get_accessible_name function not implemented yet
# def test_get_accessible_name_aria_label():
#     element = html(t'<button aria-label="Close dialog">X</button>')
#     assert _get_accessible_name(element) == "Close dialog"
#
#
# def test_get_accessible_name_text_content():
#     element = html(t"<button>Submit form</button>")
#     assert _get_accessible_name(element) == "Submit form"
#
#
# def test_get_accessible_name_empty():
#     element = html(t"<div></div>")
#     assert _get_accessible_name(element) == ""


def test_nested_text_content():
    document = html(t"<div><p>Hello <strong>bold</strong> world</p></div>")

    element = query_by_text(document, "Hello bold world")
    assert element is not None
    assert element.tag == "p"


def test_multiple_query_methods_same_element():
    document = html(
        t'<div><button data-testid="submit" aria-label="Submit form">Submit</button></div>'
    )

    # Should find the same element via different methods
    by_text = query_by_text(document, "Submit")
    by_test_id = query_by_test_id(document, "submit")
    by_role = query_by_role(document, "button")

    assert by_text is by_test_id is by_role


def test_fragment_as_container():
    fragment = html(t"<div>First</div><span>Second</span>")

    element = query_by_text(fragment, "First")
    assert element is not None
    assert element.tag == "div"

    elements = query_all_by_text(fragment, "First")
    assert len(elements) == 1
