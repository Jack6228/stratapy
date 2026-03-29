Customisation Options
===================================

Stratapy offers a vast range of customisation options to suit needs of users from different fields, and of different level of coding familiarity. This section is split into multiple sections, to help you find what you are looking for quickly, including but not limited to:

-   **Figure layout and sizing**: Adjusting the overall figure dimensions, quality, and more
-   **Legends and labels**: Customising the appearance and content of legends and axes labels
-   **Grain size**: Customising the appearance of grain size logs, including brackets, labels, and values
-   **Additional elements**: Adding features such as chronostratigraphy, sample locations, and more to your logs
-   **Customising graphics**: Adjusting the appearance of lithological patterns, minerals, and features, and adding your own custom images
-   **Advanced plotting**: Creating multi-log figures, correlated logs, and bespoke figure layouts

.. tip::
   Examples of all these customisation examples can be explored interactively in the `accompanying Jupyter notebooks <https://github.com/file>`_. The :doc:`Gallery <../reference/gallery>` also includes a range of example logs and figures which can be copied and adapted.

Click on any of the cards below to access the relevant section of examples and explanations.

.. grid:: 2

     .. grid-item-card:: Legends 
        :link: legend.html
        :link-type: url

        Control over legends

     .. grid-item-card:: Labels
        :link: labels.html
        :link-type: url

        Customising axes labels

.. grid:: 2

     .. grid-item-card:: Grain Size 
        :link: grain_size/index.html
        :link-type: url

        Customise grain size values, labels, and brackets
        
     .. grid-item-card:: Figure Layout
        :link: figure_layout.html
        :link-type: url

        Figure dimensions, sizing, resolution, and more

.. In addition to these optional arguments, once a ``LogObject`` is created and plotted, a range of methods are available to further modify and customise the log, each achieved in 1 line of code, and enabling the addition of chronostratigraphy, sample locations, text labels, and more. Each of these methods are explained in detail, with examples, in the :doc:`Additional Elements <customisation/additional_elements/index.html>` section.

.. Three easy-to-use commands in stratapy also allow complete customisation of all lithologies, minerals, and features within stratapy, as well as the opportunity to use your own images and patterns. The :doc:`Adjusting Features <customisation/customising_assets.html>` section provides a step-by-step guide on how to use these commands, along with examples to help you get started. Functionality includes: changing the legend name or colour of lithological patterns; controlling the colour, shape and name of minerals; moving features between legend categories or adding your own images; and changing the size of minerals & features.

For users wanting to create multiple logs within one figure, the :doc:`Advanced Plotting </customisation/advanced_plotting/index>` section provides a comprehensive guide on the ``sp.correlated_logs()`` and ``sp.multi_log()`` functions which automate multi-figure graphics, with examples to help you get started. 

Additionally, for those experienced using ``matplotlib``, this section also includes guidance on how to create completely bespoke figure layouts, and how to integrate stratapy's logs and functions to your own figure designs.

.. The :doc:`API Reference <reference/api_reference.html>` can be consulted for a full list of available keyword arguments for each function, along with their descriptions and default values.

.. grid:: 2

     .. grid-item-card:: Additional Elements
        :link: additional_elements/index.html
        :link-type: url

        Quickly add advanced features like chronostratigraphy or sample locations to your logs

     .. grid-item-card:: Customising Lithologies and other Graphics
        :link: adjusting_assets/index.html
        :link-type: url

        How to customise lithologies, minerals, and features in stratapy

.. grid:: 2

     .. grid-item-card:: Advanced Plotting
        :link: advanced_plotting/index.html
        :link-type: url

        Create multi-log figures, correlated logs, and bespoke layouts

     .. grid-item-card:: API Reference
        :link: reference/api_reference.html
        :link-type: url

        Full details of all functions and their parameters

.. note::
   Looking for a list of available lithologies, minerals, or features in stratapy? :doc:`Available Assets <../reference/available_assets>`