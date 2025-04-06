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
        self.layer_table_fields = {}
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
        self.layer_table_fields = {}
        for layer in QgsProject.instance().mapLayers().values():
            if self.gpkg_path in layer.source():
                layer.setReadOnly(True)
                table_name = layer.source().split("layername=")[-1].split("|")[0]
                self.layers.append(layer)
                self.layers_table.append(table_name)

                # Ad-hoc layer field names
                self.layer_table_fields[table_name] = [
                    {"name": field.name(), "type": field.displayType()} 
                    for field in layer.fields()
                ]
        self.populate_list_layers()

        # Get actual gpkg fields
        self.commited_layer_table_fields = {}
        for layer_name in self.layers_table:
            gpkg_layer = QgsVectorLayer(f"{self.gpkg_path}|layername={layer_name}", layer_name, "ogr")
            self.commited_layer_table_fields[layer_name] = [
                {"name": field.name(), "type": field.displayType()}
                for field in gpkg_layer.fields()
            ]
    
    def on_file_selected(self, file_path):
        if file_path:
            self.gpkg_path = file_path
            self.ui.pbRefreshLayers.setEnabled(True)
            self.active_layer = self.iface.activeLayer()
            self.refresh_maplayers()

        # Initialize activate
        self.iface.layerTreeView().currentLayerChanged.connect(self.on_initial_selected_layer)
    
    def activate(self):
        self.ui.pbActivate.setEnabled(False)
        self.ui.pbDeactivate.setEnabled(True)
        self.ui.pbRefreshLayers.setEnabled(False)
        self.ui.mQgsLogFile.setEnabled(False)

        # Enable editing all gpkg layers
        for layer in self.layers:
            layer.setReadOnly(False)

        # Start logging session
        self.gpkg_conn = sqlite3.connect(self.gpkg_path)
        self.gpkg_cursor = self.gpkg_conn.cursor()
        self.create_changelog()
        QgsMessageLog.logMessage(
            f"Activate tracking: {self.gpkg_path}",
            "Track Changes", 
            level=Qgis.Info
        )
        
        # disable initial layer selected
        try:
            self.iface.layerTreeView().currentLayerChanged.disconnect(self.on_initial_selected_layer)
        except Exception:
            pass

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
        # Action 3*
        self.active_layer.attributeAdded.connect(self.log_attribute_added)
        self.active_layer.attributeDeleted.connect(self.log_attribute_deleted)
        self.active_layer.attributeValueChanged.connect(self.log_attribute_value_changed)
        self.active_layer.committedAttributesAdded.connect(self.log_committed_attributes_added)
        self.active_layer.committedAttributesDeleted.connect(self.log_committed_attributes_deleted)
        self.active_layer.committedAttributeValuesChanges.connect(self.log_committed_attribute_values_changes)

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
        # Action 3*
        layer.attributeAdded.disconnect(self.log_attribute_added)
        layer.attributeDeleted.disconnect(self.log_attribute_deleted)
        layer.attributeValueChanged.disconnect(self.log_attribute_value_changed)
        layer.committedAttributesAdded.disconnect(self.log_committed_attributes_added)
        layer.committedAttributesDeleted.disconnect(self.log_committed_attributes_deleted)
        layer.committedAttributeValuesChanges.disconnect(self.log_committed_attribute_values_changes)

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

    def on_initial_selected_layer(self, layer):
        if (
            isinstance(layer, QgsVectorLayer)
            and self.gpkg_path in layer.source()
        ):
            # Disconnect existing actions
            try:
                self.disconnect_actions(self.active_layer)
            except Exception:
                pass

            # Setup ui and active layer
            self.ui.pbActivate.setEnabled(True)
            self.active_layer = layer
            self.active_layer_name = self.active_layer.source().split("layername=")[-1].split("|")[0]
            
            # Re-connect with new actions
            self.connect_actions()
        else:
            self.ui.pbActivate.setEnabled(False)

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

    def log_attribute_added(self, fid):
        field = self.active_layer.fields()[fid]
        field_object = {"name": field.name(), "type": field.displayType()}
        self.layer_table_fields[self.active_layer_name].append(field_object)
        self.logging_data(30, None, "add field", json.dumps(field_object))

    def log_attribute_deleted(self, fid):
        field = self.layer_table_fields[self.active_layer_name][fid]
        self.logging_data(31, None, "remove field", json.dumps(field))
        self.layer_table_fields[self.active_layer_name].pop(fid)

    def log_attribute_value_changed(self, fid, index, value):
        field = self.layer_table_fields[self.active_layer_name][index]
        att_object = {field["name"]: value}
        self.logging_data(32, fid, "change attribute", json.dumps(att_object))

    def log_committed_attributes_added(self, lid, attributes):
        table_name = lid[:-37]
        att_objects = [
            {"name": field.name(), "type": field.displayType()}
            for field in attributes
        ]
        self.commited_layer_table_fields[table_name].extend(att_objects)
        self.logging_data(33, None, "commit add field", json.dumps(att_objects))

    def log_committed_attributes_deleted(self, lid, attributes):
        table_name = lid[:-37]
        att_objects = []
        for idx in sorted(attributes, reverse=True):
            att_objects.append(self.commited_layer_table_fields[table_name][idx])
            del self.commited_layer_table_fields[table_name][idx]
        self.logging_data(34, None, "commit remove field", json.dumps(att_objects))

    def log_committed_attribute_values_changes(self, lid, attributes):
        table_name = lid[:-37]
        att_objects = []
        for fid, values in attributes.items():
            data = {"fid": fid}
            for cid, value in values.items():
                data[self.layer_table_fields[table_name][cid]["name"]] = value
            att_objects.append(data)
        self.logging_data(35, None, "commit change attribute", json.dumps(att_objects))

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