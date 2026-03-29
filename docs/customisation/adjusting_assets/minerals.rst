Minerals
=========================================

Similarly to lithologies and features, for minerals, an entry in the dictionary is formatted as follows:

- `key`: the name of the mineral to be used in the input file
- `value`: a tuple containing three elements:
    - fill colour (e.g., '#FFFF00', 'yellow', (1,1,0))
    - edge colour
    - marker shape

Note that for minerals, the display name is the title case of the key.

.. code-block:: python

    sp.update_minerals( {
        # Magenta diamond with black edge - overrides default garnet style
        'garnet': ('#FF00FF', 'k', 'd'),
        # Orange circle with brown edge - new mineral
        'honeystone': ('orange', 'brown', 'o'),
    } )


A full list of available marker shapes can be found in the Matplotlib documentation `here <https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers>`_.

.. note::
   Remember to run ``sp.update_minerals(...)`` **before** any plotting. Restarting the Python kernel resets all customisations to defaults.