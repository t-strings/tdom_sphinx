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
    container = html(t"""<div>
        <p>duplicate</p>
        <span>duplicate</span>
    </div>""")

    with pytest.raises(MultipleElementsError) as exc_info:
        get_by_text(container, "duplicate")
    assert "Found multiple elements with text: duplicate" in str(exc_info.value)
    # Add type checking for MultipleElementsError instance
    assert isinstance(exc_info.value, MultipleElementsError)
    assert exc_info.value.count == 2


def test_query_all_by_text():
    container = html(t"""<div>
        <p>test</p>
        <span>test</span>
        <div>other</div>
    </div>""")

    elements = query_all_by_text(container, "test")
    assert len(elements) == 2
    assert elements[0].tag == "p"
    assert elements[1].tag == "span"


def test_get_all_by_text_success():
    container = html(t"""<div>
        <p>item</p>
        <span>item</span>
    </div>""")

    elements = get_all_by_text(container, "item")
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
    container = html(t"""<div>
        <button data-testid="action">Button</button>
        <div data-testid="action">Div</div>
    </div>""")

    with pytest.raises(MultipleElementsError):
        get_by_test_id(container, "action")


def test_custom_test_id_attribute():
    container = html(t'<div><button data-qa="submit">Submit</button></div>')

    element = query_by_test_id(container, "submit", attribute="data-qa")
    assert element is not None


def test_query_all_by_test_id():
    container = html(t"""<div>
        <button data-testid="btn">Button</button>
        <input data-testid="btn" type="text" />
    </div>""")

    elements = query_all_by_test_id(container, "btn")
    assert len(elements) == 2


def test_get_all_by_test_id_success():
    container = html(t"""<div>
        <button data-testid="item">Button</button>
        <div data-testid="item">Div</div>
    </div>""")

    elements = get_all_by_test_id(container, "item")
    assert len(elements) == 2


def test_get_all_by_test_id_not_found(sample_document):
    with pytest.raises(ElementNotFoundError):
        get_all_by_test_id(sample_document, "nonexistent")


def test_explicit_role():
    container = html(t'<div><div role="button">Custom button</div></div>')

    element = query_by_role(container, "button")
    assert element is not None


def test_implicit_role_button():
    container = html(t"<div><button>Click me</button></div>")

    element = query_by_role(container, "button")
    assert element is not None
    assert element.tag == "button"


def test_implicit_role_heading():
    container = html(t"""<div>
        <h1>Title</h1>
        <h2>Subtitle</h2>
    </div>""")

    elements = query_all_by_role(container, "heading")
    assert len(elements) == 2


def test_heading_with_level():
    container = html(t"""<div>
        <h1>Title</h1>
        <h2>Subtitle</h2>
    </div>""")

    element = query_by_role(container, "heading", level=1)
    assert element is not None
    assert element.tag == "h1"

    element = query_by_role(container, "heading", level=3)
    assert element is None


def test_aria_level_attribute():
    container = html(
        t'<div><div role="heading" aria-level="3">Custom heading</div></div>'
    )

    element = query_by_role(container, "heading", level=3)
    assert element is not None


def test_input_type_roles():
    container = html(t"""<div>
        <input type="text" />
        <input type="checkbox" />
        <input type="button" />
    </div>""")

    textbox = query_by_role(container, "textbox")
    assert textbox is not None
    assert textbox.attrs["type"] == "text"

    checkbox = query_by_role(container, "checkbox")
    assert checkbox is not None
    assert checkbox.attrs["type"] == "checkbox"

    button = query_by_role(container, "button")
    assert button is not None
    assert button.attrs["type"] == "button"


# Note: Role with name parameter not fully implemented yet
# def test_role_with_name():
#     container = html(t"""<div>
#         <button aria-label="Save container">Save</button>
#         <button aria-label="Cancel operation">Cancel</button>
#     </div>""")
#
#     element = query_by_role(container, "button", name="Save")
#     assert element is not None
#     aria_label = element.attrs.get("aria-label")
#     assert aria_label is not None and "Save" in aria_label


