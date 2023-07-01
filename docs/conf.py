# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
import importlib.metadata

sys.path.insert(0, os.path.abspath('..'))

project = 'aiocord'
author = 'Exahilosys'
copyright = f'2023, {author}'
release = importlib.metadata.version(project)
version = '.'.join(release.split('.')[:2])

metadata = importlib.metadata.metadata('aiocord')

rst_prolog = """
.. |dsrc| replace:: Source:
"""

extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.extlinks',
    'sphinx_autodoc_typehints',
    'sphinx_paramlinks',
    'sphinx.ext.autosectionlabel'
]

autodoc_typehints = 'signature'

autodoc_member_order = 'bysource'

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True
}

intersphinx_mapping = {
    'python3': ('https://docs.python.org/3', None),
    'aiohttp': ('https://docs.aiohttp.org/en/stable', None),
}

extlinks = {
    'ddoc': ('https://discord.com/developers/docs%s', None)
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

paramlinks_hyperlink_param = 'name'

html_theme = 'basic'

html_static_path = ['_static']

html_css_files = [
    'main.css'
]

pygments_style = 'github-dark'

html_sidebars = {
   '**': ['searchbox.html', 'globaltoc.html']
}

html_show_copyright = False

html_show_sphinx = False

html_theme_options = {
    'globaltoc_includehidden': True,
    'globaltoc_maxdepth': -1
}

html_context = {
    'github_url': metadata['Home-Page']
}