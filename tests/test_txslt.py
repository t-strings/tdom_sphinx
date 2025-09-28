"""Tests for TXSLT functionality."""

import pytest
from tdom import Element, Text, html

from tdom_sphinx.txslt import (
    apply_templates,
    copy_of,
    select,
    template,
    value_of,
)
from tdom_sphinx.txslt.registry import reset_global_registry
from tdom_sphinx.txslt.helpers import (
    parse_html_string,
    select_one,
    select_all,
    get_text,
    get_attribute,
)


@pytest.fixture(autouse=True)
def reset_templates():
    """Reset the global template registry before each test."""
    reset_global_registry()
    yield
    reset_global_registry()


def test_template_decorator_registration():
    """Test that @template decorator registers templates."""

    @template(pattern="person")
    def person_template(node, context):
        return html(t"""<div class="person">{value_of(node)}</div>""")

    # Create a test node
    person_node = Element(tag="person", children=[Text("John Doe")])

    # Apply templates
    result = apply_templates(person_node)

    # Parse result and test
    parsed = parse_html_string(str(result))
    div = select_one(parsed, "div.person")
    assert div is not None
    assert get_text(div, strip=True) == "John Doe"


def test_recursive_template_processing():
    """Test recursive processing of nested elements."""

    @template(pattern="people")
    def people_template(node, context):
        return html(t"""
        <div class="people">
            {apply_templates(select(node, "person"))}
        </div>
        """)

    @template(pattern="person")
    def person_template(node, context):
        name = value_of(node, "name")
        age = value_of(node, "age")
        return html(t"""
        <div class="person">
            <span class="name">{name}</span>
            <span class="age">{age}</span>
        </div>
        """)

    # Create test data
    people_node = Element(
        tag="people",
        children=[
            Element(
                tag="person",
                children=[
                    Element(tag="name", children=[Text("Alice")]),
                    Element(tag="age", children=[Text("30")]),
                ],
            ),
            Element(
                tag="person",
                children=[
                    Element(tag="name", children=[Text("Bob")]),
                    Element(tag="age", children=[Text("25")]),
                ],
            ),
        ],
    )

    # Apply templates
    result = apply_templates(people_node)

    # Parse result and test
    parsed = parse_html_string(str(result))

    # Check structure
    people_div = select_one(parsed, "div.people")
    assert people_div is not None

    person_divs = select_all(parsed, "div.person")
    assert len(person_divs) == 2

    # Check first person
    first_person = person_divs[0]
    name_span = select_one(first_person, "span.name")
    age_span = select_one(first_person, "span.age")
    assert name_span is not None
    assert age_span is not None
    assert get_text(name_span, strip=True) == "Alice"
    assert get_text(age_span, strip=True) == "30"

    # Check second person
    second_person = person_divs[1]
    name_span = select_one(second_person, "span.name")
    age_span = select_one(second_person, "span.age")
    assert name_span is not None
    assert age_span is not None
    assert get_text(name_span, strip=True) == "Bob"
    assert get_text(age_span, strip=True) == "25"


def test_template_priority():
    """Test that higher priority templates are selected first."""

    @template(pattern="item", priority=1)
    def low_priority_template(node, context):
        return html(t"""<span>Low priority</span>""")

    @template(pattern="item", priority=10)
    def high_priority_template(node, context):
        return html(t"""<span>High priority</span>""")

    item_node = Element(tag="item", children=[Text("test")])
    result = apply_templates(item_node)

    parsed = parse_html_string(str(result))
    span = select_one(parsed, "span")
    assert span is not None
    assert get_text(span, strip=True) == "High priority"


def test_template_modes():
    """Test template mode functionality."""

    @template(pattern="person", mode="summary")
    def person_summary_template(node, context):
        name = value_of(node, "name")
        return html(t"""<span>{name}</span>""")

    @template(pattern="person", mode="detailed")
    def person_detailed_template(node, context):
        name = value_of(node, "name")
        age = value_of(node, "age")
        return html(t"""<div><h3>{name}</h3><p>Age: {age}</p></div>""")

    person_node = Element(
        tag="person",
        children=[
            Element(tag="name", children=[Text("Alice")]),
            Element(tag="age", children=[Text("30")]),
        ],
    )

    # Test summary mode
    summary_result = apply_templates(person_node, mode="summary")
    summary_parsed = parse_html_string(str(summary_result))
    span = select_one(summary_parsed, "span")
    assert span is not None
    assert get_text(span, strip=True) == "Alice"

    # Test detailed mode
    detailed_result = apply_templates(person_node, mode="detailed")
    detailed_parsed = parse_html_string(str(detailed_result))
    h3 = select_one(detailed_parsed, "h3")
    p = select_one(detailed_parsed, "p")
    assert h3 is not None
    assert p is not None
    assert get_text(h3, strip=True) == "Alice"
    assert get_text(p, strip=True) == "Age: 30"


