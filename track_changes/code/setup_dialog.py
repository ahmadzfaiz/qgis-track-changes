import os
import logging
from PyQt5.QtWidgets import QDialog
from qgis.core import QgsMessageLog, Qgis, QgsProject

from ..ui.main_dialog import Ui_SetupTrackingChanges


log_file_name = "test"
log_file_directory = "/Users/ahmadzaenunfaiz/Desktop/logs"

class FeatureLogger(QDialog, Ui_SetupTrackingChanges):
    def __init__(self):
        super().__init__()
        # UI setup
        self.ui = Ui_SetupTrackingChanges()
        self.ui.setupUi(self)

        # Logger info setup
        self.app_version = Qgis.QGIS_VERSION
        project = QgsProject.instance()
        self.author = project.metadata().author()
        self.connected = False

        self.layer = None
        self.layer_name = None

        log_file_path = os.path.join(log_file_directory, f"{log_file_name}.log")
        logging.basicConfig(
            filename=log_file_path,
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.DEBUG,
        )

        # Populate the combo box with vector layers
        self.populate_vector_layers()
        self.ui.cbVectorLayers.currentIndexChanged.connect(self.on_layer_selected)

        # Initially disable both buttons
        self.ui.pbActivate.setEnabled(False)
        self.ui.pbDeactivate.setEnabled(False)

        # Connect button click events
        self.ui.pbActivate.clicked.connect(self.activate_signals)
        self.ui.pbDeactivate.clicked.connect(self.deactivate_signals)

    def populate_vector_layers(self):
        """Populate the dropdown with all vector layers in the QGIS Layers Panel"""
        self.ui.cbVectorLayers.clear()
        self.ui.cbVectorLayers.addItem("Select a layer...")
        self.ui.cbVectorLayers.model().item(0).setEnabled(False)
        layers = QgsProject.instance().mapLayers().values()
        
        for layer in layers:
            if layer.type() == layer.VectorLayer:
                self.ui.cbVectorLayers.addItem(layer.name(), layer)

    def on_layer_selected(self, index):
        """ Selecting layer to track the change """
        if index >= 0:
            self.layer_name = self.ui.cbVectorLayers.currentText()
            self.layer = self.ui.cbVectorLayers.itemData(index)
            
            QgsMessageLog.logMessage(
                f"Selected Layer: {self.layer_name}",
                "Track Changes", 
                level=Qgis.Info
            )
            
            if (
                not self.ui.pbActivate.isEnabled() 
                and not self.ui.pbDeactivate.isEnabled()
            ):
                self.ui.pbActivate.setEnabled(True)

    def activate_signals(self):
        """Safely connect logger signals"""
        if self.connected:
            return
        
        if self.layer_name:
            # Track logging code 00
            logging.info(f"00 | {self.author} activated the track changes of layer \"{self.layer.id()}\" using QGIS version {self.app_version}")
            self.connected = True
            # Activate deactivate
            self.ui.pbActivate.setEnabled(False)
            self.ui.pbDeactivate.setEnabled(True)
            self.ui.cbVectorLayers.setEnabled(False)

    def deactivate_signals(self):
        """Safely disconnect logger signal"""
        # Track logging code 01
        logging.info(f"01 | {self.author} deactivated the track changes of layer \"{self.layer.id()}\" using QGIS version {self.app_version}")
        self.connected = False
        # Activate deactivate
        self.ui.pbActivate.setEnabled(True)
        self.ui.pbDeactivate.setEnabled(False)
        self.ui.cbVectorLayers.setEnabled(True)

