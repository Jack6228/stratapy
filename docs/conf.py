import os, sys
# Add path to the package
sys.path.insert(0, os.path.abspath('../'))

# -- Project information -----------------------------------------------------

project = 'stratapy'
copyright = '2026, Jack Lee Smith, Christina Antoniou, Ruaridh Alexander'
author = 'Jack Lee Smith, Christina Antoniou, Ruaridh Alexander'
release = '0.9.1'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',  # Pulls docstrings from code
    # 'sphinx.ext.viewcode', # Adds links to source code
    'sphinx.ext.napoleon', # Supports Google/NumPy docstring styles
    'sphinx_design',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme' # Clean, modern look
html_logo = '_static/stratapy_horizontal.png'  # Path to your logo file
html_theme_options = {
    'logo_only': True,  # Use logo only, no text
}
html_sidebars = {
    '**': [
        'globaltoc.html',  # Global table of contents
        'relations.html',  # Next/prev links
        'searchbox.html',  # Search box
    ]
}
html_static_path = ['_static']
html_css_files = ['styles.css']
html_favicon = '_static/stratapy_icon.png'  # Path to your favicon file
#html_extra_path = ['examples'] # Include CSV files in the build