def test_get_by_role_success():
    container = html(t"<div><nav>Navigation</nav></div>")

    element = get_by_role(container, "navigation")
    assert element.tag == "nav"


def test_get_by_role_not_found():
    container = html(t"<div><p>Just text</p></div>")

    with pytest.raises(ElementNotFoundError) as exc_info:
        get_by_role(container, "button")
    assert "Unable to find element with role 'button'" in str(exc_info.value)


def test_get_by_role_multiple_elements():
    container = html(t"""<div>
        <button>First</button>
        <button>Second</button>
    </div>""")

    with pytest.raises(MultipleElementsError):
        get_by_role(container, "button")


def test_get_all_by_role_success():
    container = html(t"""<div>
        <li>Item 1</li>
        <li>Item 2</li>
    </div>""")

    elements = get_all_by_role(container, "listitem")
    assert len(elements) == 2


def test_get_all_by_role_not_found():
    container = html(t"<div><p>Just text</p></div>")

    with pytest.raises(ElementNotFoundError):
        get_all_by_role(container, "button")


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
    from tdom import Text

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
    container = html(t"<div><p>Hello <strong>bold</strong> world</p></div>")

    element = query_by_text(container, "Hello bold world")
    assert element is not None
    assert element.tag == "p"


def test_multiple_query_methods_same_element():
    container = html(
        t'<div><button data-testid="submit" aria-label="Submit form">Submit</button></div>'
    )

    # Should find the same element via different methods
    by_text = query_by_text(container, "Submit")
    by_test_id = query_by_test_id(container, "submit")
    by_role = query_by_role(container, "button")

    assert by_text is by_test_id is by_role


def test_fragment_as_container():
    fragment = html(t"<div>First</div><span>Second</span>")

    element = query_by_text(fragment, "First")
    assert element is not None
    assert element.tag == "div"

    elements = query_all_by_text(fragment, "First")
    assert len(elements) == 1


# ===== Name Matching Tests =====


def test_role_with_name_text_content():
    """Test name matching using text content."""
    container = html(t"""<div>
        <button>Save Document</button>
        <button>Cancel Operation</button>
        <button>Delete File</button>
    </div>""")

    # Test substring matching
    element = query_by_role(container, "button", name="Save")
    assert element is not None
    assert "Save Document" in element.children[0].text

    element = query_by_role(container, "button", name="Cancel")
    assert element is not None
    assert "Cancel Operation" in element.children[0].text

    # Test full text matching
    element = query_by_role(container, "button", name="Delete File")
    assert element is not None
    assert "Delete File" in element.children[0].text


def test_role_with_name_aria_label():
    """Test name matching using aria-label."""
    container = html(t"""<div>
        <button aria-label="Save container">💾</button>
        <button aria-label="Cancel operation">❌</button>
        <button aria-label="Delete file">🗑️</button>
    </div>""")

    element = query_by_role(container, "button", name="Save")
    assert element is not None
    assert element.attrs["aria-label"] == "Save container"

    element = query_by_role(container, "button", name="Cancel")
    assert element is not None
    assert element.attrs["aria-label"] == "Cancel operation"


def test_role_with_name_link_text():
    """Test name matching for links using text content."""
    container = html(t"""<div>
        <a href="/docs">Documentation</a>
        <a href="/about">About Us</a>
        <a href="/contact">Contact</a>
    </div>""")

    element = query_by_role(container, "link", name="Documentation")
    assert element is not None
    assert element.attrs["href"] == "/docs"

    element = query_by_role(container, "link", name="About")
    assert element is not None
    assert element.attrs["href"] == "/about"


