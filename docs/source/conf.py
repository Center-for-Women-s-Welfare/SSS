# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

project = "SSS"
copyright = (
    "2022, Cheng Ren, Aziza Mirsaidova, Priyana Patel, Hector Sosa, Bryna Hazelton"
)
author = "Cheng Ren, Aziza Mirsaidova, Priyana Patel, Hector Sosa, Bryna Hazelton"
release = "0.1"

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath("../sss/"))
readme_file = os.path.join(os.path.abspath("../../"), "README.md")
index_file = os.path.join(os.path.abspath("../source/"), "index.rst")

file_base_to_convert = [
    "computer_setup",
    "developer_documentation",
    "user_documentation",
]
doc_files_in = [
    os.path.join(os.path.abspath("../"), fname + ".md")
    for fname in file_base_to_convert
]
doc_files_out = [
    os.path.join(os.path.abspath("../source/"), fname + ".rst")
    for fname in file_base_to_convert
]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_rtd_theme"]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"


def build_custom_docs(app):
    sys.path.append(os.getcwd())
    try:
        import make_index
        import make_doc_rst_files
    except BaseException:
        from source import make_index, make_doc_rst_files

    make_index.write_index_rst(readme_file=readme_file, write_file=index_file)
    make_doc_rst_files.write_rst_files(
        input_files=doc_files_in, write_files=doc_files_out
    )


def setup(app):
    app.connect("builder-inited", build_custom_docs)
