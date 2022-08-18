# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

project = 'SSS'
copyright = '2022, Cheng Ren, Aziza Mirsaidova, Priyana Patel, Hector Sosa, Bryna Hazelton'
author = 'Cheng Ren, Aziza Mirsaidova, Priyana Patel, Hector Sosa, Bryna Hazelton'
release = '0.1'

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath("../sss/"))
readme_file = os.path.join(os.path.abspath("../../"), "README.md")
index_file = os.path.join(os.path.abspath("../source/"), "index.rst")
computer_setup_in = os.path.join(os.path.abspath("../"), "computer_setup.md")
computer_setup_out = os.path.join(os.path.abspath("../source/"), "computer_setup.rst")

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

def build_custom_docs(app):
    sys.path.append(os.getcwd())
    try:
        import make_index, make_computer_setup
    except:
        from source import make_index, make_computer_setup

    make_index.write_index_rst(readme_file=readme_file, write_file=index_file)
    make_computer_setup.write_computer_setup_rst(input_file=computer_setup_in, write_file=computer_setup_out)


def setup(app):
    app.connect("builder-inited", build_custom_docs)