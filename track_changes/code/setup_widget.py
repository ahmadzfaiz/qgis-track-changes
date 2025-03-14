import logging
from PyQt5.QtWidgets import QDockWidget
from qgis.core import QgsMessageLog, Qgis, QgsProject
from qgis.gui import QgsFileWidget

from ..ui.main_dock import Ui_SetupTrackingChanges


class FeatureLogger(QDockWidget, Ui_SetupTrackingChanges):
    """
    Log codes
    00 = activate layer track change
    01 = deactivate layer track change

    10 = start editing
    11 = stop editing

    20 = features selection
    21 = feature add
    22 = feature delete
    23 = feature geometry change
    24 = feature add committed (reserved, no feature yet)
    25 = feature delete committed (reserver, no feature yet)
    26 = features geometry change committed

    30 = attribute add
    31 = attribute delete
    32 = attribute value change
    33 = attribute add committed
    34 = attribute delete committed
    35 = attribute values change committed
    """
    def __init__(self):
        super().__init__()
        # Setup UI
        self.ui = Ui_SetupTrackingChanges()
        self.ui.setupUi(self)

        # Logger info setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.log_file = None

        self.app_version = Qgis.QGIS_VERSION
        project = QgsProject.instance()
        self.author = project.metadata().author()
        self.connected = False

        self.layer = None
        self.layer_name = None

        # Setup log file to be saved
        self.ui.mQgsLogFile.setStorageMode(QgsFileWidget.SaveFile)
        self.ui.mQgsLogFile.fileChanged.connect(self.on_file_selected)

        # Populate the combo box with vector layers
        self.populate_vector_layers()
        self.ui.cbVectorLayers.currentIndexChanged.connect(self.on_layer_selected)

        # Initially disable buttons
        self.ui.cbVectorLayers.setEnabled(False)
        self.ui.pbActivate.setEnabled(False)
        self.ui.pbDeactivate.setEnabled(False)

        # Active layer label
        self.ui.labelActive.setText("No active layer")
        self.ui.labelActive.setWordWrap(True) 

        # Connect button click events
        self.ui.pbActivate.clicked.connect(self.activate_signals)
        self.ui.pbDeactivate.clicked.connect(self.deactivate_signals)
        self.ui.pbRefreshLayers.clicked.connect(self.populate_vector_layers)

    def logger_setup(self):
        if self.logger.hasHandlers():
            for handler in self.logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.close()
            self.logger.handlers.clear() 
        
        # Set up new file handler
        file_handler = logging.FileHandler(self.log_file, mode="a")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def populate_vector_layers(self):
        """Populate the dropdown with all vector layers in the QGIS Layers Panel"""
        self.ui.cbVectorLayers.clear()
        self.ui.cbVectorLayers.addItem("Select a layer...")
        self.ui.cbVectorLayers.model().item(0).setEnabled(False)
        layers = QgsProject.instance().mapLayers().values()
        
        for layer in layers:
            if layer.type() == layer.VectorLayer:
                self.ui.cbVectorLayers.addItem(layer.name(), layer)

    def on_file_selected(self, file_path):
        if file_path:
            self.ui.cbVectorLayers.setEnabled(True)
            if not file_path.lower().endswith(".log"):
                file_path += ".log"
            self.ui.mQgsLogFile.setFilePath(file_path)
            self.log_file = file_path
            self.logger_setup()

            # Add developer log message
            QgsMessageLog.logMessage(
                f"Saved log file: {file_path}",
                "Track Changes", 
                level=Qgis.Info
            )

    def on_layer_selected(self, index):
        """ Selecting layer to track the change """
        if index >= 1:
            select_layer = True
            self.layer = self.ui.cbVectorLayers.itemData(index)
            self.layer_name = self.ui.cbVectorLayers.currentText()
            
            QgsMessageLog.logMessage(
                f"Selected Layer: {self.layer_name}",
                "Track Changes", 
                level=Qgis.Info
            )
            
            if select_layer:
                self.ui.pbActivate.setEnabled(True)

            # Add field after file is selected
            try:
                self.fields = [field.name() for field in self.layer.fields()]
                self.committed_fields = [field.name() for field in self.layer.fields()]
            except:
                pass

    def activate_signals(self):
        """Safely connect logger signals"""
        self.ui.labelActive.setText(self.layer.name())
        if self.connected:
            return
        
        if self.layer_name:
            # Track logging code 00
            self.logger.info(f"00 | {self.author} activated the track changes of layer \"{self.layer.id()}\" using QGIS version {self.app_version}")
            # 1
            self.layer.editingStarted.connect(self.log_editing_started)
            self.layer.editingStopped.connect(self.log_editing_stopped)
            # 2
            self.layer.selectionChanged.connect(self.log_selection_changed)
            self.layer.featureAdded.connect(self.log_feature_added)
            self.layer.featureDeleted.connect(self.log_feature_deleted)
            self.layer.geometryChanged.connect(self.log_geometry_changed)
            self.layer.committedGeometriesChanges.connect(self.log_commited_geometries_changes)
            # 3
            self.layer.attributeAdded.connect(self.log_attribute_added)
            self.layer.attributeDeleted.connect(self.log_attribute_deleted)
            self.layer.attributeValueChanged.connect(self.log_attribute_value_changed)
            self.layer.committedAttributesAdded.connect(self.log_committed_attributes_added)
            self.layer.committedAttributesDeleted.connect(self.log_committed_attributes_deleted)
            self.layer.committedAttributeValuesChanges.connect(self.log_committed_attribute_values_changes)
            self.connected = True
            # Activate deactivate
            self.ui.pbActivate.setEnabled(False)
            self.ui.pbDeactivate.setEnabled(True)
            self.ui.cbVectorLayers.setEnabled(False)

    def deactivate_signals(self):
        """Safely disconnect logger signal"""
        self.ui.labelActive.setText("No active layer")
        # Track logging code 01
        self.logger.info(f"01 | {self.author} deactivated the track changes of layer \"{self.layer.id()}\" using QGIS version {self.app_version}")
        try:
            # 1
            self.layer.editingStarted.disconnect(self.log_editing_started)
            self.layer.editingStopped.disconnect(self.log_editing_stopped)
            # 2
            self.layer.selectionChanged.disconnect(self.log_selection_changed)
            self.layer.featureAdded.disconnect(self.log_feature_added)
            self.layer.featureDeleted.disconnect(self.log_feature_deleted)
            self.layer.geometryChanged.disconnect(self.log_geometry_changed)
            self.layer.committedGeometriesChanges.disconnect(self.log_commited_geometries_changes)
            # 3
            self.layer.attributeAdded.disconnect(self.log_attribute_added)
            self.layer.attributeDeleted.disconnect(self.log_attribute_deleted)
            self.layer.attributeValueChanged.disconnect(self.log_attribute_value_changed)
            self.layer.committedAttributesAdded.disconnect(self.log_committed_attributes_added)
            self.layer.committedAttributesDeleted.disconnect(self.log_committed_attributes_deleted)
            self.layer.committedAttributeValuesChanges.disconnect(self.log_committed_attribute_values_changes)
        except TypeError:
            pass
        self.connected = False
        # Activate deactivate
        self.ui.pbActivate.setEnabled(True)
        self.ui.pbDeactivate.setEnabled(False)
        self.ui.cbVectorLayers.setEnabled(True)

    def log_editing_started(self):
        self.logger.info(f"10 | {self.author} started editing of layer \"{self.layer.id()}\"") 

    def log_editing_stopped(self):
        self.logger.info(f"11 | {self.author} stopped editing of layer \"{self.layer.id()}\"")

    def log_selection_changed(self):
        for feature in self.layer.selectedFeatures():
            fid = feature.id()
            feature = self.layer.getFeature(fid)
            properties = {}
            attributes = feature.attributes()
            for idx, field in enumerate(self.layer.fields()):
                properties[field.name()] = attributes[idx]
            properties["geometry"] = feature.geometry().asWkt()
            self.logger.info(f"20 | {self.author} selecting feature. Layer ID: {self.layer.id()}. Feature ID: {fid}. Properties: {properties}")

    def log_feature_added(self, fid):
        feature = self.layer.getFeature(fid)
        properties = {}
        attributes = feature.attributes()
        for idx, field in enumerate(self.layer.fields()):
            properties[field.name()] = attributes[idx]
        properties["geometry"] = feature.geometry().asWkt()
        self.logger.info(f"21 | {self.author} added feature. Layer ID: {self.layer.id()}. Feature ID: {fid}. Properties: {properties}")
        
    def log_feature_deleted(self, fid):
        self.logger.info(f"22 | {self.author} deleted feature. Layer ID: {self.layer.id()}. Feature ID: {fid}")

    def log_geometry_changed(self, fid, geometry):
        new_geometry = geometry.asWkt()
        self.logger.info(f"23 | {self.author} changed geometry. Layer ID: {self.layer.id()}. Feature ID: {fid}. New geometry: {new_geometry}")
        
    def log_commited_geometries_changes(self, lid, geometries):
        self.logger.info(f"26 | Geometries changes by {self.author} is committed. Layer ID: {lid}")
        for fid, geometry in geometries.items():
            self.logger.info(f"26 | Committed changed geometry. Layer ID: {self.layer.id()}. Feature ID: {fid}. New geometry: {geometry.asWkt()}")

    def log_attribute_added(self, fid):
        field_name = self.layer.fields()[fid].name()
        self.fields.insert(fid, field_name)
        self.logger.info(f"30 | {self.author} added attribute. Layer ID: {self.layer.id()}. Field name: {field_name}")
        
    def log_attribute_deleted(self, fid):
        field_name = self.fields[fid]
        self.fields.pop(fid)
        self.logger.info(f"31 | {self.author} deleted attribute. Layer ID: {self.layer.id()}. Field name: {field_name}")
        
    def log_attribute_value_changed(self, fid, index, value):
        field_name = self.fields[index]
        self.logger.info(f"32 | {self.author} changed attribute. Layer ID: {self.layer.id()}. Feature ID: {fid}. Field name: {field_name}. Field content: {value}")
        
    def log_committed_attributes_added(self, lid, attributes):
        self.logger.info(f"33 | Attributes added by {self.author} is committed. Layer ID: {lid}")
        for attribute in attributes:
            att_name = attribute.name()
            att_index = self.layer.fields().indexFromName(att_name)
            att_type = attribute.displayType()
            self.logger.info(f"33 | Committed added attribute. Layer ID: {lid}. New field: {att_name}. Field type: {att_type}")
            self.committed_fields.insert(att_index, att_name)
            
    def log_committed_attributes_deleted(self, lid, attributes):
        self.logger.info(f"34 | Attributes deleted by {self.author} is committed. Layer ID: {lid}")
        for attribute in attributes:
            att_name = self.committed_fields[attribute]
            self.logger.info(f"33 | Committed added attribute. Layer ID: {lid}. Remove field: {att_name}")
            self.committed_fields.pop(attribute)
    
    def log_committed_attribute_values_changes(self, lid, attributes):
        self.logger.info(f"35 | Attributes changes by {self.author} is committed. Layer ID: {lid}")
        for fid, values in attributes.items():
            for cid, value in values.items():
                field_name = self.fields[cid]
                self.logger.info(f"35 | Committed changed attribute. Layer ID: {self.layer.id()}. Feature ID: {fid}. Field name: {field_name}. Field content: {value}")
