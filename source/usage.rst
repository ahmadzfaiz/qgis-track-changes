Usage Guide
===========

This section explains how to use QGIS Track Changes.

Initialize Track Changes
------------------------
1. After installation (see :doc:`installation`), you can start using the tool. The plugin should appear in **Plugin > Track Changes > Setup tracking**

   .. image:: _static/images/usage1_1.png
      :width: 600
      :alt: tracking button in Plugin menu

2. You also can find this plugin icon in the toolbar to initialize

   .. image:: _static/images/usage1_2.png
      :width: 300
      :alt: tracking button on toolbar

3. After initialized, a new panel will appear in the botom left of your QGIS

   .. image:: _static/images/usage1_3.png
      :width: 400
      :alt: Tracking changes in QGIS panel

Start Tracking Changes
----------------------

1. Add *log file destination* in file browser, name a log file. Example: `test.log`.

   .. image:: _static/images/usage2_1.png
      :width: 600
      :alt: Add log file destination

2. Select the layer that need to be tracked.

   .. image:: _static/images/usage2_2.png
      :width: 400
      :alt: Select vector layer

3. If your layer is not available yet in the list, click "Refresh Layers" button.

   .. image:: _static/images/usage2_3.png
      :width: 400
      :alt: Refresh vector layer

4. Activate the track changes by clicking "Activate" button. When activated, name of your tracked vector file will be appear below the button.

   .. image:: _static/images/usage2_4.png
      :width: 400
      :alt: Activate vector layer tracking

5. Only one layer can be tracked, if you want to track another layer e.g. `polygon` then you need to deactivate it first and change the layer.
6. Now you can track all the changes on the layer like add new feature, change attribute data, fix the geometry etc. and it's logged into your log file.

Next Steps
----------
- Explore the API reference: :doc:`api`
- Need help? Check the :doc:`faq`
