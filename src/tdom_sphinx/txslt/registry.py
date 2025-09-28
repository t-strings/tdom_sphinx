"""Template registry and context management for TXSLT."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from tdom import Node


@dataclass
class TemplateInfo:
    """Information about a registered template."""

    pattern: str
    function: Callable
    priority: int = 0
    mode: Optional[str] = None

    def matches(self, node: Node, mode: Optional[str] = None) -> bool:
        """Check if this template matches the given node and mode."""
        if self.mode != mode:
            return False
        return self._pattern_matches(node)

    def _pattern_matches(self, node: Node) -> bool:
        """Check if the pattern matches the node."""
        # Basic implementation - match by tag name for Elements
        if hasattr(node, "tag"):
            if self.pattern == "*":
                return True
            return getattr(node, "tag", "") == self.pattern

        # For text nodes, fragments, etc.
        if self.pattern in ("text()", "node()"):
            return True

        return False


@dataclass
class TemplateContext:
    """Context passed to template functions during transformation."""

    variables: Dict[str, Any] = field(default_factory=dict)
    current_node: Optional[Node] = None
    mode: Optional[str] = None
    position: int = 1
    size: int = 1

    def copy(self, **changes: Any) -> TemplateContext:
        """Create a copy of the context with optional changes."""
        new_context = TemplateContext(
            variables=self.variables.copy(),
            current_node=self.current_node,
            mode=self.mode,
            position=self.position,
            size=self.size,
        )
        for key, value in changes.items():
            setattr(new_context, key, value)
        return new_context


class TemplateRegistry:
    """Registry for storing and resolving templates."""

    def __init__(self) -> None:
        self._templates: List[TemplateInfo] = []

    def register(
        self,
        pattern: str,
        function: Callable,
        priority: int = 0,
        mode: Optional[str] = None,
    ) -> None:
        """Register a template function with a pattern."""
        template_info = TemplateInfo(
            pattern=pattern,
            function=function,
            priority=priority,
            mode=mode,
        )
        self._templates.append(template_info)
        # Sort by priority (higher priority first)
        self._templates.sort(key=lambda t: t.priority, reverse=True)

    def find_template(
        self, node: Node, mode: Optional[str] = None
    ) -> Optional[TemplateInfo]:
        """Find the best matching template for a node."""
        for template in self._templates:
            if template.matches(node, mode):
                return template
        return None

    def clear(self) -> None:
        """Clear all registered templates."""
        self._templates.clear()


# Global registry instance
_global_registry = TemplateRegistry()


def get_global_registry() -> TemplateRegistry:
    """Get the global template registry."""
    return _global_registry


def reset_global_registry() -> None:
    """Reset the global template registry (useful for testing)."""
    global _global_registry
    _global_registry = TemplateRegistry()
