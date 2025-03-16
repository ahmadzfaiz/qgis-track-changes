import os
from PyQt5.QtCore import Qt
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .setup_widget import FeatureLogger
from .about_widget import AboutWidget

class TrackChangesPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        """Create the menu action and toolbar button."""
        # Setup Tracking Action
        self.action = QAction(QIcon(self.get_icon_path("../icon.png")), "Setup tracking", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        
        # About Action
        self.about_action = QAction(QIcon(self.get_icon_path("../ui/info.png")), "About", self.iface.mainWindow())
        self.about_action.triggered.connect(self.about)

        # Add to QGIS menu
        self.iface.addPluginToMenu("Track Changes", self.action)
        self.iface.addPluginToMenu("Track Changes", self.about_action)  # Add "About" menu item

        # Add toolbar button
        self.iface.addToolBarIcon(self.action)


    def unload(self):
        """Remove the menu action and toolbar button."""
        self.iface.removePluginMenu("&Track Changes", self.action)
        self.iface.removeToolBarIcon(self.action)
        self.action = None

    def run(self):
        """Open the UI dialog."""
        if self.dialog is None:
            self.dialog = FeatureLogger()
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dialog)
            return

        # Toggle visibility
        self.dialog.setVisible(not self.dialog.isVisible())

    def about(self):
        """Show the About dialog."""
        dialog = AboutWidget(self.iface.mainWindow())  # Use AboutWidget
        dialog.exec_()  # Show the dialog

    def get_icon_path(self, path):
        """Return the absolute path to the plugin icon."""
        return os.path.join(os.path.dirname(__file__), path)
