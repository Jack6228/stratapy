Available Assets
================

This page lists the lithologies, minerals, and features available by default in stratapy. Each tab in the display below highlights the available options. 

Display options (like lithology colours, mineral colours and shapes, and custom features), as well as the names of all assets, can be customised. See :doc:`Adjusting Assets <../customisation/adjusting_assets/index>` for more details.

.. tab-set::

    .. tab-item:: Lithologies   

        **Lithological Patterns**

        Each swatch is shown with its black and white version on the top, and a default coloured version on the bottom, with the latter accessed using the key or name of the swatch, suffixed with an asterisk e.g., ``603*`` or ``724*``. As mentioned above, additional swatches can be created, either using existing patterns with different colours and names, or by using custom images - see :doc:`Adjusting Assets <../customisation/adjusting_assets/index>` for details.

        .. image:: /_static/reference/Lithologies.png
            :alt: USGS lithologies
            :width: 90%
            
        .. raw:: html

            <br><br>

        **Other Patterns**

        Also able to be coloured and modified, but no default coloured versions are provided. These patterns are accessed using the numerical keys, unless custom names are assigned.

        .. image:: /_static/reference/Patterns.png
            :alt: USGS patterns
            :width: 90%

    .. tab-item:: Minerals

        Mineral names are case insensitive.

        .. image:: /_static/reference/Minerals.png
            :alt: Available minerals
            :width: 90%

    .. tab-item:: Features

        Feature keys used in the input file are case insensitive, but the display names are always shown in title case, as seen in the figure. Display names of default features can be customised using the ``update_features()`` method, which also enables you to add new features, including custom images.

        **Sedimentary Features**

        .. image:: /_static/reference/Sedimentary_Features.png
            :alt: Available sedimentary features
            :width: 90%
            
        .. raw:: html

            <br><br>

        **Palaeontological Features**

        .. image:: /_static/reference/Palaeontological_Features.png
            :alt: Available palaeontological features
            :width: 90%
            
        .. raw:: html

            <br><br>

        **Tectonic Features**

        .. image:: /_static/reference/Tectonic_Features.png
            :alt: Available tectonic features
            :width: 90%

    .. tab-item:: Bed Contacts

        Specified in the input file.

        .. image:: /_static/reference/ContactTypes.png
            :alt: Available bed contacts
            :width: 90%