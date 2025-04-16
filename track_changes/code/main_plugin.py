import os
from PyQt5.QtCore import Qt
from qgis.PyQt.QtWidgets import QAction
from PyQt5.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .default_logger_widget import FeatureLogger as DefaultFeatureLogger
from .gpkg_logger_widget import FeatureLogger as GpkgFeatureLogger
from .about_widget import AboutWidget
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from qgis.gui import QgsInterface


class TrackChangesPlugin:
    def __init__(self, iface: "QgsInterface") -> None:
        self.iface = iface
        self.toolbar = iface.addToolBar("Track Changes")
        self.default_log_dialog: Optional[DefaultFeatureLogger] = None
        self.gpkg_log_dialog: Optional[GpkgFeatureLogger] = None

    def initGui(self) -> None:
        """Create the menu action and toolbar button."""
        # About Action
        self.about_action = QAction(
            QIcon(self.get_icon_path("../icon.png")), "About", self.iface.mainWindow()
        )
        self.about_action.triggered.connect(self.about)

        # Setup Tracking Action
        self.default_log_action = QAction(
            QIcon(self.get_icon_path("../ui/icon/default.png")),
            "Default tracking",
            self.iface.mainWindow(),
        )
        self.default_log_action.triggered.connect(self.run_default)
        self.gpkg_log_action = QAction(
            QIcon(self.get_icon_path("../ui/icon/gpkg.png")),
            "GeoPackage tracking",
            self.iface.mainWindow(),
        )
        self.gpkg_log_action.triggered.connect(self.run_gpkg)

        # Add to QGIS menu
        self.iface.addPluginToMenu("Track Changes", self.about_action)
        self.iface.addPluginToMenu("Track Changes", self.default_log_action)
        self.iface.addPluginToMenu("Track Changes", self.gpkg_log_action)

        # Add toolbar button
        self.toolbar.addAction(self.about_action)
        self.toolbar.addAction(self.default_log_action)
        self.toolbar.addAction(self.gpkg_log_action)

    def unload(self) -> None:
        """Remove the menu action and toolbar button."""
        self.iface.removePluginMenu("&Track Changes", self.default_log_action)
        self.iface.removePluginMenu("&Track Changes", self.gpkg_log_action)
        self.iface.removePluginMenu("&Track Changes", self.about_action)
        self.iface.removeToolBarIcon(self.default_log_action)
        self.iface.removeToolBarIcon(self.gpkg_log_action)
        self.iface.removeToolBarIcon(self.about_action)
        self.default_log_action = None
        self.gpkg_log_action = None
        self.about_action = None

    def run_default(self) -> None:
        """Open the default logger UI dialog."""
        if self.default_log_dialog is None:
            self.default_log_dialog = DefaultFeatureLogger()
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.default_log_dialog)
            return

        # Toggle visibility
        self.default_log_dialog.setVisible(not self.default_log_dialog.isVisible())

    def run_gpkg(self) -> None:
        """Open the GeoPackage loggerUI dialog."""
        if self.gpkg_log_dialog is None:
            self.gpkg_log_dialog = GpkgFeatureLogger(self.iface)
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.gpkg_log_dialog)
            return

        # Toggle visibility
        self.gpkg_log_dialog.setVisible(not self.gpkg_log_dialog.isVisible())

    def about(self) -> None:
        """Show the About dialog."""
        dialog = AboutWidget(self.iface.mainWindow())
        dialog.exec_()

    def get_icon_path(self, path: str) -> str:
        """Return the absolute path to the plugin icon."""
        return os.path.join(os.path.dirname(__file__), path)
