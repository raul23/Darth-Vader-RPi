# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../darth_vader_rpi'))

# -- Project information -----------------------------------------------------
from darth_vader_rpi import __version__

project = 'Darth-Vader-RPi'
copyright = '2020, Raul C.'
author = 'Raul C.'

# The full version, including alpha/beta/rc tags
release = __version__
version = __version__


# -- General configuration ---------------------------------------------------

# The master toctree document.
master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme'
]

autodoc_mock_imports = ['dv_sounds', 'pygame', 'SimulRPi']

# This value controls the docstrings inheritance. Default is True.
# Ref.: https://bit.ly/2ofNvGi
# autodoc_inherit_docstrings = False
napoleon_google_docstring = False
# If False, no cross-referencing with Python types
napoleon_use_param = True
napoleon_use_ivar = True

source_suffix = '.rst'
# source_suffix = ['.rst', '.md']

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'pygame': ('https://www.pygame.org/docs', None),
    'python': ('https://docs.python.org/3', None),
    'simulrpi': ('https://simulrpi.readthedocs.io/en/latest', None)
    # 'pyutils': ('https://py-common-utils.readthedocs.io/en/latest', None)
}

extlinks = {'simulapi': ('https://simulrpi.readthedocs.io/en/latest/'
                         'api_reference.html#%s', '')}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['test*.rst']

# The default options for autodoc directives. They are applied to all autodoc
# directives automatically.
# Ref.: https://bit.ly/2mt4jsP
autodoc_default_options = {
    # 'private-members': True,
    # 'inherited-members': True
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

"""
def setup(app):
    app.add_stylesheet('css/custom.css')
"""
