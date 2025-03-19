API Reference
=============

This section documents the core API of QGIS Track Changes.

Tracker Log Format
------------------
The tracker log will look like this: 
`<asc_time> - <level_name> - <tracking_code> | <messages>`

- `asc_time`: ASCII timestamp format used in logging. Example: `2025-03-19 12:34:56,789`
- `level_name`: Log level name such as INFO, ERROR, WARNING etc.
- `tracking_code`: Unique code per event of data change.

Tracking Code
-------------

.. list-table:: Tracking Log Codes
   :header-rows: 1
   :widths: 20 40 20

   * - Code
     - Explanation
     - Status
   * - 00
     - Activate layer track change
     - ✅ Live
   * - 01
     - Deactivate layer track change
     - ✅ Live
   * - 10
     - Start editing
     - ✅ Live
   * - 11
     - Stop editing
     - ✅ Live
   * - 20
     - Features selection
     - ✅ Live
   * - 21
     - Feature add
     - ✅ Live
   * - 22
     - Feature delete
     - ✅ Live
   * - 23
     - Feature geometry change
     - ✅ Live
   * - 24
     - Feature add committed
     - ⚠️ Reserved
   * - 25
     - Feature delete committed
     - ⚠️ Reserved
   * - 26
     - Features geometry change committed
     - ✅ Live
   * - 30
     - Attribute add
     - ✅ Live
   * - 31
     - Attribute delete
     - ✅ Live
   * - 32
     - Attribute value change
     - ✅ Live
   * - 33
     - Attribute add committed
     - ✅ Live
   * - 34
     - Attribute delete committed
     - ✅ Live
   * - 35
     - Attribute values change committed
     - ✅ Live


More API details coming soon!

Next Steps
----------
- Learn how to use the tool: :doc:`usage`
- Contribute to the project: :doc:`contributing`
