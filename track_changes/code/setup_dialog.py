import os
import logging
from PyQt5.QtWidgets import QDialog, QFileDialog
from qgis.gui import QgsFileWidget
from qgis.core import QgsMessageLog, Qgis, QgsProject

from ..ui.main_dialog import Ui_SetupTrackingChanges


class FeatureLogger(QDialog, Ui_SetupTrackingChanges):
    """
    Log codes
    00 = activate layer track change
    01 = deactivate layer track change

    10 = start editing
    11 = stop editing
    """
    def __init__(self):
        super().__init__()
        # UI setup
        self.ui = Ui_SetupTrackingChanges()
        self.ui.setupUi(self)
        self.ui.mQgsLogFile.setStorageMode(QgsFileWidget.SaveFile)
        self.ui.mQgsLogFile.fileChanged.connect(self.on_file_selected)

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

        # Populate the combo box with vector layers
        self.populate_vector_layers()
        self.ui.cbVectorLayers.currentIndexChanged.connect(self.on_layer_selected)

        # Initially disable buttons
        self.ui.pbActivate.setEnabled(False)
        self.ui.pbDeactivate.setEnabled(False)
        self.ui.cbVectorLayers.setEnabled(False)

        # Connect button click events
        self.ui.pbActivate.clicked.connect(self.activate_signals)
        self.ui.pbDeactivate.clicked.connect(self.deactivate_signals)

    def logger_setup(self):
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
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
            self.logger.info(f"00 | {self.author} activated the track changes of layer \"{self.layer.id()}\" using QGIS version {self.app_version}")
            # 1
            self.layer.editingStarted.connect(self.log_editing_started)
            self.layer.editingStopped.connect(self.log_editing_stopped)
            self.connected = True
            # Activate deactivate
            self.ui.pbActivate.setEnabled(False)
            self.ui.pbDeactivate.setEnabled(True)
            self.ui.cbVectorLayers.setEnabled(False)

    def deactivate_signals(self):
        """Safely disconnect logger signal"""
        # Track logging code 01
        self.logger.info(f"01 | {self.author} deactivated the track changes of layer \"{self.layer.id()}\" using QGIS version {self.app_version}")
        try:
            # 1
            self.layer.editingStarted.disconnect(self.log_editing_started)
            self.layer.editingStopped.disconnect(self.log_editing_stopped)
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
        
