Bouma Sequence Log
------------------

The Bouma sequence [1] is a classic sedimentary structure that represents the vertical succession of sedimentary layers deposited by turbidity currents at the bottoms of lakes, oceans and rivers.

.. image:: /_static/gallery/bouma.png
    :alt: Bouma sequence log
    :align: center
    :width: 600

Code to reproduce this figure:

.. code-block:: python

    # Update the lithologies 
    sp.update_lithologies( {
        'new_607': ('607', '#E5DC8D', 'Sandstone'), 
        'new_616': ('616', '##C2C0AE', 'Calcareous siltstone'), 
    } )

    log = sp.load('examples.bouma.csv')
    log.plot(figsize=(8, 16), dpi=300, legend_columns=2)

Data used to generate this figure:

This file is built into stratapy, the code above will work without any need to download or specify file paths.

**References**

1. A. H. Bouma. Sedimentology of Some Flysch Deposits: A Graphic Approach to Facies Interpretation. Elsevier, 1962.