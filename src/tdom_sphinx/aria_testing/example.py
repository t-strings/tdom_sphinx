"""
Example usage of the aria_testing library.
"""

from tdom import Element, Text
from aria_testing import (
    get_by_text, query_by_text,
    get_by_role, get_by_test_id,
)


def example_usage():
    # Create a sample tdom structure
    document = Element("div", children=[
        Element("h1", children=[Text("Welcome to My App")]),
        Element("nav", children=[
            Element("ul", children=[
                Element("li", children=[
                    Element("a", attrs={"href": "/home"}, children=[Text("Home")])
                ]),
                Element("li", children=[
                    Element("a", attrs={"href": "/about"}, children=[Text("About")])
                ])
            ])
        ]),
        Element("main", children=[
            Element("p", children=[Text("Hello, world!")]),
            Element("form", children=[
                Element("input", attrs={
                    "type": "text",
                    "placeholder": "Enter your name",
                    "data-testid": "name-input"
                }),
                Element("button", attrs={"type": "submit"}, children=[Text("Submit")])
            ])
        ]),
        Element("footer", children=[
            Element("p", children=[Text("© 2024 My App")])
        ])
    ])

    # Example 1: Find by text content
    heading = get_by_text(document, "Welcome to My App")
    print(f"Found heading: {heading.tag}")  # h1

    # Example 2: Find by role
    navigation = get_by_role(document, "navigation")
    print(f"Found navigation: {navigation.tag}")  # nav

    main_content = get_by_role(document, "main")
    print(f"Found main: {main_content.tag}")  # main

    submit_button = get_by_role(document, "button")
    print(f"Found button: {submit_button.tag}")  # button

    # Example 3: Find by test ID
    name_input = get_by_test_id(document, "name-input")
    print(f"Found input: {name_input.attrs['type']}")  # text

    # Example 4: Query (doesn't throw if not found)
    nonexistent = query_by_text(document, "Not found")
    print(f"Nonexistent element: {nonexistent}")  # None

    # Example 5: Find heading by level
    title = get_by_role(document, "heading", level=1)
    print(f"Found h1: {title.tag}")  # h1

    # Example 6: Substring matching
    greeting = query_by_text(document, "Hello", exact=False)
    print(f"Found greeting: {greeting.tag if greeting else 'None'}")  # p

    print("All examples completed successfully!")


if __name__ == "__main__":
    example_usage()