# main_plugin.py
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject

class TrackChangesPlugin:
    def __init__(self, iface):
        """Constructor."""
        self.iface = iface
        self.action = None

    def initGui(self):
        """Create menu item in QGIS."""
        self.action = QAction("Track Changes", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("&Track Changes", self.action)

    def unload(self):
        """Remove the menu item when the plugin is disabled."""
        self.iface.removePluginMenu("&Track Changes", self.action)

    def run(self):
        """Run when menu item is clicked."""
        print("Track Changes Plugin activated!")
