import json
import uuid
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QDockWidget
from qgis.core import QgsMessageLog, Qgis, QgsProject, QgsProviderRegistry, QgsVectorLayer

from ..ui.gpkg_logger import Ui_SetupTrackingChanges

def get_plugin_version():
    from track_changes import __version__
    return __version__

class FeatureLogger(QDockWidget, Ui_SetupTrackingChanges):
    """Feature to log GeoPackage vector data changes"""
    def __init__(self, iface):
        super().__init__()
        # Setup UI
        self.iface = iface
        self.ui = Ui_SetupTrackingChanges()
        self.ui.setupUi(self)

        # GPKG setup
        self.gpkg_path = None
        self.gpkg_conn = None

        # Project configurations
        self.app_version = Qgis.QGIS_VERSION
        project = QgsProject.instance()
        self.author = project.metadata().author()

        # Map Layer
        self.layers = []
        self.layers_table = []
        self.ui.pbRefreshLayers.clicked.connect(self.refresh_maplayers)

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
            if layer_name in self.layers_table:
                self.ui.listGpkgLayers.addItem(f"• {layer_name}")
        self.ui.mQgsLogFile.setFilePath(self.gpkg_path)

    def refresh_maplayers(self):
        """Retrieve the GeoPackage path from the active layer."""
        self.layers = []
        self.layers_table = []
        for layer in QgsProject.instance().mapLayers().values():
            if self.gpkg_path in layer.source():
                table_name = layer.source().split("layername=")[-1].split("|")[0]
                self.layers.append(layer)
                self.layers_table.append(table_name)
        
        self.populate_list_layers()
    
    def on_file_selected(self, file_path):
        if file_path:
            self.gpkg_path = file_path
            self.ui.pbActivate.setEnabled(True)
            self.ui.pbRefreshLayers.setEnabled(True)
            self.active_layer = self.iface.activeLayer()
            self.refresh_maplayers()
    
    def activate(self):
        self.ui.pbActivate.setEnabled(False)
        self.ui.pbDeactivate.setEnabled(True)
        self.ui.pbRefreshLayers.setEnabled(False)
        self.ui.mQgsLogFile.setEnabled(False)

        # Start logging session
        self.gpkg_conn = sqlite3.connect(self.gpkg_path)
        self.gpkg_cursor = self.gpkg_conn.cursor()
        self.create_changelog()
        QgsMessageLog.logMessage(
            f"Activate tracking: {self.gpkg_path}",
            "Track Changes", 
            level=Qgis.Info
        )

        # If no change active layer
        self.active_layer = self.iface.activeLayer()
        self.active_layer_name = self.active_layer.source().split("layername=")[-1].split("|")[0]
        self.connect_actions()
        # If new layer is selected
        self.layer_selection = self.iface.layerTreeView().selectionModel()
        self.layer_selection.selectionChanged.connect(self.on_selected_layer)

    def connect_actions(self):
        # Actions 1*
        self.active_layer.editingStarted.connect(self.log_editing_started)
        self.active_layer.editingStopped.connect(self.log_editing_stopped)
        # Actions 2*
        self.active_layer.selectionChanged.connect(self.log_selection_changed)
        self.active_layer.featureAdded.connect(self.log_feature_added)
        self.active_layer.featureDeleted.connect(self.log_feature_deleted)
        self.active_layer.geometryChanged.connect(self.log_geometry_changed)
        self.active_layer.committedGeometriesChanges.connect(self.log_commited_geometries_changes)

    def disconnect_actions(self, layer):
        # Actions 1*
        layer.editingStarted.disconnect(self.log_editing_started)
        layer.editingStopped.disconnect(self.log_editing_stopped)
        # Actions 2*
        layer.selectionChanged.disconnect(self.log_selection_changed)
        layer.featureAdded.disconnect(self.log_feature_added)
        layer.featureDeleted.disconnect(self.log_feature_deleted)
        layer.geometryChanged.disconnect(self.log_geometry_changed)
        layer.committedGeometriesChanges.disconnect(self.log_commited_geometries_changes)

    def deactivate(self):
        self.ui.pbActivate.setEnabled(True)
        self.ui.pbDeactivate.setEnabled(False)
        self.ui.pbRefreshLayers.setEnabled(True)
        self.ui.mQgsLogFile.setEnabled(True)

        # Stop logging session
        self.gpkg_conn.close()
        QgsMessageLog.logMessage(
            f"Deactivate tracking: {self.gpkg_path}",
            "Track Changes", 
            level=Qgis.Info
        )

        for layer in QgsProject.instance().mapLayers().values():
            if self.gpkg_path in layer.source():
                try:
                    self.disconnect_actions(layer)
                except Exception:
                    pass

    def on_selected_layer(self, selected, deselected):
        """Triggered when clicking a layer in the Layers Panel"""
        try:
            self.disconnect_actions(self.active_layer)
        except Exception:
            pass
        selected_layers = self.iface.layerTreeView().selectedLayers()
        for layer in selected_layers:
            if (
                isinstance(layer, QgsVectorLayer)
                and self.gpkg_path in layer.source()
            ):
                self.active_layer = layer
                self.active_layer_name = self.active_layer.source().split("layername=")[-1].split("|")[0]
                self.connect_actions()

    def create_changelog(self):
        self.gpkg_cursor.execute("""
            CREATE TABLE IF NOT EXISTS gpkg_changelog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_version TEXT NOT NULL DEFAULT '0.0.0',
                data_version_id TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                change_code INT NOT NULL,
                author TEXT NOT NULL,
                qgis_version TEXT,
                layer_name TEXT,
                feature_id INTEGER,
                message TEXT,
                data JSON,
                qgis_trackchanges_version TEXT
            )
        """)
        self.gpkg_conn.commit()

    def log_editing_started(self):
        self.logging_data(10, None, "start editing", None)

    def log_editing_stopped(self):
        self.logging_data(11, None, "stop editing", None)

    def log_selection_changed(self):
        for feature in self.active_layer.selectedFeatures():
            fid = feature.id()
            feature = self.active_layer.getFeature(fid)
            properties = {}
            attributes = feature.attributes()
            for idx, field in enumerate(self.active_layer.fields()):
                properties[field.name()] = attributes[idx]
            properties["geometry"] = feature.geometry().asWkt()
            self.logging_data(20, fid, "selecting feature", json.dumps(properties))

    def log_feature_added(self, fid):
        feature = self.active_layer.getFeature(fid)
        properties = {}
        attributes = feature.attributes()
        for idx, field in enumerate(self.active_layer.fields()):
            properties[field.name()] = attributes[idx]
        properties["geometry"] = feature.geometry().asWkt()
        self.logging_data(21, fid, "add feature", json.dumps(properties))

    def log_feature_deleted(self, fid):
        self.logging_data(22, fid, "delete feature", None)

    def log_geometry_changed(self, fid, geometry):
        properties = {"new_geometry": geometry.asWkt()}
        self.logging_data(23, fid, "geometry change", json.dumps(properties))
    
    def log_commited_geometries_changes(self, lid, geometries):
        geoms = [{"fid": fid, "geometry": geom.asWkt()} 
                 for fid, geom in geometries.items()]
        self.logging_data(26, None, "commit geometry change", json.dumps(geoms))

    def logging_data(self, change_code, feature_id, message, data):
        self.gpkg_cursor.execute("""
            SELECT 
                data_version, 
                data_version_id 
            FROM gpkg_changelog 
            ORDER BY id DESC 
            LIMIT 1;
        """)
        latest_record = self.gpkg_cursor.fetchone()
        if latest_record is not None:
            data_version = latest_record[0] 
            data_version_id = latest_record[1]
        else:
            data_version = "0.0.0" 
            data_version_id = uuid.uuid4().hex

        self.gpkg_cursor.execute("""
            INSERT INTO gpkg_changelog (
                data_version, 
                data_version_id, 
                timestamp, 
                change_code,
                author, 
                qgis_version, 
                layer_name, 
                feature_id, 
                message, 
                data, 
                qgis_trackchanges_version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
                data_version,
                data_version_id,
                datetime.now(),
                change_code,
                self.author,
                self.app_version,
                self.active_layer_name,
                feature_id,
                message,
                data,
                get_plugin_version()
            )
        )
        self.gpkg_conn.commit()