def test_select_function():
    """Test the select helper function."""
    root = Element(
        tag="root",
        children=[
            Element(tag="child1", children=[Text("first")]),
            Element(tag="child2", children=[Text("second")]),
            Element(tag="child1", children=[Text("third")]),
        ],
    )

    # Select all child1 elements
    child1_nodes = select(root, "child1")
    assert len(child1_nodes) == 2
    assert all(
        isinstance(node, Element) and node.tag == "child1" for node in child1_nodes
    )

    # Select all children
    all_children = select(root, "*")
    assert len(all_children) == 3


def test_value_of_function():
    """Test the value_of helper function."""
    root = Element(
        tag="person",
        children=[
            Element(tag="name", children=[Text("Alice")]),
            Element(tag="age", children=[Text("30")]),
        ],
    )

    # Get text content of specific child
    name = value_of(root, "name")
    assert name == "Alice"

    age = value_of(root, "age")
    assert age == "30"

    # Get text content of entire node
    text_node = Text("Hello World")
    assert value_of(text_node) == "Hello World"


def test_copy_of_function():
    """Test the copy_of helper function."""
    original = Element(
        tag="person",
        attrs={"id": "123"},
        children=[
            Element(tag="name", children=[Text("Alice")]),
            Text(" - "),
            Element(tag="age", children=[Text("30")]),
        ],
    )

    copied = copy_of(original)

    # Should be a different object
    assert copied is not original
    assert isinstance(copied, Element)
    assert isinstance(original, Element)
    assert copied.children[0] is not original.children[0]

    # But should have same content
    assert copied.tag == original.tag
    assert copied.attrs == original.attrs
    assert len(copied.children) == len(original.children)

    # Check deep copy
    assert isinstance(copied.children[0], Element)
    assert copied.children[0].tag == "name"
    assert value_of(copied.children[0]) == "Alice"


def test_default_template_behavior():
    """Test default behavior when no template matches."""
    # No templates registered, should use default behavior

    root = Element(
        tag="container",
        attrs={"class": "wrapper"},
        children=[
            Text("Hello "),
            Element(tag="em", children=[Text("world")]),
            Text("!"),
        ],
    )

    result = apply_templates(root)

    # Should preserve structure but process children
    assert isinstance(result, Element)
    assert result.tag == "container"
    assert result.attrs == {"class": "wrapper"}
    assert len(result.children) == 3

    parsed = parse_html_string(str(result))
    container = select_one(parsed, "container")
    assert container is not None
    assert get_attribute(container, "class") == "wrapper"

    em = select_one(container, "em")
    assert em is not None
    assert get_text(em, strip=True) == "world"


def test_complex_hierarchical_transformation():
    """Test complex hierarchical transformation similar to XSLT example."""

    @template(pattern="catalog")
    def catalog_template(node, context):
        return html(t"""
        <html>
            <body>
                <h1>Product Catalog</h1>
                <div class="products">
                    {apply_templates(select(node, "product"))}
                </div>
            </body>
        </html>
        """)

    @template(pattern="product")
    def product_template(node, context):
        name = value_of(node, "name")
        price = value_of(node, "price")
        return html(t"""
        <div class="product">
            <h2>{name}</h2>
            <p class="price">${price}</p>
            <div class="description">
                {apply_templates(select(node, "description"))}
            </div>
        </div>
        """)

    @template(pattern="description")
    def description_template(node, context):
        return html(t"""<p>{value_of(node)}</p>""")

    # Create test data
    catalog = Element(
        tag="catalog",
        children=[
            Element(
                tag="product",
                children=[
                    Element(tag="name", children=[Text("Widget A")]),
                    Element(tag="price", children=[Text("19.99")]),
                    Element(
                        tag="description",
                        children=[Text("A useful widget for everyday tasks.")],
                    ),
                ],
            ),
            Element(
                tag="product",
                children=[
                    Element(tag="name", children=[Text("Gadget B")]),
                    Element(tag="price", children=[Text("29.99")]),
                    Element(
                        tag="description",
                        children=[Text("An amazing gadget with multiple features.")],
                    ),
                ],
            ),
        ],
    )

    result = apply_templates(catalog)
    parsed = parse_html_string(str(result))

    # Check overall structure
    html_tag = select_one(parsed, "html")
    assert html_tag is not None

    h1 = select_one(parsed, "h1")
    assert h1 is not None
    assert get_text(h1, strip=True) == "Product Catalog"

    products_div = select_one(parsed, "div.products")
    assert products_div is not None

    product_divs = select_all(parsed, "div.product")
    assert len(product_divs) == 2

    # Check first product
    first_product = product_divs[0]
    h2 = select_one(first_product, "h2")
    price_p = select_one(first_product, "p.price")
    desc_p = select_one(first_product, "div.description p")

    assert h2 is not None
    assert price_p is not None
    assert desc_p is not None
    assert get_text(h2, strip=True) == "Widget A"
    assert get_text(price_p, strip=True) == "$19.99"
    assert get_text(desc_p, strip=True) == "A useful widget for everyday tasks."
