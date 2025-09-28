"""Example usage of TXSLT showing various transformation patterns."""

from tdom import Element, Text, html
from tdom_sphinx.txslt import template, apply_templates, select, value_of


def example_person_transformation():
    """Example showing basic person data transformation."""

    @template(pattern="person")
    def person_template(node, context):
        name = value_of(node, "name")
        age = value_of(node, "age")
        return html(t"""
        <div class="person">
            <h3>{name}</h3>
            <p>Age: {age}</p>
            {apply_templates(select(node, "address"))}
        </div>
        """)

    @template(pattern="address")
    def address_template(node, context):
        street = value_of(node, "street")
        city = value_of(node, "city")
        state = value_of(node, "state")
        return html(t"""
        <div class="address">
            <p>{street}</p>
            <p>{city}, {state}</p>
        </div>
        """)

    # Create sample data
    person_data = Element(
        tag="person",
        children=[
            Element(tag="name", children=[Text("John Smith")]),
            Element(tag="age", children=[Text("35")]),
            Element(
                tag="address",
                children=[
                    Element(tag="street", children=[Text("123 Main St")]),
                    Element(tag="city", children=[Text("Anytown")]),
                    Element(tag="state", children=[Text("CA")]),
                ],
            ),
        ],
    )

    return apply_templates(person_data)


def example_hierarchical_list():
    """Example showing recursive hierarchical list processing."""

    @template(pattern="items")
    def items_template(node, context):
        return html(t"""
        <ul class="item-list">
            {apply_templates(select(node, "item"))}
        </ul>
        """)

    @template(pattern="item")
    def item_template(node, context):
        name = value_of(node, "name")
        # Check for nested items
        nested_items = select(node, "items")
        return html(t"""
        <li>
            <span class="item-name">{name}</span>
            {apply_templates(nested_items)}
        </li>
        """)

    # Create hierarchical data
    hierarchical_data = Element(
        tag="items",
        children=[
            Element(
                tag="item",
                children=[
                    Element(tag="name", children=[Text("Category 1")]),
                    Element(
                        tag="items",
                        children=[
                            Element(
                                tag="item",
                                children=[
                                    Element(tag="name", children=[Text("Item 1.1")])
                                ],
                            ),
                            Element(
                                tag="item",
                                children=[
                                    Element(tag="name", children=[Text("Item 1.2")])
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            Element(
                tag="item",
                children=[Element(tag="name", children=[Text("Category 2")])],
            ),
        ],
    )

    return apply_templates(hierarchical_data)


def example_mode_based_processing():
    """Example showing mode-based template processing."""

    @template(pattern="article", mode="summary")
    def article_summary_template(node, context):
        title = value_of(node, "title")
        author = value_of(node, "author")
        return html(t"""
        <div class="article-summary">
            <h4>{title}</h4>
            <p>by {author}</p>
        </div>
        """)

    @template(pattern="article", mode="full")
    def article_full_template(node, context):
        title = value_of(node, "title")
        author = value_of(node, "author")
        content = value_of(node, "content")
        return html(t"""
        <article class="full-article">
            <header>
                <h1>{title}</h1>
                <p class="byline">by {author}</p>
            </header>
            <div class="content">
                <p>{content}</p>
            </div>
        </article>
        """)

    @template(pattern="articles")
    def articles_template(node, context):
        return html(t"""
        <div class="articles">
            <div class="summaries">
                <h2>Article Summaries</h2>
                {apply_templates(select(node, "article"), mode="summary")}
            </div>
            <div class="full-articles">
                <h2>Full Articles</h2>
                {apply_templates(select(node, "article"), mode="full")}
            </div>
        </div>
        """)

    # Create article data
    articles_data = Element(
        tag="articles",
        children=[
            Element(
                tag="article",
                children=[
                    Element(tag="title", children=[Text("Python T-Strings")]),
                    Element(tag="author", children=[Text("Jane Developer")]),
                    Element(
                        tag="content",
                        children=[Text("T-strings are a powerful new feature...")],
                    ),
                ],
            ),
            Element(
                tag="article",
                children=[
                    Element(tag="title", children=[Text("XSLT vs TXSLT")]),
                    Element(tag="author", children=[Text("Bob Transformer")]),
                    Element(
                        tag="content",
                        children=[
                            Text("Comparing traditional XSLT with modern approaches...")
                        ],
                    ),
                ],
            ),
        ],
    )

    return apply_templates(articles_data)


def example_priority_based_templates():
    """Example showing template priority in action."""

    # General template for all elements
    @template(pattern="*", priority=1)
    def general_template(node, context):
        tag_name = getattr(node, "tag", "unknown")
        content = value_of(node)
        return html(t"""<div class="general" data-tag="{tag_name}">{content}</div>""")

    # Specific template for important elements (higher priority)
    @template(pattern="important", priority=10)
    def important_template(node, context):
        content = value_of(node)
        return html(t"""<div class="important highlighted">{content}</div>""")

    # Create test data
    mixed_data = Element(
        tag="container",
        children=[
            Element(tag="normal", children=[Text("Regular content")]),
            Element(tag="important", children=[Text("Important content")]),
            Element(tag="other", children=[Text("Other content")]),
        ],
    )

    return apply_templates(mixed_data)


if __name__ == "__main__":
    # Run examples and print results
    print("=== Person Transformation ===")
    result1 = example_person_transformation()
    print(str(result1))

    print("\n=== Hierarchical List ===")
    result2 = example_hierarchical_list()
    print(str(result2))

    print("\n=== Mode-based Processing ===")
    result3 = example_mode_based_processing()
    print(str(result3))

    print("\n=== Priority-based Templates ===")
    result4 = example_priority_based_templates()
    print(str(result4))
