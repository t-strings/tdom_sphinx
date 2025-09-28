"""
Query functions for finding elements in tdom trees using accessibility patterns.
"""

from typing import Union, Optional, Pattern

from tdom import Node, Element

from .errors import ElementNotFoundError, MultipleElementsError
from .utils import (
    get_text_content,
    matches_text,
    find_elements_by_attribute,
    get_all_elements,
)


# ARIA role mapping based on HTML specification
# This is a simplified version - a full implementation would include all ARIA roles
IMPLICIT_ROLES = {
    'button': ['button'],
    'link': ['a'],
    'heading': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
    'textbox': ['input[type="text"]', 'input[type="email"]', 'input[type="password"]', 'textarea'],
    'checkbox': ['input[type="checkbox"]'],
    'radio': ['input[type="radio"]'],
    'listitem': ['li'],
    'list': ['ul', 'ol'],
    'navigation': ['nav'],
    'main': ['main'],
    'banner': ['header'],
    'contentinfo': ['footer'],
    'complementary': ['aside'],
    'form': ['form'],
    'img': ['img'],
    'table': ['table'],
    'row': ['tr'],
    'cell': ['td', 'th'],
    'columnheader': ['th'],
}


def _get_role_for_element(element: Element) -> Optional[str]:
    """Get the ARIA role for an element, either explicit or implicit."""
    # Check for explicit role attribute
    if 'role' in element.attrs:
        return element.attrs['role']

    # Check for implicit roles based on tag
    tag = element.tag.lower()
    for role, tags in IMPLICIT_ROLES.items():
        if tag in tags:
            return role

    # Special cases for input elements
    if tag == 'input':
        input_type = (element.attrs.get('type') or 'text').lower()
        type_to_role = {
            'button': 'button',
            'submit': 'button',
            'reset': 'button',
            'checkbox': 'checkbox',
            'radio': 'radio',
            'text': 'textbox',
            'email': 'textbox',
            'password': 'textbox',
            'search': 'searchbox',
            'url': 'textbox',
            'tel': 'textbox',
            'number': 'spinbutton',
            'range': 'slider',
        }
        return type_to_role.get(input_type, 'textbox')

    return None


def _get_accessible_name(element: Element) -> str:
    """Get the accessible name for an element."""
    # Check aria-label first
    if 'aria-label' in element.attrs:
        return element.attrs['aria-label'] or ""

    # Check aria-labelledby
    if 'aria-labelledby' in element.attrs:
        # In a real implementation, we'd look up the referenced element
        # For now, just return empty string
        return ""

    # For form controls, check associated label
    if element.tag.lower() in ['input', 'textarea', 'select']:
        # In a real implementation, we'd find the associated label element
        # For now, just use the element's text content
        pass

    # Fall back to text content for most elements
    return get_text_content(element)


# Text-based queries
def query_all_by_text(
    container: Node,
    text: Union[str, Pattern[str]],
    *,
    exact: bool = True,
    normalize: bool = True
) -> list[Element]:
    """
    Find all elements containing the specified text.

    Args:
        container: The container node to search within
        text: Text string or regex pattern to match
        exact: Whether to use exact matching (default) or substring matching
        normalize: Whether to normalize whitespace before matching

    Returns:
        List of matching elements
    """
    # Get all elements within the container, excluding the container itself
    all_elements = get_all_elements(container)
    # Filter out the container element if it's in the results
    if isinstance(container, Element) and all_elements and all_elements[0] is container:
        elements = all_elements[1:]  # Skip the container itself
    else:
        elements = all_elements

    results = []

    for element in elements:
        element_text = get_text_content(element)
        if matches_text(element_text, text, exact=exact, normalize=normalize):
            results.append(element)

    return results


def query_by_text(
    container: Node,
    text: Union[str, Pattern[str]],
    *,
    exact: bool = True,
    normalize: bool = True
) -> Optional[Element]:
    """
    Find a single element containing the specified text.

    Args:
        container: The container node to search within
        text: Text string or regex pattern to match
        exact: Whether to use exact matching (default) or substring matching
        normalize: Whether to normalize whitespace before matching

    Returns:
        The matching element, or None if not found
    """
    elements = query_all_by_text(container, text, exact=exact, normalize=normalize)
    return elements[0] if elements else None