def test_role_with_name_image_alt():
    """Test name matching for images using alt text."""
    container = html(t"""<div>
        <img src="logo.png" alt="Company Logo" />
        <img src="avatar.jpg" alt="User Avatar" />
        <img src="icon.svg" alt="Settings Icon" />
    </div>""")

    element = query_by_role(container, "img", name="Company")
    assert element is not None
    assert element.attrs["alt"] == "Company Logo"

    element = query_by_role(container, "img", name="Avatar")
    assert element is not None
    assert element.attrs["alt"] == "User Avatar"

    element = query_by_role(container, "img", name="Settings")
    assert element is not None
    assert element.attrs["alt"] == "Settings Icon"


def test_role_with_name_not_found():
    """Test name matching when no element matches."""
    container = html(t"""<div>
        <button>Save</button>
        <button>Cancel</button>
    </div>""")

    element = query_by_role(container, "button", name="Delete")
    assert element is None


def test_role_with_keyword_arguments():
    """Test using keyword arguments with * separator."""
    container = html(t"""<div>
        <h1>Main Title</h1>
        <h2>Subtitle</h2>
        <button>Save Changes</button>
        <button aria-label="Cancel operation">Cancel</button>
    </div>""")

    # Test with keyword arguments
    element = query_by_role(container, "heading", level=1)
    assert element is not None
    assert element.tag == "h1"

    element = query_by_role(container, "button", name="Save")
    assert element is not None
    assert "Save Changes" in element.children[0].text

    element = query_by_role(container, "button", name="Cancel")
    assert element is not None
    assert element.attrs["aria-label"] == "Cancel operation"


def test_get_all_by_role_with_name():
    """Test get_all_by_role with name filtering."""
    container = html(t"""<div>
        <button>Save File</button>
        <button>Save As</button>
        <button>Cancel</button>
        <button>Delete File</button>
    </div>""")

    elements = get_all_by_role(container, "button", name="Save")
    assert len(elements) == 2

    # Both buttons should contain "Save" in their accessible name
    for element in elements:
        text = element.children[0].text
        assert "Save" in text


def test_accessible_name_priority():
    """Test that aria-label takes priority over text content."""
    container = html(t"""<div>
        <button aria-label="Custom Label">Visible Text</button>
    </div>""")

    # Should match aria-label, not text content
    element = query_by_role(container, "button", name="Custom")
    assert element is not None

    # Should not match text content when aria-label is present
    element = query_by_role(container, "button", name="Visible")
    assert element is None


def test_form_controls_name_matching():
    """Test name matching for form controls."""
    container = html(t"""<div>
        <input type="text" placeholder="Enter your name" />
        <input type="email" value="test@example.com" />
        <textarea aria-label="Comments">Default text</textarea>
    </div>""")

    # Match by placeholder
    element = query_by_role(container, "textbox", name="Enter")
    assert element is not None
    assert element.attrs["placeholder"] == "Enter your name"

    # Match by value
    element = query_by_role(container, "textbox", name="test@")
    assert element is not None
    assert element.attrs["value"] == "test@example.com"

    # Match by aria-label (should take priority)
    element = query_by_role(container, "textbox", name="Comments")
    assert element is not None
    assert element.attrs["aria-label"] == "Comments"


# ===== Link Href Support Tests =====

def test_link_name_includes_href():
    """Test that link names include href for comprehensive matching."""
    container = html(t"""<div>
        <a href="/docs">Documentation</a>
        <a href="/api/v1">API Reference</a>
        <a href="https://example.com">External Link</a>
    </div>""")

    # Match by href path
    element = query_by_role(container, "link", name="/docs")
    assert element is not None
    assert element.attrs["href"] == "/docs"

    # Match by href with version
    element = query_by_role(container, "link", name="v1")
    assert element is not None
    assert element.attrs["href"] == "/api/v1"

    # Match by domain in href
    element = query_by_role(container, "link", name="example.com")
    assert element is not None
    assert element.attrs["href"] == "https://example.com"


