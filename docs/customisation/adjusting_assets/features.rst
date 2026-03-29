Features
=========================================

These can be customised in the same way as lithologies, using the and ``sp.update_features()`` functions. Again, the function must be called before creating any figures.

For features, an entry in the dictionary is formatted as:

- `key`: the name of the feature to be used in the input file
- `value`: a tuple containing three elements:
    - the type of feature: 'fossil', 'structure', or 'tectonic' (which determines the section of the legend in which the feature appears)
    - a filepath to a custom image (e.g., 'my_feature.png'), or an existing feature's key (e.g., 'normal grading'), to use that feature's image.
    - the name to be displayed in the legend

The example below shows the default mineral and features in our example log, and then updates them using the methods described above.

.. code-block:: python

    sp.update_features( {
        # Renames the default 'normal grading' feature to 'Grading' in the legend
        'normal grading': ('', '', 'Grading'),          
        # Moves the default 'Mollusc' feature to the sedimentary structures group
        'mollusc': ('structure', '', 'Mollusc'),               
        # Moves the default 'Bioturbation (med.)' feature to the fossils group, and re-names to 'Bioturbation'
        'bioturbation medium': ('f', '', 'Bioturbation'),   
        # Creates a new 'Scaphopod' feature using the default trace fossil image and type
        'scaphopod': ('', 'trace fossil', 'Scaphopod'),     
        # Adds a new fossil feature with a custom image and name
        'my_fossil': ('fossil', 'my_fossil.png', 'My Fossil'),
    } )

stratapy will provide insight into any errors in your input, for example, if the file path is incorrect.

.. note::
   Remember to run ``sp.update_features(...)`` **before** any plotting. Restarting the Python kernel resets all customisations to defaults.