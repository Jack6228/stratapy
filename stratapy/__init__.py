"""
stratapy: A Python package for stratigraphic plotting and analysis.

Documentation: https://stratapy.readthedocs.io/en/latest/

Publication: https://doi.org/10.1038/s41598-026-58501-2

Authors: Jack Lee Smith, Christina Antoniou, Ruaridh Alexander
"""

__all__ = ['update_minerals', 'update_lithologies', 'update_features', 'update_contacts', 'load', 'chronostratigraphy', 'multi_fig', 'correlated_logs', 'standalone_legend', 'list_examples']
__version__ = '1.0.1'
__author__ = 'Jack Lee Smith, Christina Antoniou, Ruaridh Alexander'
__license__ = 'BSD 3-Clause License'
__copyright__ = 'Copyright (c) 2026 Jack Lee Smith'
__description__ = 'A tool for automated stratigraphic log visualisation'
__url__ = 'https://stratapy.readthedocs.io/en/latest/'

from .core import *