def test_link_name_text_and_href_combined():
    """Test that both text content and href are searchable for links."""
    container = html(t"""<div>
        <a href="/download">Download Now</a>
        <a href="/signup">Join Today</a>
        <a href="/admin/users">User Management</a>
    </div>""")

    # Match by text content
    element = query_by_role(container, "link", name="Download")
    assert element is not None
    assert "Download Now" in element.children[0].text

    # Match by href path
    element = query_by_role(container, "link", name="/signup")
    assert element is not None
    assert element.attrs["href"] == "/signup"

    # Match by part of href path
    element = query_by_role(container, "link", name="admin")
    assert element is not None
    assert element.attrs["href"] == "/admin/users"

    # Match by text content when href doesn't contain the term
    element = query_by_role(container, "link", name="Join")
    assert element is not None
    assert "Join Today" in element.children[0].text


def test_link_href_only_no_text():
    """Test links with href but no text content."""
    container = html(t"""<div>
        <a href="/home" aria-label="Home Page"></a>
        <a href="/search"><img src="search.png" alt="Search" /></a>
        <a href="/profile">👤</a>
    </div>""")

    # Should match by aria-label, not href (aria-label takes priority)
    element = query_by_role(container, "link", name="Home Page")
    assert element is not None
    assert element.attrs["href"] == "/home"

    # Match by href when containing images (no aria-label)
    element = query_by_role(container, "link", name="/search")
    assert element is not None
    assert element.attrs["href"] == "/search"

    # Match by href when containing emoji/unicode (no aria-label)
    element = query_by_role(container, "link", name="/profile")
    assert element is not None
    assert element.attrs["href"] == "/profile"


def test_link_complex_href_patterns():
    """Test complex href patterns and matching."""
    container = html(t"""<div>
        <a href="https://api.github.com/repos/user/repo">GitHub API</a>
        <a href="mailto:contact@example.com">Contact Us</a>
        <a href="tel:+1-555-123-4567">Call Now</a>
        <a href="#section-1">Jump to Section</a>
        <a href="?page=2&sort=name">Next Page</a>
    </div>""")

    # Match by domain in URL
    element = query_by_role(container, "link", name="github.com")
    assert element is not None
    assert "api.github.com" in element.attrs["href"]

    # Match by email protocol and domain
    element = query_by_role(container, "link", name="mailto:")
    assert element is not None
    assert element.attrs["href"] == "mailto:contact@example.com"

    element = query_by_role(container, "link", name="example.com")
    assert element is not None
    assert "contact@example.com" in element.attrs["href"]

    # Match by phone protocol
    element = query_by_role(container, "link", name="tel:")
    assert element is not None
    assert element.attrs["href"] == "tel:+1-555-123-4567"

    # Match by phone number part
    element = query_by_role(container, "link", name="555")
    assert element is not None
    assert "555" in element.attrs["href"]

    # Match by fragment identifier
    element = query_by_role(container, "link", name="#section")
    assert element is not None
    assert element.attrs["href"] == "#section-1"

    # Match by query parameters
    element = query_by_role(container, "link", name="page=2")
    assert element is not None
    assert "page=2" in element.attrs["href"]


def test_link_priority_aria_label_over_href():
    """Test that aria-label takes priority over href and text for links."""
    container = html(t"""<div>
        <a href="/secret-path" aria-label="Public Label">Hidden Text</a>
    </div>""")

    # Should match aria-label, not href or text
    element = query_by_role(container, "link", name="Public")
    assert element is not None
    assert element.attrs["aria-label"] == "Public Label"

    # Should not match href when aria-label is present
    element = query_by_role(container, "link", name="secret")
    assert element is None

    # Should not match text content when aria-label is present
    element = query_by_role(container, "link", name="Hidden")
    assert element is None


