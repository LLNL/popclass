import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "popclass"
copyright = "2024, Lawrence Livermore National Laboratory | LLNL-SM-868436"
author = "Lawrence Livermore National Laboratory"
release = "0.1.0"

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.mathjax",
    "sphinxcontrib.bibtex",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

bibtex_bibfiles = ["refs.bib"]
bibtex_reference_style = "author_year"

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
