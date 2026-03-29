Multi-figure Sedimentary Logs
-----------------------------

This figure uses data from Southern Cyprus [1-3] to show the depositional history and incorporates customised lithological patterns, colours, and names. Three sedimentary logs are plotted in a single figure, with a shared legend and consistent formatting.

.. image:: /_static/gallery/SedimentologyLogs.png
    :alt: Multi-figure sedimentary logs
    :align: center
    :width: 600

Code to reproduce this figure:

.. code-block:: python

    sp.update_features({
        'scaphopod': ('', 'trace fossil', 'Scaphopods'),
    })
    sp.update_lithologies( {
        'conglomerate': ('coarse gravel', '', 'Conglomerate'),
        'marl': ('flint clay', '', 'Marl'),
        'crossbedded limestone': ('crossbedded limestone', '', 'Crossbedded grainstone'),
        'aeolianite': ('crossbedded sandstone', '', 'Aeolianite'),
        'limestone': ('limestone', '', 'Grainstone'),
        'packstone': ('629', '', 'Packstone'),
    })

    # Create a list of files to plot
    files = ['examples.Palamakumbura_2018.csv', 'examples.Balmer_2019.csv', 'examples.Antoniou_2025.csv']

    # Use multi_fig to plot the three logs together
    panel = sp.multi_fig(files, nrows=1, ncols=3, figsize=(20, 14), dpi=300, ppi=600, legend_loc='bottom', legend_columns=4, feature_size=.8, sharex=True)

Data used to generate this figure:

These files are built into stratapy, the code above will work without any need to download or specify file paths.

**References**

1. R. N. Palamakumbura, A. H. F. Robertson. Pliocene-Pleistocene sedimentary-tectonic development of the Mesaoria (Mesarya) Basin in an incipient, diachronous collisional setting: facies evidence from the north of Cyprus. **Geol. Mag. 155** 5 997-1022 (2018) `DOI <https://doi.org/10.1017/s0016756816001072>`_.

2. E. M. Balmer, A. H. F. Robertson, I. Raffi, D. Kroon. Pliocene-Pleistocene sedimentary development of the syntectonic Polis graben, NW Cyprus: evidence from facies analysis, nannofossil biochronology and strontium isotope dating. **Geol. Mag. 156** 5 889-917 (2019) `DOI <https://doi.org/10.1017/s0016756818000286>`_.

3. C. Antoniou, A. H. F. Robertson. Middle-Late Pleistocene to Holocene sediments of the Tremithos River and related shallow-marine to non-marine coastal deposits in SE Cyprus: Products of inter-related surface uplift and glacio-eustatic controlled sea-level change. **Sediment. Geol. 486** 106900 (2025) `DOI <https://doi.org/10.1016/j.sedgeo.2025.106900>`_.