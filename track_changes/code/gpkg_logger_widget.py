import logging
import sqlite3
from PyQt5.QtWidgets import QDockWidget
from qgis.core import QgsMessageLog, Qgis, QgsProject, QgsProviderRegistry, QgsVectorLayer
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
        self.gpkg_path = None
        self.gpkg_conn = None

        # Project configurations
        self.app_version = Qgis.QGIS_VERSION
        project = QgsProject.instance()
        self.author = project.metadata().author()

        # Map Layer
        self.layers = []
        self.ui.pbRefreshLayers.clicked.connect(self.refresh_maplayers)
        self.connected = False

        # Setup GPKG file for storing changelog
        self.ui.mQgsLogFile.setFilter("GeoPackage (*.gpkg)")
        self.ui.mQgsLogFile.fileChanged.connect(self.on_file_selected)

        # Activate/deactivate track changes
        self.ui.pbActivate.clicked.connect(self.activate)
        self.ui.pbDeactivate.clicked.connect(self.deactivate)

        # Initially disable buttons
        self.ui.pbActivate.setEnabled(False)
        self.ui.pbDeactivate.setEnabled(False)
        self.ui.pbRefreshLayers.setEnabled(False)

    def populate_list_layers(self):
        self.ui.listGpkgLayers.clear()
        provider = QgsProviderRegistry.instance().providerMetadata("ogr")
        conn = provider.createConnection(self.gpkg_path, {})
        layers = conn.tables()
        for layer in layers:
            layer_name = layer.tableName()
            if layer_name in self.layers:
                self.ui.listGpkgLayers.addItem(f"• {layer_name}")
        self.ui.mQgsLogFile.setFilePath(self.gpkg_path)

    def refresh_maplayers(self):
        """Retrieve the GeoPackage path from the active layer."""
        self.layers = []
        for layer in QgsProject.instance().mapLayers().values():
            if layer.providerType() == "ogr" and ".gpkg" in layer.source():
                table_name = layer.source().split("layername=")[-1].split("|")[0]
                self.layers.append(table_name)
        
        self.populate_list_layers()
        print(self.layers)
    
    def on_file_selected(self, file_path):
        if file_path:
            self.gpkg_path = file_path
            self.ui.pbActivate.setEnabled(True)
            self.ui.pbRefreshLayers.setEnabled(True)
            self.refresh_maplayers()
    
    def activate(self):
        self.ui.pbActivate.setEnabled(False)
        self.ui.pbDeactivate.setEnabled(True)
        self.ui.pbRefreshLayers.setEnabled(False)

        # Start logging session
        self.gpkg_conn = sqlite3.connect(self.gpkg_path)
        self.gpkg_cursor = self.gpkg_conn.cursor()
        self.create_changelog()
    
    def deactivate(self):
        self.ui.pbActivate.setEnabled(True)
        self.ui.pbDeactivate.setEnabled(False)
        self.ui.pbRefreshLayers.setEnabled(True)

        # Stop logging session
        self.gpkg_conn.close()

    def create_changelog(self):
        self.gpkg_cursor.execute("""
            CREATE TABLE IF NOT EXISTS changelog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_version TEXT NOT NULL DEFAULT '0.0.0',
                data_version_id TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                change_code TEXT NOT NULL,
                author TEXT NOT NULL,
                qgis_version TEXT,
                layer_name TEXT,
                feature_id INTEGER,
                message TEXT,
                data TEXT
            )
        """)
        self.gpkg_conn.commit()