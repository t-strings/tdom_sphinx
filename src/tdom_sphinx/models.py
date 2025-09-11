from dataclasses import dataclass
from typing import Protocol

from sphinx.application import (
    BuildEnvironment as SphinxBuildEnvironment,
)
from sphinx.application import (
    Config as SphinxConfig,
)
from sphinx.application import (
    Sphinx,
)


class _FunctionView(Protocol):
    def __call__(self, context: dict) -> str: ...


class _ClassView(Protocol):
    def __init__(self, context: dict): ...

    def render(self) -> str: ...


View = _FunctionView | _ClassView


@dataclass
class TdomContext:
    app: Sphinx
    config: SphinxConfig
    environment: SphinxBuildEnvironment
    page_context: dict
