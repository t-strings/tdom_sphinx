"""Helpers for URL and path functions."""

from itertools import repeat
from pathlib import PurePosixPath
from typing import Optional

from tdom import Node

ROOT = PurePosixPath("/")
ROOT_PATHS = ("/", "/index", PurePosixPath("/"), PurePosixPath("/index"))


def relative_path(
    current: PurePosixPath,
    target: PurePosixPath,
    static_prefix: Optional[PurePosixPath] = None,
) -> PurePosixPath:
    """Calculate a dotted path from a source to destination.

    Relative paths are hard.
    Lots of edge cases, lots of configurable policies.
    This function is the innermost logic, which presumes lots of complexity is
    handled before stuff gets passed in.

    Themester's logic is based on Python's ``PurePosixPath``: a virtual hierarchy that is sort of
    like the filesystem, but not actually tied to a filesystem.
    References to documents in the site and static assets are done as these virtual pure paths.
    Static asset references are "normalized" at definition time to be relative to a configurable site root.

    Both ``current`` and ``target`` are expected to start with a slash.
    It doesn't matter if it does or doesn't end with a slash.

    This function doesn't care about whether folders should get ``/index`` added to their path.
    In fact, it doesn't understand folders.
    It expects the path to include ``index`` when the current or target is a collection of some kind.

    Policies handled before this is called:

    - Adding '/index' to current/target if it is a collection

    - Adding a configurable suffix such as ``index.html``

    - Converting a resource to a path

    - Detecting a resource is a collection and should get ``index`` added to path

    Args:
        current: Source from which target is relative, with leading slash
        target: Destination, with leading slash
        static_prefix: Path to insert between dots and target

    Returns:
        The path to the target.

    Raises:
        ValueError: Trying to get an invalid path.
    """
    if not current.is_absolute():
        str_current = str(current)
        m = f"Source path {str_current!r} must start with a slash"
        raise ValueError(m)

    if static_prefix is None and not target.is_absolute():
        str_target = str(target)
        m = f"Target path {str_target!r} must start with a slash"
        raise ValueError(m)

    # Do an optimization...bail out immediately if the same, but make
    # it relative
    if current == target:
        return PurePosixPath(current.name)

    # noinspection PyTypeChecker
    current_parents = iter(current.parents)
    target_parents = target.parents

    result: Optional[PurePosixPath] = None
    hops = -1

    while True:
        try:
            result = next(current_parents)
            hops += 1
            if result in target_parents:
                raise StopIteration()
        except StopIteration:
            break

    # What is the "leftover" part of target?
    remainder_parts = target.relative_to(str(result))

    # How many hops up to go
    prefix = PurePosixPath("/".join(repeat("..", hops)))

    # Join it all together
    if static_prefix is None:
        v = prefix.joinpath(remainder_parts)
    else:
        v = prefix.joinpath(static_prefix, remainder_parts)
    return v


def normalize(item: PurePosixPath | str) -> PurePosixPath:
    """Convert current or target to a PurePosixPath.

    The relative function below liberally accepts a PurePosixPath, ResourceLike, or str for current/target.
    Convert to PurePosixPath.

    Args:
         item: The object to make into a "normalized" PurePosixPath.

    Returns:
         The target path.

    Raises:
        ValueError: Sending an item that isn't a known type.
    """
    # Quick convenience check, root always results in PurePosixPath('/index')
    if item in ROOT_PATHS:
        return PurePosixPath("/index")

    if isinstance(item, PurePosixPath):
        normalized_item = item
    # elif hasattr(item, "parent"):
    #     # Crappy way to check if something is a ResourceLike
    #     normalized_item = resource_path(cast(Resource, item))
    #     if isinstance(item, Mapping):
    #         # Add /index
    #         normalized_item = normalized_item / "index"
    elif isinstance(item, str):
        # Presume it is a string conforming to the path rules, though it
        # might be a non-resource object (no parent)
        normalized_item = PurePosixPath(item)
    else:
        msg = f"Cannot normalize {item}"
        raise ValueError(msg)

    return normalized_item


def relative(
    current: PurePosixPath | str,
    target: PurePosixPath | str,
    static_prefix: Optional[PurePosixPath] = None,
    suffix: Optional[str] = None,
) -> PurePosixPath:
    """Get a path but with all the framework policies on the way in/out.

    As mentioned in ``relative_path``, there are parts of the logic that it doesn't handle.
    It expects everything to be "normalized": PurePosixPaths on both sides, no concept of ``index`` for folders,
    no configurable ``.html`` suffix.
    This function does those things.

    Args:
        current: The resource, path, or string for the source.
        target: The resource, path, or string for destination.
        static_prefix: If resolving a static asset, provide this.
        suffix: If resolving a resource, provide a file extension.

    Returns:
        The path to the target.
    """
    # Normalize to a PurePosixPath
    normalized_current = normalize(current)
    normalized_target = normalize(target)

    # Are we resolving a static resource?
    if static_prefix is None:
        value = relative_path(
            normalized_current,
            normalized_target,
        )
        if suffix is not None:
            value = value.with_suffix(suffix)
    else:
        value = relative_path(
            normalized_current,
            ROOT,
            static_prefix=static_prefix,
        )
        value = value / normalized_target
    return value


def relative_tree(target_node: Node, current: PurePosixPath) -> None:
    """Rewrite certain URL-bearing attributes in a tdom tree relative to current.

    Acts on these cases:
    - In the <head>, for any <link> element with an ``href`` attribute,
      replace its value with a path made relative to ``current`` using ``relative``.
    - In the <body>, for any <a> element with an ``href`` attribute,
      replace its value with a path made relative to ``current`` using ``relative``.

    This function mutates the provided tree in-place and returns nothing.
    """

    def walk(node: object, in_head: bool = False, in_body: bool = False) -> None:
        # Detect an element-like node by duck-typing the attributes we need
        tag = getattr(node, "tag", None)
        attrs = getattr(node, "attrs", None)

        now_in_head = in_head or (tag == "head")
        now_in_body = in_body or (tag == "body")

        if now_in_head and tag == "link" and isinstance(attrs, dict):
            href = attrs.get("href")
            if isinstance(href, str) and href.startswith("/"):
                # Compute relative path string and assign back
                attrs["href"] = str(relative(current=current, target=href))

        if tag == "a" and isinstance(attrs, dict):
            href = attrs.get("href")
            if isinstance(href, str) and href.startswith("/"):
                attrs["href"] = str(relative(current=current, target=href))

        # Recurse into children if present
        children = getattr(node, "children", None)
        if isinstance(children, (list, tuple)):
            for ch in children:
                walk(ch, now_in_head, now_in_body)

    walk(target_node)
