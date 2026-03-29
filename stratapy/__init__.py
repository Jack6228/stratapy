"""
stratapy: A Python package for stratigraphic plotting and analysis.

Documentation: https://stratapy.readthedocs.io/en/latest/

Publication: https://doi.org/...

Authors: Jack Lee Smith, Christina Antoniou, Ruaridh Alexander
"""

__all__ = ['update_minerals', 'update_lithologies', 'update_features', 'load', 'chronostratigraphy', 'multi_fig', 'correlated_logs', 'standalone_legend', 'list_examples']
__version__ = '0.9.0'
__author__ = 'Jack Lee Smith, Christina Antoniou, Ruaridh Alexander'
__license__ = 'BSD 3-Clause License'
__copyright__ = 'Copyright (c) 2026 Jack Lee Smith'
__description__ = 'A tool for automated stratigraphic log visualisation'
__url__ = 'https://stratapy.readthedocs.io/en/latest/'

from .core import *