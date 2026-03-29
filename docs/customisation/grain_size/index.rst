Grain Size
==============================

In stratapy, grain size is represented on the x-axis of a plot. By default, the axis is divided into grain size labels (such as 'fine', or 'f') which are each associated with a numerical value. A range of grain size presets are available (``sedimentary``, ``volcanic``, etc.), which can be used to adjust the grain size markers and their values, but custom labels and values can also be provided to have more control over the display and position of the grain size axis. See :doc:`grain_axis_values` for more information on how to adjust the grain size axis values and labels.

Furthermore, stratapy automatically groups similar grain sizes into brackets for the aforementioned presets, such as 'sand' or 'ash'. This functionality can also be controlled, whether to be removed, or brackets are to be amended or added. See :doc:`grain_axis_brackets` for details and examples on adjusting grain size brackets.

.. grid:: 2

     .. grid-item-card:: Grain Size Axis Control
        :link: grain_axis_values.html
        :link-type: url

        Change grain size axis values and labels

     .. grid-item-card:: Grain Size Brackets
        :link: grain_axis_brackets.html
        :link-type: url

        Add, remove, or adjust grain size brackets

.. image:: /_static/reference/axes_custom_ticks_brackets.png
   :alt: Example of multiple grain size axes with different customisations or presets
   :align: center
   :width: 100%

.. toctree::
   :maxdepth: 1
   :hidden:

   grain_axis_values
   grain_axis_brackets