def test_multiple_links_href_matching():
    """Test finding specific links among multiple similar ones using href."""
    container = html(t"""<div>
        <a href="/docs/getting-started">Getting Started</a>
        <a href="/docs/api">API Documentation</a>
        <a href="/docs/examples">Code Examples</a>
        <a href="/blog/getting-started">Blog: Getting Started</a>
    </div>""")

    # Should find the docs version, not the blog version
    element = query_by_role(container, "link", name="/docs/getting")
    assert element is not None
    assert "/docs/getting-started" in element.attrs["href"]

    # Should find the API docs specifically
    element = query_by_role(container, "link", name="docs/api")
    assert element is not None
    assert element.attrs["href"] == "/docs/api"

    # Should distinguish between docs and blog by path
    element = query_by_role(container, "link", name="/blog/")
    assert element is not None
    assert "/blog/" in element.attrs["href"]

    # Get all docs links
    elements = get_all_by_role(container, "link", name="/docs/")
    assert len(elements) == 3
    for element in elements:
        assert "/docs/" in element.attrs["href"]


def test_regex_name_matching():
    """Test regex pattern matching for accessible names."""
    import re

    container = html(t"""<div>
        <button>Save Document</button>
        <button>CANCEL OPERATION</button>
        <button>Delete File</button>
        <a href="/API">API Reference</a>
        <a href="/docs">DOCUMENTATION</a>
    </div>""")

    # Case-insensitive regex for button text
    save_btn = query_by_role(container, "button", name=re.compile(r"save", re.IGNORECASE))
    assert save_btn is not None
    assert "Save Document" in save_btn.children[0].text

    # Regex to match all-caps text
    cancel_btn = query_by_role(container, "button", name=re.compile(r"^[A-Z\s]+$"))
    assert cancel_btn is not None
    assert "CANCEL OPERATION" in cancel_btn.children[0].text

    # Regex for links with case-insensitive matching
    api_link = query_by_role(container, "link", name=re.compile(r"api", re.IGNORECASE))
    assert api_link is not None
    assert api_link.attrs["href"] == "/API"

    # Get all buttons and links with all-caps names
    caps_buttons = query_all_by_role(container, "button", name=re.compile(r"^[A-Z\s]+$"))
    # Links have format "TEXT /href" so pattern needs to account for href part
    caps_links = query_all_by_role(container, "link", name=re.compile(r"^[A-Z\s]+/[A-Za-z]+$"))
    assert len(caps_buttons) == 1  # CANCEL OPERATION
    assert len(caps_links) == 1  # DOCUMENTATION /docs


def test_regex_vs_string_matching():
    """Test that regex and string matching work differently."""
    import re

    container = html(t"""<div>
        <button>save file</button>
        <button>SAVE FILE</button>
        <button>Save Document</button>
    </div>""")

    # String matching is case-sensitive substring
    element = query_by_role(container, "button", name="save")
    assert element is not None
    assert "save file" in element.children[0].text

    # Regex matching with case-insensitive flag matches all
    elements = get_all_by_role(container, "button", name=re.compile(r"save", re.IGNORECASE))
    assert len(elements) == 3

    # Regex for exact word boundaries
    element = query_by_role(container, "button", name=re.compile(r"^save file$", re.IGNORECASE))
    assert element is not None
    # Should match the lowercase one first
    text = element.children[0].text if element.children else ""
    assert text in ["save file", "SAVE FILE"]


def test_regex_with_href_matching():
    """Test regex patterns work with href + text combination for links."""
    import re

    container = html(t"""<div>
        <a href="/api/v1">API v1</a>
        <a href="/api/v2">API v2</a>
        <a href="/docs/api">API Guide</a>
        <a href="/blog">Blog Posts</a>
    </div>""")

    # Regex to match API version links (href contains /api/v)
    api_version_elements = get_all_by_role(container, "link", name=re.compile(r"/api/v\d+"))
    assert len(api_version_elements) == 2

    # Regex case-insensitive matching for "api" in either text or href
    all_api_elements = get_all_by_role(container, "link", name=re.compile(r"api", re.IGNORECASE))
    assert len(all_api_elements) == 3  # All three API-related links

    # Regex for specific version
    v2_element = query_by_role(container, "link", name=re.compile(r"v2"))
    assert v2_element is not None
    assert v2_element.attrs["href"] == "/api/v2"
