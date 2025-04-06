import json
import uuid
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QDockWidget, QListWidgetItem, QMessageBox
from qgis.core import QgsMessageLog, Qgis, QgsProject, QgsProviderRegistry, QgsVectorLayer, QgsWkbTypes
from ..ui.gpkg_logger import Ui_SetupTrackingChanges
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import QSize

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

        # Message bar
        self.message_bar = self.iface.messageBar()

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

        # Setup icons for different geometry types
        self.geometry_icons = {
            'Point': QIcon(':/images/themes/default/mIconPointLayer.svg'),
            'LineString': QIcon(':/images/themes/default/mIconLineLayer.svg'),
            'Polygon': QIcon(':/images/themes/default/mIconPolygonLayer.svg'),
            'MultiPoint': QIcon(':/images/themes/default/mIconPointLayer.svg'),
            'MultiLineString': QIcon(':/images/themes/default/mIconLineLayer.svg'),
            'MultiPolygon': QIcon(':/images/themes/default/mIconPolygonLayer.svg'),
            'NoGeometry': QIcon(':/images/themes/default/mIconTableLayer.svg')
        }

        # Set smaller icon size for the list widget
        self.ui.listGpkgLayers.setIconSize(QSize(16, 16))

        # Add timer for connection health check
        self.check_timer = QtCore.QTimer()
        self.check_timer.timeout.connect(self.check_connection_health)
        self.check_timer.setInterval(60000)  # Check every minute

    def populate_list_layers(self):
        self.ui.listGpkgLayers.clear()
        provider = QgsProviderRegistry.instance().providerMetadata("ogr")
        conn = provider.createConnection(self.gpkg_path, {})
        layers = conn.tables()
        
        for layer in layers:
            layer_name = layer.tableName()
            if layer_name in self.layers_table:
                # Get the layer from project to determine its geometry type
                gpkg_layer = QgsVectorLayer(f"{self.gpkg_path}|layername={layer_name}", layer_name, "ogr")
                geom_type = gpkg_layer.geometryType()
                
                # Create list item with appropriate icon
                item = QListWidgetItem()
                item.setText(layer_name)
                
                # Set icon based on geometry type
                if geom_type == QgsWkbTypes.PointGeometry:
                    item.setIcon(self.geometry_icons['Point'])
                elif geom_type == QgsWkbTypes.LineGeometry:
                    item.setIcon(self.geometry_icons['LineString'])
                elif geom_type == QgsWkbTypes.PolygonGeometry:
                    item.setIcon(self.geometry_icons['Polygon'])
                else:
                    item.setIcon(self.geometry_icons['NoGeometry'])
                
                self.ui.listGpkgLayers.addItem(item)
                
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
    
    def show_info(self, message, level=Qgis.Info, duration=5):
        """Show message in QGIS message bar"""
        self.message_bar.pushMessage("Track Changes", message, level=level, duration=duration)

    def activate(self):
        self.ui.pbActivate.setEnabled(False)
        self.ui.pbDeactivate.setEnabled(True)
        self.ui.pbRefreshLayers.setEnabled(False)
        self.ui.mQgsLogFile.setEnabled(False)

        # Enable editing all gpkg layers
        for layer in self.layers:
            layer.setReadOnly(False)

        # Start logging session with timeout
        self.gpkg_conn = sqlite3.connect(self.gpkg_path, timeout=30)
        self.gpkg_cursor = self.gpkg_conn.cursor()
        self.create_changelog()
        
        # Show activation message
        self.show_info(f"Track Changes activated for: {self.gpkg_path}")
        
        # disable initial layer selected
        try:
            self.iface.layerTreeView().currentLayerChanged.disconnect(self.on_initial_selected_layer)
        except Exception:
            pass

        # If new layer is selected
        self.layer_selection = self.iface.layerTreeView().selectionModel()
        self.layer_selection.selectionChanged.connect(self.on_selected_layer)
        
        # Reconnect actions to the current active layer
        current_layer = self.iface.activeLayer()
        if current_layer and isinstance(current_layer, QgsVectorLayer) and self.gpkg_path in current_layer.source():
            # Make sure to disconnect any existing handlers first
            try:
                self.disconnect_actions(current_layer)
            except Exception:
                pass
                
            self.active_layer = current_layer
            self.active_layer_name = self.active_layer.source().split("layername=")[-1].split("|")[0]
            self.connect_actions()

        self.check_timer.start()

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

        # Check for any layers in editing mode
        editing_layers = []
        for layer in QgsProject.instance().mapLayers().values():
            if self.gpkg_path in layer.source() and layer.isEditable():
                editing_layers.append(layer)

        # If there are layers being edited, show prompt
        if editing_layers:
            reply = QMessageBox.question(
                self,
                "Save Changes",
                "There are layers with unsaved changes. Do you want to save them?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )

            if reply == QMessageBox.Cancel:
                # User cancelled deactivation
                self.ui.pbActivate.setEnabled(False)
                self.ui.pbDeactivate.setEnabled(True)
                self.ui.pbRefreshLayers.setEnabled(False)
                self.ui.mQgsLogFile.setEnabled(False)
                return
            
            for layer in editing_layers:
                if reply == QMessageBox.Save:
                    if layer.commitChanges():
                        self.show_info(f"Changes saved for layer: {layer.name()}")
                    else:
                        self.show_info(f"Failed to save changes for layer: {layer.name()}", level=Qgis.Warning)
                else:  # QMessageBox.Discard
                    layer.rollBack()
                    self.show_info(f"Changes discarded for layer: {layer.name()}")

        # Stop logging session
        self.gpkg_conn.close()
        self.show_info(f"Track Changes deactivated for: {self.gpkg_path}")

        for layer in QgsProject.instance().mapLayers().values():
            if self.gpkg_path in layer.source():
                layer.setReadOnly(True)
                try:
                    self.disconnect_actions(layer)
                except Exception:
                    pass

        self.check_timer.stop()

    def on_selected_layer(self, selected, deselected):
        """Triggered when clicking a layer in the Layers Panel"""
        # Disconnect from previous active layer if it exists
        if hasattr(self, 'active_layer') and self.active_layer:
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
            if hasattr(self, 'active_layer') and self.active_layer:
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
        
        # Add indices for frequently queried columns
        self.gpkg_cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_changelog_layer 
            ON gpkg_changelog(layer_name)
        """)
        self.gpkg_cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_changelog_timestamp 
            ON gpkg_changelog(timestamp)
        """)
        self.gpkg_cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_changelog_feature 
            ON gpkg_changelog(feature_id)
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
        if data and not isinstance(data, str):
            try:
                data = json.dumps(data)
            except (TypeError, ValueError) as e:
                self.show_info(f"Invalid data format: {str(e)}", level=Qgis.Warning)
                return
        if not self.gpkg_conn:
            self.show_info("No active database connection", level=Qgis.Warning)
            return
        try:
            self.gpkg_conn.execute("BEGIN")
            self.gpkg_cursor.execute("""
                SELECT data_version, data_version_id 
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
        except sqlite3.Error as e:
            self.show_info(f"Error logging changes: {str(e)}", level=Qgis.Critical)
        except:
            self.gpkg_conn.rollback()
            raise

    def check_connection(self):
        """Check if connection is still valid"""
        if self.gpkg_conn:
            try:
                self.gpkg_conn.execute("SELECT 1")
                return True
            except sqlite3.Error:
                return False
        return False

    def reconnect(self):
        """Attempt to reconnect if connection is lost"""
        try:
            if self.gpkg_conn:
                self.gpkg_conn.close()
            self.gpkg_conn = sqlite3.connect(self.gpkg_path)
            self.gpkg_cursor = self.gpkg_conn.cursor()
            return True
        except sqlite3.Error as e:
            self.show_info(f"Failed to reconnect: {str(e)}", level=Qgis.Critical)
            return False

    def check_connection_health(self):
        """Periodic check of connection health"""
        if not self.check_connection():
            self.show_info("Connection lost, attempting to reconnect...", level=Qgis.Warning)
            if self.reconnect():
                self.show_info("Successfully reconnected")
            else:
                self.show_info("Failed to reconnect to database", level=Qgis.Critical)

    def cleanup(self):
        """Clean up resources when plugin is unloaded"""
        if self.check_timer:
            self.check_timer.stop()
        if self.gpkg_conn:
            try:
                self.gpkg_conn.close()
            except sqlite3.Error:
                pass

    def wait_for_database(self, timeout=30):
        """Wait for database to become available"""
        start_time = datetime.now()
        while (datetime.now() - start_time).seconds < timeout:
            try:
                self.gpkg_conn.execute("SELECT 1")
                return True
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    QtCore.QThread.msleep(100)
                    continue
                raise
        return False

    def verify_changelog_structure(self):
        """Verify that changelog table has correct structure"""
        try:
            self.gpkg_cursor.execute("""
                SELECT sql FROM sqlite_master 
                WHERE type='table' AND name='gpkg_changelog'
            """)
            table_sql = self.gpkg_cursor.fetchone()
            if table_sql:
                # Table exists, verify columns
                self.gpkg_cursor.execute("PRAGMA table_info(gpkg_changelog)")
                columns = {row[1] for row in self.gpkg_cursor.fetchall()}
                required_columns = {
                    'id', 'data_version', 'data_version_id', 'timestamp',
                    'change_code', 'author', 'qgis_version', 'layer_name',
                    'feature_id', 'message', 'data', 'qgis_trackchanges_version'
                }
                if not required_columns.issubset(columns):
                    QgsMessageLog.logMessage(
                        "Changelog table structure is invalid",
                        "Track Changes",
                        level=Qgis.Critical
                    )
                    return False
            return True
        except sqlite3.Error as e:
            QgsMessageLog.logMessage(
                f"Error verifying changelog structure: {str(e)}",
                "Track Changes",
                level=Qgis.Critical
            )
            return False