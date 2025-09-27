from pathlib import PurePosixPath

import pytest

from tdom_sphinx.url import normalize, relative, relative_path


def test_normalize_root_variants():
    # All root-like inputs normalize to "/index"
    for item in ("/", "/index", PurePosixPath("/"), PurePosixPath("/index")):
        assert normalize(item) == PurePosixPath("/index")


def test_normalize_string_and_path():
    assert normalize("/a/b") == PurePosixPath("/a/b")
    assert normalize("a/b") == PurePosixPath("a/b")
    p = PurePosixPath("/x/y")
    assert normalize(p) is p  # returns the same object for PurePosixPath


def test_normalize_invalid_type_raises_value_error():
    with pytest.raises(ValueError) as exc:
        normalize(123)  # type: ignore[arg-type]
    assert "Cannot normalize 123" in str(exc.value)


def test_relative_path_same_path_returns_name():
    cur = PurePosixPath("/docs/page")
    tgt = PurePosixPath("/docs/page")
    assert relative_path(cur, tgt) == PurePosixPath("page")


def test_relative_path_between_branches():
    cur = PurePosixPath("/a/b/c/index")
    tgt = PurePosixPath("/a/d/e/index")
    assert relative_path(cur, tgt) == PurePosixPath("../../d/e/index")


def test_relative_path_requires_absolute_current():
    cur = PurePosixPath("a/b")
    tgt = PurePosixPath("/a/b")
    with pytest.raises(ValueError) as exc:
        relative_path(cur, tgt)
    assert "must start with a slash" in str(exc.value)


def test_relative_path_requires_absolute_target_without_static_prefix():
    cur = PurePosixPath("/a/b")
    tgt = PurePosixPath("c/d")
    with pytest.raises(ValueError) as exc:
        relative_path(cur, tgt)
    assert "Target path 'c/d' must start with a slash" in str(exc.value)


def test_relative_to_child_no_hops():
    cur = "/a/index"
    tgt = "/a/b/index"
    assert relative(cur, tgt) == PurePosixPath("b/index")


def test_relative_to_parent_multiple_hops():
    cur = "/a/b/c/index"
    tgt = "/a/index"
    assert relative(cur, tgt) == PurePosixPath("../../index")


def test_relative_adds_suffix_when_provided():
    cur = "/a/index"
    tgt = "/a/index"
    assert relative(cur, tgt, suffix=".html") == PurePosixPath("index.html")


def test_relative_static_with_prefix_and_relative_asset():
    cur = "/a/b/c/index"
    static_prefix = PurePosixPath("_static")
    # Asset target should be a relative path to avoid overriding joined prefix
    asset = "css/site.css"
    assert relative(cur, asset, static_prefix=static_prefix) == PurePosixPath(
        "../../../_static/css/site.css"
    )


def test_relative():
    p1 = PurePosixPath("/foo/bar/boo/biz")
    p2 = PurePosixPath("/foo/baz")
    result = relative(p1, p2)
    assert result == PurePosixPath("../../baz")
