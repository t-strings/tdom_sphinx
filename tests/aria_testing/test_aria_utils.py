"""
Tests for aria_testing.utils module.
"""

import re

from tdom import Comment, Element, Fragment, Text

from tdom_sphinx.aria_testing.utils import (
    find_elements_by_tag,
    get_all_elements,
    get_text_content,
    matches_text,
    normalize_text,
)


def test_get_text_content_text_node():
    text = Text("Hello world")
    assert get_text_content(text) == "Hello world"


def test_get_text_content_element_with_text_child():
    element = Element("p", children=[Text("Hello world")])
    assert get_text_content(element) == "Hello world"


def test_get_text_content_element_with_multiple_text_children():
    element = Element("p", children=[Text("Hello "), Text("world")])
    assert get_text_content(element) == "Hello world"


def test_get_text_content_nested_elements():
    element = Element(
        "div",
        children=[
            Text("Start "),
            Element("span", children=[Text("middle")]),
            Text(" end"),
        ],
    )
    assert get_text_content(element) == "Start middle end"


def test_get_text_content_fragment():
    fragment = Fragment(
        children=[
            Text("First "),
            Element("strong", children=[Text("bold")]),
            Text(" last"),
        ]
    )
    assert get_text_content(fragment) == "First bold last"


def test_get_text_content_comment_node():
    comment = Comment("This is a comment")
    assert get_text_content(comment) == ""


def test_get_text_content_empty_element():
    element = Element("div")
    assert get_text_content(element) == ""


def test_normalize_text_basic_normalization():
    assert normalize_text("  hello  world  ") == "hello world"


def test_normalize_text_collapse_whitespace():
    text = "hello\n\t  world"
    assert normalize_text(text, collapse_whitespace=True) == "hello world"


def test_normalize_text_no_collapse_whitespace():
    text = "hello\n\t  world"
    assert normalize_text(text, collapse_whitespace=False) == "hello\n\t  world"


def test_normalize_text_trim_only():
    text = "  hello\n\t  world  "
    assert (
        normalize_text(text, collapse_whitespace=False, trim=True) == "hello\n\t  world"
    )


def test_normalize_text_no_trim():
    text = "  hello  world  "
    assert normalize_text(text, trim=False) == " hello world "


def test_normalize_text_both_disabled():
    text = "  hello\n\t  world  "
    assert normalize_text(text, collapse_whitespace=False, trim=False) == text


def test_matches_text_exact_string_match():
    assert matches_text("hello", "hello", exact=True) is True
    assert matches_text("hello", "Hello", exact=True) is False


def test_matches_text_substring_match():
    assert matches_text("hello world", "world", exact=False) is True
    assert matches_text("hello world", "WORLD", exact=False) is True
    assert matches_text("hello world", "xyz", exact=False) is False


def test_matches_text_regex_match():
    pattern = re.compile(r"\d+")
    assert matches_text("age: 25", pattern) is True
    assert matches_text("no numbers", pattern) is False


def test_matches_text_normalization():
    assert matches_text("  hello  world  ", "hello world", normalize=True) is True
    assert matches_text("  hello  world  ", "hello world", normalize=False) is False


def test_find_elements_by_tag_basic():
    container = Element(
        "div", children=[Element("button"), Element("input"), Element("button")]
    )

    results = find_elements_by_tag(container, "button")
    assert len(results) == 2


def test_find_elements_by_tag_case_insensitive():
    container = Element("div", children=[Element("BUTTON"), Element("button")])

    results = find_elements_by_tag(container, "button")
    assert len(results) == 2


def test_find_elements_by_tag_nested():
    container = Element(
        "div",
        children=[
            Element("section", children=[Element("p", children=[Text("Hello")])]),
            Element("p", children=[Text("World")]),
        ],
    )

    results = find_elements_by_tag(container, "p")
    assert len(results) == 2


def test_get_all_elements_simple():
    container = Element(
        "div", children=[Element("p"), Element("span"), Text("some text")]
    )

    results = get_all_elements(container)
    assert len(results) == 3  # div, p, span (Text is not an Element)
    assert results[0].tag == "div"
    assert results[1].tag == "p"
    assert results[2].tag == "span"


def test_get_all_elements_nested():
    container = Element(
        "div",
        children=[
            Element(
                "section",
                children=[
                    Element("h1"),
                    Element("p", children=[Element("strong")]),
                ],
            )
        ],
    )

    results = get_all_elements(container)
    assert len(results) == 5  # div, section, h1, p, strong


def test_get_all_elements_fragment():
    fragment = Fragment(children=[Element("div"), Element("span")])

    results = get_all_elements(fragment)
    assert len(results) == 2
