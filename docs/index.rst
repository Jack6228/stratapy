stratapy Documentation
======================

stratapy is a Python package which enables quick generation and easy visualisation of sedimentary logs (i.e. cores or stratigraphic sections) using stratigraphic data across multiple disciplines. It uses simple excel/csv/txt input files to plot stratigraphic columns, ideal for non-programmers. This package enables geoscientists to efficiently document, analyse, and interpret geological layers at both macro- and micro-scales for research purposes.

The buttons below will take you to the main sections of the documentation, including a quick tutorial to get you started, a customisation guide to show you how to adjust any aspect of your logs, and a reference section with examples for inspiration.

Quick Links
-----------

.. grid:: 2

     .. grid-item-card:: What is Stratapy?
        :link: getting_started/what_is_stratapy.html
        :link-type: url

        Learn what stratapy can do and how it works

     .. grid-item-card:: Installation
        :link: getting_started/installation/index.html
        :link-type: url

        Install stratapy from scratch

.. grid:: 2

     .. grid-item-card:: Tutorial
        :link: getting_started/tutorial/index.html
        :link-type: url

        From zero to your first figure

     .. grid-item-card:: Customisation How-to's
        :link: customisation/customisation_options.html
        :link-type: url

        How to customise any aspect of a log

.. grid:: 2

    .. grid-item-card:: Gallery
       :link: reference/gallery.html
       :link-type: url

       See examples & get inspiration

    .. grid-item-card:: API Reference
        :link: reference/api_reference/index.html
        :link-type: url

        Full details of all functions

.. tip::
   The documentation is complimented with a Jupyter Notebook, which includes interactive versions of the examples and tutorials. You can `download the notebook here <https://github.com/Jack6228/stratapy/blob/main/examples/Tutorial.ipynb>`_, or `use it online through Google Colab <https://colab.research.google.com/github/Jack6228/stratapy/blob/main/examples/Tutorial.ipynb>`_ (more details about Colab :doc:`here <getting_started/installation/online_platforms>`).

Citing stratapy
---------------

:octicon:`cross-reference` If you use stratapy in your research, to create figures, or for any other purpose, please cite the package using the following:

.. epigraph::

   Smith, et al. (2026). stratapy: A Tool for Automated Stratigraphic Log Visualisation. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg
   :alt: DOI badge
   :target: https://doi.org/10.5281/zenodo.XXXXXXX

.. code-block:: none

   @software{smith_stratapy_2026,
      author = {Smith, Jack Lee and Antoniou, Christina and Alexander, Ruaridh},
      title = {{stratapy: A Python tool for automated stratigraphic log visualisation}},
      month = {3},
      year = {2026},
      publisher = {Zenodo},
      version = {v0.9.0},
      doi = {},
      url = {https://github.com/Jack6228/stratapy}
   }

|PyPI| |Docs| |Colab|

.. |PyPI| image:: https://img.shields.io/badge/PyPI-stratapy-FCB001?logo=pypi
   :target: https://pypi.org/project/stratapy/

.. |Docs| image:: https://img.shields.io/badge/ReadTheDocs-latest-8ca1af?logo=readthedocs
   :target: https://stratapy.readthedocs.io/en/latest/?badge=latest

.. |Colab| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/Jack6228/stratapy/blob/main/examples/ManuscriptFigures.ipynb

.. raw:: html

   <br><br><br>

Table of Contents:
------------------

.. toctree::
   :maxdepth: 2
   :caption: GETTING STARTED

   getting_started/what_is_stratapy
   getting_started/installation/index
   getting_started/tutorial/index

.. toctree::
   :maxdepth: 2
   :caption: CUSTOMISATION GUIDE

   customisation/customisation_options
   customisation/legend
   customisation/labels
   customisation/grain_size/index
   customisation/figure_layout
   customisation/additional_elements/index
   customisation/advanced_plotting/index
   customisation/adjusting_assets/index

.. toctree::
   :maxdepth: 2
   :caption: REFERENCE

   reference/gallery
   reference/available_assets
   reference/grainsize_reference
   reference/api_reference/index
   reference/changelog

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`