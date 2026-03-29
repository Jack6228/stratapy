Lithologies
===========

.. note::
   Run ``sp.update_lithologies(...)`` **before** any plotting.
   Restarting the Python kernel resets lithologies to defaults.

Lithological patterns are customised using a dictionary which is passed to the `sp.update_lithologies()` function.

.. rubric:: What to pass to ``sp.update_lithologies()``

Each entry is:

- **key**: name used in your input file (e.g. in ``rock`` column)
- **value**: ``(pattern, colour, legend_label)``
   - ``pattern`` = existing lithology name (e.g. ``'sandstone'``), image filename (e.g. ``'my_pattern.png'``), or ``''`` (blank) for solid colour fills
   - ``colour`` = hex, named colour, RGB tuple, or RGBA tuple
   - ``legend_label`` = text shown in legend

.. rubric:: Quick Template

.. code-block:: python

   import stratapy as sp

   sp.update_lithologies({
       "input_name": ("pattern_or_image_or_empty", "colour", "Legend Label")
   })

.. rubric:: Solid-fill Lithologies

.. code-block:: python

   import stratapy as sp

   sp.update_lithologies({
       "mud": ("", 'brown', "Mud"),
       "clay": ("", "#A53535", "Clay"),
       "silt": ("", (50, 150, 250), "Silt")
   })

Use ``clay`` in your input file to get a solid red unit with legend label **Clay**. The ``mud`` and ``silt`` entries show how to use named colours and RGB tuples, respectively.

.. rubric:: New Patterned Lithologies

To use an existing pattern with a new colour and/or name, pass the name or key of the pattern as the first element of the tuple, and your chosen colour and legend label as the second and third elements, respectively.

This is particularly useful for using the unnamed patterns.

.. code-block:: python

   import stratapy as sp

   sp.update_lithologies({
       "my_limestone": ('limestone', '#FFD700', 'My New Limestone')
       "packed waste": ('430', 'tan', 'Packed waste'),
   })

Use ``my_limestone`` in your input file to get the sandstone pattern in gold. The ``packed waste`` entry shows how to use one of the built-in unnamed patterns (430) with a new name and colour.

Leaving the colour or name blank will keep the default values, e.g. ``("sandstone", "", "My New Sandstone")`` will give you a new sandstone pattern in the default colour, with a new legend label.

.. rubric:: Custom Images

To use your own custom image, pass the filename of the image as the first element of the tuple, along with its label. The colour element can be ignored. 

.. code-block:: python

   import stratapy as sp

   sp.update_lithologies({
       "custom_lithology": ("my_pattern.png", "", "Custom Lithology")
   })

Image guidance:

- square image recommended (about ``1000 x 1000`` px)
- transparent background preferred (PNG)
- tileable/seamless patterns required

The colour acts as a background behind the image pattern when applicable. Note that custom image functionality is not a thoroughly validated feature of stratapy, and may not behave as expected.