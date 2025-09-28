"""
aria_testing: A Python DOM Testing Library for tdom

This library provides accessibility-focused query functions that work with tdom's
Node, Element, Text, and Fragment types. It follows DOM Testing Library's philosophy:
"The more your tests resemble the way your software is used, the more confidence they can give you."
"""

from .queries import (
    get_by_text,
    query_by_text,
    get_all_by_text,
    query_all_by_text,
    get_by_test_id,
    query_by_test_id,
    get_all_by_test_id,
    query_all_by_test_id,
    get_by_role,
    query_by_role,
    get_all_by_role,
    query_all_by_role,
)
from .utils import get_text_content, normalize_text
from .errors import TestingLibraryError, ElementNotFoundError, MultipleElementsError

__all__ = [
    "get_by_text",
    "query_by_text",
    "get_all_by_text",
    "query_all_by_text",
    "get_by_test_id",
    "query_by_test_id",
    "get_all_by_test_id",
    "query_all_by_test_id",
    "get_by_role",
    "query_by_role",
    "get_all_by_role",
    "query_all_by_role",
    "get_text_content",
    "normalize_text",
    "TestingLibraryError",
    "ElementNotFoundError",
    "MultipleElementsError",
]