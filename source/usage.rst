Usage Guide
===========

This section explains how to use QGIS Track Changes.

Basic Usage
-----------
After installation (see :doc:`installation`), you can start using the tool.

### Running the Tool
Run the following command to track changes in a geospatial file:

   ``qgis-track-changes --input my_data.gpkg --output results.json``

Python API
----------
You can also use it in Python:

.. code-block:: python

   from qgis_track_changes import Tracker

   tracker = Tracker()
   changes = tracker.detect_changes("my_data.gpkg")
   print(changes)

Next Steps
----------
- Explore the API reference: :doc:`api`
- Need help? Check the :doc:`faq`
