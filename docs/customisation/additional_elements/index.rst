Additional Elements
=======================================

Additional functionality can be added to your stratigraphic logs using the methods described below. These methods are called on an existing ``LogObject`` instance after plotting the log, for example:

.. code-block:: python

    import stratapy as sp
    log = sp.load('my_log.csv')
    log.plot()
    log.add_chronostratigraphy()

They enable rapid enhancement of your logs with commonly used features without needing to manually create and position additional axes or elements, such as chronostratigraphy from the International Commission on Stratigraphy, which automatically aligns with your log's age range.

.. grid:: 2

     .. grid-item-card:: Chronostratigraphy
        :link: chronostratigraphy.html
        :link-type: url

         Add chronostratigraphy to your logs

     .. grid-item-card:: Sample Locations
        :link: sample_locations.html
        :link-type: url

         Mark sample locations on the y-axis

.. grid:: 2

     .. grid-item-card:: Text Labels
        :link: text_labels.html
        :link-type: url
   
         Add custom text labels to your logs

     .. grid-item-card:: Twin Y-Axis
        :link: twin_y_axis.html
        :link-type: url

         Add a secondary y-axis to your logs

.. grid:: 2

     .. grid-item-card:: Trend Arrows
        :link: trends.html
        :link-type: url
   
         Use arrows to indicate trends on your logs

     .. grid-item-card:: ...
        :link: twin_y_axis.html
        :link-type: url

         ...

.. toctree::
   :maxdepth: 1
   :hidden:

   chronostratigraphy
   sample_locations
   text_labels
   twin_y_axis
   trends