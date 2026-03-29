Advanced Plotting
=====================================

This section covers some advanced plotting techniques in stratapy, including custom figure layouts, correlated logs, and subplots of logs. This functionality allows for more complex visualisations and tailored presentations of stratigraphic data, while still being accessible to users with varying levels of programming experience.

Two built-in functions enable the contents of all logs to be placed into a single figure with a shared legend and other useful display options (e.g. vertical alignment and shared axes), which is particularly useful for complex figures with multiple logs. The sections below provide examples of how to use these functions effectively, and how ``matplotlib`` can be used to create custom figure layouts with additional panels for complementary data.

.. :doc:`correlated_logs` explains how to create side-by-side stratigraphic logs, including those shown with a shared y-axis, with a range of customisation options. For example, you can show logs taken from different locations or depths, on the same scale, use a common reference scale to show relative changes, or even ...

.. .. figure:: Profile_Background.jpg
..    :alt: Correlated Logs Example
..    :align: right
..    :width: 300px
   
..    Example of correlated logs with shared y-axis

.. :doc:`multi_fig` demonstrates how to create more custom subplot arrangements of logs, allowing for the comparison of multiple logs in a single figure. This is particularly useful for visualising many logs, each with their own axes, in a compact and informative way.

.. .. figure:: Profile_Background.jpg
..    :alt: Subplots of Logs Example
..    :align: right
..    :width: 300px
   
..    Example of subplots of multiple logs

.. Finally, :doc:`custom_figure_layouts` provides guidance on how to use ``matplotlib`` to create multi-panel figures with stratigraphic logs, complimentary data, and other elements. This is useful for creating detailed and informative figures that combine multiple aspects of your data, like the figure shown here.

.. .. figure:: Profile_Background.jpg
..    :alt: Custom Figure Layouts Example
..    :align: right
..    :width: 300px
   
..    Example of a custom figure layout with stratigraphic logs and additional data

.. grid:: 3

     .. grid-item-card:: Correlated Logs
        :link: correlated_logs.html
        :link-type: url
   
        Vertically align multiple logs with a shared legend

     .. grid-item-card:: Multiple Logs
        :link: multi_fig.html
        :link-type: url

        Plot multiple logs in one figure with a shared legend

     .. grid-item-card:: Custom Layouts
        :link: custom_figure_layouts.html
        :link-type: url
       
        Use Matplotlib to create bespoke figure layouts with logs and other data

.. toctree::
   :maxdepth: 1
   :hidden:

   correlated_logs
   multi_fig
   custom_figure_layouts