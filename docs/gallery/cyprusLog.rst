Cyprus' Depositional History
----------------------------

This figure uses data from Southern Cyprus [1] to show the depositional history and incorporates customised lithological patterns, colours, and names.

.. image:: /_static/gallery/CustomisedLog.png
    :alt: Stratigraphic log of Cyprus
    :align: center
    :width: 600

Code to reproduce this figure:

.. code-block:: python

    # Update the lithologies 
    sp.update_lithologies( {
            'ophiolite': ('721', 'dimgray', 'Troodos ophiolite'),
            'bioclastic': ('702', '#FBF4DB', 'Bioclastic calcarenites and marls'),
            'evaporites': ('724', "#9899CD", 'Evaporites'),
            'shallow': ('dolostone', "#B8E5FA", 'Shelf carbonates'),
            'shallowandreef': ('627', "#B8E5FA", 'Shelf carbonates'),
            'marly': ('clay', "#6597CE", 'Marly chalk'),
            'pelagicchalk': ('638', "#6597CE", 'Pelagic chalk'),
            'pelagicchert': ('639', "#6597CE", 'Pelagic chalk and chert'),
            'marls': ('clay', "#CFC0AC", 'Marls'),
            'reefs': ('629', "#2DB772", 'Reefs'),
            'sandstone': ('681', "#B5543E", 'Sandstones'),
    } )

    log = sp.load('examples.Papadimitriou_2018.csv')
    log.plot(ppi=600, display_mode='log', figsize=(4, 14), dpi=300, legend_border=False)

Data used to generate this figure:

These files are built into stratapy, the code above will work without any need to download or specify file paths.

**References**

1. N. Papadimitriou, R. Deschamps, V. Symeou, C. Souque, C. Gorini, F. H. Nader, C. Blanpied. The tectonostratigraphic evolution of Cenozoic basins of the Northern Tethys: The Northern margin of the Levant Basin. **Oil Gas Sci. Technol. 73** 77 (2018) `DOI <https://doi.org/10.2516/ogst/2018085>`_.