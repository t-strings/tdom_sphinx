"""
Example usage of the aria_testing library.
"""

from tdom.processor import html
from tdom_sphinx.aria_testing import (
    get_by_text, query_by_text,
    get_by_role, get_by_test_id,
)


def example_usage():
    # Create a sample tdom structure using t-strings
    document = html(t"""<div>
        <h1>Welcome to My App</h1>
        <nav>
            <ul>
                <li><a href="/home">Home</a></li>
                <li><a href="/about">About</a></li>
            </ul>
        </nav>
        <main>
            <p>Hello, world!</p>
            <form>
                <input type="text" placeholder="Enter your name" data-testid="name-input" />
                <button type="submit">Submit</button>
            </form>
        </main>
        <footer>
            <p>© 2024 My App</p>
        </footer>
    </div>""")

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

    # Example 6: Text matching
    greeting = query_by_text(document, "Hello, world!")
    print(f"Found greeting: {greeting.tag if greeting else 'None'}")  # p

    print("All examples completed successfully!")


if __name__ == "__main__":
    example_usage()