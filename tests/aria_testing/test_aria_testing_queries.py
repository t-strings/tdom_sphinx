"""
Tests for aria_testing.queries module.
"""

import re

import pytest
from tdom import Element, Fragment, Text

from tdom_sphinx.aria_testing.errors import ElementNotFoundError, MultipleElementsError
from tdom_sphinx.aria_testing.queries import (
    _get_accessible_name,
    _get_role_for_element,
    get_all_by_role,
    get_all_by_test_id,
    get_all_by_text,
    get_by_role,
    get_by_test_id,
    get_by_text,
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
    return Element(
        "div",
        children=[
            Element("h1", children=[Text("Welcome")]),
            Element("p", children=[Text("Hello world")]),
            Element("button", children=[Text("Click me")]),
            Element("input", attrs={"type": "text", "placeholder": "Enter name"}),
            Element(
                "div",
                attrs={"data-testid": "content"},
                children=[
                    Text("Main content"),
                    Element("span", children=[Text("nested")]),
                ],
            ),
            Element("button", attrs={"data-testid": "save"}, children=[Text("Save")]),
            Element(
                "button", attrs={"data-testid": "cancel"}, children=[Text("Cancel")]
            ),
        ],
    )


def test_query_by_text_exact_match(sample_document):
    element = query_by_text(sample_document, "Hello world")
    assert element is not None
    assert element.tag == "p"


def test_query_by_text_not_found(sample_document):
    element = query_by_text(sample_document, "Not found")
    assert element is None


def test_query_by_text_substring(sample_document):
    element = query_by_text(sample_document, "Hello", exact=False)
    assert element is not None
    assert element.tag == "p"


def test_query_by_text_regex(sample_document):
    pattern = re.compile(r"Click.*")
    element = query_by_text(sample_document, pattern)
    assert element is not None
    assert element.tag == "button"


def test_get_by_text_success(sample_document):
    element = get_by_text(sample_document, "Welcome")
    assert element.tag == "h1"


def test_get_by_text_not_found(sample_document):
    with pytest.raises(ElementNotFoundError) as exc_info:
        get_by_text(sample_document, "Not found")
    assert "Unable to find element with text: Not found" in str(exc_info.value)


def test_get_by_text_multiple_elements():
    document = Element(
        "div",
        children=[
            Element("p", children=[Text("duplicate")]),
            Element("span", children=[Text("duplicate")]),
        ],
    )

    with pytest.raises(MultipleElementsError) as exc_info:
        get_by_text(document, "duplicate")
    assert "Found multiple elements with text: duplicate" in str(exc_info.value)
    # Add type checking for MultipleElementsError instance
    assert isinstance(exc_info.value, MultipleElementsError)
    assert exc_info.value.count == 2


def test_query_all_by_text():
    document = Element(
        "div",
        children=[
            Element("p", children=[Text("test")]),
            Element("span", children=[Text("test")]),
            Element("div", children=[Text("other")]),
        ],
    )

    elements = query_all_by_text(document, "test")
    assert len(elements) == 2
    assert elements[0].tag == "p"
    assert elements[1].tag == "span"


def test_get_all_by_text_success():
    document = Element(
        "div",
        children=[
            Element("p", children=[Text("item")]),
            Element("span", children=[Text("item")]),
        ],
    )

    elements = get_all_by_text(document, "item")
    assert len(elements) == 2


def test_get_all_by_text_not_found(sample_document):
    with pytest.raises(ElementNotFoundError):
        get_all_by_text(sample_document, "Not found")


def test_text_normalization():
    document = Element(
        "div", children=[Element("p", children=[Text("  Hello   world  ")])]
    )

    element = query_by_text(document, "Hello world", normalize=True)
    assert element is not None

    element = query_by_text(document, "Hello world", normalize=False)
    assert element is None


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
    document = Element(
        "div",
        children=[
            Element("button", attrs={"data-testid": "action"}),
            Element("div", attrs={"data-testid": "action"}),
        ],
    )

    with pytest.raises(MultipleElementsError):
        get_by_test_id(document, "action")


def test_custom_test_id_attribute():
    document = Element("div", children=[Element("button", attrs={"data-qa": "submit"})])

    element = query_by_test_id(document, "submit", attribute="data-qa")
    assert element is not None


def test_query_all_by_test_id():
    document = Element(
        "div",
        children=[
            Element("button", attrs={"data-testid": "btn"}),
            Element("input", attrs={"data-testid": "btn"}),
        ],
    )

    elements = query_all_by_test_id(document, "btn")
    assert len(elements) == 2


def test_get_all_by_test_id_success():
    document = Element(
        "div",
        children=[
            Element("button", attrs={"data-testid": "item"}),
            Element("div", attrs={"data-testid": "item"}),
        ],
    )

    elements = get_all_by_test_id(document, "item")
    assert len(elements) == 2


def test_get_all_by_test_id_not_found(sample_document):
    with pytest.raises(ElementNotFoundError):
        get_all_by_test_id(sample_document, "nonexistent")


def test_explicit_role():
    document = Element(
        "div",
        children=[
            Element("div", attrs={"role": "button"}, children=[Text("Custom button")])
        ],
    )

    element = query_by_role(document, "button")
    assert element is not None


def test_implicit_role_button():
    document = Element("div", children=[Element("button", children=[Text("Click me")])])

    element = query_by_role(document, "button")
    assert element is not None
    assert element.tag == "button"


def test_implicit_role_heading():
    document = Element(
        "div",
        children=[
            Element("h1", children=[Text("Title")]),
            Element("h2", children=[Text("Subtitle")]),
        ],
    )

    elements = query_all_by_role(document, "heading")
    assert len(elements) == 2


def test_heading_with_level():
    document = Element(
        "div",
        children=[
            Element("h1", children=[Text("Title")]),
            Element("h2", children=[Text("Subtitle")]),
        ],
    )

    element = query_by_role(document, "heading", level=1)
    assert element is not None
    assert element.tag == "h1"

    element = query_by_role(document, "heading", level=3)
    assert element is None


def test_aria_level_attribute():
    document = Element(
        "div",
        children=[
            Element(
                "div",
                attrs={"role": "heading", "aria-level": "3"},
                children=[Text("Custom heading")],
            )
        ],
    )

    element = query_by_role(document, "heading", level=3)
    assert element is not None


def test_input_type_roles():
    document = Element(
        "div",
        children=[
            Element("input", attrs={"type": "text"}),
            Element("input", attrs={"type": "checkbox"}),
            Element("input", attrs={"type": "button"}),
        ],
    )

    textbox = query_by_role(document, "textbox")
    assert textbox is not None
    assert textbox.attrs["type"] == "text"

    checkbox = query_by_role(document, "checkbox")
    assert checkbox is not None
    assert checkbox.attrs["type"] == "checkbox"

    button = query_by_role(document, "button")
    assert button is not None
    assert button.attrs["type"] == "button"


def test_role_with_name():
    document = Element(
        "div",
        children=[
            Element(
                "button",
                attrs={"aria-label": "Save document"},
                children=[Text("Save")],
            ),
            Element(
                "button",
                attrs={"aria-label": "Cancel operation"},
                children=[Text("Cancel")],
            ),
        ],
    )

    element = query_by_role(document, "button", name="Save")
    assert element is not None
    aria_label = element.attrs.get("aria-label")
    assert aria_label is not None and "Save" in aria_label


def test_get_by_role_success():
    document = Element("div", children=[Element("nav", children=[Text("Navigation")])])

    element = get_by_role(document, "navigation")
    assert element.tag == "nav"


def test_get_by_role_not_found():
    document = Element("div", children=[Element("p", children=[Text("Just text")])])

    with pytest.raises(ElementNotFoundError) as exc_info:
        get_by_role(document, "button")
    assert "Unable to find element with role 'button'" in str(exc_info.value)


def test_get_by_role_multiple_elements():
    document = Element(
        "div",
        children=[
            Element("button", children=[Text("First")]),
            Element("button", children=[Text("Second")]),
        ],
    )

    with pytest.raises(MultipleElementsError):
        get_by_role(document, "button")


def test_get_all_by_role_success():
    document = Element(
        "div",
        children=[
            Element("li", children=[Text("Item 1")]),
            Element("li", children=[Text("Item 2")]),
        ],
    )

    elements = get_all_by_role(document, "listitem")
    assert len(elements) == 2


def test_get_all_by_role_not_found():
    document = Element("div", children=[Element("p", children=[Text("Just text")])])

    with pytest.raises(ElementNotFoundError):
        get_all_by_role(document, "button")


def test_get_role_for_element_explicit():
    element = Element("div", attrs={"role": "button"})
    assert _get_role_for_element(element) == "button"


def test_get_role_for_element_implicit_button():
    element = Element("button")
    assert _get_role_for_element(element) == "button"


def test_get_role_for_element_implicit_heading():
    element = Element("h1")
    assert _get_role_for_element(element) == "heading"


def test_get_role_for_element_input_types():
    text_input = Element("input", attrs={"type": "text"})
    assert _get_role_for_element(text_input) == "textbox"

    checkbox = Element("input", attrs={"type": "checkbox"})
    assert _get_role_for_element(checkbox) == "checkbox"

    button_input = Element("input", attrs={"type": "button"})
    assert _get_role_for_element(button_input) == "button"


def test_get_role_for_element_no_role():
    element = Element("div")
    assert _get_role_for_element(element) is None


def test_get_accessible_name_aria_label():
    element = Element("button", attrs={"aria-label": "Close dialog"})
    assert _get_accessible_name(element) == "Close dialog"


def test_get_accessible_name_text_content():
    element = Element("button", children=[Text("Submit form")])
    assert _get_accessible_name(element) == "Submit form"


def test_get_accessible_name_empty():
    element = Element("div")
    assert _get_accessible_name(element) == ""


def test_nested_text_content():
    document = Element(
        "div",
        children=[
            Element(
                "p",
                children=[
                    Text("Hello "),
                    Element("strong", children=[Text("bold")]),
                    Text(" world"),
                ],
            )
        ],
    )

    element = query_by_text(document, "Hello bold world")
    assert element is not None
    assert element.tag == "p"


def test_multiple_query_methods_same_element():
    document = Element(
        "div",
        children=[
            Element(
                "button",
                attrs={"data-testid": "submit", "aria-label": "Submit form"},
                children=[Text("Submit")],
            )
        ],
    )

    # Should find the same element via different methods
    by_text = query_by_text(document, "Submit")
    by_test_id = query_by_test_id(document, "submit")
    by_role = query_by_role(document, "button")

    assert by_text is by_test_id is by_role


def test_fragment_as_container():
    fragment = Fragment(
        children=[
            Element("div", children=[Text("First")]),
            Element("span", children=[Text("Second")]),
        ]
    )

    element = query_by_text(fragment, "First")
    assert element is not None
    assert element.tag == "div"

    elements = query_all_by_text(fragment, "First")
    assert len(elements) == 1
