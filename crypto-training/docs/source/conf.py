# -- Sphinx configuration for Crypto Training docs
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
project = 'Crypto Training'
author = 'Embedded Security Team'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
master_doc = 'index'
html_theme = 'sphinx_rtd_theme'
