"""TdomSafe: MarkupSafe functionality using tdom node trees.

A tdom-based equivalent of MarkupSafe that operates on node trees instead of strings,
providing HTML escaping and safety features while maintaining the structural benefits
of working with parsed DOM trees.
"""

from .core import (
    SafeNode,
    escape_node,
    safe_node,
    unescape_node,
    # MarkupSafe compatibility
    Markup,
    escape,
    escape_silent,
)
from .walker import NodeWalker
from .escaping import EscapeWalker, UnescapeWalker

__all__ = [
    # Core functionality
    "SafeNode",
    "escape_node",
    "safe_node",
    "unescape_node",
    # MarkupSafe compatibility
    "Markup",
    "escape",
    "escape_silent",
    # Advanced usage
    "NodeWalker",
    "EscapeWalker",
    "UnescapeWalker",
]