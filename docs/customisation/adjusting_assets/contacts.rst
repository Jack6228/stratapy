Contacts
=========================================

Contacts can be customised by passing a dictionary to ``sp.update_contacts()``.
The function must be called before creating any figures.

For contacts, an entry in the dictionary is formatted as follows:

- `key`: the name of the contact to be used in the input file
- `value`: a tuple containing four elements:
    - linewidth, as a numeric value
    - linestyle, which can be any valid Matplotlib linestyle
    - colour, which can be an RGB tuple, a Matplotlib colour string, or a hex code
    - label, which is the name to be displayed in the legend

The key is case-sensitive. Default contacts cannot be modified; if you want a different appearance, use a new key instead.

.. code-block:: python

    sp.update_contacts( {
        # Magenta dashed line - new contact
        'my_contact': (1, 'dashed', 'magenta', 'My Contact'),
        # Orange dash-dot line - new contact
        'another_contact': (1.5, 'dashdot', 'orange', 'Another Contact'),
    } )

Default contacts cannot be edited, but new ones can be added using this method. As with the default contacts, if erosion is specified for a contact, the desired contact will also be displayed as a sinusoidal line on the log.

A full list of available linestyles can be found in the Matplotlib documentation `here <https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html>`_.
A full list of available marker and line styles can be found in the Matplotlib documentation `here <https://matplotlib.org/stable/api/markers_api.html>`_.

.. note::
   Remember to run ``sp.update_contacts(...)`` **before** any plotting. Restarting the Python kernel resets all customisations to defaults.