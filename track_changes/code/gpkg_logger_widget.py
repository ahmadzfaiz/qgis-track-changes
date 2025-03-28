import logging
from PyQt5.QtWidgets import QDockWidget
from qgis.core import QgsMessageLog, Qgis, QgsProject
from qgis.gui import QgsFileWidget

from ..ui.gpkg_logger import Ui_SetupTrackingChanges

class FeatureLogger(QDockWidget, Ui_SetupTrackingChanges):
    """Feature to log GeoPackage vector data changes"""
    def __init__(self):
        super().__init__()
        # Setup UI
        self.ui = Ui_SetupTrackingChanges()
        self.ui.setupUi(self)

        # Logger info setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.gpkg_file = None

        self.app_version = Qgis.QGIS_VERSION
        project = QgsProject.instance()
        self.author = project.metadata().author()
        self.connected = False

        self.layer = None
        self.layer_name = None

    def get_gpkg_path(layer):
        """Retrieve the GeoPackage path from the active layer."""
        if layer and layer.providerType() == "ogr":
            return layer.dataProvider().dataSourceUri().split("|")[0]
        return None

    # def logger_setup(self):
    #     if self.logger.hasHandlers():
    #         for handler in self.logger.handlers:
    #             if isinstance(handler, logging.FileHandler):
    #                 handler.close()
    #         self.logger.handlers.clear() 
        
    #     # Set up new file handler
    #     file_handler = logging.FileHandler(self.log_file, mode="a")
    #     formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    #     file_handler.setFormatter(formatter)
    #     self.logger.addHandler(file_handler)