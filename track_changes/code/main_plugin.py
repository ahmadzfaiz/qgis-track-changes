import os
from PyQt5.QtCore import Qt
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .default_logger_widget import FeatureLogger
from .about_widget import AboutWidget

class TrackChangesPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.default_log_action = None
        self.default_log_dialog = None
        self.about_action = None

    def initGui(self):
        """Create the menu action and toolbar button."""
        # Setup Tracking Action
        self.default_log_action = QAction(QIcon(self.get_icon_path("../icon.png")), "Setup tracking", self.iface.mainWindow())
        self.default_log_action.triggered.connect(self.run)
        
        # About Action
        self.about_action = QAction(QIcon(self.get_icon_path("../ui/info.png")), "About", self.iface.mainWindow())
        self.about_action.triggered.connect(self.about)

        # Add to QGIS menu
        self.iface.addPluginToMenu("Track Changes", self.default_log_action)
        self.iface.addPluginToMenu("Track Changes", self.about_action)

        # Add toolbar button
        self.iface.addToolBarIcon(self.default_log_action)


    def unload(self):
        """Remove the menu action and toolbar button."""
        self.iface.removePluginMenu("&Track Changes", self.default_log_action)
        self.iface.removePluginMenu("&Track Changes", self.about_action)
        self.iface.removeToolBarIcon(self.default_log_action)
        self.default_log_action = None
        self.about_action = None

    def run(self):
        """Open the UI dialog."""
        if self.default_log_dialog is None:
            self.default_log_dialog = FeatureLogger()
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.default_log_dialog)
            return

        # Toggle visibility
        self.default_log_dialog.setVisible(not self.default_log_dialog.isVisible())

    def about(self):
        """Show the About dialog."""
        dialog = AboutWidget(self.iface.mainWindow())
        dialog.exec_()

    def get_icon_path(self, path):
        """Return the absolute path to the plugin icon."""
        return os.path.join(os.path.dirname(__file__), path)
