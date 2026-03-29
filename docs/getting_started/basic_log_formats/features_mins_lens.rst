Features, Minerals & Lenses
====================================================

In the same way we can change the layout of the log, we can also adjust how features, minerals, and lenses are displayed within a log using optional keyword arguments passed to the ``LogObject.plot()`` function. The presence of these elements in a log is determined by the relevant columns of the input file, and the following options allow us to modify how they are displayed.

.. tab-set::

    .. tab-item:: Default

        By default, all features, minerals, and lenses are shown in a column on the right-hand side of the log.

        .. code-block:: python

            import stratapy as sp
            log = sp.load('examples.tutorial.csv')

            # Default layout (grain size x-axis, filled units)
            log.plot()

        .. image:: /_static/figures/Tutorial.png
           :alt: Default Log Layout
           :align: center
           :width: 60%

    .. tab-item:: Semi-merge

        Semi-merge displays minerals and lenses within their respective units, while features remain in the right-hand column.

        .. code-block:: python

            import stratapy as sp
            log = sp.load('examples.tutorial.csv')

            # Semi-merge layout (features in column, minerals and lenses within units)
            log.plot(feature_mode='semi-merge')

        .. image:: /_static/figures/Tutorial_feature_mode_semi-merge.png
           :alt: Semi-merge Log Layout
           :align: center
           :width: 60%

    .. tab-item:: Merge

        Like semi-merge, but features are also displayed within their respective units.

        .. code-block:: python

            import stratapy as sp
            log = sp.load('examples.tutorial.csv')

            # Merge layout (all features, minerals, and lenses within units)
            log.plot(feature_mode='merge')

        .. image:: /_static/figures/Tutorial_feature_mode_merge.png
           :alt: Merge Log Layout
           :align: center
           :width: 60%

    .. tab-item:: Off

        This will prevent all features, minerals, and lenses from being displayed in the log, but will still display them in the legend. This may be useful if you want to manually place such features after plotting. To completely remove them from the log and legend, remove the relevant columns from the input file.

        .. code-block:: python

            import stratapy as sp
            log = sp.load('examples.tutorial.csv')

            # No features, minerals, or lenses displayed
            log.plot(feature_mode='off')

        .. image:: /_static/figures/Tutorial_feature_mode_off.png
           :alt: No Features Log Layout
           :align: center
           :width: 60%

stratapy's customisation parameters can be combined; for example, to create a log with a grainsize layout and semi-merged minerals and lenses, the following code can be used:

.. code-block:: python

    import stratapy as sp
    log = sp.load('examples.tutorial.csv')

    log.plot(display_mode='grainsize', feature_mode='merge')

.. image:: /_static/figures/Tutorial_multiparam.png
   :alt: Grainsize Semi-merge Log Layout
   :align: center
   :width: 60%

The next section, :doc:`Customisation Guide </customisation/customisation_options>`, goes into more detail on all of the customisation parameters available, as well as other customisation options, including figure layout, legends and labels. 

It also demonstrates the capabilities to add additional elements to a log, such as automatic addition of chronostratigraphy, labels, sample locations, and more.