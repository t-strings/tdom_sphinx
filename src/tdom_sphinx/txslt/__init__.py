"""TXSLT: T-String XSLT-like transformation language.

A t-string DSL that extends tdom's capabilities to handle recursive descent
and pattern matching transformations similar to XSLT, but with modern Python
syntax and type safety.
"""

from .core import template, apply_templates, select, value_of, copy_of, html
from .registry import TemplateRegistry, TemplateContext
from .patterns import PatternMatcher

__all__ = [
    "template",
    "apply_templates",
    "select",
    "value_of",
    "copy_of",
    "html",
    "TemplateRegistry",
    "TemplateContext",
    "PatternMatcher",
]
