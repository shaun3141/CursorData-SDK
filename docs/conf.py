"""Sphinx configuration for CursorData SDK documentation."""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Project information
project = "CursorData SDK"
copyright = "2024-2025, Shaun VanWeelden"
author = "Shaun VanWeelden"
release = "0.1.0"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.doctest",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

# Napoleon settings for NumPy/Google style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
autodoc_mock_imports = []
autodoc_typehints = "description"

# Templates
templates_path = ["_templates"]

# Exclude patterns
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML output - Using PyData Sphinx Theme for modern, expandable navigation
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_show_sourcelink = True
html_title = "CursorData SDK"
html_logo = None
html_favicon = None

# PyData Sphinx Theme options
html_theme_options = {
    "announcement": (
        "<strong>⚠️ Disclaimer:</strong> This is an unofficial project not connected "
        "with or endorsed by AnySphere (Cursor). Use at your own risk."
    ),
    "collapse_navigation": False,  # Keep sidebar sections expanded
    "navigation_depth": 4,  # Show up to 4 levels in sidebar
    "show_toc_level": 3,  # Show 3 levels in TOC
    "navbar_align": "content",
    "show_nav_level": 2,  # Show 2 levels in the sidebar by default
    "navbar_links": [],  # Remove navigation links from header navbar
    "github_url": "https://github.com/shaun3141/CursorData-SDK",
    "footer_start": ["copyright"],
    "footer_center": [],
    "primary_sidebar_end": [],  # Remove extra items from primary sidebar
}

# Add sidebars configuration
html_sidebars = {
    "**": ["sidebar-nav-bs"],
}

# Custom CSS
html_css_files = [
    "custom.css",
]

# Custom JavaScript
html_js_files = [
    "custom.js",
]

# Intersphinx mapping
# Standard library modules all use the main Python docs URL
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Doctest settings
doctest_global_setup = """
try:
    from cursordata import CursorDataClient
except ImportError:
    pass
"""

# Type hints settings
typehints_fully_qualified = False
always_document_param_types = True
typehints_document_rtype = True
typehints_use_rtype = True
typehints_defaults = "comma"

