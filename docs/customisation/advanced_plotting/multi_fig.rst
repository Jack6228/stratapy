Multi-Panel Logs
================================================

The ``multi_fig()`` function allows you to plot multiple stratigraphic logs in a single figure, each on its own axis, with a shared legend. This is ideal for comparing several logs side-by-side or in a grid, while maintaining individual axes and full customisation for each log. You can provide your own *matplotlib* figure and axes, or let ``multi_fig()`` create them automatically, control whether the logs share y-axes or have independent y-axes, and use all the same legend customisation options as for single logs.

Parameters
----------

**Required:**

- ``files``  
  A list (or other iterable) of file paths to your stratigraphic data files. Each file will be loaded and plotted as a separate log.

**Optional:**

- ``nrows`` and ``ncols``
  The number of rows and columns of axes to create for the logs. By default, a single row of axes is created. You can specify both nrows and ncols to create a custom grid layout (e.g., nrows=2, ncols=3 for a 2x3 grid).
- ``sharey`` and ``sharex``
  If True, all logs will share the same y-axis and/or x-axis limits. This is useful for directly comparing logs on the same scale. By default, each log has its own independent axes.
- ``fig`` and ``axes``
  You can provide your own *matplotlib* figure and axes to use for the logs. If not provided, they will be created automatically based on nrows and ncols.
- ``fig_kwargs``
  A dictionary of keyword arguments to pass to *matplotlib*'s ``plt.subplots()`` function when creating the figure and axes. This allows you to control the overall figure size, layout, and other properties.
- ``**kwargs``  
  Any additional keyword arguments are passed directly to the ``LogObject.plot()`` method or ``sp.load()`` function for each log (see :py:meth:`stratapy.core.LogObject.plot` or :py:meth:`stratapy.core.load` for full details). This allows you to control all aspects of the plot, such as display mode, legend options, font size, figure size, and more.

Examples
--------

.. tab-set::

    .. tab-item:: Default

        Providing a list of files will automatically create a row of figures with a shared legend.

        Here we call the returned item ``panel`` instead of ``log`` since it contains multiple logs. See below for details on the return value and its methods.

        .. code-block:: python

            files = ['examples.multi_log_1.csv', 'examples.multi_log_2.csv', 'examples.multi_log_3.csv', 'examples.multi_log_4.csv', 'examples.multi_log_5.csv', 'examples.multi_log_6.csv']

            # Call multi_fig and adjust the figure size and legend options by passing parameters which are usually passed to LogObject.plot() or sp.load()
            panel = sp.multi_fig(files, figsize=(24, 6), legend_loc='bottom', legend_columns=4)

            # Optionally save the figure
            panel.save('my_figure.png')

        .. image:: /_static/figures/multi_fig_A.png
            :alt: Example of using multi_fig to plot multiple logs in a single figure
            :width: 90%

    .. tab-item:: Custom Layout

        We can also tell the function to create a custom layout of axes, for example a 2x3 grid instead of a single row.

        .. code-block:: python

            files = ['examples.multi_log_1.csv', 'examples.multi_log_2.csv', 'examples.multi_log_3.csv', 'examples.multi_log_4.csv', 'examples.multi_log_5.csv', 'examples.multi_log_6.csv']

            # Request a 2x3 grid of axes, and adjust the figure size accordingly
            panel = sp.multi_fig(files, nrows=2, ncols=3, figsize=(16, 22))

        .. image:: /_static/figures/multi_fig_B.png
            :alt: Controlling the layout of multiple logs using multi_fig
            :width: 50%

    .. tab-item:: Shared Axes

        We can also set all logs to share the same x- and y-axis limits, useful for comparing logs directly against one other.

        Here we also use the 'grainsize' display mode and 'merge' feature mode to show how all formatting and style options are inherited from LogObject.plot().

        .. code-block:: python

            files = ['examples.multi_log_1.csv', 'examples.multi_log_2.csv', 'examples.multi_log_3.csv', 'examples.multi_log_4.csv', 'examples.multi_log_5.csv', 'examples.multi_log_6.csv']

            # Here we use a 2x3 grid, with shared x- and y-axes, as well as use the 'grainsize' display mode
            panel = sp.multi_fig(files, nrows=2, ncols=3, figsize=(16, 22), sharey=True, sharex=True, display_mode='grainsize', feature_mode='merge')

        .. image:: /_static/figures/multi_fig_C.png
            :alt: Using multi_fig to create multiple logs with shared axes
            :width: 50%

.. tip::
  This function automatically provides a legend to encompass all logs, however, if you need more control over the legend or multi-figure plots, you can also use the :py:meth:`stratapy.core.standalone_legend` function to create a standalone legend, or set ``legend=False`` in ``multi_fig()`` to prevent a legend from being created.

Return Value & Methods
----------------------

``multi_fig()`` returns a ``MultiLogObject`` instance, which contains the figure, axes, logs, and legend, as well as a convenient ``.save()`` method to save the figure to a file:

- ``fig``: The *matplotlib* figure object
- ``axes``: List of axes for each log
- ``logs``: List of ``LogObject`` instances for each log
- ``leg``: The legend object.

You can call ``.save(filename)`` on the returned object to save the figure.

.. code-block:: python

    panel = sp.multi_fig(files)
    panel.save('my_multi_log_figure.png')

Special Notes and Quirks
------------------------

- The number of files must be less than or equal to the number of axes created (either automatically or provided by the user). If there are more axes than files, the extra axes will not be displayed.
- All logs must have the same y-axis mode (e.g., all in age, all in depth, or all in height).
- The legend is shared and automatically includes all relevant entries from all logs.
- All formatting and style options are inherited from ``LogObject.plot()`` or ``sp.load()`` and can be passed directly to ``multi_fig()`` for convenience.