def get_by_text(
    container: Node,
    text: Union[str, Pattern[str]],
    *,
    exact: bool = True,
    normalize: bool = True
) -> Element:
    """
    Find a single element containing the specified text.
    Throws an error if not found or multiple elements match.

    Args:
        container: The container node to search within
        text: Text string or regex pattern to match
        exact: Whether to use exact matching (default) or substring matching
        normalize: Whether to normalize whitespace before matching

    Returns:
        The matching element

    Raises:
        ElementNotFoundError: If no matching element is found
        MultipleElementsError: If multiple elements match
    """
    elements = query_all_by_text(container, text, exact=exact, normalize=normalize)

    if not elements:
        raise ElementNotFoundError(
            f"Unable to find element with text: {text}",
            suggestion="Try using query_by_text if the element might not exist"
        )

    if len(elements) > 1:
        raise MultipleElementsError(
            f"Found multiple elements with text: {text}",
            count=len(elements)
        )

    return elements[0]


def get_all_by_text(
    container: Node,
    text: Union[str, Pattern[str]],
    *,
    exact: bool = True,
    normalize: bool = True
) -> list[Element]:
    """
    Find all elements containing the specified text.
    Throws an error if no elements are found.

    Args:
        container: The container node to search within
        text: Text string or regex pattern to match
        exact: Whether to use exact matching (default) or substring matching
        normalize: Whether to normalize whitespace before matching

    Returns:
        List of matching elements

    Raises:
        ElementNotFoundError: If no matching elements are found
    """
    elements = query_all_by_text(container, text, exact=exact, normalize=normalize)

    if not elements:
        raise ElementNotFoundError(
            f"Unable to find elements with text: {text}",
            suggestion="Try using query_all_by_text if the elements might not exist"
        )

    return elements


# Test ID-based queries
def query_all_by_test_id(
    container: Node,
    test_id: str,
    *,
    attribute: str = "data-testid"
) -> list[Element]:
    """
    Find all elements with the specified test ID.

    Args:
        container: The container node to search within
        test_id: The test ID value to match
        attribute: The attribute name to check (default: "data-testid")

    Returns:
        List of matching elements
    """
    return find_elements_by_attribute(container, attribute, test_id)


def query_by_test_id(
    container: Node,
    test_id: str,
    *,
    attribute: str = "data-testid"
) -> Optional[Element]:
    """
    Find a single element with the specified test ID.

    Args:
        container: The container node to search within
        test_id: The test ID value to match
        attribute: The attribute name to check (default: "data-testid")

    Returns:
        The matching element, or None if not found
    """
    elements = query_all_by_test_id(container, test_id, attribute=attribute)
    return elements[0] if elements else None


def get_by_test_id(
    container: Node,
    test_id: str,
    *,
    attribute: str = "data-testid"
) -> Element:
    """
    Find a single element with the specified test ID.
    Throws an error if not found or multiple elements match.

    Args:
        container: The container node to search within
        test_id: The test ID value to match
        attribute: The attribute name to check (default: "data-testid")

    Returns:
        The matching element

    Raises:
        ElementNotFoundError: If no matching element is found
        MultipleElementsError: If multiple elements match
    """
    elements = query_all_by_test_id(container, test_id, attribute=attribute)

    if not elements:
        raise ElementNotFoundError(
            f"Unable to find element with {attribute}: {test_id}",
            suggestion="Check that the test ID is correct and the element exists"
        )

    if len(elements) > 1:
        raise MultipleElementsError(
            f"Found multiple elements with {attribute}: {test_id}",
            count=len(elements)
        )

    return elements[0]


def get_all_by_test_id(
    container: Node,
    test_id: str,
    *,
    attribute: str = "data-testid"
) -> list[Element]:
    """
    Find all elements with the specified test ID.
    Throws an error if no elements are found.

    Args:
        container: The container node to search within
        test_id: The test ID value to match
        attribute: The attribute name to check (default: "data-testid")

    Returns:
        List of matching elements

    Raises:
        ElementNotFoundError: If no matching elements are found
    """
    elements = query_all_by_test_id(container, test_id, attribute=attribute)

    if not elements:
        raise ElementNotFoundError(
            f"Unable to find elements with {attribute}: {test_id}",
            suggestion="Check that the test ID is correct and elements exist"
        )

    return elements


