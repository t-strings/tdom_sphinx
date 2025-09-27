# Configuration file for the Sphinx documentation builder.
# See https://www.sphinx-doc.org/en/master/usage/configuration.html
from __future__ import annotations

import os
import sys
from datetime import datetime

# -- Path setup --------------------------------------------------------------
# Add project root to sys.path if extensions or autodoc were needed later.
ROOT = os.path.abspath(os.path.join(__file__, "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# -- Project information -----------------------------------------------------
project = "tdom-sphinx"
author = "pauleveritt"
current_year = datetime.now().year
copyright = f"{current_year}, {author}"

# -- General configuration ---------------------------------------------------
extensions = [
    # Use MyST so we can write documentation in Markdown
    "myst_parser",
    # Register our theme/extension so template bridge and events connect
    "tdom_sphinx",
]

# Source file types: prefer Markdown via MyST, but allow reST too.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# MyST configuration (keep defaults minimal for now)
myst_enable_extensions = [
    # Minimal; add as needed (def_list, colon_fence, etc.)
    "colon_fence",
]

# -- Options for HTML output -------------------------------------------------
# Our package registers the theme name as "tdom-theme"
html_theme = "tdom-theme"

# Keep warnings strict-ish for docs without blocking local work
suppress_warnings = [
    # Avoid noise if no _static/_templates
    "epub.unknown_project_files",
]

pygments_style = "sphinx"
