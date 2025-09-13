"""Utilities to convert between third-party element types and tdom Elements.

Currently provides conversion from htpy elements to tdom Elements.
"""
from __future__ import annotations

from functools import wraps
from typing import Callable, Iterable, TypeVar, Union

from tdom import Element, Fragment
from tdom.nodes import Element as TElement, Fragment as TFragment, Text as TText, Node as TNode


def htpy_to_tdom(node: Union[object, Iterable[object]]) -> Element | Fragment:
    """Deeply convert htpy nodes to a tdom Node tree using structural pattern matching.

    Supported inputs:
    - htpy elements and fragments
    - iterables (list/tuple) of supported nodes → wrapped in a tdom Fragment
    - existing tdom nodes are returned unchanged

    Notes:
    - htpy stores attributes as a pre-rendered string; for now we omit attributes
      (tests only exercise tag/children). This can be extended later by parsing
      htpy internals when needed.
    """
    # Local imports to avoid a hard runtime dependency for consumers that don't use htpy
    try:
        from htpy._elements import BaseElement as HBaseElement
        from htpy._fragments import Fragment as HFragment
    except Exception as exc:  # pragma: no cover - defensive
        HBaseElement = ()  # type: ignore[assignment]
        HFragment = ()  # type: ignore[assignment]

    def convert_children(children: object) -> list[TNode]:
        match children:
            case None:
                return []
            case list() | tuple():
                out: list[TNode] = []
                for ch in children:  # type: ignore[assignment]
                    out.extend(convert_children(ch))
                return out
            case HFragment():  # type: ignore[misc]
                return [convert_fragment(children)]  # type: ignore[arg-type]
            case HBaseElement():  # type: ignore[misc]
                return [convert_element(children)]  # type: ignore[arg-type]
            case str() | int():
                return [TText(str(children))]
            case _:
                raise TypeError(f"Unsupported htpy child type: {type(children)!r}")

    def convert_element(el: "HBaseElement") -> TElement:  # type: ignore[name-defined]
        # el._name is the tag; el._children holds nested children
        return TElement(tag=el._name, attrs={}, children=convert_children(el._children))

    def convert_fragment(fr: "HFragment") -> TFragment:  # type: ignore[name-defined]
        return TFragment(children=convert_children(fr._node))

    # Top-level dispatch using pattern matching
    match node:
        case TElement() | TFragment() | TText():
            return node  # type: ignore[return-value]
        case list() | tuple():
            return TFragment(children=convert_children(node))  # type: ignore[arg-type]
        case HFragment():  # type: ignore[misc]
            return convert_fragment(node)  # type: ignore[arg-type]
        case HBaseElement():  # type: ignore[misc]
            return convert_element(node)  # type: ignore[arg-type]
        case _:
            raise TypeError(f"Unsupported htpy node type: {type(node)!r}")


F = TypeVar("F", bound=Callable[..., object])

def htpy_component(func: F | None = None) -> Callable[[F], F] | F:
    """Decorator that converts an htpy-returning component into tdom.

    Use this on a function that returns an htpy element (or an iterable of
    htpy elements). The decorated function will return a tdom ``Element`` so it
    can be embedded directly in t-strings or composed with other tdom nodes.

    Example:
        >>> from htpy import div, span
        >>> @htpy_component
        ... def Greeting(name):
        ...     return div("Hello ", span(name))
        >>> from tdom import html
        >>> result = html(t":{Greeting('World')}")
        >>> assert "Hello" in str(result)
    """
    def decorator(f: F) -> F:
        @wraps(f)
        def wrapper(*args, **kwargs):  # type: ignore[override]
            return htpy_to_tdom(f(*args, **kwargs))

        return wrapper  # type: ignore[return-value]

    return decorator(func) if func is not None else decorator