# Role-based queries
def query_all_by_role(
    container: Node,
    role: str,
    *,
    name: Optional[str] = None,
    level: Optional[int] = None
) -> list[Element]:
    """
    Find all elements with the specified ARIA role.

    Args:
        container: The container node to search within
        role: The ARIA role to match
        name: Optional accessible name to match
        level: Optional heading level (for heading roles)

    Returns:
        List of matching elements
    """
    # Get all elements within the container, excluding the container itself
    all_elements = get_all_elements(container)
    # Filter out the container element if it's in the results
    if isinstance(container, Element) and all_elements and all_elements[0] is container:
        elements = all_elements[1:]  # Skip the container itself
    else:
        elements = all_elements

    results = []

    for element in elements:
        element_role = _get_role_for_element(element)
        if element_role != role:
            continue

        # Check heading level if specified
        if level is not None and role == 'heading':
            if element.tag.lower() == f'h{level}':
                pass  # Matches
            elif 'aria-level' in element.attrs:
                try:
                    aria_level_str = element.attrs['aria-level']
                    if aria_level_str is not None:
                        aria_level = int(aria_level_str)
                        if aria_level != level:
                            continue
                    else:
                        continue
                except ValueError:
                    continue
            else:
                continue

        # Check accessible name if specified
        if name is not None:
            element_name = _get_accessible_name(element)
            if not matches_text(element_name, name, exact=False, normalize=True):
                continue

        results.append(element)

    return results


def query_by_role(
    container: Node,
    role: str,
    *,
    name: Optional[str] = None,
    level: Optional[int] = None
) -> Optional[Element]:
    """
    Find a single element with the specified ARIA role.

    Args:
        container: The container node to search within
        role: The ARIA role to match
        name: Optional accessible name to match
        level: Optional heading level (for heading roles)

    Returns:
        The matching element, or None if not found
    """
    elements = query_all_by_role(container, role, name=name, level=level)
    return elements[0] if elements else None


def get_by_role(
    container: Node,
    role: str,
    *,
    name: Optional[str] = None,
    level: Optional[int] = None
) -> Element:
    """
    Find a single element with the specified ARIA role.
    Throws an error if not found or multiple elements match.

    Args:
        container: The container node to search within
        role: The ARIA role to match
        name: Optional accessible name to match
        level: Optional heading level (for heading roles)

    Returns:
        The matching element

    Raises:
        ElementNotFoundError: If no matching element is found
        MultipleElementsError: If multiple elements match
    """
    elements = query_all_by_role(container, role, name=name, level=level)

    if not elements:
        name_part = f" and name '{name}'" if name else ""
        level_part = f" and level {level}" if level else ""
        raise ElementNotFoundError(
            f"Unable to find element with role '{role}'{name_part}{level_part}",
            suggestion="Check that the role and attributes are correct"
        )

    if len(elements) > 1:
        raise MultipleElementsError(
            f"Found multiple elements with role '{role}'",
            count=len(elements)
        )

    return elements[0]


def get_all_by_role(
    container: Node,
    role: str,
    *,
    name: Optional[str] = None,
    level: Optional[int] = None
) -> list[Element]:
    """
    Find all elements with the specified ARIA role.
    Throws an error if no elements are found.

    Args:
        container: The container node to search within
        role: The ARIA role to match
        name: Optional accessible name to match
        level: Optional heading level (for heading roles)

    Returns:
        List of matching elements

    Raises:
        ElementNotFoundError: If no matching elements are found
    """
    elements = query_all_by_role(container, role, name=name, level=level)

    if not elements:
        name_part = f" and name '{name}'" if name else ""
        level_part = f" and level {level}" if level else ""
        raise ElementNotFoundError(
            f"Unable to find elements with role '{role}'{name_part}{level_part}",
            suggestion="Check that the role and attributes are correct"
        )

    return elements