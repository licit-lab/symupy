# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("."))
# sys.path.insert(0, os.path.abspath("../../symupy/"))

print("DEBUG:: os.cwd")
print(os.getcwd())

print("DEBUG:: sys.path")
print("================")
for item in sys.path:
    print(item)

here = os.path.abspath(os.path.dirname(__file__))
repo_root = os.path.dirname(os.path.dirname(here))
sys.path.insert(0, repo_root)

print("repo_root")
print("=====================")
print(repo_root)

# DEBUG for post insert on RTD
print("DEBUG:: Post insert to sys.path")
print("===============================")
for item in sys.path:
    print(item)

print("ENV: Environment check")
print("===============================")
conda = os.environ.get("CONDA_PREFIX")
print(conda)

# -- Project information -----------------------------------------------------

project = "Symupy"
copyright = "2021, LICIT"
author = "Andres Ladino"

from symupy.utils.constants import DEFAULT_PATH_SYMUFLOW
from symupy import __version__ as symversion

print("LIB: Library Check")
print("===============================")
print(DEFAULT_PATH_SYMUFLOW)

import symupy

# The full version, including alpha/beta/rc tags
release = symversion


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "nbsphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "myst_parser",
    # "recommonmark",
]

# Skipping errors
nbsphinx_allow_errors = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"
html_logo = "_static/logo.png"
html_title = f"v{symversion}"
html_copy_source = True
html_sourcelink_suffix = ""
html_favicon = "_static/logo.png"
html_last_updated_fmt = ""

# Options theme
html_theme_options = {
    "repository_url": "https://github.com/licit-lab/symupy",
    "use_issues_button": True,
    "use_edit_page_button": True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']