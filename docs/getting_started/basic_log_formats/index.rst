Changing the Log Format
=======================

Stratapy has a wide range of customisation options to adjust the appearance and behaviour of your logs. 

One of the main ways to customise logs is to pass different parameters to the ``load()`` and ``plot()`` functions. These parameters allow you to change things like the size, layout, and structure of a log by changing a few words.

The two pages below will introduce this parameter-customisation system using the log created in the tutorial to show two commonly used options for changing the log format, though many more are available.
  - Changing the layout of the log, for example, whether to display grain size, a simple log, or a mixture of both.
  - Adjusting how minerals, features, and lenses are displayed within a log.

.. grid:: 2

     .. grid-item-card:: Log Layout
        :link: log_layout.html
        :link-type: url

        How to change the layout of a log 

     .. grid-item-card:: Features, Minerals, and Lenses
        :link: features_mins_lens.html
        :link-type: url

        Control how features, minerals, and lenses are displayed

The rest of the customisation options available in stratapy are explained in detail throughout the :doc:`Customisation Guide </customisation/customisation_options>`, which includes sections on figure layout, legends and labels, additional elements such as chronostratigraphy and sample locations, and more. Alternatively, for those familiar with Python, the :doc:`API Reference </reference/api_reference/index>` provides a complete list of all available keyword arguments for both the ``sp.load()`` and ``LogObject.plot()`` functions.

.. toctree::
   :maxdepth: 1
   :hidden:
   
   log_layout
   features_mins_lens
