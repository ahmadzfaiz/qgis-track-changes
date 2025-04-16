import json
from typing import Optional, Union
import uuid
import sqlite3
from datetime import datetime, timezone
from PyQt5.QtWidgets import QDockWidget, QListWidgetItem, QMessageBox, QAbstractItemView
from qgis.core import (
    QgsMessageLog,
    Qgis,
    QgsProject,
    QgsProviderRegistry,
    QgsVectorLayer,
    QgsWkbTypes,
    QgsFeature,
    QgsField
)
from ..ui.gpkg_logger import Ui_SetupTrackingChanges
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import QSize


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qgis.gui import QgsInterface


def get_plugin_version() -> str:
    from track_changes import __version__

    return __version__


class FeatureLogger(QDockWidget, Ui_SetupTrackingChanges):
    """Feature to log GeoPackage vector data changes"""
    def __init__(self, iface: 'QgsInterface') -> None:
        super().__init__()
        # Setup UI
        self.iface = iface
        self.ui = Ui_SetupTrackingChanges()
        self.ui.setupUi(self)

        # GPKG setup
        self.gpkg_path: str = ""
        self.connection_timeout = 30  # seconds
        self.max_retries = 3  # Maximum number of retries for database operations
        self.gpkg_conn: Optional[sqlite3.Connection]
        self.gpkg_cursor: Optional[sqlite3.Cursor] = None

        # Project configurations
        self.app_version = Qgis.QGIS_VERSION
        project = QgsProject.instance()
        self.author = project.metadata().author()

        # Message bar
        self.message_bar = self.iface.messageBar()

        # Map Layer
        self.layers: list[QgsVectorLayer] = []
        self.layers_table: list[str] = []
        self.layer_table_fields: dict[str, list] = {}
        self.ui.pbRefreshLayers.clicked.connect(self.refresh_maplayers)

        # Make list widget non-interactive but still show selection
        self.ui.listGpkgLayers.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.listGpkgLayers.setFocusPolicy(QtCore.Qt.NoFocus)

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
            "Point": QIcon(":/images/themes/default/mIconPointLayer.svg"),
            "LineString": QIcon(":/images/themes/default/mIconLineLayer.svg"),
            "Polygon": QIcon(":/images/themes/default/mIconPolygonLayer.svg"),
            "MultiPoint": QIcon(":/images/themes/default/mIconPointLayer.svg"),
            "MultiLineString": QIcon(":/images/themes/default/mIconLineLayer.svg"),
            "MultiPolygon": QIcon(":/images/themes/default/mIconPolygonLayer.svg"),
            "NoGeometry": QIcon(":/images/themes/default/mIconTableLayer.svg"),
        }

        # Set smaller icon size for the list widget
        self.ui.listGpkgLayers.setIconSize(QSize(16, 16))

        # Add timer for connection health check
        self.check_timer: QtCore.QTimer = QtCore.QTimer()
        self.check_timer.timeout.connect(self.check_connection_health) # type: ignore[attr-defined]
        self.check_timer.setInterval(60000)  # Check every minute

    def populate_list_layers(self) -> None:
        self.ui.listGpkgLayers.clear()
        provider = QgsProviderRegistry.instance().providerMetadata("ogr")
        conn = provider.createConnection(self.gpkg_path, {})
        layers = conn.tables()

        for layer in layers:
            layer_name = layer.tableName()
            if layer_name in self.layers_table:
                # Get the layer from project to determine its geometry type
                gpkg_layer = QgsVectorLayer(
                    f"{self.gpkg_path}|layername={layer_name}", layer_name, "ogr"
                )
                geom_type = gpkg_layer.geometryType()

                # Create list item with appropriate icon
                item = QListWidgetItem()
                item.setText(layer_name)

                # Set icon based on geometry type
                if geom_type == QgsWkbTypes.PointGeometry:
                    item.setIcon(self.geometry_icons["Point"])
                elif geom_type == QgsWkbTypes.LineGeometry:
                    item.setIcon(self.geometry_icons["LineString"])
                elif geom_type == QgsWkbTypes.PolygonGeometry:
                    item.setIcon(self.geometry_icons["Polygon"])
                else:
                    item.setIcon(self.geometry_icons["NoGeometry"])

                self.ui.listGpkgLayers.addItem(item)

        self.ui.mQgsLogFile.setFilePath(self.gpkg_path)

    def refresh_maplayers(self) -> None:
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
            gpkg_layer = QgsVectorLayer(
                f"{self.gpkg_path}|layername={layer_name}", layer_name, "ogr"
            )
            self.commited_layer_table_fields[layer_name] = [
                {"name": field.name(), "type": field.displayType()}
                for field in gpkg_layer.fields()
            ]

    def on_file_selected(self, file_path: str) -> None:
        # Reset read-only state for layers from previous GeoPackage
        if hasattr(self, "gpkg_path") and self.gpkg_path:
            old_gpkg_path = self.gpkg_path
            for layer in QgsProject.instance().mapLayers().values():
                if old_gpkg_path in layer.source():
                    layer.setReadOnly(False)  # Reset to default state

        if file_path:
            self.gpkg_path = file_path
            self.ui.pbRefreshLayers.setEnabled(True)
            self.active_layer = self.iface.activeLayer()
            self.refresh_maplayers()  # This will set the new layers to read-only

        # Initialize activate
        self.iface.layerTreeView().currentLayerChanged.connect(
            self.on_initial_selected_layer
        )

    def show_info(self, message: str, level: Qgis=Qgis.Info, duration: int=5) -> None:
        """Show message in QGIS message bar"""
        self.message_bar.pushMessage(
            "Track Changes", message, level=level, duration=duration
        )

    def activate(self) -> None:
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
            self.iface.layerTreeView().currentLayerChanged.disconnect(
                self.on_initial_selected_layer
            )
        except Exception:
            pass

        # If new layer is selected
        self.layer_selection = self.iface.layerTreeView().selectionModel()
        self.layer_selection.selectionChanged.connect(self.on_selected_layer)

        # Reconnect actions to the current active layer
        current_layer = self.iface.activeLayer()
        if (
            current_layer
            and isinstance(current_layer, QgsVectorLayer)
            and self.gpkg_path in current_layer.source()
        ):
            # Make sure to disconnect any existing handlers first
            try:
                self.disconnect_actions(current_layer)
            except Exception:
                pass

            self.active_layer = current_layer
            self.active_layer_name = (
                self.active_layer.source().split("layername=")[-1].split("|")[0]
            )
            self.connect_actions()

        self.check_timer.start()

    def connect_actions(self) -> None:
        # Actions 1*
        self.active_layer.editingStarted.connect(self.log_editing_started)
        self.active_layer.editingStopped.connect(self.log_editing_stopped)
        # Actions 2*
        self.active_layer.selectionChanged.connect(self.log_selection_changed)
        self.active_layer.featureAdded.connect(self.log_feature_added)
        self.active_layer.featureDeleted.connect(self.log_feature_deleted)
        self.active_layer.geometryChanged.connect(self.log_geometry_changed)
        self.active_layer.committedFeaturesAdded.connect(
            self.log_commited_feature_added
        )
        self.active_layer.committedFeaturesRemoved.connect(
            self.log_commited_feature_deleted
        )
        self.active_layer.committedGeometriesChanges.connect(
            self.log_commited_geometries_changes
        )
        # Action 3*
        self.active_layer.attributeAdded.connect(self.log_attribute_added)
        self.active_layer.attributeDeleted.connect(self.log_attribute_deleted)
        self.active_layer.attributeValueChanged.connect(
            self.log_attribute_value_changed
        )
        self.active_layer.committedAttributesAdded.connect(
            self.log_committed_attributes_added
        )
        self.active_layer.committedAttributesDeleted.connect(
            self.log_committed_attributes_deleted
        )
        self.active_layer.committedAttributeValuesChanges.connect(
            self.log_committed_attribute_values_changes
        )
        # Action 5*
        self.active_layer.afterCommitChanges.connect(self.log_commit_changes)

    def disconnect_actions(self, layer: QgsVectorLayer) -> None:
        # Actions 1*
        layer.editingStarted.disconnect(self.log_editing_started)
        layer.editingStopped.disconnect(self.log_editing_stopped)
        # Actions 2*
        layer.selectionChanged.disconnect(self.log_selection_changed)
        layer.featureAdded.disconnect(self.log_feature_added)
        layer.featureDeleted.disconnect(self.log_feature_deleted)
        layer.geometryChanged.disconnect(self.log_geometry_changed)
        layer.committedFeaturesAdded.disconnect(self.log_commited_feature_added)
        layer.committedFeaturesRemoved.disconnect(self.log_commited_feature_deleted)
        layer.committedGeometriesChanges.disconnect(
            self.log_commited_geometries_changes
        )
        # Action 3*
        layer.attributeAdded.disconnect(self.log_attribute_added)
        layer.attributeDeleted.disconnect(self.log_attribute_deleted)
        layer.attributeValueChanged.disconnect(self.log_attribute_value_changed)
        layer.committedAttributesAdded.disconnect(self.log_committed_attributes_added)
        layer.committedAttributesDeleted.disconnect(
            self.log_committed_attributes_deleted
        )
        layer.committedAttributeValuesChanges.disconnect(
            self.log_committed_attribute_values_changes
        )
        # Action 5*
        layer.afterCommitChanges.disconnect(self.log_commit_changes)

    def deactivate(self) -> None:
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
                QMessageBox.Save,
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
                        self.show_info(
                            f"Failed to save changes for layer: {layer.name()}",
                            level=Qgis.Warning,
                        )
                else:  # QMessageBox.Discard
                    layer.rollBack()
                    self.show_info(f"Changes discarded for layer: {layer.name()}")

        # Stop logging session
        if self.gpkg_conn is not None:
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

    def on_selected_layer(self, selected: QgsVectorLayer, deselected: QgsVectorLayer) -> None:
        """Triggered when clicking a layer in the Layers Panel"""
        # Disconnect from previous active layer if it exists
        if hasattr(self, "active_layer") and self.active_layer:
            try:
                self.disconnect_actions(self.active_layer)
            except Exception:
                pass

        selected_layers = self.iface.layerTreeView().selectedLayers()

        # Clear all highlights first
        for i in range(self.ui.listGpkgLayers.count()):
            self.ui.listGpkgLayers.item(i).setBackground(QtCore.Qt.transparent)

        for layer in selected_layers:
            if isinstance(layer, QgsVectorLayer) and self.gpkg_path in layer.source():
                self.active_layer = layer
                self.active_layer_name = (
                    self.active_layer.source().split("layername=")[-1].split("|")[0]
                )
                self.connect_actions()

                # Use default highlight color
                for i in range(self.ui.listGpkgLayers.count()):
                    item = self.ui.listGpkgLayers.item(i)
                    if item.text() == self.active_layer_name:
                        item.setBackground(self.palette().highlight())

    def on_initial_selected_layer(self, layer: QgsVectorLayer) -> None:
        # Always clear highlights first
        for i in range(self.ui.listGpkgLayers.count()):
            self.ui.listGpkgLayers.item(i).setBackground(QtCore.Qt.transparent)

        if isinstance(layer, QgsVectorLayer) and self.gpkg_path in layer.source():
            # Disconnect existing actions
            if hasattr(self, "active_layer") and self.active_layer:
                try:
                    self.disconnect_actions(self.active_layer)
                except Exception:
                    pass

            # Setup ui and active layer
            self.ui.pbActivate.setEnabled(True)
            self.active_layer = layer
            self.active_layer_name = (
                self.active_layer.source().split("layername=")[-1].split("|")[0]
            )

            # Re-connect with new actions
            self.connect_actions()

            def set_highlight_layer() -> None:
                selected_layers = self.iface.layerTreeView().selectedLayers()

                # Always clear highlights first
                for i in range(self.ui.listGpkgLayers.count()):
                    self.ui.listGpkgLayers.item(i).setBackground(QtCore.Qt.transparent)

                # Only highlight if a matching layer is found
                for lyr in selected_layers:
                    source = lyr.source()
                    if isinstance(lyr, QgsVectorLayer) and self.gpkg_path in source:
                        if "layername=" in source:
                            active_layer_name = source.split("layername=")[-1]
                        else:
                            active_layer_name = lyr.name()
                        for i in range(self.ui.listGpkgLayers.count()):
                            item = self.ui.listGpkgLayers.item(i)
                            if item.text() == active_layer_name:
                                item.setBackground(self.palette().highlight())

            # Use a small delay to ensure selection is updated
            QtCore.QTimer.singleShot(50, set_highlight_layer)
        else:
            self.ui.pbActivate.setEnabled(False)

    def create_changelog(self) -> None:
        if self.gpkg_cursor is not None:
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

            # Add changelog into extension list
            self.gpkg_cursor.execute("""
                INSERT INTO gpkg_extensions (
                    table_name, column_name, extension_name, definition, scope
                )
                SELECT 
                    'gpkg_changelog', 
                    NULL, 
                    'qgis_track_changes',
                    'https://qgis-track-changes.readthedocs.io/en/latest/api.html', 
                    'read-write'
                WHERE NOT EXISTS (
                    SELECT 1 FROM gpkg_extensions
                    WHERE table_name = 'gpkg_changelog'
                    AND column_name IS NULL
                    AND extension_name = 'qgis_track_changes'
                );
            """)

            if self.gpkg_conn is not None:
                self.gpkg_conn.commit()

    def log_editing_started(self) -> None:
        self.logging_data(10, None, "start editing", None)

    def log_editing_stopped(self) -> None:
        self.logging_data(11, None, "stop editing", None)

    def log_selection_changed(self) -> None:
        for feature in self.active_layer.selectedFeatures():
            fid = feature.id()
            feature = self.active_layer.getFeature(fid)
            properties = {}
            attributes = feature.attributes()
            for idx, field in enumerate(self.active_layer.fields()):
                properties[field.name()] = attributes[idx]
            properties["geometry"] = feature.geometry().asWkt()
            self.logging_data(20, fid, "selecting feature", json.dumps(properties))

    def log_feature_added(self, fid: int) -> None:
        feature = self.active_layer.getFeature(fid)
        properties = {}
        attributes = feature.attributes()
        for idx, field in enumerate(self.active_layer.fields()):
            properties[field.name()] = attributes[idx]
        properties["geometry"] = feature.geometry().asWkt()
        self.logging_data(21, fid, "add feature", json.dumps(properties))

    def log_feature_deleted(self, fid: int) -> None:
        self.logging_data(22, fid, "delete feature", None)

    def log_geometry_changed(self, fid: int, geometry: QgsVectorLayer) -> None:
        properties = {"new_geometry": geometry.asWkt()}
        self.logging_data(23, fid, "geometry change", json.dumps(properties))

    def log_commited_feature_added(self, lid: str, features: list[QgsFeature]) -> None:
        feature_obj = []
        for feature in features:
            properties = {}
            attributes = feature.attributes()
            for idx, field in enumerate(self.active_layer.fields()):
                properties[field.name()] = attributes[idx]
            properties["geometry"] = feature.geometry().asWkt()
            feature_obj.append(properties)
        self.logging_data(24, None, "commit add feature", json.dumps(feature_obj))

    def log_commited_feature_deleted(self, lid: str, fids: str) -> None:
        self.logging_data(25, None, "commit delete feature", fids)

    def log_commited_geometries_changes(self, lid: str, geometries: dict[str, QgsVectorLayer]) -> None:
        geoms = [
            {"fid": fid, "geometry": geom.asWkt()} for fid, geom in geometries.items()
        ]
        self.logging_data(26, None, "commit geometry change", json.dumps(geoms))

    def log_attribute_added(self, fid: int) -> None:
        field = self.active_layer.fields()[fid]
        field_object = {"name": field.name(), "type": field.displayType()}
        self.layer_table_fields[self.active_layer_name].append(field_object)
        self.logging_data(30, None, "add field", json.dumps(field_object))

    def log_attribute_deleted(self, fid: int) -> None:
        field = self.layer_table_fields[self.active_layer_name][fid]
        self.logging_data(31, None, "remove field", json.dumps(field))
        self.layer_table_fields[self.active_layer_name].pop(fid)

    def log_attribute_value_changed(self, fid: int, index: int, value: str) -> None:
        field = self.layer_table_fields[self.active_layer_name][index]
        att_object = {field["name"]: value}
        self.logging_data(32, fid, "change attribute", json.dumps(att_object))

    def log_committed_attributes_added(self, lid: str, attributes: list[QgsField]) -> None:
        table_name = lid[:-37]
        att_objects = [
            {"name": field.name(), "type": field.displayType()} for field in attributes
        ]
        self.commited_layer_table_fields[table_name].extend(att_objects)
        self.logging_data(33, None, "commit add field", json.dumps(att_objects))

    def log_committed_attributes_deleted(self, lid: str, attributes: list[QgsField]) -> None:
        table_name = lid[:-37]
        att_objects = []
        for idx in sorted(attributes, reverse=True):
            att_objects.append(self.commited_layer_table_fields[table_name][idx])
            del self.commited_layer_table_fields[table_name][idx]
        self.logging_data(34, None, "commit remove field", json.dumps(att_objects))

    def log_committed_attribute_values_changes(self, lid: str, attributes: dict[str, QgsField]) -> None:
        table_name = lid[:-37]
        att_objects = []
        for fid, values in attributes.items():
            data = {"fid": fid}
            for cid, value in values.items():
                data[self.layer_table_fields[table_name][cid]["name"]] = value
            att_objects.append(data)
        self.logging_data(35, None, "commit change attribute", json.dumps(att_objects))

    def log_commit_changes(self) -> None:
        commit_obj = json.dumps(self.detect_changes())
        self.logging_data(50, None, "commit version changes", commit_obj)

    def detect_changes(self) -> dict[str, Union[str, dict]]:
        if self.gpkg_cursor is not None:
            self.gpkg_cursor.execute("""
                SELECT data_version
                FROM gpkg_changelog
                ORDER BY id DESC 
                LIMIT 1;
            """)
            last_version = self.gpkg_cursor.fetchone()[0]
            major, minor, patch = map(int, last_version.split("."))

            self.gpkg_cursor.execute(
                """
                SELECT change_code, COUNT(change_code) AS count
                FROM gpkg_changelog
                WHERE data_version = ?
                GROUP BY change_code
            """,
                (last_version,),
            )
            change_count = {}
            for item in self.gpkg_cursor.fetchall():
                change_count[item[0]] = item[1]

            # Code changes that trigger version update
            code24 = change_count.get(24, 0) > 0
            code25 = change_count.get(25, 0) > 0
            code26 = change_count.get(26, 0) > 0
            code33 = change_count.get(33, 0) > 0
            code34 = change_count.get(34, 0) > 0
            code35 = change_count.get(35, 0) > 0

            if code25 or code34:
                new_major = major + 1
                new_version = f"{new_major}.0.0"
                message = "Major version update"
            elif code24 or code33:
                new_minor = minor + 1
                new_version = f"{major}.{new_minor}.0"
                message = "Minor version update"
            elif code26 or code35:
                new_patch = patch + 1
                new_version = f"{major}.{minor}.{new_patch}"
                message = "Patch version update"
            else:
                new_version = last_version
                message = "No version update"

            return {
                "message": message,
                "old_version": last_version,
                "new_version": new_version,
                "change_counts": change_count,
            }
        
        else:
            return {}

    def logging_data(self, change_code: int, feature_id: Optional[int], message: str, data: Optional[str]) -> None:
        if data and not isinstance(data, str):
            try:
                data = json.dumps(data)
            except (TypeError, ValueError) as e:
                self.show_info(f"Invalid data format: {str(e)}", level=Qgis.Warning)
                return

        # Ensure we have a valid connection
        if not self.gpkg_conn or not self.check_connection():
            if not self.reconnect():
                self.show_info(
                    "Cannot log changes: No active database connection",
                    level=Qgis.Warning,
                )
                return

        retry_count = 0
        while retry_count < self.max_retries:
            if self.gpkg_conn is not None:
                try:
                    # Start a transaction
                    self.gpkg_conn.execute("BEGIN")

                    # Get the latest record
                    if self.gpkg_cursor is not None:
                        self.gpkg_cursor.execute("""
                            SELECT data_version, data_version_id 
                            FROM gpkg_changelog 
                            ORDER BY id DESC 
                            LIMIT 1;
                        """)
                        latest_record = self.gpkg_cursor.fetchone()

                        # Determine data version and ID
                        if change_code == 50:
                            if isinstance(data, str):
                                try:
                                    new_object = json.loads(data)
                                    data_version = new_object["new_version"]
                                except Exception:
                                    data_version = latest_record[0] if latest_record else "0.0.0"
                            else:
                                data_version = latest_record[0] if latest_record else "0.0.0"

                            try:
                                commit_version_message = new_object["message"]
                                if commit_version_message != "No version update":
                                    data_version_id = uuid.uuid4().hex
                                else:
                                    data_version_id = latest_record[1]
                            except Exception:
                                data_version_id = uuid.uuid4().hex
                        elif latest_record is not None:
                            data_version = latest_record[0]
                            data_version_id = latest_record[1]
                        else:
                            data_version = "0.0.0"
                            data_version_id = uuid.uuid4().hex

                        # Insert the log entry
                        self.gpkg_cursor.execute(
                            """
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
                        """,
                            (
                                data_version,
                                data_version_id,
                                datetime.now(timezone.utc),
                                change_code,
                                self.author,
                                self.app_version,
                                self.active_layer_name,
                                feature_id,
                                message,
                                data,
                                get_plugin_version(),
                            ),
                        )

                    # Commit the transaction
                    self.gpkg_conn.commit()
                    return  # Success, exit the retry loop

                except sqlite3.OperationalError as e:
                    # Handle specific SQLite errors
                    if "database is locked" in str(e):
                        # Wait a bit and retry
                        QtCore.QThread.msleep(100 * (retry_count + 1))
                        retry_count += 1
                        continue
                    else:
                        self.show_info(f"Database error: {str(e)}", level=Qgis.Critical)
                        self.gpkg_conn.rollback()
                        return

                except sqlite3.Error as e:
                    self.show_info(f"Error logging changes: {str(e)}", level=Qgis.Critical)
                    self.gpkg_conn.rollback()
                    return

                except Exception as e:
                    self.show_info(f"Unexpected error: {str(e)}", level=Qgis.Critical)
                    self.gpkg_conn.rollback()
                    return

        # If we've exhausted all retries
        if self.gpkg_conn is not None:
            if retry_count >= self.max_retries:
                self.show_info(
                    "Failed to log changes after multiple attempts", level=Qgis.Critical
                )
                self.gpkg_conn.rollback()

    def check_connection(self) -> bool:
        """Check if connection is still valid"""
        if self.gpkg_conn:
            try:
                self.gpkg_conn.execute("SELECT 1")
                return True
            except sqlite3.Error:
                return False
        return False

    def reconnect(self) -> bool:
        """Attempt to reconnect if connection is lost"""
        try:
            if self.gpkg_conn:
                try:
                    self.gpkg_conn.close()
                except sqlite3.Error:
                    pass  # Ignore errors when closing a potentially broken connection
                self.gpkg_conn = None
                self.gpkg_cursor = None

            # Create a new connection with timeout
            self.gpkg_conn = sqlite3.connect(
                self.gpkg_path, timeout=self.connection_timeout
            )
            self.gpkg_cursor = self.gpkg_conn.cursor()

            # Verify the connection is working
            self.gpkg_cursor.execute("SELECT 1")
            return True
        except sqlite3.Error as e:
            self.show_info(f"Failed to reconnect: {str(e)}", level=Qgis.Critical)
            return False

    def check_connection_health(self) -> None:
        """Periodic check of connection health"""
        if not self.check_connection():
            self.show_info(
                "Connection lost, attempting to reconnect...", level=Qgis.Warning
            )
            if self.reconnect():
                self.show_info("Successfully reconnected")
            else:
                self.show_info("Failed to reconnect to database", level=Qgis.Critical)
                # Try to reinitialize the connection on next operation
                self.gpkg_conn = None
                self.gpkg_cursor = None

    def cleanup(self) -> None:
        """Clean up resources when plugin is unloaded"""
        if self.check_timer:
            self.check_timer.stop()

        # Ensure all transactions are committed or rolled back
        if self.gpkg_conn:
            try:
                # Check if there's an active transaction
                if self.gpkg_cursor is not None:
                    self.gpkg_cursor.execute("SELECT 1")
                    self.gpkg_conn.commit()
            except sqlite3.Error:
                # If there's an error, try to rollback
                try:
                    self.gpkg_conn.rollback()
                except sqlite3.Error:
                    pass

        # Close the connection
        if self.gpkg_conn:
            try:
                self.gpkg_conn.close()
            except sqlite3.Error:
                pass
            finally:
                self.gpkg_conn = None
                self.gpkg_cursor = None

    def wait_for_database(self, timeout:int=30) -> bool:
        """Wait for database to become available"""
        start_time = datetime.now()
        while (datetime.now() - start_time).seconds < timeout:
            try:
                if self.gpkg_conn is not None:
                    self.gpkg_conn.execute("SELECT 1")
                    return True
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    QtCore.QThread.msleep(100)
                    continue
                raise
        return False

    def verify_changelog_structure(self) -> bool:
        """Verify that changelog table has correct structure"""
        try:
            if self.gpkg_cursor is not None:
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
                        "id",
                        "data_version",
                        "data_version_id",
                        "timestamp",
                        "change_code",
                        "author",
                        "qgis_version",
                        "layer_name",
                        "feature_id",
                        "message",
                        "data",
                        "qgis_trackchanges_version",
                    }
                    if not required_columns.issubset(columns):
                        QgsMessageLog.logMessage(
                            "Changelog table structure is invalid",
                            "Track Changes",
                            level=Qgis.Critical,
                        )
                        return False
                return True
            
            else:
                return False

        except sqlite3.Error as e:
            QgsMessageLog.logMessage(
                f"Error verifying changelog structure: {str(e)}",
                "Track Changes",
                level=Qgis.Critical,
            )
            return False
